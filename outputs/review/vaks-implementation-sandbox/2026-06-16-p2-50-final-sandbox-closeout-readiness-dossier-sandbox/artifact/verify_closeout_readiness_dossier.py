from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import build_closeout_readiness_dossier as builder


SLICE_ID = builder.SLICE_ID


def slice_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_fixtures(root: Path) -> dict:
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
    oracle = load_json(root / "artifact" / "failure-case-oracle.json")
    actual = {}
    for path in sorted((root / "failure-cases").glob("*.json")):
        actual[path.name] = builder.validate_config(load_json(path))
    mismatches = []
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
    base = root / "prototype" / "final-closeout-readiness"
    issues = []
    for name in ["receipt.json", "index.html", "style.css", "app.js"]:
        if not (base / name).exists():
            issues.append(f"missing_{name}")
    if (base / "receipt.json").exists():
        receipt = load_json(base / "receipt.json")
        if receipt.get("source_slice_count") != 6:
            issues.append("receipt_source_slice_count")
        if receipt.get("request_category_count") != 5:
            issues.append("receipt_request_category_count")
    app_path = base / "app.js"
    if app_path.exists():
        text = app_path.read_text(encoding="utf-8")
        for token in ["Ready to ask", "Not ready to execute", "Stop Conditions", "Non-Claims"]:
            if token not in text:
                issues.append(f"prototype_missing_{token}")
    return {"prototype_path": str(base), "issues": issues}


def run_p2_49_final_gate() -> dict:
    root = builder.repo_root()
    cmd = [
        sys.executable,
        "-B",
        str(root / "outputs" / "review" / "vaks-implementation-sandbox" / "2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox" / "artifact" / "verify_operator_launch_checklist.py"),
        "--final-gate",
    ]
    completed = subprocess.run(cmd, cwd=root, text=True, capture_output=True, check=False)
    parsed = json.loads(completed.stdout) if completed.stdout.strip().startswith("{") else None
    return {"returncode": completed.returncode, "parsed": parsed, "stderr": completed.stderr.strip()}


def check_reports(root: Path, final_gate: bool) -> dict:
    expected = {
        "slice-plan.md": "built_pending_review",
        "source-map.md": "built_pending_review",
        "verification.md": "local_verification_passed_pending_review",
        "reviewer-report.md": "reviewer_pass",
        "boundary-audit.md": "boundary_pass",
        "product-acceptance-report.md": "pass_product_grade",
        "next-step.md": "pass_product_grade_pending_user_decision",
    }
    statuses = {}
    issues = []
    for filename, required in expected.items():
        status = builder.frontmatter_status(root / filename)
        statuses[filename] = status
        if final_gate and status != required:
            issues.append(f"{filename}_status_{status}_expected_{required}")
        elif not final_gate and status is None:
            issues.append(f"{filename}_missing_status")
    return {"statuses": statuses, "issues": issues}


def verify(final_gate: bool, run_upstream: bool) -> dict:
    root = slice_root()
    dossier = load_json(root / "artifact" / "final-sandbox-closeout-readiness-dossier.json")
    config_errors = builder.validate_config(dossier)
    fixtures = check_fixtures(root)
    failure_cases = check_failure_cases(root)
    prototype = check_prototype(root)
    readout_issues = check_required_text(
        root / "readouts" / "final-sandbox-closeout-readiness-dossier.md",
        ["ready to ask", "not approval to merge", "p2-47", "Required Upstream Gate"],
    )
    contract_issues = check_required_text(
        root / "artifact" / "closeout-readiness-contract.md",
        ["not release approval", "verify_operator_launch_checklist.py --final-gate", "Treat Product PASS as user approval"],
    )
    oracle_doc_issues = check_required_text(
        root / "artifact" / "failure-case-oracle.md",
        ["Failure Case Oracle", "top_level_record_kind", "readiness_action_basis_ready_not_false"],
    )
    reports = check_reports(root, final_gate)
    upstream = run_p2_49_final_gate() if run_upstream else {"skipped": True}
    upstream_errors = []
    if run_upstream:
        if upstream["returncode"] != 0:
            upstream_errors.append("p2_49_final_gate_returncode")
        parsed = upstream.get("parsed") or {}
        if parsed.get("passed") is not True:
            upstream_errors.append("p2_49_final_gate_not_passed")
        if (parsed.get("summary") or {}).get("run_upstream_freeze") is not True:
            upstream_errors.append("p2_49_did_not_run_upstream_freeze")

    failures = []
    failures.extend(config_errors)
    failures.extend(fixtures["errors"])
    if failure_cases["mismatches"] or failure_cases["orphan_count"] != 0:
        failures.append("failure_case_oracle_mismatch")
    failures.extend(prototype["issues"])
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
        "positive_fixtures": fixtures,
        "failure_cases": failure_cases,
        "prototype": prototype,
        "readout_issues": readout_issues,
        "contract_issues": contract_issues,
        "oracle_doc_issues": oracle_doc_issues,
        "required_reports": reports,
        "upstream_p2_49_final_gate": upstream,
        "summary": {
            "source_slice_count": len(dossier.get("source_chain", [])),
            "request_category_count": len(dossier.get("request_categories", [])),
            "failure_case_count": failure_cases["count"],
            "positive_fixture_count": fixtures["count"],
            "run_upstream_p2_49": run_upstream,
        },
        "non_claims": builder.REQUIRED_NON_CLAIMS,
        "final_gate": final_gate,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true", help="Builder-only: regenerate current-slice artifacts.")
    parser.add_argument("--run-upstream", action="store_true", help="Read-only: run p2-49 final gate.")
    parser.add_argument("--final-gate", action="store_true", help="Require review reports and run upstream p2-49 final gate.")
    args = parser.parse_args()
    if args.rebuild:
        builder.rebuild()
    run_upstream = args.run_upstream or args.final_gate
    result = verify(final_gate=args.final_gate, run_upstream=run_upstream)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
