import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

QUERY_FILE = SANDBOX_DIR / "queries_phase_b_blind_relevance.jsonl"
RUN_MANIFEST_JSON = RESULTS_DIR / "phase_b_blind_relevance_manifest.json"
QUERY_MANIFEST_CSV = RESULTS_DIR / "phase_b_blind_relevance_query_manifest.csv"
TOP20_ITEMS_CSV = RESULTS_DIR / "phase_b_blind_relevance_top20_items.csv"
JUDGMENT_PACKET_CSV = RESULTS_DIR / "phase_b_blind_relevance_judgment_packet.csv"
JUDGMENTS_CSV = RESULTS_DIR / "phase_b_blind_relevance_judgments.csv"
JUDGED_SUMMARY_CSV = RESULTS_DIR / "phase_b_blind_relevance_judged_summary.csv"
CHECK_JSON = RESULTS_DIR / "phase_b_blind_relevance_check.json"
CHECK_MD = SANDBOX_DIR / "PHASE_B_BLIND_RELEVANCE_CHECK.md"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_BLIND_RELEVANCE_PILOT_REPORT.md"

VALID_GRADES = {"0", "1", "2"}


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def validate_artifacts(errors: list[dict]) -> dict:
    required = [
        QUERY_FILE,
        RUN_MANIFEST_JSON,
        QUERY_MANIFEST_CSV,
        TOP20_ITEMS_CSV,
        JUDGMENT_PACKET_CSV,
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


def validate_packet(errors: list[dict], manifest: dict, query_rows: list[dict], top20_rows: list[dict], packet_rows: list[dict]) -> dict:
    run_id = manifest.get("run_id")
    for name, rows in {"query_manifest": query_rows, "top20": top20_rows, "packet": packet_rows}.items():
        ids = {row.get("run_id") for row in rows}
        if ids != {run_id}:
            add_error(errors, "run_id_mismatch", f"{name}: {sorted(ids)} != {run_id}")
    query_count = int(manifest.get("query_count") or 0)
    expected_top20 = query_count * len(manifest.get("corpora") or []) * len(manifest.get("modes") or []) * int(
        manifest.get("top_k") or 0
    )
    expected_packet = query_count * len(manifest.get("corpora") or []) * len(manifest.get("modes") or []) * int(
        manifest.get("judgment_k") or 0
    )
    if len(top20_rows) != expected_top20:
        add_error(errors, "top20_row_count_mismatch", f"{len(top20_rows)} != {expected_top20}")
    if len(packet_rows) != expected_packet:
        add_error(errors, "packet_row_count_mismatch", f"{len(packet_rows)} != {expected_packet}")
    packet_ids = [row["judgment_id"] for row in packet_rows]
    if len(set(packet_ids)) != len(packet_ids):
        add_error(errors, "duplicate_judgment_ids", f"{len(set(packet_ids))} != {len(packet_ids)}")
    hard_stops = set(manifest.get("hard_stops") or [])
    for required in [
        "internal_no_parent_context_is_not_external_human_blind",
        "judgment_packet_is_not_completed_judgment",
        "does_not_validate_original_yuxi_runtime",
        "does_not_approve_c_lite_or_writeback",
    ]:
        if required not in hard_stops:
            add_error(errors, "missing_manifest_hard_stop", required)
    return {
        "query_count": query_count,
        "top20_rows": len(top20_rows),
        "judgment_packet_rows": len(packet_rows),
        "expected_judgment_packet_rows": expected_packet,
    }


def dcg(grades: list[int]) -> float:
    return sum(((2**grade - 1) / math.log2(idx + 2)) for idx, grade in enumerate(grades))


def summarize_judgments(judgments: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in judgments:
        grouped[(row["corpus"], row["mode"], row["query_id"])].append(row)
    per_query = []
    for (corpus, mode, query_id), rows in grouped.items():
        rows.sort(key=lambda row: int(row["rank"]))
        grades = [int(row["judged_relevance"]) for row in rows]
        binary = [grade >= 2 for grade in grades]
        first_rel = next((idx + 1 for idx, grade in enumerate(grades) if grade >= 2), 0)
        ideal = sorted(grades, reverse=True)
        per_query.append(
            {
                "corpus": corpus,
                "mode": mode,
                "query_id": query_id,
                "relevant_at_5": sum(1 for grade in grades if grade >= 2),
                "borderline_at_5": sum(1 for grade in grades if grade == 1),
                "judged_mrr_at_5": 1.0 / first_rel if first_rel else 0.0,
                "ndcg_at_5": (dcg(grades) / dcg(ideal)) if dcg(ideal) else 0.0,
                "has_relevant_at_5": any(binary),
            }
        )
    summary_grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in per_query:
        summary_grouped[(row["corpus"], row["mode"])].append(row)
    summary = []
    for (corpus, mode), rows in sorted(summary_grouped.items()):
        summary.append(
            {
                "corpus": corpus,
                "mode": mode,
                "queries": len(rows),
                "hit_at_5_judged": f"{sum(1 for row in rows if row['has_relevant_at_5'])}/{len(rows)}",
                "mean_relevant_at_5": f"{statistics.mean(row['relevant_at_5'] for row in rows):.4f}",
                "mean_borderline_at_5": f"{statistics.mean(row['borderline_at_5'] for row in rows):.4f}",
                "judged_mrr_at_5": f"{statistics.mean(row['judged_mrr_at_5'] for row in rows):.4f}",
                "ndcg_at_5": f"{statistics.mean(row['ndcg_at_5'] for row in rows):.4f}",
            }
        )
    return summary


def validate_judgments(errors: list[dict], packet_rows: list[dict]) -> dict:
    if not JUDGMENTS_CSV.exists():
        return {
            "judgment_status": "pending",
            "judgment_rows": 0,
            "missing_judgment_rows": len(packet_rows),
            "summary_rows": 0,
        }
    judgments = read_csv(JUDGMENTS_CSV)
    packet_by_id = {row["judgment_id"]: row for row in packet_rows}
    judgment_by_id = {row["judgment_id"]: row for row in judgments}
    missing = sorted(set(packet_by_id) - set(judgment_by_id))
    extra = sorted(set(judgment_by_id) - set(packet_by_id))
    if missing:
        add_error(errors, "missing_judgments", f"{len(missing)} missing; first={missing[:5]}")
    if extra:
        add_error(errors, "extra_judgments", f"{len(extra)} extra; first={extra[:5]}")
    bad_grades = [
        row["judgment_id"]
        for row in judgments
        if str(row.get("judged_relevance", "")).strip() not in VALID_GRADES
    ]
    if bad_grades:
        add_error(errors, "bad_judged_relevance", f"{len(bad_grades)} bad; first={bad_grades[:5]}")
    missing_basis = [row["judgment_id"] for row in judgments if not row.get("judgment_basis")]
    if missing_basis:
        add_error(errors, "missing_judgment_basis", f"{len(missing_basis)} missing; first={missing_basis[:5]}")
    if not missing and not extra and not bad_grades and not missing_basis:
        summary = summarize_judgments(judgments)
        write_csv(JUDGED_SUMMARY_CSV, summary)
        judge_ids = {row.get("judge_id", "") for row in judgments}
        if judge_ids == {"codex_internal_heuristic_judge_v1"}:
            status = "complete_internal_only"
        else:
            status = "complete"
    else:
        summary = []
        status = "invalid"
    return {
        "judgment_status": status,
        "judgment_rows": len(judgments),
        "missing_judgment_rows": len(missing),
        "summary_rows": len(summary),
    }


def write_report(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_blind_relevance_check",
        f"status: {result['blind_relevance_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: blind_relevance_check_not_external_human_judgment",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Blind Relevance Check",
        "",
        "## Result",
        "",
        "```text",
        f"status: {result['blind_relevance_check_status']}",
        f"error count: {result['error_count']}",
        f"query count: {result['packet']['query_count']}",
        f"judgment packet rows: {result['packet']['judgment_packet_rows']}",
        f"judgment status: {result['judgments']['judgment_status']}",
        f"judgment rows: {result['judgments']['judgment_rows']}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "This is a relevance-judgment scaffold and internal blind packet unless an external human/model judge fills the judgment file.",
        "complete_internal_only means only the internal heuristic/model-assisted judgment is complete.",
        "It does not validate original Yuxi runtime or C-lite.",
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
    query_rows = read_csv(QUERY_MANIFEST_CSV) if QUERY_MANIFEST_CSV.exists() else []
    top20_rows = read_csv(TOP20_ITEMS_CSV) if TOP20_ITEMS_CSV.exists() else []
    packet_rows = read_csv(JUDGMENT_PACKET_CSV) if JUDGMENT_PACKET_CSV.exists() else []
    packet = validate_packet(errors, manifest, query_rows, top20_rows, packet_rows) if manifest else {}
    judgments = validate_judgments(errors, packet_rows) if packet_rows else {}
    status = "pass" if not errors else "fail"
    if judgments.get("judgment_status") == "pending" and not errors:
        status = "pending_judgment"
    result = {
        "blind_relevance_check_status": status,
        "error_count": len(errors),
        "errors": errors,
        "artifacts": artifacts,
        "packet": packet,
        "judgments": judgments,
    }
    CHECK_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(result)
    print(f"blind relevance check status: {status}")
    print(f"error count: {len(errors)}")
    print(f"judgment status: {judgments.get('judgment_status')}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
