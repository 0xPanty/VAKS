import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

MANIFEST_PATH = RESULTS_DIR / "phase_b_pre_commit_manifest.json"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_PRE_COMMIT_MANIFEST_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_pre_commit_manifest_check.json"

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
    "results/phase_b_pre_commit_manifest.json",
    "PHASE_B_PRE_COMMIT_MANIFEST_PACKET.md",
    "PHASE_B_PRE_COMMIT_MANIFEST_DECISION.md",
    "results/phase_b_next_action_gate_check.json",
    "PHASE_B_NEXT_ACTION_GATE_DECISION.md",
]


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


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


def validate_prior_gates(errors: list[dict], manifest: dict) -> dict:
    expected = {
        "next_action_gate": ("phase_b_next_action_gate_check.json", "next_action_gate_check_status"),
        "commit_readiness": ("phase_b_commit_readiness_check.json", "commit_readiness_check_status"),
        "keep_stop": ("phase_b_keep_stop_synthesis_check.json", "keep_stop_synthesis_status"),
    }
    observed = {}
    prior = manifest.get("prior_gates") or {}
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


def validate_decision(errors: list[dict], manifest: dict) -> None:
    if manifest.get("artifact_kind") != "vaks_phase_b_pre_commit_manifest":
        add_error(errors, "bad_artifact_kind", str(manifest.get("artifact_kind")))
    if manifest.get("compared_against_previous_version") != "phase_b_next_action_gate":
        add_error(errors, "bad_previous_version", str(manifest.get("compared_against_previous_version")))
    if manifest.get("pre_commit_manifest_status") != "ready_pending_user_approval":
        add_error(errors, "bad_manifest_status", str(manifest.get("pre_commit_manifest_status")))
    for key in ["commit_without_user_approval_allowed", "commit_performed", "stage_performed"]:
        if manifest.get(key) is not False:
            add_error(errors, f"{key}_leak", str(manifest.get(key)))
    scope = manifest.get("recommended_commit_scope") or {}
    if scope.get("mainline_docs") != APPROVED_DOC_SCOPE:
        add_error(errors, "bad_doc_scope", str(scope.get("mainline_docs")))
    if scope.get("sandbox_evidence_bundle") != SANDBOX_REL:
        add_error(errors, "bad_sandbox_scope", str(scope.get("sandbox_evidence_bundle")))
    if set(manifest.get("excluded_from_scope") or []) != set(DEFERRED_FILES):
        add_error(errors, "bad_excluded_scope", str(manifest.get("excluded_from_scope")))
    branch = manifest.get("branch_state") or {}
    for key in ["runtime_adoption_allowed", "c_lite_allowed", "original_yuxi_runtime_validated"]:
        if branch.get(key) is not False:
            add_error(errors, f"{key}_leak", str(branch.get(key)))
    hard_stops = set(manifest.get("hard_stops") or [])
    for required in [
        "manifest_is_not_commit_approval",
        "do_not_stage_or_commit_without_user_approval",
        "do_not_claim_runtime_or_c_lite_readiness",
        "do_not_treat_sandbox_manifest_as_reviewed_truth",
    ]:
        if required not in hard_stops:
            add_error(errors, "missing_hard_stop", required)


def validate_worktree(errors: list[dict]) -> dict:
    proc = run_git(["status", "--porcelain", "--", *APPROVED_DOC_SCOPE, *DEFERRED_FILES, SANDBOX_REL])
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    core_paths = {line[3:].strip() for line in lines if not line[3:].replace("\\", "/").startswith(SANDBOX_REL)}
    unexpected = sorted(core_paths - set(APPROVED_DOC_SCOPE))
    missing = sorted(set(APPROVED_DOC_SCOPE) - core_paths)
    if unexpected:
        add_error(errors, "unexpected_core_doc_changed", ",".join(unexpected))
    if missing:
        add_error(errors, "approved_doc_not_dirty", ",".join(missing))
    if core_paths & set(DEFERRED_FILES):
        add_error(errors, "deferred_file_dirty", ",".join(sorted(core_paths & set(DEFERRED_FILES))))
    staged = run_git(["diff", "--cached", "--name-only", "--", *APPROVED_DOC_SCOPE, SANDBOX_REL]).stdout.splitlines()
    staged = [line for line in staged if line.strip()]
    if staged:
        add_error(errors, "unexpected_staged_paths", ",".join(staged))
    diff_check = run_git(["diff", "--check", "--", *APPROVED_DOC_SCOPE])
    if diff_check.returncode != 0:
        add_error(errors, "diff_check_failed", (diff_check.stdout + diff_check.stderr).strip())
    return {
        "status_lines": lines,
        "staged_paths": staged,
        "diff_check_returncode": diff_check.returncode,
        "diff_check_stdout": diff_check.stdout,
        "diff_check_stderr": diff_check.stderr,
    }


