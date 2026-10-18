import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
REFRESHED_SUPPORT_PATH = RESULTS_DIR / "phase_b_refreshed_support_check_candidates.jsonl"
REVIEW_PACKETS_PATH = RESULTS_DIR / "phase_b_review_queue_packets.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_review_queue_packet_summary.json"

REVIEW_STEPS = [
    "inspect_source_span",
    "decide_span_supports_target",
    "assign_evidence_role",
    "write_reviewer_note_if_inferential",
    "keep_background_context_out_of_support",
    "run_evidence_sufficiency_only_after_support_review",
]


def load_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def packet_priority(check: dict) -> str:
    if check.get("support_check_status") == "blocked_no_source_anchor":
        return "blocked"
    if check.get("query_intent") in {"action", "evidence"}:
        return "high"
    return "normal"


def queue_item_type(check: dict) -> str:
    if check.get("support_check_status") == "blocked_no_source_anchor":
        return "missing_evidence"
    return "missing_evidence"


def suggested_action(check: dict) -> str:
    if check.get("support_check_status") == "blocked_no_source_anchor":
        return "mark_review_due"
    return "request_evidence"


def packet_status(check: dict) -> str:
    if check.get("support_check_status") == "blocked_no_source_anchor":
        return "blocked_no_source_anchor"
    return "open"


def build_review_item(item: dict) -> dict:
    anchor = item.get("source_anchor") or {}
    support = item.get("evidence_support") or {}
    return {
        "evidence_item_id": item.get("evidence_item_id"),
        "review_item_status": "needs_manual_evidence_support_review",
        "source_anchor_ref": {
            "vault_path": anchor.get("vault_path"),
            "heading_or_anchor": anchor.get("heading_or_anchor"),
            "source_clickback": anchor.get("source_clickback"),
            "source_range": anchor.get("source_range"),
            "source_hash": anchor.get("source_hash"),
            "current_source_hash": anchor.get("current_source_hash"),
            "current_source_hash_matches_receipt": anchor.get("current_source_hash_matches_receipt"),
            "chunk_hash": anchor.get("chunk_hash"),
            "source_span_available": anchor.get("source_span_available"),
        },
        "quote_or_excerpt": anchor.get("quote_or_excerpt"),
        "pre_review_evidence_support": {
            "span_supports_target": support.get("span_supports_target"),
            "evidence_role": support.get("evidence_role"),
            "reviewer_note": support.get("reviewer_note"),
        },
        "review_allowed_outcomes": [
            "supported_direct",
            "partial_inferential_with_note",
            "background_context_only",
            "counterexample",
            "unsupported",
            "unclear",
        ],
        "support_counts_for_promotion": False,
        "warning_codes": item.get("warning_codes") or [],
        "authority_bucket": item.get("authority_bucket"),
        "usage_badge": item.get("usage_badge"),
        "retrieval_reasons": item.get("retrieval_reasons") or [],
    }


