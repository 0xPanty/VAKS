from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import build_operator_launch_checklist as builder


SLICE_ID = builder.SLICE_ID


def slice_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_fixture_dir(root: Path) -> dict:
    result = {"count": 0, "fixtures": [], "errors": []}
    for path in sorted((root / "fixtures").glob("*.json")):
        data = load_json(path)
        errors = builder.validate_config(data)
        result["fixtures"].append({"file": path.name, "errors": errors})
        result["count"] += 1
        if errors:
            result["errors"].append({"file": path.name, "errors": errors})
    if result["count"] != 3:
        result["errors"].append({"file": "fixtures", "errors": [f"fixture_count_{result['count']}"]})
    return result


def check_failure_cases(root: Path) -> dict:
    oracle_path = root / "artifact" / "failure-case-oracle.json"
    oracle = load_json(oracle_path)
    actual = {}
    mismatches = []
    for path in sorted((root / "failure-cases").glob("*.json")):
        data = load_json(path)
        actual[path.name] = builder.validate_config(data)
    for filename, expected in oracle.items():
        if actual.get(filename) != expected:
            mismatches.append({"file": filename, "expected": expected, "actual": actual.get(filename)})
    orphan = sorted(set(actual) - set(oracle))
    return {
        "count": len(oracle),
        "actual_file_count": len(actual),
        "orphan_count": len(orphan),
        "mismatches": mismatches,
    }


def check_required_text(path: Path, required: list[str]) -> list[str]:
    if not path.exists():
        return [f"missing_{path.name}"]
    text = path.read_text(encoding="utf-8")
    return [f"missing_text_{item}" for item in required if item not in text]


def check_prototype(root: Path) -> dict:
    base = root / "prototype" / "operator-launch-checklist"
    issues = []
    for name in ["receipt.json", "index.html", "style.css", "app.js"]:
        if not (base / name).exists():
            issues.append(f"missing_{name}")
    if (base / "receipt.json").exists():
        receipt = load_json(base / "receipt.json")
        if receipt.get("source_slice_count") != 5:
            issues.append("receipt_source_slice_count")
        if receipt.get("launch_step_count") != 8:
            issues.append("receipt_launch_step_count")
    return {"prototype_path": str(base), "issues": issues}


def check_reports(root: Path, final_gate: bool) -> dict:
    expected = {
        "slice-plan.md": "built_pending_review",
        "source-map.md": "built_pending_review",
        "verification.md": "local_verification_passed_pending_review",
        "reviewer-report.md": "reviewer_pass",
        "boundary-audit.md": "boundary_pass",
        "product-acceptance-report.md": "pass_product_grade",
        "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
    }
    statuses = {}
    issues = []
    for filename, required_status in expected.items():
        path = root / filename
        status = builder.frontmatter_status(path)
        statuses[filename] = status
        if final_gate and status != required_status:
            issues.append(f"{filename}_status_{status}_expected_{required_status}")
        elif not final_gate and status is None:
            issues.append(f"{filename}_missing_status")
    return {"statuses": statuses, "issues": issues}


def run_freeze_final_gate() -> dict:
    root = builder.repo_root()
    command = [
        sys.executable,
        "-B",
        str(root / "outputs" / "review" / "vaks-implementation-sandbox" / "2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox" / "artifact" / "verify_freeze_bundle.py"),
        "--final-gate",
    ]
    completed = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    parsed = None
    if completed.stdout.strip().startswith("{"):
        parsed = json.loads(completed.stdout)
    return {
        "returncode": completed.returncode,
        "parsed": parsed,
        "stderr": completed.stderr.strip(),
    }


def verify(final_gate: bool, run_upstream_freeze: bool) -> dict:
    root = slice_root()
    artifact_path = root / "artifact" / "operator-launch-checklist.json"
    data = load_json(artifact_path)
    config_errors = builder.validate_config(data)
    fixture_result = check_fixture_dir(root)
    failure_result = check_failure_cases(root)
    prototype_result = check_prototype(root)
    readout_issues = check_required_text(
        root / "readouts" / "operator-launch-checklist.md",
        ["Run the p2-48 freeze final gate", "drift-sensitive diagnostic context", "not mainline", "not action basis", "Stop Immediately If"],
    )
    contract_issues = check_required_text(
        root / "artifact" / "operator-launch-checklist-contract.md",
        ["verify_freeze_bundle.py --final-gate", "drift-sensitive", "not re-acceptance", "Builder-only rebuild command"],
    )
    oracle_doc_issues = check_required_text(
        root / "artifact" / "failure-case-oracle.md",
        ["Failure Case Oracle", "top_level_record_kind", "operation_auto_advance_not_false"],
    )
    reports = check_reports(root, final_gate)
    upstream_freeze = run_freeze_final_gate() if run_upstream_freeze else {"skipped": True}
    upstream_errors = []
    if run_upstream_freeze:
        if upstream_freeze["returncode"] != 0:
            upstream_errors.append("upstream_freeze_returncode")
        parsed = upstream_freeze.get("parsed") or {}
        if parsed.get("passed") is not True:
            upstream_errors.append("upstream_freeze_not_passed")
        summary = parsed.get("summary") or {}
        if summary.get("missing_file_count") != 0:
            upstream_errors.append("upstream_freeze_missing_files")
        if summary.get("report_status_mismatch_count") != 0:
            upstream_errors.append("upstream_freeze_status_mismatch")

    failures = []
    failures.extend(config_errors)
    failures.extend(fixture_result["errors"])
    if failure_result["mismatches"] or failure_result["orphan_count"] != 0:
        failures.append("failure_case_oracle_mismatch")
    failures.extend(prototype_result["issues"])
    failures.extend(readout_issues)
    failures.extend(contract_issues)
    failures.extend(oracle_doc_issues)
    failures.extend(reports["issues"])
    failures.extend(upstream_errors)

    return {
        "slice_id": SLICE_ID,
        "passed": not failures,
        "failures": failures,
        "config_errors": config_errors,
        "positive_fixtures": fixture_result,
        "failure_cases": failure_result,
        "prototype": prototype_result,
        "readout_issues": readout_issues,
        "contract_issues": contract_issues,
        "oracle_doc_issues": oracle_doc_issues,
        "required_reports": reports,
        "upstream_freeze": upstream_freeze,
        "summary": {
            "source_slice_count": len(data.get("source_chain", [])),
            "launch_step_count": len(data.get("launch_sequence", [])),
            "failure_case_count": failure_result["count"],
            "positive_fixture_count": fixture_result["count"],
            "run_upstream_freeze": run_upstream_freeze,
        },
        "non_claims": builder.REQUIRED_NON_CLAIMS,
        "final_gate": final_gate,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true", help="Builder-only: regenerate current-slice artifacts.")
    parser.add_argument("--final-gate", action="store_true", help="Require review reports to be written.")
    parser.add_argument("--run-upstream-freeze", action="store_true", help="Read-only: run p2-48 freeze final gate.")
    args = parser.parse_args()
    if args.rebuild:
        builder.rebuild()
    run_upstream_freeze = args.run_upstream_freeze or args.final_gate
    result = verify(final_gate=args.final_gate, run_upstream_freeze=run_upstream_freeze)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
