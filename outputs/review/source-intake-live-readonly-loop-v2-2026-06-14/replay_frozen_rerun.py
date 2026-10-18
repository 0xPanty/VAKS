#!/usr/bin/env python
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "frozen_corpus"
MANIFEST = ROOT / "results" / "frozen_query_manifest.json"
OUT = ROOT / "results" / "frozen_replay_check.json"
TOKEN_RE = re.compile(r"[a-z0-9]+|[\u4e00-\u9fff]+", re.IGNORECASE)

def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if len(t) > 1]

def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    try:
        data = yaml.safe_load(text[4:end]) or {}
    except Exception:
        data = {}
    return data if isinstance(data, dict) else {}, text[end + 4 :]

def infer_kind(path: str, fm: dict) -> str:
    if fm.get("record_kind"):
        return str(fm["record_kind"])
    if path.startswith("raw/"):
        return "source_card"
    if path.startswith("outputs/review/source_annotations/") or path.endswith("source-annotation.md"):
        return "source_annotation"
    if path.endswith("candidate-distillation.md"):
        return "candidate_distillation"
    if "project_lens_overlays/" in path or path.endswith("-overlay.md"):
        return "project_overlay"
    return "source_card"

def headings(body: str) -> str:
    return "\n".join(line for line in body.splitlines() if line.lstrip().startswith("#"))

def score(query: str, rel_path: str, text: str, title: str) -> float:
    terms = set(tokenize(query))
    path_tokens = Counter(tokenize(rel_path))
    title_tokens = Counter(tokenize(title))
    heading_tokens = Counter(tokenize(headings(text)))
    body_tokens = Counter(tokenize(text[:20000]))
    total = 0.0
    for term in terms:
        total += path_tokens.get(term, 0) * 6.0
        total += title_tokens.get(term, 0) * 4.0
        total += heading_tokens.get(term, 0) * 2.5
        total += min(body_tokens.get(term, 0), 6) * 1.0
    kind = infer_kind(rel_path, {})
    if kind == "source_card" and "source" in terms:
        total += 1.5
    if kind == "candidate_distillation" and "candidate" in terms:
        total += 4.0
    return total

def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    docs = []
    for path in sorted(CORPUS.rglob("*.md")):
        rel = path.relative_to(CORPUS).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body = split_frontmatter(text)
        docs.append({"path": rel, "title": str(fm.get("title") or path.stem), "text": body, "kind": infer_kind(rel, fm)})
    checks = []
    for query in manifest["queries"]:
        ranked = []
        for doc in docs:
            s = score(query["query"], doc["path"], doc["text"], doc["title"])
            if s > 0:
                ranked.append((s, doc["path"]))
        ranked.sort(key=lambda item: (-item[0], item[1]))
        actual = [path for _, path in ranked[: len(query["expected_top_paths"])]]
        expected = query["expected_top_paths"]
        checks.append({
            "case_id": query["case_id"],
            "expected": expected,
            "actual": actual,
            "match": set(actual) == set(expected),
            "match_kind": "top_k_membership_not_exact_order",
        })
    result = {
        "status": "pass" if all(check["match"] for check in checks) else "fail",
        "frozen_scope": manifest["frozen_scope"],
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "pass" else 1

if __name__ == "__main__":
    raise SystemExit(main())
