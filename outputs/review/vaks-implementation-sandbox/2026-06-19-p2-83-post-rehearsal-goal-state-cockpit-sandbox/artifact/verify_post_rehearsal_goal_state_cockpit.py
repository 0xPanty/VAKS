from __future__ import annotations

import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT = SLICE_ROOT / "artifact" / "post_rehearsal_goal_state_cockpit.json"
FAILURES = SLICE_ROOT / "failure-cases" / "post-rehearsal-goal-state-cockpit-failures.json"
FIXTURES_DIR = SLICE_ROOT / "fixtures"


REQUIRED_FILES = [
    "slice-plan.md",
    "source-map.md",
    "artifact/build_post_rehearsal_goal_state_cockpit.py",
    "artifact/verify_post_rehearsal_goal_state_cockpit.py",
    "artifact/post_rehearsal_goal_state_cockpit.json",
    "artifact/post_rehearsal_goal_state_cockpit.md",
    "artifact/post_rehearsal_goal_state_cockpit.html",
    "failure-cases/post-rehearsal-goal-state-cockpit-failures.json",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

REQUIRED_FIXTURES = {
    "positive-post-rehearsal-state.json",
    "positive-user-answer-classification.json",
    "positive-operator-decision-matrix.json",
    "positive-byte-safety-evidence-rollup.json",
    "positive-authority-boundary-rollup.json",
}

REQUIRED_FAILURE_CASES = {
    "P2-83-FAIL-01-all-done-overclaim",
    "P2-83-FAIL-02-generic-continuation-as-approval",
    "P2-83-FAIL-03-rehearsal-as-write-authority",
    "P2-83-FAIL-04-missing-byte-safety-rollup",
    "P2-83-FAIL-05-stale-pre-p2-82-status-surface",
    "P2-83-FAIL-06-mainline-authority-confusion",
    "P2-83-FAIL-07-product-acceptance-confusion",
    "P2-83-FAIL-08-path-boundary-violation",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel_json(rel: str) -> dict:
    return load_json(REPO_ROOT / rel)


def frontmatter_status(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    for line in lines[1:]:
        if line == "---":
            break
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return None


def check(final_gate: bool = False) -> dict:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (SLICE_ROOT / rel).exists():
            failures.append(f"missing required file: {rel}")

    fixture_names = {path.name for path in FIXTURES_DIR.glob("*.json")}
    missing_fixtures = REQUIRED_FIXTURES - fixture_names
    if missing_fixtures:
        failures.append(f"missing fixtures: {sorted(missing_fixtures)}")

    if not ARTIFACT.exists():
        payload = {}
    else:
        payload = load_json(ARTIFACT)

    if not FAILURES.exists():
        failure_payload = {"failure_cases": []}
    else:
        failure_payload = load_json(FAILURES)
    failure_ids = {case.get("case_id") for case in failure_payload.get("failure_cases", [])}
    missing_failure_cases = REQUIRED_FAILURE_CASES - failure_ids
    if missing_failure_cases:
        failures.append(f"missing failure cases: {sorted(missing_failure_cases)}")

    if payload.get("slice_id") != SLICE_ID:
        failures.append("artifact slice_id mismatch")

    summary = payload.get("status_summary", {})
    expected_summary = {
        "original_items": 20,
        "legacy_product_acceptance_evidence_count": 20,
        "legacy_core_pass_evidence_count": 20,
        "sidecar_closeout_passed_count": 20,
        "old_slice_current_strict_final_gate_count": 0,
        "pending_status_change_count": 75,
        "transaction_operation_count": 75,
        "p2_82_fixture_copy_count": 75,
        "p2_82_fixture_apply_write_count": 75,
        "p2_82_fixture_rollback_write_count": 75,
        "p2_82_final_copy_byte_hash_restored_count": 75,
        "old_slice_writes_applied": 0,
        "goal_complete_now": False,
        "p2_82_product_acceptance_status": "pass_product_grade",
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            failures.append(f"summary mismatch for {key}: expected {expected!r}, got {summary.get(key)!r}")

    decision = payload.get("decision_matrix", {})
    decision_expectations = {
        "can_continue_sandbox_only": True,
        "can_claim_all_done": False,
        "can_execute_old_file_normalization_now": False,
        "can_merge_mainline_now": False,
        "can_treat_retrieval_as_evidence_support": False,
        "can_treat_product_acceptance_as_user_write_approval": False,
        "requires_exact_p2_75_phrase_for_old_file_write": True,
    }
    for key, expected in decision_expectations.items():
        if decision.get(key) is not expected:
            failures.append(f"decision mismatch for {key}: expected {expected!r}, got {decision.get(key)!r}")

    authority = payload.get("authority_flags", {})
    false_authority_fields = [
        "approval_collected",
        "executor_write_allowed",
        "old_slice_write_allowed_now",
        "normalization_applied",
        "mainline_ready",
        "promotion_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
        "action_basis_ready",
        "goal_complete_now",
    ]
    for key in false_authority_fields:
        if authority.get(key) is not False:
            failures.append(f"authority flag must remain false: {key}")
    if authority.get("old_slice_writes_applied") != 0:
        failures.append("authority old_slice_writes_applied must be 0")

    source_inputs = payload.get("source_inputs", {})
    if "p2_82_copy_rehearsal" not in source_inputs:
        failures.append("artifact does not incorporate p2-82 rehearsal source")

    p2_78 = rel_json("outputs/review/vaks-implementation-sandbox/2026-06-19-p2-78-goal-completion-gap-ledger-sandbox/artifact/goal_completion_gap_ledger.json")
    if p2_78["goal_verdict"]["goal_complete_now"] is not False:
        failures.append("source p2-78 unexpectedly says goal complete")

    p2_82 = rel_json("outputs/review/vaks-implementation-sandbox/2026-06-19-p2-82-old-file-status-normalization-sandbox-copy-executor-rehearsal-sandbox/artifact/sandbox_copy_executor_rehearsal.json")
    if p2_82["summary"]["final_copy_byte_sha_match_count"] != 75:
        failures.append("source p2-82 final byte hash count is not 75")
    if p2_82["gate"]["executor_write_allowed_now"] is not False:
        failures.append("source p2-82 unexpectedly allows executor writes")

    p2_75 = rel_json("outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request.json")
    if p2_75["current_state"]["user_approval_collected"] is not False:
        failures.append("source p2-75 unexpectedly has user approval")

    md_text = (SLICE_ROOT / "artifact" / "post_rehearsal_goal_state_cockpit.md").read_text(encoding="utf-8") if (SLICE_ROOT / "artifact" / "post_rehearsal_goal_state_cockpit.md").exists() else ""
    html_text = (SLICE_ROOT / "artifact" / "post_rehearsal_goal_state_cockpit.html").read_text(encoding="utf-8") if (SLICE_ROOT / "artifact" / "post_rehearsal_goal_state_cockpit.html").exists() else ""
    for needle in ["old-file current strict final-gate complete: 0", "p2-82 byte-safe fixture rollback: 75/75", "old slice writes applied: 0"]:
        if needle not in md_text:
            failures.append(f"markdown cockpit missing: {needle}")
    for needle in ["Old-file strict complete", "p2-82 byte-safe rollback", "sandbox-only"]:
        if needle not in html_text:
            failures.append(f"html cockpit missing: {needle}")

    if final_gate:
        report_statuses = {
            "verification.md": "local_verification_passed",
            "reviewer-report.md": "review_pass_no_blocker",
            "boundary-audit.md": "pass_boundary",
            "product-acceptance-report.md": "pass_product_grade",
            "next-step.md": "pass_product_grade_pending_next_slice",
        }
        for rel, expected in report_statuses.items():
            actual = frontmatter_status(SLICE_ROOT / rel)
            if actual != expected:
                failures.append(f"{rel} status expected {expected!r}, got {actual!r}")

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": len(fixture_names),
            "failure_case_count": len(failure_ids),
            "original_items": summary.get("original_items"),
            "sidecar_closeout_passed_count": summary.get("sidecar_closeout_passed_count"),
            "old_slice_current_strict_final_gate_count": summary.get("old_slice_current_strict_final_gate_count"),
            "pending_status_change_count": summary.get("pending_status_change_count"),
            "p2_82_final_copy_byte_hash_restored_count": summary.get("p2_82_final_copy_byte_hash_restored_count"),
            "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
            "goal_complete_now": summary.get("goal_complete_now"),
            "final_gate": final_gate,
        },
    }
    return result


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = check(final_gate=args.final_gate)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
