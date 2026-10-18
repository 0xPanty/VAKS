import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
OUTCOMES_PATH = RESULTS_DIR / "phase_b_simulated_reviewer_outcomes.jsonl"
GATES_PATH = RESULTS_DIR / "phase_b_promotion_gate_evaluations.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_promotion_gate_evaluation_summary.json"


def load_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def support_like_counts(outcome: dict) -> dict:
    direct = 0
    inferential = 0
    counterexample = 0
    for item in outcome.get("simulated_item_outcomes") or []:
        support = item.get("simulated_evidence_support") or {}
        if support.get("span_supports_target") == "supported" and support.get("evidence_role") == "direct_support":
            direct += 1
        if support.get("span_supports_target") == "partial" and support.get("evidence_role") == "inferential_support":
            inferential += 1
        if support.get("evidence_role") == "counterexample":
            counterexample += 1
    return {
        "simulated_direct_support_count": direct,
        "simulated_inferential_support_count": inferential,
        "simulated_support_like_count": direct + inferential,
        "simulated_counterexample_count": counterexample,
    }


def blockers_for(outcome: dict, counts: dict) -> list[str]:
    blockers = [
        "human_review_required",
        "evidence_packet_not_created",
        "evidence_sufficiency_not_run",
        "approval_integrity_not_checked",
        "automatic_promotion_forbidden",
    ]
    if outcome.get("simulated_review_applied"):
        blockers.append("simulation_only_not_reviewed_support")
    if counts["simulated_support_like_count"] > 0:
        blockers.append("support_like_metadata_not_human_reviewed")
    if counts["simulated_counterexample_count"] > 0:
        blockers.append("counterexample_requires_review")
    if outcome.get("review_result") == "not_reviewed":
        blockers.append("source_packet_not_reviewed")
    if outcome.get("review_result") == "blocked_no_source_anchor":
        blockers.append("missing_source_anchor")
    if outcome.get("source_refresh_needed_count"):
        blockers.append("source_refresh_needed")
    return list(dict.fromkeys(blockers))


def build_gate(outcome: dict, built_at: str) -> dict:
    counts = support_like_counts(outcome)
    blockers = blockers_for(outcome, counts)
    return {
        "artifact_kind": "vaks_phase_b_promotion_gate_evaluation",
        "promotion_gate_id": outcome.get("outcome_id"),
        "source_outcome_id": outcome.get("outcome_id"),
        "source_review_packet_id": outcome.get("source_review_packet_id"),
        "source_refreshed_support_check_id": outcome.get("source_refreshed_support_check_id"),
        "source_set": outcome.get("source_set"),
        "corpus": outcome.get("corpus"),
        "query_id": outcome.get("query_id"),
        "query_group": outcome.get("query_group"),
        "query_intent": outcome.get("query_intent"),
        "truth_boundary": "promotion_gate_evaluation_not_promotion",
        "gate_status": "blocked",
        "checked_for": ["promotion", "action_basis"],
        "blockers": blockers,
        "support_like_metadata": counts,
        "human_reviewed_support_count": 0,
        "reviewed_support_count": 0,
        "promotion_support_count": 0,
        "evidence_packet_created": False,
        "evidence_sufficiency": {
            "state": "insufficient",
            "checked_for": "promotion",
            "missing": blockers,
            "required_next_step": "human_review_required",
            "reviewer_note": "Simulation-only outcome cannot satisfy promotion or action-basis gates.",
        },
        "promotion_allowed": False,
        "action_basis_allowed": False,
        "action_readiness": "not_ready",
        "evidence_packet_allowed": False,
        "evidence_sufficiency_passed": False,
        "automatic_promotion_allowed": False,
        "formal_writeback_allowed": False,
        "truth_confidence_change_allowed": False,
        "reviewed_relation_creation_allowed": False,
        "source_outcome_boundary": {
            "truth_boundary": outcome.get("truth_boundary"),
            "human_reviewed": outcome.get("human_reviewed"),
            "counts_as_reviewed_support": outcome.get("counts_as_reviewed_support"),
            "support_passed_count": outcome.get("support_passed_count"),
            "support_counts_for_promotion_count": outcome.get("support_counts_for_promotion_count"),
            "action_basis_allowed": outcome.get("action_basis_allowed"),
            "evidence_packet_allowed": outcome.get("evidence_packet_allowed"),
            "evidence_sufficiency_passed": outcome.get("evidence_sufficiency_passed"),
            "automatic_promotion_allowed": outcome.get("automatic_promotion_allowed"),
            "formal_writeback_allowed": outcome.get("formal_writeback_allowed"),
        },
        "generated_by": "phase_b_promotion_gate_evaluator",
        "built_at": built_at,
    }


