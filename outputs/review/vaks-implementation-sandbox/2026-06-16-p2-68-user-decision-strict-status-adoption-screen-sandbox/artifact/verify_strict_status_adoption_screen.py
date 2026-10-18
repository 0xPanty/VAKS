from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-68-user-decision-strict-status-adoption-screen-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-67-user-decision-strict-status-package-sandbox"

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"
OUTPUT_JSON = ARTIFACT / "strict_status_adoption_screen.json"

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
    "build_strict_status_adoption_screen.py",
    "verify_strict_status_adoption_screen.py",
    "strict_status_adoption_screen_contract.json",
    "strict_status_adoption_screen.json",
    "strict_status_adoption_screen.md",
    "strict_status_adoption_screen.html",
]

EXPECTED_SOURCE_STATUSES = {
    "verification": "local_verification_passed",
    "reviewer": "review_pass_no_blocker",
    "boundary": "pass_boundary",
    "product": "pass_product_grade",
    "next_step": "pass_product_grade_pending_next_slice",
}

HARD_NO_REQUIRED = {
    "do_not_modify_old_slices",
    "do_not_create_shared_helper",
    "do_not_edit_tools",
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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def import_builder():
    path = ARTIFACT / "build_strict_status_adoption_screen.py"
    spec = importlib.util.spec_from_file_location("p2_68_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-68 builder")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def strict_status(text: str) -> str | None:
    return import_builder().strict_status(text)


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
    add_failure(failures, contract.get("record_kind") == "sandbox_strict_status_adoption_screen_contract", "wrong contract record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong contract slice_id")
    add_failure(failures, contract.get("source_slice_id") == SOURCE_SLICE_ID, "wrong contract source_slice_id")
    add_failure(failures, set(contract.get("allowed_next_without_separate_user_approval", [])) == {"future_new_sandbox_verifier_adoption", "package_only_hold"}, "allowed options mismatch")
    add_failure(failures, set(contract.get("parked_requires_separate_user_approval", [])) == {"old_slice_backfill", "shared_helper_or_tools_adoption", "mainline_integration"}, "parked options mismatch")
    output = contract.get("output_contract", {})
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


def validate_payload(payload: dict, current: dict, failures: list[str], label: str) -> None:
    add_failure(failures, payload.get("record_kind") == "sandbox_strict_status_adoption_screen", f"{label} wrong record_kind")
    add_failure(failures, payload.get("slice_id") == SLICE_ID, f"{label} wrong slice_id")
    add_failure(failures, payload.get("source_slice_id") == SOURCE_SLICE_ID, f"{label} wrong source_slice_id")
    add_failure(failures, payload == current, f"{label} does not match current builder output")
    add_failure(failures, payload.get("adoption_screen_ready") is True, f"{label} not ready")
    statuses = payload.get("source_statuses", {})
    for name, expected in EXPECTED_SOURCE_STATUSES.items():
        item = statuses.get(name, {}) if isinstance(statuses, dict) else {}
        add_failure(failures, item.get("status") == expected, f"{label} source {name} wrong status")
        add_failure(failures, item.get("matches_expected") is True, f"{label} source {name} not matched")
        add_failure(failures, SOURCE_SLICE_ID in str(item.get("path", "")), f"{label} source {name} path outside source slice")
    options = payload.get("adoption_options", [])
    by_id = {item.get("option_id"): item for item in options if isinstance(item, dict)}
    add_failure(failures, by_id.get("future_new_sandbox_verifier_adoption", {}).get("decision") == "RECOMMENDED_NEXT", f"{label} future verifier adoption not recommended")
    add_failure(failures, by_id.get("package_only_hold", {}).get("decision") == "ALLOW_AS_PARKED_OPTION", f"{label} package hold mismatch")
    for option_id in ["old_slice_backfill", "shared_helper_or_tools_adoption", "mainline_integration"]:
        add_failure(failures, by_id.get(option_id, {}).get("decision") == "PARK_REQUIRES_SEPARATE_USER_APPROVAL", f"{label} {option_id} not parked")
        add_failure(failures, by_id.get(option_id, {}).get("allowed_without_separate_user_approval") is False, f"{label} {option_id} allowed without approval")
    rec = payload.get("recommended_next_slice", {})
    add_failure(failures, rec.get("write_scope") == "new sandbox path only", f"{label} recommended next scope not sandbox")
    add_failure(failures, rec.get("slice_id") == "2026-06-16-p2-69-user-decision-future-verifier-adoption-prototype-sandbox", f"{label} wrong recommended next slice")
    flags = payload.get("readiness_flags", {})
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
        add_failure(failures, isinstance(flags, dict) and flags.get(flag) is False, f"{label} {flag} not false")
    add_failure(failures, HARD_NO_REQUIRED <= set(payload.get("hard_no", [])), f"{label} hard_no incomplete")


def validate_fixtures(fixtures: list[Path], payload: dict, failures: list[str]) -> int:
    seen = set()
    by_id = {item.get("option_id"): item for item in payload.get("adoption_options", []) if isinstance(item, dict)}
    for path in fixtures:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"{path.name} is not object")
            continue
        fixture_id = fixture.get("fixture_id")
        seen.add(fixture_id)
        option = by_id.get(fixture.get("option_id"), {})
        expected = fixture.get("expected", {})
        add_failure(failures, bool(option), f"{fixture_id} missing option")
        if isinstance(expected, dict):
            for key, value in expected.items():
                add_failure(failures, option.get(key) == value, f"{fixture_id} {key} mismatch")
    for required in ["recommend-future-sandbox-adoption", "allow-package-hold", "park-mainline-integration"]:
        add_failure(failures, required in seen, f"missing fixture {required}")
    return len(fixtures)


