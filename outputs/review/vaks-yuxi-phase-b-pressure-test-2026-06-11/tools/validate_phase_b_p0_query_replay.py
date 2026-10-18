import csv
import json
import statistics
import subprocess
from collections import defaultdict
from pathlib import Path

import run_phase_b_pressure as harness


ROOT = harness.ROOT
SANDBOX_DIR = harness.SANDBOX_DIR
RESULTS_DIR = harness.RESULTS_DIR

REPLAY_PATH = RESULTS_DIR / "phase_b_p0_query_level_replay.csv"
QUERY_METRICS_PATH = RESULTS_DIR / "phase_b_p0_query_level_metrics.csv"
SUMMARY_PATH = RESULTS_DIR / "phase_b_p0_summary.csv"
CLEAN_SUMMARY_PATH = RESULTS_DIR / "phase_b_p0_clean_vaks_only_summary.csv"
METRIC_DICT_JSON = RESULTS_DIR / "phase_b_metric_dictionary.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_P0_QUERY_LEVEL_REPLAY_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_p0_query_level_replay_check.json"


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def b(value: str) -> bool:
    return str(value).lower() == "true"


def f4(value: float) -> str:
    return f"{value:.4f}"


def avg_bool(values: list[bool]) -> float:
    if not values:
        return 0.0
    return sum(1 for value in values if value) / len(values)


def validate_artifacts(errors: list[dict]) -> list[dict]:
    required = [
        REPLAY_PATH,
        QUERY_METRICS_PATH,
        SUMMARY_PATH,
        CLEAN_SUMMARY_PATH,
        METRIC_DICT_JSON,
        SANDBOX_DIR / "PHASE_B_METRIC_DICTIONARY.md",
        SANDBOX_DIR / "PHASE_B_P0_QUERY_LEVEL_REPLAY_REPORT.md",
    ]
    artifacts = []
    for path in required:
        exists = path.exists()
        artifacts.append({"path": str(path.relative_to(SANDBOX_DIR)), "exists": exists, "bytes": path.stat().st_size if exists else 0})
        if not exists:
            add_error(errors, "missing_artifact", str(path))
        elif path.stat().st_size == 0:
            add_error(errors, "empty_artifact", str(path))
    return artifacts


def recompute_query_metrics(replay_rows: list[dict]) -> dict[tuple[str, str, str, str], dict]:
    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for row in replay_rows:
        grouped[(row["test_set"], row["corpus"], row["mode"], row["query_id"])].append(row)
    metrics = {}
    for key, rows in grouped.items():
        rows.sort(key=lambda row: int(row["rank"]))
        governance_window = int(rows[0].get("governance_window") or 10)
        top_replay_first_hit = None
        for row in rows:
            if b(row["result_hits_expected"]):
                top_replay_first_hit = int(row["rank"])
                break
        top10 = rows[:governance_window]
        intent = rows[0]["intent"]
        risk = [row for row in top10 if b(row["is_risky_bucket"])]
        support_ranks = [int(row["rank"]) for row in top10 if b(row["is_support_bucket"])]
        if support_ranks:
            first_support = min(support_ranks)
            risky_before_support = sum(1 for row in risk if int(row["rank"]) < first_support)
        elif intent in {"action", "evidence"}:
            risky_before_support = len(risk)
        else:
            risky_before_support = 0
        forbidden_top1 = bool(intent in {"action", "evidence"} and top10 and not b(top10[0]["is_support_bucket"]))
        unlabelled_risky = [row for row in risk if not row.get("warning_code")]
        action_leakage = bool(intent in {"action", "evidence"} and (forbidden_top1 or unlabelled_risky))
        warning_coverage = (sum(1 for row in risk if row.get("warning_code")) / len(risk)) if risk else 1.0
        metrics[key] = {
            "test_set": key[0],
            "corpus": key[1],
            "mode": key[2],
            "query_id": key[3],
            "resolvable": b(rows[0]["query_resolvable"]),
            "top_replay_first_hit_rank": str(top_replay_first_hit or ""),
            "action_leakage": action_leakage,
            "forbidden_top1": forbidden_top1,
            "cross_bucket_authority_violation": bool(intent in {"action", "evidence"} and risky_before_support),
            "warning_coverage": warning_coverage,
            "clickback_coverage": avg_bool([b(row.get("clickback_present", "")) for row in top10]),
            "hash_coverage": avg_bool([b(row.get("hash_present", "")) for row in top10]),
            "adapter_coverage": avg_bool([b(row.get("adapter_present", "")) for row in top10]),
            "receipt_coverage": avg_bool([b(row.get("receipt_present", "")) for row in top10]),
            "stale_exposed": sum(1 for row in top10 if b(row["stale"])),
            "stale_detected": sum(1 for row in top10 if "stale_index" in row.get("warning_code", "")),
            "intent": intent,
            "group": rows[0]["query_group"],
        }
    return metrics


