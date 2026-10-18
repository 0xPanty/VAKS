import csv
import json
from collections import defaultdict
from pathlib import Path

import run_phase_b_pressure as harness


SANDBOX_DIR = harness.SANDBOX_DIR
RESULTS_DIR = harness.RESULTS_DIR

RECEIPTS_CSV = RESULTS_DIR / "phase_b_top11_20_item_receipts.csv"
SUMMARY_JSON = RESULTS_DIR / "phase_b_top11_20_item_receipts_summary.json"
SUMMARY_CSV = RESULTS_DIR / "phase_b_top11_20_item_receipts_summary.csv"
CHECK_JSON = RESULTS_DIR / "phase_b_top11_20_item_receipts_check.json"
CHECK_MD = SANDBOX_DIR / "PHASE_B_TOP11_20_ITEM_RECEIPTS_CHECK.md"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_TOP11_20_ITEM_RECEIPTS_REPORT.md"

RECEIPT_MIN_RANK = 11
RECEIPT_MAX_RANK = 20


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def b(value: str) -> bool:
    return str(value).lower() == "true"


def validate_artifacts(errors: list[dict]) -> dict:
    artifacts = []
    for path in [RECEIPTS_CSV, SUMMARY_JSON, SUMMARY_CSV, REPORT_PATH]:
        exists = path.exists()
        artifacts.append(
            {"path": str(path.relative_to(SANDBOX_DIR)), "exists": exists, "bytes": path.stat().st_size if exists else 0}
        )
        if not exists:
            add_error(errors, "missing_artifact", str(path))
        elif path.stat().st_size == 0:
            add_error(errors, "empty_artifact", str(path))
    return {"artifacts": artifacts}


def validate_rows(errors: list[dict], rows: list[dict], summary_rows: list[dict]) -> dict:
    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        rank = int(row["rank"])
        if not (RECEIPT_MIN_RANK <= rank <= RECEIPT_MAX_RANK):
            add_error(errors, "rank_outside_receipt_window", f"{row['test_set']}:{row['query_id']}:{row['mode']}:{rank}")
        grouped[(row["test_set"], row["corpus"], row["mode"], row["query_id"])].append(row)

    incomplete_groups = 0
    duplicate_rank_groups = 0
    missing_first_hit_receipts = 0
    for key, group_rows in grouped.items():
        ranks = [int(row["rank"]) for row in group_rows]
        if sorted(ranks) != list(range(RECEIPT_MIN_RANK, RECEIPT_MAX_RANK + 1)):
            incomplete_groups += 1
            if incomplete_groups <= 20:
                add_error(errors, "incomplete_rank_window", f"{key}:{sorted(ranks)}")
        if len(set(ranks)) != len(ranks):
            duplicate_rank_groups += 1
            if duplicate_rank_groups <= 20:
                add_error(errors, "duplicate_rank_in_window", str(key))
        metric_rank_raw = str(group_rows[0].get("query_first_hit_rank") or "")
        metric_rank = int(metric_rank_raw) if metric_rank_raw else 0
        if RECEIPT_MIN_RANK <= metric_rank <= RECEIPT_MAX_RANK:
            hit_rows = [row for row in group_rows if int(row["rank"]) == metric_rank and b(row["result_hits_expected"])]
            if not hit_rows:
                missing_first_hit_receipts += 1
                if missing_first_hit_receipts <= 20:
                    add_error(errors, "missing_first_hit_receipt", f"{key}:first_hit={metric_rank}")

    summary_by_key = {(row["test_set"], row["corpus"], row["mode"]): row for row in summary_rows}
    observed_summary: dict[tuple[str, str, str], dict] = defaultdict(
        lambda: {
            "queries": 0,
            "receipt_rows_rank_11_20": 0,
            "expected_receipt_rows": 0,
            "queries_with_first_hit_11_20": 0,
            "missing_first_hit_receipts": 0,
        }
    )
    for key, group_rows in grouped.items():
        test_set, corpus, mode, _query_id = key
        s_key = (test_set, corpus, mode)
        observed_summary[s_key]["queries"] += 1
        observed_summary[s_key]["receipt_rows_rank_11_20"] += len(group_rows)
        observed_summary[s_key]["expected_receipt_rows"] += 10
        metric_rank_raw = str(group_rows[0].get("query_first_hit_rank") or "")
        metric_rank = int(metric_rank_raw) if metric_rank_raw else 0
        if RECEIPT_MIN_RANK <= metric_rank <= RECEIPT_MAX_RANK:
            observed_summary[s_key]["queries_with_first_hit_11_20"] += 1
            if not any(int(row["rank"]) == metric_rank and b(row["result_hits_expected"]) for row in group_rows):
                observed_summary[s_key]["missing_first_hit_receipts"] += 1

    if set(summary_by_key) != set(observed_summary):
        add_error(errors, "summary_key_set_mismatch", f"{len(summary_by_key)} != {len(observed_summary)}")
    for key, observed in observed_summary.items():
        summary = summary_by_key.get(key)
        if not summary:
            continue
        for field, value in observed.items():
            if int(summary.get(field) or 0) != int(value):
                add_error(errors, "summary_value_mismatch", f"{key}:{field}:{summary.get(field)} != {value}")

    return {
        "receipt_rows": len(rows),
        "query_mode_corpus_groups": len(grouped),
        "summary_rows": len(summary_rows),
        "incomplete_groups": incomplete_groups,
        "duplicate_rank_groups": duplicate_rank_groups,
        "missing_first_hit_receipts": missing_first_hit_receipts,
    }


