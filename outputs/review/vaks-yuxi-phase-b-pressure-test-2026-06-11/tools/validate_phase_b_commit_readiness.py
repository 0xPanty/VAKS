import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

READINESS_PATH = RESULTS_DIR / "phase_b_commit_readiness.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_COMMIT_READINESS_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_commit_readiness_check.json"

APPROVED_DOC_SCOPE = [
    "SOURCE_INTAKE.md",
    "IMPLEMENTATION_BLUEPRINT.md",
    "DEV_CONTEXT.md",
    "MEMORY_TIER.md",
]

DEFERRED_FILES = [
    "SCHEMA.md",
    "REVIEW_QUEUE.md",
    "templates/architecture-review-window-prompt.md",
]

SANDBOX_REL = "outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/"

REQUIRED_ARTIFACTS = [
    "results/phase_b_commit_readiness.json",
    "PHASE_B_COMMIT_READINESS_PACKET.md",
    "PHASE_B_COMMIT_READINESS_DECISION.md",
    "results/phase_b_keep_stop_synthesis_check.json",
    "PHASE_B_KEEP_STOP_SYNTHESIS_DECISION.md",
]


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)


def status_lines(paths: list[str]) -> list[str]:
    proc = run_git(["status", "--porcelain", "--", *paths])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip())
    return [line for line in proc.stdout.splitlines() if line.strip()]


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


def validate_decision(errors: list[dict], readiness: dict) -> None:
    if readiness.get("artifact_kind") != "vaks_phase_b_commit_readiness":
        add_error(errors, "bad_artifact_kind", str(readiness.get("artifact_kind")))
    if readiness.get("compared_against_previous_version") != "phase_b_keep_stop_synthesis":
        add_error(errors, "bad_previous_version", str(readiness.get("compared_against_previous_version")))
    if readiness.get("commit_readiness_status") != "ready_pending_user_approval":
        add_error(errors, "bad_commit_readiness_status", str(readiness.get("commit_readiness_status")))
    if readiness.get("commit_without_user_approval_allowed") is not False:
        add_error(errors, "commit_without_approval_leak", str(readiness.get("commit_without_user_approval_allowed")))
    scope = readiness.get("recommended_commit_scope") or {}
    if scope.get("mainline_docs") != APPROVED_DOC_SCOPE:
        add_error(errors, "bad_mainline_doc_scope", str(scope.get("mainline_docs")))
    if scope.get("sandbox_evidence_bundle") != SANDBOX_REL:
        add_error(errors, "bad_sandbox_scope", str(scope.get("sandbox_evidence_bundle")))
    if set(readiness.get("excluded_from_commit_scope") or []) != set(DEFERRED_FILES):
        add_error(errors, "bad_excluded_scope", str(readiness.get("excluded_from_commit_scope")))
    hard_stops = set(readiness.get("hard_stops") or [])
    for required in [
        "no_commit_without_user_approval",
        "do_not_claim_original_yuxi_runtime_validated",
        "do_not_start_c_lite_from_this_commit",
        "do_not_treat_sandbox_outputs_as_reviewed_truth",
    ]:
        if required not in hard_stops:
            add_error(errors, "missing_hard_stop", required)


def validate_prior_gates(errors: list[dict], readiness: dict) -> dict:
    keep_stop = read_json(RESULTS_DIR / "phase_b_keep_stop_synthesis_check.json")
    minimal = read_json(RESULTS_DIR / "phase_b_minimal_doc_patch_check.json")
    promotion = read_json(RESULTS_DIR / "phase_b_promotion_gate_check.json")
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    runtime = read_json(RESULTS_DIR / "phase_b_runtime_feasibility_check.json")
    checks = {
        "keep_stop": (keep_stop.get("keep_stop_synthesis_status"), keep_stop.get("error_count")),
        "minimal_doc_patch": (minimal.get("minimal_doc_patch_status"), minimal.get("error_count")),
        "promotion_gate": (promotion.get("promotion_gate_status"), promotion.get("error_count")),
        "adapter_contract": (contract.get("contract_status"), contract.get("error_count")),
        "runtime_feasibility": (runtime.get("runtime_feasibility_status"), runtime.get("error_count")),
    }
    for name, (status, error_count) in checks.items():
        if status != "pass" or int(error_count if error_count is not None else -1) != 0:
            add_error(errors, "prior_gate_not_pass", f"{name}: {status} / {error_count}")
    summary = readiness.get("keep_stop_summary") or {}
    if summary.get("status") != "pass" or int(summary.get("errors") if summary.get("errors") is not None else -1) != 0:
        add_error(errors, "bad_keep_stop_summary", str(summary))
    for key in ["runtime_adoption_allowed", "c_lite_allowed", "original_yuxi_runtime_validated"]:
        if summary.get(key) is not False:
            add_error(errors, f"{key}_leak", str(summary.get(key)))
    return {name: {"status": status, "errors": error_count} for name, (status, error_count) in checks.items()}


