import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
REVIEW_PACKETS_PATH = RESULTS_DIR / "phase_b_review_queue_packets.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_review_queue_packet_summary.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_REVIEW_QUEUE_PACKET_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_review_queue_packet_check.json"

APPROVED_MINIMAL_PATCH_SET = {
    "SOURCE_INTAKE.md",
    "IMPLEMENTATION_BLUEPRINT.md",
    "DEV_CONTEXT.md",
    "MEMORY_TIER.md",
}

CORE_DOCS = [
    "AGENTS.md",
    "README.md",
    "FUSION_ARCHITECTURE_V0_2_DRAFT.md",
    "SECOND_BRAIN_MODEL.md",
    "ARCHITECTURE_PRINCIPLES.md",
    "SCHEMA.md",
    "IMPLEMENTATION_BLUEPRINT.md",
    "SOURCE_INTAKE.md",
    "REFERENCE_REVIEW_PROTOCOL.md",
    "MEMORY_TIER.md",
    "DEV_CONTEXT.md",
    "REVIEW_QUEUE.md",
    "FEEDBACK.md",
    "templates/architecture-review-window-prompt.md",
]

REQUIRED_STEPS = {
    "inspect_source_span",
    "decide_span_supports_target",
    "assign_evidence_role",
    "write_reviewer_note_if_inferential",
    "keep_background_context_out_of_support",
    "run_evidence_sufficiency_only_after_support_review",
}

REQUIRED_ARTIFACTS = [
    "results/phase_b_review_queue_packets.jsonl",
    "results/phase_b_review_queue_packet_summary.json",
    "results/phase_b_refreshed_support_check_candidates.jsonl",
    "results/phase_b_refreshed_support_check_candidate_check.json",
    "PHASE_B_REFRESHED_SUPPORT_CHECK_CANDIDATE_DECISION.md",
]


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def load_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if line:
                yield line_no, json.loads(line)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_review_item(errors: list[dict], line_no: int, item: dict, counts: Counter) -> None:
    counts["review_items"] += 1
    anchor = item.get("source_anchor_ref") or {}
    support = item.get("pre_review_evidence_support") or {}
    if item.get("review_item_status") != "needs_manual_evidence_support_review":
        add_error(errors, "bad_review_item_status", f"line {line_no}:{item.get('evidence_item_id')}")
    if support.get("span_supports_target") != "unclear":
        add_error(errors, "pre_review_support_auto_pass", f"line {line_no}:{support.get('span_supports_target')}")
    if support.get("evidence_role") != "background_context":
        add_error(errors, "bad_pre_review_role", f"line {line_no}:{support.get('evidence_role')}")
    if item.get("support_counts_for_promotion") is not False:
        add_error(errors, "review_item_promotion_support_leak", f"line {line_no}:{item.get('evidence_item_id')}")
    if not anchor.get("source_span_available"):
        add_error(errors, "review_item_missing_source_span", f"line {line_no}:{item.get('evidence_item_id')}")
    else:
        counts["source_span_available"] += 1
    if anchor.get("current_source_hash_matches_receipt") is not True:
        counts["source_refresh_needed"] += 1
        add_error(errors, "review_item_source_refresh_needed", f"line {line_no}:{item.get('evidence_item_id')}")
    else:
        counts["current_source_hash_match"] += 1
    if not item.get("quote_or_excerpt"):
        add_error(errors, "missing_quote_or_excerpt", f"line {line_no}:{item.get('evidence_item_id')}")


