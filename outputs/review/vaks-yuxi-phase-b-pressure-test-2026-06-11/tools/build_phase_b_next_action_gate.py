import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

GATE_PATH = RESULTS_DIR / "phase_b_next_action_gate.json"
PACKET_PATH = SANDBOX_DIR / "PHASE_B_NEXT_ACTION_GATE_PACKET.md"
DECISION_PATH = SANDBOX_DIR / "PHASE_B_NEXT_ACTION_GATE_DECISION.md"

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


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)


def status_lines(paths: list[str]) -> list[str]:
    proc = run_git(["status", "--porcelain", "--", *paths])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip())
    return [line for line in proc.stdout.splitlines() if line.strip()]


def build_gate() -> dict:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    commit_readiness = read_json(RESULTS_DIR / "phase_b_commit_readiness_check.json")
    commit_payload = read_json(RESULTS_DIR / "phase_b_commit_readiness.json")
    keep_stop = read_json(RESULTS_DIR / "phase_b_keep_stop_synthesis_check.json")
    runtime = read_json(RESULTS_DIR / "phase_b_runtime_feasibility_check.json")
    minimal = read_json(RESULTS_DIR / "phase_b_minimal_doc_patch_check.json")
    promotion = read_json(RESULTS_DIR / "phase_b_promotion_gate_check.json")
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    core_status = status_lines(APPROVED_DOC_SCOPE + DEFERRED_FILES)
    sandbox_status = status_lines([SANDBOX_REL])
    staged = run_git(["diff", "--cached", "--name-only", "--", *APPROVED_DOC_SCOPE, SANDBOX_REL]).stdout.splitlines()
    docker_path = (runtime.get("environment") or {}).get("docker_path")
    return {
        "artifact_kind": "vaks_phase_b_next_action_gate",
        "built_at": built_at,
        "compared_against_previous_version": "phase_b_commit_readiness",
        "next_action_gate_status": "pass",
        "recommended_next_action": "await_user_approved_commit_or_runner_choice",
        "commit_path": {
            "status": "ready_pending_user_approval",
            "commit_without_user_approval_allowed": False,
            "recommended_scope": commit_payload.get("recommended_commit_scope"),
            "excluded_scope": DEFERRED_FILES,
            "suggested_commit_message": commit_payload.get("suggested_commit_message"),
        },
        "original_yuxi_runtime_path": {
            "status": "blocked_until_docker_or_remote_runner",
            "docker_path": docker_path,
            "original_yuxi_runtime_validated": False,
            "can_continue_if": "Docker/Compose or a remote runner is provided and a new runtime gate passes.",
        },
        "c_lite_path": {
            "status": "not_allowed_from_current_evidence",
            "c_lite_allowed": False,
            "required_before_open": [
                "user approves next sandbox explicitly",
                "Phase B documentation/evidence commit is either completed or deliberately deferred",
                "original runtime/full-stack assumptions are not claimed without runtime evidence",
                "new C-lite validator preserves no writeback/action/truth promotion",
            ],
        },
        "runtime_adoption_path": {
            "status": "not_allowed",
            "runtime_adoption_allowed": False,
            "reason": "Original Yuxi full-stack is unvalidated locally and Phase B is only a sandbox/documentation candidate.",
        },
        "prior_gates": {
            "commit_readiness": {
                "status": commit_readiness.get("commit_readiness_check_status"),
                "errors": commit_readiness.get("error_count"),
            },
            "keep_stop": {
                "status": keep_stop.get("keep_stop_synthesis_status"),
                "errors": keep_stop.get("error_count"),
            },
            "minimal_doc_patch": {
                "status": minimal.get("minimal_doc_patch_status"),
                "errors": minimal.get("error_count"),
            },
            "promotion_gate": {
                "status": promotion.get("promotion_gate_status"),
                "errors": promotion.get("error_count"),
            },
            "adapter_contract": {
                "status": contract.get("contract_status"),
                "errors": contract.get("error_count"),
            },
            "runtime_feasibility": {
                "status": runtime.get("runtime_feasibility_status"),
                "errors": runtime.get("error_count"),
            },
        },
        "worktree": {
            "core_status_lines": core_status,
            "sandbox_status_lines": sandbox_status,
            "staged_paths": [line for line in staged if line.strip()],
        },
        "hard_stops": [
            "do_not_commit_without_user_approval",
            "do_not_start_c_lite_without_new_user_gate",
            "do_not_claim_original_yuxi_runtime_validated",
            "do_not_claim_runtime_adoption",
            "do_not_treat_sandbox_or_commit_as_reviewed_truth",
            "do_not_stage_deferred_files",
        ],
    }


