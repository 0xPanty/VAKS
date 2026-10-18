import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import run_phase_b_pressure as harness


RESULTS_DIR = harness.RESULTS_DIR
DEFAULT_STALE_PATHS = {"SCHEMA.md", "SOURCE_INTAKE.md", "FEEDBACK.md"}
SKELETON_MODE = "vaks_b_adapter_skeleton"
SELECTOR_RE = re.compile(r"^L(?P<start>\d+)-L(?P<end>\d+)$")


class VaksPhaseBAdapter:
    def __init__(self, corpus: str, stale_paths: set[str] | None = None, indexed_at: str | None = None):
        self.corpus = corpus
        self.index = harness.CorpusIndex(corpus, stale_paths=stale_paths or DEFAULT_STALE_PATHS)
        self.indexed_at = indexed_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        self.indexed_source_hash_by_chunk = {chunk.chunk_hash: chunk.indexed_source_hash for chunk in self.index.chunks}

    def chunk_manifest_rows(self):
        for chunk in self.index.chunks:
            selector = normalize_selector(chunk.path, chunk.selector_or_line_range)
            yield {
                "artifact_kind": "vaks_phase_b_chunk_manifest",
                "corpus": self.corpus,
                "vaks_record_id": f"{self.corpus}:{chunk.chunk_id}",
                "vault_path": chunk.path,
                "heading_or_anchor": chunk.heading,
                "selector_or_line_range": selector,
                "source_hash": chunk.source_hash,
                "indexed_source_hash": chunk.indexed_source_hash,
                "chunk_hash": chunk.chunk_hash,
                "source_family_id": chunk.path,
                "record_kind": chunk.record_kind,
                "knowledge_status": chunk.status,
                "review_state": review_state_for(chunk),
                "relation_state": relation_state_for(chunk),
                "retrieval_policy": retrieval_policy_for(chunk),
                "authority_badge": harness.authority_badge_for(chunk, True),
                "usage_badge": "manifest_only",
                "temporal_badge": "stale" if chunk.stale else "current",
                "warning_code": manifest_warning_for(chunk),
                "retrieval_reasons": [],
                "graph_path": [],
                "source_clickback": clickback_for(chunk.path, selector),
                "generated_by": "vaks_phase_b_adapter_skeleton",
                "indexed_at": self.indexed_at,
            }

    def query(self, query: dict, top_k: int):
        results = harness.search_chunk_mode(self.index, query, SKELETON_MODE, top_k)
        return [self.adapter_result(query, result) for result in results]

    def adapter_result(self, query: dict, result: harness.SearchResult) -> dict:
        action_basis_allowed = result.bucket in harness.SUPPORT_BUCKETS and query["intent"] == "action"
        pack_allowed = result.bucket in harness.SUPPORT_BUCKETS or query["intent"] not in {"action", "evidence"}
        selector = normalize_selector(result.path, result.selector_or_line_range)
        return {
            "artifact_kind": "vaks_phase_b_adapter_result",
            "corpus": self.corpus,
            "query_id": query["id"],
            "query_group": query["group"],
            "query_intent": query["intent"],
            "mode": SKELETON_MODE,
            "rank": result.rank,
            "vaks_record_id": f"{self.corpus}:{result.path}:{result.chunk_hash or result.source_hash}",
            "vault_path": result.path,
            "heading_or_anchor": result.heading,
            "selector_or_line_range": selector,
            "source_hash": result.source_hash,
            "indexed_source_hash": self.indexed_source_hash_by_chunk.get(result.chunk_hash or "", result.source_hash),
            "chunk_hash": result.chunk_hash,
            "source_family_id": result.path,
            "record_kind": result.record_kind,
            "knowledge_status": result.status,
            "review_state": review_state_for_result(result),
            "relation_state": relation_state_for_result(result),
            "retrieval_policy": {
                "policy_kind": "phase_b_skeleton_bucket_local",
                "pack_allowed": pack_allowed,
                "action_basis_allowed": action_basis_allowed,
                "authority_bucket": result.bucket,
                "local_bucket_rank": result.local_bucket_rank,
            },
            "authority_badge": result.authority_badge,
            "usage_badge": result.usage_badge,
            "temporal_badge": result.temporal_badge or "current",
            "warning_code": result.warning_code,
            "retrieval_reasons": result.retrieval_reasons,
            "graph_path": [],
            "source_clickback": clickback_for(result.path, selector),
            "retrieval_receipt": {
                "score": result.score,
                "rank": result.rank,
                "mode": SKELETON_MODE,
                "bucket": result.bucket,
                "local_bucket_rank": result.local_bucket_rank,
                "receipt_present": result.receipt_present,
            },
            "generated_by": "vaks_phase_b_adapter_skeleton",
            "indexed_at": self.indexed_at,
            "snippet": " ".join(result.text.split())[:360],
        }