def validate_packet(errors: list[dict], line_no: int, packet: dict, counts: Counter) -> None:
    counts["review_packets"] += 1
    counts[f"source_set:{packet.get('source_set')}"] += 1
    counts[f"corpus:{packet.get('corpus')}"] += 1
    freshness = packet.get("source_freshness") or {}
    boundary = packet.get("source_refreshed_support_boundary") or {}
    if packet.get("artifact_kind") != "vaks_phase_b_review_queue_packet":
        add_error(errors, "bad_artifact_kind", f"line {line_no}")
    if packet.get("record_type") != "review-queue-item":
        add_error(errors, "bad_record_type", f"line {line_no}:{packet.get('record_type')}")
    if packet.get("truth_boundary") != "review_queue_packet_not_reviewed_support":
        add_error(errors, "bad_truth_boundary", f"line {line_no}:{packet.get('truth_boundary')}")
    if packet.get("item_type") != "missing_evidence":
        add_error(errors, "bad_item_type", f"line {line_no}:{packet.get('item_type')}")
    if packet.get("review_route") != "evidence_check":
        add_error(errors, "bad_review_route", f"line {line_no}:{packet.get('review_route')}")
    if packet.get("promotion_target") != "none":
        add_error(errors, "promotion_target_leak", f"line {line_no}:{packet.get('promotion_target')}")
    if packet.get("review_result") != "not_reviewed":
        add_error(errors, "review_result_auto_set", f"line {line_no}:{packet.get('review_result')}")
    if (packet.get("approval_integrity") or {}).get("checked_specific_evidence") is not False:
        add_error(errors, "approval_integrity_checked_without_human", f"line {line_no}")
    for key in [
        "action_basis_allowed",
        "evidence_packet_allowed",
        "evidence_sufficiency_passed",
        "automatic_promotion_allowed",
    ]:
        if packet.get(key) is not False:
            add_error(errors, f"{key}_leak", f"line {line_no}:{packet.get(key)}")
    if int(packet.get("support_passed_count") or 0) != 0:
        add_error(errors, "support_passed_leak", f"line {line_no}")
    if int(packet.get("support_counts_for_promotion_count") or 0) != 0:
        add_error(errors, "promotion_support_leak", f"line {line_no}")
    missing_steps = REQUIRED_STEPS - set(packet.get("review_steps") or [])
    if missing_steps:
        add_error(errors, "missing_review_steps", f"line {line_no}:{sorted(missing_steps)}")
    for key in ["action_basis_allowed", "evidence_packet_allowed", "evidence_sufficiency_passed"]:
        if boundary.get(key) is not False:
            add_error(errors, f"source_boundary_{key}_leak", f"line {line_no}")
    items = packet.get("review_items") or []
    if packet.get("review_queue_state") == "blocked_no_source_anchor":
        counts["blocked_no_source_anchor"] += 1
        if packet.get("status") != "parked":
            add_error(errors, "blocked_packet_not_parked", f"line {line_no}")
        if items:
            add_error(errors, "blocked_packet_has_review_items", f"line {line_no}")
        if packet.get("suggested_action") != "mark_review_due":
            add_error(errors, "blocked_packet_bad_action", f"line {line_no}:{packet.get('suggested_action')}")
        return
    if packet.get("review_queue_state") != "open":
        add_error(errors, "bad_review_queue_state", f"line {line_no}:{packet.get('review_queue_state')}")
    else:
        counts["open_packets"] += 1
    if packet.get("status") != "open":
        add_error(errors, "open_packet_bad_status", f"line {line_no}:{packet.get('status')}")
    if packet.get("suggested_action") != "request_evidence":
        add_error(errors, "open_packet_bad_action", f"line {line_no}:{packet.get('suggested_action')}")
    if int(freshness.get("source_refresh_needed_count") or 0) != 0:
        add_error(errors, "packet_refresh_needed_leftover", f"line {line_no}:{freshness.get('source_refresh_needed_count')}")
    if not items:
        add_error(errors, "open_packet_missing_review_items", f"line {line_no}")
    for item in items:
        validate_review_item(errors, line_no, item, counts)


def validate_prior_gates(errors: list[dict]) -> dict:
    refreshed = read_json(RESULTS_DIR / "phase_b_refreshed_support_check_candidate_check.json")
    source_refresh = read_json(RESULTS_DIR / "phase_b_source_refresh_candidate_check.json")
    support = read_json(RESULTS_DIR / "phase_b_evidence_support_check_candidate_check.json")
    envelope = read_json(RESULTS_DIR / "phase_b_evidence_envelope_candidate_check.json")
    context_pack = read_json(RESULTS_DIR / "phase_b_context_pack_candidate_check.json")
    runtime = read_json(RESULTS_DIR / "phase_b_runtime_feasibility_check.json")
    minimal = read_json(RESULTS_DIR / "phase_b_minimal_doc_patch_check.json")
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    gates = {
        "refreshed_support_check": (refreshed.get("refreshed_support_check_status"), refreshed.get("error_count")),
        "source_refresh": (source_refresh.get("source_refresh_status"), source_refresh.get("error_count")),
        "evidence_support_check": (support.get("evidence_support_check_status"), support.get("error_count")),
        "evidence_envelope": (envelope.get("evidence_envelope_status"), envelope.get("error_count")),
        "context_pack": (context_pack.get("context_pack_status"), context_pack.get("error_count")),
        "runtime_feasibility": (runtime.get("runtime_feasibility_status"), runtime.get("error_count")),
        "minimal_doc_patch": (minimal.get("minimal_doc_patch_status"), minimal.get("error_count")),
        "contract": (contract.get("contract_status"), contract.get("error_count")),
    }
    for name, (status, error_count) in gates.items():
        if status != "pass" or int(error_count if error_count is not None else -1) != 0:
            add_error(errors, "prior_gate_not_pass", f"{name}: {status} / {error_count}")
    return {name: {"status": status, "errors": error_count} for name, (status, error_count) in gates.items()}


def validate_artifacts(errors: list[dict]) -> list[dict]:
    artifacts = []
    for rel in REQUIRED_ARTIFACTS:
        path = SANDBOX_DIR / rel
        exists = path.exists()
        artifacts.append({"path": rel, "exists": exists, "bytes": path.stat().st_size if exists else 0})
        if not exists:
            add_error(errors, "missing_required_artifact", rel)
        elif path.stat().st_size == 0:
            add_error(errors, "empty_required_artifact", rel)
    return artifacts