def apply_mutation(payload: dict, mutation: dict) -> dict:
    mutated = json.loads(json.dumps(payload, ensure_ascii=False))
    cursor = mutated
    path = mutation["set_path"]["path"]
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = mutation["set_path"]["value"]
    return mutated


def validate_failure_cases(files: list[Path], payload: dict, current: dict, failures: list[str]) -> int:
    cases: list[dict] = []
    for path in files:
        data = load_json(path)
        if isinstance(data, list):
            cases.extend(item for item in data if isinstance(item, dict))
        elif isinstance(data, dict):
            cases.append(data)
    add_failure(failures, len(cases) >= 10, "expected at least 10 failure cases")
    ids = [case.get("failure_id") for case in cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure ids not unique")
    joined = "\n".join(str(case) for case in cases)
    for token in ["old_slice", "shared_helper", "tools", "mainline", "promotion", "action_basis", "user_approval", "dependency", "network", "mcp"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for case in cases:
        mutation = case.get("mutation")
        add_failure(failures, isinstance(mutation, dict) and bool(mutation), f"{case.get('failure_id')} missing mutation")
        if isinstance(mutation, dict):
            mutated = apply_mutation(payload, mutation)
            local_failures: list[str] = []
            validate_payload(mutated, current, local_failures, "mutated")
            add_failure(failures, bool(local_failures), f"{case.get('failure_id')} mutation was not rejected")
        add_failure(failures, HARD_NO_REQUIRED <= set(case.get("hard_no", [])), f"{case.get('failure_id')} hard_no incomplete")
    return len(cases)


def final_status(path: Path) -> str | None:
    return strict_status(read_text(path))


def validate_final_reports(failures: list[str]) -> None:
    add_failure(failures, final_status(ROOT / "verification.md") == "local_verification_passed", "verification status not passed")
    add_failure(failures, final_status(ROOT / "reviewer-report.md") == "review_pass_no_blocker", "Reviewer report status not passed")
    add_failure(failures, final_status(ROOT / "boundary-audit.md") == "pass_boundary", "Boundary audit status not passed")
    add_failure(failures, final_status(ROOT / "product-acceptance-report.md") == "pass_product_grade", "Product report status not passed")
    add_failure(failures, final_status(ROOT / "next-step.md") == "pass_product_grade_pending_next_slice", "next-step status not passed")


def verify(final_gate: bool = False) -> dict:
    failures: list[str] = []
    fixtures, failure_files = validate_files(failures)
    contract_path = ARTIFACT / "strict_status_adoption_screen_contract.json"
    contract = load_json(contract_path) if contract_path.exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    payload = load_json(OUTPUT_JSON) if OUTPUT_JSON.exists() else {}
    builder = import_builder()
    current = builder.build_screen()
    if isinstance(payload, dict):
        validate_payload(payload, current, failures, "payload")
    else:
        failures.append("payload is not object")
        payload = {}
    fixture_count = validate_fixtures(fixtures, payload, failures)
    failure_case_count = validate_failure_cases(failure_files, payload, current, failures)
    if final_gate:
        validate_final_reports(failures)
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "source_slice_id": SOURCE_SLICE_ID,
            "adoption_screen_ready": payload.get("adoption_screen_ready"),
            "fixture_count": fixture_count,
            "failure_case_count": failure_case_count,
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
