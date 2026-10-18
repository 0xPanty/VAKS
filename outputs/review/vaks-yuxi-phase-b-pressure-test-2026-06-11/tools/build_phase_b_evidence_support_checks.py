import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
ENVELOPES_PATH = RESULTS_DIR / "phase_b_evidence_envelope_candidates.jsonl"
SUPPORT_CHECKS_PATH = RESULTS_DIR / "phase_b_evidence_support_check_candidates.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_evidence_support_check_candidate_summary.json"

SELECTOR_RE = re.compile(r"^L(?P<start>\d+)-L(?P<end>\d+)$")

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


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_selector(selector: str | None) -> tuple[int | None, int | None]:
    match = SELECTOR_RE.match(selector or "")
    if not match:
        return None, None
    return int(match.group("start")), int(match.group("end"))


def source_span(candidate: dict) -> dict:
    vault_path = candidate.get("vault_path") or ""
    selector = candidate.get("selector_or_line_range")
    target = ROOT / vault_path
    start, end = parse_selector(selector)
    if not vault_path or start is None or end is None:
        return {
            "source_span_available": False,
            "source_span_error": "missing_or_unparseable_line_range",
            "current_source_hash": "",
            "current_source_hash_matches_receipt": False,
            "source_range": selector or "",
            "quote_or_excerpt": "",
        }
    if not target.exists() or not target.is_file():
        return {
            "source_span_available": False,
            "source_span_error": "source_file_missing",
            "current_source_hash": "",
            "current_source_hash_matches_receipt": False,
            "source_range": selector,
            "quote_or_excerpt": "",
        }
    text = read_text(target)
    lines = text.splitlines()
    safe_start = max(1, min(start, len(lines) or 1))
    safe_end = max(safe_start, min(end, len(lines) or safe_start))
    excerpt = "\n".join(lines[safe_start - 1 : safe_end]).strip()
    current_hash = sha256_text(text)
    receipt_hash = candidate.get("source_hash") or ""
    return {
        "source_span_available": bool(excerpt),
        "source_span_error": "" if excerpt else "empty_source_span",
        "current_source_hash": current_hash,
        "current_source_hash_matches_receipt": bool(receipt_hash and current_hash == receipt_hash),
        "source_range": f"L{safe_start}-L{safe_end}",
        "quote_or_excerpt": excerpt[:1200],
    }


def warning_codes(candidate: dict, span: dict) -> list[str]:
    warnings = list(candidate.get("warning_codes") or [])
    if not span.get("source_span_available"):
        warnings.append("missing_source_span")
    if not span.get("current_source_hash_matches_receipt"):
        warnings.append("source_hash_mismatch_requires_refresh")
    if candidate.get("temporal_badge") == "stale":
        warnings.append("stale_index")
    if "graph_neighbor" in set(candidate.get("retrieval_reasons") or []):
        warnings.append("graph_metadata_not_reviewed_relation")
    return list(dict.fromkeys(warnings))


def build_evidence_item(envelope: dict, candidate: dict, index: int) -> dict:
    span = source_span(candidate)
    warnings = warning_codes(candidate, span)
    return {
        "evidence_item_id": f"{envelope.get('envelope_id')}:support:{index:02d}",
        "target": {
            "target_kind": "query_review_target",
            "target_id": envelope.get("query_id"),
            "target_group": envelope.get("query_group"),
            "target_intent": envelope.get("query_intent"),
            "target_status": "not_fixed_review_candidate",
        },
        "source_anchor": {
            "vault_path": candidate.get("vault_path"),
            "heading_or_anchor": candidate.get("heading_or_anchor"),
            "source_clickback": candidate.get("source_clickback"),
            "source_range": span["source_range"],
            "quote_or_excerpt": span["quote_or_excerpt"],
            "source_hash": candidate.get("source_hash"),
            "current_source_hash": span["current_source_hash"],
            "current_source_hash_matches_receipt": span["current_source_hash_matches_receipt"],
            "chunk_hash": candidate.get("chunk_hash"),
            "source_span_available": span["source_span_available"],
            "source_span_error": span["source_span_error"],
        },
        "evidence_support": {
            "span_supports_target": "unclear",
            "evidence_role": "background_context",
            "reviewer_note": "Not reviewed. Generated from retrieval-derived source anchor for support-check preparation only.",
        },
        "support_check_status": "candidate_support_check_not_reviewed",
        "support_counts_for_promotion": False,
        "warning_codes": warnings,
        "authority_bucket": candidate.get("authority_bucket"),
        "usage_badge": candidate.get("usage_badge"),
        "retrieval_reasons": candidate.get("retrieval_reasons") or [],
    }


