import csv
import json
from collections import defaultdict
from pathlib import Path

import build_phase_b_p0_query_replay as p0
import run_phase_b_pressure as harness


SANDBOX_DIR = harness.SANDBOX_DIR
RESULTS_DIR = harness.RESULTS_DIR

RECEIPTS_CSV = RESULTS_DIR / "phase_b_top11_20_item_receipts.csv"
SUMMARY_JSON = RESULTS_DIR / "phase_b_top11_20_item_receipts_summary.json"
SUMMARY_CSV = RESULTS_DIR / "phase_b_top11_20_item_receipts_summary.csv"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_TOP11_20_ITEM_RECEIPTS_REPORT.md"

RECEIPT_MIN_RANK = 11
RECEIPT_MAX_RANK = 20
TOP_K = 20
GOVERNANCE_K = 10
MODE_ORDER = p0.MODE_ORDER

TEST_SETS = {
    "main": SANDBOX_DIR / "queries_phase_b.jsonl",
    "holdout_used": SANDBOX_DIR / "queries_phase_b_holdout.jsonl",
}


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def bool_text(value) -> str:
    return "true" if value is True or str(value).lower() == "true" else "false"


def query_metric_fields(query: dict, results: list[harness.SearchResult], index: harness.CorpusIndex) -> dict:
    metric = harness.evaluate_results(query, results, harness.terms_resolvable(index, query.get("expected_terms") or []))
    return {
        "query_resolvable": bool_text(metric["resolvable"]),
        "query_hit_at_5": bool_text(metric["hit_at_5"]),
        "query_hit_at_10": bool_text(metric["hit_at_10"]),
        "query_mrr": metric["mrr"],
        "query_first_hit_rank": metric["first_hit_rank"],
        "query_action_leakage": bool_text(metric["action_leakage"]),
        "query_forbidden_top1": bool_text(metric["forbidden_top1"]),
        "query_cross_bucket_violation": bool_text(metric["cross_bucket_authority_violation"]),
        "query_warning_coverage": metric["warning_coverage"],
        "query_clickback_coverage": metric["clickback_coverage"],
        "query_hash_coverage": metric["hash_coverage"],
        "query_adapter_coverage": metric["adapter_coverage"],
        "query_receipt_coverage": metric["receipt_coverage"],
        "query_stale_exposed": metric["stale_exposed"],
        "query_stale_detected": metric["stale_detected"],
    }


def receipt_row(test_set: str, corpus: str, query: dict, result: harness.SearchResult, metric: dict) -> dict:
    support_bucket = result.bucket in harness.SUPPORT_BUCKETS
    risky_bucket = result.bucket in harness.RISK_BUCKETS
    row = harness.result_to_dict(query, result, corpus)
    return {
        "test_set": test_set,
        "corpus": corpus,
        "mode": row["mode"],
        "query_id": row["query_id"],
        "query_group": row["query_group"],
        "intent": row["intent"],
        "query_text": query["query"],
        "expected_terms_json": json.dumps(query.get("expected_terms") or [], ensure_ascii=False),
        "needs_boundary_warning": bool_text(query.get("needs_boundary_warning", False)),
        **metric,
        "rank": row["rank"],
        "path": row["path"],
        "heading": row["heading"],
        "score": row["score"],
        "bucket": row["bucket"],
        "is_support_bucket": bool_text(support_bucket),
        "is_risky_bucket": bool_text(risky_bucket),
        "status": row["status"],
        "record_kind": row["record_kind"],
        "selector_or_line_range": row.get("selector_or_line_range", ""),
        "retrieval_reasons": row.get("retrieval_reasons", ""),
        "warning_code": row.get("warning_code", ""),
        "authority_badge": row.get("authority_badge", ""),
        "usage_badge": row.get("usage_badge", ""),
        "temporal_badge": row.get("temporal_badge", ""),
        "stale": bool_text(row.get("stale", "")),
        "source_hash_present": bool_text(bool(row.get("source_hash", ""))),
        "chunk_hash_present": bool_text(bool(row.get("chunk_hash", ""))),
        "source_hash": row.get("source_hash", ""),
        "chunk_hash": row.get("chunk_hash", ""),
        "local_bucket_rank": row.get("local_bucket_rank", ""),
        "metric_result_limit": TOP_K,
        "replay_rank_window": f"{RECEIPT_MIN_RANK}-{RECEIPT_MAX_RANK}",
        "governance_window": GOVERNANCE_K,
        "clickback_present": bool_text(result.clickback_present),
        "hash_present": bool_text(result.hash_present),
        "adapter_present": bool_text(result.adapter_present),
        "receipt_present": bool_text(result.receipt_present),
        "result_hits_expected": bool_text(harness.term_hit(result, query.get("expected_terms") or [])),
        "result_forbidden_top1": "false",
        "result_unlabelled_risky": bool_text(risky_bucket and not row.get("warning_code", "")),
        "snippet": row.get("snippet", ""),
    }


