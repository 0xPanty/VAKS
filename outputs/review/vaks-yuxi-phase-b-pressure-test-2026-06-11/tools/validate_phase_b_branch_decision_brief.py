import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

JSON_PATH = RESULTS_DIR / "phase_b_branch_decision_brief.json"
CHECK_PATH = RESULTS_DIR / "phase_b_branch_decision_brief_check.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_BRANCH_DECISION_BRIEF_CHECK.md"

APPROVED_DOC_SCOPE = [
    "SOURCE_INTAKE.md",
    "IMPLEMENTATION_BLUEPRINT.md",
    "DEV_CONTEXT.md",
    "MEMORY_TIER.md",
]

SANDBOX_REL = "outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/"

REQUIRED_ARTIFACTS = [
    "results/phase_b_branch_decision_brief.json",
    "PHASE_B_BRANCH_DECISION_BRIEF.md",
    "PHASE_B_BRANCH_DECISION_BRIEF_DECISION.md",
    "results/phase_b_pre_commit_manifest_check.json",
    "PHASE_B_PRE_COMMIT_MANIFEST_DECISION.md",
]


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)


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


def validate_decision(errors: list[dict], brief: dict) -> None:
    if brief.get("artifact_kind") != "vaks_phase_b_branch_decision_brief":
        add_error(errors, "bad_artifact_kind", str(brief.get("artifact_kind")))
    if brief.get("compared_against_previous_version") != "phase_b_pre_commit_manifest":
        add_error(errors, "bad_previous_version", str(brief.get("compared_against_previous_version")))
    if brief.get("branch_decision_brief_status") != "ready_for_user_choice":
        add_error(errors, "bad_brief_status", str(brief.get("branch_decision_brief_status")))
    if brief.get("recommended_branch") != "user_approved_commit":
        add_error(errors, "bad_recommended_branch", str(brief.get("recommended_branch")))
    for key in ["commit_without_user_approval_allowed", "stage_performed", "commit_performed"]:
        if brief.get(key) is not False:
            add_error(errors, f"{key}_leak", str(brief.get(key)))
    branches = {item.get("branch"): item.get("status") for item in brief.get("available_branches") or []}
    expected = {
        "user_approved_commit": "ready_pending_user_approval",
        "original_yuxi_full_stack_test": "blocked_until_docker_or_remote_runner",
        "c_lite_sandbox": "not_allowed_without_new_user_gate",
        "runtime_adoption": "not_allowed",
    }
    for branch, status in expected.items():
        if branches.get(branch) != status:
            add_error(errors, "bad_branch_status", f"{branch}: {branches.get(branch)} != {status}")
    scope = brief.get("commit_scope") or {}
    if scope.get("mainline_docs") != APPROVED_DOC_SCOPE:
        add_error(errors, "bad_commit_scope_docs", str(scope.get("mainline_docs")))
    if scope.get("sandbox_evidence_bundle") != SANDBOX_REL:
        add_error(errors, "bad_commit_scope_sandbox", str(scope.get("sandbox_evidence_bundle")))


def validate_prior_gates(errors: list[dict], brief: dict) -> dict:
    expected = {
        "pre_commit_manifest": ("phase_b_pre_commit_manifest_check.json", "pre_commit_manifest_check_status"),
        "next_action_gate": ("phase_b_next_action_gate_check.json", "next_action_gate_check_status"),
        "commit_readiness": ("phase_b_commit_readiness_check.json", "commit_readiness_check_status"),
        "keep_stop": ("phase_b_keep_stop_synthesis_check.json", "keep_stop_synthesis_status"),
    }
    observed = {}
    prior = brief.get("prior_gates") or {}
    for name, (file_name, status_key) in expected.items():
        payload = read_json(RESULTS_DIR / file_name)
        status = payload.get(status_key)
        error_count = payload.get("error_count")
        observed[name] = {"status": status, "errors": error_count}
        if status != "pass" or int(error_count if error_count is not None else -1) != 0:
            add_error(errors, "prior_gate_not_pass", f"{name}: {status} / {error_count}")
        if (prior.get(name) or {}).get("status") != status or (prior.get(name) or {}).get("errors") != error_count:
            add_error(errors, "prior_gate_mismatch", f"{name}: {prior.get(name)} != {observed[name]}")
    return observed


