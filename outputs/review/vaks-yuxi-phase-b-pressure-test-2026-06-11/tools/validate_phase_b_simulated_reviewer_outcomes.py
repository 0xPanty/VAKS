import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
OUTCOMES_PATH = RESULTS_DIR / "phase_b_simulated_reviewer_outcomes.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_simulated_reviewer_outcome_summary.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_SIMULATED_REVIEWER_OUTCOME_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_simulated_reviewer_outcome_check.json"

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

REQUIRED_ARTIFACTS = [
    "results/phase_b_simulated_reviewer_outcomes.jsonl",
    "results/phase_b_simulated_reviewer_outcome_summary.json",
    "results/phase_b_review_queue_packets.jsonl",
    "results/phase_b_review_queue_packet_check.json",
    "PHASE_B_REVIEW_QUEUE_PACKET_DECISION.md",
]

ALLOWED_REVIEW_RESULTS = {
    "simulation_recorded_not_human_review",
    "not_reviewed",
    "blocked_no_source_anchor",
}


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


def validate_item_outcome(errors: list[dict], line_no: int, item: dict, counts: Counter) -> None:
    counts["simulated_item_outcomes"] += 1
    support = item.get("simulated_evidence_support") or {}
    role = support.get("evidence_role")
    status = support.get("span_supports_target")
    if item.get("human_reviewed") is not False:
        add_error(errors, "item_human_reviewed_leak", f"line {line_no}:{item.get('evidence_item_id')}")
    if item.get("counts_as_reviewed_support") is not False:
        add_error(errors, "item_reviewed_support_leak", f"line {line_no}:{item.get('evidence_item_id')}")
    if item.get("support_counts_for_promotion") is not False:
        add_error(errors, "item_promotion_support_leak", f"line {line_no}:{item.get('evidence_item_id')}")
    if item.get("allowed_next_step") != "human_review_required":
        add_error(errors, "bad_allowed_next_step", f"line {line_no}:{item.get('allowed_next_step')}")
    if role == "direct_support" and status == "supported":
        counts["simulated_direct_support"] += 1
    elif role == "inferential_support" and status == "partial":
        counts["simulated_inferential_support"] += 1
        if not support.get("reviewer_note"):
            add_error(errors, "inferential_missing_note", f"line {line_no}:{item.get('evidence_item_id')}")
    elif role == "background_context":
        counts["simulated_background"] += 1
    elif role == "counterexample":
        counts["simulated_counterexample"] += 1
    else:
        add_error(errors, "bad_simulated_support_shape", f"line {line_no}:{status}/{role}")


