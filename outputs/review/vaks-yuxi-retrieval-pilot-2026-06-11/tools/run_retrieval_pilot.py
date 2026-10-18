import argparse
import csv
import hashlib
import json
import math
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# tools/run_retrieval_pilot.py -> pilot dir -> outputs/review -> outputs -> repo root
ROOT = Path(__file__).resolve().parents[4]
PILOT_DIR = Path(__file__).resolve().parents[1]


PRIMARY_FILES = [
    "README.md",
    "SCHEMA.md",
    "SOURCE_INTAKE.md",
    "REVIEW_QUEUE.md",
    "FEEDBACK.md",
    "DEV_CONTEXT.md",
    "MEMORY_TIER.md",
    "FUSION_ARCHITECTURE_V0_2_DRAFT.md",
    "ARCHITECTURE_PRINCIPLES.md",
    "IMPLEMENTATION_BLUEPRINT.md",
    "SECOND_BRAIN_MODEL.md",
]

PRIMARY_DIRS = [
    "wiki",
    "raw",
    "outputs/qa",
    "outputs/review/project_lens_overlays",
    "outputs/review/vaks-retrieval-layer-design-2026-06-11",
]

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")
CJK_RE = re.compile(r"[\u4e00-\u9fff]+")
WORD_RE = re.compile(r"[a-zA-Z0-9_./:-]{2,}")


@dataclass
class Chunk:
    chunk_id: str
    path: str
    heading: str
    text: str
    status: str
    bucket: str
    action_basis_allowed: bool
    links: list


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def infer_status(path: str, fm: dict) -> tuple[str, str, bool]:
    explicit = (fm.get("knowledge_status") or fm.get("status") or "").lower()
    action_raw = (fm.get("action_basis_allowed") or "").lower()

    if "action_basis_allowed" in fm:
        action = action_raw == "true"
    else:
        action = False

    p = path.replace("\\", "/")
    if explicit in {"reviewed", "active", "adopted"} and p.startswith("wiki/"):
        return "reviewed", "reviewed", action
    if p.startswith("raw/"):
        return "raw", "raw", False
    if "project_lens_overlays" in p or "project_overlays" in p:
        return "candidate", "overlay", False
    if p.startswith("outputs/review/"):
        return "candidate", "candidate", False
    if p.startswith("outputs/qa/"):
        return "candidate", "qa", False
    if p.startswith("wiki/summaries/"):
        return "candidate", "summary", False
    if p.startswith("wiki/"):
        return "reviewed", "reviewed", action
    if explicit:
        return explicit, explicit, action
    return "unknown", "unknown", action


def iter_markdown_files(corpus: str) -> list[Path]:
    files = []
    if corpus == "full":
        files = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
    else:
        for rel in PRIMARY_FILES:
            p = ROOT / rel
            if p.exists():
                files.append(p)
        for rel in PRIMARY_DIRS:
            d = ROOT / rel
            if d.exists():
                files.extend(d.rglob("*.md"))
        review_dir = ROOT / "outputs/review"
        if review_dir.exists():
            files.extend(review_dir.glob("2026-06-11-*.md"))

    seen = {}
    for p in files:
        try:
            rel = p.relative_to(ROOT).as_posix()
        except ValueError:
            continue
        if any(part in {".git", "node_modules"} for part in p.parts):
            continue
        seen[rel] = p
    return [seen[k] for k in sorted(seen)]


def split_chunks(path: Path, rel: str, text: str, fm: dict) -> list[tuple[str, str]]:
    clean = FRONTMATTER_RE.sub("", text, count=1)
    matches = list(HEADING_RE.finditer(clean))
    if not matches:
        return [(Path(rel).name, clean[:5000])]

    chunks = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(clean)
        heading = m.group(2).strip()
        body = clean[start:end].strip()
        if not body:
            continue
        if len(body) <= 2500:
            chunks.append((heading, body))
            continue
        paras = re.split(r"\n\s*\n", body)
        buf = ""
        part = 1
        for para in paras:
            if len(buf) + len(para) > 2200 and buf:
                chunks.append((f"{heading} / part {part}", buf.strip()))
                part += 1
                buf = para
            else:
                buf = f"{buf}\n\n{para}" if buf else para
        if buf.strip():
            chunks.append((f"{heading} / part {part}", buf.strip()))
    return chunks


