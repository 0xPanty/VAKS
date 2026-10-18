import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

SYNTHESIS_PATH = RESULTS_DIR / "phase_b_keep_stop_synthesis.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_KEEP_STOP_SYNTHESIS_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_keep_stop_synthesis_check.json"

APPROVED_DOC_SCOPE = [
    "SOURCE_INTAKE.md",
    "IMPLEMENTATION_BLUEPRINT.md",
    "DEV_CONTEXT.md",
    "MEMORY_TIER.md",
]

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
    "results/phase_b_keep_stop_synthesis.json",
    "PHASE_B_KEEP_STOP_SYNTHESIS_PACKET.md",
    "PHASE_B_KEEP_STOP_SYNTHESIS_DECISION.md",
    "PHASE_B_PROMOTION_GATE_DECISION.md",
    "results/phase_b_promotion_gate_check.json",
]

REQUIRED_FALSE_FLAGS = [
    "original_yuxi_runtime_validated",
    "runtime_adoption_allowed",
    "c_lite_allowed",
    "skills_mcp_subagents_allowed",
    "formal_writeback_allowed",
]

REQUIRED_ZERO_COUNTS = [
    "promotion_allowed_count",
    "action_basis_allowed_count",
    "action_ready_count",
    "evidence_packet_created_count",
    "evidence_packet_allowed_count",
    "evidence_sufficiency_passed_count",
    "automatic_promotion_allowed_count",
    "truth_confidence_change_allowed_count",
    "reviewed_relation_creation_allowed_count",
]

PRIOR_GATES = {
    "promotion_gate": ("phase_b_promotion_gate_check.json", "promotion_gate_status"),
    "simulated_reviewer_outcome": ("phase_b_simulated_reviewer_outcome_check.json", "simulated_reviewer_outcome_status"),
    "review_queue_packet": ("phase_b_review_queue_packet_check.json", "review_queue_packet_status"),
    "refreshed_support_check": ("phase_b_refreshed_support_check_candidate_check.json", "refreshed_support_check_status"),
    "source_refresh": ("phase_b_source_refresh_candidate_check.json", "source_refresh_status"),
    "evidence_support_check": ("phase_b_evidence_support_check_candidate_check.json", "evidence_support_check_status"),
    "evidence_envelope": ("phase_b_evidence_envelope_candidate_check.json", "evidence_envelope_status"),
    "context_pack": ("phase_b_context_pack_candidate_check.json", "context_pack_status"),
    "runtime_feasibility": ("phase_b_runtime_feasibility_check.json", "runtime_feasibility_status"),
    "minimal_doc_patch": ("phase_b_minimal_doc_patch_check.json", "minimal_doc_patch_status"),
    "adapter_contract": ("phase_b_adapter_contract_test.json", "contract_status"),
    "integration_readiness": ("phase_b_integration_readiness_check.json", "readiness_status"),
    "mainline_readiness": ("phase_b_mainline_readiness_check.json", "mainline_readiness_status"),
    "external_review_result": ("phase_b_external_review_result_check.json", "external_review_status"),
    "pro_review_prompt": ("phase_b_pro_review_prompt_check.json", "prompt_status"),
}


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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


def validate_prior_gates(errors: list[dict], synthesis: dict) -> dict:
    gates = {}
    for name, (file_name, status_key) in PRIOR_GATES.items():
        payload = read_json(RESULTS_DIR / file_name)
        status = payload.get(status_key)
        error_count = payload.get("error_count")
        gates[name] = {"status": status, "errors": error_count}
        if status != "pass" or int(error_count if error_count is not None else -1) != 0:
            add_error(errors, "prior_gate_not_pass", f"{name}: {status} / {error_count}")
        synthesized = (synthesis.get("prior_gates") or {}).get(name) or {}
        if synthesized.get("status") != status or synthesized.get("errors") != error_count:
            add_error(errors, "prior_gate_mismatch_in_synthesis", f"{name}: {synthesized} != {gates[name]}")
    return gates


def validate_core_doc_scope(errors: list[dict], synthesis: dict) -> dict:
    proc = subprocess.run(["git", "status", "--porcelain", "--", *CORE_DOCS], cwd=ROOT, text=True, capture_output=True)
    dirty = [line for line in proc.stdout.splitlines() if line.strip()]
    dirty_paths = [line[3:].strip() for line in dirty]
    dirty_set = set(dirty_paths)
    approved_set = set(APPROVED_DOC_SCOPE)
    unexpected = sorted(dirty_set - approved_set)
    missing = sorted(approved_set - dirty_set)
    if unexpected:
        add_error(errors, "unexpected_core_doc_changed", ",".join(unexpected))
    if missing:
        add_error(errors, "approved_doc_missing_from_dirty_set", ",".join(missing))
    if synthesis.get("documentation_patch_scope") != APPROVED_DOC_SCOPE:
        add_error(errors, "bad_documentation_patch_scope", str(synthesis.get("documentation_patch_scope")))
    if set(synthesis.get("changed_core_docs_observed") or []) != approved_set:
        add_error(errors, "bad_changed_core_docs_observed", str(synthesis.get("changed_core_docs_observed")))
    return {"dirty": dirty}


