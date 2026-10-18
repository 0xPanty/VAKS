import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import build_phase_b_p0_query_replay as p0
import run_phase_b_pressure as harness


SANDBOX_DIR = harness.SANDBOX_DIR
RESULTS_DIR = harness.RESULTS_DIR

RUN_MANIFEST_JSON = RESULTS_DIR / "phase_b_frozen_rerun_v2_manifest.json"
CORPUS_MANIFEST_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_corpus_manifest.csv"
QUERY_MANIFEST_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_query_manifest.csv"
TOP20_ITEMS_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_top20_items.csv"
TOP1_10_REPLAY_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_top1_10_replay.csv"
TOP11_20_RECEIPTS_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_top11_20_receipts.csv"
QUERY_METRICS_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_query_metrics.csv"
SUMMARY_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_summary.csv"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_FROZEN_RERUN_V2_REPORT.md"

TEST_SETS = {
    "main": SANDBOX_DIR / "queries_phase_b.jsonl",
    "holdout_used": SANDBOX_DIR / "queries_phase_b_holdout.jsonl",
}

MODE_ORDER = p0.MODE_ORDER
TOP_K = 20
GOVERNANCE_K = 10
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


def metric_row(run_id: str, test_set: str, corpus: str, mode: str, query: dict, metric: dict) -> dict:
    return {
        "run_id": run_id,
        "test_set": test_set,
        "corpus": corpus,
        "mode": mode,
        "query_id": query["id"],
        "group": metric["group"],
        "intent": metric["intent"],
        "resolvable": bool_text(metric["resolvable"]),
        "hit_at_5": bool_text(metric["hit_at_5"]),
        "hit_at_10": bool_text(metric["hit_at_10"]),
        "mrr": f"{float(metric['mrr']):.12f}",
        "first_hit_rank": metric["first_hit_rank"],
        "dangerous_exposed_top10": metric["dangerous_exposed_top10"],
        "warning_coverage": f"{float(metric['warning_coverage']):.12f}",
        "action_leakage": bool_text(metric["action_leakage"]),
        "forbidden_top1": bool_text(metric["forbidden_top1"]),
        "cross_bucket_authority_violation": bool_text(metric["cross_bucket_authority_violation"]),
        "clickback_coverage": f"{float(metric['clickback_coverage']):.12f}",
        "hash_coverage": f"{float(metric['hash_coverage']):.12f}",
        "adapter_coverage": f"{float(metric['adapter_coverage']):.12f}",
        "receipt_coverage": f"{float(metric['receipt_coverage']):.12f}",
        "stale_exposed": metric["stale_exposed"],
        "stale_detected": metric["stale_detected"],
        "top1_bucket": metric["top1_bucket"],
        "top1_path": metric["top1_path"],
        "top1_warning": metric["top1_warning"],
    }


def item_row(run_id: str, test_set: str, corpus: str, query: dict, result: harness.SearchResult, metric: dict) -> dict:
    base = harness.result_to_dict(query, result, corpus)
    support_bucket = result.bucket in harness.SUPPORT_BUCKETS
    risky_bucket = result.bucket in harness.RISK_BUCKETS
    return {
        "run_id": run_id,
        "test_set": test_set,
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
        "is_support_bucket": bool_text(support_bucket),
        "is_risky_bucket": bool_text(risky_bucket),
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
        "metric_result_limit": TOP_K,
        "governance_window": GOVERNANCE_K,
        "clickback_present": bool_text(result.clickback_present),
        "hash_present": bool_text(result.hash_present),
        "adapter_present": bool_text(result.adapter_present),
        "receipt_present": bool_text(result.receipt_present),
        "result_hits_expected": bool_text(harness.term_hit(result, query.get("expected_terms") or [])),
        "query_first_hit_rank": metric["first_hit_rank"],
        "query_hit_at_5": bool_text(metric["hit_at_5"]),
        "query_hit_at_10": bool_text(metric["hit_at_10"]),
        "query_mrr": f"{float(metric['mrr']):.12f}",
        "query_action_leakage": bool_text(metric["action_leakage"]),
        "snippet": base["snippet"],
    }