def validate_file_records(errors: list[dict], manifest: dict) -> dict:
    records = manifest.get("file_records") or []
    if not records:
        add_error(errors, "empty_file_records", "0")
    seen = set()
    total_bytes = 0
    doc_hits = set()
    sandbox_hits = 0
    for record in records:
        rel = record.get("path")
        if not rel:
            add_error(errors, "record_missing_path", str(record))
            continue
        if rel in seen:
            add_error(errors, "duplicate_record", rel)
        seen.add(rel)
        if "__pycache__" in rel:
            add_error(errors, "pycache_recorded", rel)
        if rel in set(manifest.get("circular_audit_artifacts_excluded_from_hash_manifest") or []):
            add_error(errors, "circular_artifact_recorded", rel)
        path = ROOT / rel
        if not path.exists():
            add_error(errors, "record_path_missing", rel)
            continue
        actual_bytes = path.stat().st_size
        actual_hash = sha256(path)
        total_bytes += actual_bytes
        if int(record.get("bytes") if record.get("bytes") is not None else -1) != actual_bytes:
            add_error(errors, "record_bytes_mismatch", f"{rel}: {record.get('bytes')} != {actual_bytes}")
        if record.get("sha256") != actual_hash:
            add_error(errors, "record_hash_mismatch", rel)
        if rel in APPROVED_DOC_SCOPE:
            doc_hits.add(rel)
        if rel.startswith(SANDBOX_REL):
            sandbox_hits += 1
    if doc_hits != set(APPROVED_DOC_SCOPE):
        add_error(errors, "doc_records_missing", ",".join(sorted(set(APPROVED_DOC_SCOPE) - doc_hits)))
    if sandbox_hits <= 0:
        add_error(errors, "sandbox_records_missing", "0")
    if int(manifest.get("file_count") or -1) != len(records):
        add_error(errors, "file_count_mismatch", f"{manifest.get('file_count')} != {len(records)}")
    if int(manifest.get("total_bytes") or -1) != total_bytes:
        add_error(errors, "total_bytes_mismatch", f"{manifest.get('total_bytes')} != {total_bytes}")
    return {"record_count": len(records), "total_bytes": total_bytes, "sandbox_record_count": sandbox_hits}


def validate_text(errors: list[dict]) -> dict:
    packet = (SANDBOX_DIR / "PHASE_B_PRE_COMMIT_MANIFEST_PACKET.md").read_text(encoding="utf-8")
    decision = (SANDBOX_DIR / "PHASE_B_PRE_COMMIT_MANIFEST_DECISION.md").read_text(encoding="utf-8")
    for snippet in [
        "pre_commit_manifest_status: ready_pending_user_approval",
        "commit_without_user_approval_allowed: false",
        "stage_performed: false",
        "commit_performed: false",
        "Phase B next-action gate",
    ]:
        if snippet not in packet:
            add_error(errors, "packet_snippet_missing", snippet)
    for snippet in [
        "This is still not approval to stage or commit.",
        "runtime_adoption_allowed: false",
        "c_lite_allowed: false",
    ]:
        if snippet not in decision:
            add_error(errors, "decision_snippet_missing", snippet)
    return {"packet_bytes": len(packet.encode("utf-8")), "decision_bytes": len(decision.encode("utf-8"))}


def write_markdown(result: dict) -> None:
    manifest = result["manifest"]
    lines = [
        "---",
        "record_kind: sandbox_pre_commit_manifest_check",
        f"status: {result['pre_commit_manifest_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: pre_commit_manifest_not_commit_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Pre-Commit Manifest Check",
        "",
        "## Result",
        "",
        "```text",
        f"pre commit manifest check status: {result['pre_commit_manifest_check_status']}",
        f"error count: {result['error_count']}",
        f"pre_commit_manifest_status: {manifest.get('pre_commit_manifest_status')}",
        f"file_count: {manifest.get('file_count')}",
        f"total_bytes: {manifest.get('total_bytes')}",
        f"commit_without_user_approval_allowed: {str(manifest.get('commit_without_user_approval_allowed')).lower()}",
        f"stage_performed: {str(manifest.get('stage_performed')).lower()}",
        f"commit_performed: {str(manifest.get('commit_performed')).lower()}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: Phase B next-action gate",
        "required: add file hashes without staging, committing, or granting new authority",
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
    manifest = read_json(MANIFEST_PATH)
    artifacts = validate_artifacts(errors)
    validate_decision(errors, manifest)
    prior_gates = validate_prior_gates(errors, manifest)
    worktree = validate_worktree(errors)
    file_records = validate_file_records(errors, manifest)
    text = validate_text(errors)
    result = {
        "pre_commit_manifest_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "manifest": manifest,
        "artifacts": artifacts,
        "prior_gates": prior_gates,
        "worktree": worktree,
        "file_records": file_records,
        "text": text,
    }
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(result)
    return result


def main() -> int:
    result = validate_all()
    print(f"pre commit manifest check status: {result['pre_commit_manifest_check_status']}")
    print(f"error count: {result['error_count']}")
    print(f"file_count: {result['manifest'].get('file_count')}")
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
