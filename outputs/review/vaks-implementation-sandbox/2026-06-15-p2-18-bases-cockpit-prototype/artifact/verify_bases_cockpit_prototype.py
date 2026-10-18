#!/usr/bin/env python3
"""Run the P2-18 Bases cockpit prototype verification suite."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import bases_cockpit_validator as cockpit


sys.dont_write_bytecode = True

SANDBOX_ROOT = Path(__file__).resolve().parents[1]
ORACLE_PATH = SANDBOX_ROOT / "artifact" / "failure-case-oracle.json"


def codes(result: dict) -> list[str]:
    return sorted({issue["code"] for issue in result["issues"]})


def load_oracle() -> dict[str, dict]:
    with ORACLE_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("failure-case oracle must be an object")
    return data


def run_case(path: Path, oracle: dict[str, dict]) -> dict:
    manifest = cockpit.load_manifest(path)
    result = cockpit.validate_manifest(manifest)
    rel_path = str(path.relative_to(SANDBOX_ROOT)).replace("\\", "/")
    expectations = oracle.get(rel_path)
    problems: list[str] = []
    if expectations is None:
        problems.append(f"missing oracle entry for {rel_path}")
        expectations = {}
    expected_valid = bool(expectations.get("expected_valid", True))
    expected_codes = sorted(expectations.get("expected_codes", []))
    allowed_extra = sorted(expectations.get("allowed_extra_codes", []))
    issue_codes = codes(result)
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
    oracle = load_oracle()
    positives = sorted((SANDBOX_ROOT / "fixtures").glob("valid-*.json"))
    prototypes = sorted((SANDBOX_ROOT / "prototype").glob("*.json"))
    failures = sorted((SANDBOX_ROOT / "failure-cases").glob("*.json"))
    results = [run_case(path, oracle) for path in positives + prototypes + failures]
    problems = [problem for result in results for problem in result["problems"]]
    if not prototypes:
        problems.append("no prototype artifacts found")
    expected_paths = {str(path.relative_to(SANDBOX_ROOT)).replace("\\", "/") for path in positives + prototypes + failures}
    extra_oracle = sorted(set(oracle) - expected_paths)
    if extra_oracle:
        problems.append(f"oracle entries without files: {extra_oracle}")
    summary = {
        "slice_id": "2026-06-15-p2-18-bases-cockpit-prototype",
        "positive_fixtures": len(positives),
        "prototype_artifacts": len(prototypes),
        "failure_cases": len(failures),
        "passed": not problems,
        "failures": problems,
        "non_claims": {
            "suite_pass_not_real_bases": True,
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
