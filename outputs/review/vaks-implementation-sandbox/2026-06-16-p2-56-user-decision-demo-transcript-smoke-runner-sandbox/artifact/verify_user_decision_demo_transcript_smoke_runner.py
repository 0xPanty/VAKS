from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-56-user-decision-demo-transcript-smoke-runner-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-55-user-decision-e2e-dry-run-simulator-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"

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

REQUIRED_ROOT = [
    "slice-plan.md",
    "source-map.md",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

REQUIRED_ARTIFACT = [
    "build_user_decision_demo_transcript_smoke_runner.py",
    "run_user_decision_demo_transcript.py",
    "verify_user_decision_demo_transcript_smoke_runner.py",
    "user_decision_demo_transcript_contract.json",
    "user_decision_demo_transcript_readout.md",
    "user_decision_demo_transcript_prototype.html",
]


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def import_runner():
    path = ARTIFACT / "run_user_decision_demo_transcript.py"
    spec = importlib.util.spec_from_file_location("p2_56_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load smoke runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frontmatter_status(path: Path) -> str:
    if not path.exists():
        return "missing"
    for line in read_text(path).splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def validate_files(failures: list[str]) -> tuple[list[Path], list[Path]]:
    for filename in REQUIRED_ROOT:
        add_failure(failures, (ROOT / filename).exists(), f"missing root file: {filename}")
    for filename in REQUIRED_ARTIFACT:
        add_failure(failures, (ARTIFACT / filename).exists(), f"missing artifact file: {filename}")
    fixture_files = sorted(FIXTURES.glob("*.json"))
    failure_files = sorted(FAILURE_CASES.glob("*.json"))
    add_failure(failures, len(fixture_files) >= 9, "expected at least 9 fixtures")
    add_failure(failures, len(failure_files) >= 1, "expected failure cases")
    return fixture_files, failure_files


def transcript_safe(result: dict, contract: dict) -> tuple[bool, list[str]]:
    reasons = []
    transcript = result.get("transcript_markdown", "")
    rules = contract.get("transcript_safety_rules", {})
    for phrase in rules.get("must_include_phrases", []):
        if phrase not in transcript:
            reasons.append(f"missing required phrase: {phrase}")
    for phrase in rules.get("dangerous_positive_phrases", []):
        if phrase in transcript:
            reasons.append(f"dangerous phrase present: {phrase}")
    return not reasons, reasons


def validate_contract(contract: dict, failures: list[str]) -> None:
    add_failure(failures, contract.get("record_kind") == "sandbox_user_decision_demo_transcript_smoke_runner_contract", "wrong record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong slice_id")
    add_failure(failures, contract.get("source_slice_id") == SOURCE_SLICE_ID, "wrong source_slice_id")
    add_failure(failures, contract.get("truth_boundary") == "demo_transcript_not_user_decision_or_execution_authority", "wrong truth boundary")
    source_gate = contract.get("source_final_gate_command", "")
    add_failure(failures, SOURCE_SLICE_ID in source_gate and "--final-gate" in source_gate, "source gate incomplete")
    output = contract.get("output_contract", {})
    for flag in [
        "automatic_execution",
        "decision_collected",
        "ready_to_execute",
        "mainline_ready",
        "promotion_ready",
        "action_basis_ready",
    ]:
        add_failure(failures, output.get(flag) is False, f"contract {flag} not false")
    add_failure(failures, MUST_NOT_REQUIRED <= set(output.get("must_not", [])), "contract must_not incomplete")
    usage = contract.get("ordinary_agent_usage", {})
    add_failure(failures, "Builder-only" in usage.get("rebuild", ""), "rebuild not Builder-only")
    add_failure(failures, "--run-upstream" in usage.get("upstream_verifier", ""), "upstream usage missing")
    add_failure(failures, "--final-gate" in usage.get("final_gate", ""), "final gate usage missing")
    non_claims = "\n".join(str(item) for item in contract.get("required_non_claims", []))
    for phrase in ["not a user decision", "not execution authority", "cannot approve merge", "demo of safe next replies", "must_not"]:
        add_failure(failures, phrase in non_claims, f"missing non-claim phrase: {phrase}")


def validate_demo_result(result: dict, contract: dict, failures: list[str], label: str) -> None:
    add_failure(failures, result.get("record_kind") == "sandbox_user_decision_demo_transcript_result", f"{label} wrong record_kind")
    add_failure(failures, result.get("truth_boundary") == "demo_transcript_not_user_decision_or_execution_authority", f"{label} wrong truth boundary")
    for flag in ["automatic_execution", "decision_collected", "ready_to_execute", "mainline_ready", "promotion_ready", "action_basis_ready"]:
        add_failure(failures, result.get(flag) is False, f"{label} {flag} not false")
    add_failure(failures, MUST_NOT_REQUIRED <= set(result.get("must_not", [])), f"{label} top-level must_not incomplete")
    safe, reasons = transcript_safe(result, contract)
    add_failure(failures, safe, f"{label} transcript unsafe: {reasons}")
    for row in result.get("rows", []):
        row_label = f"{label} row {row.get('scenario_id')}"
        for flag in ["automatic_execution", "decision_collected", "ready_to_execute"]:
            add_failure(failures, row.get(flag) is False, f"{row_label} {flag} not false")
        add_failure(failures, MUST_NOT_REQUIRED <= set(row.get("must_not", [])), f"{row_label} must_not incomplete")
        add_failure(failures, row.get("classifier_case_id") == row.get("expected_case_id"), f"{row_label} case mismatch")
        add_failure(failures, row.get("reply_id") == row.get("expected_reply_id"), f"{row_label} reply mismatch")


def validate_fixtures(fixture_files: list[Path], result: dict, failures: list[str]) -> int:
    by_id = {row.get("scenario_id"): row for row in result.get("rows", [])}
    seen = set()
    for path in fixture_files:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"{path.name} is not object")
            continue
        scenario_id = fixture.get("scenario_id")
        seen.add(str(scenario_id))
        row = by_id.get(scenario_id)
        add_failure(failures, isinstance(row, dict), f"{path.name} scenario missing from demo")
        if isinstance(row, dict):
            add_failure(failures, row.get("classifier_case_id") == fixture.get("expected_case_id"), f"{path.name} case mismatch")
            add_failure(failures, row.get("reply_id") == fixture.get("expected_reply_id"), f"{path.name} reply mismatch")
            add_failure(failures, row.get("automatic_execution") is False, f"{path.name} automatic_execution not false")
            add_failure(failures, row.get("decision_collected") is False, f"{path.name} decision_collected not false")
            add_failure(failures, row.get("ready_to_execute") is False, f"{path.name} ready_to_execute not false")
            add_failure(failures, MUST_NOT_REQUIRED <= set(row.get("must_not", [])), f"{path.name} row must_not incomplete")
    for required in ["no_reply", "option_a", "option_b", "option_c", "option_d", "ambiguous", "multiple", "execution_words", "unknown_fallback"]:
        add_failure(failures, required in seen, f"missing fixture for {required}")
    return len(fixture_files)


def apply_mutation(result: dict, mutation: dict) -> dict:
    mutated = json.loads(json.dumps(result, ensure_ascii=False))
    if mutation.get("transcript_append"):
        mutated["transcript_markdown"] += "\n" + mutation["transcript_append"]
    if mutation.get("remove_top_level_must_not"):
        mutated["must_not"] = []
    scenario_id = mutation.get("scenario_id")
    if scenario_id:
        for row in mutated.get("rows", []):
            if row.get("scenario_id") == scenario_id:
                if mutation.get("remove_scenario_must_not"):
                    row["must_not"] = [item for item in row.get("must_not", []) if item != mutation["remove_scenario_must_not"]]
                if "set_scenario_automatic_execution" in mutation:
                    row["automatic_execution"] = mutation["set_scenario_automatic_execution"]
                if "set_scenario_ready_to_execute" in mutation:
                    row["ready_to_execute"] = mutation["set_scenario_ready_to_execute"]
                if mutation.get("set_case_id"):
                    row["classifier_case_id"] = mutation["set_case_id"]
                if mutation.get("set_reply_id"):
                    row["reply_id"] = mutation["set_reply_id"]
    return mutated


def validate_failure_cases(failure_files: list[Path], result: dict, contract: dict, failures: list[str]) -> int:
    all_cases = []
    for path in failure_files:
        payload = load_json(path)
        if isinstance(payload, list):
            all_cases.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            all_cases.append(payload)
    add_failure(failures, len(all_cases) >= 10, "expected at least 10 failure cases")
    ids = [item.get("failure_id") for item in all_cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure ids not unique")
    joined = "\n".join(str(item) for item in all_cases)
    for token in ["execution", "merge", "must_not", "scenario", "case", "reply", "unknown", "upstream"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for item in all_cases:
        mutation = item.get("mutation")
        add_failure(failures, isinstance(mutation, dict) and bool(mutation), f"{item.get('failure_id')} lacks mutation")
        if isinstance(mutation, dict):
            if mutation.get("upstream_gate_required") is False:
                add_failure(failures, True, f"{item.get('failure_id')} covered by final gate upstream requirement")
                continue
            mutated = apply_mutation(result, mutation)
            local_failures = []
            validate_demo_result(mutated, contract, local_failures, "mutated")
            add_failure(failures, bool(local_failures), f"{item.get('failure_id')} mutation was not rejected")
    return len(all_cases)


def run_upstream_gate() -> tuple[bool, dict | None, str]:
    script = (
        WORKSPACE
        / "outputs"
        / "review"
        / "vaks-implementation-sandbox"
        / SOURCE_SLICE_ID
        / "artifact"
        / "verify_user_decision_e2e_simulator.py"
    )
    if not script.exists():
        return False, None, f"missing upstream verifier: {script}"
    result = subprocess.run(
        [sys.executable, "-B", str(script), "--final-gate"],
        cwd=str(WORKSPACE),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return False, None, result.stderr or result.stdout
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return False, None, f"upstream output is not JSON: {exc}"
    return payload.get("passed") is True, payload, ""


def validate_final_reports(failures: list[str]) -> None:
    add_failure(failures, frontmatter_status(ROOT / "verification.md") == "local_verification_passed", "verification status not passed")
    add_failure(failures, "REVIEW_PASS_NO_BLOCKER" in read_text(ROOT / "reviewer-report.md"), "Reviewer report lacks REVIEW_PASS_NO_BLOCKER")
    add_failure(failures, "PASS_BOUNDARY" in read_text(ROOT / "boundary-audit.md"), "Boundary audit lacks PASS_BOUNDARY")
    add_failure(failures, "PASS_PRODUCT_GRADE" in read_text(ROOT / "product-acceptance-report.md"), "Product report lacks PASS_PRODUCT_GRADE")
    add_failure(failures, frontmatter_status(ROOT / "next-step.md") == "pass_product_grade_pending_user_response", "next-step status not passed")


def verify(run_upstream: bool = False, final_gate: bool = False) -> dict:
    failures = []
    fixture_files, failure_files = validate_files(failures)
    contract_path = ARTIFACT / "user_decision_demo_transcript_contract.json"
    contract = load_json(contract_path) if contract_path.exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
        contract = {}
    runner = import_runner()
    result = runner.run_demo()
    validate_demo_result(result, contract, failures, "demo")
    fixture_count = validate_fixtures(fixture_files, result, failures)
    failure_case_count = validate_failure_cases(failure_files, result, contract, failures)

    upstream_payload = None
    if run_upstream or final_gate:
        upstream_passed, upstream_payload, upstream_error = run_upstream_gate()
        add_failure(failures, upstream_passed, f"upstream p2-55 final gate failed: {upstream_error}")
    if final_gate:
        validate_final_reports(failures)
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "scenario_count": result.get("scenario_count"),
            "fixture_count": fixture_count,
            "failure_case_count": failure_case_count,
            "run_upstream_p2_55": bool(run_upstream or final_gate),
            "upstream_p2_55_passed": upstream_payload.get("passed") if isinstance(upstream_payload, dict) else None,
            "final_gate": final_gate,
        },
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-upstream", action="store_true")
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = verify(run_upstream=args.run_upstream, final_gate=args.final_gate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
