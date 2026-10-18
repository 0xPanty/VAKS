from __future__ import annotations

import hashlib
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-86-approval-to-prewrite-gate-chain-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT = SLICE_ROOT / "artifact" / "approval_to_prewrite_gate_chain.json"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURES = SLICE_ROOT / "failure-cases" / "approval-to-prewrite-gate-chain-failures.json"
P2_80 = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json"


REQUIRED_FILES = [
    "slice-plan.md",
    "source-map.md",
    "artifact/build_approval_to_prewrite_gate_chain.py",
    "artifact/verify_approval_to_prewrite_gate_chain.py",
    "artifact/approval_to_prewrite_gate_chain.json",
    "artifact/approval_to_prewrite_gate_chain.md",
    "artifact/approval_to_prewrite_gate_chain.html",
    "failure-cases/approval-to-prewrite-gate-chain-failures.json",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

EXPECTED_STATES = {
    "POS-01-exact-clean-prewrite-ready": "ready_for_prewrite_confirmation",
    "NEG-01-generic-continuation": "blocked_no_exact_approval",
    "NEG-02-product-acceptance-as-approval": "blocked_no_exact_approval",
    "NEG-03-hash-drift": "blocked_prewrite_hash_or_missing_target",
    "NEG-04-missing-rehearsal": "blocked_missing_byte_safe_rehearsal",
    "NEG-05-boundary-not-passed": "blocked_boundary_not_passed",
    "NEG-06-mainline-request": "blocked_mainline_authority_request",
    "NEG-07-immediate-write-request": "blocked_immediate_write_request",
}

EXPECTED_FAILURE_CASES = {
    "P2-86-FAIL-01-generic-approval",
    "P2-86-FAIL-02-product-acceptance-approval",
    "P2-86-FAIL-03-hash-drift-override",
    "P2-86-FAIL-04-missing-rehearsal-override",
    "P2-86-FAIL-05-boundary-override",
    "P2-86-FAIL-06-mainline-authority-confusion",
    "P2-86-FAIL-07-immediate-write-confusion",
    "P2-86-FAIL-08-fixture-approval-confusion",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def check_current_hashes() -> dict:
    p2_80 = load_json(P2_80)
    results = []
    for op in p2_80["transaction_operations"]:
        path = REPO_ROOT / op["target_path"]
        exists = path.exists()
        current_hash = sha256_bytes(path.read_bytes()) if exists else None
        results.append(
            {
                "exists": exists,
                "matches": exists and current_hash == op["prewrite_required_hash"],
            }
        )
    return {
        "target_count": len(results),
        "exists_count": sum(1 for item in results if item["exists"]),
        "hash_match_count": sum(1 for item in results if item["matches"]),
        "missing_count": sum(1 for item in results if not item["exists"]),
        "hash_mismatch_count": sum(1 for item in results if item["exists"] and not item["matches"]),
    }


def check(final_gate: bool = False) -> dict:
    failures: list[str] = []
    for rel in REQUIRED_FILES:
        if not (SLICE_ROOT / rel).exists():
            failures.append(f"missing required file: {rel}")

    payload = load_json(ARTIFACT) if ARTIFACT.exists() else {}
    summary = payload.get("summary", {})
    current_hashes = check_current_hashes()
    if current_hashes["target_count"] != 75:
        failures.append("current hash target count is not 75")
    if current_hashes["hash_match_count"] != 75:
        failures.append(f"current hash match count is not 75: {current_hashes}")
    if summary.get("fresh_hash_match_count") != current_hashes["hash_match_count"]:
        failures.append("artifact fresh hash match count does not match current read")

    expected_summary = {
        "target_count": 75,
        "fresh_hash_match_count": 75,
        "fresh_hash_mismatch_count": 0,
        "fresh_missing_count": 0,
        "p2_82_final_copy_byte_hash_restored_count": 75,
        "p2_83_goal_complete_now": False,
        "scenario_count": 8,
        "positive_ready_count": 1,
        "negative_blocked_count": 7,
        "executor_write_allowed_now": False,
        "old_slice_writes_applied": 0,
        "user_approval_collected_by_this_slice": False,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            failures.append(f"summary mismatch for {key}: expected {expected!r}, got {summary.get(key)!r}")

    fixture_files = sorted(FIXTURES_DIR.glob("*.json")) if FIXTURES_DIR.exists() else []
    if len(fixture_files) != len(EXPECTED_STATES):
        failures.append(f"expected {len(EXPECTED_STATES)} fixture files, found {len(fixture_files)}")

    result_by_id = {item.get("scenario_id"): item for item in payload.get("gate_results", [])}
    for scenario_id, expected_state in EXPECTED_STATES.items():
        result = result_by_id.get(scenario_id)
        if not result:
            failures.append(f"missing gate result: {scenario_id}")
            continue
        if result.get("gate_state") != expected_state:
            failures.append(f"{scenario_id} expected {expected_state}, got {result.get('gate_state')}")
        if result.get("executor_write_allowed_now") is not False:
            failures.append(f"{scenario_id} grants write authority")
        if result.get("old_slice_writes_applied") != 0:
            failures.append(f"{scenario_id} applied old-slice writes")
        if result.get("fixture_match_is_user_approval") is not False:
            failures.append(f"{scenario_id} treats fixture as user approval")

    for fixture_path in fixture_files:
        fixture = load_json(fixture_path)
        result = fixture.get("result", {})
        expected = EXPECTED_STATES.get(fixture.get("scenario_id"))
        if result.get("gate_state") != expected:
            failures.append(f"fixture {fixture_path.name} gate_state mismatch")

    failure_payload = load_json(FAILURES) if FAILURES.exists() else {"failure_cases": []}
    failure_ids = {case.get("case_id") for case in failure_payload.get("failure_cases", [])}
    missing_failure_cases = EXPECTED_FAILURE_CASES - failure_ids
    if missing_failure_cases:
        failures.append(f"missing failure cases: {sorted(missing_failure_cases)}")

    authority = payload.get("authority_flags", {})
    for key in [
        "fixture_exact_phrase_is_user_approval",
        "approval_collected",
        "ready_for_prewrite_is_write_authority",
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

    md_text = (SLICE_ROOT / "artifact" / "approval_to_prewrite_gate_chain.md").read_text(encoding="utf-8") if (SLICE_ROOT / "artifact" / "approval_to_prewrite_gate_chain.md").exists() else ""
    html_text = (SLICE_ROOT / "artifact" / "approval_to_prewrite_gate_chain.html").read_text(encoding="utf-8") if (SLICE_ROOT / "artifact" / "approval_to_prewrite_gate_chain.html").exists() else ""
    for needle in ["fresh_hash_match_count: 75", "positive_ready_count: 1", "executor_write_allowed_now: false"]:
        if needle not in md_text:
            failures.append(f"markdown missing: {needle}")
    for needle in ["Approval To Prewrite Gate", "Ready-for-prewrite is not old-file write authority", "75/75"]:
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
            "fixture_count": len(fixture_files),
            "fresh_hash_match_count": summary.get("fresh_hash_match_count"),
            "positive_ready_count": summary.get("positive_ready_count"),
            "negative_blocked_count": summary.get("negative_blocked_count"),
            "executor_write_allowed_now": summary.get("executor_write_allowed_now"),
            "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
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
