from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-52-user-decision-no-auto-advance-guard-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-51-user-decision-request-packet-sandbox"
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
    "user_decision_no_auto_advance_guard.json",
    "no_auto_advance_guard_readout.md",
    "no_auto_advance_guard_prototype.html",
    "build_user_decision_no_auto_advance_guard.py",
    "verify_user_decision_no_auto_advance_guard.py",
]

REQUIRED_CASES = {
    "no_reply",
    "explicit_A",
    "explicit_B",
    "explicit_C",
    "explicit_D",
    "ambiguous_reply",
    "multiple_options",
    "approval_with_execution_words",
}

FALSE_FORBIDDEN = {
    "commit",
    "push",
    "obsidian_sync",
    "formal_vault_write",
    "mainline_merge",
    "promotion",
    "release",
    "reviewed_knowledge_write",
    "evidence_support_creation",
    "action_basis_creation",
    "template_write",
    "tool_write",
    "dependency_install",
    "background_service",
    "hook_install",
    "mcp_write_tool",
}

FALSE_READINESS = {
    "user_choice_collected",
    "ready_to_execute",
    "auto_advance_allowed",
    "mainline_ready",
    "promotion_ready",
    "release_ready",
    "formal_vault_ready",
    "reviewed_knowledge_ready",
    "evidence_support_ready",
    "action_basis_ready",
}

EXPECTED_ALLOWED_NEXT_MESSAGES = {
    "no_reply": "wait_for_user_or_report_sandbox_status",
    "explicit_A": "acknowledge_sandbox_reference_only",
    "explicit_B": "ask_user_for_separate_read_only_review_planning_scope",
    "explicit_C": "ask_user_for_separate_allowed_paths_and_scope",
    "explicit_D": "acknowledge_park_or_reject_status",
    "ambiguous_reply": "ask_one_short_clarification",
    "multiple_options": "ask_user_to_choose_one_option",
    "approval_with_execution_words": "stop_and_ask_for_separate_explicit_scope",
}

