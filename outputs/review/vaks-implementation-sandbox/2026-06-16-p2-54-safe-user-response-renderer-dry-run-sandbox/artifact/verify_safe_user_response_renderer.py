from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-54-safe-user-response-renderer-dry-run-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-53-user-response-classifier-dry-run-sandbox"
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
    "build_safe_user_response_renderer.py",
    "render_safe_user_response.py",
    "verify_safe_user_response_renderer.py",
    "safe_user_response_renderer_contract.json",
    "safe_user_response_renderer_readout.md",
    "safe_user_response_renderer_prototype.html",
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
    "unknown_case_fallback",
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
    "start_future_slice_by_inference",
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def import_renderer():
    renderer_path = ARTIFACT / "render_safe_user_response.py"
    spec = importlib.util.spec_from_file_location("p2_54_renderer", renderer_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load renderer")
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


def policy_by_case(contract: dict) -> dict[str, dict]:
    return {item.get("case_id"): item for item in contract.get("render_policy", []) if isinstance(item, dict)}


def reply_safety(reply: str, contract: dict) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    rules = contract.get("reply_safety_rules", {})
    required = rules.get("required_boundary_terms", [])
    dangerous = rules.get("dangerous_positive_phrases", [])
    if not any(term in reply for term in required):
        reasons.append("missing negative boundary term")
    for phrase in dangerous:
        if phrase in reply:
            reasons.append(f"contains dangerous positive phrase: {phrase}")
    return not reasons, reasons


def validate_files(failures: list[str]) -> tuple[list[Path], list[Path]]:
    for filename in REQUIRED_ROOT_FILES:
        add_failure(failures, (ROOT / filename).exists(), f"missing required root file: {filename}")
    for filename in REQUIRED_ARTIFACT_FILES:
        add_failure(failures, (ARTIFACT / filename).exists(), f"missing artifact file: {filename}")
    fixture_files = sorted(FIXTURES.glob("*.json"))
    failure_files = sorted(FAILURE_CASES.glob("*.json"))
    add_failure(failures, len(fixture_files) >= 8, "expected at least 8 fixtures")
    add_failure(failures, len(failure_files) >= 1, "expected failure case file")
    return fixture_files, failure_files


def validate_contract(contract: dict, failures: list[str]) -> None:
    add_failure(failures, contract.get("record_kind") == "sandbox_safe_user_response_renderer_contract", "wrong record_kind")
    add_failure(failures, contract.get("slice_id") == SLICE_ID, "wrong slice_id")
    add_failure(failures, contract.get("source_slice_id") == SOURCE_SLICE_ID, "wrong source_slice_id")
    add_failure(
        failures,
        contract.get("truth_boundary") == "dry_run_renderer_not_user_decision_or_execution_authority",
        "wrong truth boundary",
    )
    source_gate = contract.get("source_final_gate_command", "")
    add_failure(failures, SOURCE_SLICE_ID in source_gate and "--final-gate" in source_gate, "source final gate is incomplete")

    policy = policy_by_case(contract)
    add_failure(failures, set(policy) == EXPECTED_CASES, "render policy cases mismatch")
    reply_ids = [item.get("reply_id") for item in policy.values()]
    add_failure(failures, len(reply_ids) == len(set(reply_ids)), "reply ids are not unique")
    for case_id, item in policy.items():
        add_failure(failures, item.get("reply"), f"{case_id} reply is empty")
        add_failure(failures, item.get("next_step"), f"{case_id} next_step is empty")
        safe, reasons = reply_safety(item.get("reply", ""), contract)
        add_failure(failures, safe, f"{case_id} reply is unsafe: {reasons}")
    add_failure(failures, "范围" in policy.get("explicit_B", {}).get("reply", ""), "B reply does not ask for scope")
    add_failure(failures, "不会启动" in policy.get("explicit_B", {}).get("reply", ""), "B reply does not deny starting work")
    c_reply = policy.get("explicit_C", {}).get("reply", "")
    add_failure(failures, "允许路径" in c_reply and "不会改主线" in c_reply, "C reply lacks allowed-path/mainline boundary")
    stop_reply = policy.get("approval_with_execution_words", {}).get("reply", "")
    add_failure(failures, "停止" in stop_reply and "不执行" in stop_reply, "execution-word reply does not stop")
    fallback_reply = policy.get("unknown_case_fallback", {}).get("reply", "")
    add_failure(failures, "停止" in fallback_reply and "不执行" in fallback_reply, "unknown-case fallback does not stop")

    output_contract = contract.get("output_contract", {})
    add_failure(failures, output_contract.get("automatic_execution") is False, "output contract automatic_execution not false")
    add_failure(failures, MUST_NOT_REQUIRED <= set(output_contract.get("must_not", [])), "output contract must_not incomplete")

    usage = contract.get("ordinary_agent_usage", {})
    add_failure(failures, "Builder-only" in usage.get("rebuild", ""), "rebuild is not Builder-only")
    add_failure(failures, "--run-upstream" in usage.get("upstream_verifier", ""), "upstream usage missing --run-upstream")
    add_failure(failures, "--final-gate" in usage.get("final_gate", ""), "final gate usage missing --final-gate")

    non_claims = "\n".join(str(item) for item in contract.get("required_non_claims", []))
    for phrase in ["not a user decision", "not execution authority", "cannot approve merge", "negative", "do not start work"]:
        add_failure(failures, phrase in non_claims, f"missing non-claim phrase: {phrase}")


def validate_render_output(output: dict, contract: dict, failures: list[str], label: str) -> None:
    add_failure(failures, output.get("record_kind") == "sandbox_safe_user_response_renderer_result", f"{label} wrong record_kind")
    add_failure(failures, output.get("truth_boundary") == "dry_run_reply_not_user_decision_or_execution_authority", f"{label} wrong truth boundary")
    add_failure(failures, output.get("automatic_execution") is False, f"{label} automatic_execution is not false")
    add_failure(failures, MUST_NOT_REQUIRED <= set(output.get("must_not", [])), f"{label} must_not incomplete")
    safe, reasons = reply_safety(output.get("reply", ""), contract)
    add_failure(failures, safe, f"{label} reply unsafe: {reasons}")


def validate_fixtures(fixture_files: list[Path], contract: dict, failures: list[str]) -> int:
    renderer = import_renderer()
    seen_cases: set[str] = set()
    for path in fixture_files:
        fixture = load_json(path)
        if not isinstance(fixture, dict):
            failures.append(f"fixture {path.name} is not an object")
            continue
        output = renderer.render(fixture.get("input_text", ""))
        label = f"fixture {path.name}"
        expected_case = fixture.get("expected_case_id")
        seen_cases.add(str(expected_case))
        if expected_case == "unknown_case_fallback":
            add_failure(failures, output.get("reply_id") == "stop_for_unknown_classifier_case", f"{label} did not use unknown fallback")
        else:
            add_failure(failures, output.get("classifier_case_id") == expected_case, f"{label} case mismatch")
        add_failure(failures, output.get("reply_id") == fixture.get("expected_reply_id"), f"{label} reply_id mismatch")
        add_failure(failures, output.get("next_step") == fixture.get("expected_next_step"), f"{label} next_step mismatch")
        add_failure(failures, fixture.get("automatic_execution") is False, f"{label} fixture automatic_execution not false")
        validate_render_output(output, contract, failures, label)
    for case_id in EXPECTED_CASES:
        add_failure(failures, case_id in seen_cases, f"missing fixture for {case_id}")
    return len(fixture_files)


def validate_failure_cases(failure_files: list[Path], contract: dict, failures: list[str]) -> int:
    renderer = import_renderer()
    all_cases: list[dict] = []
    for path in failure_files:
        payload = load_json(path)
        if isinstance(payload, list):
            all_cases.extend(item for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            all_cases.append(payload)
    add_failure(failures, len(all_cases) >= 12, "expected at least 12 failure cases")
    ids = [item.get("failure_id") for item in all_cases]
    add_failure(failures, len(ids) == len(set(ids)), "failure case ids are not unique")
    joined = "\n".join(str(item) for item in all_cases)
    for token in ["merge", "commit", "push", "sync", "write", "scope", "ambiguous", "multiple", "source_p2_53"]:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")

    for item in all_cases:
        failure_id = str(item.get("failure_id"))
        output = renderer.render(item.get("input_text", ""))
        if item.get("expected_case_id"):
            if item.get("expected_case_id") == "unknown_case_fallback":
                add_failure(failures, output.get("reply_id") == "stop_for_unknown_classifier_case", f"{failure_id} did not use unknown fallback")
            else:
                add_failure(failures, output.get("classifier_case_id") == item.get("expected_case_id"), f"{failure_id} case mismatch")
        validate_render_output(output, contract, failures, failure_id)
        unsafe_reply = item.get("unsafe_reply", "")
        add_failure(failures, bool(unsafe_reply), f"{failure_id} lacks unsafe_reply")
        safe, _ = reply_safety(unsafe_reply, contract)
        add_failure(failures, not safe, f"{failure_id} unsafe_reply was not rejected by safety checker")
        add_failure(failures, MUST_NOT_REQUIRED <= set(item.get("must_not", [])), f"{failure_id} must_not incomplete")
    return len(all_cases)


def run_upstream_gate() -> tuple[bool, dict | None, str]:
    script = (
        WORKSPACE
        / "outputs"
        / "review"
        / "vaks-implementation-sandbox"
        / SOURCE_SLICE_ID
        / "artifact"
        / "verify_user_response_classifier_dry_run.py"
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
    add_failure(failures, frontmatter_status(ROOT / "verification.md") == "local_verification_passed", "verification status is not local_verification_passed")
    add_failure(failures, "REVIEW_PASS_NO_BLOCKER" in read_text(ROOT / "reviewer-report.md"), "Reviewer report lacks REVIEW_PASS_NO_BLOCKER")
    add_failure(failures, "PASS_BOUNDARY" in read_text(ROOT / "boundary-audit.md"), "Boundary audit lacks PASS_BOUNDARY")
    add_failure(failures, "PASS_PRODUCT_GRADE" in read_text(ROOT / "product-acceptance-report.md"), "Product report lacks PASS_PRODUCT_GRADE")
    add_failure(
        failures,
        frontmatter_status(ROOT / "next-step.md") == "pass_product_grade_pending_user_response",
        "next-step status is not pass_product_grade_pending_user_response",
    )


def verify(run_upstream: bool = False, final_gate: bool = False) -> dict:
    failures: list[str] = []
    fixture_files, failure_files = validate_files(failures)
    contract_path = ARTIFACT / "safe_user_response_renderer_contract.json"
    data = load_json(contract_path) if contract_path.exists() else {}
    if isinstance(data, dict):
        validate_contract(data, failures)
        fixture_count = validate_fixtures(fixture_files, data, failures)
        failure_case_count = validate_failure_cases(failure_files, data, failures)
    else:
        failures.append("contract is not an object")
        fixture_count = len(fixture_files)
        failure_case_count = len(failure_files)

    upstream_payload = None
    if run_upstream or final_gate:
        upstream_passed, upstream_payload, upstream_error = run_upstream_gate()
        add_failure(failures, upstream_passed, f"upstream p2-53 final gate failed: {upstream_error}")

    if final_gate:
        validate_final_reports(failures)

    summary = {
        "slice_id": SLICE_ID,
        "fixture_count": fixture_count,
        "failure_case_count": failure_case_count,
        "render_case_count": len(policy_by_case(data)) if isinstance(data, dict) else 0,
        "run_upstream_p2_53": bool(run_upstream or final_gate),
        "upstream_p2_53_passed": upstream_payload.get("passed") if isinstance(upstream_payload, dict) else None,
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
