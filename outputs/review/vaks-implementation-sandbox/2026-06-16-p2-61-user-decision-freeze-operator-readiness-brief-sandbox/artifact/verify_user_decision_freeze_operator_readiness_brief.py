from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-61-user-decision-freeze-operator-readiness-brief-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-60-user-decision-index-freeze-checksum-sandbox"

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"
BRIEF_JSON = ARTIFACT / "user_decision_freeze_operator_readiness_brief.json"

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
    "build_user_decision_freeze_operator_readiness_brief.py",
    "verify_user_decision_freeze_operator_readiness_brief.py",
    "user_decision_freeze_operator_readiness_brief_contract.json",
    "user_decision_freeze_operator_readiness_brief.json",
    "user_decision_freeze_operator_readiness_brief.md",
    "user_decision_freeze_operator_readiness_brief.html",
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
    "do_not_treat_checksum_as_user_approval",
}

DANGEROUS_PHRASES = [
    "mainline approved",
    "promotion approved",
    "execution approved",
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
    path = ARTIFACT / "build_user_decision_freeze_operator_readiness_brief.py"
    spec = importlib.util.spec_from_file_location("p2_61_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-61 builder")
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


def validate_contract(contract: dict, failures: list[str]) -> None:
    add_failure(failures, contract.get("record_kind") == "sandbox_user_decision_freeze_operator_readiness_brief_contract", "wrong contract record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong contract slice_id")
    add_failure(failures, contract.get("source_slice_id") == SOURCE_SLICE_ID, "wrong contract source_slice_id")
    add_failure(failures, contract.get("generation_contract", {}).get("source_execution_by_builder") is False, "builder source execution must be false")
    command = contract.get("manual_readonly_verification_command", "")
    add_failure(failures, SOURCE_SLICE_ID in command and "--final-gate" in command, "manual verification command incomplete")
    add_failure(failures, HARD_NO_REQUIRED <= set(contract.get("output_contract", {}).get("hard_no", [])), "contract hard_no incomplete")


def dangerous_text_in_outputs() -> bool:
    text = "\n".join(
        [
            read_text(ARTIFACT / "user_decision_freeze_operator_readiness_brief.md"),
            read_text(ARTIFACT / "user_decision_freeze_operator_readiness_brief.html"),
            read_text(BRIEF_JSON),
        ]
    )
    return any(phrase in text for phrase in DANGEROUS_PHRASES)


def builder_uses_subprocess() -> bool:
    text = read_text(ARTIFACT / "build_user_decision_freeze_operator_readiness_brief.py")
    return "subprocess" in text or "Start-Process" in text


def validate_brief(brief: dict, current: dict, failures: list[str], label: str) -> None:
    add_failure(failures, brief.get("record_kind") == "sandbox_user_decision_freeze_operator_readiness_brief", f"{label} wrong record_kind")
    add_failure(failures, brief.get("slice_id") == SLICE_ID, f"{label} wrong slice_id")
    add_failure(failures, brief.get("source_slice_id") == SOURCE_SLICE_ID, f"{label} wrong source_slice_id")
    add_failure(failures, brief.get("brief_ready") is True, f"{label} brief_ready not true")
    inputs = brief.get("readiness_inputs", {})
    current_inputs = current.get("readiness_inputs", {})
    add_failure(failures, isinstance(inputs, dict), f"{label} readiness_inputs missing")
    if isinstance(inputs, dict):
        add_failure(failures, inputs.get("source_manifest_exists") is True, f"{label} source manifest missing")
        add_failure(failures, inputs.get("source_slice_count") == 9, f"{label} wrong source slice count")
        add_failure(failures, inputs.get("entry_count") == current_inputs.get("entry_count"), f"{label} entry count drift")
        add_failure(failures, inputs.get("entry_count") == 268, f"{label} expected 268 frozen entries")
        add_failure(failures, inputs.get("missing_count") == 0, f"{label} missing count not zero")
        add_failure(failures, inputs.get("hash_algorithm") == "sha256_bytes", f"{label} wrong hash algorithm")
        add_failure(failures, inputs.get("freeze_ready") is True, f"{label} source freeze not ready")
        add_failure(failures, inputs.get("latest_source_final_gate_passed") is True, f"{label} source final gate not passed")
    status = brief.get("source_status", {})
    if isinstance(status, dict):
        add_failure(failures, status.get("verification_status") == "local_verification_passed", f"{label} source verification not passed")
        add_failure(failures, status.get("reviewer_passed") is True, f"{label} source reviewer not passed")
        add_failure(failures, status.get("boundary_passed") is True, f"{label} source boundary not passed")
        add_failure(failures, status.get("product_acceptance_passed") is True, f"{label} source product not passed")
        add_failure(failures, status.get("next_step_status") == "pass_product_grade_pending_next_slice", f"{label} source next-step not passed")
    else:
        failures.append(f"{label} source_status missing")
    manual = brief.get("manual_readonly_verification", {})
    if isinstance(manual, dict):
        command = manual.get("command", "")
        add_failure(failures, SOURCE_SLICE_ID in command and "--final-gate" in command, f"{label} manual command incomplete")
        add_failure(failures, manual.get("automation_by_this_artifact") is False, f"{label} manual command automated by artifact")
        add_failure(failures, manual.get("writes_files") is False, f"{label} manual command claims writes")
    else:
        failures.append(f"{label} manual verification missing")
    flags = brief.get("readiness_flags", {})
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
    add_failure(failures, HARD_NO_REQUIRED <= set(brief.get("hard_no", [])), f"{label} hard_no incomplete")
    add_failure(failures, not builder_uses_subprocess(), f"{label} builder must not execute subprocess")
    add_failure(failures, not dangerous_text_in_outputs(), f"{label} dangerous phrase in output")
    serialized = json.dumps(brief, ensure_ascii=False)
    add_failure(failures, not any(phrase in serialized for phrase in DANGEROUS_PHRASES), f"{label} dangerous phrase in brief object")


def validate_fixtures(fixtures: list[Path], brief: dict, failures: list[str]) -> int:
    seen = set()
    for path in fixtures:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"{path.name} is not object")
            continue
        seen.add(fixture.get("fixture_id"))
        if fixture.get("fixture_id") == "freeze-summary":
            add_failure(failures, brief.get("readiness_inputs", {}).get("entry_count") == fixture.get("entry_count"), "freeze-summary entry mismatch")
            add_failure(failures, brief.get("readiness_inputs", {}).get("source_slice_count") == fixture.get("source_slice_count"), "freeze-summary source mismatch")
        elif fixture.get("fixture_id") == "manual-verification":
            manual = brief.get("manual_readonly_verification", {})
            add_failure(failures, fixture.get("requires_final_gate") is ("--final-gate" in manual.get("command", "")), "manual verification final gate mismatch")
            add_failure(failures, manual.get("automation_by_this_artifact") is False, "manual verification should not be automated")
        elif fixture.get("fixture_id") == "hard-boundary":
            add_failure(failures, HARD_NO_REQUIRED <= set(brief.get("hard_no", [])), "hard-boundary fixture mismatch")
        else:
            failures.append(f"unknown fixture {path.name}")
    for required in ["freeze-summary", "manual-verification", "hard-boundary"]:
        add_failure(failures, required in seen, f"missing fixture {required}")
    return len(fixtures)