def validate_core_doc_scope(errors: list[dict]) -> dict:
    proc = subprocess.run(["git", "status", "--porcelain", "--", *CORE_DOCS], cwd=ROOT, text=True, capture_output=True)
    dirty = [line for line in proc.stdout.splitlines() if line.strip()]
    dirty_paths = {line[3:].strip() for line in dirty}
    unexpected = sorted(dirty_paths - APPROVED_MINIMAL_PATCH_SET)
    if unexpected:
        add_error(errors, "unexpected_core_doc_changed", ",".join(unexpected))
    return {"dirty": dirty}


def validate_all() -> dict:
    errors: list[dict] = []
    counts: Counter = Counter()
    summary = read_json(SUMMARY_PATH)
    previous = read_json(RESULTS_DIR / "phase_b_refreshed_support_check_candidate_summary.json")
    if int(summary.get("review_packet_count") or 0) != 90:
        add_error(errors, "summary_review_packet_count_mismatch", str(summary.get("review_packet_count")))
    refresh_needed_raw = summary.get("source_refresh_needed_count")
    if int(refresh_needed_raw if refresh_needed_raw is not None else -1) != 0:
        add_error(errors, "summary_source_refresh_needed_leftover", str(summary.get("source_refresh_needed_count")))
    previous_refresh_needed_raw = previous.get("source_refresh_needed_count")
    if int(previous_refresh_needed_raw if previous_refresh_needed_raw is not None else -1) != 0:
        add_error(errors, "previous_refreshed_support_not_clean", str(previous.get("source_refresh_needed_count")))
    for key in [
        "support_passed_count",
        "support_counts_for_promotion_count",
        "action_basis_allowed_count",
        "evidence_packet_allowed_count",
        "evidence_sufficiency_passed_count",
        "automatic_promotion_allowed_count",
    ]:
        value = summary.get(key)
        if int(value if value is not None else -1) != 0:
            add_error(errors, f"summary_{key}_leak", str(value))
    for line_no, packet in load_jsonl(REVIEW_PACKETS_PATH):
        validate_packet(errors, line_no, packet, counts)
    expected_pairs = [
        ("review_packets", "review_packet_count"),
        ("open_packets", "open_packet_count"),
        ("blocked_no_source_anchor", "blocked_no_source_anchor_count"),
        ("review_items", "review_item_count"),
        ("source_span_available", "source_span_available_count"),
        ("current_source_hash_match", "current_source_hash_match_count"),
        ("source_refresh_needed", "source_refresh_needed_count"),
    ]
    for count_key, summary_key in expected_pairs:
        if int(counts.get(count_key, 0)) != int(summary.get(summary_key) or 0):
            add_error(errors, f"{count_key}_mismatch", f"{counts.get(count_key, 0)} != {summary.get(summary_key)}")
    artifacts = validate_artifacts(errors)
    prior_gates = validate_prior_gates(errors)
    core_docs = validate_core_doc_scope(errors)
    result = {
        "review_queue_packet_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "counts": dict(counts),
        "summary": summary,
        "previous_refreshed_support_summary": previous,
        "artifacts": artifacts,
        "prior_gates": prior_gates,
        "core_docs": core_docs,
    }
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(result)
    return result


def write_markdown(result: dict) -> None:
    previous = result["previous_refreshed_support_summary"]
    lines = [
        "---",
        "record_kind: sandbox_review_queue_packet_check",
        f"status: {result['review_queue_packet_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: review_queue_packet_not_reviewed_support",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Review Queue Packet Check",
        "",
        "## Result",
        "",
        "```text",
        f"review queue packet status: {result['review_queue_packet_status']}",
        f"error count: {result['error_count']}",
        f"review packet count: {result['counts'].get('review_packets', 0)}",
        f"open packet count: {result['counts'].get('open_packets', 0)}",
        f"blocked_no_source_anchor_count: {result['counts'].get('blocked_no_source_anchor', 0)}",
        f"review item count: {result['counts'].get('review_items', 0)}",
        f"source_span_available_count: {result['counts'].get('source_span_available', 0)}",
        f"current_source_hash_match_count: {result['counts'].get('current_source_hash_match', 0)}",
        f"previous_source_refresh_needed_count: {previous.get('source_refresh_needed_count')}",
        f"current_source_refresh_needed_count: {result['summary'].get('source_refresh_needed_count')}",
        f"review_result_not_reviewed_count: {result['summary'].get('review_result_not_reviewed_count')}",
        f"support_passed_count: {result['summary'].get('support_passed_count')}",
        f"action_basis_allowed_count: {result['summary'].get('action_basis_allowed_count')}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: refreshed support-check candidate",
        "required: create review queue packets without review/support/promotion/action leakage",
        "```",
        "",
        "## Prior Gates",
        "",
        "```text",
    ]
    for name, gate in result["prior_gates"].items():
        lines.append(f"{name}: {gate['status']} / {gate['errors']} errors")
    lines.extend(["```", "", "## Errors", ""])
    if result["errors"]:
        for error in result["errors"]:
            lines.append(f"- {error['code']}: {error['detail']}")
    else:
        lines.append("- none")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    result = validate_all()
    print(f"review queue packet status: {result['review_queue_packet_status']}")
    print(f"review packet count: {result['counts'].get('review_packets', 0)}")
    print(f"review item count: {result['counts'].get('review_items', 0)}")
    print(f"error count: {result['error_count']}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
