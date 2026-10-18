import json
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
CASES_PATH = RESULTS_DIR / "phase_b_p1_promotion_gate_calibration_cases.jsonl"
EVALS_PATH = RESULTS_DIR / "phase_b_p1_promotion_gate_calibration_evaluations.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_p1_promotion_gate_calibration_summary.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_P1_PROMOTION_GATE_CALIBRATION_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_p1_promotion_gate_calibration_check.json"


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_report(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_p1_promotion_gate_calibration_check",
        f"status: {result['calibration_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: synthetic_gate_calibration_not_promotion",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B P1 Promotion Gate Calibration Check",
        "",
        "## Result",
        "",
        "```text",
        f"status: {result['calibration_check_status']}",
        f"error count: {result['error_count']}",
        f"case count: {result['case_count']}",
        f"evaluation count: {result['evaluation_count']}",
        "```",
        "",
        "## Errors",
        "",
    ]
    if result["errors"]:
        lines.extend(f"- {item['code']}: {item['detail']}" for item in result["errors"][:80])
    else:
        lines.append("- none")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    errors: list[dict] = []
    required = [CASES_PATH, EVALS_PATH, SUMMARY_PATH, SANDBOX_DIR / "PHASE_B_P1_PROMOTION_GATE_CALIBRATION_REPORT.md"]
    for path in required:
        if not path.exists():
            add_error(errors, "missing_artifact", str(path))
        elif path.stat().st_size == 0:
            add_error(errors, "empty_artifact", str(path))
    cases = load_jsonl(CASES_PATH) if CASES_PATH.exists() else []
    evals = load_jsonl(EVALS_PATH) if EVALS_PATH.exists() else []
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8")) if SUMMARY_PATH.exists() else {}

    if len(cases) != 24:
        add_error(errors, "case_count_mismatch", str(len(cases)))
    if len(evals) != 24:
        add_error(errors, "evaluation_count_mismatch", str(len(evals)))
    if len({case.get("case_id") for case in cases}) != len(cases):
        add_error(errors, "duplicate_case_ids", "cases")
    if {case.get("case_id") for case in cases} != {item.get("case_id") for item in evals}:
        add_error(errors, "case_eval_id_mismatch", "case/eval sets differ")

    positives = [item for item in evals if item.get("expected") == "allow_manual_promotion_candidate"]
    negatives = [item for item in evals if item.get("expected") == "blocked"]
    if len(positives) != 12 or len(negatives) != 12:
        add_error(errors, "positive_negative_count_mismatch", f"{len(positives)} / {len(negatives)}")
    false_positive = [item["case_id"] for item in negatives if item.get("gate_status") != "blocked"]
    false_negative = [item["case_id"] for item in positives if item.get("gate_status") != "allow_manual_promotion_candidate"]
    if false_positive:
        add_error(errors, "false_positive", ",".join(false_positive))
    if len(false_negative) > 2:
        add_error(errors, "true_positive_rate_below_0_8", ",".join(false_negative))
    for item in evals:
        for key in [
            "action_basis_allowed",
            "automatic_promotion_allowed",
            "formal_writeback_allowed",
            "truth_confidence_change_allowed",
            "reviewed_relation_creation_allowed",
        ]:
            if item.get(key) is not False:
                add_error(errors, f"{key}_leak", item.get("case_id", ""))
        if item.get("expected") == "blocked":
            expected_blocker = item.get("expected_blocker")
            if expected_blocker and expected_blocker not in set(item.get("blockers") or []):
                add_error(errors, "missing_expected_blocker", f"{item.get('case_id')}:{expected_blocker}")

    expected_zero = [
        "action_basis_allowed_count",
        "automatic_promotion_allowed_count",
        "formal_writeback_allowed_count",
        "truth_confidence_change_allowed_count",
        "reviewed_relation_creation_allowed_count",
    ]
    for key in expected_zero:
        if int(summary.get(key) or 0) != 0:
            add_error(errors, f"summary_{key}_leak", str(summary.get(key)))
    if summary.get("calibration_status") != "pass":
        add_error(errors, "summary_status_not_pass", str(summary.get("calibration_status")))
    result = {
        "calibration_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "case_count": len(cases),
        "evaluation_count": len(evals),
        "summary": summary,
    }
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(result)
    print(f"promotion gate calibration check status: {result['calibration_check_status']}")
    print(f"error count: {result['error_count']}")


if __name__ == "__main__":
    main()
