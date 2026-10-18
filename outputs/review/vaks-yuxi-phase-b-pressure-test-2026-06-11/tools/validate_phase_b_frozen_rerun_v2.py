import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

RUN_MANIFEST_JSON = RESULTS_DIR / "phase_b_frozen_rerun_v2_manifest.json"
CORPUS_MANIFEST_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_corpus_manifest.csv"
QUERY_MANIFEST_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_query_manifest.csv"
TOP20_ITEMS_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_top20_items.csv"
TOP1_10_REPLAY_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_top1_10_replay.csv"
TOP11_20_RECEIPTS_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_top11_20_receipts.csv"
QUERY_METRICS_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_query_metrics.csv"
SUMMARY_CSV = RESULTS_DIR / "phase_b_frozen_rerun_v2_summary.csv"
CHECK_JSON = RESULTS_DIR / "phase_b_frozen_rerun_v2_check.json"
CHECK_MD = SANDBOX_DIR / "PHASE_B_FROZEN_RERUN_V2_CHECK.md"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_FROZEN_RERUN_V2_REPORT.md"

SUPPORT_BUCKETS = {"core_framework", "reviewed"}
RISK_BUCKETS = {"raw", "candidate", "summary", "qa", "overlay", "feedback", "diagnostic", "unknown"}
TOP_K = 20
GOVERNANCE_K = 10


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def b(value) -> bool:
    return str(value).lower() == "true"


def f4(value: float) -> str:
    return f"{value:.4f}"


def avg_bool(values: list[bool]) -> float:
    if not values:
        return 0.0
    return sum(1 for value in values if value) / len(values)


def validate_artifacts(errors: list[dict]) -> dict:
    required = [
        RUN_MANIFEST_JSON,
        CORPUS_MANIFEST_CSV,
        QUERY_MANIFEST_CSV,
        TOP20_ITEMS_CSV,
        TOP1_10_REPLAY_CSV,
        TOP11_20_RECEIPTS_CSV,
        QUERY_METRICS_CSV,
        SUMMARY_CSV,
        REPORT_PATH,
    ]
    artifacts = []
    for path in required:
        exists = path.exists()
        artifacts.append(
            {"path": str(path.relative_to(SANDBOX_DIR)), "exists": exists, "bytes": path.stat().st_size if exists else 0}
        )
        if not exists:
            add_error(errors, "missing_artifact", str(path))
        elif path.stat().st_size == 0:
            add_error(errors, "empty_artifact", str(path))
    return {"artifacts": artifacts}


def run_id_set(rows: list[dict]) -> set[str]:
    return {row.get("run_id", "") for row in rows}


def validate_run_identity(errors: list[dict], manifest: dict, datasets: dict[str, list[dict]]) -> dict:
    run_id = manifest.get("run_id")
    if not run_id:
        add_error(errors, "manifest_missing_run_id", "")
    observed = {}
    for name, rows in datasets.items():
        ids = run_id_set(rows)
        observed[name] = sorted(ids)
        if ids != {run_id}:
            add_error(errors, "run_id_mismatch", f"{name}: {sorted(ids)} != {run_id}")
    return {"run_id": run_id, "observed": observed}


