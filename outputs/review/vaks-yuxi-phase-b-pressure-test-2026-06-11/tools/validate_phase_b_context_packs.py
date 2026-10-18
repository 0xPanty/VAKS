import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
PACKS_PATH = RESULTS_DIR / "phase_b_context_pack_candidates.jsonl"
SUMMARY_PATH = RESULTS_DIR / "phase_b_context_pack_candidate_summary.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_CONTEXT_PACK_CANDIDATE_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_context_pack_candidate_check.json"

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

REQUIRED_STOP_CONDITIONS = {
    "do_not_treat_pack_as_action_basis",
    "do_not_treat_retrieval_score_as_evidence_support",
    "do_not_treat_graph_metadata_as_reviewed_relation",
    "run_vaks_action_gate_before_action_use",
}

REQUIRED_ARTIFACTS = [
    "PHASE_B_CONTEXT_PACK_CANDIDATE_DECISION.md",
    "PHASE_B_CONTEXT_PACK_CANDIDATE_CHECK.md",
    "PHASE_B_RUNTIME_FEASIBILITY_DECISION.md",
    "results/phase_b_context_pack_candidates.jsonl",
    "results/phase_b_context_pack_candidate_summary.json",
    "results/phase_b_runtime_feasibility_check.json",
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


def validate_pack(errors: list[dict], line_no: int, pack: dict, counts: Counter) -> None:
    counts["packs"] += 1
    counts[f"source_set:{pack.get('source_set')}"] += 1
    counts[f"corpus:{pack.get('corpus')}"] += 1
    policy = pack.get("pack_policy") or {}
    sections = pack.get("context_sections") or {}
    summary = pack.get("coverage_summary") or {}
    if pack.get("artifact_kind") != "vaks_phase_b_context_pack_candidate":
        add_error(errors, "bad_artifact_kind", f"line {line_no}")
    if pack.get("pack_status") != "candidate_not_action_basis":
        add_error(errors, "bad_pack_status", f"line {line_no}: {pack.get('pack_status')}")
    if policy.get("action_basis_allowed") is not False:
        add_error(errors, "pack_action_basis_leak", f"line {line_no}: {policy}")
    if policy.get("review_required_before_action") is not True:
        add_error(errors, "missing_review_required_before_action", f"line {line_no}")
    if policy.get("support_requires_evidence_packet") is not True:
        add_error(errors, "missing_support_requires_evidence_packet", f"line {line_no}")
    stop_conditions = set(sections.get("stop_conditions") or [])
    missing_stops = REQUIRED_STOP_CONDITIONS - stop_conditions
    if missing_stops:
        add_error(errors, "missing_stop_conditions", f"line {line_no}: {sorted(missing_stops)}")
    warnings = set(sections.get("warnings") or [])
    if "context_pack_candidate_not_action_basis" not in warnings:
        add_error(errors, "missing_candidate_warning", f"line {line_no}")
    if "vaks_action_gate_required" not in warnings:
        add_error(errors, "missing_action_gate_warning", f"line {line_no}")
    if int(summary.get("receipt_count") or 0) != 10:
        add_error(errors, "bad_receipt_count", f"line {line_no}: {summary.get('receipt_count')}")
    if int(summary.get("suppressed_receipt_action_flags") or 0) > 0:
        counts["packs_with_suppressed_receipt_action_flags"] += 1
        if "receipt_action_flag_suppressed_at_pack_level" not in warnings:
            add_error(errors, "missing_suppressed_receipt_warning", f"line {line_no}")
    for section_name in ["primary", "neighbors"]:
        for item in sections.get(section_name) or []:
            if not item.get("source_clickback"):
                add_error(errors, "missing_clickback", f"line {line_no}:{section_name}")
            if not item.get("source_hash") or not item.get("chunk_hash"):
                add_error(errors, "missing_hash", f"line {line_no}:{section_name}")
            if item.get("authority_bucket") not in {"core_framework", "reviewed"} and section_name == "primary":
                add_error(errors, "non_support_in_primary", f"line {line_no}:{item.get('vault_path')}")
            if item.get("receipt_action_basis_allowed") and policy.get("action_basis_allowed"):
                add_error(errors, "receipt_action_flag_unsuppressed", f"line {line_no}:{item.get('vault_path')}")


def validate_prior_gates(errors: list[dict]) -> dict:
    runtime = read_json(RESULTS_DIR / "phase_b_runtime_feasibility_check.json")
    minimal = read_json(RESULTS_DIR / "phase_b_minimal_doc_patch_check.json")
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    gates = {
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
    if int(summary.get("pack_count") or 0) != 90:
        add_error(errors, "summary_pack_count_mismatch", str(summary.get("pack_count")))
    action_basis_allowed_count = summary.get("action_basis_allowed_count")
    if int(action_basis_allowed_count if action_basis_allowed_count is not None else -1) != 0:
        add_error(errors, "summary_action_basis_leak", str(summary.get("action_basis_allowed_count")))
    for line_no, pack in load_jsonl(PACKS_PATH):
        validate_pack(errors, line_no, pack, counts)
    if counts["packs"] != int(summary.get("pack_count") or 0):
        add_error(errors, "pack_count_mismatch", f"{counts['packs']} != {summary.get('pack_count')}")
    artifacts = validate_artifacts(errors)
    prior_gates = validate_prior_gates(errors)
    core_docs = validate_core_doc_scope(errors)
    result = {
        "context_pack_status": "pass" if not errors else "fail",
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
        "record_kind: sandbox_context_pack_candidate_check",
        f"status: {result['context_pack_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: diagnostic_not_action_basis",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Context Pack Candidate Check",
        "",
        "## Result",
        "",
        "```text",
        f"context pack status: {result['context_pack_status']}",
        f"error count: {result['error_count']}",
        f"pack count: {result['counts'].get('packs', 0)}",
        f"action_basis_allowed_count: {result['summary'].get('action_basis_allowed_count')}",
        f"packs with suppressed receipt action flags: {result['counts'].get('packs_with_suppressed_receipt_action_flags', 0)}",
        f"required artifacts checked: {len(result['artifacts'])}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: runtime feasibility decision",
        "required: keep runtime/minimal/contract gates pass and produce candidate packs without action-basis leakage",
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
    print(f"context pack status: {result['context_pack_status']}")
    print(f"pack count: {result['counts'].get('packs', 0)}")
    print(f"error count: {result['error_count']}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
