import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
SUPPORT_CHECKS_PATH = RESULTS_DIR / "phase_b_evidence_support_check_candidates.jsonl"
REFRESH_PATH = RESULTS_DIR / "phase_b_source_refresh_candidates.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_source_refresh_candidate_summary.json"

SELECTOR_RE = re.compile(r"^L(?P<start>\d+)-L(?P<end>\d+)$")


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


def refresh_span(anchor: dict) -> dict:
    vault_path = anchor.get("vault_path") or ""
    source_range = anchor.get("source_range")
    start, end = parse_selector(source_range)
    target = ROOT / vault_path
    if not vault_path or start is None or end is None:
        return {
            "source_span_available": False,
            "source_span_error": "missing_or_unparseable_line_range",
            "current_source_hash": "",
            "source_range": source_range or "",
            "quote_or_excerpt": "",
        }
    if not target.exists() or not target.is_file():
        return {
            "source_span_available": False,
            "source_span_error": "source_file_missing",
            "current_source_hash": "",
            "source_range": source_range,
            "quote_or_excerpt": "",
        }
    text = read_text(target)
    lines = text.splitlines()
    safe_start = max(1, min(start, len(lines) or 1))
    safe_end = max(safe_start, min(end, len(lines) or safe_start))
    excerpt = "\n".join(lines[safe_start - 1 : safe_end]).strip()
    return {
        "source_span_available": bool(excerpt),
        "source_span_error": "" if excerpt else "empty_source_span",
        "current_source_hash": sha256_text(text),
        "source_range": f"L{safe_start}-L{safe_end}",
        "quote_or_excerpt": excerpt[:1200],
    }


def refreshed_warnings(original_warnings: list[str], refreshed: dict, previous_matched: bool) -> list[str]:
    warnings = [item for item in original_warnings if item != "source_hash_mismatch_requires_refresh"]
    if not refreshed.get("source_span_available"):
        warnings.append("source_refresh_blocked_missing_span")
    elif not previous_matched:
        warnings.append("source_hash_refreshed")
    return list(dict.fromkeys(warnings))


def build_refresh_item(item: dict) -> dict:
    anchor = item.get("source_anchor") or {}
    refreshed = refresh_span(anchor)
    previous_matched = bool(anchor.get("current_source_hash_matches_receipt"))
    source_span_available = bool(refreshed.get("source_span_available"))
    refreshed_hash = refreshed.get("current_source_hash") or ""
    refresh_status = "blocked_missing_source_span"
    if source_span_available and previous_matched:
        refresh_status = "already_current"
    elif source_span_available:
        refresh_status = "refreshed_current_source_hash"
    return {
        "evidence_item_id": item.get("evidence_item_id"),
        "refresh_status": refresh_status,
        "previous_source_hash": anchor.get("source_hash"),
        "previous_current_source_hash": anchor.get("current_source_hash"),
        "previous_current_source_hash_matches_receipt": previous_matched,
        "refreshed_source_hash": refreshed_hash,
        "refreshed_source_hash_matches_current": bool(source_span_available and refreshed_hash),
        "source_anchor": {
            "vault_path": anchor.get("vault_path"),
            "heading_or_anchor": anchor.get("heading_or_anchor"),
            "source_clickback": anchor.get("source_clickback"),
            "source_range": refreshed.get("source_range"),
            "quote_or_excerpt": refreshed.get("quote_or_excerpt"),
            "source_hash": refreshed_hash,
            "current_source_hash": refreshed_hash,
            "current_source_hash_matches_receipt": bool(source_span_available and refreshed_hash),
            "chunk_hash": anchor.get("chunk_hash"),
            "source_span_available": source_span_available,
            "source_span_error": refreshed.get("source_span_error"),
        },
        "evidence_support": {
            "span_supports_target": "unclear",
            "evidence_role": "background_context",
            "reviewer_note": "Source hash/span refreshed only. Semantic support still not reviewed.",
        },
        "support_check_status": "candidate_support_check_not_reviewed",
        "support_counts_for_promotion": False,
        "warning_codes": refreshed_warnings(item.get("warning_codes") or [], refreshed, previous_matched),
        "authority_bucket": item.get("authority_bucket"),
        "usage_badge": item.get("usage_badge"),
        "retrieval_reasons": item.get("retrieval_reasons") or [],
    }


