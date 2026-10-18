from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-64-user-decision-replay-portability-audit-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-63-user-decision-runbook-replay-regression-sandbox"

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"
AUDIT_JSON = ARTIFACT / "user_decision_replay_portability_audit.json"

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
    "build_user_decision_replay_portability_audit.py",
    "verify_user_decision_replay_portability_audit.py",
    "user_decision_replay_portability_audit_contract.json",
    "user_decision_replay_portability_audit.json",
    "user_decision_replay_portability_audit.md",
    "user_decision_replay_portability_audit.html",
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
    "do_not_use_mcp_write_tool",
    "do_not_create_reviewed_knowledge",
    "do_not_create_evidence_support",
    "do_not_create_action_basis",
    "do_not_collect_user_approval_by_inference",
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
    path = ARTIFACT / "build_user_decision_replay_portability_audit.py"
    spec = importlib.util.spec_from_file_location("p2_64_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-64 builder")
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


def dangerous_text_in_outputs() -> bool:
    text = "\n".join(
        [
            read_text(ARTIFACT / "user_decision_replay_portability_audit.md"),
            read_text(ARTIFACT / "user_decision_replay_portability_audit.html"),
            read_text(AUDIT_JSON),
        ]
    )
    return any(phrase in text for phrase in DANGEROUS_PHRASES)


def validate_contract(contract: dict, failures: list[str]) -> None:
    add_failure(failures, contract.get("record_kind") == "sandbox_user_decision_replay_portability_audit_contract", "wrong contract record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong contract slice_id")
    add_failure(failures, contract.get("source_slice_id") == SOURCE_SLICE_ID, "wrong contract source_slice_id")
    add_failure(failures, contract.get("generation_contract", {}).get("source_execution_by_builder") is False, "builder source execution must be false")
    output = contract.get("output_contract", {})
    add_failure(failures, output.get("dry_run_only") is True, "contract dry_run_only not true")
    for flag in [
        "dependency_install_required",
        "network_required",
        "mcp_required",
        "background_service_required",
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
        add_failure(failures, output.get(flag) is False, f"contract {flag} not false")


def validate_audit(audit: dict, current: dict, failures: list[str], label: str) -> None:
    add_failure(failures, audit.get("record_kind") == "sandbox_user_decision_replay_portability_audit", f"{label} wrong record_kind")
    add_failure(failures, audit.get("slice_id") == SLICE_ID, f"{label} wrong slice_id")
    add_failure(failures, audit.get("source_slice_id") == SOURCE_SLICE_ID, f"{label} wrong source_slice_id")
    add_failure(failures, audit.get("portability_ready") is True, f"{label} portability_ready not true")
    source = audit.get("source_summary", {})
    current_source = current.get("source_summary", {})
    if isinstance(source, dict):
        add_failure(failures, source.get("replay_ready") is True, f"{label} source replay not ready")
        add_failure(failures, source.get("replay_count") == current_source.get("replay_count") == 15, f"{label} replay count drift")
        add_failure(failures, source.get("passed_count") == current_source.get("passed_count") == 15, f"{label} passed count drift")
        status = source.get("source_status", {})
        if isinstance(status, dict):
            add_failure(failures, status.get("verification_status") == "local_verification_passed", f"{label} source verification not passed")
            add_failure(failures, status.get("reviewer_passed") is True, f"{label} source reviewer not passed")
            add_failure(failures, status.get("boundary_passed") is True, f"{label} source boundary not passed")
            add_failure(failures, status.get("product_acceptance_passed") is True, f"{label} source product not passed")
            add_failure(failures, status.get("next_step_status") == "pass_product_grade_pending_next_slice", f"{label} source next-step not passed")
    else:
        failures.append(f"{label} source_summary missing")
    deps = audit.get("dependency_audit", {})
    if isinstance(deps, dict):
        add_failure(failures, deps.get("standard_library_only") is True, f"{label} standard library only not true")
        add_failure(failures, deps.get("dependency_install_required") is False, f"{label} dependency install required")
        add_failure(failures, deps.get("network_required") is False, f"{label} network required")
        add_failure(failures, deps.get("mcp_required") is False, f"{label} mcp required")
        add_failure(failures, deps.get("background_service_required") is False, f"{label} background service required")
    else:
        failures.append(f"{label} dependency_audit missing")
    execution = audit.get("execution_audit", {})
    if isinstance(execution, dict):
        add_failure(failures, execution.get("source_execution_by_builder") is False, f"{label} source execution by builder not false")
        add_failure(failures, execution.get("builder_process_execution_tokens") == [], f"{label} builder process execution tokens present")
    else:
        failures.append(f"{label} execution_audit missing")
    path_audit = audit.get("path_audit", {})
    if isinstance(path_audit, dict):
        add_failure(failures, path_audit.get("stable_paths") is True, f"{label} stable paths not true")
        source_paths = path_audit.get("source_paths", [])
        add_failure(failures, isinstance(source_paths, list) and len(source_paths) >= 8, f"{label} source paths incomplete")
        add_failure(failures, all(SOURCE_SLICE_ID in str(path) for path in source_paths), f"{label} source path outside source slice")
    else:
        failures.append(f"{label} path_audit missing")
    command = audit.get("command_audit", {})
    if isinstance(command, dict):
        add_failure(failures, command.get("clear_commands") is True, f"{label} clear commands not true")
        commands = command.get("commands", {})
        if isinstance(commands, dict):
            for key in ["build_replay", "verify_replay", "final_gate"]:
                add_failure(failures, key in commands, f"{label} missing command {key}")
                add_failure(failures, str(commands.get(key, "")).startswith("python -B .\\outputs\\review\\vaks-implementation-sandbox\\"), f"{label} command {key} not portable")
            add_failure(failures, "--final-gate" in str(commands.get("final_gate", "")), f"{label} final gate command missing flag")
        else:
            failures.append(f"{label} commands missing")
        sequence = command.get("operator_sequence", [])
        add_failure(failures, isinstance(sequence, list) and len(sequence) >= 5, f"{label} operator sequence incomplete")
    else:
        failures.append(f"{label} command_audit missing")
    flags = audit.get("readiness_flags", {})
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
    add_failure(failures, HARD_NO_REQUIRED <= set(audit.get("hard_no", [])), f"{label} hard_no incomplete")
    add_failure(failures, not dangerous_text_in_outputs(), f"{label} dangerous phrase in finished outputs")
    add_failure(failures, not any(phrase in json.dumps(audit, ensure_ascii=False) for phrase in DANGEROUS_PHRASES), f"{label} dangerous phrase in audit object")


def validate_fixtures(fixtures: list[Path], audit: dict, failures: list[str]) -> int:
    seen = set()
    for path in fixtures:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"{path.name} is not object")
            continue
        seen.add(fixture.get("fixture_id"))
        if fixture.get("fixture_id") == "dependency-portable":
            deps = audit.get("dependency_audit", {})
            add_failure(failures, deps.get("standard_library_only") is True, "dependency fixture mismatch")
            add_failure(failures, deps.get("dependency_install_required") is False, "dependency install fixture mismatch")
        elif fixture.get("fixture_id") == "command-portable":
            command = audit.get("command_audit", {})
            add_failure(failures, command.get("clear_commands") is True, "command fixture mismatch")
        elif fixture.get("fixture_id") == "path-portable":
            add_failure(failures, audit.get("path_audit", {}).get("stable_paths") is True, "path fixture mismatch")
        else:
            failures.append(f"unknown fixture {path.name}")
    for required in ["dependency-portable", "command-portable", "path-portable"]:
        add_failure(failures, required in seen, f"missing fixture {required}")
    return len(fixtures)


