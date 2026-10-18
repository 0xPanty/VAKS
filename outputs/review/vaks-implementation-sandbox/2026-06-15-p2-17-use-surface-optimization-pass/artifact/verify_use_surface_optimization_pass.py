#!/usr/bin/env python3
"""Run the P2-17 use-surface optimization sandbox verification suite."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import use_surface_optimizer as optimizer


sys.dont_write_bytecode = True

SANDBOX_ROOT = Path(__file__).resolve().parents[1]


def codes(result: dict) -> list[str]:
    return sorted({issue["code"] for issue in result["issues"]})


def run_case(path: Path) -> dict:
    manifest = optimizer.load_manifest(path)
    result = optimizer.validate_manifest(manifest)
    expected_valid = bool(manifest.get("expected_valid", True))
    expected_codes = sorted(manifest.get("expected_codes", []))
    allowed_extra = sorted(manifest.get("allowed_extra_codes", []))
    issue_codes = codes(result)
    problems: list[str] = []
    if result["valid"] != expected_valid:
        problems.append(f"valid expected {expected_valid} got {result['valid']}")
    missing = [code for code in expected_codes if code not in issue_codes]
    if missing:
        problems.append(f"missing expected codes: {missing}")
    unexpected = [code for code in issue_codes if code not in expected_codes and code not in allowed_extra]
    if unexpected:
        problems.append(f"unexpected codes: {unexpected}")
    return {
        "path": str(path.relative_to(SANDBOX_ROOT)),
        "expected_valid": expected_valid,
        "expected_codes": expected_codes,
        "allowed_extra_codes": allowed_extra,
        "valid": result["valid"],
        "issue_codes": issue_codes,
        "problems": problems,
    }


def main() -> int:
    positives = sorted((SANDBOX_ROOT / "fixtures").glob("valid-*.json"))
    prototypes = sorted((SANDBOX_ROOT / "prototype").glob("*.json"))
    failures = sorted((SANDBOX_ROOT / "failure-cases").glob("*.json"))
    results = [run_case(path) for path in positives + prototypes + failures]
    problems = [problem for result in results for problem in result["problems"]]
    summary = {
        "slice_id": "2026-06-15-p2-17-use-surface-optimization-pass",
        "positive_fixtures": len(positives),
        "prototype_artifacts": len(prototypes),
        "failure_cases": len(failures),
        "passed": not problems,
        "failures": problems,
        "non_claims": {
            "suite_pass_not_reviewed_knowledge": True,
            "suite_pass_not_evidence_support": True,
            "suite_pass_not_action_basis": True,
            "suite_pass_not_mainline_readiness": True,
        },
        "results": results,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
