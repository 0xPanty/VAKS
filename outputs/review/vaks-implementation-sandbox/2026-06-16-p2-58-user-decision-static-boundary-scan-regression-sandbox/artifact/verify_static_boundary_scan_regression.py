from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-57-user-decision-chain-regression-bundle-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"

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
    "static_boundary_scan_regression.py",
    "verify_static_boundary_scan_regression.py",
    "build_static_boundary_scan_regression_readout.py",
    "static_boundary_scan_regression_contract.json",
    "static_boundary_scan_regression_readout.md",
    "static_boundary_scan_regression_prototype.html",
]

MUST_NOT_REQUIRED = {
    "execute_option",
    "merge_mainline",
    "promote",
    "sync_obsidian",
    "commit",
    "push",
    "write_reviewed_knowledge",
    "create_evidence_support",
    "create_action_basis",
    "start_future_slice_by_inference",
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def import_scanner():
    path = ARTIFACT / "static_boundary_scan_regression.py"
    spec = importlib.util.spec_from_file_location("p2_58_scanner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scanner")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def frontmatter_status(path: Path) -> str:
    for line in read_text(path).splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def validate_files(failures: list[str]) -> tuple[list[Path], list[Path]]:
    for filename in REQUIRED_ROOT:
        add_failure(failures, (ROOT / filename).exists(), f"missing root file: {filename}")
    for filename in REQUIRED_ARTIFACT:
        add_failure(failures, (ARTIFACT / filename).exists(), f"missing artifact file: {filename}")
    fixture_files = sorted(FIXTURES.glob("*.json"))
    failure_files = sorted(FAILURE_CASES.glob("*.json"))
    add_failure(failures, len(fixture_files) >= 3, "expected at least 3 positive fixtures")
    add_failure(failures, len(failure_files) >= 1, "expected failure cases")
    return fixture_files, failure_files


def validate_contract(contract: dict, failures: list[str]) -> None:
    add_failure(failures, contract.get("record_kind") == "sandbox_static_boundary_scan_regression_contract", "wrong record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong slice_id")
    add_failure(failures, contract.get("source_slice_id") == SOURCE_SLICE_ID, "wrong source_slice_id")
    add_failure(
        failures,
        contract.get("truth_boundary") == "static_scan_regression_not_general_security_or_execution_authority",
        "wrong truth boundary",
    )
    gate = contract.get("source_final_gate_command", "")
    add_failure(failures, SOURCE_SLICE_ID in gate and "--final-gate" in gate, "source final gate incomplete")
    output = contract.get("output_contract", {})
    for flag in ["automatic_execution", "mainline_ready", "promotion_ready", "action_basis_ready"]:
        add_failure(failures, output.get(flag) is False, f"contract {flag} not false")
    add_failure(failures, MUST_NOT_REQUIRED <= set(output.get("must_not", [])), "contract must_not incomplete")
    add_failure(failures, len(contract.get("live_positive_sources", [])) >= 2, "live positive source coverage too small")
    limits = "\n".join(contract.get("scanner_limits", []))
    for phrase in ["not a general security sandbox", "not execution authority", "not mainline approval"]:
        add_failure(failures, phrase in limits, f"missing scanner limit: {phrase}")


def validate_positive_fixtures(fixture_files: list[Path], scanner, failures: list[str]) -> int:
    seen = set()
    for path in fixture_files:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"{path.name} is not object")
            continue
        fixture_id = fixture.get("fixture_id")
        seen.add(str(fixture_id))
        source = fixture.get("source", "")
        allowed = fixture.get("allowed_write_lines", [])
        issues = scanner.scan_python_source(source, allowed_write_lines=allowed)
        add_failure(failures, issues == fixture.get("expected_issues", []), f"{path.name} issues mismatch: {issues}")
    for required in ["safe_reader", "safe_allowed_builder", "safe_subprocess_final_gate"]:
        add_failure(failures, required in seen, f"missing positive fixture {required}")
    return len(fixture_files)


