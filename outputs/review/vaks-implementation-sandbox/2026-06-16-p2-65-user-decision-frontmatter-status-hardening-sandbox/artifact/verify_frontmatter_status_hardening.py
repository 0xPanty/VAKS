from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-65-user-decision-frontmatter-status-hardening-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-64-user-decision-replay-portability-audit-sandbox"

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"
OUTPUT_JSON = ARTIFACT / "frontmatter_status_hardening.json"

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
    "build_frontmatter_status_hardening.py",
    "verify_frontmatter_status_hardening.py",
    "frontmatter_status_hardening_contract.json",
    "frontmatter_status_hardening.json",
    "frontmatter_status_hardening.md",
    "frontmatter_status_hardening.html",
]

EXPECTED_SOURCE_STATUSES = {
    "verification": "local_verification_passed",
    "reviewer": "review_pass_no_blocker",
    "boundary": "pass_boundary",
    "product": "pass_product_grade",
    "next_step": "pass_product_grade_pending_next_slice",
}

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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def import_builder():
    path = ARTIFACT / "build_frontmatter_status_hardening.py"
    spec = importlib.util.spec_from_file_location("p2_65_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-65 builder")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_status(text: str) -> dict:
    return import_builder().parse_strict_frontmatter_status(text)


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
    add_failure(failures, contract.get("record_kind") == "sandbox_frontmatter_status_hardening_contract", "wrong contract record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong contract slice_id")
    add_failure(failures, contract.get("source_slice_id") == SOURCE_SLICE_ID, "wrong contract source_slice_id")
    parser = contract.get("parser_contract", {})
    for key in [
        "requires_opening_frontmatter_delimiter",
        "requires_closing_frontmatter_delimiter",
        "requires_exactly_one_status_in_frontmatter",
        "requires_non_empty_status",
        "ignores_body_status_mentions",
        "does_not_substring_match_pass_tokens",
    ]:
        add_failure(failures, isinstance(parser, dict) and parser.get(key) is True, f"contract parser {key} not true")
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
    add_failure(failures, payload.get("record_kind") == "sandbox_frontmatter_status_hardening", f"{label} wrong record_kind")
    add_failure(failures, payload.get("slice_id") == SLICE_ID, f"{label} wrong slice_id")
    add_failure(failures, payload.get("source_slice_id") == SOURCE_SLICE_ID, f"{label} wrong source_slice_id")
    add_failure(failures, payload == current, f"{label} does not match current builder output")
    add_failure(failures, payload.get("frontmatter_status_hardening_ready") is True, f"{label} hardening not ready")
    statuses = payload.get("source_statuses", {})
    if isinstance(statuses, dict):
        for name, expected in EXPECTED_SOURCE_STATUSES.items():
            item = statuses.get(name, {})
            add_failure(failures, isinstance(item, dict), f"{label} missing source status {name}")
            if isinstance(item, dict):
                add_failure(failures, item.get("valid_frontmatter") is True, f"{label} {name} invalid frontmatter")
                add_failure(failures, item.get("status") == expected, f"{label} {name} wrong status")
                add_failure(failures, item.get("matches_expected") is True, f"{label} {name} does not match expected")
                add_failure(failures, SOURCE_SLICE_ID in str(item.get("path", "")), f"{label} {name} path outside source slice")
    else:
        failures.append(f"{label} source_statuses missing")
    parser = payload.get("parser_contract", {})
    for key, value in parser.items() if isinstance(parser, dict) else []:
        add_failure(failures, value is True, f"{label} parser contract {key} not true")
    flags = payload.get("readiness_flags", {})
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
    add_failure(failures, HARD_NO_REQUIRED <= set(payload.get("hard_no", [])), f"{label} hard_no incomplete")


