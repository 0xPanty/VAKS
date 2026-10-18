import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

GATE_PATH = RESULTS_DIR / "phase_b_next_action_gate.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_NEXT_ACTION_GATE_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_next_action_gate_check.json"

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
    "results/phase_b_next_action_gate.json",
    "PHASE_B_NEXT_ACTION_GATE_PACKET.md",
    "PHASE_B_NEXT_ACTION_GATE_DECISION.md",
    "results/phase_b_commit_readiness_check.json",
    "PHASE_B_COMMIT_READINESS_DECISION.md",
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


def validate_decision(errors: list[dict], gate: dict) -> None:
    if gate.get("artifact_kind") != "vaks_phase_b_next_action_gate":
        add_error(errors, "bad_artifact_kind", str(gate.get("artifact_kind")))
    if gate.get("compared_against_previous_version") != "phase_b_commit_readiness":
        add_error(errors, "bad_previous_version", str(gate.get("compared_against_previous_version")))
    if gate.get("next_action_gate_status") != "pass":
        add_error(errors, "bad_next_action_gate_status", str(gate.get("next_action_gate_status")))
    if gate.get("recommended_next_action") != "await_user_approved_commit_or_runner_choice":
        add_error(errors, "bad_recommended_next_action", str(gate.get("recommended_next_action")))
    commit_path = gate.get("commit_path") or {}
    runtime_path = gate.get("original_yuxi_runtime_path") or {}
    c_lite_path = gate.get("c_lite_path") or {}
    adoption_path = gate.get("runtime_adoption_path") or {}
    if commit_path.get("status") != "ready_pending_user_approval":
        add_error(errors, "bad_commit_path_status", str(commit_path.get("status")))
    if commit_path.get("commit_without_user_approval_allowed") is not False:
        add_error(errors, "commit_without_approval_leak", str(commit_path.get("commit_without_user_approval_allowed")))
    if runtime_path.get("status") != "blocked_until_docker_or_remote_runner":
        add_error(errors, "bad_runtime_path_status", str(runtime_path.get("status")))
    if runtime_path.get("docker_path") is not None:
        add_error(errors, "unexpected_docker_available", str(runtime_path.get("docker_path")))
    if runtime_path.get("original_yuxi_runtime_validated") is not False:
        add_error(errors, "original_yuxi_runtime_validated_leak", str(runtime_path.get("original_yuxi_runtime_validated")))
    if c_lite_path.get("status") != "not_allowed_from_current_evidence":
        add_error(errors, "bad_c_lite_path_status", str(c_lite_path.get("status")))
    if c_lite_path.get("c_lite_allowed") is not False:
        add_error(errors, "c_lite_allowed_leak", str(c_lite_path.get("c_lite_allowed")))
    if adoption_path.get("status") != "not_allowed":
        add_error(errors, "bad_runtime_adoption_status", str(adoption_path.get("status")))
    if adoption_path.get("runtime_adoption_allowed") is not False:
        add_error(errors, "runtime_adoption_allowed_leak", str(adoption_path.get("runtime_adoption_allowed")))
    hard_stops = set(gate.get("hard_stops") or [])
    for required in [
        "do_not_commit_without_user_approval",
        "do_not_start_c_lite_without_new_user_gate",
        "do_not_claim_original_yuxi_runtime_validated",
        "do_not_claim_runtime_adoption",
        "do_not_treat_sandbox_or_commit_as_reviewed_truth",
    ]:
        if required not in hard_stops:
            add_error(errors, "missing_hard_stop", required)


def validate_prior_gates(errors: list[dict], gate: dict) -> dict:
    expected = {
        "commit_readiness": ("phase_b_commit_readiness_check.json", "commit_readiness_check_status"),
        "keep_stop": ("phase_b_keep_stop_synthesis_check.json", "keep_stop_synthesis_status"),
        "minimal_doc_patch": ("phase_b_minimal_doc_patch_check.json", "minimal_doc_patch_status"),
        "promotion_gate": ("phase_b_promotion_gate_check.json", "promotion_gate_status"),
        "adapter_contract": ("phase_b_adapter_contract_test.json", "contract_status"),
        "runtime_feasibility": ("phase_b_runtime_feasibility_check.json", "runtime_feasibility_status"),
    }
    observed = {}
    gate_prior = gate.get("prior_gates") or {}
    for name, (file_name, status_key) in expected.items():
        payload = read_json(RESULTS_DIR / file_name)
        status = payload.get(status_key)
        error_count = payload.get("error_count")
        observed[name] = {"status": status, "errors": error_count}
        if status != "pass" or int(error_count if error_count is not None else -1) != 0:
            add_error(errors, "prior_gate_not_pass", f"{name}: {status} / {error_count}")
        synthesized = gate_prior.get(name) or {}
        if synthesized.get("status") != status or synthesized.get("errors") != error_count:
            add_error(errors, "prior_gate_mismatch", f"{name}: {synthesized} != {observed[name]}")
    return observed


