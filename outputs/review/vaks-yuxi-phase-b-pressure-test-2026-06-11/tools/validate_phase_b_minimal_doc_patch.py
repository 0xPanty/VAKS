import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_MINIMAL_DOC_PATCH_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_minimal_doc_patch_check.json"

APPROVED_TOUCH_SET = {
    "SOURCE_INTAKE.md",
    "IMPLEMENTATION_BLUEPRINT.md",
    "DEV_CONTEXT.md",
    "MEMORY_TIER.md",
}

DEFERRED_FILES = {
    "SCHEMA.md",
    "REVIEW_QUEUE.md",
    "templates/architecture-review-window-prompt.md",
}

REQUIRED_SANDBOX_ARTIFACTS = [
    "PHASE_B_EXTERNAL_REVIEW_RESULT.md",
    "PHASE_B_EXTERNAL_REVIEW_DECISION.md",
    "PHASE_B_MINIMAL_DOC_PATCH_DECISION.md",
    "PHASE_B_MINIMAL_DOC_PATCH_CHECK.md",
    "results/phase_b_external_review_result_check.json",
]

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

REQUIRED_SNIPPETS = {
    "SOURCE_INTAKE.md": [
        "documentation-only Phase B direction",
        "does not approve runtime, default, or production adoption",
        "apply VAKS authority buckets before ranking or RRF fusion",
        "graph_path",
        "recall metadata only",
        "not reviewed relations",
        "not promote raw, candidate, diagnostic, feedback, or overlay",
        "action basis",
    ],
    "IMPLEMENTATION_BLUEPRINT.md": [
        "Phase B query-layer documentation",
        "read-only derived adapter",
        "filter by VAKS authority bucket before ranking",
        "context-pack candidates with click-back and warnings",
        "before any runtime/default/production adoption beyond this documentation note",
        "Do not attach Skills, MCP writes, subagents, formal writeback, or production",
    ],
    "DEV_CONTEXT.md": [
        "Retrieval receipts may help assemble a context-pack candidate",
        "They are not action basis by themselves",
        "before it can be reviewed for action-facing use",
        "preconditions for review only",
        "not enough to create action basis",
        "truth confidence",
        "reviewed relations",
    ],
    "MEMORY_TIER.md": [
        "Retrieval activation is not truth",
        "may improve routing or create review_due pressure only",
        "must not automatically create a queue item",
        "evidence support",
        "truth confidence",
        "reviewed relation",
        "action readiness",
        "action basis",
    ],
}


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def run_git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def changed_core_docs(errors: list[dict]) -> list[str]:
    proc = run_git(["status", "--porcelain", "--", *CORE_DOCS])
    if proc.returncode != 0:
        add_error(errors, "git_status_failed", proc.stderr.strip())
        return []
    changed = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        changed.append(path)
    return changed


def validate_touch_set(errors: list[dict], changed: list[str]) -> None:
    changed_set = set(changed)
    unexpected = sorted(changed_set - APPROVED_TOUCH_SET)
    missing = sorted(APPROVED_TOUCH_SET - changed_set)
    deferred_touched = sorted(changed_set & DEFERRED_FILES)
    if unexpected:
        add_error(errors, "unexpected_core_doc_changed", ",".join(unexpected))
    if missing:
        add_error(errors, "approved_touch_file_not_changed", ",".join(missing))
    if deferred_touched:
        add_error(errors, "deferred_file_changed", ",".join(deferred_touched))


def validate_snippets(errors: list[dict]) -> dict:
    coverage = {}
    for rel, snippets in REQUIRED_SNIPPETS.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        lower = text.lower()
        missing = [snippet for snippet in snippets if snippet.lower() not in lower]
        coverage[rel] = {"required": len(snippets), "missing": missing}
        if missing:
            add_error(errors, "required_snippet_missing", f"{rel}: {missing}")
    return coverage


def validate_sandbox_artifacts(errors: list[dict]) -> list[dict]:
    artifacts = []
    for rel in REQUIRED_SANDBOX_ARTIFACTS:
        path = SANDBOX_DIR / rel
        exists = path.exists()
        artifacts.append({"path": rel, "exists": exists, "bytes": path.stat().st_size if exists else 0})
        if not exists:
            add_error(errors, "missing_required_sandbox_artifact", rel)
        elif path.stat().st_size == 0:
            add_error(errors, "empty_required_sandbox_artifact", rel)
    return artifacts


def validate_prior_gates(errors: list[dict]) -> dict:
    external = read_json(RESULTS_DIR / "phase_b_external_review_result_check.json")
    prompt = read_json(RESULTS_DIR / "phase_b_pro_review_prompt_check.json")
    mainline = read_json(RESULTS_DIR / "phase_b_mainline_readiness_check.json")
    readiness = read_json(RESULTS_DIR / "phase_b_integration_readiness_check.json")
    contract = read_json(RESULTS_DIR / "phase_b_adapter_contract_test.json")
    checks = [
        ("external_review", external.get("external_review_status"), external.get("error_count")),
        ("prompt", prompt.get("prompt_status"), prompt.get("error_count")),
        ("mainline_readiness", mainline.get("mainline_readiness_status"), mainline.get("error_count")),
        ("integration_readiness", readiness.get("readiness_status"), readiness.get("error_count")),
        ("contract", contract.get("contract_status"), contract.get("error_count")),
    ]
    for name, status, error_count in checks:
        expected_status = "pass" if name != "contract" else "pass"
        if status != expected_status or int(error_count if error_count is not None else -1) != 0:
            add_error(errors, "prior_gate_not_pass", f"{name}: {status} / {error_count}")
    return {name: {"status": status, "errors": error_count} for name, status, error_count in checks}


def write_reports(result: dict) -> None:
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "---",
        "record_kind: sandbox_minimal_doc_patch_check",
        f"status: {result['minimal_doc_patch_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: diagnostic_not_mainline_decision",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Minimal Documentation Patch Check",
        "",
        "## Result",
        "",
        "```text",
        f"minimal doc patch status: {result['minimal_doc_patch_status']}",
        f"error count: {result['error_count']}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: external review result",
        "required: only approved four files changed, deferred files untouched, prior gates pass",
        "```",
        "",
        "## Changed Core Docs",
        "",
        "```text",
        *result["changed_core_docs"],
        "```",
        "",
        "## Prior Gates",
        "",
        "```text",
    ]
    for name, gate in result["prior_gates"].items():
        lines.append(f"{name}: {gate['status']} / {gate['errors']} errors")
    lines.extend(
        [
            "```",
            "",
            "## Errors",
            "",
        ]
    )
    if result["errors"]:
        for error in result["errors"]:
            lines.append(f"- {error['code']}: {error['detail']}")
    else:
        lines.append("- none")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    errors: list[dict] = []
    changed = changed_core_docs(errors)
    validate_touch_set(errors, changed)
    snippet_coverage = validate_snippets(errors)
    sandbox_artifacts = validate_sandbox_artifacts(errors)
    prior_gates = validate_prior_gates(errors)
    result = {
        "minimal_doc_patch_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "changed_core_docs": changed,
        "snippet_coverage": snippet_coverage,
        "sandbox_artifacts": sandbox_artifacts,
        "prior_gates": prior_gates,
    }
    write_reports(result)
    print(f"minimal doc patch status: {result['minimal_doc_patch_status']}")
    print(f"error count: {result['error_count']}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
