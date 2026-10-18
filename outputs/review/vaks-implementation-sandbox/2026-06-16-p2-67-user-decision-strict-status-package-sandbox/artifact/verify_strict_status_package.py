from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-67-user-decision-strict-status-package-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-66-user-decision-chain-hardening-readiness-sandbox"

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"
OUTPUT_JSON = ARTIFACT / "strict_status_package_manifest.json"

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
    "strict_status_package.py",
    "build_strict_status_package.py",
    "verify_strict_status_package.py",
    "strict_status_package_contract.json",
    "strict_status_package_manifest.json",
    "strict_status_package_manifest.md",
    "strict_status_package_manifest.html",
]

HARD_NO_REQUIRED = {
    "do_not_modify_old_slices",
    "do_not_create_shared_helper",
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


def import_module(name: str, path: Path):
    if str(ARTIFACT) not in sys.path:
        sys.path.insert(0, str(ARTIFACT))
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def package_module():
    return import_module("strict_status_package_for_verify", ARTIFACT / "strict_status_package.py")


def builder_module():
    return import_module("p2_67_builder", ARTIFACT / "build_strict_status_package.py")


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
    add_failure(failures, contract.get("record_kind") == "sandbox_strict_status_package_contract", "wrong contract record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong contract slice_id")
    add_failure(failures, contract.get("source_slice_id") == SOURCE_SLICE_ID, "wrong contract source_slice_id")
    api = contract.get("package_api", {})
    add_failure(failures, "parse_strict_frontmatter_status" in api, "contract missing parse API")
    add_failure(failures, "status_matches" in api, "contract missing status_matches API")
    behavior = contract.get("behavior_contract", {})
    add_failure(failures, behavior.get("builder_writes_manifest_outputs") is True, "contract builder_writes_manifest_outputs not true")
    add_failure(failures, behavior.get("builder_write_scope") == "this sandbox artifact directory only", "contract builder_write_scope mismatch")
    add_failure(failures, behavior.get("verifier_read_only") is True, "contract verifier_read_only not true")
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


def validate_manifest(payload: dict, current: dict, failures: list[str]) -> None:
    add_failure(failures, payload.get("record_kind") == "sandbox_strict_status_package_manifest", "wrong record_kind")
    add_failure(failures, payload.get("slice_id") == SLICE_ID, "wrong slice_id")
    add_failure(failures, payload.get("source_slice_id") == SOURCE_SLICE_ID, "wrong source_slice_id")
    add_failure(failures, payload == current, "manifest does not match current builder output")
    add_failure(failures, payload.get("package_ready") is True, "package not ready")
    add_failure(failures, "artifact/strict_status_package.py" in payload.get("package_files", []), "package file missing from manifest")
    tests = payload.get("self_tests", {})
    add_failure(failures, isinstance(tests, dict) and all(tests.values()), "self tests not all true")
    behavior = payload.get("behavior_contract", {})
    add_failure(failures, behavior.get("builder_writes_manifest_outputs") is True, "manifest builder_writes_manifest_outputs not true")
    add_failure(failures, str(behavior.get("builder_write_scope", "")).endswith("2026-06-16-p2-67-user-decision-strict-status-package-sandbox/artifact"), "manifest builder_write_scope outside artifact")
    add_failure(failures, behavior.get("verifier_read_only") is True, "manifest verifier_read_only not true")
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
        add_failure(failures, isinstance(flags, dict) and flags.get(flag) is False, f"{flag} not false")
    add_failure(failures, HARD_NO_REQUIRED <= set(payload.get("hard_no", [])), "hard_no incomplete")


def validate_fixtures(fixtures: list[Path], failures: list[str]) -> int:
    pkg = package_module()
    seen = set()
    for path in fixtures:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"{path.name} is not object")
            continue
        fixture_id = fixture.get("fixture_id")
        seen.add(fixture_id)
        parsed = pkg.parse_strict_frontmatter_status(fixture.get("document", ""))
        expected = fixture.get("expected", {})
        add_failure(failures, parsed.get("valid") is expected.get("valid"), f"{fixture_id} valid mismatch")
        add_failure(failures, parsed.get("status") == expected.get("status"), f"{fixture_id} status mismatch")
        if "status_matches" in expected:
            add_failure(failures, pkg.status_matches(fixture.get("document", ""), expected.get("status")) is expected.get("status_matches"), f"{fixture_id} status_matches mismatch")
    for required in ["valid-pass-status", "body-status-ignored", "status-matches-api"]:
        add_failure(failures, required in seen, f"missing fixture {required}")
    return len(fixtures)


