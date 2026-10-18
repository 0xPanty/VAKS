from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-55-user-decision-e2e-dry-run-simulator-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-54-safe-user-response-renderer-dry-run-sandbox"
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

EXPECTED_REPLY_BY_CASE = {
    "no_reply": "keep_reference_no_action",
    "explicit_A": "acknowledge_reference_only",
    "explicit_B": "ask_readonly_planning_scope",
    "explicit_C": "ask_mainline_review_scope",
    "explicit_D": "acknowledge_park_or_reject",
    "ambiguous_reply": "ask_one_clarification",
    "multiple_options": "ask_choose_one",
    "approval_with_execution_words": "stop_for_separate_scope",
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
    "build_user_decision_e2e_simulator.py",
    "simulate_user_decision_dry_run.py",
    "verify_user_decision_e2e_simulator.py",
    "user_decision_e2e_simulator_contract.json",
    "user_decision_e2e_simulator_readout.md",
    "user_decision_e2e_simulator_prototype.html",
]


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def import_simulator():
    path = ARTIFACT / "simulate_user_decision_dry_run.py"
    spec = importlib.util.spec_from_file_location("p2_55_simulator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load simulator")
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
    add_failure(failures, len(fixture_files) >= 10, "expected at least 10 fixtures")
    add_failure(failures, len(failure_files) >= 1, "expected failure cases")
    return fixture_files, failure_files


def validate_contract(contract: dict, failures: list[str]) -> None:
    add_failure(failures, contract.get("record_kind") == "sandbox_user_decision_e2e_dry_run_simulator_contract", "wrong record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong slice_id")
    add_failure(failures, contract.get("source_slice_id") == SOURCE_SLICE_ID, "wrong source_slice_id")
    add_failure(failures, contract.get("truth_boundary") == "e2e_dry_run_not_user_decision_or_execution_authority", "wrong truth boundary")
    add_failure(failures, SOURCE_SLICE_ID in contract.get("source_final_gate_command", ""), "source gate omits p2-54")
    add_failure(failures, "--final-gate" in contract.get("source_final_gate_command", ""), "source gate omits --final-gate")
    output = contract.get("simulation_output_contract", {})
    for flag in [
        "automatic_execution",
        "decision_collected",
        "ready_to_execute",
        "mainline_ready",
        "promotion_ready",
        "action_basis_ready",
    ]:
        add_failure(failures, output.get(flag) is False, f"contract {flag} is not false")
    add_failure(failures, MUST_NOT_REQUIRED <= set(output.get("must_not", [])), "contract must_not incomplete")
    usage = contract.get("ordinary_agent_usage", {})
    add_failure(failures, "Builder-only" in usage.get("rebuild", ""), "rebuild not Builder-only")
    add_failure(failures, "--run-upstream" in usage.get("upstream_verifier", ""), "upstream usage missing")
    add_failure(failures, "--final-gate" in usage.get("final_gate", ""), "final gate usage missing")
    non_claims = "\n".join(str(item) for item in contract.get("required_non_claims", []))
    for phrase in ["not a user decision", "not execution authority", "cannot approve merge", "only shows", "fail closed"]:
        add_failure(failures, phrase in non_claims, f"missing non-claim phrase: {phrase}")


def validate_simulation_output(output: dict, failures: list[str], label: str) -> None:
    add_failure(failures, output.get("record_kind") == "sandbox_user_decision_e2e_dry_run_result", f"{label} wrong record_kind")
    add_failure(failures, output.get("truth_boundary") == "e2e_dry_run_result_not_user_decision_or_execution_authority", f"{label} wrong truth boundary")
    add_failure(failures, output.get("automatic_execution") is False, f"{label} automatic_execution true")
    add_failure(failures, output.get("decision_collected") is False, f"{label} decision_collected true")
    add_failure(failures, output.get("ready_to_execute") is False, f"{label} ready_to_execute true")
    add_failure(failures, output.get("mainline_ready") is False, f"{label} mainline_ready true")
    add_failure(failures, output.get("promotion_ready") is False, f"{label} promotion_ready true")
    add_failure(failures, output.get("action_basis_ready") is False, f"{label} action_basis_ready true")
    add_failure(failures, output.get("classifier", {}).get("automatic_execution") is False, f"{label} classifier executes")
    add_failure(failures, output.get("renderer", {}).get("automatic_execution") is False, f"{label} renderer executes")
    classifier_case = output.get("classifier", {}).get("case_id")
    renderer_case = output.get("renderer", {}).get("classifier_case_id")
    reply_id = output.get("renderer", {}).get("reply_id")
    if classifier_case in EXPECTED_REPLY_BY_CASE:
        recomputed_unknown_fallback = False
        recomputed_consistent = renderer_case == classifier_case and reply_id == EXPECTED_REPLY_BY_CASE[classifier_case]
    else:
        recomputed_unknown_fallback = reply_id == "stop_for_unknown_classifier_case"
        recomputed_consistent = recomputed_unknown_fallback
    add_failure(failures, recomputed_consistent, f"{label} recomputed case/reply consistency failed")
    add_failure(
        failures,
        output.get("consistency", {}).get("case_consistent") is recomputed_consistent,
        f"{label} stored case_consistent disagrees with recomputed consistency",
    )
    add_failure(
        failures,
        output.get("consistency", {}).get("unknown_fallback") is recomputed_unknown_fallback,
        f"{label} stored unknown_fallback disagrees with recomputed fallback",
    )
    add_failure(failures, output.get("consistency", {}).get("reply_present") is True, f"{label} reply missing")
    add_failure(failures, MUST_NOT_REQUIRED <= set(output.get("must_not", [])), f"{label} must_not incomplete")


