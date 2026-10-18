import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-19-p2-104-post-opus-user-approval-decision-packet-sandbox"
EXACT_APPROVAL_PHRASE = (
    "I explicitly approve post-Opus mainline consideration for VAKS sandbox closeout: "
    "prepare a separate merge proposal only; do not merge, promote, commit, push, sync, "
    "or write reviewed knowledge/action basis without my next explicit approval."
)

HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

PACKET_PATH = ARTIFACT_DIR / "post-opus-user-approval-decision-packet.md"
CONTROL_CARD_PATH = ARTIFACT_DIR / "post-opus-user-approval-control-card.json"
FAILURE_CASE_PATH = FAILURE_DIR / "post-opus-user-approval-failures.json"

AUTHORITY_FALSE_FLAGS = [
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


def validate_record(record: dict) -> list[str]:
    failures = []
    if record.get("record_kind") != "post_opus_user_approval_decision_dry_run":
        failures.append("record_kind_mismatch")
    if record.get("dry_run_only") is not True:
        failures.append("dry_run_only_not_true")
    if record.get("user_approval_present") is True and record.get("validated_opus_pass_present") is not True:
        failures.append("user_approval_before_validated_opus_pass")
    if record.get("user_approval_present") is True and record.get("user_message") != EXACT_APPROVAL_PHRASE:
        failures.append("exact_approval_phrase_mismatch")
    flags = record.get("authority_flags", {})
    for flag in AUTHORITY_FALSE_FLAGS:
        if flags.get(flag) is not False:
            failures.append(f"authority_flag_overclaim:{flag}")
    if record.get("allowed_next_state") == "prepare_merge_proposal_only":
        if record.get("actual_opus_result_present") is not True:
            failures.append("merge_proposal_without_actual_opus_result")
        if record.get("validated_opus_pass_present") is not True:
            failures.append("merge_proposal_without_validated_opus_pass")
        if record.get("user_approval_present") is not True:
            failures.append("merge_proposal_without_user_approval")
    return failures


def verify(final_gate: bool = False) -> dict:
    failures = []
    control = load_json(CONTROL_CARD_PATH, failures) if CONTROL_CARD_PATH.exists() else None
    failure_payload = load_json(FAILURE_CASE_PATH, failures) if FAILURE_CASE_PATH.exists() else None
    if not PACKET_PATH.exists():
        failures.append("missing_packet")

    if control:
        if control.get("record_kind") != "post_opus_user_approval_control_card":
            failures.append("control_record_kind_mismatch")
        if control.get("slice_id") != SLICE_ID:
            failures.append("control_slice_id_mismatch")
        if control.get("exact_approval_phrase") != EXACT_APPROVAL_PHRASE:
            failures.append("control_exact_phrase_mismatch")
        current = control.get("current_state", {})
        for key in [
            "dry_run_only",
        ]:
            if current.get(key) is not True:
                failures.append(f"current_state_expected_true:{key}")
        for key in [
            "actual_opus_result_present",
            "validated_opus_pass_present",
            "user_approval_present",
            "ready_for_merge_proposal",
            "mainline_merge_allowed",
            "goal_complete_now",
        ]:
            if current.get(key) is not False:
                failures.append(f"current_state_overclaim:{key}")
        post = control.get("post_exact_approval_allowed_state", {})
        if post.get("prepare_merge_proposal_only") is not True:
            failures.append("post_exact_approval_missing_merge_proposal_only")
        for key in AUTHORITY_FALSE_FLAGS:
            if post.get(key) is not False:
                failures.append(f"post_exact_approval_overclaim:{key}")

    if PACKET_PATH.exists():
        packet = PACKET_PATH.read_text(encoding="utf-8")
        for phrase in [
            EXACT_APPROVAL_PHRASE,
            "Opus PASS is not user approval",
            "not merge",
            "reviewed knowledge",
            "evidence support",
            "action basis",
            "commit",
            "push",
            "sync",
            "goal completion",
            "Prepare a separate merge proposal only",
        ]:
            if phrase not in packet:
                failures.append(f"packet_missing_phrase:{phrase}")

    fixture_files = sorted(FIXTURES_DIR.glob("*.json"))
    if len(fixture_files) != 3:
        failures.append(f"fixture_count_mismatch:{len(fixture_files)}")
    for fixture in fixture_files:
        record = load_json(fixture, failures)
        if not record:
            continue
        record_failures = validate_record(record)
        if record_failures:
            failures.append(f"fixture_invalid:{fixture.name}:{'|'.join(record_failures)}")

    failure_case_count = 0
    expected_failure_hits = 0
    if not failure_payload:
        failures.append("missing_failure_cases")
    else:
        cases = failure_payload.get("failure_cases", [])
        failure_case_count = len(cases)
        if failure_case_count < 8:
            failures.append(f"failure_case_count_too_low:{failure_case_count}")
        for case in cases:
            actual = validate_record(case.get("record", {}))
            expected = case.get("expected_failure")
            if expected in actual:
                expected_failure_hits += 1
            else:
                failures.append(f"failure_case_not_caught:{case.get('id')}:{expected}:{actual}")

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
        "fixture_count": len(fixture_files),
        "failure_case_count": failure_case_count,
        "expected_failure_hits": expected_failure_hits,
        "actual_opus_result_present": bool(control and control.get("current_state", {}).get("actual_opus_result_present")),
        "validated_opus_pass_present": bool(control and control.get("current_state", {}).get("validated_opus_pass_present")),
        "user_approval_present": bool(control and control.get("current_state", {}).get("user_approval_present")),
        "ready_for_merge_proposal": bool(control and control.get("current_state", {}).get("ready_for_merge_proposal")),
        "mainline_merge_allowed": bool(control and control.get("current_state", {}).get("mainline_merge_allowed")),
        "goal_complete_now": bool(control and control.get("current_state", {}).get("goal_complete_now")),
        "final_gate": final_gate,
    }
    return {"passed": not failures, "failures": failures, "summary": summary}


if __name__ == "__main__":
    result = verify(final_gate="--final-gate" in sys.argv)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["passed"] else 1)
