import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
PACKS_PATH = RESULTS_DIR / "phase_b_context_pack_candidates.jsonl"
ENVELOPES_PATH = RESULTS_DIR / "phase_b_evidence_envelope_candidates.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_evidence_envelope_candidate_summary.json"

REQUIRED_NEXT_GATES = [
    "evidence_support_check",
    "evidence_sufficiency_gate",
    "human_or_explicit_review",
    "action_gate_if_action_use",
]

BASE_NOT_ENOUGH = [
    "evidence_support_check_not_run",
    "evidence_sufficiency_gate_not_run",
    "human_review_not_done",
    "not_action_basis",
]


def load_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def candidate_anchor(item: dict, role: str) -> dict:
    reasons = set(item.get("retrieval_reasons") or [])
    warning_reasons = []
    if item.get("warning_code"):
        warning_reasons.extend(str(item["warning_code"]).split(";"))
    if item.get("temporal_badge") == "stale":
        warning_reasons.append("stale_index")
    if "graph_neighbor" in reasons:
        warning_reasons.append("graph_metadata_not_reviewed_relation")
    if item.get("receipt_action_basis_allowed"):
        warning_reasons.append("receipt_action_flag_suppressed_at_envelope_level")
    return {
        "vault_path": item.get("vault_path"),
        "heading_or_anchor": item.get("heading_or_anchor"),
        "selector_or_line_range": item.get("selector_or_line_range"),
        "source_clickback": item.get("source_clickback"),
        "source_hash": item.get("source_hash"),
        "indexed_source_hash": item.get("indexed_source_hash"),
        "chunk_hash": item.get("chunk_hash"),
        "authority_bucket": item.get("authority_bucket"),
        "authority_badge": item.get("authority_badge"),
        "usage_badge": item.get("usage_badge"),
        "review_state": item.get("review_state"),
        "relation_state": item.get("relation_state"),
        "temporal_badge": item.get("temporal_badge"),
        "retrieval_reasons": item.get("retrieval_reasons") or [],
        "candidate_support_role": role,
        "support_status": "candidate_source_anchor_not_evidence_support",
        "warning_codes": list(dict.fromkeys(warning_reasons)),
    }


def challenge_kind(item: dict) -> str:
    if item.get("authority_bucket") not in {"core_framework", "reviewed"}:
        return "non_support_authority_bucket"
    if item.get("temporal_badge") == "stale":
        return "temporal_or_index_staleness"
    if "graph_neighbor" in set(item.get("retrieval_reasons") or []):
        return "graph_metadata_needs_relation_review"
    if item.get("warning_code"):
        return "receipt_warning_needs_review"
    if item.get("receipt_action_basis_allowed"):
        return "action_flag_suppressed"
    return "scope_or_warrant_gap"


def build_challenge_candidates(pack: dict) -> list[dict]:
    sections = pack.get("context_sections") or {}
    items = list(sections.get("primary") or []) + list(sections.get("neighbors") or [])
    challenges = []
    for item in items:
        reasons = set(item.get("retrieval_reasons") or [])
        has_challenge = (
            item.get("authority_bucket") not in {"core_framework", "reviewed"}
            or bool(item.get("warning_code"))
            or item.get("temporal_badge") == "stale"
            or "graph_neighbor" in reasons
            or bool(item.get("receipt_action_basis_allowed"))
        )
        if has_challenge:
            challenge = candidate_anchor(item, "known_challenge_or_scope_input")
            challenge["challenge_kind"] = challenge_kind(item)
            challenges.append(challenge)
    return challenges[:5]


def build_warrant_text(pack: dict) -> str:
    query_id = pack.get("query_id")
    primary_count = (pack.get("coverage_summary") or {}).get("primary_count", 0)
    stale_count = (pack.get("coverage_summary") or {}).get("stale_count", 0)
    return (
        f"Draft review orientation for {query_id}: {primary_count} primary "
        f"core/reviewed anchors can orient a reviewer, but this remains retrieval "
        f"receipt material only. It still needs source-span support review, a "
        f"non-circular warrant, scope/risk review, challenge review, and the "
        f"Evidence Sufficiency Gate before any action-facing use. "
        f"Stale or refresh-needed anchors observed: {stale_count}."
    )