def validate_failure_cases(failure_files: list[Path], scanner, failures: list[str]) -> int:
    cases: list[dict] = []
    for path in failure_files:
        payload = load_json(path)
        if isinstance(payload, list):
            cases.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            cases.append(payload)
    add_failure(failures, len(cases) >= 22, "expected at least 22 failure cases")
    ids = [item.get("failure_id") for item in cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure ids not unique")
    joined = "\n".join(str(item) for item in cases)
    for token in [
        "git_push",
        "git_commit",
        "pip_install",
        "npm_install",
        "pnpm_add",
        "yarn_add",
        "shell_true",
        "start_process",
        "register_scheduled_task",
        "new_service",
        "schtasks",
        "mcp_write",
        "hook_installed",
        "unauthorized_write_text",
        "write_mode_open",
        "unauthorized_write_bytes",
        "dynamic-variable",
        "path-open",
        "read-write-mode",
        "annassign-dynamic",
        "remove_item",
    ]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for item in cases:
        source = item.get("source", "")
        expected_issue = item.get("expected_issue_id")
        allowed = item.get("allowed_write_lines", [])
        issues = scanner.scan_python_source(source, allowed_write_lines=allowed)
        issue_ids = {issue.get("issue_id") for issue in issues}
        add_failure(failures, expected_issue in issue_ids, f"{item.get('failure_id')} did not produce {expected_issue}: {issues}")
        add_failure(failures, MUST_NOT_REQUIRED <= set(item.get("must_not", [])), f"{item.get('failure_id')} must_not incomplete")
    missing = scanner.scan_live_source("outputs/review/vaks-implementation-sandbox/__missing_static_scan_source__.py")
    add_failure(failures, missing.get("exists") is False, "missing live source was not reported as exists:false")
    add_failure(
        failures,
        any(issue.get("issue_id") == "source_missing" for issue in missing.get("issues", [])),
        "missing live source lacks source_missing issue",
    )
    return len(cases)


def run_source_gate() -> tuple[bool, dict | None, str]:
    script = (
        WORKSPACE
        / "outputs"
        / "review"
        / "vaks-implementation-sandbox"
        / SOURCE_SLICE_ID
        / "artifact"
        / "verify_user_decision_chain_regression_bundle.py"
    )
    result = subprocess.run(
        [sys.executable, "-B", str(script), "--final-gate"],
        cwd=str(WORKSPACE),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return False, None, result.stderr or result.stdout
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return False, None, f"source gate output is not JSON: {exc}"
    return payload.get("passed") is True, payload, ""


def validate_final_reports(failures: list[str]) -> None:
    add_failure(failures, frontmatter_status(ROOT / "verification.md") == "local_verification_passed", "verification status not passed")
    add_failure(failures, "REVIEW_PASS_NO_BLOCKER" in read_text(ROOT / "reviewer-report.md"), "Reviewer report lacks REVIEW_PASS_NO_BLOCKER")
    add_failure(failures, "PASS_BOUNDARY" in read_text(ROOT / "boundary-audit.md"), "Boundary audit lacks PASS_BOUNDARY")
    add_failure(failures, "PASS_PRODUCT_GRADE" in read_text(ROOT / "product-acceptance-report.md"), "Product report lacks PASS_PRODUCT_GRADE")
    add_failure(failures, frontmatter_status(ROOT / "next-step.md") == "pass_product_grade_pending_next_slice", "next-step status not passed")


def verify(final_gate: bool = False) -> dict:
    failures: list[str] = []
    fixture_files, failure_files = validate_files(failures)
    contract_path = ARTIFACT / "static_boundary_scan_regression_contract.json"
    contract = load_json(contract_path) if contract_path.exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    scanner = import_scanner()
    result = scanner.run_regression()
    add_failure(failures, result.get("record_kind") == "sandbox_static_boundary_scan_regression_result", "wrong result record_kind")
    add_failure(failures, all(not item["issues"] for item in result.get("positive_results", [])), f"live positive sources had issues: {result.get('positive_results')}")
    add_failure(failures, MUST_NOT_REQUIRED <= set(result.get("must_not", [])), "result must_not incomplete")
    fixture_count = validate_positive_fixtures(fixture_files, scanner, failures)
    failure_case_count = validate_failure_cases(failure_files, scanner, failures)
    source_payload = None
    if final_gate:
        source_passed, source_payload, source_error = run_source_gate()
        add_failure(failures, source_passed, f"source p2-57 final gate failed: {source_error}")
        validate_final_reports(failures)
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": fixture_count,
            "failure_case_count": failure_case_count,
            "live_positive_source_count": len(result.get("positive_results", [])),
            "source_p2_57_final_gate_passed": source_payload.get("passed") if isinstance(source_payload, dict) else None,
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