def validate_worktree(errors: list[dict]) -> dict:
    staged = run_git(["diff", "--cached", "--name-only", "--", *APPROVED_DOC_SCOPE, SANDBOX_REL]).stdout.splitlines()
    staged = [line for line in staged if line.strip()]
    if staged:
        add_error(errors, "unexpected_staged_paths", ",".join(staged))
    return {"staged_paths": staged}


def validate_text(errors: list[dict]) -> dict:
    brief_text = (SANDBOX_DIR / "PHASE_B_BRANCH_DECISION_BRIEF.md").read_text(encoding="utf-8")
    decision_text = (SANDBOX_DIR / "PHASE_B_BRANCH_DECISION_BRIEF_DECISION.md").read_text(encoding="utf-8")
    for snippet in [
        "The only ready branch is a user-approved documentation/evidence commit.",
        "C-lite and runtime adoption are not allowed from current evidence.",
        "commit_without_user_approval_allowed: false",
        "no new authority",
    ]:
        if snippet not in brief_text:
            add_error(errors, "brief_snippet_missing", snippet)
    for snippet in [
        "This is not approval to stage, commit, start C-lite, or claim runtime adoption.",
        "branch_decision_brief_status: ready_for_user_choice",
        "runtime_adoption_allowed: false",
        "c_lite_allowed: false",
    ]:
        if snippet not in decision_text:
            add_error(errors, "decision_snippet_missing", snippet)
    return {"brief_bytes": len(brief_text.encode("utf-8")), "decision_bytes": len(decision_text.encode("utf-8"))}


def write_markdown(result: dict) -> None:
    brief = result["brief"]
    lines = [
        "---",
        "record_kind: sandbox_branch_decision_brief_check",
        f"status: {result['branch_decision_brief_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: branch_decision_brief_not_action_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Branch Decision Brief Check",
        "",
        "## Result",
        "",
        "```text",
        f"branch decision brief check status: {result['branch_decision_brief_check_status']}",
        f"error count: {result['error_count']}",
        f"branch_decision_brief_status: {brief.get('branch_decision_brief_status')}",
        f"recommended_branch: {brief.get('recommended_branch')}",
        f"commit_without_user_approval_allowed: {str(brief.get('commit_without_user_approval_allowed')).lower()}",
        f"stage_performed: {str(brief.get('stage_performed')).lower()}",
        f"commit_performed: {str(brief.get('commit_performed')).lower()}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: Phase B pre-commit manifest",
        "required: human-readable branch brief without granting commit/runtime/C-lite authority",
        "```",
        "",
        "## Errors",
        "",
    ]
    if result["errors"]:
        for error in result["errors"]:
            lines.append(f"- {error['code']}: {error['detail']}")
    else:
        lines.append("- none")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def validate_all() -> dict:
    errors: list[dict] = []
    brief = read_json(JSON_PATH)
    artifacts = validate_artifacts(errors)
    validate_decision(errors, brief)
    prior_gates = validate_prior_gates(errors, brief)
    worktree = validate_worktree(errors)
    text = validate_text(errors)
    result = {
        "branch_decision_brief_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "brief": brief,
        "artifacts": artifacts,
        "prior_gates": prior_gates,
        "worktree": worktree,
        "text": text,
    }
    CHECK_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(result)
    return result


def main() -> int:
    result = validate_all()
    print(f"branch decision brief check status: {result['branch_decision_brief_check_status']}")
    print(f"error count: {result['error_count']}")
    print(f"recommended_branch: {result['brief'].get('recommended_branch')}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