def build_refresh_record(check: dict, built_at: str) -> dict:
    items = check.get("evidence_items") or []
    refresh_items = [build_refresh_item(item) for item in items]
    blocked = check.get("support_check_status") == "blocked_no_source_anchor"
    return {
        "artifact_kind": "vaks_phase_b_source_refresh_candidate",
        "source_refresh_id": check.get("support_check_id"),
        "source_support_check_id": check.get("support_check_id"),
        "source_envelope_id": check.get("source_envelope_id"),
        "source_pack_id": check.get("source_pack_id"),
        "source_set": check.get("source_set"),
        "corpus": check.get("corpus"),
        "query_id": check.get("query_id"),
        "query_group": check.get("query_group"),
        "query_intent": check.get("query_intent"),
        "source_refresh_status": "blocked_no_source_anchor" if blocked else "refreshed_snapshot_candidate",
        "truth_boundary": "source_refresh_candidate_not_support",
        "action_basis_allowed": False,
        "evidence_packet_allowed": False,
        "evidence_sufficiency_passed": False,
        "support_passed_count": 0,
        "support_counts_for_promotion_count": 0,
        "refresh_policy": {
            "policy_kind": "phase_b_source_refresh_candidate",
            "refresh_scope": "source_hash_and_span_snapshot_only",
            "rerank_or_retrieve_changed": False,
            "semantic_support_reviewed": False,
            "action_basis_allowed": False,
            "evidence_packet_allowed": False,
        },
        "refresh_items": refresh_items,
        "source_support_boundary": {
            "support_check_status": check.get("support_check_status"),
            "truth_boundary": check.get("truth_boundary"),
            "action_basis_allowed": check.get("action_basis_allowed"),
            "evidence_packet_allowed": check.get("evidence_packet_allowed"),
            "evidence_sufficiency_passed": check.get("evidence_sufficiency_passed"),
        },
        "generated_by": "phase_b_source_refresh_candidate_builder",
        "built_at": built_at,
    }


def build_all(output_path: Path) -> dict:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    support_checks = list(load_jsonl(SUPPORT_CHECKS_PATH))
    refresh_records = [build_refresh_record(check, built_at) for check in support_checks]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in refresh_records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    refresh_items = [item for record in refresh_records for item in record["refresh_items"]]
    pre_mismatch = sum(1 for item in refresh_items if not item["previous_current_source_hash_matches_receipt"])
    post_mismatch = sum(1 for item in refresh_items if not item["refreshed_source_hash_matches_current"])
    summary = {
        "artifact_kind": "vaks_phase_b_source_refresh_summary",
        "source_refresh_count": len(refresh_records),
        "source_support_check_count": len(support_checks),
        "refresh_item_count": len(refresh_items),
        "source_span_available_count": sum(
            1 for item in refresh_items if item["source_anchor"]["source_span_available"]
        ),
        "pre_refresh_mismatch_count": pre_mismatch,
        "post_refresh_mismatch_count": post_mismatch,
        "refreshed_item_count": sum(
            1 for item in refresh_items if item["refresh_status"] == "refreshed_current_source_hash"
        ),
        "already_current_item_count": sum(
            1 for item in refresh_items if item["refresh_status"] == "already_current"
        ),
        "blocked_no_source_anchor_count": sum(
            1 for item in refresh_records if item["source_refresh_status"] == "blocked_no_source_anchor"
        ),
        "support_passed_count": 0,
        "support_counts_for_promotion_count": 0,
        "action_basis_allowed_count": sum(1 for item in refresh_records if item["action_basis_allowed"]),
        "evidence_packet_allowed_count": sum(1 for item in refresh_records if item["evidence_packet_allowed"]),
        "evidence_sufficiency_passed_count": sum(
            1 for item in refresh_records if item["evidence_sufficiency_passed"]
        ),
        "output_path": str(output_path),
        "built_at": built_at,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=REFRESH_PATH)
    args = parser.parse_args()
    summary = build_all(args.output)
    print(f"source refresh candidates: {summary['source_refresh_count']}")
    print(f"refresh item count: {summary['refresh_item_count']}")
    print(f"pre_refresh_mismatch_count: {summary['pre_refresh_mismatch_count']}")
    print(f"post_refresh_mismatch_count: {summary['post_refresh_mismatch_count']}")


if __name__ == "__main__":
    main()