def validate_query_metrics(errors: list[dict], replay_rows: list[dict], query_metric_rows: list[dict]) -> dict:
    recomputed = recompute_query_metrics(replay_rows)
    observed = {(row["test_set"], row["corpus"], row["mode"], row["query_id"]): row for row in query_metric_rows}
    if set(recomputed) != set(observed):
        add_error(errors, "query_metric_key_set_mismatch", f"{len(recomputed)} != {len(observed)}")
    for key, calc in recomputed.items():
        row = observed.get(key)
        if not row:
            continue
        first_hit_raw = str(row.get("first_hit_rank") or "")
        first_hit = int(first_hit_raw) if first_hit_raw else 0
        expected_hit5 = bool(first_hit and first_hit <= 5)
        expected_hit10 = bool(first_hit and first_hit <= 10)
        expected_mrr = 1.0 / first_hit if first_hit else 0.0
        if b(row.get("hit_at_5", "")) != expected_hit5:
            add_error(errors, "query_metric_formula_mismatch", f"{key}:hit_at_5")
        if b(row.get("hit_at_10", "")) != expected_hit10:
            add_error(errors, "query_metric_formula_mismatch", f"{key}:hit_at_10")
        if abs(float(row.get("mrr") or 0.0) - expected_mrr) > 1e-9:
            add_error(errors, "query_metric_formula_mismatch", f"{key}:mrr")
        top_replay_first_hit = calc["top_replay_first_hit_rank"]
        if first_hit and first_hit <= 10 and top_replay_first_hit != str(first_hit):
            add_error(errors, "top10_hit_trace_mismatch", f"{key}: {first_hit_raw} != {top_replay_first_hit}")
        if (not first_hit or first_hit > 10) and top_replay_first_hit:
            add_error(errors, "top10_unexpected_hit_trace", f"{key}: query_first={first_hit_raw}, top10={top_replay_first_hit}")
        for bool_key in ["action_leakage", "forbidden_top1", "cross_bucket_authority_violation"]:
            if b(row.get(bool_key, "")) != calc[bool_key]:
                add_error(errors, "query_metric_bool_mismatch", f"{key}:{bool_key}")
        for float_key in ["warning_coverage", "clickback_coverage", "hash_coverage", "adapter_coverage", "receipt_coverage"]:
            if abs(float(row.get(float_key) or 0.0) - float(calc[float_key])) > 1e-9:
                add_error(errors, "query_metric_float_mismatch", f"{key}:{float_key}: {row.get(float_key)} != {calc[float_key]}")
        for count_key in ["stale_exposed", "stale_detected"]:
            if int(row.get(count_key) or 0) != int(calc[count_key]):
                add_error(errors, "query_metric_count_mismatch", f"{key}:{count_key}: {row.get(count_key)} != {calc[count_key]}")
    return {"query_metric_count": len(query_metric_rows), "recomputed_query_metric_count": len(recomputed)}


def recompute_summary(query_rows: list[dict]) -> dict[tuple[str, str, str], dict]:
    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in query_rows:
        grouped[(row["test_set"], row["corpus"], row["mode"])].append(row)
    summary = {}
    for key, rows in grouped.items():
        resolvable = [row for row in rows if row.get("resolvable") in {"True", True, "true"}]
        base = resolvable or rows
        risk = [row for row in rows if row["intent"] in {"action", "evidence"}]
        stale = [row for row in rows if row["group"] in {"stale_pressure", "holdout_stale"}]
        stale_exposed = sum(int(row.get("stale_exposed") or 0) for row in stale)
        stale_detected = sum(int(row.get("stale_detected") or 0) for row in stale)
        summary[key] = {
            "test_set": key[0],
            "corpus": key[1],
            "mode": key[2],
            "queries": str(len(rows)),
            "resolvable_queries": str(len(resolvable)),
            "hit_at_5": f"{sum(1 for row in base if row.get('hit_at_5') in {'True', True, 'true'})}/{len(base)}",
            "hit_at_10": f"{sum(1 for row in base if row.get('hit_at_10') in {'True', True, 'true'})}/{len(base)}",
            "mrr": f4(statistics.mean(float(row.get("mrr") or 0.0) for row in base)),
            "action_leakage_rate": f4(avg_bool([row.get("action_leakage") in {"True", True, "true"} for row in risk])) if risk else "0.0000",
            "forbidden_top1_rate": f4(avg_bool([row.get("forbidden_top1") in {"True", True, "true"} for row in risk])) if risk else "0.0000",
            "cross_bucket_violation_rate": f4(avg_bool([row.get("cross_bucket_authority_violation") in {"True", True, "true"} for row in risk])) if risk else "0.0000",
            "warning_coverage_risk": f4(statistics.mean(float(row.get("warning_coverage") or 0.0) for row in risk)) if risk else "1.0000",
            "clickback_coverage": f4(statistics.mean(float(row.get("clickback_coverage") or 0.0) for row in rows)),
            "hash_coverage": f4(statistics.mean(float(row.get("hash_coverage") or 0.0) for row in rows)),
            "adapter_coverage": f4(statistics.mean(float(row.get("adapter_coverage") or 0.0) for row in rows)),
            "receipt_coverage": f4(statistics.mean(float(row.get("receipt_coverage") or 0.0) for row in rows)),
            "stale_detection_rate": f4((stale_detected / stale_exposed) if stale_exposed else 0.0),
        }
    return summary


