#!/usr/bin/env python3
"""
Suite runner for the P1-09 read-only query loop pilot.

It validates positive fixtures and failure cases against expected outcome and
issue codes. It is read-only and writes no durable files.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
PILOT_PATH = ROOT / "artifact" / "read_only_query_loop_pilot.py"
FIXTURES = ROOT / "fixtures"
FAILURES = ROOT / "failure-cases"


def load_pilot():
    spec = importlib.util.spec_from_file_location("read_only_query_loop_pilot", PILOT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load pilot from {PILOT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["read_only_query_loop_pilot"] = module
    spec.loader.exec_module(module)
    return module


def check_file(path: Path, pilot, receipt_validator) -> dict[str, object]:
    scenario = pilot.load_scenario(path)
    result = pilot.run_scenario(scenario, receipt_validator=receipt_validator)
    expected_valid = pilot.as_bool(scenario.get("expected_valid"))
    expected_outcome = pilot.norm(scenario.get("expected_outcome"))
    expected_codes = {code.upper() for code in pilot.as_list(scenario.get("expected_codes"))}
    issue_codes = set(result["issue_codes"])

    problems: list[str] = []
    if expected_valid and not result["valid"]:
        problems.append("expected valid but scenario was blocked")
    if not expected_valid and result["valid"]:
        problems.append("expected invalid but scenario was valid")
    if expected_outcome and pilot.norm(result["outcome"]) != expected_outcome:
        problems.append(
            f"expected outcome {expected_outcome!r} but got {result['outcome']!r}"
        )
    missing_codes = sorted(expected_codes.difference(issue_codes))
    if missing_codes:
        problems.append(f"missing expected issue codes: {missing_codes}")

    return {
        "path": str(path.relative_to(ROOT)),
        "expected_valid": expected_valid,
        "valid": result["valid"],
        "expected_outcome": expected_outcome,
        "outcome": result["outcome"],
        "expected_codes": sorted(expected_codes),
        "issue_codes": sorted(issue_codes),
        "problems": problems,
    }


def main() -> int:
    pilot = load_pilot()
    receipt_validator = pilot.load_receipt_validator()
    positive_paths = sorted(FIXTURES.glob("*.md"))
    failure_paths = sorted(FAILURES.glob("*.md"))
    results = [
        check_file(path, pilot, receipt_validator)
        for path in positive_paths + failure_paths
    ]
    failures = [result for result in results if result["problems"]]
    summary = {
        "slice_id": "2026-06-15-p1-09-read-only-query-loop-pilot-sandbox",
        "positive_fixtures": len(positive_paths),
        "failure_cases": len(failure_paths),
        "passed": not failures,
        "failures": failures,
        "results": results,
        "query_loop_non_claims": {
            "suite_pass_not_reviewer_approval": True,
            "suite_pass_not_evidence_support": True,
            "suite_pass_not_action_basis": True,
            "suite_pass_not_reviewed_knowledge": True,
            "suite_pass_not_mainline_readiness": True,
        },
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