def validate_outcome(errors: list[dict], line_no: int, outcome: dict, counts: Counter) -> None:
    counts["outcome_records"] += 1
    counts[f"source_set:{outcome.get('source_set')}"] += 1
    counts[f"corpus:{outcome.get('corpus')}"] += 1
    boundary = outcome.get("source_review_packet_boundary") or {}
    if outcome.get("artifact_kind") != "vaks_phase_b_simulated_reviewer_outcome":
        add_error(errors, "bad_artifact_kind", f"line {line_no}")
    if outcome.get("truth_boundary") != "simulated_reviewer_outcome_not_reviewed_support":
        add_error(errors, "bad_truth_boundary", f"line {line_no}:{outcome.get('truth_boundary')}")
    if outcome.get("review_result") not in ALLOWED_REVIEW_RESULTS:
        add_error(errors, "bad_review_result", f"line {line_no}:{outcome.get('review_result')}")
    if outcome.get("human_reviewed") is not False:
        add_error(errors, "human_reviewed_leak", f"line {line_no}")
    if (outcome.get("approval_integrity") or {}).get("checked_specific_evidence") is not False:
        add_error(errors, "approval_integrity_checked_without_human", f"line {line_no}")
    for key in [
        "action_basis_allowed",
        "evidence_packet_allowed",
        "evidence_sufficiency_passed",
        "automatic_promotion_allowed",
        "formal_writeback_allowed",
        "counts_as_reviewed_support",
    ]:
        if outcome.get(key) is not False:
            add_error(errors, f"{key}_leak", f"line {line_no}:{outcome.get(key)}")
    for count_key in [
        "support_passed_count",
        "support_counts_for_promotion_count",
        "human_reviewed_support_count",
    ]:
        if int(outcome.get(count_key) or 0) != 0:
            add_error(errors, f"{count_key}_leak", f"line {line_no}:{outcome.get(count_key)}")
    if int(outcome.get("source_refresh_needed_count") or 0) != 0:
        add_error(errors, "source_refresh_needed_leftover", f"line {line_no}:{outcome.get('source_refresh_needed_count')}")
    for key in [
        "action_basis_allowed",
        "evidence_packet_allowed",
        "evidence_sufficiency_passed",
        "automatic_promotion_allowed",
    ]:
        if boundary.get(key) is not False:
            add_error(errors, f"source_boundary_{key}_leak", f"line {line_no}")
    items = outcome.get("simulated_item_outcomes") or []
    if outcome.get("simulated_review_applied"):
        counts["simulated_packets"] += 1
        if outcome.get("review_result") != "simulation_recorded_not_human_review":
            add_error(errors, "simulated_packet_bad_result", f"line {line_no}:{outcome.get('review_result')}")
        if outcome.get("review_queue_state_after_simulation") != "in-review":
            add_error(errors, "simulated_packet_bad_queue_state", f"line {line_no}:{outcome.get('review_queue_state_after_simulation')}")
        if not items:
            add_error(errors, "simulated_packet_missing_items", f"line {line_no}")
    elif outcome.get("review_result") == "blocked_no_source_anchor":
        counts["blocked_no_source_anchor"] += 1
        if outcome.get("review_queue_state_after_simulation") != "parked":
            add_error(errors, "blocked_packet_bad_queue_state", f"line {line_no}:{outcome.get('review_queue_state_after_simulation')}")
        if items:
            add_error(errors, "blocked_packet_has_simulated_items", f"line {line_no}")
    else:
        counts["not_reviewed_packets"] += 1
        if outcome.get("review_result") != "not_reviewed":
            add_error(errors, "unselected_packet_bad_result", f"line {line_no}:{outcome.get('review_result')}")
        if outcome.get("review_queue_state_after_simulation") != "open":
            add_error(errors, "unselected_packet_bad_queue_state", f"line {line_no}:{outcome.get('review_queue_state_after_simulation')}")
        if items:
            add_error(errors, "unselected_packet_has_items", f"line {line_no}")
    for item in items:
        validate_item_outcome(errors, line_no, item, counts)