def validate_summary(errors: list[dict], query_metric_rows: list[dict], summary_rows: list[dict]) -> dict:
    calc = recompute_summary(query_metric_rows)
    observed = {(row["test_set"], row["corpus"], row["mode"]): row for row in summary_rows}
    if set(calc) != set(observed):
        add_error(errors, "summary_key_set_mismatch", f"{len(calc)} != {len(observed)}")
    for key, expected in calc.items():
        actual = observed.get(key)
        if not actual:
            continue
        for metric in [
            "hit_at_5",
            "hit_at_10",
            "mrr",
            "action_leakage_rate",
            "forbidden_top1_rate",
            "cross_bucket_violation_rate",
            "warning_coverage_risk",
            "clickback_coverage",
            "hash_coverage",
            "adapter_coverage",
            "receipt_coverage",
            "stale_detection_rate",
        ]:
            if str(actual.get(metric)) != str(expected.get(metric)):
                add_error(errors, "summary_metric_mismatch", f"{key}:{metric}: {actual.get(metric)} != {expected.get(metric)}")
    return {"summary_count": len(summary_rows), "recomputed_summary_count": len(calc)}


def validate_metric_dictionary(errors: list[dict]) -> dict:
    payload = read_json(METRIC_DICT_JSON)
    metrics = {item.get("metric") for item in payload.get("metrics", [])}
    required = {
        "hit_at_5",
        "hit_at_10",
        "mrr",
        "action_leakage_rate",
        "forbidden_top1_rate",
        "cross_bucket_violation_rate",
        "warning_coverage_risk",
        "clickback_coverage",
        "hash_coverage",
        "receipt_coverage",
        "stale_detection_rate",
    }
    missing = sorted(required - metrics)
    if missing:
        add_error(errors, "metric_dictionary_missing", ",".join(missing))
    return {"metric_count": len(metrics)}


def validate_worktree(errors: list[dict]) -> dict:
    proc = subprocess.run(
        ["git", "status", "--porcelain", "--", "SOURCE_INTAKE.md", "IMPLEMENTATION_BLUEPRINT.md", "DEV_CONTEXT.md", "MEMORY_TIER.md", str(SANDBOX_DIR.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--", str(SANDBOX_DIR.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
    ).stdout.splitlines()
    staged = [line for line in staged if line.strip()]
    if staged:
        add_error(errors, "unexpected_staged_paths", ",".join(staged))
    return {"status": proc.stdout.splitlines(), "staged_paths": staged}


def write_report(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_p0_query_level_replay_check",
        f"status: {result['p0_query_replay_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: query_replay_not_mainline_decision",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B P0 Query-Level Replay Check",
        "",
        "## Result",
        "",
        "```text",
        f"p0 query replay check status: {result['p0_query_replay_check_status']}",
        f"error count: {result['error_count']}",
        f"replay rows: {result['counts']['replay_rows']}",
        f"query metric rows: {result['query_metrics']['query_metric_count']}",
        f"summary rows: {result['summary']['summary_count']}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "Adds query-level replay and metric definitions.",
        "Does not run original Yuxi runtime.",
        "Does not create a fresh blind holdout.",
        "Does not approve C-lite, writeback, action basis, or runtime adoption.",
        "```",
        "",
        "## Errors",
        "",
    ]
    if result["errors"]:
        for error in result["errors"]:
            lines.append(f"- {error['code']}: {error['detail']}")
    else:
        lines.append("- none")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def validate_all() -> dict:
    errors: list[dict] = []
    artifacts = validate_artifacts(errors)
    replay_rows = read_csv(REPLAY_PATH)
    query_rows = read_csv(QUERY_METRICS_PATH)
    summary_rows = read_csv(SUMMARY_PATH)
    query_metrics = validate_query_metrics(errors, replay_rows, query_rows)
    summary = validate_summary(errors, query_rows, summary_rows)
    dictionary = validate_metric_dictionary(errors)
    worktree = validate_worktree(errors)
    result = {
        "p0_query_replay_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "counts": {"replay_rows": len(replay_rows)},
        "artifacts": artifacts,
        "query_metrics": query_metrics,
        "summary": summary,
        "metric_dictionary": dictionary,
        "worktree": worktree,
    }
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(result)
    return result


def main() -> int:
    result = validate_all()
    print(f"p0 query replay check status: {result['p0_query_replay_check_status']}")
    print(f"error count: {result['error_count']}")
    print(f"replay rows: {result['counts']['replay_rows']}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
