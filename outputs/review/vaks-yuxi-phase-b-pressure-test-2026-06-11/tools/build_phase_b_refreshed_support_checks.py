import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
SOURCE_REFRESH_PATH = RESULTS_DIR / "phase_b_source_refresh_candidates.jsonl"
REFRESHED_SUPPORT_PATH = RESULTS_DIR / "phase_b_refreshed_support_check_candidates.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_refreshed_support_check_candidate_summary.json"

REQUIRED_NEXT_GATES = [
    "human_evidence_support_review",
    "non_circular_warrant_review",
    "evidence_sufficiency_gate",
    "action_gate_if_action_use",
]


def load_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def support_notes(items: list[dict], record: dict) -> list[str]:
    notes = [
        "refreshed_source_span_snapshot_applied",
        "semantic_support_not_reviewed",
        "support_status_remains_unclear",
    ]
    if not items:
        notes.append("no_source_anchor_available")
    if any(item.get("refresh_status") == "refreshed_current_source_hash" for item in items):
        notes.append("source_hash_refresh_applied")
    if record.get("source_refresh_status") == "blocked_no_source_anchor":
        notes.append("blocked_no_source_anchor")
    return list(dict.fromkeys(notes))


def build_evidence_item(item: dict) -> dict:
    anchor = item.get("source_anchor") or {}
    warnings = [
        warning
        for warning in item.get("warning_codes") or []
        if warning != "source_hash_mismatch_requires_refresh"
    ]
    return {
        "evidence_item_id": item.get("evidence_item_id"),
        "refresh_status": item.get("refresh_status"),
        "source_anchor": {
            "vault_path": anchor.get("vault_path"),
            "heading_or_anchor": anchor.get("heading_or_anchor"),
            "source_clickback": anchor.get("source_clickback"),
            "source_range": anchor.get("source_range"),
            "quote_or_excerpt": anchor.get("quote_or_excerpt"),
            "source_hash": anchor.get("source_hash"),
            "current_source_hash": anchor.get("current_source_hash"),
            "current_source_hash_matches_receipt": anchor.get("current_source_hash_matches_receipt"),
            "chunk_hash": anchor.get("chunk_hash"),
            "source_span_available": anchor.get("source_span_available"),
            "source_span_error": anchor.get("source_span_error"),
        },
        "evidence_support": {
            "span_supports_target": "unclear",
            "evidence_role": "background_context",
            "reviewer_note": "Rebuilt after source refresh. Semantic support still not reviewed.",
        },
        "support_check_status": "candidate_support_check_not_reviewed",
        "support_counts_for_promotion": False,
        "warning_codes": warnings,
        "authority_bucket": item.get("authority_bucket"),
        "usage_badge": item.get("usage_badge"),
        "retrieval_reasons": item.get("retrieval_reasons") or [],
    }


def build_refreshed_check(record: dict, built_at: str) -> dict:
    refresh_items = record.get("refresh_items") or []
    evidence_items = [build_evidence_item(item) for item in refresh_items]
    blocked = record.get("source_refresh_status") == "blocked_no_source_anchor"
    return {
        "artifact_kind": "vaks_phase_b_refreshed_support_check_candidate",
        "refreshed_support_check_id": record.get("source_refresh_id"),
        "source_refresh_id": record.get("source_refresh_id"),
        "source_support_check_id": record.get("source_support_check_id"),
        "source_envelope_id": record.get("source_envelope_id"),
        "source_pack_id": record.get("source_pack_id"),
        "source_set": record.get("source_set"),
        "corpus": record.get("corpus"),
        "query_id": record.get("query_id"),
        "query_group": record.get("query_group"),
        "query_intent": record.get("query_intent"),
        "support_check_status": "blocked_no_source_anchor" if blocked else "candidate_support_check_not_reviewed",
        "truth_boundary": "refreshed_source_span_check_candidate_not_support",
        "action_basis_allowed": False,
        "evidence_packet_allowed": False,
        "evidence_sufficiency_passed": False,
        "support_passed_count": 0,
        "support_counts_for_promotion_count": 0,
        "source_refresh_needed_count": sum(
            1
            for item in evidence_items
            if not (item.get("source_anchor") or {}).get("current_source_hash_matches_receipt")
        ),
        "evidence_items": evidence_items,
        "rebuild_policy": {
            "policy_kind": "phase_b_refreshed_support_check_candidate",
            "source": "phase_b_source_refresh_candidate",
            "source_hash_and_span_refreshed": True,
            "rerank_or_retrieve_changed": False,
            "semantic_support_reviewed": False,
            "action_basis_allowed": False,
            "evidence_packet_allowed": False,
        },
        "support_check_notes": support_notes(evidence_items, record),
        "required_next_gates": REQUIRED_NEXT_GATES,
        "source_refresh_boundary": {
            "source_refresh_status": record.get("source_refresh_status"),
            "truth_boundary": record.get("truth_boundary"),
            "action_basis_allowed": record.get("action_basis_allowed"),
            "evidence_packet_allowed": record.get("evidence_packet_allowed"),
            "evidence_sufficiency_passed": record.get("evidence_sufficiency_passed"),
        },
        "generated_by": "phase_b_refreshed_support_check_candidate_builder",
        "built_at": built_at,
    }


def build_all(output_path: Path) -> dict:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    source_refresh_records = list(load_jsonl(SOURCE_REFRESH_PATH))
    checks = [build_refreshed_check(record, built_at) for record in source_refresh_records]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for check in checks:
            handle.write(json.dumps(check, ensure_ascii=False, sort_keys=True) + "\n")
    items = [item for check in checks for item in check["evidence_items"]]
    summary = {
        "artifact_kind": "vaks_phase_b_refreshed_support_check_summary",
        "refreshed_support_check_count": len(checks),
        "source_refresh_count": len(source_refresh_records),
        "evidence_item_count": len(items),
        "source_span_available_count": sum(
            1 for item in items if item["source_anchor"]["source_span_available"]
        ),
        "current_source_hash_match_count": sum(
            1 for item in items if item["source_anchor"]["current_source_hash_matches_receipt"]
        ),
        "source_refresh_needed_count": sum(
            1 for item in items if not item["source_anchor"]["current_source_hash_matches_receipt"]
        ),
        "refreshed_item_count": sum(1 for item in items if item.get("refresh_status") == "refreshed_current_source_hash"),
        "already_current_item_count": sum(1 for item in items if item.get("refresh_status") == "already_current"),
        "blocked_no_source_anchor_count": sum(
            1 for check in checks if check["support_check_status"] == "blocked_no_source_anchor"
        ),
        "support_passed_count": 0,
        "support_counts_for_promotion_count": 0,
        "action_basis_allowed_count": sum(1 for check in checks if check["action_basis_allowed"]),
        "evidence_packet_allowed_count": sum(1 for check in checks if check["evidence_packet_allowed"]),
        "evidence_sufficiency_passed_count": sum(1 for check in checks if check["evidence_sufficiency_passed"]),
        "output_path": str(output_path),
        "built_at": built_at,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=REFRESHED_SUPPORT_PATH)
    args = parser.parse_args()
    summary = build_all(args.output)
    print(f"refreshed support checks: {summary['refreshed_support_check_count']}")
    print(f"evidence item count: {summary['evidence_item_count']}")
    print(f"source_refresh_needed_count: {summary['source_refresh_needed_count']}")
    print(f"support_passed_count: {summary['support_passed_count']}")


if __name__ == "__main__":
    main()