def tokenize(text: str) -> list[str]:
    lowered = text.lower()
    tokens = WORD_RE.findall(lowered)
    for seq in CJK_RE.findall(text):
        tokens.extend(list(seq))
        tokens.extend(seq[i : i + 2] for i in range(max(0, len(seq) - 1)))
    return tokens


def build_chunks(corpus: str) -> list[Chunk]:
    chunks = []
    for file_path in iter_markdown_files(corpus):
        rel = file_path.relative_to(ROOT).as_posix()
        text = read_text(file_path)
        fm = parse_frontmatter(text)
        status, bucket, action = infer_status(rel, fm)
        links = sorted(set(WIKILINK_RE.findall(text)))
        for heading, body in split_chunks(file_path, rel, text, fm):
            cid = f"c{len(chunks):06d}"
            full_text = f"{rel}\n{heading}\n{body}"
            chunks.append(Chunk(cid, rel, heading, full_text, status, bucket, action, links))
    return chunks


def bm25_scores(query: str, docs: list[str]) -> np.ndarray:
    tokenized_docs = [tokenize(d) for d in docs]
    q_tokens = tokenize(query)
    if not q_tokens:
        return np.zeros(len(docs))
    df = Counter()
    for toks in tokenized_docs:
        for t in set(toks):
            df[t] += 1
    avgdl = sum(len(t) for t in tokenized_docs) / max(1, len(tokenized_docs))
    scores = []
    k1 = 1.5
    b = 0.75
    n = len(tokenized_docs)
    for toks in tokenized_docs:
        tf = Counter(toks)
        dl = len(toks)
        score = 0.0
        for term in q_tokens:
            if tf[term] == 0:
                continue
            idf = math.log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
            denom = tf[term] + k1 * (1 - b + b * dl / max(1, avgdl))
            score += idf * (tf[term] * (k1 + 1)) / denom
        scores.append(score)
    return np.array(scores, dtype=float)


def rrf(rankings: list[list[int]], k: int = 60) -> dict[int, float]:
    scores = defaultdict(float)
    for ranking in rankings:
        for rank, idx in enumerate(ranking, start=1):
            scores[idx] += 1.0 / (k + rank)
    return dict(scores)


def graph_boost(query: str, chunks: list[Chunk]) -> list[int]:
    q = query.lower()
    hits = []
    for i, ch in enumerate(chunks):
        link_blob = " ".join(ch.links).lower()
        path_heading = f"{ch.path} {ch.heading}".lower()
        score = 0
        for token in tokenize(q):
            if len(token) < 3:
                continue
            if token in link_blob:
                score += 2
            if token in path_heading:
                score += 1
        if score:
            hits.append((score, i))
    hits.sort(reverse=True)
    return [i for _, i in hits[:50]]


def warning_for(chunk: Chunk, intent: str) -> str:
    if intent in {"action", "evidence"} and not chunk.action_basis_allowed:
        return "not_action_basis"
    if chunk.bucket in {"raw", "candidate", "overlay", "summary", "qa"}:
        return f"{chunk.bucket}_is_activation_only"
    return ""


def expected_hit(results: list[dict], expected: list[str], topn: int) -> bool:
    needles = [e.lower() for e in expected]
    for row in results[:topn]:
        hay = f"{row['path']} {row['heading']} {row.get('snippet','')}".lower()
        if any(n in hay for n in needles):
            return True
    return False