def write_packet(gate: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_next_action_gate_packet",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: next_action_gate_not_action_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Next-Action Gate Packet",
        "",
        "## Decision",
        "",
        "```text",
        f"next_action_gate_status: {gate['next_action_gate_status']}",
        f"recommended_next_action: {gate['recommended_next_action']}",
        f"commit_path: {gate['commit_path']['status']}",
        f"original_yuxi_runtime_path: {gate['original_yuxi_runtime_path']['status']}",
        f"c_lite_path: {gate['c_lite_path']['status']}",
        f"runtime_adoption_path: {gate['runtime_adoption_path']['status']}",
        "```",
        "",
        "## Compared Against Previous Version",
        "",
        "Previous version:",
        "",
        "```text",
        "Phase B commit-readiness scope check",
        "```",
        "",
        "This step adds:",
        "",
        "```text",
        "branch choice gate",
        "commit vs runtime vs C-lite separation",
        "explicit external-condition and user-approval requirements",
        "```",
        "",
        "It preserves:",
        "",
        "```text",
        f"commit_without_user_approval_allowed: {str(gate['commit_path']['commit_without_user_approval_allowed']).lower()}",
        f"original_yuxi_runtime_validated: {str(gate['original_yuxi_runtime_path']['original_yuxi_runtime_validated']).lower()}",
        f"runtime_adoption_allowed: {str(gate['runtime_adoption_path']['runtime_adoption_allowed']).lower()}",
        f"c_lite_allowed: {str(gate['c_lite_path']['c_lite_allowed']).lower()}",
        "```",
        "",
        "## Allowed Branches",
        "",
        "```text",
        "1. User-approved commit: ready, but waiting for explicit approval.",
        "2. Original Yuxi full-stack test: blocked until Docker/Compose or remote runner exists.",
        "3. C-lite design: parked; requires a new explicit user gate and a new validator.",
        "4. Runtime adoption: not allowed from current evidence.",
        "```",
        "",
        "## Prior Gates",
        "",
        "```text",
    ]
    for name, prior in gate["prior_gates"].items():
        lines.append(f"{name}: {prior['status']} / {prior['errors']} errors")
    lines.extend(
        [
            "```",
            "",
            "## Worktree",
            "",
            "```text",
            *(gate["worktree"]["core_status_lines"] or ["<no core doc status>"]),
            *(gate["worktree"]["sandbox_status_lines"] or ["<no sandbox status>"]),
            "```",
            "",
            "## Hard Stops",
            "",
            "```text",
            *gate["hard_stops"],
            "```",
            "",
        ]
    )
    PACKET_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_decision(gate: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_iteration_decision",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: next_action_gate_not_action_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Next-Action Gate Decision",
        "",
        "## Decision",
        "",
        "The next action is gated, not automatic.",
        "",
        "The best available branch is a user-approved commit of the validated",
        "four-file documentation patch plus the Phase B sandbox evidence bundle.",
        "",
        "Original Yuxi runtime testing remains blocked until Docker/Compose or a",
        "remote runner exists. C-lite and runtime adoption remain not allowed.",
        "",
        "## Compared Against Previous Version",
        "",
        "Previous version: commit-readiness scope check.",
        "",
        "This step adds branch selection without granting new authority.",
        "",
        "## Result",
        "",
        "```text",
        f"next_action_gate_status: {gate['next_action_gate_status']}",
        f"recommended_next_action: {gate['recommended_next_action']}",
        f"commit_without_user_approval_allowed: {str(gate['commit_path']['commit_without_user_approval_allowed']).lower()}",
        f"original_yuxi_runtime_validated: {str(gate['original_yuxi_runtime_path']['original_yuxi_runtime_validated']).lower()}",
        f"runtime_adoption_allowed: {str(gate['runtime_adoption_path']['runtime_adoption_allowed']).lower()}",
        f"c_lite_allowed: {str(gate['c_lite_path']['c_lite_allowed']).lower()}",
        "```",
        "",
    ]
    DECISION_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    gate = build_gate()
    GATE_PATH.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")
    write_packet(gate)
    write_decision(gate)
    print(f"next_action_gate_status: {gate['next_action_gate_status']}")
    print(f"recommended_next_action: {gate['recommended_next_action']}")
    print(f"commit_without_user_approval_allowed: {gate['commit_path']['commit_without_user_approval_allowed']}")


if __name__ == "__main__":
    main()