def apply_mutation(audit: dict, mutation: dict) -> dict:
    mutated = json.loads(json.dumps(audit, ensure_ascii=False))
    if "set_top" in mutation:
        for key, value in mutation["set_top"].items():
            mutated[key] = value
    if "set_path" in mutation:
        cursor = mutated
        path = mutation["set_path"]["path"]
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = mutation["set_path"]["value"]
    if "remove_hard_no" in mutation:
        value = mutation["remove_hard_no"]
        mutated["hard_no"] = [item for item in mutated.get("hard_no", []) if item != value]
    return mutated


def validate_failure_cases(files: list[Path], audit: dict, current: dict, failures: list[str]) -> int:
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
    for token in ["dependency", "network", "mcp", "service", "execution", "path", "command", "replay", "mainline", "promotion", "action_basis", "user_approval", "dangerous", "hard_no"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for case in cases:
        mutation = case.get("mutation")
        add_failure(failures, isinstance(mutation, dict) and bool(mutation), f"{case.get('failure_id')} lacks mutation")
        if isinstance(mutation, dict):
            mutated = apply_mutation(audit, mutation)
            local_failures: list[str] = []
            validate_audit(mutated, current, local_failures, "mutated")
            add_failure(failures, bool(local_failures), f"{case.get('failure_id')} mutation was not rejected")
        add_failure(failures, HARD_NO_REQUIRED <= set(case.get("hard_no", [])), f"{case.get('failure_id')} hard_no incomplete")
    return len(cases)


def validate_final_reports(failures: list[str]) -> None:
    add_failure(failures, frontmatter_status(ROOT / "verification.md") == "local_verification_passed", "verification status not passed")
    add_failure(failures, frontmatter_status(ROOT / "reviewer-report.md") == "review_pass_no_blocker", "Reviewer report status not review_pass_no_blocker")
    add_failure(failures, frontmatter_status(ROOT / "boundary-audit.md") == "pass_boundary", "Boundary audit status not pass_boundary")
    add_failure(failures, frontmatter_status(ROOT / "product-acceptance-report.md") == "pass_product_grade", "Product report status not pass_product_grade")
    add_failure(failures, frontmatter_status(ROOT / "next-step.md") == "pass_product_grade_pending_next_slice", "next-step status not passed")


def verify(final_gate: bool = False) -> dict:
    failures: list[str] = []
    fixtures, failure_files = validate_files(failures)
    contract = load_json(ARTIFACT / "user_decision_replay_portability_audit_contract.json") if (ARTIFACT / "user_decision_replay_portability_audit_contract.json").exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    audit = load_json(AUDIT_JSON) if AUDIT_JSON.exists() else {}
    builder = import_builder()
    current = builder.build_audit()
    if isinstance(audit, dict):
        validate_audit(audit, current, failures, "audit")
    else:
        failures.append("audit is not object")
        audit = {}
    fixture_count = validate_fixtures(fixtures, audit, failures)
    failure_case_count = validate_failure_cases(failure_files, audit, current, failures)
    if final_gate:
        validate_final_reports(failures)
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "source_slice_id": SOURCE_SLICE_ID,
            "portability_ready": audit.get("portability_ready"),
            "fixture_count": fixture_count,
            "failure_case_count": failure_case_count,
            "standard_library_only": audit.get("dependency_audit", {}).get("standard_library_only"),
            "stable_paths": audit.get("path_audit", {}).get("stable_paths"),
            "clear_commands": audit.get("command_audit", {}).get("clear_commands"),
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
