from __future__ import annotations

import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-89-approval-dependency-closeout-packet-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT = SLICE_ROOT / "artifact" / "approval_dependency_closeout_packet.json"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURES = SLICE_ROOT / "failure-cases" / "approval-dependency-closeout-failures.json"
P2_88 = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-88-old-file-normalization-user-decision-packet-sandbox/artifact/old_file_normalization_user_decision_packet.json"


REQUIRED_FILES = [
    "slice-plan.md",
    "source-map.md",
    "artifact/build_approval_dependency_closeout_packet.py",
    "artifact/verify_approval_dependency_closeout_packet.py",
    "artifact/approval_dependency_closeout_packet.json",
    "artifact/approval_dependency_closeout_packet.md",
    "artifact/approval_dependency_closeout_packet.html",
    "failure-cases/approval-dependency-closeout-failures.json",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

REQUIRED_FIXTURES = {
    "technical-readiness-clean.json",
    "approval-gap-open.json",
    "executor-not-authorized.json",
    "goal-not-complete.json",
    "decision-packet-linked.json",
}

REQUIRED_FAILURE_CASES = {
    "P2-89-FAIL-01-claims-approval-collected",
    "P2-89-FAIL-02-executor-write-allowed",
    "P2-89-FAIL-03-old-writes-applied",
    "P2-89-FAIL-04-goal-complete",
    "P2-89-FAIL-05-missing-technical-evidence",
    "P2-89-FAIL-06-missing-next-stop-rule",
    "P2-89-FAIL-07-mainline-or-truth-authority",
    "P2-89-FAIL-08-missing-user-decision-link",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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

    payload = load_json(ARTIFACT) if ARTIFACT.exists() else {}
    p88 = load_json(P2_88)
    readiness = payload.get("technical_readiness", {})
    dependency = payload.get("approval_dependency", {})
    executor = payload.get("executor_status", {})
    authority = payload.get("authority_flags", {})

    expected_readiness = {
        "status_changes": 75,
        "preview_operation_count": 75,
        "prewrite_hash_match_count": 75,
        "body_unchanged_count": 75,
        "non_status_frontmatter_unchanged_count": 75,
        "old_slice_writes_applied": 0,
        "decision_option_count": 4,
        "p2_86_positive_ready_count": 1,
    }
    for key, expected in expected_readiness.items():
        if readiness.get(key) != expected:
            failures.append(f"readiness mismatch for {key}: expected {expected!r}, got {readiness.get(key)!r}")
    if readiness.get("decision_option_count") != p88["summary"]["decision_option_count"]:
        failures.append("decision option count does not match p2-88")

    if dependency.get("blocking_condition") != "missing_exact_p2_75_user_approval":
        failures.append("missing exact approval blocking condition not preserved")
    if dependency.get("exact_approval_collected") is not False:
        failures.append("exact approval must remain uncollected")
    if dependency.get("generic_language_is_not_approval") is not True:
        failures.append("generic language must remain non-approval")
    if dependency.get("decision_packet") != "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-88-old-file-normalization-user-decision-packet-sandbox/artifact/old_file_normalization_user_decision_packet.json":
        failures.append("p2-88 decision packet link missing")

    expected_executor_false = [
        "executor_write_allowed_now",
        "old_slice_write_allowed",
    ]
    for key in expected_executor_false:
        if executor.get(key) is not False:
            failures.append(f"executor flag must be false: {key}")
    for key in [
        "ready_for_prewrite_confirmation_only",
        "requires_exact_approval_before_executor_slice",
        "requires_fresh_prewrite_gate_after_approval",
        "requires_stop_before_any_old_file_write",
    ]:
        if executor.get(key) is not True:
            failures.append(f"executor stop rule must be true: {key}")

    for key in [
        "user_approval_collected",
        "packet_authorizes_write",
        "executor_write_allowed",
        "old_slice_write_allowed",
        "normalization_applied",
        "mainline_ready",
        "promotion_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
        "action_basis_ready",
        "goal_complete_now",
    ]:
        if authority.get(key) is not False:
            failures.append(f"authority flag must remain false: {key}")
    if authority.get("old_slice_writes_applied") != 0:
        failures.append("authority old_slice_writes_applied must be 0")

    fixture_names = {path.name for path in FIXTURES_DIR.glob("*.json")} if FIXTURES_DIR.exists() else set()
    missing_fixtures = REQUIRED_FIXTURES - fixture_names
    if missing_fixtures:
        failures.append(f"missing fixtures: {sorted(missing_fixtures)}")

    failure_payload = load_json(FAILURES) if FAILURES.exists() else {"failure_cases": []}
    failure_ids = {case.get("case_id") for case in failure_payload.get("failure_cases", [])}
    missing_failure_cases = REQUIRED_FAILURE_CASES - failure_ids
    if missing_failure_cases:
        failures.append(f"missing failure cases: {sorted(missing_failure_cases)}")

    md_path = SLICE_ROOT / "artifact" / "approval_dependency_closeout_packet.md"
    html_path = SLICE_ROOT / "artifact" / "approval_dependency_closeout_packet.html"
    md_text = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
    html_text = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
    for needle in [
        "missing_exact_p2_75_user_approval",
        "old_slice_writes_applied: 0",
        "goal completion",
        "not approval",
        "not write authority",
    ]:
        if needle not in md_text:
            failures.append(f"markdown missing: {needle}")
    for needle in [
        "p2-89 Approval Dependency Closeout",
        "Approval collected",
        "false",
        "Unsafe Actions",
    ]:
        if needle not in html_text:
            failures.append(f"html missing: {needle}")

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
            "preview_operation_count": readiness.get("preview_operation_count"),
            "old_slice_writes_applied": readiness.get("old_slice_writes_applied"),
            "exact_approval_collected": dependency.get("exact_approval_collected"),
            "executor_write_allowed_now": executor.get("executor_write_allowed_now"),
            "goal_complete_now": authority.get("goal_complete_now"),
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
