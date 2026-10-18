from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
CONTRACT_PATH = ROOT / "artifact" / "user_decision_chain_regression_contract.json"
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
P2_56_SLICE_ID = "2026-06-16-p2-56-user-decision-demo-transcript-smoke-runner-sandbox"
P2_56_RUNNER = SANDBOX_ROOT / P2_56_SLICE_ID / "artifact" / "run_user_decision_demo_transcript.py"
P2_56_VERIFIER = SANDBOX_ROOT / P2_56_SLICE_ID / "artifact" / "verify_user_decision_demo_transcript_smoke_runner.py"


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


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise TypeError(f"{path} is not a JSON object")
    return payload


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def contains_token(path: Path, token: str) -> bool:
    return token in read_text(path)


def reviewer_pass(path: Path) -> bool:
    text = read_text(path)
    return (
        "REVIEW_PASS_NO_BLOCKER" in text
        or "REVIEW_PASS" in text
        or "PASS_REVIEWER" in text
        or "status: reviewer_pass" in text
    )


def frontmatter_status(path: Path) -> str:
    for line in read_text(path).splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def import_p2_56_runner():
    spec = importlib.util.spec_from_file_location("p2_56_demo_runner", P2_56_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-56 demo runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_p2_56_final_gate() -> dict:
    result = subprocess.run(
        [sys.executable, "-B", str(P2_56_VERIFIER), "--final-gate"],
        cwd=str(WORKSPACE),
        text=True,
        capture_output=True,
        check=False,
    )
    payload: dict = {
        "passed": False,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    if result.stdout.strip():
        try:
            parsed = json.loads(result.stdout)
            if isinstance(parsed, dict):
                payload.update(parsed)
        except json.JSONDecodeError:
            payload["parse_error"] = "stdout_not_json"
    return payload


def collect_source_report(slice_id: str) -> dict:
    root = SANDBOX_ROOT / slice_id
    product_path = root / "product-acceptance-report.md"
    boundary_path = root / "boundary-audit.md"
    reviewer_path = root / "reviewer-report.md"
    verification_path = root / "verification.md"
    next_path = root / "next-step.md"
    return {
        "slice_id": slice_id,
        "root_exists": root.exists(),
        "product_pass": contains_token(product_path, "PASS_PRODUCT_GRADE"),
        "reviewer_pass": reviewer_pass(reviewer_path),
        "boundary_pass": contains_token(boundary_path, "PASS_BOUNDARY"),
        "verification_present": verification_path.exists(),
        "verification_status": frontmatter_status(verification_path),
        "next_step_present": next_path.exists(),
        "product_report": str(product_path.relative_to(WORKSPACE)),
        "boundary_audit": str(boundary_path.relative_to(WORKSPACE)),
        "reviewer_report": str(reviewer_path.relative_to(WORKSPACE)),
    }


def row_safe(row: dict) -> bool:
    return (
        row.get("automatic_execution") is False
        and row.get("decision_collected") is False
        and row.get("ready_to_execute") is False
        and MUST_NOT_REQUIRED <= set(row.get("must_not", []))
    )


def demo_safe(demo: dict) -> bool:
    rows = demo.get("rows", [])
    return (
        demo.get("automatic_execution") is False
        and demo.get("decision_collected") is False
        and demo.get("ready_to_execute") is False
        and demo.get("mainline_ready") is False
        and demo.get("promotion_ready") is False
        and demo.get("action_basis_ready") is False
        and MUST_NOT_REQUIRED <= set(demo.get("must_not", []))
        and isinstance(rows, list)
        and len(rows) >= 9
        and all(isinstance(row, dict) and row_safe(row) for row in rows)
    )


def render_readout(result: dict) -> str:
    lines = [
        "# User Decision Chain Regression Readout",
        "",
        "This bundle is a sandbox regression proof only. It is not a user decision, execution authority, mainline approval, promotion approval, Obsidian sync approval, reviewed knowledge, evidence support, or action basis.",
        "",
        "| Source slice | Product | Reviewer | Boundary | Verification |",
        "| --- | --- | --- | --- | --- |",
    ]
    for report in result["source_reports"]:
        lines.append(
            "| `{slice_id}` | {product} | {reviewer} | {boundary} | `{verification}` |".format(
                slice_id=report["slice_id"],
                product="PASS" if report["product_pass"] else "FAIL",
                reviewer="PASS" if report["reviewer_pass"] else "FAIL",
                boundary="PASS" if report["boundary_pass"] else "FAIL",
                verification=report["verification_status"],
            )
        )
    lines.extend(
        [
            "",
            "## Gate Summary",
            "",
            f"- p2-56 final gate passed: `{result['p2_56_final_gate_passed']}`",
            f"- p2-56 demo scenario count: `{result['demo_summary']['scenario_count']}`",
            f"- demo safe: `{result['demo_summary']['demo_safe']}`",
            f"- chain passed: `{result['chain_passed']}`",
            "",
            "## must_not",
            "",
        ]
    )
    lines.extend(f"- `{item}`" for item in result["must_not"])
    return "\n".join(lines)


def run_bundle() -> dict:
    contract = load_json(CONTRACT_PATH)
    source_slice_ids = list(contract["source_slice_ids"])
    source_reports = [collect_source_report(slice_id) for slice_id in source_slice_ids]
    p2_56_gate = run_p2_56_final_gate()
    p2_56_runner = import_p2_56_runner()
    demo_result = p2_56_runner.run_demo()
    source_all_pass = all(
        report["root_exists"]
        and report["product_pass"]
        and report["reviewer_pass"]
        and report["boundary_pass"]
        and report["verification_present"]
        and report["next_step_present"]
        for report in source_reports
    )
    safe_demo = demo_safe(demo_result)
    top_flags_false = True
    must_not = list(contract["output_contract"]["must_not"])
    result = {
        "record_kind": "sandbox_user_decision_chain_regression_result",
        "slice_id": contract["slice_id"],
        "source_slice_ids": source_slice_ids,
        "truth_boundary": "chain_regression_bundle_not_user_decision_or_execution_authority",
        "automatic_execution": False,
        "decision_collected": False,
        "ready_to_execute": False,
        "mainline_ready": False,
        "promotion_ready": False,
        "action_basis_ready": False,
        "source_reports": source_reports,
        "source_pass_counts": {
            "source_count": len(source_reports),
            "product_pass": sum(1 for report in source_reports if report["product_pass"]),
            "reviewer_pass": sum(1 for report in source_reports if report["reviewer_pass"]),
            "boundary_pass": sum(1 for report in source_reports if report["boundary_pass"]),
            "verification_present": sum(1 for report in source_reports if report["verification_present"]),
        },
        "p2_56_final_gate_passed": p2_56_gate.get("passed") is True,
        "p2_56_final_gate_summary": p2_56_gate.get("summary", {}),
        "demo_summary": {
            "scenario_count": demo_result.get("scenario_count"),
            "demo_safe": safe_demo,
            "automatic_execution": demo_result.get("automatic_execution"),
            "decision_collected": demo_result.get("decision_collected"),
            "ready_to_execute": demo_result.get("ready_to_execute"),
        },
        "demo_rows": demo_result.get("rows", []),
        "must_not": must_not,
        "chain_passed": source_all_pass
        and p2_56_gate.get("passed") is True
        and safe_demo
        and top_flags_false
        and MUST_NOT_REQUIRED <= set(must_not),
        "non_claims": contract["required_non_claims"],
    }
    result["readout_markdown"] = render_readout(result)
    return result


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()
    result = run_bundle()
    if args.markdown:
        print(result["readout_markdown"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["chain_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
