import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
SUPPORT_CHECKS_PATH = RESULTS_DIR / "phase_b_evidence_support_check_candidates.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_evidence_support_check_candidate_summary.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_EVIDENCE_SUPPORT_CHECK_CANDIDATE_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_evidence_support_check_candidate_check.json"

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

REQUIRED_NEXT_GATES = {
    "human_evidence_support_review",
    "non_circular_warrant_review",
    "evidence_sufficiency_gate",
    "action_gate_if_action_use",
}

REQUIRED_NOTES = {
    "semantic_support_not_reviewed",
    "support_status_remains_unclear",
}

ALLOWED_CHECK_STATUSES = {
    "candidate_support_check_not_reviewed",
    "blocked_no_source_anchor",
}

REQUIRED_ARTIFACTS = [
    "results/phase_b_evidence_support_check_candidates.jsonl",
    "results/phase_b_evidence_support_check_candidate_summary.json",
    "results/phase_b_evidence_envelope_candidates.jsonl",
    "results/phase_b_evidence_envelope_candidate_check.json",
    "PHASE_B_EVIDENCE_ENVELOPE_CANDIDATE_DECISION.md",
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


def validate_item(errors: list[dict], line_no: int, item: dict, counts: Counter) -> None:
    counts["evidence_items"] += 1
    anchor = item.get("source_anchor") or {}
    support = item.get("evidence_support") or {}
    target = item.get("target") or {}
    if item.get("support_check_status") != "candidate_support_check_not_reviewed":
        add_error(errors, "bad_item_status", f"line {line_no}:{item.get('evidence_item_id')}")
    if item.get("support_counts_for_promotion") is not False:
        add_error(errors, "item_support_counts_for_promotion_leak", f"line {line_no}:{item.get('evidence_item_id')}")
    if support.get("span_supports_target") != "unclear":
        add_error(errors, "semantic_support_auto_pass", f"line {line_no}:{support.get('span_supports_target')}")
    if support.get("evidence_role") != "background_context":
        add_error(errors, "bad_evidence_role", f"line {line_no}:{support.get('evidence_role')}")
    if not support.get("reviewer_note"):
        add_error(errors, "missing_reviewer_note", f"line {line_no}:{item.get('evidence_item_id')}")
    if target.get("target_status") != "not_fixed_review_candidate":
        add_error(errors, "target_fixed_without_review", f"line {line_no}:{target.get('target_status')}")
    if not anchor.get("source_clickback") or not anchor.get("source_range"):
        add_error(errors, "missing_source_range_or_clickback", f"line {line_no}:{item.get('evidence_item_id')}")
    if not anchor.get("source_hash") or not anchor.get("current_source_hash") or not anchor.get("chunk_hash"):
        add_error(errors, "missing_hash", f"line {line_no}:{item.get('evidence_item_id')}")
    if anchor.get("source_span_available"):
        counts["source_span_available"] += 1
        if not anchor.get("quote_or_excerpt"):
            add_error(errors, "missing_quote_or_excerpt", f"line {line_no}:{item.get('evidence_item_id')}")
    if anchor.get("current_source_hash_matches_receipt"):
        counts["current_source_hash_match"] += 1
    else:
        counts["source_refresh_needed"] += 1
        if "source_hash_mismatch_requires_refresh" not in set(item.get("warning_codes") or []):
            add_error(errors, "missing_refresh_warning", f"line {line_no}:{item.get('evidence_item_id')}")


def validate_check(errors: list[dict], line_no: int, check: dict, counts: Counter) -> None:
    counts["support_checks"] += 1
    counts[f"source_set:{check.get('source_set')}"] += 1
    counts[f"corpus:{check.get('corpus')}"] += 1
    policy = check.get("support_check_policy") or {}
    boundary = check.get("source_envelope_boundary") or {}
    if check.get("artifact_kind") != "vaks_phase_b_evidence_support_check_candidate":
        add_error(errors, "bad_artifact_kind", f"line {line_no}")
    if check.get("support_check_status") not in ALLOWED_CHECK_STATUSES:
        add_error(errors, "bad_check_status", f"line {line_no}:{check.get('support_check_status')}")
    if check.get("truth_boundary") != "source_span_check_candidate_not_support":
        add_error(errors, "bad_truth_boundary", f"line {line_no}:{check.get('truth_boundary')}")
    for key in ["action_basis_allowed", "evidence_packet_allowed", "evidence_sufficiency_passed"]:
        if check.get(key) is not False:
            add_error(errors, f"{key}_leak", f"line {line_no}:{check.get(key)}")
    if int(check.get("support_passed_count") or 0) != 0:
        add_error(errors, "support_passed_leak", f"line {line_no}:{check.get('support_passed_count')}")
    if int(check.get("support_counts_for_promotion_count") or 0) != 0:
        add_error(errors, "promotion_support_leak", f"line {line_no}:{check.get('support_counts_for_promotion_count')}")
    if policy.get("semantic_support_reviewed") is not False:
        add_error(errors, "semantic_support_reviewed_leak", f"line {line_no}")
    if policy.get("action_basis_allowed") is not False or policy.get("evidence_packet_allowed") is not False:
        add_error(errors, "policy_permission_leak", f"line {line_no}")
    if policy.get("review_required_before_support") is not True:
        add_error(errors, "missing_review_required_before_support", f"line {line_no}")
    if boundary.get("action_basis_allowed") is not False:
        add_error(errors, "source_envelope_action_basis_leak", f"line {line_no}")
    if boundary.get("evidence_packet_allowed") is not False:
        add_error(errors, "source_envelope_packet_leak", f"line {line_no}")
    if boundary.get("evidence_sufficiency_passed") is not False:
        add_error(errors, "source_envelope_sufficiency_leak", f"line {line_no}")
    missing_gates = REQUIRED_NEXT_GATES - set(check.get("required_next_gates") or [])
    if missing_gates:
        add_error(errors, "missing_required_next_gate", f"line {line_no}:{sorted(missing_gates)}")
    missing_notes = REQUIRED_NOTES - set(check.get("support_check_notes") or [])
    if missing_notes:
        add_error(errors, "missing_support_check_note", f"line {line_no}:{sorted(missing_notes)}")
    items = check.get("evidence_items") or []
    if items:
        if "source_span_snapshot_created" not in set(check.get("support_check_notes") or []):
            add_error(errors, "missing_source_span_snapshot_note", f"line {line_no}")
        if check.get("support_check_status") == "blocked_no_source_anchor":
            add_error(errors, "blocked_check_has_items", f"line {line_no}")
    else:
        counts["blocked_no_source_anchor"] += 1
    if not items and check.get("support_check_status") != "blocked_no_source_anchor":
        add_error(errors, "missing_evidence_items", f"line {line_no}")
    if not items and "no_source_anchor_available" not in set(check.get("support_check_notes") or []):
        add_error(errors, "missing_no_source_anchor_note", f"line {line_no}")
    for item in items:
        validate_item(errors, line_no, item, counts)


def validate_prior_gates(errors: list[dict]) -> dict:
    envelope = read_json(RESULTS_DIR / "phase_b_evidence_envelope_candidate_check.json")
    context_pack = read_json(RESULTS_DIR / "phase_b_context_pack_candidate_check.json")
    runtime = read_json(RESULTS_DIR / "phase_b_runtime_feasibility_check.json")
    minimal = read_json(RESULTS_DIR / "phase_b_minimal_doc_patch_check.json")
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    gates = {
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
    if int(summary.get("support_check_count") or 0) != 90:
        add_error(errors, "summary_support_check_count_mismatch", str(summary.get("support_check_count")))
    for key in [
        "support_passed_count",
        "support_counts_for_promotion_count",
        "action_basis_allowed_count",
        "evidence_packet_allowed_count",
        "evidence_sufficiency_passed_count",
    ]:
        value = summary.get(key)
        if int(value if value is not None else -1) != 0:
            add_error(errors, f"summary_{key}_leak", str(value))
    for line_no, check in load_jsonl(SUPPORT_CHECKS_PATH):
        validate_check(errors, line_no, check, counts)
    if counts["support_checks"] != int(summary.get("support_check_count") or 0):
        add_error(errors, "support_check_count_mismatch", f"{counts['support_checks']} != {summary.get('support_check_count')}")
    if counts["evidence_items"] != int(summary.get("evidence_item_count") or 0):
        add_error(errors, "evidence_item_count_mismatch", f"{counts['evidence_items']} != {summary.get('evidence_item_count')}")
    if counts["source_span_available"] != int(summary.get("source_span_available_count") or 0):
        add_error(errors, "source_span_count_mismatch", f"{counts['source_span_available']} != {summary.get('source_span_available_count')}")
    if counts["current_source_hash_match"] != int(summary.get("current_source_hash_match_count") or 0):
        add_error(errors, "hash_match_count_mismatch", f"{counts['current_source_hash_match']} != {summary.get('current_source_hash_match_count')}")
    if counts["blocked_no_source_anchor"] != int(summary.get("blocked_no_source_anchor_count") or 0):
        add_error(errors, "blocked_no_source_anchor_count_mismatch", f"{counts['blocked_no_source_anchor']} != {summary.get('blocked_no_source_anchor_count')}")
    artifacts = validate_artifacts(errors)
    prior_gates = validate_prior_gates(errors)
    core_docs = validate_core_doc_scope(errors)
    result = {
        "evidence_support_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "counts": dict(counts),
        "summary": summary,
        "artifacts": artifacts,
        "prior_gates": prior_gates,
        "core_docs": core_docs,
    }
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(result)
    return result


def write_markdown(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_evidence_support_check_candidate_check",
        f"status: {result['evidence_support_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: source_span_check_candidate_not_support",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Evidence Support Check Candidate Check",
        "",
        "## Result",
        "",
        "```text",
        f"evidence support check status: {result['evidence_support_check_status']}",
        f"error count: {result['error_count']}",
        f"support check count: {result['counts'].get('support_checks', 0)}",
        f"evidence item count: {result['counts'].get('evidence_items', 0)}",
        f"source_span_available_count: {result['counts'].get('source_span_available', 0)}",
        f"current_source_hash_match_count: {result['counts'].get('current_source_hash_match', 0)}",
        f"source_refresh_needed_count: {result['counts'].get('source_refresh_needed', 0)}",
        f"blocked_no_source_anchor_count: {result['counts'].get('blocked_no_source_anchor', 0)}",
        f"support_passed_count: {result['summary'].get('support_passed_count')}",
        f"support_counts_for_promotion_count: {result['summary'].get('support_counts_for_promotion_count')}",
        f"action_basis_allowed_count: {result['summary'].get('action_basis_allowed_count')}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: evidence-envelope / warrant-draft assembly",
        "required: create source-span support-check candidates without semantic support or action leakage",
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
    print(f"evidence support check status: {result['evidence_support_check_status']}")
    print(f"support check count: {result['counts'].get('support_checks', 0)}")
    print(f"evidence item count: {result['counts'].get('evidence_items', 0)}")
    print(f"error count: {result['error_count']}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
