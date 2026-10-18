import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
GATES_PATH = RESULTS_DIR / "phase_b_promotion_gate_evaluations.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_promotion_gate_evaluation_summary.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_PROMOTION_GATE_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_promotion_gate_check.json"

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

REQUIRED_ZERO_SUMMARY = [
    "human_reviewed_support_count",
    "reviewed_support_count",
    "promotion_support_count",
    "promotion_allowed_count",
    "action_basis_allowed_count",
    "action_ready_count",
    "evidence_packet_created_count",
    "evidence_packet_allowed_count",
    "evidence_sufficiency_passed_count",
    "automatic_promotion_allowed_count",
    "formal_writeback_allowed_count",
    "truth_confidence_change_allowed_count",
    "reviewed_relation_creation_allowed_count",
]

REQUIRED_ARTIFACTS = [
    "results/phase_b_promotion_gate_evaluations.jsonl",
    "results/phase_b_promotion_gate_evaluation_summary.json",
    "results/phase_b_simulated_reviewer_outcomes.jsonl",
    "results/phase_b_simulated_reviewer_outcome_check.json",
    "PHASE_B_SIMULATED_REVIEWER_OUTCOME_DECISION.md",
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


def validate_gate(errors: list[dict], line_no: int, gate: dict, counts: Counter) -> None:
    counts["gate_records"] += 1
    counts[f"source_set:{gate.get('source_set')}"] += 1
    counts[f"corpus:{gate.get('corpus')}"] += 1
    support_like = gate.get("support_like_metadata") or {}
    sufficiency = gate.get("evidence_sufficiency") or {}
    boundary = gate.get("source_outcome_boundary") or {}
    if gate.get("artifact_kind") != "vaks_phase_b_promotion_gate_evaluation":
        add_error(errors, "bad_artifact_kind", f"line {line_no}")
    if gate.get("truth_boundary") != "promotion_gate_evaluation_not_promotion":
        add_error(errors, "bad_truth_boundary", f"line {line_no}:{gate.get('truth_boundary')}")
    if gate.get("gate_status") != "blocked":
        add_error(errors, "gate_not_blocked", f"line {line_no}:{gate.get('gate_status')}")
    else:
        counts["blocked_gates"] += 1
    if not gate.get("blockers"):
        add_error(errors, "missing_blockers", f"line {line_no}")
    for required in [
        "human_review_required",
        "evidence_packet_not_created",
        "evidence_sufficiency_not_run",
        "approval_integrity_not_checked",
        "automatic_promotion_forbidden",
    ]:
        if required not in set(gate.get("blockers") or []):
            add_error(errors, "missing_required_blocker", f"line {line_no}:{required}")
    if int(support_like.get("simulated_support_like_count") or 0) > 0:
        counts["gates_with_support_like_metadata"] += 1
        if "support_like_metadata_not_human_reviewed" not in set(gate.get("blockers") or []):
            add_error(errors, "support_like_without_blocker", f"line {line_no}")
    if int(support_like.get("simulated_counterexample_count") or 0) > 0:
        counts["gates_with_counterexample"] += 1
        if "counterexample_requires_review" not in set(gate.get("blockers") or []):
            add_error(errors, "counterexample_without_blocker", f"line {line_no}")
    for key in [
        "promotion_allowed",
        "action_basis_allowed",
        "evidence_packet_created",
        "evidence_packet_allowed",
        "evidence_sufficiency_passed",
        "automatic_promotion_allowed",
        "formal_writeback_allowed",
        "truth_confidence_change_allowed",
        "reviewed_relation_creation_allowed",
    ]:
        if gate.get(key) is not False:
            add_error(errors, f"{key}_leak", f"line {line_no}:{gate.get(key)}")
    for count_key in [
        "human_reviewed_support_count",
        "reviewed_support_count",
        "promotion_support_count",
    ]:
        if int(gate.get(count_key) or 0) != 0:
            add_error(errors, f"{count_key}_leak", f"line {line_no}:{gate.get(count_key)}")
    if gate.get("action_readiness") != "not_ready":
        add_error(errors, "action_readiness_leak", f"line {line_no}:{gate.get('action_readiness')}")
    if sufficiency.get("state") != "insufficient":
        add_error(errors, "bad_sufficiency_state", f"line {line_no}:{sufficiency.get('state')}")
    if sufficiency.get("required_next_step") != "human_review_required":
        add_error(errors, "bad_sufficiency_next_step", f"line {line_no}:{sufficiency.get('required_next_step')}")
    for key in [
        "action_basis_allowed",
        "evidence_packet_allowed",
        "evidence_sufficiency_passed",
        "automatic_promotion_allowed",
        "formal_writeback_allowed",
    ]:
        if boundary.get(key) is not False:
            add_error(errors, f"source_boundary_{key}_leak", f"line {line_no}")


def validate_prior_gates(errors: list[dict]) -> dict:
    simulated = read_json(RESULTS_DIR / "phase_b_simulated_reviewer_outcome_check.json")
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
        "simulated_reviewer_outcome": (simulated.get("simulated_reviewer_outcome_status"), simulated.get("error_count")),
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
    previous = read_json(RESULTS_DIR / "phase_b_simulated_reviewer_outcome_summary.json")
    if int(previous.get("simulated_direct_support_count") or 0) + int(previous.get("simulated_inferential_support_count") or 0) <= 0:
        add_error(errors, "previous_missing_support_like_metadata", "0")
    if int(summary.get("simulated_support_like_count") or 0) <= 0:
        add_error(errors, "missing_support_like_metadata", str(summary.get("simulated_support_like_count")))
    if int(summary.get("blocked_gate_count") or 0) != int(summary.get("gate_record_count") or -1):
        add_error(errors, "not_all_gates_blocked", f"{summary.get('blocked_gate_count')} != {summary.get('gate_record_count')}")
    for key in REQUIRED_ZERO_SUMMARY:
        value = summary.get(key)
        if int(value if value is not None else -1) != 0:
            add_error(errors, f"summary_{key}_leak", str(value))
    for line_no, gate in load_jsonl(GATES_PATH):
        validate_gate(errors, line_no, gate, counts)
    expected_pairs = [
        ("gate_records", "gate_record_count"),
        ("blocked_gates", "blocked_gate_count"),
        ("gates_with_support_like_metadata", "blocked_due_support_like_not_human_reviewed_count"),
        ("gates_with_counterexample", "simulated_counterexample_count"),
    ]
    for count_key, summary_key in expected_pairs:
        expected = int(summary.get(summary_key) or 0)
        if count_key == "gates_with_counterexample":
            expected = int(summary.get("simulated_counterexample_count") or 0)
            expected = sum(1 for _, gate in load_jsonl(GATES_PATH) if (gate.get("support_like_metadata") or {}).get("simulated_counterexample_count"))
        if int(counts.get(count_key, 0)) != expected:
            add_error(errors, f"{count_key}_mismatch", f"{counts.get(count_key, 0)} != {expected}")
    artifacts = validate_artifacts(errors)
    prior_gates = validate_prior_gates(errors)
    core_docs = validate_core_doc_scope(errors)
    result = {
        "promotion_gate_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "counts": dict(counts),
        "summary": summary,
        "previous_simulated_outcome_summary": previous,
        "artifacts": artifacts,
        "prior_gates": prior_gates,
        "core_docs": core_docs,
    }
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(result)
    return result


def write_markdown(result: dict) -> None:
    previous = result["previous_simulated_outcome_summary"]
    lines = [
        "---",
        "record_kind: sandbox_promotion_gate_check",
        f"status: {result['promotion_gate_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: promotion_gate_evaluation_not_promotion",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Promotion Gate Check",
        "",
        "## Result",
        "",
        "```text",
        f"promotion gate status: {result['promotion_gate_status']}",
        f"error count: {result['error_count']}",
        f"gate record count: {result['counts'].get('gate_records', 0)}",
        f"blocked gate count: {result['summary'].get('blocked_gate_count')}",
        f"previous simulated support-like count: {int(previous.get('simulated_direct_support_count') or 0) + int(previous.get('simulated_inferential_support_count') or 0)}",
        f"simulated support-like count: {result['summary'].get('simulated_support_like_count')}",
        f"blocked_due_support_like_not_human_reviewed_count: {result['summary'].get('blocked_due_support_like_not_human_reviewed_count')}",
        f"human_reviewed_support_count: {result['summary'].get('human_reviewed_support_count')}",
        f"promotion_allowed_count: {result['summary'].get('promotion_allowed_count')}",
        f"evidence_sufficiency_passed_count: {result['summary'].get('evidence_sufficiency_passed_count')}",
        f"action_basis_allowed_count: {result['summary'].get('action_basis_allowed_count')}",
        f"formal_writeback_allowed_count: {result['summary'].get('formal_writeback_allowed_count')}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: simulated reviewer outcome",
        "required: support-like simulated metadata must be blocked from promotion, sufficiency pass, writeback, and action basis",
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
    print(f"promotion gate status: {result['promotion_gate_status']}")
    print(f"gate record count: {result['counts'].get('gate_records', 0)}")
    print(f"blocked gate count: {result['summary'].get('blocked_gate_count')}")
    print(f"error count: {result['error_count']}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