def validate_retrieval_value(errors: list[dict], synthesis: dict) -> dict:
    retrieval = synthesis.get("retrieval_evidence") or {}
    positive_checks = retrieval.get("positive_checks") or {}
    false_checks = [name for name, value in positive_checks.items() if value is not True]
    if false_checks:
        add_error(errors, "retrieval_positive_check_failed", ",".join(false_checks))
    if synthesis.get("positive_value_confirmed") is not True:
        add_error(errors, "positive_value_not_confirmed", str(synthesis.get("positive_value_confirmed")))
    main_primary = ((retrieval.get("main_pressure") or {}).get("primary") or {})
    main_full = ((retrieval.get("main_pressure") or {}).get("full") or {})
    holdout_primary = ((retrieval.get("holdout_pressure") or {}).get("primary") or {})
    holdout_full = ((retrieval.get("holdout_pressure") or {}).get("full") or {})
    required_pairs = [
        ("main_primary_baseline_hit_at_5", main_primary.get("baseline_file_lexical", {}).get("hit_at_5"), "27/30"),
        ("main_primary_skeleton_hit_at_5", main_primary.get("vaks_b_adapter_skeleton", {}).get("hit_at_5"), "30/30"),
        ("main_full_baseline_hit_at_5", main_full.get("baseline_file_lexical", {}).get("hit_at_5"), "27/30"),
        ("main_full_skeleton_hit_at_5", main_full.get("vaks_b_adapter_skeleton", {}).get("hit_at_5"), "30/30"),
        ("holdout_primary_baseline_hit_at_5", holdout_primary.get("baseline_file_lexical", {}).get("hit_at_5"), "9/15"),
        ("holdout_primary_skeleton_hit_at_5", holdout_primary.get("vaks_b_adapter_skeleton", {}).get("hit_at_5"), "12/15"),
        ("holdout_full_yuxi_native_hit_at_5", holdout_full.get("yuxi_native_profile", {}).get("hit_at_5"), "8/15"),
        ("holdout_full_skeleton_hit_at_5", holdout_full.get("vaks_b_adapter_skeleton", {}).get("hit_at_5"), "13/15"),
    ]
    for name, actual, expected in required_pairs:
        if actual != expected:
            add_error(errors, "retrieval_metric_mismatch", f"{name}: {actual} != {expected}")
    return {"positive_checks": positive_checks}


def validate_pipeline_counts(errors: list[dict], synthesis: dict) -> dict:
    counts = synthesis.get("pipeline_counts") or {}
    expected = {
        "context_pack_count": 90,
        "evidence_envelope_count": 90,
        "support_check_count": 90,
        "evidence_item_count": 389,
        "source_span_available_count": 389,
        "pre_refresh_needed_count": 68,
        "post_refresh_needed_count": 0,
        "pre_refresh_mismatch_count": 68,
        "post_refresh_mismatch_count": 0,
        "current_source_hash_match_count": 389,
        "review_packet_count": 90,
        "open_packet_count": 88,
        "blocked_no_source_anchor_count": 2,
        "simulated_support_like_count": 24,
        "blocked_gate_count": 90,
        "gate_record_count": 90,
    }
    for key, expected_value in expected.items():
        actual = counts.get(key)
        if int(actual if actual is not None else -1) != expected_value:
            add_error(errors, "pipeline_count_mismatch", f"{key}: {actual} != {expected_value}")
    if synthesis.get("no_boundary_leak_confirmed") is not True:
        add_error(errors, "boundary_leak_not_confirmed", str(synthesis.get("no_boundary_leak_confirmed")))
    return counts