def review_state_for(chunk) -> str:
    if chunk.bucket in harness.SUPPORT_BUCKETS:
        return "reviewed_or_core"
    if chunk.bucket in {"candidate", "summary", "qa", "diagnostic", "overlay", "raw"}:
        return "candidate_or_source_only"
    if chunk.bucket == "feedback":
        return "feedback_event_only"
    return "unknown"


def relation_state_for(chunk) -> str:
    if chunk.bucket in harness.SUPPORT_BUCKETS:
        return "no_relation_asserted_by_adapter"
    return "candidate_relation_only"


def retrieval_policy_for(chunk) -> dict:
    pack_allowed = chunk.bucket in harness.SUPPORT_BUCKETS
    return {
        "policy_kind": "phase_b_skeleton_manifest",
        "pack_allowed": pack_allowed,
        "action_basis_allowed": bool(chunk.action_basis_allowed and chunk.bucket in harness.SUPPORT_BUCKETS),
        "authority_bucket": chunk.bucket,
    }


def manifest_warning_for(chunk) -> str:
    warnings: list[str] = []
    if chunk.bucket == "raw":
        warnings.append("raw_provenance_only")
    elif chunk.bucket in {"candidate", "summary", "qa", "diagnostic"}:
        warnings.append("candidate_or_diagnostic_only")
    elif chunk.bucket == "overlay":
        warnings.append("overlay_project_only")
    elif chunk.bucket == "feedback":
        warnings.append("feedback_not_truth")
    if chunk.stale:
        warnings.append("stale_index")
    return ";".join(dict.fromkeys(warnings))


def review_state_for_result(result: harness.SearchResult) -> str:
    if result.bucket in harness.SUPPORT_BUCKETS:
        return "reviewed_or_core"
    if result.bucket == "feedback":
        return "feedback_event_only"
    return "candidate_or_source_only"


def relation_state_for_result(result: harness.SearchResult) -> str:
    if result.bucket in harness.SUPPORT_BUCKETS:
        return "no_relation_asserted_by_adapter"
    return "candidate_relation_only"


def normalize_selector(vault_path: str, selector: str | None) -> str:
    selector = selector or "L1-L1"
    match = SELECTOR_RE.match(selector)
    if not match:
        return selector
    start = int(match.group("start"))
    end = int(match.group("end"))
    target = harness.ROOT / vault_path
    try:
        line_count = len(target.read_text(encoding="utf-8", errors="replace").splitlines()) or 1
    except OSError:
        line_count = max(start, end)
    start = max(1, min(start, line_count))
    end = max(start, min(end, line_count))
    return f"L{start}-L{end}"


def clickback_for(vault_path: str, selector: str) -> str:
    return f"{vault_path}:{selector}"


def write_jsonl(path: Path, rows) -> int:
    count = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def load_queries(query_file: Path) -> list[dict]:
    return harness.load_queries(query_file)


def write_manifest(corpora: list[str], result_prefix: str) -> None:
    summary = []
    for corpus in corpora:
        adapter = VaksPhaseBAdapter(corpus)
        path = RESULTS_DIR / f"{result_prefix}_{corpus}_chunk_manifest.jsonl"
        count = write_jsonl(path, adapter.chunk_manifest_rows())
        summary.append({"corpus": corpus, "manifest_path": str(path), "chunks": count, "indexed_at": adapter.indexed_at})
    (RESULTS_DIR / f"{result_prefix}_manifest_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def write_receipts(corpora: list[str], query_file: Path, result_prefix: str, top_k: int) -> None:
    queries = load_queries(query_file)
    summary = []
    for corpus in corpora:
        adapter = VaksPhaseBAdapter(corpus)

        def rows():
            for query in queries:
                for result in adapter.query(query, top_k):
                    yield result

        path = RESULTS_DIR / f"{result_prefix}_{corpus}_retrieval_receipts.jsonl"
        count = write_jsonl(path, rows())
        summary.append(
            {
                "corpus": corpus,
                "receipt_path": str(path),
                "queries": len(queries),
                "results": count,
                "indexed_at": adapter.indexed_at,
            }
        )
    (RESULTS_DIR / f"{result_prefix}_receipt_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["manifest", "receipts", "all"])
    parser.add_argument("--corpus", action="append", choices=["primary", "full"], default=None)
    parser.add_argument("--query-file", type=Path, default=harness.QUERY_FILE)
    parser.add_argument("--result-prefix", default="phase_b_skeleton")
    parser.add_argument("--top-k", type=int, default=10)
    args = parser.parse_args()
    corpora = args.corpus or ["primary", "full"]
    if args.command in {"manifest", "all"}:
        write_manifest(corpora, args.result_prefix)
    if args.command in {"receipts", "all"}:
        write_receipts(corpora, args.query_file, args.result_prefix, args.top_k)


if __name__ == "__main__":
    main()
