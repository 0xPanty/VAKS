import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_RUNTIME_FEASIBILITY_REPORT.md"
CHECK_PATH = SANDBOX_DIR / "PHASE_B_RUNTIME_FEASIBILITY_CHECK.md"
JSON_CHECK_PATH = RESULTS_DIR / "phase_b_runtime_feasibility_check.json"

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

REQUIRED_ARTIFACTS = [
    "PHASE_B_RUNTIME_FEASIBILITY_REPORT.md",
    "external/YUXI_RUNTIME_FEASIBILITY_EVIDENCE.md",
    "PHASE_B_MINIMAL_DOC_PATCH_CHECK.md",
    "results/phase_b_minimal_doc_patch_check.json",
    "results/phase_b_adapter_contract_test.json",
]

REQUIRED_REPORT_STRINGS = [
    "Docker and Docker Compose are unavailable",
    "minimal documentation-only patch",
    "Current Yuxi HEAD",
    "a8536a2e8520d1992a31bb6c22f219e60deca131",
    "Lite mode uses make up-lite, which still calls docker compose",
    "Host-only smoke is not enough",
    "Original Yuxi runtime/full-stack: still blocked by local Docker absence",
    "Do not run partial host-only Yuxi smoke as evidence of runtime value",
    "commit the four-file documentation-only patch",
    "install/provide Docker",
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


def validate_report(errors: list[dict]) -> dict:
    text = REPORT_PATH.read_text(encoding="utf-8")
    lower = text.lower()
    for needle in REQUIRED_REPORT_STRINGS:
        if needle.lower() not in lower:
            add_error(errors, "report_missing_required_string", needle)
    return {"bytes": REPORT_PATH.stat().st_size}


def validate_environment(errors: list[dict]) -> dict:
    docker_path = shutil.which("docker")
    if docker_path:
        add_error(errors, "docker_available_recheck_needed", docker_path)
    return {"docker_path": docker_path}


def validate_prior_gates(errors: list[dict]) -> dict:
    minimal = read_json(RESULTS_DIR / "phase_b_minimal_doc_patch_check.json")
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    if minimal.get("minimal_doc_patch_status") != "pass" or int(minimal.get("error_count", -1)) != 0:
        add_error(errors, "minimal_doc_patch_not_pass", json.dumps(minimal.get("errors", []), ensure_ascii=False))
    if contract.get("contract_status") != "pass" or int(contract.get("error_count", -1)) != 0:
        add_error(errors, "contract_not_pass", json.dumps(contract.get("errors", []), ensure_ascii=False))
    return {
        "minimal_doc_patch": {"status": minimal.get("minimal_doc_patch_status"), "errors": minimal.get("error_count")},
        "contract": {"status": contract.get("contract_status"), "errors": contract.get("error_count")},
    }


def validate_core_doc_scope(errors: list[dict]) -> dict:
    proc = run_git(["status", "--porcelain", "--", *CORE_DOCS])
    if proc.returncode != 0:
        add_error(errors, "git_status_failed", proc.stderr.strip())
        return {"returncode": proc.returncode, "dirty": []}
    dirty = [line for line in proc.stdout.splitlines() if line.strip()]
    dirty_paths = {line[3:].strip() for line in dirty}
    unexpected = sorted(dirty_paths - APPROVED_MINIMAL_PATCH_SET)
    missing = sorted(APPROVED_MINIMAL_PATCH_SET - dirty_paths)
    if unexpected:
        add_error(errors, "unexpected_core_doc_changed", ",".join(unexpected))
    if missing:
        add_error(errors, "approved_doc_patch_missing", ",".join(missing))
    return {"returncode": proc.returncode, "dirty": dirty}


def write_reports(result: dict) -> None:
    JSON_CHECK_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "---",
        "record_kind: sandbox_runtime_feasibility_check",
        f"status: {result['runtime_feasibility_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: diagnostic_not_mainline_decision",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Runtime Feasibility Check",
        "",
        "## Result",
        "",
        "```text",
        f"runtime feasibility status: {result['runtime_feasibility_status']}",
        f"error count: {result['error_count']}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: minimal documentation-only patch",
        "required: preserve minimal patch gates and avoid false runtime claim",
        "```",
        "",
        "## Checks",
        "",
        "```text",
        f"docker path: {result['environment'].get('docker_path')}",
        f"minimal doc patch: {result['prior_gates']['minimal_doc_patch']['status']} / {result['prior_gates']['minimal_doc_patch']['errors']} errors",
        f"contract: {result['prior_gates']['contract']['status']} / {result['prior_gates']['contract']['errors']} errors",
        f"changed core docs: {len(result['core_docs'].get('dirty', []))}",
        f"required artifacts checked: {len(result['artifacts'])}",
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
    CHECK_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    errors: list[dict] = []
    artifacts = validate_artifacts(errors)
    report = validate_report(errors)
    environment = validate_environment(errors)
    prior_gates = validate_prior_gates(errors)
    core_docs = validate_core_doc_scope(errors)
    result = {
        "runtime_feasibility_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "artifacts": artifacts,
        "report": report,
        "environment": environment,
        "prior_gates": prior_gates,
        "core_docs": core_docs,
    }
    write_reports(result)
    print(f"runtime feasibility status: {result['runtime_feasibility_status']}")
    print(f"error count: {result['error_count']}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
