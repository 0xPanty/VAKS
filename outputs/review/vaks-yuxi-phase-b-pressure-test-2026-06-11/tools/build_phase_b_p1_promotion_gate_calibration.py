import json
from datetime import datetime, timezone
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
CASES_PATH = RESULTS_DIR / "phase_b_p1_promotion_gate_calibration_cases.jsonl"
EVALS_PATH = RESULTS_DIR / "phase_b_p1_promotion_gate_calibration_evaluations.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_p1_promotion_gate_calibration_summary.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_P1_PROMOTION_GATE_CALIBRATION_REPORT.md"


POSITIVE_CASES = [
    "reviewed_direct_anchor",
    "reviewed_two_source_support",
    "reviewed_scope_limited_pattern",
    "reviewed_decision_support",
    "reviewed_relation_edge_support",
    "reviewed_source_refresh_passed",
    "reviewed_counterevidence_addressed",
    "reviewed_temporal_current",
    "reviewed_action_warrant_present",
    "reviewed_approval_integrity_checked",
    "reviewed_clickback_hash_receipt_present",
    "reviewed_feedback_review_due_resolved",
]

NEGATIVE_CASES = [
    ("simulation_only", "simulation_only_not_reviewed_support"),
    ("missing_source_anchor", "missing_source_anchor"),
    ("not_human_reviewed", "human_review_required"),
    ("support_like_metadata_only", "support_like_metadata_not_human_reviewed"),
    ("counterexample_unresolved", "counterexample_requires_review"),
    ("stale_source_unresolved", "source_refresh_needed"),
    ("eval_score_only", "eval_score_not_evidence_support"),
    ("feedback_only", "feedback_not_truth"),
    ("graph_edge_only", "graph_edge_not_reviewed_relation"),
    ("context_pack_no_warrant", "missing_warrant"),
    ("approval_not_specific", "approval_integrity_not_checked"),
    ("auto_writeback_requested", "automatic_promotion_forbidden"),
]


def positive_case(idx: int, name: str) -> dict:
    return {
        "case_id": f"pg_pos_{idx:02d}_{name}",
        "expected": "allow_manual_promotion_candidate",
        "human_reviewed": True,
        "source_anchor_present": True,
        "evidence_packet_created": True,
        "evidence_sufficiency_passed": True,
        "approval_integrity_checked": True,
        "support_like_metadata_only": False,
        "counterexample_unresolved": False,
        "source_refresh_needed": False,
        "eval_score_only": False,
        "feedback_only": False,
        "graph_edge_only": False,
        "warrant_present": True,
        "automatic_promotion_requested": False,
        "reviewed_support_count": 1 + (idx % 2),
    }


def negative_case(idx: int, name: str, blocker: str) -> dict:
    case = positive_case(idx, name)
    case.update(
        {
            "case_id": f"pg_neg_{idx:02d}_{name}",
            "expected": "blocked",
            "expected_blocker": blocker,
        }
    )
    if blocker == "simulation_only_not_reviewed_support":
        case["simulation_only"] = True
        case["human_reviewed"] = False
    elif blocker == "missing_source_anchor":
        case["source_anchor_present"] = False
    elif blocker == "human_review_required":
        case["human_reviewed"] = False
    elif blocker == "support_like_metadata_not_human_reviewed":
        case["support_like_metadata_only"] = True
        case["reviewed_support_count"] = 0
    elif blocker == "counterexample_requires_review":
        case["counterexample_unresolved"] = True
    elif blocker == "source_refresh_needed":
        case["source_refresh_needed"] = True
    elif blocker == "eval_score_not_evidence_support":
        case["eval_score_only"] = True
        case["reviewed_support_count"] = 0
    elif blocker == "feedback_not_truth":
        case["feedback_only"] = True
        case["reviewed_support_count"] = 0
    elif blocker == "graph_edge_not_reviewed_relation":
        case["graph_edge_only"] = True
        case["reviewed_support_count"] = 0
    elif blocker == "missing_warrant":
        case["warrant_present"] = False
    elif blocker == "approval_integrity_not_checked":
        case["approval_integrity_checked"] = False
    elif blocker == "automatic_promotion_forbidden":
        case["automatic_promotion_requested"] = True
    return case


def blockers_for(case: dict) -> list[str]:
    blockers = []
    if case.get("simulation_only"):
        blockers.append("simulation_only_not_reviewed_support")
    if not case.get("source_anchor_present"):
        blockers.append("missing_source_anchor")
    if not case.get("human_reviewed"):
        blockers.append("human_review_required")
    if case.get("support_like_metadata_only"):
        blockers.append("support_like_metadata_not_human_reviewed")
    if case.get("counterexample_unresolved"):
        blockers.append("counterexample_requires_review")
    if case.get("source_refresh_needed"):
        blockers.append("source_refresh_needed")
    if case.get("eval_score_only"):
        blockers.append("eval_score_not_evidence_support")
    if case.get("feedback_only"):
        blockers.append("feedback_not_truth")
    if case.get("graph_edge_only"):
        blockers.append("graph_edge_not_reviewed_relation")
    if not case.get("warrant_present"):
        blockers.append("missing_warrant")
    if not case.get("approval_integrity_checked"):
        blockers.append("approval_integrity_not_checked")
    if case.get("automatic_promotion_requested"):
        blockers.append("automatic_promotion_forbidden")
    if not case.get("evidence_packet_created"):
        blockers.append("evidence_packet_not_created")
    if not case.get("evidence_sufficiency_passed"):
        blockers.append("evidence_sufficiency_not_passed")
    if int(case.get("reviewed_support_count") or 0) <= 0:
        blockers.append("reviewed_support_required")
    return list(dict.fromkeys(blockers))