def validate_worktree(errors: list[dict], readiness: dict) -> dict:
    core = status_lines(APPROVED_DOC_SCOPE + DEFERRED_FILES)
    sandbox = status_lines([SANDBOX_REL])
    core_paths = [line[3:].strip() for line in core]
    core_set = set(core_paths)
    approved_set = set(APPROVED_DOC_SCOPE)
    unexpected = sorted(core_set - approved_set)
    missing = sorted(approved_set - core_set)
    deferred_touched = sorted(core_set & set(DEFERRED_FILES))
    if unexpected:
        add_error(errors, "unexpected_core_doc_changed", ",".join(unexpected))
    if missing:
        add_error(errors, "approved_doc_not_dirty", ",".join(missing))
    if deferred_touched:
        add_error(errors, "deferred_file_dirty", ",".join(deferred_touched))
    if not sandbox or not all(line.startswith("?? ") or line.startswith(" M ") or line.startswith("M ") for line in sandbox):
        add_error(errors, "sandbox_status_not_visible", str(sandbox))
    if any("__pycache__" in line for line in sandbox):
        add_error(errors, "pycache_present_in_status", str(sandbox))
    observed = readiness.get("current_worktree_evidence") or {}
    if set(observed.get("changed_core_docs_observed") or []) != approved_set:
        add_error(errors, "changed_core_docs_observed_mismatch", str(observed.get("changed_core_docs_observed")))
    staged = run_git(["diff", "--cached", "--name-only", "--", *APPROVED_DOC_SCOPE, SANDBOX_REL])
    staged_paths = [line for line in staged.stdout.splitlines() if line.strip()]
    if staged_paths:
        add_error(errors, "unexpected_staged_paths", ",".join(staged_paths))
    diff_check = run_git(["diff", "--check", "--", *APPROVED_DOC_SCOPE])
    if diff_check.returncode != 0:
        add_error(errors, "diff_check_failed", (diff_check.stdout + diff_check.stderr).strip())
    return {
        "core_status_lines": core,
        "sandbox_status_lines": sandbox,
        "staged_paths": staged_paths,
        "diff_check_returncode": diff_check.returncode,
        "diff_check_stdout": diff_check.stdout,
        "diff_check_stderr": diff_check.stderr,
    }


def validate_text(errors: list[dict]) -> dict:
    packet = (SANDBOX_DIR / "PHASE_B_COMMIT_READINESS_PACKET.md").read_text(encoding="utf-8")
    decision = (SANDBOX_DIR / "PHASE_B_COMMIT_READINESS_DECISION.md").read_text(encoding="utf-8")
    for snippet in [
        "commit_readiness_status: ready_pending_user_approval",
        "commit_without_user_approval_allowed: false",
        "Phase B keep/stop synthesis",
        "runtime adoption",
        "C-lite",
    ]:
        if snippet not in packet:
            add_error(errors, "packet_snippet_missing", snippet)
    for snippet in [
        "ready for a user-approved documentation/evidence commit",
        "This is not commit approval",
        SANDBOX_REL,
    ]:
        if snippet not in decision:
            add_error(errors, "decision_snippet_missing", snippet)
    return {"packet_bytes": len(packet.encode("utf-8")), "decision_bytes": len(decision.encode("utf-8"))}


def write_markdown(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_commit_readiness_check",
        f"status: {result['commit_readiness_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: commit_readiness_not_commit_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Commit Readiness Check",
        "",
        "## Result",
        "",
        "```text",
        f"commit readiness check status: {result['commit_readiness_check_status']}",
        f"error count: {result['error_count']}",
        f"commit_readiness_status: {result['readiness'].get('commit_readiness_status')}",
        f"commit_without_user_approval_allowed: {str(result['readiness'].get('commit_without_user_approval_allowed')).lower()}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: Phase B keep/stop synthesis",
        "required: exact commit scope, no staged files, no runtime/C-lite/writeback claim",
        "```",
        "",
        "## Prior Gates",
        "",
        "```text",
    ]
    for name, gate in result["prior_gates"].items():
        lines.append(f"{name}: {gate['status']} / {gate['errors']} errors")
    lines.extend(["```", "", "## Worktree", "", "```text"])
    lines.extend(result["worktree"]["core_status_lines"] or ["<no core status>"])
    lines.extend(result["worktree"]["sandbox_status_lines"] or ["<no sandbox status>"])
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
    readiness = read_json(READINESS_PATH)
    artifacts = validate_artifacts(errors)
    validate_decision(errors, readiness)
    prior_gates = validate_prior_gates(errors, readiness)
    worktree = validate_worktree(errors, readiness)
    text = validate_text(errors)
    result = {
        "commit_readiness_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "readiness": readiness,
        "artifacts": artifacts,
        "prior_gates": prior_gates,
        "worktree": worktree,
        "text": text,
    }
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(result)
    return result


def main() -> int:
    result = validate_all()
    print(f"commit readiness check status: {result['commit_readiness_check_status']}")
    print(f"error count: {result['error_count']}")
    print(f"commit_readiness_status: {result['readiness'].get('commit_readiness_status')}")
    print(f"commit_without_user_approval_allowed: {result['readiness'].get('commit_without_user_approval_allowed')}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