def build_rows() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    metric_rows: list[dict] = []
    stale_paths = {"SCHEMA.md", "SOURCE_INTAKE.md", "FEEDBACK.md"}
    for test_set, query_path in TEST_SETS.items():
        queries = harness.load_queries(query_path)
        for corpus in ["primary", "full"]:
            index = harness.CorpusIndex(corpus, stale_paths=stale_paths)
            print(f"building receipts: {test_set}/{corpus} queries={len(queries)}", flush=True)
            for query in queries:
                for mode in MODE_ORDER:
                    results = p0.search_mode(index, query, mode, TOP_K)
                    metric = query_metric_fields(query, results, index)
                    metric_rows.append(
                        {
                            "test_set": test_set,
                            "corpus": corpus,
                            "mode": mode,
                            "query_id": query["id"],
                            "first_hit_rank": metric["query_first_hit_rank"],
                            "hit_at_5": metric["query_hit_at_5"],
                            "hit_at_10": metric["query_hit_at_10"],
                            "mrr": metric["query_mrr"],
                        }
                    )
                    for result in results:
                        if RECEIPT_MIN_RANK <= result.rank <= RECEIPT_MAX_RANK:
                            rows.append(receipt_row(test_set, corpus, query, result, metric))
    summary_rows = summarize(rows, metric_rows)
    return rows, summary_rows


def summarize(rows: list[dict], metric_rows: list[dict]) -> list[dict]:
    receipt_counts: dict[tuple[str, str, str], int] = defaultdict(int)
    hit_11_20_counts: dict[tuple[str, str, str], int] = defaultdict(int)
    query_counts: dict[tuple[str, str, str], int] = defaultdict(int)
    missing_receipt_hits: dict[tuple[str, str, str], int] = defaultdict(int)

    receipt_keys = {
        (row["test_set"], row["corpus"], row["mode"], row["query_id"], str(row["rank"])) for row in rows
    }
    for row in rows:
        receipt_counts[(row["test_set"], row["corpus"], row["mode"])] += 1
    for row in metric_rows:
        key = (row["test_set"], row["corpus"], row["mode"])
        query_counts[key] += 1
        rank_raw = str(row.get("first_hit_rank") or "")
        rank = int(rank_raw) if rank_raw else 0
        if RECEIPT_MIN_RANK <= rank <= RECEIPT_MAX_RANK:
            hit_11_20_counts[key] += 1
            receipt_key = (row["test_set"], row["corpus"], row["mode"], row["query_id"], str(rank))
            if receipt_key not in receipt_keys:
                missing_receipt_hits[key] += 1

    summary_rows: list[dict] = []
    for key in sorted(query_counts):
        test_set, corpus, mode = key
        summary_rows.append(
            {
                "test_set": test_set,
                "corpus": corpus,
                "mode": mode,
                "queries": query_counts[key],
                "receipt_rows_rank_11_20": receipt_counts[key],
                "expected_receipt_rows": query_counts[key] * 10,
                "queries_with_first_hit_11_20": hit_11_20_counts[key],
                "missing_first_hit_receipts": missing_receipt_hits[key],
            }
        )
    return summary_rows


def write_report(rows: list[dict], summary_rows: list[dict]) -> None:
    total_queries = sum(int(row["queries"]) for row in summary_rows)
    hit_11_20 = sum(int(row["queries_with_first_hit_11_20"]) for row in summary_rows)
    missing_hits = sum(int(row["missing_first_hit_receipts"]) for row in summary_rows)
    lines = [
        "---",
        "record_kind: sandbox_top11_20_item_receipts_report",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: item_receipts_are_replay_evidence_not_runtime_validation",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Top11-20 Item Receipts Report",
        "",
        "## What This Adds",
        "",
        "```text",
        "item-level receipts for ranks 11-20",
        "covers the existing P0 main and holdout_used query sets",
        "keeps top10 governance window unchanged",
        "fills the previous gap where first_hit_rank 11-20 existed only as query-level data",
        "```",
        "",
        "## Counts",
        "",
        "```text",
        f"receipt rows: {len(rows)}",
        f"query-mode-corpus rows summarized: {total_queries}",
        f"queries with first_hit_rank 11-20: {hit_11_20}",
        f"missing first-hit receipts: {missing_hits}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "This is replay/audit evidence for local proxy runs.",
        "It does not expand the governance window beyond top10.",
        "It does not validate original Yuxi runtime, answer-loop behavior, C-lite, or writeback.",
        "```",
        "",
        "## Artifacts",
        "",
        "```text",
        "results/phase_b_top11_20_item_receipts.csv",
        "results/phase_b_top11_20_item_receipts_summary.csv",
        "results/phase_b_top11_20_item_receipts_summary.json",
        "```",
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows, summary_rows = build_rows()
    write_csv(RECEIPTS_CSV, rows)
    write_csv(SUMMARY_CSV, summary_rows)
    SUMMARY_JSON.write_text(
        json.dumps(
            {
                "artifact_kind": "phase_b_top11_20_item_receipts_summary",
                "truth_boundary": "top11_20_receipts_are_local_replay_evidence",
                "action_basis_allowed": False,
                "receipt_rank_window": [RECEIPT_MIN_RANK, RECEIPT_MAX_RANK],
                "metric_result_limit": TOP_K,
                "governance_window": GOVERNANCE_K,
                "summary_rows": summary_rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    write_report(rows, summary_rows)
    print(f"top11-20 receipt rows: {len(rows)}")
    print(f"summary rows: {len(summary_rows)}")


if __name__ == "__main__":
    main()
