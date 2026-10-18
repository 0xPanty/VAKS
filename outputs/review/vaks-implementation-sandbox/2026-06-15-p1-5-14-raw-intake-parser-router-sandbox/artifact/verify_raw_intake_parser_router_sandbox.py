#!/usr/bin/env python3
"""
Suite runner for the P1.5-14 raw intake parser router sandbox.

It validates positive JSON fixtures and failure-case JSON manifests against
expected validity and required issue codes. It is read-only and writes no
durable files.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
CHECK_PATH = ROOT / "artifact" / "raw_intake_parser_router_sandbox.py"
FIXTURES = ROOT / "fixtures"
FAILURES = ROOT / "failure-cases"


def load_check_module():
    spec = importlib.util.spec_from_file_location("raw_intake_parser_router_sandbox", CHECK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load raw intake parser router module from {CHECK_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["raw_intake_parser_router_sandbox"] = module
    spec.loader.exec_module(module)
    return module


def check_file(path: Path, module) -> dict[str, object]:
    manifest = module.load_manifest(path)
    issues = module.validate_manifest(manifest)
    result = module.summarize(manifest, issues)
    expected_valid = module.as_bool(manifest.get("expected_valid"))
    expected_codes = {code.upper() for code in module.as_list(manifest.get("expected_codes"))}
    issue_codes = set(result["issue_codes"])

    problems: list[str] = []
    if expected_valid and not result["valid"]:
        problems.append("expected valid but manifest was blocked")
    if not expected_valid and result["valid"]:
        problems.append("expected invalid but manifest was valid")
    missing_codes = sorted(expected_codes.difference(issue_codes))
    if missing_codes:
        problems.append(f"missing expected issue codes: {missing_codes}")

    return {
        "path": str(path.relative_to(ROOT)),
        "expected_valid": expected_valid,
        "valid": result["valid"],
        "expected_codes": sorted(expected_codes),
        "issue_codes": sorted(issue_codes),
        "problems": problems,
    }


def main() -> int:
    module = load_check_module()
    positive_paths = sorted(FIXTURES.glob("*.json"))
    failure_paths = sorted(FAILURES.glob("*.json"))
    results = [check_file(path, module) for path in positive_paths + failure_paths]
    failures = [result for result in results if result["problems"]]
    summary = {
        "slice_id": "2026-06-15-p1-5-14-raw-intake-parser-router-sandbox",
        "positive_fixtures": len(positive_paths),
        "failure_cases": len(failure_paths),
        "passed": not failures,
        "failures": failures,
        "results": results,
        "raw_parser_router_non_claims": {
            "suite_pass_not_reviewed_knowledge": True,
            "suite_pass_not_evidence_support": True,
            "suite_pass_not_action_basis": True,
            "suite_pass_not_promotion": True,
            "suite_pass_not_mainline_readiness": True,
            "suite_pass_not_dependency_install_permission": True,
        },
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