def validate_split_exports(errors: list[dict], top20: list[dict], top10: list[dict], top11_20: list[dict]) -> dict:
    top20_keys = {
        (row["run_id"], row["test_set"], row["corpus"], row["mode"], row["query_id"], row["rank"], row["path"], row["heading"])
        for row in top20
    }
    top10_keys = {
        (row["run_id"], row["test_set"], row["corpus"], row["mode"], row["query_id"], row["rank"], row["path"], row["heading"])
        for row in top10
    }
    top11_20_keys = {
        (row["run_id"], row["test_set"], row["corpus"], row["mode"], row["query_id"], row["rank"], row["path"], row["heading"])
        for row in top11_20
    }
    expected_top10 = {
        (row["run_id"], row["test_set"], row["corpus"], row["mode"], row["query_id"], row["rank"], row["path"], row["heading"])
        for row in top20
        if int(row["rank"]) <= 10
    }
    expected_top11_20 = {
        (row["run_id"], row["test_set"], row["corpus"], row["mode"], row["query_id"], row["rank"], row["path"], row["heading"])
        for row in top20
        if 11 <= int(row["rank"]) <= 20
    }
    if top10_keys != expected_top10:
        add_error(errors, "top1_10_split_mismatch", f"{len(top10_keys)} != {len(expected_top10)}")
    if top11_20_keys != expected_top11_20:
        add_error(errors, "top11_20_split_mismatch", f"{len(top11_20_keys)} != {len(expected_top11_20)}")
    if len(top20_keys) != len(top20):
        add_error(errors, "duplicate_top20_item_keys", f"{len(top20_keys)} != {len(top20)}")
    return {"top20_rows": len(top20), "top1_10_rows": len(top10), "top11_20_rows": len(top11_20)}


def recompute_query_metrics(top20_rows: list[dict]) -> dict[tuple[str, str, str, str], dict]:
    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for row in top20_rows:
        grouped[(row["test_set"], row["corpus"], row["mode"], row["query_id"])].append(row)

    metrics = {}
    for key, rows in grouped.items():
        rows.sort(key=lambda row: int(row["rank"]))
        ranks = [int(row["rank"]) for row in rows]
        top10 = rows[:GOVERNANCE_K]
        first_hit = 0
        for row in rows:
            if b(row["result_hits_expected"]):
                first_hit = int(row["rank"])
                break
        intent = rows[0]["intent"]
        risk = [row for row in top10 if row["bucket"] in RISK_BUCKETS]
        support_ranks = [int(row["rank"]) for row in top10 if row["bucket"] in SUPPORT_BUCKETS]
        if support_ranks:
            first_support = min(support_ranks)
            risky_before_support = sum(1 for row in risk if int(row["rank"]) < first_support)
        elif intent in {"action", "evidence"}:
            risky_before_support = len(risk)
        else:
            risky_before_support = 0
        forbidden_top1 = bool(intent in {"action", "evidence"} and top10 and top10[0]["bucket"] not in SUPPORT_BUCKETS)
        unlabelled_risky = [row for row in risk if not row.get("warning_code")]
        action_leakage = bool(intent in {"action", "evidence"} and (forbidden_top1 or unlabelled_risky))
        stale_exposed = [row for row in top10 if b(row.get("stale", ""))]
        stale_detected = [row for row in stale_exposed if "stale_index" in row.get("warning_code", "")]
        metrics[key] = {
            "test_set": key[0],
            "corpus": key[1],
            "mode": key[2],
            "query_id": key[3],
            "group": rows[0]["query_group"],
            "intent": intent,
            "rank_window": ranks,
            "hit_at_5": bool(first_hit and first_hit <= 5),
            "hit_at_10": bool(first_hit and first_hit <= 10),
            "mrr": 1.0 / first_hit if first_hit else 0.0,
            "first_hit_rank": str(first_hit or ""),
            "dangerous_exposed_top10": len(risk),
            "warning_coverage": (sum(1 for row in risk if row.get("warning_code")) / len(risk)) if risk else 1.0,
            "action_leakage": action_leakage,
            "forbidden_top1": forbidden_top1,
            "cross_bucket_authority_violation": bool(intent in {"action", "evidence"} and risky_before_support),
            "clickback_coverage": avg_bool([b(row.get("clickback_present", "")) for row in top10]),
            "hash_coverage": avg_bool([b(row.get("hash_present", "")) for row in top10]),
            "adapter_coverage": avg_bool([b(row.get("adapter_present", "")) for row in top10]),
            "receipt_coverage": avg_bool([b(row.get("receipt_present", "")) for row in top10]),
            "stale_exposed": len(stale_exposed),
            "stale_detected": len(stale_detected),
            "top1_bucket": top10[0]["bucket"] if top10 else "",
            "top1_path": top10[0]["path"] if top10 else "",
            "top1_warning": top10[0].get("warning_code", "") if top10 else "",
        }
    return metrics


