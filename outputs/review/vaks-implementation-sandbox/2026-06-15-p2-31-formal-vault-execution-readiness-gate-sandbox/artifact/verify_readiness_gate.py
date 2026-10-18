from __future__ import annotations

import argparse
import json
import subprocess
import sys

from readiness_gate_common import (
    ROOT,
    SLICE_ID,
    SOURCE_SLICE,
    check_required_reports,
    inspect_prototype,
    read_json_path,
    run_manual_negative_probes,
    validate_config,
    validate_failure_cases,
)


def maybe_rebuild() -> None:
    script = ROOT / "artifact" / "build_readiness_gate.py"
    subprocess.run([sys.executable, "-B", str(script)], check=True)


def run(final_gate: bool = False, rebuild: bool = False) -> dict:
    if rebuild:
        maybe_rebuild()
    fixtures = []
    failures = []
    for path in sorted((ROOT / "fixtures").glob("*.json")):
        errors = validate_config(read_json_path(path))
        fixtures.append({"file": path.name, "errors": errors})
        if errors:
            failures.append(f"fixture_failed:{path.name}")
    failure_cases = validate_failure_cases()
    if failure_cases["mismatches"]:
        failures.append("failure_case_mismatches")
    prototype = inspect_prototype()
    if prototype["issues"]:
        failures.append("prototype_issues")
    manual_probes = run_manual_negative_probes()
    if manual_probes["mismatches"]:
        failures.append("manual_negative_probe_mismatches")
    reports = check_required_reports(final_gate=final_gate)
    if reports["issues"]:
        failures.append("required_report_issues")
    result = {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE,
        "rebuild": rebuild,
        "final_gate": final_gate,
        "passed": not failures,
        "failures": failures,
        "positive_fixtures": fixtures,
        "failure_cases": failure_cases,
        "manual_negative_probes": manual_probes,
        "prototype": prototype,
        "required_reports": reports,
        "non_claims": [
            "sandbox verification only",
            "not actual approval",
            "not execution permission",
            "not execution readiness",
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "not mainline approval",
            "not formal vault approval",
        ],
    }
    return result


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