def build_all(output_path: Path) -> dict:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    outcomes = list(load_jsonl(OUTCOMES_PATH))
    gates = [build_gate(outcome, built_at) for outcome in outcomes]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for gate in gates:
            handle.write(json.dumps(gate, ensure_ascii=False, sort_keys=True) + "\n")
    summary = {
        "artifact_kind": "vaks_phase_b_promotion_gate_summary",
        "gate_record_count": len(gates),
        "source_outcome_record_count": len(outcomes),
        "blocked_gate_count": sum(1 for gate in gates if gate["gate_status"] == "blocked"),
        "simulated_support_like_count": sum(gate["support_like_metadata"]["simulated_support_like_count"] for gate in gates),
        "simulated_direct_support_count": sum(gate["support_like_metadata"]["simulated_direct_support_count"] for gate in gates),
        "simulated_inferential_support_count": sum(gate["support_like_metadata"]["simulated_inferential_support_count"] for gate in gates),
        "simulated_counterexample_count": sum(gate["support_like_metadata"]["simulated_counterexample_count"] for gate in gates),
        "blocked_due_simulation_only_count": sum(
            1 for gate in gates if "simulation_only_not_reviewed_support" in gate["blockers"]
        ),
        "blocked_due_support_like_not_human_reviewed_count": sum(
            1 for gate in gates if "support_like_metadata_not_human_reviewed" in gate["blockers"]
        ),
        "blocked_due_missing_source_anchor_count": sum(1 for gate in gates if "missing_source_anchor" in gate["blockers"]),
        "human_reviewed_support_count": 0,
        "reviewed_support_count": 0,
        "promotion_support_count": 0,
        "promotion_allowed_count": sum(1 for gate in gates if gate["promotion_allowed"]),
        "action_basis_allowed_count": sum(1 for gate in gates if gate["action_basis_allowed"]),
        "action_ready_count": sum(1 for gate in gates if gate["action_readiness"] == "ready"),
        "evidence_packet_created_count": sum(1 for gate in gates if gate["evidence_packet_created"]),
        "evidence_packet_allowed_count": sum(1 for gate in gates if gate["evidence_packet_allowed"]),
        "evidence_sufficiency_passed_count": sum(1 for gate in gates if gate["evidence_sufficiency_passed"]),
        "automatic_promotion_allowed_count": sum(1 for gate in gates if gate["automatic_promotion_allowed"]),
        "formal_writeback_allowed_count": sum(1 for gate in gates if gate["formal_writeback_allowed"]),
        "truth_confidence_change_allowed_count": sum(1 for gate in gates if gate["truth_confidence_change_allowed"]),
        "reviewed_relation_creation_allowed_count": sum(1 for gate in gates if gate["reviewed_relation_creation_allowed"]),
        "output_path": str(output_path),
        "built_at": built_at,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=GATES_PATH)
    args = parser.parse_args()
    summary = build_all(args.output)
    print(f"promotion gate records: {summary['gate_record_count']}")
    print(f"blocked gates: {summary['blocked_gate_count']}")
    print(f"simulated support-like count: {summary['simulated_support_like_count']}")
    print(f"promotion_allowed_count: {summary['promotion_allowed_count']}")


if __name__ == "__main__":
    main()