def validate_query_metrics(errors: list[dict], top20_rows: list[dict], query_rows: list[dict]) -> dict:
    calc = recompute_query_metrics(top20_rows)
    observed = {(row["test_set"], row["corpus"], row["mode"], row["query_id"]): row for row in query_rows}
    if set(calc) != set(observed):
        add_error(errors, "query_metric_key_set_mismatch", f"{len(calc)} != {len(observed)}")
    incomplete_rank_windows = 0
    mismatch_count = 0
    for key, expected in calc.items():
        if expected["rank_window"] != list(range(1, TOP_K + 1)):
            incomplete_rank_windows += 1
            if incomplete_rank_windows <= 20:
                add_error(errors, "rank_window_incomplete", f"{key}:{expected['rank_window']}")
        actual = observed.get(key)
        if not actual:
            continue
        checks = {
            "hit_at_5": b(actual.get("hit_at_5")) == expected["hit_at_5"],
            "hit_at_10": b(actual.get("hit_at_10")) == expected["hit_at_10"],
            "action_leakage": b(actual.get("action_leakage")) == expected["action_leakage"],
            "forbidden_top1": b(actual.get("forbidden_top1")) == expected["forbidden_top1"],
            "cross_bucket_authority_violation": b(actual.get("cross_bucket_authority_violation"))
            == expected["cross_bucket_authority_violation"],
            "first_hit_rank": str(actual.get("first_hit_rank") or "") == expected["first_hit_rank"],
            "dangerous_exposed_top10": int(actual.get("dangerous_exposed_top10") or 0)
            == expected["dangerous_exposed_top10"],
            "stale_exposed": int(actual.get("stale_exposed") or 0) == expected["stale_exposed"],
            "stale_detected": int(actual.get("stale_detected") or 0) == expected["stale_detected"],
            "top1_bucket": str(actual.get("top1_bucket") or "") == expected["top1_bucket"],
            "top1_path": str(actual.get("top1_path") or "") == expected["top1_path"],
            "top1_warning": str(actual.get("top1_warning") or "") == expected["top1_warning"],
        }
        float_checks = {
            "mrr": abs(float(actual.get("mrr") or 0.0) - expected["mrr"]) <= 1e-9,
            "warning_coverage": abs(float(actual.get("warning_coverage") or 0.0) - expected["warning_coverage"]) <= 1e-9,
            "clickback_coverage": abs(float(actual.get("clickback_coverage") or 0.0) - expected["clickback_coverage"]) <= 1e-9,
            "hash_coverage": abs(float(actual.get("hash_coverage") or 0.0) - expected["hash_coverage"]) <= 1e-9,
            "adapter_coverage": abs(float(actual.get("adapter_coverage") or 0.0) - expected["adapter_coverage"]) <= 1e-9,
            "receipt_coverage": abs(float(actual.get("receipt_coverage") or 0.0) - expected["receipt_coverage"]) <= 1e-9,
        }
        for name, passed in {**checks, **float_checks}.items():
            if not passed:
                mismatch_count += 1
                if mismatch_count <= 50:
                    add_error(errors, "query_metric_mismatch", f"{key}:{name}")
    return {
        "query_metric_rows": len(query_rows),
        "recomputed_query_metric_rows": len(calc),
        "incomplete_rank_windows": incomplete_rank_windows,
        "metric_mismatch_count": mismatch_count,
    }