def run_queries(chunks: list[Chunk], query_cases: list[dict], out_dir: Path, corpus: str):
    docs = [c.text for c in chunks]

    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=1, max_features=80000)
    matrix = vectorizer.fit_transform(docs)

    # T0 is file-level lexical baseline.
    file_texts = defaultdict(str)
    file_meta = {}
    for ch in chunks:
        file_texts[ch.path] += "\n" + ch.text
        file_meta[ch.path] = ch
    file_paths = sorted(file_texts)
    file_docs = [file_texts[p] for p in file_paths]

    rows = []
    top_results = {}

    for case in query_cases:
        qid = case["id"]
        query = case["query"]
        expected = case.get("expected", [])
        intent = case.get("intent", "exploration")

        # T0
        file_scores = bm25_scores(query, file_docs)
        file_order = list(np.argsort(-file_scores)[:10])
        t0 = []
        for rank, idx in enumerate(file_order, start=1):
            p = file_paths[idx]
            meta = file_meta[p]
            t0.append({
                "mode": "T0_baseline_file_lexical",
                "rank": rank,
                "path": p,
                "heading": Path(p).name,
                "score": float(file_scores[idx]),
                "status": meta.status,
                "bucket": meta.bucket,
                "action_basis_allowed": meta.action_basis_allowed,
                "warning": "",
                "snippet": file_docs[idx][:220].replace("\n", " "),
            })

        # T1/T2
        bm25 = bm25_scores(query, docs)
        bm25_order = list(np.argsort(-bm25)[:80])
        qv = vectorizer.transform([query])
        dense_scores = cosine_similarity(qv, matrix).ravel()
        dense_order = list(np.argsort(-dense_scores)[:80])
        graph_order = graph_boost(query, chunks)
        fused = rrf([bm25_order, dense_order, graph_order])
        order = [idx for idx, _ in sorted(fused.items(), key=lambda kv: kv[1], reverse=True)[:10]]

        t1 = []
        t2 = []
        for rank, idx in enumerate(order, start=1):
            ch = chunks[idx]
            base = {
                "rank": rank,
                "path": ch.path,
                "heading": ch.heading,
                "score": float(fused[idx]),
                "status": ch.status,
                "bucket": ch.bucket,
                "action_basis_allowed": ch.action_basis_allowed,
                "snippet": ch.text[:220].replace("\n", " "),
            }
            t1.append({"mode": "T1_yuxi_like_no_labels", **base, "warning": ""})
            t2.append({"mode": "T2_yuxi_like_boundary_labels", **base, "warning": warning_for(ch, intent)})

        for mode_rows in [t0, t1, t2]:
            mode = mode_rows[0]["mode"]
            hit5 = expected_hit(mode_rows, expected, 5)
            hit10 = expected_hit(mode_rows, expected, 10)
            top1 = mode_rows[0]
            top5 = mode_rows[:5]
            top5_warning_count = sum(1 for r in top5 if r.get("warning"))
            top5_nonreviewed_count = sum(1 for r in top5 if r["bucket"] != "reviewed")
            rows.append({
                "corpus": corpus,
                "query_id": qid,
                "intent": intent,
                "mode": mode,
                "hit_at_5": hit5,
                "hit_at_10": hit10,
                "top1_path": top1["path"],
                "top1_heading": top1["heading"],
                "top1_bucket": top1["bucket"],
                "top1_status": top1["status"],
                "candidate_or_raw_top1": top1["bucket"] != "reviewed",
                "top5_nonreviewed_count": top5_nonreviewed_count,
                "top5_warning_count": top5_warning_count,
                "warning_emitted": top5_warning_count > 0,
                "needs_boundary_warning": bool(case.get("needs_boundary_warning")),
            })
            top_results[f"{corpus}:{qid}:{mode}"] = mode_rows

    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / f"results-{corpus}.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    with (out_dir / f"top-results-{corpus}.json").open("w", encoding="utf-8") as f:
        json.dump(top_results, f, ensure_ascii=False, indent=2)
    return rows