def validate_failure_cases(files: list[Path], failures: list[str]) -> int:
    pkg = package_module()
    cases: list[dict] = []
    for path in files:
        data = load_json(path)
        if isinstance(data, list):
            cases.extend(item for item in data if isinstance(item, dict))
        elif isinstance(data, dict):
            cases.append(data)
    add_failure(failures, len(cases) >= 8, "expected at least 8 failure cases")
    ids = [case.get("failure_id") for case in cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure ids not unique")
    joined = "\n".join(str(case) for case in cases)
    for token in ["opening", "closing", "duplicate", "empty", "body", "substring", "uppercase", "authority"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for case in cases:
        parsed = pkg.parse_strict_frontmatter_status(case.get("document", ""))
        if "expected_valid" in case:
            add_failure(failures, parsed.get("valid") is case.get("expected_valid"), f"{case.get('failure_id')} valid mismatch")
        if "expected_status" in case:
            add_failure(failures, parsed.get("status") == case.get("expected_status"), f"{case.get('failure_id')} status mismatch")
        if case.get("forbidden_status"):
            add_failure(failures, parsed.get("status") != case.get("forbidden_status"), f"{case.get('failure_id')} returned forbidden status")
        for error in case.get("expected_errors_contains", []):
            add_failure(failures, error in parsed.get("errors", []), f"{case.get('failure_id')} missing error {error}")
        add_failure(failures, HARD_NO_REQUIRED <= set(case.get("hard_no", [])), f"{case.get('failure_id')} hard_no incomplete")
    return len(cases)


def final_status(path: Path) -> str | None:
    return package_module().parse_strict_frontmatter_status(read_text(path)).get("status")


def validate_final_reports(failures: list[str]) -> None:
    add_failure(failures, final_status(ROOT / "verification.md") == "local_verification_passed", "verification status not passed")
    add_failure(failures, final_status(ROOT / "reviewer-report.md") == "review_pass_no_blocker", "Reviewer report status not passed")
    add_failure(failures, final_status(ROOT / "boundary-audit.md") == "pass_boundary", "Boundary audit status not passed")
    add_failure(failures, final_status(ROOT / "product-acceptance-report.md") == "pass_product_grade", "Product report status not passed")
    add_failure(failures, final_status(ROOT / "next-step.md") == "pass_product_grade_pending_next_slice", "next-step status not passed")


def verify(final_gate: bool = False) -> dict:
    failures: list[str] = []
    fixtures, failure_files = validate_files(failures)
    contract_path = ARTIFACT / "strict_status_package_contract.json"
    contract = load_json(contract_path) if contract_path.exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    payload = load_json(OUTPUT_JSON) if OUTPUT_JSON.exists() else {}
    current = builder_module().build_manifest()
    if isinstance(payload, dict):
        validate_manifest(payload, current, failures)
    else:
        failures.append("manifest is not object")
        payload = {}
    fixture_count = validate_fixtures(fixtures, failures)
    failure_case_count = validate_failure_cases(failure_files, failures)
    if final_gate:
        validate_final_reports(failures)
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "source_slice_id": SOURCE_SLICE_ID,
            "package_ready": payload.get("package_ready"),
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
