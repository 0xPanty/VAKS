import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
REVIEW_PACKETS_PATH = RESULTS_DIR / "phase_b_review_queue_packets.jsonl"
OUTCOMES_PATH = RESULTS_DIR / "phase_b_simulated_reviewer_outcomes.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_simulated_reviewer_outcome_summary.json"

SIMULATED_PACKET_LIMIT = 12


def load_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def outcome_for_item(index: int) -> dict:
    pattern = (index - 1) % 5
    if pattern == 0:
        return {
            "span_supports_target": "supported",
            "evidence_role": "direct_support",
            "reviewer_note": "Simulated only: span appears directly relevant to the target review question.",
        }
    if pattern == 1:
        return {
            "span_supports_target": "partial",
            "evidence_role": "inferential_support",
            "reviewer_note": "Simulated only: span may support the target only with explicit reasoning.",
        }
    if pattern == 2:
        return {
            "span_supports_target": "unclear",
            "evidence_role": "background_context",
            "reviewer_note": "Simulated only: useful context, not support.",
        }
    if pattern == 3:
        return {
            "span_supports_target": "unsupported",
            "evidence_role": "background_context",
            "reviewer_note": "Simulated only: span does not bear directly enough on the target.",
        }
    return {
        "span_supports_target": "partial",
        "evidence_role": "counterexample",
        "reviewer_note": "Simulated only: span may challenge or narrow the target.",
    }


def build_item_outcome(item: dict, index: int) -> dict:
    simulated_support = outcome_for_item(index)
    return {
        "evidence_item_id": item.get("evidence_item_id"),
        "source_anchor_ref": item.get("source_anchor_ref"),
        "simulated_evidence_support": simulated_support,
        "simulation_kind": "deterministic_sandbox_review",
        "human_reviewed": False,
        "counts_as_reviewed_support": False,
        "support_counts_for_promotion": False,
        "allowed_next_step": "human_review_required",
        "warning_codes": item.get("warning_codes") or [],
    }


def selected_packet_ids(packets: list[dict]) -> set[str]:
    open_packets = [packet for packet in packets if packet.get("review_queue_state") == "open"]
    open_packets = sorted(open_packets, key=lambda row: row.get("review_packet_id") or "")
    return {packet.get("review_packet_id") for packet in open_packets[:SIMULATED_PACKET_LIMIT]}


def build_outcome(packet: dict, built_at: str, selected_ids: set[str]) -> dict:
    packet_id = packet.get("review_packet_id")
    selected = packet_id in selected_ids
    blocked = packet.get("review_queue_state") == "blocked_no_source_anchor"
    item_outcomes = [
        build_item_outcome(item, index)
        for index, item in enumerate(packet.get("review_items") or [], start=1)
    ] if selected else []
    if blocked:
        review_result = "blocked_no_source_anchor"
        queue_state = "parked"
    elif selected:
        review_result = "simulation_recorded_not_human_review"
        queue_state = "in-review"
    else:
        review_result = "not_reviewed"
        queue_state = "open"
    return {
        "artifact_kind": "vaks_phase_b_simulated_reviewer_outcome",
        "outcome_id": packet_id,
        "source_review_packet_id": packet_id,
        "source_refreshed_support_check_id": packet.get("source_refreshed_support_check_id"),
        "source_set": packet.get("source_set"),
        "corpus": packet.get("corpus"),
        "query_id": packet.get("query_id"),
        "query_group": packet.get("query_group"),
        "query_intent": packet.get("query_intent"),
        "truth_boundary": "simulated_reviewer_outcome_not_reviewed_support",
        "simulated_review_applied": selected,
        "simulation_scope": "sample_only",
        "review_result": review_result,
        "review_queue_state_after_simulation": queue_state,
        "human_reviewed": False,
        "approval_integrity": {
            "approved_by": "",
            "approval_source": "simulation_only",
            "approved_at": "",
            "llm_assisted": True,
            "checked_specific_evidence": False,
            "checked_body_hash": "",
        },
        "action_basis_allowed": False,
        "evidence_packet_allowed": False,
        "evidence_sufficiency_passed": False,
        "automatic_promotion_allowed": False,
        "formal_writeback_allowed": False,
        "counts_as_reviewed_support": False,
        "support_passed_count": 0,
        "support_counts_for_promotion_count": 0,
        "human_reviewed_support_count": 0,
        "simulated_item_outcomes": item_outcomes,
        "source_refresh_needed_count": (packet.get("source_freshness") or {}).get("source_refresh_needed_count"),
        "source_review_packet_boundary": {
            "truth_boundary": packet.get("truth_boundary"),
            "review_result": packet.get("review_result"),
            "action_basis_allowed": packet.get("action_basis_allowed"),
            "evidence_packet_allowed": packet.get("evidence_packet_allowed"),
            "evidence_sufficiency_passed": packet.get("evidence_sufficiency_passed"),
            "automatic_promotion_allowed": packet.get("automatic_promotion_allowed"),
        },
        "generated_by": "phase_b_simulated_reviewer_outcome_builder",
        "built_at": built_at,
    }


