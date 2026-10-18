from __future__ import annotations

import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-88-old-file-normalization-user-decision-packet-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT = SLICE_ROOT / "artifact" / "old_file_normalization_user_decision_packet.json"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURES = SLICE_ROOT / "failure-cases" / "old-file-normalization-user-decision-packet-failures.json"
P2_75_CONTRACT = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request_contract.json"
P2_86_GATE_CHAIN = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-86-approval-to-prewrite-gate-chain-sandbox/artifact/approval_to_prewrite_gate_chain.json"
P2_87_DIFF_PREVIEW = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-87-old-file-status-normalization-diff-preview-sandbox/artifact/old_file_status_normalization_diff_preview.json"


REQUIRED_FILES = [
    "slice-plan.md",
    "source-map.md",
    "artifact/build_old_file_normalization_user_decision_packet.py",
    "artifact/verify_old_file_normalization_user_decision_packet.py",
    "artifact/old_file_normalization_user_decision_packet.json",
    "artifact/old_file_normalization_user_decision_packet.md",
    "artifact/old_file_normalization_user_decision_packet.html",
    "failure-cases/old-file-normalization-user-decision-packet-failures.json",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

REQUIRED_FIXTURES = {
    "exact-approval-phrase-present.json",
    "generic-language-still-not-approval.json",
    "diff-preview-75-clean.json",
    "decision-options-no-write-authority.json",
    "p2-75-gap-preserved.json",
}

REQUIRED_FAILURE_CASES = {
    "P2-88-FAIL-01-missing-exact-approval-phrase",
    "P2-88-FAIL-02-generic-language-treated-as-approval",
    "P2-88-FAIL-03-preview-count-not-75",
    "P2-88-FAIL-04-preview-cleanliness-not-proven",
    "P2-88-FAIL-05-packet-authorizes-write",
    "P2-88-FAIL-06-p2-75-gap-closed-without-user",
    "P2-88-FAIL-07-mainline-or-truth-authority",
    "P2-88-FAIL-08-missing-non-approval-option",
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
    p2_75 = load_json(P2_75_CONTRACT)
    p2_86 = load_json(P2_86_GATE_CHAIN)
    p2_87 = load_json(P2_87_DIFF_PREVIEW)
    exact_phrase = p2_75["exact_approval_phrase"]

    if payload.get("approval_contract", {}).get("exact_approval_phrase") != exact_phrase:
        failures.append("exact approval phrase missing or altered")
    if payload.get("approval_contract", {}).get("packet_collects_approval") is not False:
        failures.append("packet must not collect approval")
    if payload.get("approval_contract", {}).get("phrase_in_this_packet_is_instructional_only") is not True:
        failures.append("exact phrase display must be instructional only")
    if payload.get("approval_contract", {}).get("non_approval_examples") != p2_75["non_approval_examples"]:
        failures.append("non-approval examples drifted from p2-75")

    summary = payload.get("summary", {})
    expected_summary = {
        "original_items": 20,
        "status_changes": 75,
        "preview_operation_count": 75,
        "prewrite_hash_match_count": 75,
        "body_unchanged_count": 75,
        "non_status_frontmatter_unchanged_count": 75,
        "old_slice_writes_applied": 0,
        "p2_86_executor_write_allowed_now": False,
        "p2_86_positive_ready_count": 1,
        "p2_75_exact_approval_collected": False,
        "decision_option_count": 4,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            failures.append(f"summary mismatch for {key}: expected {expected!r}, got {summary.get(key)!r}")

    source_summary = p2_87.get("summary", {})
    for key in [
        "preview_operation_count",
        "prewrite_hash_match_count",
        "body_unchanged_count",
        "non_status_frontmatter_unchanged_count",
        "old_slice_writes_applied",
    ]:
        if summary.get(key) != source_summary.get(key):
            failures.append(f"summary does not match p2-87 for {key}")
    if summary.get("p2_86_executor_write_allowed_now") != p2_86["summary"]["executor_write_allowed_now"]:
        failures.append("executor write authority does not match p2-86")

    options = payload.get("decision_options", [])
    option_ids = {option.get("option_id") for option in options}
    required_options = {"approve_with_exact_phrase", "withhold_approval", "request_revision", "reject_or_park"}
    missing_options = required_options - option_ids
    if missing_options:
        failures.append(f"missing decision options: {sorted(missing_options)}")
    for option in options:
        if option.get("old_file_write_allowed_by_this_packet") is not False:
            failures.append(f"option writes now: {option.get('option_id')}")
    approve = next((option for option in options if option.get("option_id") == "approve_with_exact_phrase"), {})
    if approve.get("required_text") != exact_phrase:
        failures.append("approve option does not carry exact phrase")

    authority = payload.get("authority_flags", {})
    for key in [
        "phrase_display_is_user_approval",
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

    md_path = SLICE_ROOT / "artifact" / "old_file_normalization_user_decision_packet.md"
    html_path = SLICE_ROOT / "artifact" / "old_file_normalization_user_decision_packet.html"
    md_text = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
    html_text = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
    for needle in [
        "Exact Approval Phrase",
        exact_phrase,
        "approve_with_exact_phrase",
        "withhold_approval",
        "request_revision",
        "reject_or_park",
        "Old slice writes applied: 0",
        "This is a decision packet only.",
    ]:
        if needle not in md_text:
            failures.append(f"markdown missing: {needle[:60]}")
    for needle in [
        "p2-88 Old-File Normalization Decision Packet",
        exact_phrase,
        "Decision packet only",
        "false",
    ]:
        if needle not in html_text:
            failures.append(f"html missing: {needle[:60]}")

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
            "preview_operation_count": summary.get("preview_operation_count"),
            "decision_option_count": summary.get("decision_option_count"),
            "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
            "p2_75_exact_approval_collected": summary.get("p2_75_exact_approval_collected"),
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