def apply_mutation(brief: dict, mutation: dict) -> dict:
    mutated = json.loads(json.dumps(brief, ensure_ascii=False))
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


def validate_failure_cases(files: list[Path], brief: dict, current: dict, failures: list[str]) -> int:
    cases: list[dict] = []
    for path in files:
        payload = load_json(path)
        if isinstance(payload, list):
            cases.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            cases.append(payload)
    add_failure(failures, len(cases) >= 12, "expected at least 12 failure cases")
    ids = [case.get("failure_id") for case in cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure ids not unique")
    joined = "\n".join(str(case) for case in cases)
    for token in ["entry", "source", "manifest", "final", "automation", "mainline", "promotion", "action_basis", "user_approval", "hard_no", "dangerous", "hash"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for case in cases:
        mutation = case.get("mutation")
        add_failure(failures, isinstance(mutation, dict) and bool(mutation), f"{case.get('failure_id')} lacks mutation")
        if isinstance(mutation, dict):
            mutated = apply_mutation(brief, mutation)
            local_failures: list[str] = []
            validate_brief(mutated, current, local_failures, "mutated")
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
    contract = load_json(ARTIFACT / "user_decision_freeze_operator_readiness_brief_contract.json") if (ARTIFACT / "user_decision_freeze_operator_readiness_brief_contract.json").exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    brief = load_json(BRIEF_JSON) if BRIEF_JSON.exists() else {}
    builder = import_builder()
    current = builder.build_brief()
    if isinstance(brief, dict):
        validate_brief(brief, current, failures, "brief")
    else:
        failures.append("brief is not object")
        brief = {}
    fixture_count = validate_fixtures(fixtures, brief, failures)
    failure_case_count = validate_failure_cases(failure_files, brief, current, failures)
    if final_gate:
        validate_final_reports(failures)
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "source_slice_id": SOURCE_SLICE_ID,
            "entry_count": brief.get("readiness_inputs", {}).get("entry_count"),
            "fixture_count": fixture_count,
            "failure_case_count": failure_case_count,
            "brief_ready": brief.get("brief_ready"),
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
