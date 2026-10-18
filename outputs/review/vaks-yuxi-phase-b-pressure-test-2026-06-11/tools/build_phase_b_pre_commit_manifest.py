import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

MANIFEST_PATH = RESULTS_DIR / "phase_b_pre_commit_manifest.json"
PACKET_PATH = SANDBOX_DIR / "PHASE_B_PRE_COMMIT_MANIFEST_PACKET.md"
DECISION_PATH = SANDBOX_DIR / "PHASE_B_PRE_COMMIT_MANIFEST_DECISION.md"

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

CIRCULAR_AUDIT_ARTIFACTS = {
    "outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/results/phase_b_pre_commit_manifest.json",
    "outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/results/phase_b_pre_commit_manifest_check.json",
    "outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/PHASE_B_PRE_COMMIT_MANIFEST_PACKET.md",
    "outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/PHASE_B_PRE_COMMIT_MANIFEST_DECISION.md",
    "outputs/review/vaks-yuxi-phase-b-pressure-test-2026-06-11/PHASE_B_PRE_COMMIT_MANIFEST_CHECK.md",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)


def to_rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def status_map() -> dict[str, str]:
    proc = run_git(["status", "--porcelain", "-uall", "--", *APPROVED_DOC_SCOPE, SANDBOX_REL])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip())
    mapping: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        status = line[:2]
        rel = line[3:].replace("\\", "/")
        mapping[rel] = status
    return mapping


def iter_scope_files() -> list[Path]:
    files = [ROOT / rel for rel in APPROVED_DOC_SCOPE]
    for path in SANDBOX_DIR.rglob("*"):
        if path.is_file():
            rel = to_rel(path)
            if "__pycache__" in rel:
                continue
            if rel in CIRCULAR_AUDIT_ARTIFACTS:
                continue
            files.append(path)
    return sorted(files, key=lambda path: to_rel(path))


