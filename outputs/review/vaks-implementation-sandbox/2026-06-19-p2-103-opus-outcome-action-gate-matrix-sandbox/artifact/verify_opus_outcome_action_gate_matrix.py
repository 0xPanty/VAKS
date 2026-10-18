import copy
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-19-p2-103-opus-outcome-action-gate-matrix-sandbox"

HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

MATRIX_PATH = ARTIFACT_DIR / "opus-outcome-action-gate-matrix.json"
RUNBOOK_PATH = ARTIFACT_DIR / "opus-outcome-action-gate-runbook.md"
FAILURE_CASE_PATH = FAILURE_DIR / "opus-outcome-action-gate-failures.json"

EXPECTED_TOKENS = [
    "OPUS_PASS_SANDBOX_CLOSEOUT",
    "OPUS_REVISE_SANDBOX_CLOSEOUT",
    "OPUS_BLOCKED_NEEDS_USER",
]
UNSAFE_ACTION_FLAGS = [
    "mainline_merge_allowed",
    "promotion_allowed",
    "reviewed_knowledge_write_allowed",
    "evidence_support_write_allowed",
    "action_basis_allowed",
    "commit_allowed",
    "push_allowed",
    "sync_allowed",
    "goal_complete_now",
]
EXPECTED_FINAL_STATUSES = {
    "verification.md": "local_verification_passed",
    "reviewer-report.md": "review_pass_no_blocker",
    "boundary-audit.md": "pass_boundary",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_next_slice",
}


def load_json(path: Path, failures: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"json_load_failed:{path.name}:{exc}")
        return None