def build_corpus_manifest(run_id: str, indexes: dict[str, harness.CorpusIndex]) -> list[dict]:
    rows: list[dict] = []
    for corpus, index in indexes.items():
        for doc in index.files:
            path = harness.ROOT / doc.path
            stat = path.stat()
            rows.append(
                {
                    "run_id": run_id,
                    "corpus": corpus,
                    "path": doc.path,
                    "bytes": stat.st_size,
                    "sha256": sha256_file(path),
                    "source_hash": doc.source_hash,
                    "status": doc.status,
                    "bucket": doc.bucket,
                    "record_kind": doc.record_kind,
                }
            )
    return rows


def build_query_manifest(run_id: str, query_by_set: dict[str, list[dict]]) -> list[dict]:
    rows: list[dict] = []
    for test_set, queries in query_by_set.items():
        query_file = TEST_SETS[test_set]
        for query in queries:
            canonical = json.dumps(query, ensure_ascii=False, sort_keys=True)
            rows.append(
                {
                    "run_id": run_id,
                    "test_set": test_set,
                    "query_file": query_file.relative_to(SANDBOX_DIR).as_posix(),
                    "query_file_sha256": sha256_file(query_file),
                    "query_id": query["id"],
                    "group": query["group"],
                    "intent": query["intent"],
                    "query_sha256": sha256_text(canonical),
                    "expected_terms_json": json.dumps(query.get("expected_terms") or [], ensure_ascii=False),
                    "needs_boundary_warning": bool_text(query.get("needs_boundary_warning", False)),
                }
            )
    return rows


def summarize(run_id: str, query_rows: list[dict]) -> list[dict]:
    summary_rows = p0.summarize_p0_metrics(query_rows)
    for row in summary_rows:
        row["run_id"] = run_id
    return summary_rows


def build_manifest(run_id: str, started_at: str, corpus_rows: list[dict], query_rows: list[dict]) -> dict:
    script_files = [
        "tools/run_phase_b_pressure.py",
        "tools/build_phase_b_p0_query_replay.py",
        "tools/build_phase_b_frozen_rerun_v2.py",
    ]
    scripts = []
    for rel in script_files:
        path = SANDBOX_DIR / rel
        scripts.append({"path": rel, "sha256": sha256_file(path), "bytes": path.stat().st_size})
    return {
        "artifact_kind": "phase_b_frozen_rerun_v2_manifest",
        "run_id": run_id,
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "truth_boundary": "single_run_replay_bundle_not_runtime_validation",
        "action_basis_allowed": False,
        "test_sets": list(TEST_SETS),
        "corpora": ["primary", "full"],
        "modes": MODE_ORDER,
        "metric_result_limit": TOP_K,
        "governance_window": GOVERNANCE_K,
        "stale_paths": sorted(STALE_PATHS),
        "corpus_file_records": len(corpus_rows),
        "query_records": len(query_rows),
        "script_records": scripts,
        "artifacts": {
            "corpus_manifest": CORPUS_MANIFEST_CSV.relative_to(SANDBOX_DIR).as_posix(),
            "query_manifest": QUERY_MANIFEST_CSV.relative_to(SANDBOX_DIR).as_posix(),
            "top20_items": TOP20_ITEMS_CSV.relative_to(SANDBOX_DIR).as_posix(),
            "top1_10_replay": TOP1_10_REPLAY_CSV.relative_to(SANDBOX_DIR).as_posix(),
            "top11_20_receipts": TOP11_20_RECEIPTS_CSV.relative_to(SANDBOX_DIR).as_posix(),
            "query_metrics": QUERY_METRICS_CSV.relative_to(SANDBOX_DIR).as_posix(),
            "summary": SUMMARY_CSV.relative_to(SANDBOX_DIR).as_posix(),
        },
        "hard_stops": [
            "single_run_bundle_is_still_local_proxy_evidence",
            "does_not_validate_original_yuxi_runtime",
            "does_not_create_relevance_judgment",
            "does_not_approve_c_lite_or_writeback",
        ],
    }


