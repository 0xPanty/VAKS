from __future__ import annotations

import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-90-post-approval-executor-handoff-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
ARTIFACT = SLICE_ROOT / "artifact" / "post_approval_executor_handoff.json"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURES = SLICE_ROOT / "failure-cases" / "post-approval-executor-handoff-failures.json"

REQUIRED_FILES = [
    "slice-plan.md",
    "source-map.md",
    "artifact/build_post_approval_executor_handoff.py",
    "artifact/verify_post_approval_executor_handoff.py",
    "artifact/post_approval_executor_handoff.json",
    "artifact/post_approval_executor_handoff.md",
    "artifact/post_approval_executor_handoff.html",
    "failure-cases/post-approval-executor-handoff-failures.json",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

REQUIRED_FIXTURES = {
    "current-execution-blocked.json",
    "future-prewrite-required.json",
    "status-only-scope.json",
    "protected-paths-excluded.json",
    "handoff-not-goal-complete.json",
}

REQUIRED_FAILURE_CASES = {
    "P2-90-FAIL-01-claims-current-write-authority",
    "P2-90-FAIL-02-skips-fresh-prewrite-gate",
    "P2-90-FAIL-03-missing-exact-approval-prerequisite",
    "P2-90-FAIL-04-target-count-drift",
    "P2-90-FAIL-05-allows-body-or-artifact-edits",
    "P2-90-FAIL-06-missing-rollback-or-audit",
    "P2-90-FAIL-07-mainline-or-truth-authority",
    "P2-90-FAIL-08-goal-complete",
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
    current = payload.get("current_status", {})
    prereq = payload.get("future_prerequisites", {})
    scope = payload.get("executor_scope_if_future_gate_passes", {})
    authority = payload.get("authority_flags", {})

    expected_current = {
        "exact_approval_collected_now": False,
        "executor_write_allowed_now": False,
        "old_slice_writes_applied": 0,
        "goal_complete_now": False,
        "blocking_condition": "missing_exact_p2_75_user_approval",
    }
    for key, expected in expected_current.items():
        if current.get(key) != expected:
            failures.append(f"current status mismatch for {key}: expected {expected!r}, got {current.get(key)!r}")

    for key in [
        "exact_approval_required",
        "fresh_prewrite_gate_required_after_approval",
        "fresh_boundary_audit_required_after_approval",
        "stop_before_any_write_required",
    ]:
        if prereq.get(key) is not True:
            failures.append(f"future prerequisite must be true: {key}")
    if not prereq.get("exact_approval_phrase", "").startswith("I explicitly approve p2-75"):
        failures.append("exact approval phrase missing")

    expected_scope = {
        "allowed_edit_kind": "status_only_frontmatter_normalization",
        "allowed_field": "frontmatter.status",
        "operation_count": 75,
        "unique_target_file_count": 75,
        "body_content_edits_allowed": False,
        "artifact_edits_allowed": False,
        "tools_templates_edits_allowed": False,
        "wiki_truth_layer_edits_allowed": False,
        "mainline_edits_allowed": False,
        "obsidian_sync_allowed": False,
        "commit_push_allowed": False,
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            failures.append(f"scope mismatch for {key}: expected {expected!r}, got {scope.get(key)!r}")

    stages = payload.get("future_executor_stages", [])
    if len(stages) != 5:
        failures.append(f"expected 5 future executor stages, found {len(stages)}")
    if any(stage.get("write_allowed") is True for stage in stages[:4]):
        failures.append("pre-apply stages must not allow writes")

    if len(payload.get("future_verification_requirements", [])) < 6:
        failures.append("future verification requirements too thin")

    for key in [
        "user_approval_collected",
        "handoff_authorizes_write",
        "executor_write_allowed_now",
        "old_slice_write_allowed_now",
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

    md_path = SLICE_ROOT / "artifact" / "post_approval_executor_handoff.md"
    html_path = SLICE_ROOT / "artifact" / "post_approval_executor_handoff.html"
    md_text = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
    html_text = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
    for needle in [
        "executor_write_allowed_now: `false`",
        "fresh_prewrite_gate_required_after_approval: `true`",
        "operation_count: 75",
        "not write authority",
        "not goal completion",
    ]:
        if needle not in md_text:
            failures.append(f"markdown missing: {needle}")
    for needle in [
        "p2-90 Post-Approval Executor Handoff",
        "Write allowed now",
        "false",
        "Future Executor Stages",
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
            "operation_count": scope.get("operation_count"),
            "exact_approval_collected_now": current.get("exact_approval_collected_now"),
            "executor_write_allowed_now": current.get("executor_write_allowed_now"),
            "fresh_prewrite_gate_required_after_approval": prereq.get("fresh_prewrite_gate_required_after_approval"),
            "old_slice_writes_applied": current.get("old_slice_writes_applied"),
            "goal_complete_now": current.get("goal_complete_now"),
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