def build_packet(check: dict, built_at: str) -> dict:
    items = check.get("evidence_items") or []
    review_items = [build_review_item(item) for item in items]
    status = packet_status(check)
    return {
        "artifact_kind": "vaks_phase_b_review_queue_packet",
        "review_packet_id": check.get("refreshed_support_check_id"),
        "source_refreshed_support_check_id": check.get("refreshed_support_check_id"),
        "source_refresh_id": check.get("source_refresh_id"),
        "source_support_check_id": check.get("source_support_check_id"),
        "source_envelope_id": check.get("source_envelope_id"),
        "source_pack_id": check.get("source_pack_id"),
        "source_set": check.get("source_set"),
        "corpus": check.get("corpus"),
        "query_id": check.get("query_id"),
        "query_group": check.get("query_group"),
        "query_intent": check.get("query_intent"),
        "record_type": "review-queue-item",
        "review_queue_state": status,
        "item_type": queue_item_type(check),
        "review_route": "evidence_check",
        "triggered_by": [
            "retrieval_receipt",
            "context_pack_candidate",
            "evidence_envelope_candidate",
            "refreshed_support_check_candidate",
        ],
        "reason": (
            "manual evidence_support review required for refreshed source spans"
            if status == "open"
            else "no source anchor available; reviewer must request evidence or keep blocked"
        ),
        "suggested_action": suggested_action(check),
        "status": "open" if status == "open" else "parked",
        "priority": packet_priority(check),
        "promotion_target": "none",
        "review_object_state": "draft",
        "truth_boundary": "review_queue_packet_not_reviewed_support",
        "review_result": "not_reviewed",
        "reviewed_by": "",
        "reviewed_at": "",
        "approval_integrity": {
            "approved_by": "",
            "approval_source": "",
            "approved_at": "",
            "llm_assisted": True,
            "checked_specific_evidence": False,
            "checked_body_hash": "",
        },
        "action_basis_allowed": False,
        "evidence_packet_allowed": False,
        "evidence_sufficiency_passed": False,
        "automatic_promotion_allowed": False,
        "support_passed_count": 0,
        "support_counts_for_promotion_count": 0,
        "review_items": review_items,
        "review_steps": REVIEW_STEPS,
        "source_freshness": {
            "source_refresh_needed_count": check.get("source_refresh_needed_count"),
            "source_span_available_count": sum(
                1 for item in review_items if item["source_anchor_ref"].get("source_span_available")
            ),
            "current_source_hash_match_count": sum(
                1 for item in review_items if item["source_anchor_ref"].get("current_source_hash_matches_receipt")
            ),
        },
        "source_refreshed_support_boundary": {
            "support_check_status": check.get("support_check_status"),
            "truth_boundary": check.get("truth_boundary"),
            "action_basis_allowed": check.get("action_basis_allowed"),
            "evidence_packet_allowed": check.get("evidence_packet_allowed"),
            "evidence_sufficiency_passed": check.get("evidence_sufficiency_passed"),
        },
        "generated_by": "phase_b_review_queue_packet_builder",
        "built_at": built_at,
    }


def build_all(output_path: Path) -> dict:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    checks = list(load_jsonl(REFRESHED_SUPPORT_PATH))
    packets = [build_packet(check, built_at) for check in checks]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for packet in packets:
            handle.write(json.dumps(packet, ensure_ascii=False, sort_keys=True) + "\n")
    review_items = [item for packet in packets for item in packet["review_items"]]
    summary = {
        "artifact_kind": "vaks_phase_b_review_queue_packet_summary",
        "review_packet_count": len(packets),
        "source_refreshed_support_check_count": len(checks),
        "open_packet_count": sum(1 for packet in packets if packet["review_queue_state"] == "open"),
        "blocked_no_source_anchor_count": sum(
            1 for packet in packets if packet["review_queue_state"] == "blocked_no_source_anchor"
        ),
        "review_item_count": len(review_items),
        "source_span_available_count": sum(
            1 for item in review_items if item["source_anchor_ref"]["source_span_available"]
        ),
        "current_source_hash_match_count": sum(
            1 for item in review_items if item["source_anchor_ref"]["current_source_hash_matches_receipt"]
        ),
        "source_refresh_needed_count": sum(packet["source_freshness"]["source_refresh_needed_count"] for packet in packets),
        "review_result_not_reviewed_count": sum(1 for packet in packets if packet["review_result"] == "not_reviewed"),
        "support_passed_count": 0,
        "support_counts_for_promotion_count": 0,
        "action_basis_allowed_count": sum(1 for packet in packets if packet["action_basis_allowed"]),
        "evidence_packet_allowed_count": sum(1 for packet in packets if packet["evidence_packet_allowed"]),
        "evidence_sufficiency_passed_count": sum(1 for packet in packets if packet["evidence_sufficiency_passed"]),
        "automatic_promotion_allowed_count": sum(1 for packet in packets if packet["automatic_promotion_allowed"]),
        "output_path": str(output_path),
        "built_at": built_at,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=REVIEW_PACKETS_PATH)
    args = parser.parse_args()
    summary = build_all(args.output)
    print(f"review packets: {summary['review_packet_count']}")
    print(f"open packets: {summary['open_packet_count']}")
    print(f"blocked packets: {summary['blocked_no_source_anchor_count']}")
    print(f"review items: {summary['review_item_count']}")


if __name__ == "__main__":
    main()