def not_enough_because(pack: dict) -> list[str]:
    sections = pack.get("context_sections") or {}
    reasons = list(BASE_NOT_ENOUGH)
    reasons.extend(sections.get("gaps") or [])
    reasons.extend(sections.get("stop_conditions") or [])
    return list(dict.fromkeys(reasons))


def build_envelope(pack: dict, built_at: str) -> dict:
    sections = pack.get("context_sections") or {}
    summary = pack.get("coverage_summary") or {}
    support_candidates = [
        candidate_anchor(item, "possible_review_input")
        for item in sections.get("primary") or []
    ]
    warnings = list(
        dict.fromkeys(
            list(sections.get("warnings") or [])
            + [
                "evidence_envelope_candidate_not_evidence_packet",
                "warrant_draft_not_reviewed_support",
            ]
        )
    )
    return {
        "artifact_kind": "vaks_phase_b_evidence_envelope_candidate",
        "envelope_id": pack.get("pack_id"),
        "source_pack_id": pack.get("pack_id"),
        "source_set": pack.get("source_set"),
        "corpus": pack.get("corpus"),
        "query_id": pack.get("query_id"),
        "query_group": pack.get("query_group"),
        "query_intent": pack.get("query_intent"),
        "draft_status": "warrant_draft_not_evidence_packet",
        "truth_boundary": "candidate_review_input_not_support",
        "action_basis_allowed": False,
        "evidence_packet_allowed": False,
        "evidence_sufficiency_passed": False,
        "envelope_policy": {
            "policy_kind": "phase_b_evidence_envelope_candidate",
            "review_input_allowed": True,
            "action_basis_allowed": False,
            "evidence_packet_allowed": False,
            "review_required_before_action": True,
        },
        "warrant": {
            "draft_text": build_warrant_text(pack),
            "warrant_status": "draft_needs_review",
            "basis": "retrieval_receipts_only",
            "non_circularity_checked": False,
            "not_enough_because": not_enough_because(pack),
        },
        "support_candidates": support_candidates,
        "challenge_candidates": build_challenge_candidates(pack),
        "risk_and_scope": {
            "warnings": warnings,
            "gaps": sections.get("gaps") or [],
            "stop_conditions": sections.get("stop_conditions") or [],
            "temporal_or_refresh_needed": bool(summary.get("stale_count")),
        },
        "required_next_gates": REQUIRED_NEXT_GATES,
        "suppressed_flags": {
            "source_pack_action_basis_allowed": bool(
                (pack.get("pack_policy") or {}).get("action_basis_allowed")
            ),
            "suppressed_receipt_action_flags": int(summary.get("suppressed_receipt_action_flags") or 0),
        },
        "source_pack_coverage_summary": summary,
        "generated_by": "phase_b_evidence_envelope_candidate_builder",
        "built_at": built_at,
    }


def build_all(output_path: Path) -> dict:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    packs = list(load_jsonl(PACKS_PATH))
    envelopes = [build_envelope(pack, built_at) for pack in packs]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for envelope in envelopes:
            handle.write(json.dumps(envelope, ensure_ascii=False, sort_keys=True) + "\n")
    summary = {
        "artifact_kind": "vaks_phase_b_evidence_envelope_summary",
        "envelope_count": len(envelopes),
        "source_pack_count": len(packs),
        "action_basis_allowed_count": sum(1 for item in envelopes if item["action_basis_allowed"]),
        "evidence_packet_allowed_count": sum(1 for item in envelopes if item["evidence_packet_allowed"]),
        "evidence_sufficiency_passed_count": sum(1 for item in envelopes if item["evidence_sufficiency_passed"]),
        "envelopes_with_suppressed_receipt_action_flags": sum(
            1 for item in envelopes if item["suppressed_flags"]["suppressed_receipt_action_flags"]
        ),
        "output_path": str(output_path),
        "built_at": built_at,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ENVELOPES_PATH)
    args = parser.parse_args()
    summary = build_all(args.output)
    print(f"evidence envelope candidates: {summary['envelope_count']}")
    print(f"action_basis_allowed_count: {summary['action_basis_allowed_count']}")
    print(f"evidence_packet_allowed_count: {summary['evidence_packet_allowed_count']}")
    print(f"evidence_sufficiency_passed_count: {summary['evidence_sufficiency_passed_count']}")


if __name__ == "__main__":
    main()
