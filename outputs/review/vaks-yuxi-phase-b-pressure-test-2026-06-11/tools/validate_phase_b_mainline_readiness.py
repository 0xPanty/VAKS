import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
PACKET_PATH = SANDBOX_DIR / "PHASE_B_MAINLINE_READINESS_PACKET.md"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_MAINLINE_READINESS_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_mainline_readiness_check.json"

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

APPROVED_MINIMAL_PATCH_SET = {
    "SOURCE_INTAKE.md",
    "IMPLEMENTATION_BLUEPRINT.md",
    "DEV_CONTEXT.md",
    "MEMORY_TIER.md",
}

REQUIRED_PACKET_STRINGS = [
    "not approved for mainline edits yet",
    "Compared Against Previous Version",
    "integration readiness package",
    "Candidate Mainline Touch Set",
    "SOURCE_INTAKE.md",
    "IMPLEMENTATION_BLUEPRINT.md",
    "DEV_CONTEXT.md",
    "MEMORY_TIER.md",
    "Deferred unless Pro says necessary",
    "Candidate Snippet Summaries",
    "Phase B Read-Only Retrieval Adapter",
    "authority buckets must be applied before",
    "They are not action basis by themselves",
    "Retrieval activation is not truth",
    "Evidence Map",
    "Remaining Blockers",
    "original Yuxi full-stack was not run locally",
    "Pro Review Questions",
    "Mainline Entry Gate",
    "contract validator: pass / 0 errors",
    "readiness validator: pass / 0 errors",
    "mainline-readiness validator: pass / 0 errors",
    "no Skills, MCP writes, subagents, or formal writeback are approved",
]

REQUIRED_ARTIFACTS = [
    "PHASE_B_MAINLINE_READINESS_PACKET.md",
    "PHASE_B_MAINLINE_READINESS_DECISION.md",
    "PHASE_B_INTEGRATION_READINESS_CHECK.md",
    "PHASE_B_INTEGRATION_READINESS_DECISION.md",
    "PHASE_B_CONTRACT_TEST_DECISION.md",
    "results/phase_b_integration_readiness_check.json",
    "results/phase_b_adapter_contract_test.json",
]

METRIC_FLOORS = {
    ("main", "primary"): {"hit_at_5": "30/30", "hit_at_10": "30/30", "mrr": 1.0},
    ("main", "full"): {"hit_at_5": "30/30", "hit_at_10": "30/30", "mrr": 1.0},
    ("holdout", "primary"): {"hit_at_5": "12/15", "hit_at_10": "13/15", "mrr": 0.7811},
    ("holdout", "full"): {"hit_at_5": "13/15", "hit_at_10": "13/15", "mrr": 0.7591},
}


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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


def validate_packet(errors: list[dict]) -> dict:
    text = PACKET_PATH.read_text(encoding="utf-8")
    lower = text.lower()
    for needle in REQUIRED_PACKET_STRINGS:
        if needle.lower() not in lower:
            add_error(errors, "packet_missing_required_string", needle)
    return {"bytes": PACKET_PATH.stat().st_size}


def validate_readiness(errors: list[dict]) -> dict:
    readiness = read_json(RESULTS_DIR / "phase_b_integration_readiness_check.json")
    if readiness.get("readiness_status") != "pass":
        add_error(errors, "readiness_not_pass", str(readiness.get("readiness_status")))
    if int(readiness.get("error_count", -1)) != 0:
        add_error(errors, "readiness_errors_present", str(readiness.get("error_count")))

    seen = {}
    for row in readiness.get("metrics", []):
        key = (row.get("set"), row.get("corpus"))
        seen[key] = row
        expected = METRIC_FLOORS.get(key)
        if not expected:
            continue
        for metric in ["hit_at_5", "hit_at_10"]:
            if row.get(metric) != expected[metric]:
                add_error(errors, "metric_floor_mismatch", f"{key}:{metric} {row.get(metric)} != {expected[metric]}")
        if float(row.get("mrr", "0")) + 0.00005 < expected["mrr"]:
            add_error(errors, "mrr_below_floor", f"{key}: {row.get('mrr')} < {expected['mrr']}")
        for metric in ["action_leakage_rate", "forbidden_top1_rate", "cross_bucket_violation_rate"]:
            if float(row.get(metric, "1")) != 0.0:
                add_error(errors, "governance_floor_mismatch", f"{key}:{metric}={row.get(metric)}")
    for key in METRIC_FLOORS:
        if key not in seen:
            add_error(errors, "missing_metric_floor_row", str(key))
    return readiness


def validate_contract(errors: list[dict]) -> dict:
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    if contract.get("contract_status") != "pass":
        add_error(errors, "contract_not_pass", str(contract.get("contract_status")))
    if int(contract.get("error_count", -1)) != 0:
        add_error(errors, "contract_errors_present", str(contract.get("error_count")))
    return contract


def validate_core_docs_clean(errors: list[dict]) -> dict:
    proc = subprocess.run(
        ["git", "status", "--porcelain", "--", *CORE_DOCS],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        add_error(errors, "git_status_failed", proc.stderr.strip())
    dirty = [line for line in proc.stdout.splitlines() if line.strip()]
    dirty_paths = {line[3:].strip() for line in dirty}
    approved_patch_present = (SANDBOX_DIR / "PHASE_B_MINIMAL_DOC_PATCH_DECISION.md").exists()
    approved_patch_dirty = bool(dirty_paths) and dirty_paths <= APPROVED_MINIMAL_PATCH_SET and approved_patch_present
    if dirty and not approved_patch_dirty:
        add_error(errors, "core_docs_modified", "\n".join(dirty))
    return {"returncode": proc.returncode, "dirty": dirty, "approved_patch_dirty": approved_patch_dirty}


def write_reports(result: dict) -> None:
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "---",
        "record_kind: sandbox_mainline_readiness_check",
        f"status: {result['mainline_readiness_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: diagnostic_not_mainline_decision",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Mainline-Readiness Check",
        "",
        "## Result",
        "",
        "```text",
        f"mainline readiness status: {result['mainline_readiness_status']}",
        f"error count: {result['error_count']}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: integration readiness package",
        "required: keep readiness pass, contract pass, metric floors, and clean core docs",
        "```",
        "",
        "## Checks",
        "",
        "```text",
        f"readiness: {result['readiness'].get('readiness_status')} / {result['readiness'].get('error_count')} errors",
        f"contract: {result['contract'].get('contract_status')} / {result['contract'].get('error_count')} errors",
        f"core docs dirty lines: {len(result['core_docs'].get('dirty', []))}",
        f"approved patch dirty: {result['core_docs'].get('approved_patch_dirty')}",
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
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    errors: list[dict] = []
    artifacts = validate_artifacts(errors)
    packet = validate_packet(errors)
    readiness = validate_readiness(errors)
    contract = validate_contract(errors)
    core_docs = validate_core_docs_clean(errors)
    result = {
        "mainline_readiness_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "artifacts": artifacts,
        "packet": packet,
        "readiness": {"readiness_status": readiness.get("readiness_status"), "error_count": readiness.get("error_count")},
        "contract": {"contract_status": contract.get("contract_status"), "error_count": contract.get("error_count")},
        "core_docs": core_docs,
    }
    write_reports(result)
    print(f"mainline readiness status: {result['mainline_readiness_status']}")
    print(f"error count: {result['error_count']}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
