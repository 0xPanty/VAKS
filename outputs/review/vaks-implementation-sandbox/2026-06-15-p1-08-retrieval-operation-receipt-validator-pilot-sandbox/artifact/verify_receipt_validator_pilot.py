#!/usr/bin/env python3
"""
Suite runner for the P1-08 receipt validator pilot.

It checks all positive fixtures and all failure cases against the expected
frontmatter codes. The runner is read-only and writes no cache files.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "artifact" / "receipt_validator_pilot.py"
FIXTURES = ROOT / "fixtures"
FAILURES = ROOT / "failure-cases"


def load_validator():
    spec = importlib.util.spec_from_file_location("receipt_validator_pilot", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator from {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["receipt_validator_pilot"] = module
    spec.loader.exec_module(module)
    return module


def check_file(path: Path, validator) -> dict[str, object]:
    record, issues = validator.validate_path(path)
    expected_valid = validator.as_bool(record.get("expected_valid"))
    expected_codes = {code.upper() for code in validator.as_list(record.get("expected_codes"))}
    issue_codes = {issue.code for issue in issues}

    problems: list[str] = []
    if expected_valid and issues:
        problems.append("expected valid but validator returned issues")
    if not expected_valid and not issues:
        problems.append("expected invalid but validator returned no issues")
    missing_codes = sorted(expected_codes.difference(issue_codes))
    if missing_codes:
        problems.append(f"missing expected issue codes: {missing_codes}")

    return {
        "path": str(path.relative_to(ROOT)),
        "expected_valid": expected_valid,
        "valid": not issues,
        "expected_codes": sorted(expected_codes),
        "issue_codes": sorted(issue_codes),
        "problems": problems,
    }


def main() -> int:
    validator = load_validator()
    positive_paths = sorted(FIXTURES.glob("*.md"))
    failure_paths = sorted(FAILURES.glob("*.md"))

    results = [check_file(path, validator) for path in positive_paths + failure_paths]
    failures = [result for result in results if result["problems"]]
    summary = {
        "slice_id": "2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox",
        "positive_fixtures": len(positive_paths),
        "failure_cases": len(failure_paths),
        "passed": not failures,
        "failures": failures,
        "results": results,
        "authority_non_claims": {
            "suite_pass_not_reviewer_approval": True,
            "suite_pass_not_evidence_support": True,
            "suite_pass_not_reviewed_knowledge": True,
            "suite_pass_not_action_basis": True,
            "suite_pass_not_mainline_readiness": True,
        },
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