def evaluate(case: dict, built_at: str) -> dict:
    blockers = blockers_for(case)
    allowed = not blockers
    return {
        "artifact_kind": "phase_b_p1_promotion_gate_calibration_evaluation",
        "case_id": case["case_id"],
        "expected": case["expected"],
        "truth_boundary": "synthetic_gate_calibration_not_promotion",
        "gate_status": "allow_manual_promotion_candidate" if allowed else "blocked",
        "blockers": blockers,
        "promotion_allowed": allowed,
        "action_basis_allowed": False,
        "automatic_promotion_allowed": False,
        "formal_writeback_allowed": False,
        "truth_confidence_change_allowed": False,
        "reviewed_relation_creation_allowed": False,
        "evidence_packet_created": bool(case.get("evidence_packet_created")),
        "evidence_sufficiency_passed": bool(case.get("evidence_sufficiency_passed")),
        "human_reviewed_support_count": int(case.get("reviewed_support_count") or 0) if case.get("human_reviewed") else 0,
        "reviewed_support_count": int(case.get("reviewed_support_count") or 0) if allowed else 0,
        "expected_blocker": case.get("expected_blocker", ""),
        "built_at": built_at,
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_report(summary: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_p1_promotion_gate_calibration_report",
        f"status: {summary['calibration_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: synthetic_gate_calibration_not_promotion",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B P1 Promotion Gate Calibration Report",
        "",
        "## Result",
        "",
        "```text",
        f"positive cases: {summary['positive_case_count']}",
        f"negative cases: {summary['negative_case_count']}",
        f"true positive rate: {summary['true_positive_rate']:.4f}",
        f"false positive rate: {summary['false_positive_rate']:.4f}",
        f"automatic promotion allowed: {summary['automatic_promotion_allowed_count']}",
        f"formal writeback allowed: {summary['formal_writeback_allowed_count']}",
        f"reviewed relation creation allowed: {summary['reviewed_relation_creation_allowed_count']}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "Synthetic calibration only.",
        "Positive means eligible for manual promotion candidate handling, not auto writeback.",
        "This rebuts the all-block rule-logic concern; it does not prove operational calibration on real mixed evidence packets.",
        "Does not create reviewed knowledge, truth confidence change, action basis, or reviewed relation.",
        "```",
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    cases = [positive_case(idx, name) for idx, name in enumerate(POSITIVE_CASES, start=1)]
    cases.extend(negative_case(idx, name, blocker) for idx, (name, blocker) in enumerate(NEGATIVE_CASES, start=1))
    evals = [evaluate(case, built_at) for case in cases]
    write_jsonl(CASES_PATH, cases)
    write_jsonl(EVALS_PATH, evals)
    positives = [item for item in evals if item["expected"] == "allow_manual_promotion_candidate"]
    negatives = [item for item in evals if item["expected"] == "blocked"]
    true_positive = sum(1 for item in positives if item["gate_status"] == "allow_manual_promotion_candidate")
    false_negative = len(positives) - true_positive
    false_positive = sum(1 for item in negatives if item["gate_status"] != "blocked")
    true_negative = len(negatives) - false_positive
    summary = {
        "artifact_kind": "phase_b_p1_promotion_gate_calibration_summary",
        "truth_boundary": "synthetic_gate_calibration_not_promotion",
        "calibration_status": "pass" if false_positive == 0 and true_positive / len(positives) >= 0.8 else "fail",
        "case_count": len(evals),
        "positive_case_count": len(positives),
        "negative_case_count": len(negatives),
        "true_positive_count": true_positive,
        "false_negative_count": false_negative,
        "true_negative_count": true_negative,
        "false_positive_count": false_positive,
        "true_positive_rate": true_positive / len(positives),
        "false_positive_rate": false_positive / len(negatives),
        "promotion_allowed_count": sum(1 for item in evals if item["promotion_allowed"]),
        "action_basis_allowed_count": sum(1 for item in evals if item["action_basis_allowed"]),
        "automatic_promotion_allowed_count": sum(1 for item in evals if item["automatic_promotion_allowed"]),
        "formal_writeback_allowed_count": sum(1 for item in evals if item["formal_writeback_allowed"]),
        "truth_confidence_change_allowed_count": sum(1 for item in evals if item["truth_confidence_change_allowed"]),
        "reviewed_relation_creation_allowed_count": sum(1 for item in evals if item["reviewed_relation_creation_allowed"]),
        "built_at": built_at,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(summary)
    print(f"promotion gate calibration status: {summary['calibration_status']}")
    print(f"TPR: {summary['true_positive_rate']:.4f}")
    print(f"FPR: {summary['false_positive_rate']:.4f}")


if __name__ == "__main__":
    main()
