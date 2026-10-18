import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
PROMPT_PATH = SANDBOX_DIR / "PHASE_B_PRO_REVIEW_PROMPT.md"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_PRO_REVIEW_PROMPT_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_pro_review_prompt_check.json"

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

REQUIRED_STRINGS = [
    "不要替我合并",
    "不要改文件",
    "不要把 sandbox 结果当成主线结论",
    "Phase B 是否值得做一个最小 documentation-only 主线说明补丁",
    "VAKS Markdown/YAML remains source of truth",
    "Yuxi-like runtime is read-only derived adapter only",
    "Retrieval score is not evidence support",
    "Vector similarity is not truth confidence",
    "Graph edge is not reviewed relation",
    "Chunk manifest is not reviewed knowledge",
    "Retrieval receipt is not action basis",
    "No Skills",
    "No MCP writes",
    "No subagents as production evidence",
    "No formal writeback",
    "No production readiness claim",
    "PHASE_B_MAINLINE_READINESS_PACKET.md",
    "PHASE_B_INTEGRATION_READINESS_PACKAGE.md",
    "PHASE_B_CONTRACT_TEST_DECISION.md",
    "mainline-readiness validator",
    "core docs",
    "dirty lines: 0",
    "SOURCE_INTAKE.md",
    "IMPLEMENTATION_BLUEPRINT.md",
    "DEV_CONTEXT.md",
    "MEMORY_TIER.md",
    "APPROVE_MINIMAL_DOC_PATCH / REVISE_BEFORE_PATCH / REJECT_FOR_NOW",
    "Hidden risk",
    "truth / reviewed relation / action basis",
    "请不要因为指标好就建议进入主线",
]

REQUIRED_ARTIFACTS = [
    "PHASE_B_PRO_REVIEW_PROMPT.md",
    "PHASE_B_PRO_REVIEW_PROMPT_DECISION.md",
    "PHASE_B_MAINLINE_READINESS_PACKET.md",
    "PHASE_B_MAINLINE_READINESS_DECISION.md",
    "PHASE_B_MAINLINE_READINESS_CHECK.md",
    "results/phase_b_mainline_readiness_check.json",
    "results/phase_b_integration_readiness_check.json",
    "results/phase_b_adapter_contract_test.json",
]


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


def validate_prompt(errors: list[dict]) -> dict:
    text = PROMPT_PATH.read_text(encoding="utf-8")
    lower = text.lower()
    for needle in REQUIRED_STRINGS:
        if needle.lower() not in lower:
            add_error(errors, "prompt_missing_required_string", needle)
    return {"bytes": PROMPT_PATH.stat().st_size}


def validate_prior_gates(errors: list[dict]) -> dict:
    mainline = read_json(RESULTS_DIR / "phase_b_mainline_readiness_check.json")
    readiness = read_json(RESULTS_DIR / "phase_b_integration_readiness_check.json")
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    if mainline.get("mainline_readiness_status") != "pass" or int(mainline.get("error_count", -1)) != 0:
        add_error(errors, "mainline_readiness_not_pass", json.dumps(mainline.get("errors", []), ensure_ascii=False))
    if readiness.get("readiness_status") != "pass" or int(readiness.get("error_count", -1)) != 0:
        add_error(errors, "integration_readiness_not_pass", json.dumps(readiness.get("errors", []), ensure_ascii=False))
    if contract.get("contract_status") != "pass" or int(contract.get("error_count", -1)) != 0:
        add_error(errors, "contract_not_pass", json.dumps(contract.get("errors", []), ensure_ascii=False))
    return {
        "mainline_readiness": {
            "status": mainline.get("mainline_readiness_status"),
            "errors": mainline.get("error_count"),
        },
        "integration_readiness": {
            "status": readiness.get("readiness_status"),
            "errors": readiness.get("error_count"),
        },
        "contract": {
            "status": contract.get("contract_status"),
            "errors": contract.get("error_count"),
        },
    }


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
        "record_kind: sandbox_external_review_prompt_check",
        f"status: {result['prompt_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: diagnostic_not_mainline_decision",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Pro Review Prompt Check",
        "",
        "## Result",
        "",
        "```text",
        f"prompt status: {result['prompt_status']}",
        f"error count: {result['error_count']}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: mainline-readiness packet",
        "required: keep all prior gates pass, keep core docs clean, and produce a self-contained Pro prompt",
        "```",
        "",
        "## Checks",
        "",
        "```text",
        f"mainline readiness: {result['prior_gates']['mainline_readiness']['status']} / {result['prior_gates']['mainline_readiness']['errors']} errors",
        f"integration readiness: {result['prior_gates']['integration_readiness']['status']} / {result['prior_gates']['integration_readiness']['errors']} errors",
        f"contract: {result['prior_gates']['contract']['status']} / {result['prior_gates']['contract']['errors']} errors",
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
    prompt = validate_prompt(errors)
    prior_gates = validate_prior_gates(errors)
    core_docs = validate_core_docs_clean(errors)
    result = {
        "prompt_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "artifacts": artifacts,
        "prompt": prompt,
        "prior_gates": prior_gates,
        "core_docs": core_docs,
    }
    write_reports(result)
    print(f"prompt status: {result['prompt_status']}")
    print(f"error count: {result['error_count']}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