def build_all(output_path: Path) -> dict:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    packets = list(load_jsonl(REVIEW_PACKETS_PATH))
    selected_ids = selected_packet_ids(packets)
    outcomes = [build_outcome(packet, built_at, selected_ids) for packet in packets]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for outcome in outcomes:
            handle.write(json.dumps(outcome, ensure_ascii=False, sort_keys=True) + "\n")
    item_outcomes = [item for outcome in outcomes for item in outcome["simulated_item_outcomes"]]
    summary = {
        "artifact_kind": "vaks_phase_b_simulated_reviewer_outcome_summary",
        "outcome_record_count": len(outcomes),
        "source_review_packet_count": len(packets),
        "simulated_packet_count": sum(1 for item in outcomes if item["simulated_review_applied"]),
        "not_reviewed_packet_count": sum(1 for item in outcomes if item["review_result"] == "not_reviewed"),
        "blocked_no_source_anchor_count": sum(1 for item in outcomes if item["review_result"] == "blocked_no_source_anchor"),
        "simulated_item_outcome_count": len(item_outcomes),
        "simulated_direct_support_count": sum(
            1
            for item in item_outcomes
            if item["simulated_evidence_support"]["span_supports_target"] == "supported"
            and item["simulated_evidence_support"]["evidence_role"] == "direct_support"
        ),
        "simulated_inferential_support_count": sum(
            1 for item in item_outcomes if item["simulated_evidence_support"]["evidence_role"] == "inferential_support"
        ),
        "simulated_background_count": sum(
            1 for item in item_outcomes if item["simulated_evidence_support"]["evidence_role"] == "background_context"
        ),
        "simulated_counterexample_count": sum(
            1 for item in item_outcomes if item["simulated_evidence_support"]["evidence_role"] == "counterexample"
        ),
        "source_refresh_needed_count": sum(int(item.get("source_refresh_needed_count") or 0) for item in outcomes),
        "human_reviewed_support_count": 0,
        "support_passed_count": 0,
        "support_counts_for_promotion_count": 0,
        "action_basis_allowed_count": sum(1 for item in outcomes if item["action_basis_allowed"]),
        "evidence_packet_allowed_count": sum(1 for item in outcomes if item["evidence_packet_allowed"]),
        "evidence_sufficiency_passed_count": sum(1 for item in outcomes if item["evidence_sufficiency_passed"]),
        "automatic_promotion_allowed_count": sum(1 for item in outcomes if item["automatic_promotion_allowed"]),
        "formal_writeback_allowed_count": sum(1 for item in outcomes if item["formal_writeback_allowed"]),
        "output_path": str(output_path),
        "built_at": built_at,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTCOMES_PATH)
    args = parser.parse_args()
    summary = build_all(args.output)
    print(f"outcome records: {summary['outcome_record_count']}")
    print(f"simulated packets: {summary['simulated_packet_count']}")
    print(f"simulated item outcomes: {summary['simulated_item_outcome_count']}")
    print(f"support_passed_count: {summary['support_passed_count']}")


if __name__ == "__main__":
    main()