def validate_summary_json(errors: list[dict], summary_rows: list[dict]) -> dict:
    payload = read_json(SUMMARY_JSON)
    if payload.get("receipt_rank_window") != [RECEIPT_MIN_RANK, RECEIPT_MAX_RANK]:
        add_error(errors, "summary_json_rank_window_mismatch", str(payload.get("receipt_rank_window")))
    if len(payload.get("summary_rows", [])) != len(summary_rows):
        add_error(errors, "summary_json_row_count_mismatch", f"{len(payload.get('summary_rows', []))} != {len(summary_rows)}")
    return {
        "metric_result_limit": payload.get("metric_result_limit"),
        "governance_window": payload.get("governance_window"),
    }


def write_report(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_top11_20_item_receipts_check",
        f"status: {result['top11_20_item_receipts_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: receipt_check_not_runtime_validation",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Top11-20 Item Receipts Check",
        "",
        "## Result",
        "",
        "```text",
        f"status: {result['top11_20_item_receipts_check_status']}",
        f"error count: {result['error_count']}",
        f"receipt rows: {result['row_check']['receipt_rows']}",
        f"query-mode-corpus groups: {result['row_check']['query_mode_corpus_groups']}",
        f"missing first-hit receipts: {result['row_check']['missing_first_hit_receipts']}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "This verifies rank 11-20 local replay receipts.",
        "It keeps top10 governance metrics unchanged.",
        "It does not validate original Yuxi runtime, answer-loop behavior, C-lite, or writeback.",
        "```",
        "",
        "## Errors",
        "",
    ]
    if result["errors"]:
        lines.extend(f"- {error['code']}: {error['detail']}" for error in result["errors"])
    else:
        lines.append("- none")
    lines.append("")
    CHECK_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    errors: list[dict] = []
    artifacts = validate_artifacts(errors)
    rows = read_csv(RECEIPTS_CSV) if RECEIPTS_CSV.exists() else []
    summary_rows = read_csv(SUMMARY_CSV) if SUMMARY_CSV.exists() else []
    row_check = validate_rows(errors, rows, summary_rows) if rows and summary_rows else {}
    summary_json = validate_summary_json(errors, summary_rows) if SUMMARY_JSON.exists() else {}
    result = {
        "top11_20_item_receipts_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "artifacts": artifacts,
        "row_check": row_check,
        "summary_json": summary_json,
    }
    CHECK_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(result)
    print(f"top11-20 item receipts check status: {result['top11_20_item_receipts_check_status']}")
    print(f"error count: {result['error_count']}")


if __name__ == "__main__":
    main()