def validate_decision_flags(errors: list[dict], synthesis: dict) -> None:
    if synthesis.get("artifact_kind") != "vaks_phase_b_keep_stop_synthesis":
        add_error(errors, "bad_artifact_kind", str(synthesis.get("artifact_kind")))
    if synthesis.get("compared_against_previous_version") != "phase_b_promotion_gate_sufficiency_block":
        add_error(errors, "bad_previous_version", str(synthesis.get("compared_against_previous_version")))
    if synthesis.get("keep_stop_decision") != "keep_phase_b_as_sandbox_candidate":
        add_error(errors, "bad_keep_stop_decision", str(synthesis.get("keep_stop_decision")))
    if synthesis.get("reject_full_runtime_adoption") is not True:
        add_error(errors, "full_runtime_adoption_not_rejected", str(synthesis.get("reject_full_runtime_adoption")))
    if synthesis.get("runtime_status") != "original_yuxi_full_stack_unvalidated_docker_unavailable":
        add_error(errors, "bad_runtime_status", str(synthesis.get("runtime_status")))
    if synthesis.get("mainline_status") != "documentation_only_patch_validated_not_committed":
        add_error(errors, "bad_mainline_status", str(synthesis.get("mainline_status")))
    for key in REQUIRED_FALSE_FLAGS:
        if synthesis.get(key) is not False:
            add_error(errors, f"{key}_leak", str(synthesis.get(key)))
    for key in REQUIRED_ZERO_COUNTS:
        value = synthesis.get(key)
        if int(value if value is not None else -1) != 0:
            add_error(errors, f"{key}_leak", str(value))
    hard_stops = set(synthesis.get("hard_stops") or [])
    for required in [
        "do_not_claim_original_yuxi_runtime_validated",
        "do_not_promote_to_c_lite",
        "do_not_attach_skills_mcp_subagents_or_writeback",
        "do_not_create_evidence_packet_or_action_basis_from_simulation",
    ]:
        if required not in hard_stops:
            add_error(errors, "missing_hard_stop", required)


def validate_packet_text(errors: list[dict]) -> dict:
    packet = (SANDBOX_DIR / "PHASE_B_KEEP_STOP_SYNTHESIS_PACKET.md").read_text(encoding="utf-8")
    decision = (SANDBOX_DIR / "PHASE_B_KEEP_STOP_SYNTHESIS_DECISION.md").read_text(encoding="utf-8")
    required_packet_snippets = [
        "keep_stop_decision: keep_phase_b_as_sandbox_candidate",
        "positive_value_confirmed: true",
        "no_boundary_leak_confirmed: true",
        "original Yuxi full-stack testing",
        "Do not start C-lite or runtime adoption from this packet alone.",
    ]
    required_decision_snippets = [
        "Keep Phase B as a positive sandbox and documentation candidate only.",
        "original_yuxi_runtime_validated: false",
        "runtime_adoption_allowed: false",
        "c_lite_allowed: false",
    ]
    for snippet in required_packet_snippets:
        if snippet not in packet:
            add_error(errors, "packet_snippet_missing", snippet)
    for snippet in required_decision_snippets:
        if snippet not in decision:
            add_error(errors, "decision_snippet_missing", snippet)
    return {"packet_bytes": len(packet.encode("utf-8")), "decision_bytes": len(decision.encode("utf-8"))}


def write_markdown(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_keep_stop_synthesis_check",
        f"status: {result['keep_stop_synthesis_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: keep_stop_synthesis_not_runtime_adoption",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Keep / Stop Synthesis Check",
        "",
        "## Result",
        "",
        "```text",
        f"keep stop synthesis status: {result['keep_stop_synthesis_status']}",
        f"error count: {result['error_count']}",
        f"keep_stop_decision: {result['synthesis'].get('keep_stop_decision')}",
        f"positive_value_confirmed: {str(result['synthesis'].get('positive_value_confirmed')).lower()}",
        f"no_boundary_leak_confirmed: {str(result['synthesis'].get('no_boundary_leak_confirmed')).lower()}",
        f"promotion_allowed_count: {result['synthesis'].get('promotion_allowed_count')}",
        f"action_basis_allowed_count: {result['synthesis'].get('action_basis_allowed_count')}",
        f"runtime_adoption_allowed: {str(result['synthesis'].get('runtime_adoption_allowed')).lower()}",
        f"c_lite_allowed: {str(result['synthesis'].get('c_lite_allowed')).lower()}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: promotion-gate / sufficiency-block sandbox",
        "required: synthesize keep/stop without granting new authority",
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


def validate_all() -> dict:
    errors: list[dict] = []
    synthesis = read_json(SYNTHESIS_PATH)
    artifacts = validate_artifacts(errors)
    prior_gates = validate_prior_gates(errors, synthesis)
    core_docs = validate_core_doc_scope(errors, synthesis)
    retrieval = validate_retrieval_value(errors, synthesis)
    pipeline_counts = validate_pipeline_counts(errors, synthesis)
    validate_decision_flags(errors, synthesis)
    packet_text = validate_packet_text(errors)
    result = {
        "keep_stop_synthesis_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "synthesis": synthesis,
        "artifacts": artifacts,
        "prior_gates": prior_gates,
        "core_docs": core_docs,
        "retrieval": retrieval,
        "pipeline_counts": pipeline_counts,
        "packet_text": packet_text,
    }
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(result)
    return result


def main() -> int:
    result = validate_all()
    print(f"keep stop synthesis status: {result['keep_stop_synthesis_status']}")
    print(f"error count: {result['error_count']}")
    print(f"keep_stop_decision: {result['synthesis'].get('keep_stop_decision')}")
    print(f"positive_value_confirmed: {result['synthesis'].get('positive_value_confirmed')}")
    print(f"no_boundary_leak_confirmed: {result['synthesis'].get('no_boundary_leak_confirmed')}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