def validate_fixtures(fixture_files: list[Path], failures: list[str]) -> int:
    simulator = import_simulator()
    seen_cases: set[str] = set()
    for path in fixture_files:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"{path.name} is not object")
            continue
        output = simulator.simulate(fixture.get("input_text", ""))
        label = f"fixture {path.name}"
        expected_case = fixture.get("expected_case_id")
        expected_reply = fixture.get("expected_reply_id")
        seen_cases.add(str(expected_case))
        if expected_case == "unknown_case_fallback":
            add_failure(failures, output.get("renderer", {}).get("reply_id") == expected_reply, f"{label} fallback reply mismatch")
        else:
            add_failure(failures, output.get("classifier", {}).get("case_id") == expected_case, f"{label} classifier case mismatch")
            add_failure(failures, output.get("renderer", {}).get("classifier_case_id") == expected_case, f"{label} renderer case mismatch")
            add_failure(failures, output.get("renderer", {}).get("reply_id") == expected_reply, f"{label} reply mismatch")
        validate_simulation_output(output, failures, label)
    for required in [
        "no_reply",
        "explicit_A",
        "explicit_B",
        "explicit_C",
        "explicit_D",
        "ambiguous_reply",
        "multiple_options",
        "approval_with_execution_words",
        "unknown_case_fallback",
    ]:
        add_failure(failures, required in seen_cases, f"missing fixture for {required}")
    return len(fixture_files)


def set_nested(data: dict, dotted_key: str, value: object) -> None:
    target = data
    parts = dotted_key.split(".")
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    target[parts[-1]] = value


def apply_mutation(output: dict, mutation: dict) -> dict:
    mutated = json.loads(json.dumps(output, ensure_ascii=False))
    for key, value in mutation.items():
        if key == "must_not_remove":
            mutated["must_not"] = [item for item in mutated.get("must_not", []) if item != value]
        elif key == "upstream_gate_checked":
            mutated["upstream_gate_checked"] = value
        else:
            set_nested(mutated, key, value)
    return mutated


def collect_output_failures(output: dict) -> list[str]:
    failures: list[str] = []
    validate_simulation_output(output, failures, "mutated")
    return failures


def validate_failure_cases(failure_files: list[Path], failures: list[str]) -> int:
    simulator = import_simulator()
    all_cases: list[dict] = []
    for path in failure_files:
        payload = load_json(path)
        if isinstance(payload, list):
            all_cases.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            all_cases.append(payload)
    add_failure(failures, len(all_cases) >= 12, "expected at least 12 failure cases")
    ids = [item.get("failure_id") for item in all_cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure ids not unique")
    joined = "\n".join(str(item) for item in all_cases)
    for token in ["mismatch", "automatic", "decision", "ready", "mainline", "promotion", "action_basis", "must_not", "unknown", "execution", "multiple", "ambiguous"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    for item in all_cases:
        add_failure(failures, bool(item.get("input_text") is not None), f"{item.get('failure_id')} lacks input_text")
        mutation = item.get("mutation")
        add_failure(failures, isinstance(mutation, dict) and bool(mutation), f"{item.get('failure_id')} lacks executable mutation")
        if isinstance(mutation, dict) and mutation:
            base_output = simulator.simulate(item.get("input_text", ""))
            mutated = apply_mutation(base_output, mutation)
            mutation_failures = collect_output_failures(mutated)
            add_failure(failures, bool(mutation_failures), f"{item.get('failure_id')} mutated state was not rejected")
        add_failure(failures, MUST_NOT_REQUIRED <= set(item.get("must_not", [])), f"{item.get('failure_id')} must_not incomplete")
    return len(all_cases)


def run_upstream_gate() -> tuple[bool, dict | None, str]:
    script = (
        WORKSPACE
        / "outputs"
        / "review"
        / "vaks-implementation-sandbox"
        / SOURCE_SLICE_ID
        / "artifact"
        / "verify_safe_user_response_renderer.py"
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
    failures: list[str] = []
    fixture_files, failure_files = validate_files(failures)
    contract_path = ARTIFACT / "user_decision_e2e_simulator_contract.json"
    contract = load_json(contract_path) if contract_path.exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
    else:
        failures.append("contract is not object")
    fixture_count = validate_fixtures(fixture_files, failures)
    failure_case_count = validate_failure_cases(failure_files, failures)
    upstream_payload = None
    if run_upstream or final_gate:
        upstream_passed, upstream_payload, upstream_error = run_upstream_gate()
        add_failure(failures, upstream_passed, f"upstream p2-54 final gate failed: {upstream_error}")
    if final_gate:
        validate_final_reports(failures)
    return {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": fixture_count,
            "failure_case_count": failure_case_count,
            "run_upstream_p2_54": bool(run_upstream or final_gate),
            "upstream_p2_54_passed": upstream_payload.get("passed") if isinstance(upstream_payload, dict) else None,
            "final_gate": final_gate,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-upstream", action="store_true")
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = verify(run_upstream=args.run_upstream, final_gate=args.final_gate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
