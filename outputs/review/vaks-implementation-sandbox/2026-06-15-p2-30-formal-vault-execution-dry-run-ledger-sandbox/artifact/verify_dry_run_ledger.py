from __future__ import annotations

import argparse
import json
import subprocess
import sys

from dry_run_ledger_common import (
    ROOT,
    SLICE_ID,
    SOURCE_SLICE,
    check_required_reports,
    inspect_prototype,
    read_json_path,
    validate_config,
    validate_failure_cases,
)


def maybe_rebuild() -> None:
    script = ROOT / "artifact" / "build_dry_run_ledger.py"
    subprocess.run([sys.executable, "-B", str(script), "--rebuild"], check=True)


def run(final_gate: bool = False, rebuild: bool = False) -> dict:
    if rebuild:
        maybe_rebuild()
    failures = []
    fixtures = []
    for fixture_path in sorted((ROOT / "fixtures").glob("valid-*.json")):
        config = read_json_path(fixture_path)
        errors = validate_config(config)
        fixtures.append({"file": fixture_path.name, "errors": errors})
        if errors:
            failures.append(f"positive_fixture_failed:{fixture_path.name}")
    failure_cases = validate_failure_cases()
    oracle = read_json_path(ROOT / "artifact" / "failure-case-oracle.json")
    if failure_cases["mismatches"]:
        failures.append("failure_case_mismatches")
    if failure_cases["count"] != oracle.get("case_count"):
        failures.append("failure_case_count_not_oracle_locked")
    if failure_cases["count"] < 100:
        failures.append("insufficient_failure_cases")
    prototype = inspect_prototype()
    if prototype["issues"]:
        failures.append("prototype_issues")
    required_reports = check_required_reports(final_gate=final_gate)
    if required_reports["issues"]:
        failures.append("required_report_issues")
    return {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE,
        "rebuild": rebuild,
        "final_gate": final_gate,
        "passed": not failures,
        "failures": failures,
        "positive_fixtures": fixtures,
        "failure_cases": failure_cases,
        "prototype": prototype,
        "required_reports": required_reports,
        "non_claims": [
            "sandbox verification only",
            "not actual approval",
            "not execution readiness",
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "not mainline approval",
            "not formal vault approval",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = run(final_gate=args.final_gate, rebuild=args.rebuild)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