def build_manifest() -> dict:
    built_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    next_action = read_json(RESULTS_DIR / "phase_b_next_action_gate_check.json")
    next_gate = read_json(RESULTS_DIR / "phase_b_next_action_gate.json")
    commit_readiness = read_json(RESULTS_DIR / "phase_b_commit_readiness_check.json")
    keep_stop = read_json(RESULTS_DIR / "phase_b_keep_stop_synthesis_check.json")
    statuses = status_map()
    file_records = []
    for path in iter_scope_files():
        rel = to_rel(path)
        file_records.append(
            {
                "path": rel,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "git_status": statuses.get(rel, "tracked_or_parent_status"),
            }
        )
    staged = run_git(["diff", "--cached", "--name-only", "--", *APPROVED_DOC_SCOPE, SANDBOX_REL]).stdout.splitlines()
    return {
        "artifact_kind": "vaks_phase_b_pre_commit_manifest",
        "built_at": built_at,
        "compared_against_previous_version": "phase_b_next_action_gate",
        "pre_commit_manifest_status": "ready_pending_user_approval",
        "commit_without_user_approval_allowed": False,
        "commit_performed": False,
        "stage_performed": False,
        "recommended_commit_scope": {
            "mainline_docs": APPROVED_DOC_SCOPE,
            "sandbox_evidence_bundle": SANDBOX_REL,
        },
        "excluded_from_scope": DEFERRED_FILES,
        "circular_audit_artifacts_excluded_from_hash_manifest": sorted(CIRCULAR_AUDIT_ARTIFACTS),
        "file_count": len(file_records),
        "total_bytes": sum(record["bytes"] for record in file_records),
        "file_records": file_records,
        "prior_gates": {
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
        "branch_state": {
            "recommended_next_action": next_gate.get("recommended_next_action"),
            "runtime_adoption_allowed": (next_gate.get("runtime_adoption_path") or {}).get("runtime_adoption_allowed"),
            "c_lite_allowed": (next_gate.get("c_lite_path") or {}).get("c_lite_allowed"),
            "original_yuxi_runtime_validated": (next_gate.get("original_yuxi_runtime_path") or {}).get(
                "original_yuxi_runtime_validated"
            ),
        },
        "staged_paths": [line for line in staged if line.strip()],
        "hard_stops": [
            "manifest_is_not_commit_approval",
            "do_not_stage_or_commit_without_user_approval",
            "do_not_add_deferred_files_to_scope",
            "do_not_claim_runtime_or_c_lite_readiness",
            "do_not_treat_sandbox_manifest_as_reviewed_truth",
        ],
    }


def write_packet(manifest: dict) -> None:
    first_records = manifest["file_records"][:12]
    lines = [
        "---",
        "record_kind: sandbox_pre_commit_manifest_packet",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: pre_commit_manifest_not_commit_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Pre-Commit Manifest Packet",
        "",
        "## Decision",
        "",
        "```text",
        f"pre_commit_manifest_status: {manifest['pre_commit_manifest_status']}",
        f"commit_without_user_approval_allowed: {str(manifest['commit_without_user_approval_allowed']).lower()}",
        f"stage_performed: {str(manifest['stage_performed']).lower()}",
        f"commit_performed: {str(manifest['commit_performed']).lower()}",
        f"file_count: {manifest['file_count']}",
        f"total_bytes: {manifest['total_bytes']}",
        "```",
        "",
        "## Compared Against Previous Version",
        "",
        "Previous version:",
        "",
        "```text",
        "Phase B next-action gate",
        "```",
        "",
        "This step adds:",
        "",
        "```text",
        "file-level manifest",
        "sha256 fingerprints",
        "pre-commit scope evidence",
        "```",
        "",
        "It preserves:",
        "",
        "```text",
        f"recommended_next_action: {manifest['branch_state']['recommended_next_action']}",
        f"runtime_adoption_allowed: {str(manifest['branch_state']['runtime_adoption_allowed']).lower()}",
        f"c_lite_allowed: {str(manifest['branch_state']['c_lite_allowed']).lower()}",
        f"original_yuxi_runtime_validated: {str(manifest['branch_state']['original_yuxi_runtime_validated']).lower()}",
        "```",
        "",
        "## Recommended Scope",
        "",
        "```text",
        *manifest["recommended_commit_scope"]["mainline_docs"],
        manifest["recommended_commit_scope"]["sandbox_evidence_bundle"],
        "```",
        "",
        "## Manifest Sample",
        "",
        "```text",
    ]
    for record in first_records:
        lines.append(f"{record['git_status']} {record['path']} sha256={record['sha256'][:16]}... bytes={record['bytes']}")
    if manifest["file_count"] > len(first_records):
        lines.append(f"... {manifest['file_count'] - len(first_records)} more files")
    lines.extend(
        [
            "```",
            "",
            "## Hard Stops",
            "",
            "```text",
            *manifest["hard_stops"],
            "```",
            "",
        ]
    )
    PACKET_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_decision(manifest: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_iteration_decision",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: pre_commit_manifest_not_commit_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Pre-Commit Manifest Decision",
        "",
        "## Decision",
        "",
        "The proposed Phase B commit scope now has a file-level manifest and hashes.",
        "",
        "This is still not approval to stage or commit.",
        "",
        "## Compared Against Previous Version",
        "",
        "Previous version: next-action gate.",
        "",
        "This step adds auditability but grants no new authority.",
        "",
        "## Result",
        "",
        "```text",
        f"pre_commit_manifest_status: {manifest['pre_commit_manifest_status']}",
        f"commit_without_user_approval_allowed: {str(manifest['commit_without_user_approval_allowed']).lower()}",
        f"stage_performed: {str(manifest['stage_performed']).lower()}",
        f"commit_performed: {str(manifest['commit_performed']).lower()}",
        f"file_count: {manifest['file_count']}",
        f"total_bytes: {manifest['total_bytes']}",
        f"runtime_adoption_allowed: {str(manifest['branch_state']['runtime_adoption_allowed']).lower()}",
        f"c_lite_allowed: {str(manifest['branch_state']['c_lite_allowed']).lower()}",
        "```",
        "",
    ]
    DECISION_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    manifest = build_manifest()
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    write_packet(manifest)
    write_decision(manifest)
    print(f"pre_commit_manifest_status: {manifest['pre_commit_manifest_status']}")
    print(f"file_count: {manifest['file_count']}")
    print(f"commit_without_user_approval_allowed: {manifest['commit_without_user_approval_allowed']}")


if __name__ == "__main__":
    main()