def validate_worktree(errors: list[dict], gate: dict) -> dict:
    core = status_lines(APPROVED_DOC_SCOPE + DEFERRED_FILES)
    sandbox = status_lines([SANDBOX_REL])
    staged = run_git(["diff", "--cached", "--name-only", "--", *APPROVED_DOC_SCOPE, SANDBOX_REL]).stdout.splitlines()
    core_paths = {line[3:].strip() for line in core}
    unexpected = sorted(core_paths - set(APPROVED_DOC_SCOPE))
    missing = sorted(set(APPROVED_DOC_SCOPE) - core_paths)
    deferred = sorted(core_paths & set(DEFERRED_FILES))
    if unexpected:
        add_error(errors, "unexpected_core_doc_changed", ",".join(unexpected))
    if missing:
        add_error(errors, "approved_doc_not_dirty", ",".join(missing))
    if deferred:
        add_error(errors, "deferred_file_dirty", ",".join(deferred))
    if staged:
        add_error(errors, "unexpected_staged_paths", ",".join(staged))
    if not sandbox:
        add_error(errors, "sandbox_status_missing", "")
    if any("__pycache__" in line for line in sandbox):
        add_error(errors, "pycache_present", str(sandbox))
    recorded = gate.get("worktree") or {}
    if set(recorded.get("staged_paths") or []) != set([line for line in staged if line.strip()]):
        add_error(errors, "recorded_staged_mismatch", str(recorded.get("staged_paths")))
    return {
        "core_status_lines": core,
        "sandbox_status_lines": sandbox,
        "staged_paths": [line for line in staged if line.strip()],
    }


def validate_text(errors: list[dict]) -> dict:
    packet = (SANDBOX_DIR / "PHASE_B_NEXT_ACTION_GATE_PACKET.md").read_text(encoding="utf-8")
    decision = (SANDBOX_DIR / "PHASE_B_NEXT_ACTION_GATE_DECISION.md").read_text(encoding="utf-8")
    for snippet in [
        "next_action_gate_status: pass",
        "recommended_next_action: await_user_approved_commit_or_runner_choice",
        "commit_without_user_approval_allowed: false",
        "runtime_adoption_allowed: false",
        "c_lite_allowed: false",
    ]:
        if snippet not in packet:
            add_error(errors, "packet_snippet_missing", snippet)
    for snippet in [
        "The next action is gated, not automatic.",
        "C-lite and runtime adoption remain not allowed.",
        "commit_without_user_approval_allowed: false",
    ]:
        if snippet not in decision:
            add_error(errors, "decision_snippet_missing", snippet)
    return {"packet_bytes": len(packet.encode("utf-8")), "decision_bytes": len(decision.encode("utf-8"))}


def write_markdown(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_next_action_gate_check",
        f"status: {result['next_action_gate_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: next_action_gate_not_action_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Next-Action Gate Check",
        "",
        "## Result",
        "",
        "```text",
        f"next action gate check status: {result['next_action_gate_check_status']}",
        f"error count: {result['error_count']}",
        f"recommended_next_action: {result['gate'].get('recommended_next_action')}",
        f"commit_without_user_approval_allowed: {str((result['gate'].get('commit_path') or {}).get('commit_without_user_approval_allowed')).lower()}",
        f"runtime_adoption_allowed: {str((result['gate'].get('runtime_adoption_path') or {}).get('runtime_adoption_allowed')).lower()}",
        f"c_lite_allowed: {str((result['gate'].get('c_lite_path') or {}).get('c_lite_allowed')).lower()}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: Phase B commit-readiness",
        "required: choose next branch without granting commit/runtime/C-lite authority",
        "```",
        "",
        "## Prior Gates",
        "",
        "```text",
    ]
    for name, prior in result["prior_gates"].items():
        lines.append(f"{name}: {prior['status']} / {prior['errors']} errors")
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
    gate = read_json(GATE_PATH)
    artifacts = validate_artifacts(errors)
    validate_decision(errors, gate)
    prior_gates = validate_prior_gates(errors, gate)
    worktree = validate_worktree(errors, gate)
    text = validate_text(errors)
    result = {
        "next_action_gate_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "gate": gate,
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
    print(f"next action gate check status: {result['next_action_gate_check_status']}")
    print(f"error count: {result['error_count']}")
    print(f"recommended_next_action: {result['gate'].get('recommended_next_action')}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