def summarize(rows: list[dict], chunks: list[Chunk], corpus: str, out_dir: Path):
    by_mode = defaultdict(list)
    for row in rows:
        by_mode[row["mode"]].append(row)

    lines = []
    lines.append(f"# Retrieval Pilot Summary: {corpus}\n")
    lines.append("## Corpus\n")
    lines.append(f"- chunks indexed: {len(chunks)}")
    lines.append(f"- files indexed: {len(set(c.path for c in chunks))}")
    lines.append(f"- corpus hash: `{sha256_text('|'.join(sorted(set(c.path for c in chunks))))[:16]}`\n")
    lines.append("## Metrics\n")
    lines.append("| Mode | hit@5 | hit@10 | candidate/raw top1 | warning when needed |")
    lines.append("|---|---:|---:|---:|---:|")
    for mode, items in by_mode.items():
        total = len(items)
        hit5 = sum(1 for r in items if r["hit_at_5"] == True or r["hit_at_5"] == "True")
        hit10 = sum(1 for r in items if r["hit_at_10"] == True or r["hit_at_10"] == "True")
        cr = sum(1 for r in items if r["candidate_or_raw_top1"] == True or r["candidate_or_raw_top1"] == "True")
        needed = [r for r in items if r["needs_boundary_warning"] == True or r["needs_boundary_warning"] == "True"]
        warn = sum(1 for r in needed if r["warning_emitted"] == True or r["warning_emitted"] == "True")
        warn_den = len(needed) or 1
        lines.append(f"| {mode} | {hit5}/{total} | {hit10}/{total} | {cr}/{total} | {warn}/{warn_den} |")

    lines.append("\n## Provisional Interpretation\n")
    t0 = by_mode.get("T0_baseline_file_lexical", [])
    t1 = by_mode.get("T1_yuxi_like_no_labels", [])
    t2 = by_mode.get("T2_yuxi_like_boundary_labels", [])
    t0_hit = sum(1 for r in t0 if r["hit_at_5"] == True or r["hit_at_5"] == "True")
    t1_hit = sum(1 for r in t1 if r["hit_at_5"] == True or r["hit_at_5"] == "True")
    t2_warn = sum(1 for r in t2 if (r["needs_boundary_warning"] == True or r["needs_boundary_warning"] == "True") and (r["warning_emitted"] == True or r["warning_emitted"] == "True"))
    needed = sum(1 for r in t2 if r["needs_boundary_warning"] == True or r["needs_boundary_warning"] == "True")
    if t1_hit > t0_hit:
        lines.append("- Yuxi-like retrieval improved expected-source hit@5 over the baseline.")
    elif t1_hit == t0_hit:
        lines.append("- Yuxi-like retrieval matched the baseline hit@5; inspect anchor quality before claiming value.")
    else:
        lines.append("- Yuxi-like retrieval underperformed the baseline hit@5; do not adopt without redesign.")
    lines.append(f"- Boundary-label mode emitted warnings for {t2_warn}/{needed} warning-needed cases.")
    lines.append("- This is a local simulation, not proof that Yuxi production deployment will behave identically.")

    (out_dir / f"summary-{corpus}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_queries() -> list[dict]:
    path = PILOT_DIR / "queries.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", choices=["primary", "full"], default="primary")
    args = parser.parse_args()

    out_dir = PILOT_DIR / "results"
    chunks = build_chunks(args.corpus)
    queries = load_queries()
    rows = run_queries(chunks, queries, out_dir, args.corpus)
    summarize(rows, chunks, args.corpus, out_dir)

    print(json.dumps({
        "corpus": args.corpus,
        "files": len(set(c.path for c in chunks)),
        "chunks": len(chunks),
        "queries": len(queries),
        "results_dir": str(out_dir.relative_to(ROOT)),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
