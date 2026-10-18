from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-62-user-decision-operator-runbook-dry-run-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-61-user-decision-freeze-operator-readiness-brief-sandbox"
MANUAL_VERIFY_SOURCE_SLICE_ID = "2026-06-16-p2-60-user-decision-index-freeze-checksum-sandbox"

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"
RUNBOOK_JSON = ARTIFACT / "user_decision_operator_runbook_dry_run.json"

REQUIRED_ROOT = [
    "slice-plan.md",
    "source-map.md",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

REQUIRED_ARTIFACT = [
    "build_user_decision_operator_runbook_dry_run.py",
    "verify_user_decision_operator_runbook_dry_run.py",
    "user_decision_operator_runbook_dry_run_contract.json",
    "user_decision_operator_runbook_dry_run.json",
    "user_decision_operator_runbook_dry_run.md",
    "user_decision_operator_runbook_dry_run.html",
]

HARD_NO_REQUIRED = {
    "do_not_execute_user_decision_option",
    "do_not_merge_mainline",
    "do_not_promote",
    "do_not_sync_obsidian",
    "do_not_commit",
    "do_not_push",
    "do_not_install_dependencies",
    "do_not_start_background_service",
    "do_not_install_hooks",
    "do_not_use_mcp_write_tool",
    "do_not_create_reviewed_knowledge",
    "do_not_create_evidence_support",
    "do_not_create_action_basis",
    "do_not_collect_user_approval_by_inference",
}

STOP_REQUEST_KINDS = {
    "execute_user_decision_option",
    "merge_mainline",
    "promote",
    "sync_obsidian",
    "commit",
    "push",
    "create_reviewed_knowledge",
    "create_evidence_support",
    "create_action_basis",
    "infer_user_approval",
}

DANGEROUS_PHRASES = [
    "execution approved",
    "mainline approved",
    "promotion approved",
    "sync approved",
    "reviewed knowledge created",
    "evidence support created",
    "action basis created",
    "user approval collected",
    "可以合并",
    "已合并",
    "执行授权",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def frontmatter_status(path: Path) -> str:
    for line in read_text(path).splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def import_builder():
    path = ARTIFACT / "build_user_decision_operator_runbook_dry_run.py"
    spec = importlib.util.spec_from_file_location("p2_62_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-62 builder")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_files(failures: list[str]) -> tuple[list[Path], list[Path]]:
    for filename in REQUIRED_ROOT:
        add_failure(failures, (ROOT / filename).exists(), f"missing root file: {filename}")
    for filename in REQUIRED_ARTIFACT:
        add_failure(failures, (ARTIFACT / filename).exists(), f"missing artifact file: {filename}")
    fixtures = sorted(FIXTURES.glob("*.json"))
    failure_files = sorted(FAILURE_CASES.glob("*.json"))
    add_failure(failures, len(fixtures) >= 3, "expected at least 3 fixtures")
    add_failure(failures, len(failure_files) >= 1, "expected failure case file")
    return fixtures, failure_files


def builder_uses_execution() -> bool:
    text = read_text(ARTIFACT / "build_user_decision_operator_runbook_dry_run.py")
    return any(token in text for token in ["subprocess", "Start-Process", "Popen", "os.system"])


def dangerous_text_in_outputs() -> bool:
    text = "\n".join(
        [
            read_text(ARTIFACT / "user_decision_operator_runbook_dry_run.md"),
            read_text(ARTIFACT / "user_decision_operator_runbook_dry_run.html"),
            read_text(RUNBOOK_JSON),
        ]
    )
    return any(phrase in text for phrase in DANGEROUS_PHRASES)


def validate_contract(contract: dict, failures: list[str]) -> None:
    add_failure(failures, contract.get("record_kind") == "sandbox_user_decision_operator_runbook_dry_run_contract", "wrong contract record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong contract slice_id")
    add_failure(failures, contract.get("source_slice_id") == SOURCE_SLICE_ID, "wrong contract source_slice_id")
    add_failure(failures, contract.get("generation_contract", {}).get("source_execution_by_builder") is False, "builder source execution must be false")
    add_failure(failures, HARD_NO_REQUIRED <= set(contract.get("output_contract", {}).get("hard_no", [])), "contract hard_no incomplete")


def decision_by_kind(runbook: dict) -> dict:
    table = runbook.get("operator_decision_table", [])
    return {row.get("request_kind"): row for row in table if isinstance(row, dict)}


def validate_runbook(runbook: dict, current: dict, failures: list[str], label: str) -> None:
    add_failure(failures, runbook.get("record_kind") == "sandbox_user_decision_operator_runbook_dry_run", f"{label} wrong record_kind")
    add_failure(failures, runbook.get("slice_id") == SLICE_ID, f"{label} wrong slice_id")
    add_failure(failures, runbook.get("source_slice_id") == SOURCE_SLICE_ID, f"{label} wrong source_slice_id")
    add_failure(failures, runbook.get("dry_run_only") is True, f"{label} dry_run_only not true")
    add_failure(failures, runbook.get("source_execution_by_builder") is False, f"{label} source_execution_by_builder not false")
    add_failure(failures, runbook.get("runbook_ready") is True, f"{label} runbook_ready not true")
    summary = runbook.get("source_summary", {})
    current_summary = current.get("source_summary", {})
    if isinstance(summary, dict):
        add_failure(failures, summary.get("brief_ready") is True, f"{label} source brief not ready")
        add_failure(failures, summary.get("entry_count") == current_summary.get("entry_count") == 268, f"{label} entry count drift")
        add_failure(failures, summary.get("source_slice_count") == 9, f"{label} wrong source slice count")
        add_failure(failures, summary.get("manual_verification_automated_by_source") is False, f"{label} source manual verification automated")
        command = str(summary.get("manual_verification_command", ""))
        add_failure(failures, MANUAL_VERIFY_SOURCE_SLICE_ID in command and "--final-gate" in command, f"{label} manual command incomplete")
        source_status = summary.get("source_status", {})
        if isinstance(source_status, dict):
            add_failure(failures, source_status.get("verification_status") == "local_verification_passed", f"{label} source verification not passed")
            add_failure(failures, source_status.get("reviewer_passed") is True, f"{label} source reviewer not passed")
            add_failure(failures, source_status.get("boundary_passed") is True, f"{label} source boundary not passed")
            add_failure(failures, source_status.get("product_acceptance_passed") is True, f"{label} source product not passed")
            add_failure(failures, source_status.get("next_step_status") == "pass_product_grade_pending_next_slice", f"{label} source next-step not passed")
    else:
        failures.append(f"{label} source_summary missing")
    decisions = decision_by_kind(runbook)
    for request_kind in ["inspect_readiness_brief", "inspect_frozen_handoff_chain"]:
        row = decisions.get(request_kind, {})
        add_failure(failures, row.get("decision") == "ALLOW_READ_ONLY_INSPECTION", f"{label} {request_kind} not read-only inspect")
        add_failure(failures, row.get("writes_files") is False, f"{label} {request_kind} writes files")
        add_failure(failures, row.get("creates_authority") is False, f"{label} {request_kind} creates authority")
    manual = decisions.get("manual_drift_check", {})
    add_failure(failures, manual.get("decision") == "ALLOW_MANUAL_READONLY_VERIFICATION", f"{label} manual drift decision wrong")
    add_failure(failures, manual.get("manual_only") is True, f"{label} manual drift not manual only")
    add_failure(failures, manual.get("writes_files") is False, f"{label} manual drift writes files")
    add_failure(failures, manual.get("creates_authority") is False, f"{label} manual drift creates authority")
    for request_kind in STOP_REQUEST_KINDS:
        row = decisions.get(request_kind, {})
        add_failure(failures, row.get("decision") == "STOP_REQUIRE_SEPARATE_USER_APPROVAL", f"{label} {request_kind} not stopped")
        add_failure(failures, row.get("writes_files") is False, f"{label} {request_kind} writes files")
        add_failure(failures, row.get("creates_authority") is False, f"{label} {request_kind} creates authority")
    flags = runbook.get("readiness_flags", {})
    for flag in [
        "automatic_execution",
        "mainline_ready",
        "promotion_ready",
        "formal_vault_ready",
        "obsidian_sync_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
        "action_basis_ready",
        "user_approval_collected",
    ]:
        add_failure(failures, isinstance(flags, dict) and flags.get(flag) is False, f"{label} {flag} not false")
    add_failure(failures, HARD_NO_REQUIRED <= set(runbook.get("hard_no", [])), f"{label} hard_no incomplete")
    add_failure(failures, not builder_uses_execution(), f"{label} builder must not execute subprocess/process commands")
    add_failure(failures, not dangerous_text_in_outputs(), f"{label} dangerous phrase in finished outputs")
    add_failure(failures, not any(phrase in json.dumps(runbook, ensure_ascii=False) for phrase in DANGEROUS_PHRASES), f"{label} dangerous phrase in runbook object")


def validate_fixtures(fixtures: list[Path], runbook: dict, failures: list[str]) -> int:
    seen = set()
    decisions = decision_by_kind(runbook)
    for path in fixtures:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"{path.name} is not object")
            continue
        seen.add(fixture.get("fixture_id"))
        if fixture.get("fixture_id") == "readonly-inspection":
            for request_kind in fixture.get("request_kinds", []):
                add_failure(failures, decisions.get(request_kind, {}).get("decision") == "ALLOW_READ_ONLY_INSPECTION", f"{request_kind} fixture mismatch")
        elif fixture.get("fixture_id") == "stop-boundaries":
            for request_kind in fixture.get("request_kinds", []):
                add_failure(failures, decisions.get(request_kind, {}).get("decision") == "STOP_REQUIRE_SEPARATE_USER_APPROVAL", f"{request_kind} should stop")
        elif fixture.get("fixture_id") == "source-ready":
            add_failure(failures, runbook.get("source_summary", {}).get("entry_count") == fixture.get("entry_count"), "source-ready entry mismatch")
            add_failure(failures, runbook.get("runbook_ready") is True, "source-ready runbook not ready")
        else:
            failures.append(f"unknown fixture {path.name}")
    for required in ["readonly-inspection", "stop-boundaries", "source-ready"]:
        add_failure(failures, required in seen, f"missing fixture {required}")
    return len(fixtures)


def apply_mutation(runbook: dict, mutation: dict) -> dict:
    mutated = json.loads(json.dumps(runbook, ensure_ascii=False))
    if "set_top" in mutation:
        for key, value in mutation["set_top"].items():
            mutated[key] = value
    if "set_path" in mutation:
        cursor = mutated
        path = mutation["set_path"]["path"]
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = mutation["set_path"]["value"]
    if "set_decision" in mutation:
        target = mutation["set_decision"]["request_kind"]
        for row in mutated.get("operator_decision_table", []):
            if row.get("request_kind") == target:
                row["decision"] = mutation["set_decision"]["decision"]
    if "remove_hard_no" in mutation:
        value = mutation["remove_hard_no"]
        mutated["hard_no"] = [item for item in mutated.get("hard_no", []) if item != value]
    return mutated


def validate_failure_cases(files: list[Path], runbook: dict, current: dict, failures: list[str]) -> int:
    cases: list[dict] = []
    for path in files:
        payload = load_json(path)
        if isinstance(payload, list):
            cases.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            cases.append(payload)
    add_failure(failures, len(cases) >= 14, "expected at least 14 failure cases")
    ids = [case.get("failure_id") for case in cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure ids not unique")
    joined = "\n".join(str(case) for case in cases)
    for token in ["execute", "merge", "promotion", "sync", "commit", "push", "reviewed", "evidence", "action_basis", "user_approval", "dry_run", "manual", "entry", "dangerous"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for case in cases:
        mutation = case.get("mutation")
        add_failure(failures, isinstance(mutation, dict) and bool(mutation), f"{case.get('failure_id')} lacks mutation")
        if isinstance(mutation, dict):
            mutated = apply_mutation(runbook, mutation)
            local_failures: list[str] = []
            validate_runbook(mutated, current, local_failures, "mutated")
            add_failure(failures, bool(local_failures), f"{case.get('failure_id')} mutation was not rejected")
        add_failure(failures, HARD_NO_REQUIRED <= set(case.get("hard_no", [])), f"{case.get('failure_id')} hard_no incomplete")
    return len(cases)


def validate_final_reports(failures: list[str]) -> None:
    add_failure(failures, frontmatter_status(ROOT / "verification.md") == "local_verification_passed", "verification status not passed")
    add_failure(failures, "REVIEW_PASS_NO_BLOCKER" in read_text(ROOT / "reviewer-report.md"), "Reviewer report lacks REVIEW_PASS_NO_BLOCKER")
    add_failure(failures, "PASS_BOUNDARY" in read_text(ROOT / "boundary-audit.md"), "Boundary audit lacks PASS_BOUNDARY")
    add_failure(failures, "PASS_PRODUCT_GRADE" in read_text(ROOT / "product-acceptance-report.md"), "Product report lacks PASS_PRODUCT_GRADE")
    add_failure(failures, frontmatter_status(ROOT / "next-step.md") == "pass_product_grade_pending_next_slice", "next-step status not passed")


def verify(final_gate: bool = False) -> dict:
    failures: list[str] = []
    fixtures, failure_files = validate_files(failures)
    contract = load_json(ARTIFACT / "user_decision_operator_runbook_dry_run_contract.json") if (ARTIFACT / "user_decision_operator_runbook_dry_run_contract.json").exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    runbook = load_json(RUNBOOK_JSON) if RUNBOOK_JSON.exists() else {}
    builder = import_builder()
    current = builder.build_runbook()
    if isinstance(runbook, dict):
        validate_runbook(runbook, current, failures, "runbook")
    else:
        failures.append("runbook is not object")
        runbook = {}
    fixture_count = validate_fixtures(fixtures, runbook, failures)
    failure_case_count = validate_failure_cases(failure_files, runbook, current, failures)
    if final_gate:
        validate_final_reports(failures)
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "source_slice_id": SOURCE_SLICE_ID,
            "scenario_count": len(runbook.get("operator_decision_table", [])),
            "fixture_count": fixture_count,
            "failure_case_count": failure_case_count,
            "runbook_ready": runbook.get("runbook_ready"),
            "final_gate": final_gate,
        },
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = verify(final_gate=args.final_gate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
