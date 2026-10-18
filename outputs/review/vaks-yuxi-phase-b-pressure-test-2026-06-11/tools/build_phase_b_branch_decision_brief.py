import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

BRIEF_PATH = SANDBOX_DIR / "PHASE_B_BRANCH_DECISION_BRIEF.md"
DECISION_PATH = SANDBOX_DIR / "PHASE_B_BRANCH_DECISION_BRIEF_DECISION.md"
JSON_PATH = RESULTS_DIR / "phase_b_branch_decision_brief.json"

APPROVED_DOC_SCOPE = [
    "SOURCE_INTAKE.md",
    "IMPLEMENTATION_BLUEPRINT.md",
    "DEV_CONTEXT.md",
    "MEMORY_TIER.md",
]

SANDBOX_REL = "outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)


def status_lines() -> list[str]:
    proc = run_git(["status", "--porcelain", "--", *APPROVED_DOC_SCOPE, SANDBOX_REL])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip())
    return [line for line in proc.stdout.splitlines() if line.strip()]


def build_brief() -> dict:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    pre_commit = read_json(RESULTS_DIR / "phase_b_pre_commit_manifest_check.json")
    next_action = read_json(RESULTS_DIR / "phase_b_next_action_gate_check.json")
    commit_readiness = read_json(RESULTS_DIR / "phase_b_commit_readiness_check.json")
    keep_stop = read_json(RESULTS_DIR / "phase_b_keep_stop_synthesis_check.json")
    manifest = read_json(RESULTS_DIR / "phase_b_pre_commit_manifest.json")
    staged = run_git(["diff", "--cached", "--name-only", "--", *APPROVED_DOC_SCOPE, SANDBOX_REL]).stdout.splitlines()
    return {
        "artifact_kind": "vaks_phase_b_branch_decision_brief",
        "built_at": built_at,
        "compared_against_previous_version": "phase_b_pre_commit_manifest",
        "branch_decision_brief_status": "ready_for_user_choice",
        "commit_without_user_approval_allowed": False,
        "stage_performed": False,
        "commit_performed": False,
        "recommended_branch": "user_approved_commit",
        "available_branches": [
            {
                "branch": "user_approved_commit",
                "status": "ready_pending_user_approval",
                "meaning": "Commit the validated four docs plus Phase B sandbox evidence bundle.",
            },
            {
                "branch": "original_yuxi_full_stack_test",
                "status": "blocked_until_docker_or_remote_runner",
                "meaning": "Run original Yuxi only when Docker/Compose or a remote runner exists.",
            },
            {
                "branch": "c_lite_sandbox",
                "status": "not_allowed_without_new_user_gate",
                "meaning": "Requires an explicit new user approval and a fresh validator.",
            },
            {
                "branch": "runtime_adoption",
                "status": "not_allowed",
                "meaning": "Current evidence does not approve runtime/default adoption.",
            },
        ],
        "commit_scope": {
            "mainline_docs": APPROVED_DOC_SCOPE,
            "sandbox_evidence_bundle": SANDBOX_REL,
        },
        "manifest_snapshot": {
            "status": manifest.get("pre_commit_manifest_status"),
            "file_count": manifest.get("file_count"),
            "total_bytes": manifest.get("total_bytes"),
        },
        "prior_gates": {
            "pre_commit_manifest": {
                "status": pre_commit.get("pre_commit_manifest_check_status"),
                "errors": pre_commit.get("error_count"),
            },
            "next_action_gate": {
                "status": next_action.get("next_action_gate_check_status"),
                "errors": next_action.get("error_count"),
            },
            "commit_readiness": {
                "status": commit_readiness.get("commit_readiness_check_status"),
                "errors": commit_readiness.get("error_count"),
            },
            "keep_stop": {
                "status": keep_stop.get("keep_stop_synthesis_status"),
                "errors": keep_stop.get("error_count"),
            },
        },
        "worktree": {
            "status_lines": status_lines(),
            "staged_paths": [line for line in staged if line.strip()],
        },
        "copy_paste_prompt": (
            "继续 VAKS Phase B。先读 "
            "outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/PHASE_B_BRANCH_DECISION_BRIEF.md。"
            " 当前只能在三条路中选：批准提交、提供 Docker/远程 runner 测原版 Yuxi、或明确开新的 C-lite 沙盒 gate。"
            " 不要自动 commit，不要自动 C-lite，不要声称 runtime adoption。"
        ),
    }


def write_brief(brief: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_branch_decision_brief",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: branch_decision_brief_not_action_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Branch Decision Brief",
        "",
        "## Plain Decision",
        "",
        "```text",
        "The Phase B evidence is positive enough to keep as a governed retrieval adapter candidate.",
        "The only ready branch is a user-approved documentation/evidence commit.",
        "Original Yuxi full-stack testing needs Docker/Compose or a remote runner.",
        "C-lite and runtime adoption are not allowed from current evidence.",
        "```",
        "",
        "## Compared Against Previous Version",
        "",
        "Previous version:",
        "",
        "```text",
        "Phase B pre-commit manifest",
        "```",
        "",
        "This step adds:",
        "",
        "```text",
        "human-readable branch choice brief",
        "copy-paste recovery prompt",
        "no new authority",
        "```",
        "",
        "It preserves:",
        "",
        "```text",
        f"commit_without_user_approval_allowed: {str(brief['commit_without_user_approval_allowed']).lower()}",
        f"stage_performed: {str(brief['stage_performed']).lower()}",
        f"commit_performed: {str(brief['commit_performed']).lower()}",
        "runtime_adoption_allowed: false",
        "c_lite_allowed: false",
        "```",
        "",
        "## Branches",
        "",
        "```text",
    ]
    for item in brief["available_branches"]:
        lines.append(f"{item['branch']}: {item['status']} - {item['meaning']}")
    lines.extend(
        [
            "```",
            "",
            "## Commit Scope If Approved",
            "",
            "```text",
            *brief["commit_scope"]["mainline_docs"],
            brief["commit_scope"]["sandbox_evidence_bundle"],
            "```",
            "",
            "## Recovery Prompt",
            "",
            "```text",
            brief["copy_paste_prompt"],
            "```",
            "",
        ]
    )
    BRIEF_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_decision(brief: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_iteration_decision",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: branch_decision_brief_not_action_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Branch Decision Brief Decision",
        "",
        "## Decision",
        "",
        "The branch decision is now summarized for the user or next window.",
        "",
        "This is not approval to stage, commit, start C-lite, or claim runtime adoption.",
        "",
        "## Compared Against Previous Version",
        "",
        "Previous version: pre-commit manifest.",
        "",
        "This step improves handoff clarity and grants no new authority.",
        "",
        "## Result",
        "",
        "```text",
        f"branch_decision_brief_status: {brief['branch_decision_brief_status']}",
        f"recommended_branch: {brief['recommended_branch']}",
        f"commit_without_user_approval_allowed: {str(brief['commit_without_user_approval_allowed']).lower()}",
        f"stage_performed: {str(brief['stage_performed']).lower()}",
        f"commit_performed: {str(brief['commit_performed']).lower()}",
        "runtime_adoption_allowed: false",
        "c_lite_allowed: false",
        "```",
        "",
    ]
    DECISION_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    brief = build_brief()
    JSON_PATH.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")
    write_brief(brief)
    write_decision(brief)
    print(f"branch_decision_brief_status: {brief['branch_decision_brief_status']}")
    print(f"recommended_branch: {brief['recommended_branch']}")
    print(f"commit_without_user_approval_allowed: {brief['commit_without_user_approval_allowed']}")


if __name__ == "__main__":
    main()
