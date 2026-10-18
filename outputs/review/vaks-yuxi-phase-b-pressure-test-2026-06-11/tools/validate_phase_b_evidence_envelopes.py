import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
ENVELOPES_PATH = RESULTS_DIR / "phase_b_evidence_envelope_candidates.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_evidence_envelope_candidate_summary.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_EVIDENCE_ENVELOPE_CANDIDATE_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_evidence_envelope_candidate_check.json"

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
    "evidence_support_check",
    "evidence_sufficiency_gate",
    "human_or_explicit_review",
    "action_gate_if_action_use",
}

REQUIRED_NOT_ENOUGH = {
    "evidence_support_check_not_run",
    "evidence_sufficiency_gate_not_run",
    "human_review_not_done",
    "not_action_basis",
}

REQUIRED_ARTIFACTS = [
    "results/phase_b_evidence_envelope_candidates.jsonl",
    "results/phase_b_evidence_envelope_candidate_summary.json",
    "results/phase_b_context_pack_candidates.jsonl",
    "results/phase_b_context_pack_candidate_check.json",
    "PHASE_B_CONTEXT_PACK_CANDIDATE_DECISION.md",
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


def validate_anchor(errors: list[dict], line_no: int, section_name: str, item: dict) -> None:
    if not item.get("source_clickback"):
        add_error(errors, "missing_clickback", f"line {line_no}:{section_name}")
    if not item.get("source_hash") or not item.get("chunk_hash"):
        add_error(errors, "missing_hash", f"line {line_no}:{section_name}")
    if item.get("support_status") != "candidate_source_anchor_not_evidence_support":
        add_error(errors, "bad_support_status", f"line {line_no}:{section_name}:{item.get('support_status')}")
    if item.get("candidate_support_role") not in {"possible_review_input", "known_challenge_or_scope_input"}:
        add_error(errors, "bad_candidate_role", f"line {line_no}:{section_name}:{item.get('candidate_support_role')}")


def validate_envelope(errors: list[dict], line_no: int, envelope: dict, counts: Counter) -> None:
    counts["envelopes"] += 1
    counts[f"source_set:{envelope.get('source_set')}"] += 1
    counts[f"corpus:{envelope.get('corpus')}"] += 1
    policy = envelope.get("envelope_policy") or {}
    warrant = envelope.get("warrant") or {}
    risk = envelope.get("risk_and_scope") or {}
    suppressed = envelope.get("suppressed_flags") or {}
    if envelope.get("artifact_kind") != "vaks_phase_b_evidence_envelope_candidate":
        add_error(errors, "bad_artifact_kind", f"line {line_no}")
    if envelope.get("draft_status") != "warrant_draft_not_evidence_packet":
        add_error(errors, "bad_draft_status", f"line {line_no}:{envelope.get('draft_status')}")
    if envelope.get("truth_boundary") != "candidate_review_input_not_support":
        add_error(errors, "bad_truth_boundary", f"line {line_no}:{envelope.get('truth_boundary')}")
    for key in ["action_basis_allowed", "evidence_packet_allowed", "evidence_sufficiency_passed"]:
        if envelope.get(key) is not False:
            add_error(errors, f"{key}_leak", f"line {line_no}:{envelope.get(key)}")
    if policy.get("action_basis_allowed") is not False:
        add_error(errors, "policy_action_basis_leak", f"line {line_no}")
    if policy.get("evidence_packet_allowed") is not False:
        add_error(errors, "policy_evidence_packet_leak", f"line {line_no}")
    if policy.get("review_required_before_action") is not True:
        add_error(errors, "missing_review_required_before_action", f"line {line_no}")
    if warrant.get("warrant_status") != "draft_needs_review":
        add_error(errors, "bad_warrant_status", f"line {line_no}:{warrant.get('warrant_status')}")
    if warrant.get("basis") != "retrieval_receipts_only":
        add_error(errors, "bad_warrant_basis", f"line {line_no}:{warrant.get('basis')}")
    if warrant.get("non_circularity_checked") is not False:
        add_error(errors, "non_circularity_false_required", f"line {line_no}")
    missing_reasons = REQUIRED_NOT_ENOUGH - set(warrant.get("not_enough_because") or [])
    if missing_reasons:
        add_error(errors, "missing_not_enough_reason", f"line {line_no}:{sorted(missing_reasons)}")
    missing_gates = REQUIRED_NEXT_GATES - set(envelope.get("required_next_gates") or [])
    if missing_gates:
        add_error(errors, "missing_required_next_gate", f"line {line_no}:{sorted(missing_gates)}")
    warnings = set(risk.get("warnings") or [])
    if "evidence_envelope_candidate_not_evidence_packet" not in warnings:
        add_error(errors, "missing_envelope_warning", f"line {line_no}")
    if "warrant_draft_not_reviewed_support" not in warnings:
        add_error(errors, "missing_warrant_warning", f"line {line_no}")
    if int(suppressed.get("suppressed_receipt_action_flags") or 0) > 0:
        counts["envelopes_with_suppressed_receipt_action_flags"] += 1
        if "receipt_action_flag_suppressed_at_pack_level" not in warnings:
            add_error(errors, "missing_suppressed_receipt_warning", f"line {line_no}")
    for item in envelope.get("support_candidates") or []:
        validate_anchor(errors, line_no, "support_candidates", item)
        if item.get("candidate_support_role") != "possible_review_input":
            add_error(errors, "support_candidate_wrong_role", f"line {line_no}:{item.get('candidate_support_role')}")
    for item in envelope.get("challenge_candidates") or []:
        validate_anchor(errors, line_no, "challenge_candidates", item)
        if not item.get("challenge_kind"):
            add_error(errors, "challenge_missing_kind", f"line {line_no}")
    if int((envelope.get("source_pack_coverage_summary") or {}).get("primary_count") or 0) != len(
        envelope.get("support_candidates") or []
    ):
        add_error(errors, "support_candidate_count_mismatch", f"line {line_no}")


def validate_prior_gates(errors: list[dict]) -> dict:
    context_pack = read_json(RESULTS_DIR / "phase_b_context_pack_candidate_check.json")
    runtime = read_json(RESULTS_DIR / "phase_b_runtime_feasibility_check.json")
    minimal = read_json(RESULTS_DIR / "phase_b_minimal_doc_patch_check.json")
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    gates = {
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
    if int(summary.get("envelope_count") or 0) != 90:
        add_error(errors, "summary_envelope_count_mismatch", str(summary.get("envelope_count")))
    for key in ["action_basis_allowed_count", "evidence_packet_allowed_count", "evidence_sufficiency_passed_count"]:
        value = summary.get(key)
        if int(value if value is not None else -1) != 0:
            add_error(errors, f"summary_{key}_leak", str(value))
    for line_no, envelope in load_jsonl(ENVELOPES_PATH):
        validate_envelope(errors, line_no, envelope, counts)
    if counts["envelopes"] != int(summary.get("envelope_count") or 0):
        add_error(errors, "envelope_count_mismatch", f"{counts['envelopes']} != {summary.get('envelope_count')}")
    artifacts = validate_artifacts(errors)
    prior_gates = validate_prior_gates(errors)
    core_docs = validate_core_doc_scope(errors)
    result = {
        "evidence_envelope_status": "pass" if not errors else "fail",
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
        "record_kind: sandbox_evidence_envelope_candidate_check",
        f"status: {result['evidence_envelope_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: diagnostic_not_evidence_packet",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Evidence Envelope Candidate Check",
        "",
        "## Result",
        "",
        "```text",
        f"evidence envelope status: {result['evidence_envelope_status']}",
        f"error count: {result['error_count']}",
        f"envelope count: {result['counts'].get('envelopes', 0)}",
        f"action_basis_allowed_count: {result['summary'].get('action_basis_allowed_count')}",
        f"evidence_packet_allowed_count: {result['summary'].get('evidence_packet_allowed_count')}",
        f"evidence_sufficiency_passed_count: {result['summary'].get('evidence_sufficiency_passed_count')}",
        f"envelopes with suppressed receipt action flags: {result['counts'].get('envelopes_with_suppressed_receipt_action_flags', 0)}",
        f"required artifacts checked: {len(result['artifacts'])}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: context-pack candidate assembly",
        "required: keep context-pack/runtime/minimal/contract gates pass and produce warrant drafts without evidence/action leakage",
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
    print(f"evidence envelope status: {result['evidence_envelope_status']}")
    print(f"envelope count: {result['counts'].get('envelopes', 0)}")
    print(f"error count: {result['error_count']}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