def write_report(manifest: dict, item_rows: list[dict], query_metric_rows: list[dict], summary_rows: list[dict]) -> None:
    lines = [
        "---",
        "record_kind: sandbox_frozen_rerun_v2_report",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: single_run_replay_bundle_not_runtime_validation",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Frozen Rerun V2 Report",
        "",
        "## What This Adds",
        "",
        "```text",
        f"run_id: {manifest['run_id']}",
        "single invocation over frozen corpus/query/script hashes",
        "top20 item-level export",
        "top1-10 replay split",
        "top11-20 receipt split",
        "query-level metrics",
        "summary",
        "corpus and query manifests",
        "```",
        "",
        "## Counts",
        "",
        "```text",
        f"corpus file records: {manifest['corpus_file_records']}",
        f"query records: {manifest['query_records']}",
        f"top20 item rows: {len(item_rows)}",
        f"query metric rows: {len(query_metric_rows)}",
        f"summary rows: {len(summary_rows)}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "This replaces the patched-together P0 replay/hardening story with one single-run local bundle.",
        "It is still expected_terms-based proxy retrieval evidence, not human relevance judgment.",
        "It does not validate original Yuxi runtime.",
        "It does not approve C-lite, writeback, action basis, or core-doc strong conclusions.",
        "```",
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    started_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_id = f"phase_b_frozen_rerun_v2_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    query_by_set = {test_set: harness.load_queries(path) for test_set, path in TEST_SETS.items()}
    indexes = {corpus: harness.CorpusIndex(corpus, stale_paths=STALE_PATHS) for corpus in ["primary", "full"]}
    corpus_rows = build_corpus_manifest(run_id, indexes)
    query_manifest_rows = build_query_manifest(run_id, query_by_set)
    item_rows: list[dict] = []
    query_metric_rows: list[dict] = []
    p0_summary_input_rows: list[dict] = []

    for test_set, queries in query_by_set.items():
        for corpus, index in indexes.items():
            print(f"frozen rerun v2: {test_set}/{corpus} queries={len(queries)}", flush=True)
            resolvable_cache = {
                query["id"]: harness.terms_resolvable(index, query.get("expected_terms") or []) for query in queries
            }
            for query in queries:
                for mode in MODE_ORDER:
                    results = p0.search_mode(index, query, mode, TOP_K)
                    metric = harness.evaluate_results(query, results, resolvable_cache[query["id"]])
                    query_metric_rows.append(metric_row(run_id, test_set, corpus, mode, query, metric))
                    p0_input = dict(metric)
                    p0_input.update({"test_set": test_set, "corpus": corpus, "mode": mode})
                    p0_summary_input_rows.append(p0_input)
                    for result in results:
                        item_rows.append(item_row(run_id, test_set, corpus, query, result, metric))

    summary_rows = summarize(run_id, p0_summary_input_rows)
    manifest = build_manifest(run_id, started_at, corpus_rows, query_manifest_rows)

    write_csv(CORPUS_MANIFEST_CSV, corpus_rows)
    write_csv(QUERY_MANIFEST_CSV, query_manifest_rows)
    write_csv(TOP20_ITEMS_CSV, item_rows)
    write_csv(TOP1_10_REPLAY_CSV, [row for row in item_rows if int(row["rank"]) <= 10])
    write_csv(TOP11_20_RECEIPTS_CSV, [row for row in item_rows if 11 <= int(row["rank"]) <= 20])
    write_csv(QUERY_METRICS_CSV, query_metric_rows)
    write_csv(SUMMARY_CSV, summary_rows)
    RUN_MANIFEST_JSON.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(manifest, item_rows, query_metric_rows, summary_rows)
    print(f"run_id: {run_id}")
    print(f"top20 item rows: {len(item_rows)}")
    print(f"query metric rows: {len(query_metric_rows)}")
    print(f"summary rows: {len(summary_rows)}")


if __name__ == "__main__":
    main()