def validate_fixtures(fixtures: list[Path], failures: list[str]) -> int:
    seen = set()
    for path in fixtures:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"{path.name} is not object")
            continue
        fixture_id = fixture.get("fixture_id")
        seen.add(fixture_id)
        document = fixture.get("document")
        expected = fixture.get("expected", {})
        add_failure(failures, isinstance(document, str) and bool(document), f"{fixture_id} missing document")
        parsed = parse_status(document if isinstance(document, str) else "")
        if isinstance(expected, dict):
            add_failure(failures, parsed.get("valid") is expected.get("valid"), f"{fixture_id} valid mismatch")
            add_failure(failures, parsed.get("status") == expected.get("status"), f"{fixture_id} status mismatch")
            if expected.get("body_status_ignored") is True:
                add_failure(failures, parsed.get("status") != expected.get("body_status"), f"{fixture_id} body status was not ignored")
        else:
            failures.append(f"{fixture_id} expected missing")
    for required in ["valid-product-frontmatter", "valid-next-step-frontmatter", "body-status-ignored"]:
        add_failure(failures, required in seen, f"missing fixture {required}")
    return len(fixtures)


def validate_failure_cases(files: list[Path], failures: list[str]) -> int:
    cases: list[dict] = []
    for path in files:
        payload = load_json(path)
        if isinstance(payload, list):
            cases.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            cases.append(payload)
    add_failure(failures, len(cases) >= 8, "expected at least 8 failure cases")
    ids = [case.get("failure_id") for case in cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure ids not unique")
    joined = "\n".join(str(case) for case in cases)
    for token in ["opening", "closing", "body", "duplicate", "empty", "uppercase", "substring", "authority"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for case in cases:
        document = case.get("document")
        add_failure(failures, isinstance(document, str) and bool(document), f"{case.get('failure_id')} missing document")
        parsed = parse_status(document if isinstance(document, str) else "")
        if "expected_valid" in case:
            add_failure(failures, parsed.get("valid") is case.get("expected_valid"), f"{case.get('failure_id')} valid mismatch")
        expected_status = case.get("expected_status")
        if expected_status:
            add_failure(failures, parsed.get("status") == expected_status, f"{case.get('failure_id')} status mismatch")
        forbidden_status = case.get("forbidden_status")
        if forbidden_status:
            add_failure(failures, parsed.get("status") != forbidden_status, f"{case.get('failure_id')} returned forbidden status")
        for error in case.get("expected_errors_contains", []):
            add_failure(failures, error in parsed.get("errors", []), f"{case.get('failure_id')} missing error {error}")
        add_failure(failures, HARD_NO_REQUIRED <= set(case.get("hard_no", [])), f"{case.get('failure_id')} hard_no incomplete")
    return len(cases)


def final_status(path: Path) -> str | None:
    parsed = parse_status(read_text(path))
    return parsed.get("status") if parsed.get("valid") else None


def validate_final_reports(failures: list[str]) -> None:
    add_failure(failures, final_status(ROOT / "verification.md") == "local_verification_passed", "verification status not passed")
    add_failure(failures, final_status(ROOT / "reviewer-report.md") == "review_pass_no_blocker", "Reviewer report status not passed")
    add_failure(failures, final_status(ROOT / "boundary-audit.md") == "pass_boundary", "Boundary audit status not passed")
    add_failure(failures, final_status(ROOT / "product-acceptance-report.md") == "pass_product_grade", "Product report status not passed")
    add_failure(failures, final_status(ROOT / "next-step.md") == "pass_product_grade_pending_next_slice", "next-step status not passed")


def verify(final_gate: bool = False) -> dict:
    failures: list[str] = []
    fixtures, failure_files = validate_files(failures)
    contract_path = ARTIFACT / "frontmatter_status_hardening_contract.json"
    contract = load_json(contract_path) if contract_path.exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    payload = load_json(OUTPUT_JSON) if OUTPUT_JSON.exists() else {}
    builder = import_builder()
    current = builder.build_hardening()
    if isinstance(payload, dict):
        validate_payload(payload, current, failures, "payload")
    else:
        failures.append("payload is not object")
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
            "frontmatter_status_hardening_ready": payload.get("frontmatter_status_hardening_ready"),
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
