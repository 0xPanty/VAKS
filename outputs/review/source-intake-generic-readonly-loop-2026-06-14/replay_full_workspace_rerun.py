#!/usr/bin/env python
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "frozen_full_workspace_corpus"
QUERY_MANIFEST = ROOT / "results" / "full_workspace_query_manifest.json"
OUT = ROOT / "results" / "full_workspace_replay_check.json"
TOKEN_RE = re.compile(r"[a-z0-9]+|[\u4e00-\u9fff]+", re.IGNORECASE)

TYPE_ALIASES = {
    "source": "source_card",
    "source_record": "source_card",
    "video_source_card": "source_card",
    "source_snapshot_index": "source_card",
    "source_annotation": "source_annotation",
    "candidate_distillation": "candidate_distillation",
    "candidate_distillation_refresh": "candidate_distillation",
    "project_lens_overlay": "project_overlay",
    "project_overlay": "project_overlay",
}

def tokenize(text: str) -> list[str]:
    raw = TOKEN_RE.findall(text.lower())
    expanded = []
    for token in raw:
        expanded.append(token)
        if "-" in token or "_" in token:
            expanded.extend(t for t in re.split(r"[-_]+", token) if t)
    return [t for t in expanded if len(t) > 1]

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

def infer_record_kind(path: str, fm: dict) -> str:
    if fm.get("record_kind"):
        return TYPE_ALIASES.get(str(fm["record_kind"]), str(fm["record_kind"]))
    if fm.get("type") in TYPE_ALIASES:
        return TYPE_ALIASES[str(fm["type"])]
    if path.startswith("raw/"):
        return "source_card"
    if path.startswith("outputs/review/source_annotations/") or path.endswith("source-annotation.md"):
        return "source_annotation"
    if path.startswith("wiki/") and str(fm.get("status", "")).lower() == "reviewed":
        return "reviewed_material"
    if path.endswith("candidate-distillation.md") or path.endswith("refresh.md"):
        return "candidate_distillation"
    if "project_lens_overlays/" in path or "project_overlays/" in path or path.endswith("-overlay.md"):
        return "project_overlay"
    return "source_card"

def infer_status(record_kind: str, fm: dict) -> str:
    if fm.get("knowledge_status"):
        return str(fm["knowledge_status"])
    if str(fm.get("status", "")).lower() == "reviewed":
        return "reviewed"
    if record_kind == "source_card":
        return "raw"
    return "candidate"

def authority_bucket(record_kind: str, knowledge_status: str) -> str:
    if knowledge_status == "reviewed" or record_kind == "reviewed_material":
        return "reviewed"
    if record_kind == "source_card":
        return "raw_anchor"
    if record_kind == "source_annotation":
        return "source_annotation"
    if record_kind == "candidate_distillation":
        return "candidate"
    if record_kind == "project_overlay":
        return "overlay"
    if record_kind == "feedback_event":
        return "feedback"
    return "unknown"

def headings(body: str) -> str:
    return "\n".join(line for line in body.splitlines() if line.lstrip().startswith("#"))

def score(query: str, rel_path: str, title: str, body: str, record_kind: str) -> float:
    terms = set(tokenize(query))
    path_tokens = Counter(tokenize(rel_path))
    title_tokens = Counter(tokenize(title))
    heading_tokens = Counter(tokenize(headings(body)))
    body_tokens = Counter(tokenize(body[:20000]))
    total = 0.0
    for term in terms:
        total += path_tokens.get(term, 0) * 6.0
        total += title_tokens.get(term, 0) * 4.0
        total += heading_tokens.get(term, 0) * 2.5
        total += min(body_tokens.get(term, 0), 6) * 1.0
    if record_kind == "source_card" and "source" in terms:
        total += 1.5
    if record_kind == "source_annotation" and ("annotation" in terms or "anchor" in terms or "source" in terms):
        total += 3.0
    if record_kind == "candidate_distillation" and "candidate" in terms:
        total += 4.0
    if record_kind == "project_overlay" and "overlay" in terms:
        total += 4.0
    return total

def main() -> int:
    manifest = json.loads(QUERY_MANIFEST.read_text(encoding="utf-8"))
    docs = []
    for path in sorted(CORPUS.rglob("*.md")):
        rel = path.relative_to(CORPUS).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body = split_frontmatter(text)
        kind = infer_record_kind(rel, fm)
        status = infer_status(kind, fm)
        docs.append({
            "path": rel,
            "title": str(fm.get("title") or path.stem),
            "body": body,
            "kind": kind,
            "status": status,
            "authority_bucket": authority_bucket(kind, status),
        })
    checks = []
    for query in manifest["queries"]:
        policy = query.get("query_policy") or {}
        allowed_buckets = set(policy.get("allowed_authority_buckets") or [])
        candidate_docs = [
            doc for doc in docs if not allowed_buckets or doc["authority_bucket"] in allowed_buckets
        ]
        ranked = []
        for doc in candidate_docs:
            s = score(query["query"], doc["path"], doc["title"], doc["body"], doc["kind"])
            if s > 0:
                ranked.append((s, doc["path"]))
        ranked.sort(key=lambda item: (-item[0], item[1]))
        expected = query["expected_top_paths"]
        actual = [path for _, path in ranked[: len(expected)]]
        checks.append({"case_id": query["case_id"], "expected": expected, "actual": actual, "match": actual == expected})
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
