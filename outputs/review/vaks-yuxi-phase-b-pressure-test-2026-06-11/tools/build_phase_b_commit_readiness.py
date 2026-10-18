import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

READINESS_PATH = RESULTS_DIR / "phase_b_commit_readiness.json"
PACKET_PATH = SANDBOX_DIR / "PHASE_B_COMMIT_READINESS_PACKET.md"
DECISION_PATH = SANDBOX_DIR / "PHASE_B_COMMIT_READINESS_DECISION.md"

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


def git_status_lines(paths: list[str]) -> list[str]:
    proc = run_git(["status", "--porcelain", "--", *paths])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip())
    return [line for line in proc.stdout.splitlines() if line.strip()]


def diff_numstat(paths: list[str]) -> list[dict]:
    proc = run_git(["diff", "--numstat", "--", *paths])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip())
    rows = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        added, deleted, path = line.split("\t", 2)
        rows.append({"path": path, "added": added, "deleted": deleted})
    return rows


def build_readiness() -> dict:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    keep_stop = read_json(RESULTS_DIR / "phase_b_keep_stop_synthesis_check.json")
    keep_stop_synthesis = read_json(RESULTS_DIR / "phase_b_keep_stop_synthesis.json")
    minimal_doc = read_json(RESULTS_DIR / "phase_b_minimal_doc_patch_check.json")
    promotion_gate = read_json(RESULTS_DIR / "phase_b_promotion_gate_check.json")
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    runtime = read_json(RESULTS_DIR / "phase_b_runtime_feasibility_check.json")
    core_status = git_status_lines(APPROVED_DOC_SCOPE + DEFERRED_FILES)
    sandbox_status = git_status_lines([SANDBOX_REL])
    doc_diff = diff_numstat(APPROVED_DOC_SCOPE)
    recommended_scope = {
        "mainline_docs": APPROVED_DOC_SCOPE,
        "sandbox_evidence_bundle": SANDBOX_REL,
    }
    return {
        "artifact_kind": "vaks_phase_b_commit_readiness",
        "built_at": built_at,
        "compared_against_previous_version": "phase_b_keep_stop_synthesis",
        "commit_readiness_status": "ready_pending_user_approval",
        "commit_without_user_approval_allowed": False,
        "recommended_commit_scope": recommended_scope,
        "excluded_from_commit_scope": DEFERRED_FILES,
        "suggested_commit_message": "docs(vaks): record phase b yuxi retrieval adapter guardrails",
        "why_this_is_positive": [
            "keeps the positive Phase B evidence durable",
            "commits only the validated documentation patch and sandbox evidence",
            "does not claim runtime adoption or C-lite readiness",
            "preserves explicit blockers for promotion, writeback, and action basis",
        ],
        "keep_stop_summary": {
            "status": keep_stop.get("keep_stop_synthesis_status"),
            "errors": keep_stop.get("error_count"),
            "decision": keep_stop_synthesis.get("keep_stop_decision"),
            "positive_value_confirmed": keep_stop_synthesis.get("positive_value_confirmed"),
            "no_boundary_leak_confirmed": keep_stop_synthesis.get("no_boundary_leak_confirmed"),
            "runtime_adoption_allowed": keep_stop_synthesis.get("runtime_adoption_allowed"),
            "c_lite_allowed": keep_stop_synthesis.get("c_lite_allowed"),
            "original_yuxi_runtime_validated": keep_stop_synthesis.get("original_yuxi_runtime_validated"),
        },
        "prior_gates": {
            "minimal_doc_patch": {
                "status": minimal_doc.get("minimal_doc_patch_status"),
                "errors": minimal_doc.get("error_count"),
            },
            "promotion_gate": {
                "status": promotion_gate.get("promotion_gate_status"),
                "errors": promotion_gate.get("error_count"),
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
        "current_worktree_evidence": {
            "core_status_lines": core_status,
            "sandbox_status_lines": sandbox_status,
            "doc_diff_numstat": doc_diff,
            "changed_core_docs_observed": minimal_doc.get("changed_core_docs"),
        },
        "hard_stops": [
            "no_commit_without_user_approval",
            "do_not_stage_scema_review_queue_or_templates",
            "do_not_claim_original_yuxi_runtime_validated",
            "do_not_start_c_lite_from_this_commit",
            "do_not_treat_sandbox_outputs_as_reviewed_truth",
        ],
    }


def write_packet(readiness: dict) -> None:
    worktree = readiness["current_worktree_evidence"]
    keep_stop = readiness["keep_stop_summary"]
    lines = [
        "---",
        "record_kind: sandbox_commit_readiness_packet",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: commit_readiness_not_commit_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Commit Readiness Packet",
        "",
        "## Decision",
        "",
        "```text",
        f"commit_readiness_status: {readiness['commit_readiness_status']}",
        f"commit_without_user_approval_allowed: {str(readiness['commit_without_user_approval_allowed']).lower()}",
        f"suggested_commit_message: {readiness['suggested_commit_message']}",
        "```",
        "",
        "## Compared Against Previous Version",
        "",
        "Previous version:",
        "",
        "```text",
        "Phase B keep/stop synthesis",
        "```",
        "",
        "This step adds:",
        "",
        "```text",
        "exact commit scope recommendation",
        "explicit no-approval/no-commit boundary",
        "deferred-file and runtime/C-lite stop list",
        "```",
        "",
        "It preserves:",
        "",
        "```text",
        f"keep_stop_status: {keep_stop['status']} / {keep_stop['errors']} errors",
        f"keep_stop_decision: {keep_stop['decision']}",
        f"positive_value_confirmed: {str(keep_stop['positive_value_confirmed']).lower()}",
        f"no_boundary_leak_confirmed: {str(keep_stop['no_boundary_leak_confirmed']).lower()}",
        f"runtime_adoption_allowed: {str(keep_stop['runtime_adoption_allowed']).lower()}",
        f"c_lite_allowed: {str(keep_stop['c_lite_allowed']).lower()}",
        f"original_yuxi_runtime_validated: {str(keep_stop['original_yuxi_runtime_validated']).lower()}",
        "```",
        "",
        "## Recommended Commit Scope",
        "",
        "```text",
        *readiness["recommended_commit_scope"]["mainline_docs"],
        readiness["recommended_commit_scope"]["sandbox_evidence_bundle"],
        "```",
        "",
        "## Excluded / Deferred",
        "",
        "```text",
        *readiness["excluded_from_commit_scope"],
        "runtime adoption",
        "C-lite",
        "Skills / MCP writes / subagents",
        "formal writeback",
        "Evidence Packet / action basis",
        "```",
        "",
        "## Current Worktree Evidence",
        "",
        "Core status lines:",
        "",
        "```text",
        *(worktree["core_status_lines"] or ["<none>"]),
        "```",
        "",
        "Sandbox status lines:",
        "",
        "```text",
        *(worktree["sandbox_status_lines"] or ["<none>"]),
        "```",
        "",
        "Doc diff numstat:",
        "",
        "```text",
    ]
    if worktree["doc_diff_numstat"]:
        for row in worktree["doc_diff_numstat"]:
            lines.append(f"{row['path']}: +{row['added']} -{row['deleted']}")
    else:
        lines.append("<none>")
    lines.extend(
        [
            "```",
            "",
            "## Hard Stops",
            "",
            "```text",
            *readiness["hard_stops"],
            "```",
            "",
        ]
    )
    PACKET_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_decision(readiness: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_iteration_decision",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: commit_readiness_not_commit_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Commit Readiness Decision",
        "",
        "## Decision",
        "",
        "The Phase B package is ready for a user-approved documentation/evidence commit.",
        "",
        "This is not commit approval, runtime adoption, C-lite approval, or truth promotion.",
        "",
        "## Compared Against Previous Version",
        "",
        "Previous version: keep/stop synthesis.",
        "",
        "This step adds commit-scope discipline and preserves the keep/stop boundary.",
        "",
        "## Result",
        "",
        "```text",
        f"commit_readiness_status: {readiness['commit_readiness_status']}",
        f"commit_without_user_approval_allowed: {str(readiness['commit_without_user_approval_allowed']).lower()}",
        f"keep_stop_status: {readiness['keep_stop_summary']['status']} / {readiness['keep_stop_summary']['errors']} errors",
        f"minimal_doc_patch: {readiness['prior_gates']['minimal_doc_patch']['status']} / {readiness['prior_gates']['minimal_doc_patch']['errors']} errors",
        f"promotion_gate: {readiness['prior_gates']['promotion_gate']['status']} / {readiness['prior_gates']['promotion_gate']['errors']} errors",
        f"adapter_contract: {readiness['prior_gates']['adapter_contract']['status']} / {readiness['prior_gates']['adapter_contract']['errors']} errors",
        "```",
        "",
        "## Recommended Commit Scope",
        "",
        "```text",
        "SOURCE_INTAKE.md",
        "IMPLEMENTATION_BLUEPRINT.md",
        "DEV_CONTEXT.md",
        "MEMORY_TIER.md",
        SANDBOX_REL,
        "```",
        "",
    ]
    DECISION_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    readiness = build_readiness()
    READINESS_PATH.write_text(json.dumps(readiness, ensure_ascii=False, indent=2), encoding="utf-8")
    write_packet(readiness)
    write_decision(readiness)
    print(f"commit_readiness_status: {readiness['commit_readiness_status']}")
    print(f"commit_without_user_approval_allowed: {readiness['commit_without_user_approval_allowed']}")
    print(f"keep_stop_status: {readiness['keep_stop_summary']['status']}")


if __name__ == "__main__":
    main()