DANGEROUS_NEXT_MESSAGE_TOKENS = {
    "open",
    "start",
    "execute",
    "run",
    "merge",
    "promote",
    "promotion",
    "commit",
    "push",
    "sync",
    "write",
    "release",
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def add_failure(failures: list[str], condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def frontmatter_status(path: Path) -> str:
    if not path.exists():
        return "missing"
    text = read_text(path)
    for line in text.splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def policy_by_case(config: dict) -> dict[str, dict]:
    policy = config.get("response_policy", [])
    if not isinstance(policy, list):
        return {}
    return {
        item.get("case_id"): item
        for item in policy
        if isinstance(item, dict) and isinstance(item.get("case_id"), str)
    }


def validate_config(config: dict, failures: list[str]) -> None:
    add_failure(failures, config.get("record_kind") == "sandbox_user_decision_no_auto_advance_guard", "wrong record_kind")
    add_failure(failures, config.get("slice_id") == SLICE_ID, "wrong slice_id")
    add_failure(failures, config.get("source_slice_id") == SOURCE_SLICE_ID, "wrong source_slice_id")
    add_failure(
        failures,
        config.get("truth_boundary") == "response_handling_guard_not_user_choice_or_execution_authority",
        "truth_boundary does not preserve non-authority role",
    )
    add_failure(failures, config.get("safe_default_if_no_reply") == "A_keep_sandbox_reference", "no-reply default is not A")

    scope = config.get("scope", {})
    add_failure(failures, isinstance(scope, dict), "scope is missing or not an object")
    if isinstance(scope, dict):
        add_failure(failures, SOURCE_SLICE_ID in scope.get("source_packet", ""), "source packet does not reference p2-51")
        source_gate = scope.get("source_final_gate_command", "")
        add_failure(failures, SOURCE_SLICE_ID in source_gate, "source final gate does not reference p2-51")
        add_failure(failures, "--final-gate" in source_gate, "source final gate omits --final-gate")
        add_failure(failures, scope.get("does_not_modify_mainline") is True, "mainline non-modification flag missing")
        add_failure(failures, scope.get("does_not_collect_user_decision") is True, "decision non-collection flag missing")
        add_failure(failures, scope.get("does_not_execute_any_option") is True, "execution non-authority flag missing")

    cases = policy_by_case(config)
    add_failure(failures, set(cases) == REQUIRED_CASES, f"response policy cases mismatch: {sorted(cases)}")
    for case_id, item in cases.items():
        add_failure(failures, item.get("automatic_execution") is False, f"{case_id} allows automatic execution")
        allowed_next = item.get("allowed_next_message")
        add_failure(
            failures,
            allowed_next == EXPECTED_ALLOWED_NEXT_MESSAGES.get(case_id),
            f"{case_id} allowed_next_message is not the expected safe wording",
        )
        tokens = set(str(allowed_next).lower().replace("-", "_").split("_"))
        unsafe_tokens = sorted(tokens & DANGEROUS_NEXT_MESSAGE_TOKENS)
        add_failure(
            failures,
            not unsafe_tokens,
            f"{case_id} allowed_next_message contains dangerous token(s): {unsafe_tokens}",
        )

    no_reply = cases.get("no_reply", {})
    add_failure(failures, no_reply.get("result") == "A_keep_sandbox_reference", "no_reply does not keep sandbox reference")
    add_failure(failures, no_reply.get("action") == "no_action", "no_reply action is not no_action")

    explicit_a = cases.get("explicit_A", {})
    add_failure(failures, explicit_a.get("result") == "A_keep_sandbox_reference", "explicit_A does not keep sandbox reference")
    add_failure(failures, explicit_a.get("action") == "no_action", "explicit_A action is not no_action")

    explicit_b = cases.get("explicit_B", {})
    add_failure(failures, explicit_b.get("requires_new_scope") is True, "explicit_B does not require new scope")
    add_failure(failures, explicit_b.get("requires_separate_user_approval") is True, "explicit_B lacks separate approval")
    add_failure(
        failures,
        explicit_b.get("action") == "ask_for_separate_read_only_planning_scope_before_any_future_slice",
        "explicit_B action is not separate-scope-first",
    )

    explicit_c = cases.get("explicit_C", {})
    add_failure(failures, explicit_c.get("requires_new_scope") is True, "explicit_C does not require new scope")
    add_failure(failures, explicit_c.get("requires_separate_user_approval") is True, "explicit_C lacks separate approval")
    add_failure(failures, explicit_c.get("requires_explicit_allowed_paths") is True, "explicit_C lacks explicit-path requirement")
    add_failure(failures, explicit_c.get("action") == "ask_for_separate_mainline_review_scope", "explicit_C action is not a scope question")

    explicit_d = cases.get("explicit_D", {})
    add_failure(failures, explicit_d.get("action") == "no_action", "explicit_D action is not no_action")

    for case_id in ("ambiguous_reply", "multiple_options", "approval_with_execution_words"):
        item = cases.get(case_id, {})
        add_failure(failures, item.get("requires_clarification") is True, f"{case_id} does not require clarification")
        add_failure(failures, item.get("automatic_execution") is False, f"{case_id} allows execution")

    boundary_cross = cases.get("approval_with_execution_words", {})
    add_failure(
        failures,
        boundary_cross.get("requires_new_scope") is True and boundary_cross.get("requires_separate_user_approval") is True,
        "execution-word reply does not require new scope and approval",
    )

    forbidden = config.get("forbidden_operations", {})
    add_failure(failures, set(forbidden) == FALSE_FORBIDDEN, "forbidden operation set mismatch")
    for name in FALSE_FORBIDDEN:
        add_failure(failures, forbidden.get(name) is False, f"forbidden operation {name} is not false")

    flags = config.get("readiness_flags", {})
    add_failure(failures, flags.get("guard_ready") is True, "guard_ready is not true")
    add_failure(failures, flags.get("ready_to_wait_for_user") is True, "ready_to_wait_for_user is not true")
    for name in FALSE_READINESS:
        add_failure(failures, flags.get(name) is False, f"readiness flag {name} is not false")

    non_claims = config.get("required_non_claims", [])
    add_failure(failures, isinstance(non_claims, list) and len(non_claims) >= 5, "not enough non-claims")
    joined = "\n".join(str(item) for item in non_claims)
    for phrase in ["not a user decision", "not approval", "not promotion", "not reviewed knowledge", "separately scoped"]:
        add_failure(failures, phrase in joined, f"missing non-claim phrase: {phrase}")

    usage = config.get("ordinary_agent_usage", {})
    add_failure(failures, "Builder-only" in usage.get("rebuild", ""), "rebuild is not marked Builder-only")
    add_failure(failures, "--final-gate" in usage.get("final_gate", ""), "final_gate usage missing --final-gate")
    add_failure(failures, "--run-upstream" in usage.get("upstream_verifier", ""), "upstream usage missing --run-upstream")


def validate_files(failures: list[str]) -> tuple[list[Path], list[Path]]:
    for filename in REQUIRED_ROOT_FILES:
        add_failure(failures, (ROOT / filename).exists(), f"missing required root file: {filename}")
    for filename in REQUIRED_ARTIFACT_FILES:
        add_failure(failures, (ARTIFACT / filename).exists(), f"missing artifact file: {filename}")

    fixture_files = sorted(FIXTURES.glob("*.json"))
    failure_files = sorted(FAILURE_CASES.glob("*.json"))
    add_failure(failures, len(fixture_files) >= 4, "expected at least 4 positive fixtures")
    add_failure(failures, len(failure_files) >= 1, "expected failure case file")
    return fixture_files, failure_files


def validate_fixtures(fixture_files: list[Path], config: dict, failures: list[str]) -> None:
    cases = set()
    policy = policy_by_case(config)
    for path in fixture_files:
        payload = load_json(path)
        if isinstance(payload, dict):
            case_id = payload.get("case_id")
            cases.add(case_id)
            policy_item = policy.get(case_id)
            add_failure(failures, isinstance(policy_item, dict), f"fixture {path.name} references unknown case")
            if isinstance(policy_item, dict):
                add_failure(failures, "expected_result" in payload, f"fixture {path.name} lacks expected_result")
                add_failure(
                    failures,
                    payload.get("expected_result") == policy_item.get("result"),
                    f"fixture {path.name} expected_result drifts from response policy",
                )
                add_failure(failures, "expected_action" in payload, f"fixture {path.name} lacks expected_action")
                add_failure(
                    failures,
                    payload.get("expected_action") == policy_item.get("action"),
                    f"fixture {path.name} expected_action drifts from response policy",
                )
                for flag in ("requires_new_scope", "requires_separate_user_approval", "requires_explicit_allowed_paths"):
                    add_failure(failures, flag in payload, f"fixture {path.name} lacks {flag}")
                    add_failure(
                        failures,
                        payload.get(flag) is bool(policy_item.get(flag, False)),
                        f"fixture {path.name} {flag} drifts from response policy",
                    )
            for forbidden in payload.get("must_not", []):
                add_failure(
                    failures,
                    forbidden in {
                        "execute_option",
                        "merge",
                        "promote",
                        "sync",
                        "commit",
                        "push",
                        "mainline_merge",
                        "promotion",
                    },
                    f"fixture {path.name} has unexpected must_not token {forbidden}",
                )
    for required in ("no_reply", "explicit_A", "explicit_B", "explicit_C"):
        add_failure(failures, required in cases, f"missing positive fixture for {required}")


def validate_failure_cases(failure_files: list[Path], failures: list[str]) -> int:
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
    required_tokens = [
        "no_reply",
        "explicit_B",
        "explicit_C",
        "ambiguous",
        "multiple",
        "commit",
        "push",
        "sync",
        "mainline",
        "promotion",
        "action_basis",
        "source_final_gate",
        "allowed_next_message",
    ]
    joined = "\n".join(str(item) for item in all_cases)
    for token in required_tokens:
        add_failure(failures, token in joined, f"failure cases do not cover {token}")
    return len(all_cases)


def validate_source_product_report(failures: list[str]) -> None:
    source_report = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox" / SOURCE_SLICE_ID / "product-acceptance-report.md"
    add_failure(failures, source_report.exists(), "source p2-51 product report missing")
    if source_report.exists():
        text = read_text(source_report)
        add_failure(failures, "PASS_PRODUCT_GRADE" in text, "source p2-51 is not Product PASS")


def run_upstream_gate() -> tuple[bool, dict | None, str]:
    script = (
        WORKSPACE
        / "outputs"
        / "review"
        / "vaks-implementation-sandbox"
        / SOURCE_SLICE_ID
        / "artifact"
        / "verify_user_decision_request_packet.py"
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

    config_path = ARTIFACT / "user_decision_no_auto_advance_guard.json"
    config = load_json(config_path) if config_path.exists() else {}
    if isinstance(config, dict):
        validate_config(config, failures)
    else:
        failures.append("guard config is not an object")

    validate_fixtures(fixture_files, config if isinstance(config, dict) else {}, failures)
    failure_case_count = validate_failure_cases(failure_files, failures)
    validate_source_product_report(failures)

    upstream_payload = None
    if run_upstream or final_gate:
        upstream_passed, upstream_payload, upstream_error = run_upstream_gate()
        add_failure(failures, upstream_passed, f"upstream p2-51 final gate failed: {upstream_error}")

    if final_gate:
        validate_final_reports(failures)

    summary = {
        "slice_id": SLICE_ID,
        "fixture_count": len(fixture_files),
        "failure_case_count": failure_case_count,
        "response_case_count": len(policy_by_case(config)) if isinstance(config, dict) else 0,
        "run_upstream_p2_51": bool(run_upstream or final_gate),
        "upstream_p2_51_passed": upstream_payload.get("passed") if isinstance(upstream_payload, dict) else None,
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