def recompute_summary(query_rows: list[dict]) -> dict[tuple[str, str, str], dict]:
    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in query_rows:
        grouped[(row["test_set"], row["corpus"], row["mode"])].append(row)
    summary = {}
    for key, rows in grouped.items():
        resolvable = [row for row in rows if b(row.get("resolvable"))]
        base = resolvable or rows
        risk = [row for row in rows if row["intent"] in {"action", "evidence"}]
        stale = [row for row in rows if row["group"] in {"stale_pressure", "holdout_stale"}]
        stale_exposed = sum(int(row.get("stale_exposed") or 0) for row in stale)
        stale_detected = sum(int(row.get("stale_detected") or 0) for row in stale)
        summary[key] = {
            "run_id": rows[0]["run_id"],
            "test_set": key[0],
            "corpus": key[1],
            "mode": key[2],
            "queries": str(len(rows)),
            "resolvable_queries": str(len(resolvable)),
            "hit_at_5": f"{sum(1 for row in base if b(row.get('hit_at_5')) )}/{len(base)}",
            "hit_at_10": f"{sum(1 for row in base if b(row.get('hit_at_10')) )}/{len(base)}",
            "mrr": f4(statistics.mean(float(row.get("mrr") or 0.0) for row in base)),
            "action_leakage_rate": f4(avg_bool([b(row.get("action_leakage")) for row in risk])) if risk else "0.0000",
            "forbidden_top1_rate": f4(avg_bool([b(row.get("forbidden_top1")) for row in risk])) if risk else "0.0000",
            "cross_bucket_violation_rate": f4(avg_bool([b(row.get("cross_bucket_authority_violation")) for row in risk]))
            if risk
            else "0.0000",
            "warning_coverage_risk": f4(statistics.mean(float(row.get("warning_coverage") or 0.0) for row in risk))
            if risk
            else "1.0000",
            "clickback_coverage": f4(statistics.mean(float(row.get("clickback_coverage") or 0.0) for row in rows)),
            "hash_coverage": f4(statistics.mean(float(row.get("hash_coverage") or 0.0) for row in rows)),
            "adapter_coverage": f4(statistics.mean(float(row.get("adapter_coverage") or 0.0) for row in rows)),
            "receipt_coverage": f4(statistics.mean(float(row.get("receipt_coverage") or 0.0) for row in rows)),
            "stale_detection_rate": f4((stale_detected / stale_exposed) if stale_exposed else 0.0),
        }
    return summary


def validate_summary(errors: list[dict], query_rows: list[dict], summary_rows: list[dict]) -> dict:
    calc = recompute_summary(query_rows)
    observed = {(row["test_set"], row["corpus"], row["mode"]): row for row in summary_rows}
    if set(calc) != set(observed):
        add_error(errors, "summary_key_set_mismatch", f"{len(calc)} != {len(observed)}")
    mismatch_count = 0
    fields = [
        "run_id",
        "queries",
        "resolvable_queries",
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
    ]
    for key, expected in calc.items():
        actual = observed.get(key)
        if not actual:
            continue
        for field in fields:
            if str(actual.get(field, "")) != str(expected.get(field, "")):
                mismatch_count += 1
                if mismatch_count <= 50:
                    add_error(errors, "summary_mismatch", f"{key}:{field}:{actual.get(field)} != {expected.get(field)}")
    return {"summary_rows": len(summary_rows), "recomputed_summary_rows": len(calc), "summary_mismatch_count": mismatch_count}


def validate_manifests(errors: list[dict], manifest: dict, corpus_rows: list[dict], query_manifest_rows: list[dict]) -> dict:
    if manifest.get("artifact_kind") != "phase_b_frozen_rerun_v2_manifest":
        add_error(errors, "bad_manifest_artifact_kind", str(manifest.get("artifact_kind")))
    if manifest.get("corpus_file_records") != len(corpus_rows):
        add_error(errors, "manifest_corpus_count_mismatch", f"{manifest.get('corpus_file_records')} != {len(corpus_rows)}")
    if manifest.get("query_records") != len(query_manifest_rows):
        add_error(errors, "manifest_query_count_mismatch", f"{manifest.get('query_records')} != {len(query_manifest_rows)}")
    corpus_keys = {(row["run_id"], row["corpus"], row["path"]) for row in corpus_rows}
    query_keys = {(row["run_id"], row["test_set"], row["query_id"]) for row in query_manifest_rows}
    if len(corpus_keys) != len(corpus_rows):
        add_error(errors, "duplicate_corpus_manifest_keys", f"{len(corpus_keys)} != {len(corpus_rows)}")
    if len(query_keys) != len(query_manifest_rows):
        add_error(errors, "duplicate_query_manifest_keys", f"{len(query_keys)} != {len(query_manifest_rows)}")
    hard_stops = set(manifest.get("hard_stops") or [])
    for required in [
        "does_not_validate_original_yuxi_runtime",
        "does_not_create_relevance_judgment",
        "does_not_approve_c_lite_or_writeback",
    ]:
        if required not in hard_stops:
            add_error(errors, "missing_manifest_hard_stop", required)
    return {"corpus_manifest_rows": len(corpus_rows), "query_manifest_rows": len(query_manifest_rows)}


