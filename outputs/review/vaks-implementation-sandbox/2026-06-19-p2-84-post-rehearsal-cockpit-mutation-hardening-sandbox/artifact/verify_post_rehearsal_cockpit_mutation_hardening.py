from __future__ import annotations

import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-84-post-rehearsal-cockpit-mutation-hardening-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT = SLICE_ROOT / "artifact" / "post_rehearsal_cockpit_mutation_hardening.json"
FAILURES = SLICE_ROOT / "failure-cases" / "post-rehearsal-cockpit-mutation-hardening-failures.json"
BASELINE = SLICE_ROOT / "fixtures" / "baseline-p2-83-cockpit.json"
MUTANTS_DIR = SLICE_ROOT / "fixtures" / "mutants"


REQUIRED_FILES = [
    "slice-plan.md",
    "source-map.md",
    "artifact/build_post_rehearsal_cockpit_mutation_hardening.py",
    "artifact/verify_post_rehearsal_cockpit_mutation_hardening.py",
    "artifact/post_rehearsal_cockpit_mutation_hardening.json",
    "artifact/post_rehearsal_cockpit_mutation_hardening.md",
    "artifact/post_rehearsal_cockpit_mutation_hardening.html",
    "fixtures/baseline-p2-83-cockpit.json",
    "failure-cases/post-rehearsal-cockpit-mutation-hardening-failures.json",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

EXPECTED_MUTATIONS = {
    "MUT-01-all-done-overclaim": "all_done_overclaim",
    "MUT-02-generic-continuation-as-approval": "generic_continuation_as_approval",
    "MUT-03-rehearsal-as-write-authority": "rehearsal_as_write_authority",
    "MUT-04-missing-byte-safety-rollup": "missing_byte_safety_rollup",
    "MUT-05-stale-pre-p2-82-status-surface": "stale_pre_p2_82_status_surface",
    "MUT-06-mainline-authority-confusion": "mainline_authority_confusion",
    "MUT-07-product-acceptance-as-user-approval": "product_acceptance_as_user_approval",
    "MUT-08-path-boundary-violation": "path_boundary_violation",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def planned_write_within_slice(path: str) -> bool:
    norm = path.replace("\\", "/")
    allowed = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"
    return norm.startswith(allowed)


def validate_cockpit(payload: dict) -> list[str]:
    failures: list[str] = []
    summary = payload.get("status_summary", {})
    plain = payload.get("plain_answer", {})
    decision = payload.get("decision_matrix", {})
    authority = payload.get("authority_flags", {})
    sources = payload.get("source_inputs", {})

    if summary.get("old_slice_current_strict_final_gate_count") != 0:
        failures.append("old_file_strict_count_changed")
    if summary.get("pending_status_change_count") != 75:
        failures.append("pending_status_change_count_changed")
    if summary.get("old_slice_writes_applied") != 0:
        failures.append("old_slice_write_applied")
    if summary.get("goal_complete_now") is not False or plain.get("all_done_product_grade") is not False or decision.get("can_claim_all_done") is not False:
        failures.append("all_done_overclaim")

    first_route = (payload.get("next_action_router") or [{}])[0]
    if first_route.get("old_file_write_allowed") is not False:
        failures.append("generic_continuation_as_approval")

    if decision.get("can_execute_old_file_normalization_now") is not False or authority.get("executor_write_allowed") is not False:
        failures.append("rehearsal_as_write_authority")

    if summary.get("p2_82_final_copy_byte_hash_restored_count") != 75:
        failures.append("missing_byte_safety_rollup")

    if "p2_82_copy_rehearsal" not in sources or summary.get("p2_82_fixture_copy_count") != 75:
        failures.append("stale_pre_p2_82_status_surface")

    if decision.get("can_merge_mainline_now") is not False or authority.get("mainline_ready") is not False or authority.get("promotion_ready") is not False or authority.get("reviewed_knowledge_ready") is not False or authority.get("action_basis_ready") is not False:
        failures.append("mainline_authority_confusion")

    if decision.get("can_treat_product_acceptance_as_user_write_approval") is not False or authority.get("approval_collected") is not False:
        failures.append("product_acceptance_as_user_approval")

    for path in payload.get("planned_write_paths", []):
        if not planned_write_within_slice(str(path)):
            failures.append("path_boundary_violation")
            break

    return sorted(set(failures))


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
    baseline = load_json(BASELINE) if BASELINE.exists() else {}

    baseline_failures = validate_cockpit(baseline)
    if baseline_failures:
        failures.append(f"baseline cockpit should pass but failed: {baseline_failures}")

    mutant_files = sorted(MUTANTS_DIR.glob("MUT-*.json")) if MUTANTS_DIR.exists() else []
    if len(mutant_files) != len(EXPECTED_MUTATIONS):
        failures.append(f"expected {len(EXPECTED_MUTATIONS)} mutant files, found {len(mutant_files)}")

    mutant_results = []
    for mutant_path in mutant_files:
        case_id = mutant_path.stem
        observed = validate_cockpit(load_json(mutant_path))
        expected = EXPECTED_MUTATIONS.get(case_id)
        failed_as_expected = expected in observed
        mutant_results.append(
            {
                "case_id": case_id,
                "expected_failure_code": expected,
                "observed_failures": observed,
                "failed_as_expected": failed_as_expected,
            }
        )
        if not failed_as_expected:
            failures.append(f"{case_id} did not fail with expected code {expected}; observed {observed}")

    if payload.get("slice_id") != SLICE_ID:
        failures.append("artifact slice_id mismatch")
    summary = payload.get("summary", {})
    expected_summary = {
        "baseline_passed": True,
        "baseline_failure_count": 0,
        "mutation_count": 8,
        "expected_mutation_fail_count": 8,
        "unexpected_pass_count": 0,
        "unexpected_failure_count": 0,
        "old_slice_writes_applied": 0,
        "p2_83_files_modified": 0,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            failures.append(f"summary mismatch for {key}: expected {expected!r}, got {summary.get(key)!r}")

    report_results = {item.get("case_id"): item for item in payload.get("mutation_results", [])}
    for case_id, expected in EXPECTED_MUTATIONS.items():
        result = report_results.get(case_id)
        if not result:
            failures.append(f"report missing mutation result: {case_id}")
            continue
        if result.get("expected_failure_code") != expected:
            failures.append(f"{case_id} report expected code mismatch")
        if result.get("failed_as_expected") is not True:
            failures.append(f"{case_id} report did not mark failed_as_expected")

    failure_payload = load_json(FAILURES) if FAILURES.exists() else {"failure_cases": []}
    failure_case_ids = {case.get("case_id") for case in failure_payload.get("failure_cases", [])}
    missing_failure_cases = set(EXPECTED_MUTATIONS) - failure_case_ids
    if missing_failure_cases:
        failures.append(f"missing failure case records: {sorted(missing_failure_cases)}")

    md_text = (SLICE_ROOT / "artifact" / "post_rehearsal_cockpit_mutation_hardening.md").read_text(encoding="utf-8") if (SLICE_ROOT / "artifact" / "post_rehearsal_cockpit_mutation_hardening.md").exists() else ""
    html_text = (SLICE_ROOT / "artifact" / "post_rehearsal_cockpit_mutation_hardening.html").read_text(encoding="utf-8") if (SLICE_ROOT / "artifact" / "post_rehearsal_cockpit_mutation_hardening.html").exists() else ""
    for needle in ["baseline_passed: true", "expected_mutation_fail_count: 8", "unexpected_pass_count: 0"]:
        if needle not in md_text:
            failures.append(f"markdown report missing: {needle}")
    for needle in ["Mutation Hardening", "Failed As Expected", "8/8"]:
        if needle not in html_text:
            failures.append(f"html report missing: {needle}")

    authority = payload.get("authority_flags", {})
    for key in [
        "p2_83_write_allowed",
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
        failures.append("old_slice_writes_applied authority flag must be 0")

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
            "baseline_passed": not baseline_failures,
            "mutation_file_count": len(mutant_files),
            "expected_mutation_fail_count": sum(1 for item in mutant_results if item["failed_as_expected"]),
            "unexpected_pass_count": sum(1 for item in mutant_results if not item["observed_failures"]),
            "failure_case_count": len(failure_case_ids),
            "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
            "p2_83_files_modified": summary.get("p2_83_files_modified"),
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