def frontmatter_status(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return "missing_frontmatter"
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def validate_outcome(token: str, record: dict, allowed_tokens: list[str]) -> list[str]:
    failures = []
    if token not in allowed_tokens:
        failures.append("unknown_token")
        return failures
    if record.get("token") != token:
        failures.append("token_mismatch")
    flags = record.get("authority_flags", {})
    for flag in UNSAFE_ACTION_FLAGS:
        if flags.get(flag) is not False:
            failures.append(f"unsafe_action_allowed:{flag}")
    if flags.get("external_opus_result_required") is not True:
        failures.append("external_opus_result_gate_missing")
    if flags.get("mainline_actions_require_separate_user_approval") is not True:
        failures.append("mainline_user_gate_missing")
    if flags.get("sandbox_only") is not True:
        failures.append("sandbox_only_missing")
    prohibited = set(record.get("prohibited_actions", []))
    for action in [
        "automatic_mainline_merge",
        "automatic_promotion",
        "write_reviewed_knowledge",
        "write_evidence_support",
        "create_action_basis",
        "commit",
        "push",
        "obsidian_sync",
    ]:
        if action not in prohibited:
            failures.append(f"missing_prohibited_action:{action}")
    if token == "OPUS_PASS_SANDBOX_CLOSEOUT":
        if "prepare_user_approval_decision_packet" not in record.get("allowed_next_actions", []):
            failures.append("pass_missing_user_decision_packet_action")
        if record.get("required_user_state") != "explicit_user_mainline_approval_still_required":
            failures.append("pass_user_state_mismatch")
    if token == "OPUS_BLOCKED_NEEDS_USER":
        if record.get("stop_state") != "blocked_needs_user":
            failures.append("blocked_stop_state_mismatch")
        if "stop_and_ask_user" not in record.get("allowed_next_actions", []):
            failures.append("blocked_missing_stop_action")
    return failures


def verify(final_gate: bool = False) -> dict:
    failures = []
    matrix = load_json(MATRIX_PATH, failures) if MATRIX_PATH.exists() else None
    failure_payload = load_json(FAILURE_CASE_PATH, failures) if FAILURE_CASE_PATH.exists() else None

    if not RUNBOOK_PATH.exists():
        failures.append("missing_runbook")

    if not matrix:
        failures.append("missing_matrix")
        allowed_tokens = []
        outcomes = {}
    else:
        if matrix.get("record_kind") != "opus_outcome_action_gate_matrix":
            failures.append("matrix_record_kind_mismatch")
        if matrix.get("slice_id") != SLICE_ID:
            failures.append("matrix_slice_id_mismatch")
        allowed_tokens = matrix.get("allowed_conclusion_tokens", [])
        outcomes = matrix.get("outcomes", {})
        if allowed_tokens != EXPECTED_TOKENS:
            failures.append("allowed_tokens_mismatch")
        if set(outcomes) != set(EXPECTED_TOKENS):
            failures.append("outcomes_token_set_mismatch")
        for token, record in outcomes.items():
            outcome_failures = validate_outcome(token, record, allowed_tokens)
            if outcome_failures:
                failures.append(f"outcome_invalid:{token}:{'|'.join(outcome_failures)}")
        invariants = matrix.get("global_invariants", {})
        for key in [
            "automatic_mainline_merge",
            "automatic_promotion",
            "reviewed_knowledge_write",
            "evidence_support_write",
            "action_basis",
            "commit_push_sync",
            "goal_complete_now",
        ]:
            if invariants.get(key) is not False:
                failures.append(f"global_invariant_overclaim:{key}")
        if invariants.get("external_opus_result_is_not_user_mainline_approval") is not True:
            failures.append("missing_opus_not_user_approval_invariant")
        summary = matrix.get("summary", {})
        for key in ["actual_opus_result_present", "opus_approval_claimed", "mainline_ready", "goal_complete_now"]:
            if summary.get(key) is not False:
                failures.append(f"summary_overclaim:{key}")

    fixture_files = sorted(FIXTURES_DIR.glob("valid-*.json"))
    if len(fixture_files) != 3:
        failures.append(f"fixture_count_mismatch:{len(fixture_files)}")
    for fixture in fixture_files:
        record = load_json(fixture, failures)
        if record:
            token = record.get("token")
            fixture_failures = validate_outcome(token, record, allowed_tokens)
            if fixture_failures:
                failures.append(f"fixture_invalid:{fixture.name}:{'|'.join(fixture_failures)}")

    failure_case_count = 0
    expected_failure_hits = 0
    if not failure_payload:
        failures.append("missing_failure_cases")
    else:
        cases = failure_payload.get("failure_cases", [])
        failure_case_count = len(cases)
        if failure_case_count < 12:
            failures.append(f"failure_case_count_too_low:{failure_case_count}")
        for case in cases:
            token = case.get("token")
            expected = case.get("expected_failure")
            if token not in outcomes:
                actual = ["unknown_token"]
            else:
                mutated = copy.deepcopy(outcomes[token])
                mutated["authority_flags"].update(case.get("mutations", {}))
                actual = validate_outcome(token, mutated, allowed_tokens)
            if expected in actual:
                expected_failure_hits += 1
            else:
                failures.append(f"failure_case_not_caught:{case.get('id')}:{expected}:{actual}")

    if RUNBOOK_PATH.exists():
        runbook = RUNBOOK_PATH.read_text(encoding="utf-8")
        for phrase in [
            "does not authorize automatic mainline merge",
            "No Opus outcome authorizes automatic merge",
            "reviewed knowledge writes",
            "evidence support writes",
            "action basis",
            "commit",
            "push",
            "sync",
        ]:
            if phrase not in runbook:
                failures.append(f"runbook_missing_boundary_phrase:{phrase}")

    if final_gate:
        for filename, expected in EXPECTED_FINAL_STATUSES.items():
            report_path = SLICE_DIR / filename
            if not report_path.exists():
                failures.append(f"final_gate_missing_report:{filename}")
                continue
            actual = frontmatter_status(report_path)
            if actual != expected:
                failures.append(f"final_gate_status:{filename}:expected={expected}:actual={actual}")

    summary = {
        "outcome_count": len(outcomes),
        "fixture_count": len(fixture_files),
        "failure_case_count": failure_case_count,
        "expected_failure_hits": expected_failure_hits,
        "pass_does_not_authorize_merge": bool(matrix and matrix.get("summary", {}).get("pass_does_not_authorize_merge")),
        "actual_opus_result_present": bool(matrix and matrix.get("summary", {}).get("actual_opus_result_present")),
        "opus_approval_claimed": bool(matrix and matrix.get("summary", {}).get("opus_approval_claimed")),
        "mainline_ready": bool(matrix and matrix.get("summary", {}).get("mainline_ready")),
        "goal_complete_now": bool(matrix and matrix.get("summary", {}).get("goal_complete_now")),
        "final_gate": final_gate,
    }
    return {"passed": not failures, "failures": failures, "summary": summary}


if __name__ == "__main__":
    result = verify(final_gate="--final-gate" in sys.argv)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["passed"] else 1)
