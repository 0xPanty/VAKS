import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
REFRESHED_SUPPORT_PATH = RESULTS_DIR / "phase_b_refreshed_support_check_candidates.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_refreshed_support_check_candidate_summary.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_REFRESHED_SUPPORT_CHECK_CANDIDATE_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_refreshed_support_check_candidate_check.json"

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

REQUIRED_GATES = {
    "human_evidence_support_review",
    "non_circular_warrant_review",
    "evidence_sufficiency_gate",
    "action_gate_if_action_use",
}

REQUIRED_ARTIFACTS = [
    "results/phase_b_refreshed_support_check_candidates.jsonl",
    "results/phase_b_refreshed_support_check_candidate_summary.json",
    "results/phase_b_source_refresh_candidates.jsonl",
    "results/phase_b_source_refresh_candidate_check.json",
    "PHASE_B_SOURCE_REFRESH_CANDIDATE_DECISION.md",
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
    if item.get("refresh_status") == "refreshed_current_source_hash":
        counts["refreshed_items"] += 1
        if "source_hash_refreshed" not in set(item.get("warning_codes") or []):
            add_error(errors, "missing_refreshed_warning", f"line {line_no}:{item.get('evidence_item_id')}")
    elif item.get("refresh_status") == "already_current":
        counts["already_current_items"] += 1
    else:
        add_error(errors, "bad_refresh_status", f"line {line_no}:{item.get('evidence_item_id')}")
    if "source_hash_mismatch_requires_refresh" in set(item.get("warning_codes") or []):
        add_error(errors, "stale_refresh_warning_leftover", f"line {line_no}:{item.get('evidence_item_id')}")
    if not anchor.get("source_span_available"):
        add_error(errors, "missing_source_span", f"line {line_no}:{item.get('evidence_item_id')}")
    else:
        counts["source_span_available"] += 1
    if not anchor.get("quote_or_excerpt"):
        add_error(errors, "missing_quote_or_excerpt", f"line {line_no}:{item.get('evidence_item_id')}")
    if not anchor.get("source_hash") or anchor.get("source_hash") != anchor.get("current_source_hash"):
        add_error(errors, "bad_source_hash_pair", f"line {line_no}:{item.get('evidence_item_id')}")
    if anchor.get("current_source_hash_matches_receipt") is not True:
        counts["source_refresh_needed"] += 1
        add_error(errors, "source_refresh_needed_leftover", f"line {line_no}:{item.get('evidence_item_id')}")
    else:
        counts["current_source_hash_match"] += 1
    if support.get("span_supports_target") != "unclear":
        add_error(errors, "semantic_support_auto_pass", f"line {line_no}:{support.get('span_supports_target')}")
    if support.get("evidence_role") != "background_context":
        add_error(errors, "bad_evidence_role", f"line {line_no}:{support.get('evidence_role')}")
    if item.get("support_counts_for_promotion") is not False:
        add_error(errors, "promotion_support_leak", f"line {line_no}:{item.get('evidence_item_id')}")


def validate_check(errors: list[dict], line_no: int, check: dict, counts: Counter) -> None:
    counts["refreshed_support_checks"] += 1
    counts[f"source_set:{check.get('source_set')}"] += 1
    counts[f"corpus:{check.get('corpus')}"] += 1
    policy = check.get("rebuild_policy") or {}
    boundary = check.get("source_refresh_boundary") or {}
    if check.get("artifact_kind") != "vaks_phase_b_refreshed_support_check_candidate":
        add_error(errors, "bad_artifact_kind", f"line {line_no}")
    if check.get("truth_boundary") != "refreshed_source_span_check_candidate_not_support":
        add_error(errors, "bad_truth_boundary", f"line {line_no}:{check.get('truth_boundary')}")
    for key in ["action_basis_allowed", "evidence_packet_allowed", "evidence_sufficiency_passed"]:
        if check.get(key) is not False:
            add_error(errors, f"{key}_leak", f"line {line_no}:{check.get(key)}")
    if int(check.get("support_passed_count") or 0) != 0:
        add_error(errors, "support_passed_leak", f"line {line_no}")
    if int(check.get("support_counts_for_promotion_count") or 0) != 0:
        add_error(errors, "promotion_support_leak", f"line {line_no}")
    if int(check.get("source_refresh_needed_count") or 0) != 0:
        add_error(errors, "check_source_refresh_needed_leftover", f"line {line_no}")
    if policy.get("source") != "phase_b_source_refresh_candidate":
        add_error(errors, "bad_rebuild_source", f"line {line_no}:{policy.get('source')}")
    if policy.get("source_hash_and_span_refreshed") is not True:
        add_error(errors, "missing_refreshed_policy", f"line {line_no}")
    if policy.get("rerank_or_retrieve_changed") is not False:
        add_error(errors, "rerank_changed_in_rebuild", f"line {line_no}")
    if policy.get("semantic_support_reviewed") is not False:
        add_error(errors, "semantic_support_reviewed_leak", f"line {line_no}")
    if policy.get("action_basis_allowed") is not False or policy.get("evidence_packet_allowed") is not False:
        add_error(errors, "policy_permission_leak", f"line {line_no}")
    if boundary.get("action_basis_allowed") is not False:
        add_error(errors, "source_refresh_action_basis_leak", f"line {line_no}")
    if boundary.get("evidence_packet_allowed") is not False:
        add_error(errors, "source_refresh_packet_leak", f"line {line_no}")
    if boundary.get("evidence_sufficiency_passed") is not False:
        add_error(errors, "source_refresh_sufficiency_leak", f"line {line_no}")
    missing_gates = REQUIRED_GATES - set(check.get("required_next_gates") or [])
    if missing_gates:
        add_error(errors, "missing_required_gate", f"line {line_no}:{sorted(missing_gates)}")
    items = check.get("evidence_items") or []
    if check.get("support_check_status") == "blocked_no_source_anchor":
        counts["blocked_no_source_anchor"] += 1
        if items:
            add_error(errors, "blocked_check_has_items", f"line {line_no}")
        if "no_source_anchor_available" not in set(check.get("support_check_notes") or []):
            add_error(errors, "missing_no_anchor_note", f"line {line_no}")
        return
    if check.get("support_check_status") != "candidate_support_check_not_reviewed":
        add_error(errors, "bad_support_check_status", f"line {line_no}:{check.get('support_check_status')}")
    if not items:
        add_error(errors, "missing_evidence_items", f"line {line_no}")
    for note in ["refreshed_source_span_snapshot_applied", "semantic_support_not_reviewed", "support_status_remains_unclear"]:
        if note not in set(check.get("support_check_notes") or []):
            add_error(errors, "missing_support_note", f"line {line_no}:{note}")
    for item in items:
        validate_item(errors, line_no, item, counts)


def validate_prior_gates(errors: list[dict]) -> dict:
    source_refresh = read_json(RESULTS_DIR / "phase_b_source_refresh_candidate_check.json")
    support = read_json(RESULTS_DIR / "phase_b_evidence_support_check_candidate_check.json")
    envelope = read_json(RESULTS_DIR / "phase_b_evidence_envelope_candidate_check.json")
    context_pack = read_json(RESULTS_DIR / "phase_b_context_pack_candidate_check.json")
    runtime = read_json(RESULTS_DIR / "phase_b_runtime_feasibility_check.json")
    minimal = read_json(RESULTS_DIR / "phase_b_minimal_doc_patch_check.json")
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    gates = {
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
    previous_support = read_json(RESULTS_DIR / "phase_b_evidence_support_check_candidate_summary.json")
    source_refresh = read_json(RESULTS_DIR / "phase_b_source_refresh_candidate_summary.json")
    if int(summary.get("refreshed_support_check_count") or 0) != 90:
        add_error(errors, "summary_refreshed_support_count_mismatch", str(summary.get("refreshed_support_check_count")))
    previous_refresh_needed = int(previous_support.get("source_refresh_needed_count") or 0)
    current_refresh_needed_raw = summary.get("source_refresh_needed_count")
    current_refresh_needed = int(current_refresh_needed_raw if current_refresh_needed_raw is not None else -1)
    if previous_refresh_needed <= 0:
        add_error(errors, "missing_positive_previous_refresh_needed", str(previous_refresh_needed))
    if current_refresh_needed != 0:
        add_error(errors, "summary_source_refresh_needed_leftover", str(current_refresh_needed))
    post_refresh_raw = source_refresh.get("post_refresh_mismatch_count")
    if int(post_refresh_raw if post_refresh_raw is not None else -1) != 0:
        add_error(errors, "source_refresh_prior_not_clean", str(source_refresh.get("post_refresh_mismatch_count")))
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
    for line_no, check in load_jsonl(REFRESHED_SUPPORT_PATH):
        validate_check(errors, line_no, check, counts)
    expected_pairs = [
        ("refreshed_support_checks", "refreshed_support_check_count"),
        ("evidence_items", "evidence_item_count"),
        ("source_span_available", "source_span_available_count"),
        ("current_source_hash_match", "current_source_hash_match_count"),
        ("source_refresh_needed", "source_refresh_needed_count"),
        ("refreshed_items", "refreshed_item_count"),
        ("already_current_items", "already_current_item_count"),
        ("blocked_no_source_anchor", "blocked_no_source_anchor_count"),
    ]
    for count_key, summary_key in expected_pairs:
        if int(counts.get(count_key, 0)) != int(summary.get(summary_key) or 0):
            add_error(errors, f"{count_key}_mismatch", f"{counts.get(count_key, 0)} != {summary.get(summary_key)}")
    artifacts = validate_artifacts(errors)
    prior_gates = validate_prior_gates(errors)
    core_docs = validate_core_doc_scope(errors)
    result = {
        "refreshed_support_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "counts": dict(counts),
        "summary": summary,
        "previous_support_summary": previous_support,
        "source_refresh_summary": source_refresh,
        "artifacts": artifacts,
        "prior_gates": prior_gates,
        "core_docs": core_docs,
    }
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(result)
    return result


def write_markdown(result: dict) -> None:
    previous = result["previous_support_summary"]
    lines = [
        "---",
        "record_kind: sandbox_refreshed_support_check_candidate_check",
        f"status: {result['refreshed_support_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: refreshed_source_span_check_candidate_not_support",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Refreshed Support Check Candidate Check",
        "",
        "## Result",
        "",
        "```text",
        f"refreshed support check status: {result['refreshed_support_check_status']}",
        f"error count: {result['error_count']}",
        f"refreshed support check count: {result['counts'].get('refreshed_support_checks', 0)}",
        f"evidence item count: {result['counts'].get('evidence_items', 0)}",
        f"source_span_available_count: {result['counts'].get('source_span_available', 0)}",
        f"previous_source_refresh_needed_count: {previous.get('source_refresh_needed_count')}",
        f"current_source_refresh_needed_count: {result['summary'].get('source_refresh_needed_count')}",
        f"current_source_hash_match_count: {result['summary'].get('current_source_hash_match_count')}",
        f"refreshed_item_count: {result['summary'].get('refreshed_item_count')}",
        f"already_current_item_count: {result['summary'].get('already_current_item_count')}",
        f"blocked_no_source_anchor_count: {result['summary'].get('blocked_no_source_anchor_count')}",
        f"support_passed_count: {result['summary'].get('support_passed_count')}",
        f"action_basis_allowed_count: {result['summary'].get('action_basis_allowed_count')}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: source-refresh candidate assembly and original Evidence Support Check candidate summary",
        "required: rebuild support-check view with refresh-needed count at 0 and no support/action leakage",
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
    print(f"refreshed support check status: {result['refreshed_support_check_status']}")
    print(f"refreshed support check count: {result['counts'].get('refreshed_support_checks', 0)}")
    print(f"evidence item count: {result['counts'].get('evidence_items', 0)}")
    print(f"error count: {result['error_count']}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