def support_check_notes(items: list[dict]) -> list[str]:
    notes = [
        "source_span_snapshot_created",
        "semantic_support_not_reviewed",
        "support_status_remains_unclear",
    ]
    if not items:
        notes.append("no_source_anchor_available")
    if any(not item["source_anchor"]["source_span_available"] for item in items):
        notes.append("missing_source_span_present")
    if any(not item["source_anchor"]["current_source_hash_matches_receipt"] for item in items):
        notes.append("source_refresh_needed_before_support_review")
    if any("graph_metadata_not_reviewed_relation" in item["warning_codes"] for item in items):
        notes.append("graph_metadata_requires_relation_review")
    return list(dict.fromkeys(notes))


def build_support_check(envelope: dict, built_at: str) -> dict:
    candidates = envelope.get("support_candidates") or []
    items = [build_evidence_item(envelope, candidate, index) for index, candidate in enumerate(candidates, start=1)]
    support_check_status = "candidate_support_check_not_reviewed" if items else "blocked_no_source_anchor"
    return {
        "artifact_kind": "vaks_phase_b_evidence_support_check_candidate",
        "support_check_id": envelope.get("envelope_id"),
        "source_envelope_id": envelope.get("envelope_id"),
        "source_pack_id": envelope.get("source_pack_id"),
        "source_set": envelope.get("source_set"),
        "corpus": envelope.get("corpus"),
        "query_id": envelope.get("query_id"),
        "query_group": envelope.get("query_group"),
        "query_intent": envelope.get("query_intent"),
        "support_check_status": support_check_status,
        "truth_boundary": "source_span_check_candidate_not_support",
        "action_basis_allowed": False,
        "evidence_packet_allowed": False,
        "evidence_sufficiency_passed": False,
        "support_passed_count": 0,
        "support_counts_for_promotion_count": 0,
        "source_envelope_support_candidate_count": len(candidates),
        "evidence_items": items,
        "support_check_policy": {
            "policy_kind": "phase_b_evidence_support_check_candidate",
            "source_span_snapshot_allowed": True,
            "semantic_support_reviewed": False,
            "action_basis_allowed": False,
            "evidence_packet_allowed": False,
            "review_required_before_support": True,
        },
        "support_check_notes": support_check_notes(items),
        "required_next_gates": REQUIRED_NEXT_GATES,
        "source_envelope_boundary": {
            "draft_status": envelope.get("draft_status"),
            "truth_boundary": envelope.get("truth_boundary"),
            "action_basis_allowed": envelope.get("action_basis_allowed"),
            "evidence_packet_allowed": envelope.get("evidence_packet_allowed"),
            "evidence_sufficiency_passed": envelope.get("evidence_sufficiency_passed"),
        },
        "generated_by": "phase_b_evidence_support_check_candidate_builder",
        "built_at": built_at,
    }


def build_all(output_path: Path) -> dict:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    envelopes = list(load_jsonl(ENVELOPES_PATH))
    checks = [build_support_check(envelope, built_at) for envelope in envelopes]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for check in checks:
            handle.write(json.dumps(check, ensure_ascii=False, sort_keys=True) + "\n")
    item_count = sum(len(check["evidence_items"]) for check in checks)
    span_count = sum(
        1
        for check in checks
        for item in check["evidence_items"]
        if item["source_anchor"]["source_span_available"]
    )
    hash_match_count = sum(
        1
        for check in checks
        for item in check["evidence_items"]
        if item["source_anchor"]["current_source_hash_matches_receipt"]
    )
    summary = {
        "artifact_kind": "vaks_phase_b_evidence_support_check_summary",
        "support_check_count": len(checks),
        "source_envelope_count": len(envelopes),
        "evidence_item_count": item_count,
        "source_span_available_count": span_count,
        "current_source_hash_match_count": hash_match_count,
        "source_refresh_needed_count": item_count - hash_match_count,
        "blocked_no_source_anchor_count": sum(
            1 for item in checks if item["support_check_status"] == "blocked_no_source_anchor"
        ),
        "support_passed_count": 0,
        "support_counts_for_promotion_count": 0,
        "action_basis_allowed_count": sum(1 for item in checks if item["action_basis_allowed"]),
        "evidence_packet_allowed_count": sum(1 for item in checks if item["evidence_packet_allowed"]),
        "evidence_sufficiency_passed_count": sum(1 for item in checks if item["evidence_sufficiency_passed"]),
        "output_path": str(output_path),
        "built_at": built_at,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=SUPPORT_CHECKS_PATH)
    args = parser.parse_args()
    summary = build_all(args.output)
    print(f"support check candidates: {summary['support_check_count']}")
    print(f"evidence item count: {summary['evidence_item_count']}")
    print(f"source span available count: {summary['source_span_available_count']}")
    print(f"blocked_no_source_anchor_count: {summary['blocked_no_source_anchor_count']}")
    print(f"support_passed_count: {summary['support_passed_count']}")


if __name__ == "__main__":
    main()
