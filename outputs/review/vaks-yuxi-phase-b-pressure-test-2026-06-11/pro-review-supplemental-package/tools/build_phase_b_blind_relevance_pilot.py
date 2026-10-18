import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import build_phase_b_p0_query_replay as p0
import run_phase_b_pressure as harness


SANDBOX_DIR = harness.SANDBOX_DIR
RESULTS_DIR = harness.RESULTS_DIR

QUERY_FILE = SANDBOX_DIR / "queries_phase_b_blind_relevance.jsonl"
RUN_MANIFEST_JSON = RESULTS_DIR / "phase_b_blind_relevance_manifest.json"
QUERY_MANIFEST_CSV = RESULTS_DIR / "phase_b_blind_relevance_query_manifest.csv"
TOP20_ITEMS_CSV = RESULTS_DIR / "phase_b_blind_relevance_top20_items.csv"
JUDGMENT_PACKET_CSV = RESULTS_DIR / "phase_b_blind_relevance_judgment_packet.csv"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_BLIND_RELEVANCE_PILOT_REPORT.md"

TOP_K = 20
JUDGMENT_K = 5
TEST_SET = "blind_relevance_internal"
CORPORA = ["primary", "full"]
MODES = [
    "baseline_file_lexical",
    "vaks_only_lexical_bucket",
    "vaks_b_adapter_skeleton",
    "yuxi_native_profile",
]
STALE_PATHS = {"SCHEMA.md", "SOURCE_INTAKE.md", "FEEDBACK.md"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def bool_text(value) -> str:
    return "true" if value is True or str(value).lower() == "true" else "false"


def load_queries() -> list[dict]:
    if not QUERY_FILE.exists():
        raise FileNotFoundError(f"Missing blind relevance query file: {QUERY_FILE}")
    queries = []
    for line in QUERY_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        query = json.loads(line)
        query.setdefault("expected_terms", [])
        queries.append(query)
    return queries


def query_manifest_rows(run_id: str, queries: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for query in queries:
        canonical = json.dumps(query, ensure_ascii=False, sort_keys=True)
        rows.append(
            {
                "run_id": run_id,
                "test_set": TEST_SET,
                "query_file": QUERY_FILE.relative_to(SANDBOX_DIR).as_posix(),
                "query_file_sha256": sha256_file(QUERY_FILE),
                "query_id": query["id"],
                "group": query["group"],
                "intent": query["intent"],
                "query_sha256": sha256_text(canonical),
                "query": query["query"],
                "relevance_question": query["relevance_question"],
                "relevant_criteria": query["relevant_criteria"],
                "borderline_criteria": query["borderline_criteria"],
                "non_relevant_criteria": query["non_relevant_criteria"],
                "needs_boundary_warning": bool_text(query.get("needs_boundary_warning", False)),
                "risk_note": query.get("risk_note", ""),
            }
        )
    return rows


def item_row(run_id: str, corpus: str, query: dict, result: harness.SearchResult) -> dict:
    base = harness.result_to_dict(query, result, corpus)
    return {
        "run_id": run_id,
        "test_set": TEST_SET,
        "corpus": corpus,
        "mode": base["mode"],
        "query_id": base["query_id"],
        "query_group": base["query_group"],
        "intent": base["intent"],
        "rank": base["rank"],
        "path": base["path"],
        "heading": base["heading"],
        "score": base["score"],
        "bucket": base["bucket"],
        "is_support_bucket": bool_text(result.bucket in harness.SUPPORT_BUCKETS),
        "is_risky_bucket": bool_text(result.bucket in harness.RISK_BUCKETS),
        "status": base["status"],
        "record_kind": base["record_kind"],
        "selector_or_line_range": base["selector_or_line_range"],
        "retrieval_reasons": base["retrieval_reasons"],
        "warning_code": base["warning_code"],
        "authority_badge": base["authority_badge"],
        "usage_badge": base["usage_badge"],
        "temporal_badge": base["temporal_badge"],
        "stale": bool_text(base["stale"]),
        "source_hash": base["source_hash"],
        "chunk_hash": base["chunk_hash"],
        "source_hash_present": bool_text(bool(base["source_hash"])),
        "chunk_hash_present": bool_text(bool(base["chunk_hash"])),
        "local_bucket_rank": base["local_bucket_rank"],
        "clickback_present": bool_text(result.clickback_present),
        "hash_present": bool_text(result.hash_present),
        "adapter_present": bool_text(result.adapter_present),
        "receipt_present": bool_text(result.receipt_present),
        "snippet": base["snippet"],
    }


def packet_row(item: dict, query: dict) -> dict:
    return {
        "judgment_id": "|".join(
            [
                item["run_id"],
                item["corpus"],
                item["mode"],
                item["query_id"],
                str(item["rank"]),
            ]
        ),
        "run_id": item["run_id"],
        "test_set": item["test_set"],
        "corpus": item["corpus"],
        "mode": item["mode"],
        "query_id": item["query_id"],
        "rank": item["rank"],
        "intent": item["intent"],
        "query": query["query"],
        "relevance_question": query["relevance_question"],
        "relevant_criteria": query["relevant_criteria"],
        "borderline_criteria": query["borderline_criteria"],
        "non_relevant_criteria": query["non_relevant_criteria"],
        "path": item["path"],
        "heading": item["heading"],
        "bucket": item["bucket"],
        "status": item["status"],
        "warning_code": item["warning_code"],
        "snippet": item["snippet"],
        "judged_relevance": "",
        "judgment_basis": "",
        "judge_id": "",
        "judge_blind_to_expected_terms": "true",
    }


def build_manifest(run_id: str, started_at: str, queries: list[dict], item_rows: list[dict], packet_rows: list[dict]) -> dict:
    scripts = []
    for rel in [
        "tools/run_phase_b_pressure.py",
        "tools/build_phase_b_p0_query_replay.py",
        "tools/build_phase_b_blind_relevance_pilot.py",
    ]:
        path = SANDBOX_DIR / rel
        scripts.append({"path": rel, "sha256": sha256_file(path), "bytes": path.stat().st_size})
    return {
        "artifact_kind": "phase_b_blind_relevance_manifest",
        "run_id": run_id,
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "truth_boundary": "blind_relevance_packet_not_external_human_judgment",
        "action_basis_allowed": False,
        "query_file": QUERY_FILE.relative_to(SANDBOX_DIR).as_posix(),
        "query_file_sha256": sha256_file(QUERY_FILE),
        "query_count": len(queries),
        "corpora": CORPORA,
        "modes": MODES,
        "top_k": TOP_K,
        "judgment_k": JUDGMENT_K,
        "top20_item_rows": len(item_rows),
        "judgment_packet_rows": len(packet_rows),
        "script_records": scripts,
        "artifacts": {
            "query_manifest": QUERY_MANIFEST_CSV.relative_to(SANDBOX_DIR).as_posix(),
            "top20_items": TOP20_ITEMS_CSV.relative_to(SANDBOX_DIR).as_posix(),
            "judgment_packet": JUDGMENT_PACKET_CSV.relative_to(SANDBOX_DIR).as_posix(),
        },
        "hard_stops": [
            "internal_no_parent_context_is_not_external_human_blind",
            "judgment_packet_is_not_completed_judgment",
            "does_not_validate_original_yuxi_runtime",
            "does_not_approve_c_lite_or_writeback",
        ],
    }


def write_report(manifest: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_blind_relevance_pilot_report",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: blind_relevance_packet_not_external_human_judgment",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Blind Relevance Pilot Report",
        "",
        "## What This Adds",
        "",
        "```text",
        f"run_id: {manifest['run_id']}",
        f"query_count: {manifest['query_count']}",
        f"top20_item_rows: {manifest['top20_item_rows']}",
        f"judgment_packet_rows: {manifest['judgment_packet_rows']}",
        "judgment modes: baseline_file_lexical, vaks_only_lexical_bucket, vaks_b_adapter_skeleton, yuxi_native_profile",
        "judgment scope: top5 over primary/full",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "This creates the blind-query relevance-judgment packet.",
        "It does not itself complete relevance judgment.",
        "The query author is internal/no-parent-context, not external human.",
        "It does not validate original Yuxi runtime or C-lite.",
        "```",
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    queries = load_queries()
    started_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_id = f"phase_b_blind_relevance_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    indexes = {corpus: harness.CorpusIndex(corpus, stale_paths=STALE_PATHS) for corpus in CORPORA}
    item_rows: list[dict] = []
    packet_rows: list[dict] = []
    query_by_id = {query["id"]: query for query in queries}

    for corpus, index in indexes.items():
        print(f"blind relevance retrieval: {corpus} queries={len(queries)}", flush=True)
        for query in queries:
            for mode in MODES:
                results = p0.search_mode(index, query, mode, TOP_K)
                for result in results:
                    row = item_row(run_id, corpus, query, result)
                    item_rows.append(row)
                    if result.rank <= JUDGMENT_K:
                        packet_rows.append(packet_row(row, query_by_id[query["id"]]))

    query_rows = query_manifest_rows(run_id, queries)
    manifest = build_manifest(run_id, started_at, queries, item_rows, packet_rows)
    write_csv(QUERY_MANIFEST_CSV, query_rows)
    write_csv(TOP20_ITEMS_CSV, item_rows)
    write_csv(JUDGMENT_PACKET_CSV, packet_rows)
    RUN_MANIFEST_JSON.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(manifest)
    print(f"run_id: {run_id}")
    print(f"top20 item rows: {len(item_rows)}")
    print(f"judgment packet rows: {len(packet_rows)}")


if __name__ == "__main__":
    main()