def validate_prior_gates(errors: list[dict]) -> dict:
    review_queue = read_json(RESULTS_DIR / "phase_b_review_queue_packet_check.json")
    refreshed = read_json(RESULTS_DIR / "phase_b_refreshed_support_check_candidate_check.json")
    source_refresh = read_json(RESULTS_DIR / "phase_b_source_refresh_candidate_check.json")
    support = read_json(RESULTS_DIR / "phase_b_evidence_support_check_candidate_check.json")
    envelope = read_json(RESULTS_DIR / "phase_b_evidence_envelope_candidate_check.json")
    context_pack = read_json(RESULTS_DIR / "phase_b_context_pack_candidate_check.json")
    runtime = read_json(RESULTS_DIR / "phase_b_runtime_feasibility_check.json")
    minimal = read_json(RESULTS_DIR / "phase_b_minimal_doc_patch_check.json")
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    gates = {
        "review_queue_packet": (review_queue.get("review_queue_packet_status"), review_queue.get("error_count")),
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
    previous = read_json(RESULTS_DIR / "phase_b_review_queue_packet_summary.json")
    if int(previous.get("review_result_not_reviewed_count") or 0) != 90:
        add_error(errors, "previous_review_queue_not_baseline", str(previous.get("review_result_not_reviewed_count")))
    if int(summary.get("simulated_packet_count") or 0) <= 0:
        add_error(errors, "missing_simulated_packets", str(summary.get("simulated_packet_count")))
    if int(summary.get("simulated_item_outcome_count") or 0) <= 0:
        add_error(errors, "missing_simulated_items", str(summary.get("simulated_item_outcome_count")))
    for key in [
        "source_refresh_needed_count",
        "human_reviewed_support_count",
        "support_passed_count",
        "support_counts_for_promotion_count",
        "action_basis_allowed_count",
        "evidence_packet_allowed_count",
        "evidence_sufficiency_passed_count",
        "automatic_promotion_allowed_count",
        "formal_writeback_allowed_count",
    ]:
        value = summary.get(key)
        if int(value if value is not None else -1) != 0:
            add_error(errors, f"summary_{key}_leak", str(value))
    for line_no, outcome in load_jsonl(OUTCOMES_PATH):
        validate_outcome(errors, line_no, outcome, counts)
    expected_pairs = [
        ("outcome_records", "outcome_record_count"),
        ("simulated_packets", "simulated_packet_count"),
        ("not_reviewed_packets", "not_reviewed_packet_count"),
        ("blocked_no_source_anchor", "blocked_no_source_anchor_count"),
        ("simulated_item_outcomes", "simulated_item_outcome_count"),
        ("simulated_direct_support", "simulated_direct_support_count"),
        ("simulated_inferential_support", "simulated_inferential_support_count"),
        ("simulated_background", "simulated_background_count"),
        ("simulated_counterexample", "simulated_counterexample_count"),
    ]
    for count_key, summary_key in expected_pairs:
        if int(counts.get(count_key, 0)) != int(summary.get(summary_key) or 0):
            add_error(errors, f"{count_key}_mismatch", f"{counts.get(count_key, 0)} != {summary.get(summary_key)}")
    artifacts = validate_artifacts(errors)
    prior_gates = validate_prior_gates(errors)
    core_docs = validate_core_doc_scope(errors)
    result = {
        "simulated_reviewer_outcome_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "counts": dict(counts),
        "summary": summary,
        "previous_review_queue_summary": previous,
        "artifacts": artifacts,
        "prior_gates": prior_gates,
        "core_docs": core_docs,
    }
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(result)
    return result


def write_markdown(result: dict) -> None:
    previous = result["previous_review_queue_summary"]
    lines = [
        "---",
        "record_kind: sandbox_simulated_reviewer_outcome_check",
        f"status: {result['simulated_reviewer_outcome_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: simulated_reviewer_outcome_not_reviewed_support",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Simulated Reviewer Outcome Check",
        "",
        "## Result",
        "",
        "```text",
        f"simulated reviewer outcome status: {result['simulated_reviewer_outcome_status']}",
        f"error count: {result['error_count']}",
        f"outcome record count: {result['counts'].get('outcome_records', 0)}",
        f"previous_review_result_not_reviewed_count: {previous.get('review_result_not_reviewed_count')}",
        f"simulated_packet_count: {result['summary'].get('simulated_packet_count')}",
        f"not_reviewed_packet_count: {result['summary'].get('not_reviewed_packet_count')}",
        f"blocked_no_source_anchor_count: {result['summary'].get('blocked_no_source_anchor_count')}",
        f"simulated_item_outcome_count: {result['summary'].get('simulated_item_outcome_count')}",
        f"simulated_direct_support_count: {result['summary'].get('simulated_direct_support_count')}",
        f"simulated_inferential_support_count: {result['summary'].get('simulated_inferential_support_count')}",
        f"human_reviewed_support_count: {result['summary'].get('human_reviewed_support_count')}",
        f"support_passed_count: {result['summary'].get('support_passed_count')}",
        f"action_basis_allowed_count: {result['summary'].get('action_basis_allowed_count')}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: review queue packet",
        "required: simulated outcome metadata without human-reviewed support, promotion, writeback, or action leakage",
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
    print(f"simulated reviewer outcome status: {result['simulated_reviewer_outcome_status']}")
    print(f"outcome record count: {result['counts'].get('outcome_records', 0)}")
    print(f"simulated item outcome count: {result['counts'].get('simulated_item_outcomes', 0)}")
    print(f"error count: {result['error_count']}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