def write_report(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_frozen_rerun_v2_check",
        f"status: {result['frozen_rerun_v2_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: single_run_consistency_check_not_runtime_validation",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Frozen Rerun V2 Check",
        "",
        "## Result",
        "",
        "```text",
        f"status: {result['frozen_rerun_v2_check_status']}",
        f"error count: {result['error_count']}",
        f"run_id: {result['run_identity']['run_id']}",
        f"top20 rows: {result['split_exports']['top20_rows']}",
        f"query metric rows: {result['query_metrics']['query_metric_rows']}",
        f"summary rows: {result['summary']['summary_rows']}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "This checks exact cross-artifact consistency inside one local frozen rerun bundle.",
        "It does not add human relevance judgment.",
        "It does not validate original Yuxi runtime.",
        "It does not approve C-lite, writeback, action basis, or core-doc strong conclusions.",
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


def main() -> int:
    errors: list[dict] = []
    artifacts = validate_artifacts(errors)
    manifest = read_json(RUN_MANIFEST_JSON) if RUN_MANIFEST_JSON.exists() else {}
    corpus_rows = read_csv(CORPUS_MANIFEST_CSV) if CORPUS_MANIFEST_CSV.exists() else []
    query_manifest_rows = read_csv(QUERY_MANIFEST_CSV) if QUERY_MANIFEST_CSV.exists() else []
    top20_rows = read_csv(TOP20_ITEMS_CSV) if TOP20_ITEMS_CSV.exists() else []
    top10_rows = read_csv(TOP1_10_REPLAY_CSV) if TOP1_10_REPLAY_CSV.exists() else []
    top11_20_rows = read_csv(TOP11_20_RECEIPTS_CSV) if TOP11_20_RECEIPTS_CSV.exists() else []
    query_rows = read_csv(QUERY_METRICS_CSV) if QUERY_METRICS_CSV.exists() else []
    summary_rows = read_csv(SUMMARY_CSV) if SUMMARY_CSV.exists() else []
    datasets = {
        "corpus_manifest": corpus_rows,
        "query_manifest": query_manifest_rows,
        "top20_items": top20_rows,
        "top1_10_replay": top10_rows,
        "top11_20_receipts": top11_20_rows,
        "query_metrics": query_rows,
        "summary": summary_rows,
    }
    run_identity = validate_run_identity(errors, manifest, datasets) if manifest else {"run_id": ""}
    manifest_check = validate_manifests(errors, manifest, corpus_rows, query_manifest_rows) if manifest else {}
    split_exports = validate_split_exports(errors, top20_rows, top10_rows, top11_20_rows)
    query_metrics = validate_query_metrics(errors, top20_rows, query_rows)
    summary = validate_summary(errors, query_rows, summary_rows)
    result = {
        "frozen_rerun_v2_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "artifacts": artifacts,
        "run_identity": run_identity,
        "manifest": manifest_check,
        "split_exports": split_exports,
        "query_metrics": query_metrics,
        "summary": summary,
    }
    CHECK_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(result)
    print(f"frozen rerun v2 check status: {result['frozen_rerun_v2_check_status']}")
    print(f"error count: {result['error_count']}")
    print(f"top20 rows: {split_exports['top20_rows']}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
