from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-53-user-response-classifier-dry-run-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-52-user-decision-no-auto-advance-guard-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
ARTIFACT = ROOT / "artifact"
FIXTURES = ROOT / "fixtures"
FAILURE_CASES = ROOT / "failure-cases"

REQUIRED_ROOT_FILES = [
    "slice-plan.md",
    "source-map.md",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

REQUIRED_ARTIFACT_FILES = [
    "build_user_response_classifier_dry_run.py",
    "classify_user_response_dry_run.py",
    "verify_user_response_classifier_dry_run.py",
    "user_response_classifier_contract.json",
    "user_response_classifier_readout.md",
    "user_response_classifier_prototype.html",
]

EXPECTED_CASES = {
    "no_reply",
    "explicit_A",
    "explicit_B",
    "explicit_C",
    "explicit_D",
    "ambiguous_reply",
    "multiple_options",
    "approval_with_execution_words",
}

FALSE_ALWAYS = {
    "automatic_execution",
}

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
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def import_classifier():
    classifier_path = ARTIFACT / "classify_user_response_dry_run.py"
    spec = importlib.util.spec_from_file_location("p2_53_classifier", classifier_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load classifier module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def policy_by_case(contract: dict) -> dict[str, dict]:
    policy = contract.get("response_policy", [])
    if not isinstance(policy, list):
        return {}
    return {item.get("case_id"): item for item in policy if isinstance(item, dict)}


def frontmatter_status(path: Path) -> str:
    if not path.exists():
        return "missing"
    for line in read_text(path).splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def validate_files(failures: list[str]) -> tuple[list[Path], list[Path]]:
    for filename in REQUIRED_ROOT_FILES:
        add_failure(failures, (ROOT / filename).exists(), f"missing required root file: {filename}")
    for filename in REQUIRED_ARTIFACT_FILES:
        add_failure(failures, (ARTIFACT / filename).exists(), f"missing artifact file: {filename}")
    fixture_files = sorted(FIXTURES.glob("*.json"))
    failure_files = sorted(FAILURE_CASES.glob("*.json"))
    add_failure(failures, len(fixture_files) >= 12, "expected at least 12 positive fixtures")
    add_failure(failures, len(failure_files) >= 1, "expected failure case file")
    return fixture_files, failure_files


def validate_contract(contract: dict, failures: list[str]) -> None:
    add_failure(
        failures,
        contract.get("record_kind") == "sandbox_user_response_classifier_dry_run_contract",
        "wrong contract record_kind",
    )
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong slice_id")
    add_failure(failures, contract.get("source_slice_id") == SOURCE_SLICE_ID, "wrong source_slice_id")
    add_failure(
        failures,
        contract.get("truth_boundary") == "dry_run_classifier_not_user_decision_or_execution_authority",
        "truth boundary is not dry-run non-authority",
    )
    add_failure(failures, "--final-gate" in contract.get("source_final_gate_command", ""), "source final gate omits --final-gate")
    add_failure(failures, SOURCE_SLICE_ID in contract.get("source_final_gate_command", ""), "source final gate omits p2-52")

    policy = policy_by_case(contract)
    add_failure(failures, set(policy) == EXPECTED_CASES, "response policy cases mismatch")
    for case_id, item in policy.items():
        for field in FALSE_ALWAYS:
            add_failure(failures, item.get(field) is False, f"{case_id} {field} is not false")
        for field in (
            "result",
            "safe_next_step",
            "requires_clarification",
            "requires_new_scope",
            "requires_separate_user_approval",
            "requires_explicit_allowed_paths",
        ):
            add_failure(failures, field in item, f"{case_id} missing {field}")

    add_failure(failures, policy.get("explicit_B", {}).get("requires_new_scope") is True, "B lacks new scope")
    add_failure(failures, policy.get("explicit_B", {}).get("requires_separate_user_approval") is True, "B lacks separate approval")
    add_failure(failures, policy.get("explicit_B", {}).get("requires_explicit_allowed_paths") is False, "B incorrectly requires explicit paths")
    add_failure(failures, policy.get("explicit_C", {}).get("requires_explicit_allowed_paths") is True, "C lacks explicit allowed paths")
    add_failure(failures, policy.get("approval_with_execution_words", {}).get("requires_new_scope") is True, "execution words lack new scope")
    add_failure(
        failures,
        policy.get("approval_with_execution_words", {}).get("requires_explicit_allowed_paths") is True,
        "execution words lack explicit paths",
    )

    output_contract = contract.get("dry_run_output_contract", {})
    add_failure(failures, output_contract.get("automatic_execution") is False, "output contract automatic_execution is not false")
    must_not = set(output_contract.get("must_not", []))
    add_failure(failures, MUST_NOT_REQUIRED <= must_not, "output contract must_not is incomplete")

    usage = contract.get("ordinary_agent_usage", {})
    add_failure(failures, "Builder-only" in usage.get("rebuild", ""), "rebuild is not Builder-only")
    add_failure(failures, "--run-upstream" in usage.get("upstream_verifier", ""), "upstream verifier usage missing --run-upstream")
    add_failure(failures, "--final-gate" in usage.get("final_gate", ""), "final gate usage missing --final-gate")

    non_claims = "\n".join(str(item) for item in contract.get("required_non_claims", []))
    for phrase in ["not a user decision", "not execution authority", "cannot approve merge", "Ambiguous", "B and C"]:
        add_failure(failures, phrase in non_claims, f"missing non-claim phrase: {phrase}")


def validate_fixture_outputs(fixture_files: list[Path], contract: dict, failures: list[str]) -> int:
    classifier = import_classifier()
    policy = policy_by_case(contract)
    seen_cases: set[str] = set()
    for path in fixture_files:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"fixture {path.name} is not an object")
            continue
        expected_case = fixture.get("case_id")
        seen_cases.add(str(expected_case))
        result = classifier.classify(fixture.get("input_text"))
        add_failure(failures, result.get("case_id") == expected_case, f"{path.name} classified as {result.get('case_id')}, expected {expected_case}")
        policy_item = policy.get(str(expected_case), {})
        for field, output_field in (
            ("expected_result", "result"),
            ("expected_safe_next_step", "safe_next_step"),
        ):
            add_failure(failures, field in fixture, f"{path.name} missing {field}")
            add_failure(failures, fixture.get(field) == result.get(output_field), f"{path.name} {field} drifts from classifier output")
            add_failure(failures, fixture.get(field) == policy_item.get(output_field), f"{path.name} {field} drifts from policy")
        for flag in (
            "automatic_execution",
            "requires_clarification",
            "requires_new_scope",
            "requires_separate_user_approval",
            "requires_explicit_allowed_paths",
        ):
            add_failure(failures, flag in fixture, f"{path.name} missing {flag}")
            add_failure(failures, fixture.get(flag) == result.get(flag), f"{path.name} {flag} drifts from classifier output")
            add_failure(failures, fixture.get(flag) == policy_item.get(flag), f"{path.name} {flag} drifts from policy")
        add_failure(failures, result.get("automatic_execution") is False, f"{path.name} allows execution")
        add_failure(failures, MUST_NOT_REQUIRED <= set(result.get("must_not", [])), f"{path.name} must_not incomplete")

    for case_id in EXPECTED_CASES:
        add_failure(failures, case_id in seen_cases, f"missing fixture for {case_id}")
    return len(fixture_files)


def validate_failure_cases(failure_files: list[Path], contract: dict, failures: list[str]) -> int:
    classifier = import_classifier()
    all_cases: list[dict] = []
    for path in failure_files:
        payload = load_json(path)
        if isinstance(payload, list):
            all_cases.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            all_cases.append(payload)
    add_failure(failures, len(all_cases) >= 40, "expected at least 40 failure cases")
    ids = [item.get("failure_id") for item in all_cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure case ids are not unique")
    policy = policy_by_case(contract)
    for item in all_cases:
        failure_id = item.get("failure_id", "unknown_failure")
        add_failure(failures, "input_text" in item, f"{failure_id} lacks input_text")
        add_failure(failures, "expected_case_id" in item, f"{failure_id} lacks expected_case_id")
        expected_case_id = item.get("expected_case_id")
        result = classifier.classify(item.get("input_text"))
        policy_item = policy.get(str(expected_case_id), {})
        add_failure(
            failures,
            result.get("case_id") == expected_case_id,
            f"{failure_id} classified as {result.get('case_id')}, expected {expected_case_id}",
        )
        for field, output_field in (
            ("expected_result", "result"),
            ("expected_safe_next_step", "safe_next_step"),
        ):
            add_failure(failures, field in item, f"{failure_id} lacks {field}")
            add_failure(failures, item.get(field) == result.get(output_field), f"{failure_id} {field} drifts from classifier output")
            add_failure(failures, item.get(field) == policy_item.get(output_field), f"{failure_id} {field} drifts from policy")
        for flag in (
            "automatic_execution",
            "requires_clarification",
            "requires_new_scope",
            "requires_separate_user_approval",
            "requires_explicit_allowed_paths",
        ):
            add_failure(failures, flag in item, f"{failure_id} lacks {flag}")
            add_failure(failures, item.get(flag) == result.get(flag), f"{failure_id} {flag} drifts from classifier output")
            add_failure(failures, item.get(flag) == policy_item.get(flag), f"{failure_id} {flag} drifts from policy")
        add_failure(failures, result.get("automatic_execution") is False, f"{failure_id} allows execution")
        add_failure(failures, MUST_NOT_REQUIRED <= set(result.get("must_not", [])), f"{failure_id} must_not incomplete")
        add_failure(failures, MUST_NOT_REQUIRED <= set(item.get("must_not", [])), f"{failure_id} fixture must_not incomplete")
    joined = "\n".join(str(item) for item in all_cases)
    for token in [
        "no_reply",
        "explicit_B",
        "explicit_C",
        "ambiguous",
        "multiple",
        "execution",
        "commit",
        "push",
        "sync",
        "merge",
        "promote",
    ]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    return len(all_cases)


def run_upstream_gate() -> tuple[bool, dict | None, str]:
    script = (
        WORKSPACE
        / "outputs"
        / "review"
        / "vaks-implementation-sandbox"
        / SOURCE_SLICE_ID
        / "artifact"
        / "verify_user_decision_no_auto_advance_guard.py"
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
    verification = ROOT / "verification.md"
    reviewer = ROOT / "reviewer-report.md"
    boundary = ROOT / "boundary-audit.md"
    product = ROOT / "product-acceptance-report.md"
    next_step = ROOT / "next-step.md"

    add_failure(failures, frontmatter_status(verification) == "local_verification_passed", "verification status is not local_verification_passed")
    add_failure(failures, "REVIEW_PASS_NO_BLOCKER" in read_text(reviewer), "Reviewer report lacks REVIEW_PASS_NO_BLOCKER")
    add_failure(failures, "PASS_BOUNDARY" in read_text(boundary), "Boundary audit lacks PASS_BOUNDARY")
    add_failure(failures, "PASS_PRODUCT_GRADE" in read_text(product), "Product report lacks PASS_PRODUCT_GRADE")
    add_failure(
        failures,
        frontmatter_status(next_step) == "pass_product_grade_pending_user_response",
        "next-step status is not pass_product_grade_pending_user_response",
    )


def verify(run_upstream: bool = False, final_gate: bool = False) -> dict:
    failures: list[str] = []
    fixture_files, failure_files = validate_files(failures)
    contract_path = ARTIFACT / "user_response_classifier_contract.json"
    contract = load_json(contract_path) if contract_path.exists() else {}
    if isinstance(contract, dict):
        validate_contract(contract, failures)
        fixture_count = validate_fixture_outputs(fixture_files, contract, failures)
    else:
        failures.append("contract is not an object")
        fixture_count = len(fixture_files)
    failure_case_count = validate_failure_cases(failure_files, contract if isinstance(contract, dict) else {}, failures)

    upstream_payload = None
    if run_upstream or final_gate:
        upstream_passed, upstream_payload, upstream_error = run_upstream_gate()
        add_failure(failures, upstream_passed, f"upstream p2-52 final gate failed: {upstream_error}")

    if final_gate:
        validate_final_reports(failures)

    summary = {
        "slice_id": SLICE_ID,
        "fixture_count": fixture_count,
        "failure_case_count": failure_case_count,
        "response_case_count": len(policy_by_case(contract)) if isinstance(contract, dict) else 0,
        "run_upstream_p2_52": bool(run_upstream or final_gate),
        "upstream_p2_52_passed": upstream_payload.get("passed") if isinstance(upstream_payload, dict) else None,
        "final_gate": final_gate,
    }
    return {"passed": not failures, "failures": failures, "summary": summary}


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
