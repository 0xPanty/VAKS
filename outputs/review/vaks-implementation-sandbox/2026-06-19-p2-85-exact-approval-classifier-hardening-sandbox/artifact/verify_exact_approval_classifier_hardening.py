from __future__ import annotations

import hashlib
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-85-exact-approval-classifier-hardening-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT = SLICE_ROOT / "artifact" / "exact_approval_classifier_hardening.json"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURES = SLICE_ROOT / "failure-cases" / "exact-approval-classifier-failures.json"
P2_75 = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request.json"


REQUIRED_FILES = [
    "slice-plan.md",
    "source-map.md",
    "artifact/build_exact_approval_classifier_hardening.py",
    "artifact/verify_exact_approval_classifier_hardening.py",
    "artifact/exact_approval_classifier_hardening.json",
    "artifact/exact_approval_classifier_hardening.md",
    "artifact/exact_approval_classifier_hardening.html",
    "failure-cases/exact-approval-classifier-failures.json",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

EXPECTED_CASES = {
    "POS-01-exact-phrase": True,
    "NEG-01-chinese-generic-continue": False,
    "NEG-02-english-generic-go-ahead": False,
    "NEG-03-paraphrase": False,
    "NEG-04-partial-phrase": False,
    "NEG-05-wrong-count": False,
    "NEG-06-missing-prohibitions": False,
    "NEG-07-extra-authority": False,
    "NEG-08-whitespace-variation": False,
    "NEG-09-case-variation": False,
}

EXPECTED_FAILURE_CASES = {
    "P2-85-FAIL-01-generic-chinese-approval-confusion",
    "P2-85-FAIL-02-generic-english-approval-confusion",
    "P2-85-FAIL-03-paraphrase-approval-confusion",
    "P2-85-FAIL-04-partial-phrase-approval-confusion",
    "P2-85-FAIL-05-wrong-count-approval-confusion",
    "P2-85-FAIL-06-missing-prohibitions-approval-confusion",
    "P2-85-FAIL-07-extra-authority-approval-confusion",
    "P2-85-FAIL-08-whitespace-or-case-normalization-confusion",
    "P2-85-FAIL-09-classifier-pass-as-user-approval",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def classify(text: str, exact_phrase: str) -> dict:
    matched = text == exact_phrase
    return {
        "matched_exact_phrase": matched,
        "approval_class": "exact_p2_75_approval" if matched else "not_approval",
        "old_file_write_allowed_by_this_slice": False,
        "requires_future_executor_slice": matched,
    }


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
    p2_75 = load_json(P2_75)
    exact_phrase = p2_75["request"]["exact_approval_phrase"]
    contract = payload.get("approval_contract", {})
    if contract.get("exact_phrase") != exact_phrase:
        failures.append("contract exact phrase does not match p2-75 source")
    if contract.get("exact_phrase_sha256") != sha256_text(exact_phrase):
        failures.append("contract exact phrase sha mismatch")
    if contract.get("match_rule") != "input_text == exact_phrase":
        failures.append("match rule is not strict equality")
    if contract.get("normalization_allowed") is not False:
        failures.append("normalization must not be allowed")

    fixture_files = sorted(FIXTURES_DIR.glob("*.json")) if FIXTURES_DIR.exists() else []
    if len(fixture_files) != len(EXPECTED_CASES):
        failures.append(f"expected {len(EXPECTED_CASES)} fixtures, found {len(fixture_files)}")

    fixture_results = {}
    for fixture_path in fixture_files:
        fixture = load_json(fixture_path)
        case_id = fixture.get("case_id")
        expected = EXPECTED_CASES.get(case_id)
        if expected is None:
            failures.append(f"unexpected fixture case: {case_id}")
            continue
        observed = classify(fixture.get("input_text", ""), exact_phrase)
        fixture_results[case_id] = observed
        if observed["matched_exact_phrase"] is not expected:
            failures.append(f"{case_id} expected match {expected}, got {observed['matched_exact_phrase']}")
        if observed["approval_class"] != fixture.get("expected_class"):
            failures.append(f"{case_id} approval class mismatch")
        if observed["old_file_write_allowed_by_this_slice"] is not False:
            failures.append(f"{case_id} grants old-file write authority")

    report_cases = {case.get("case_id"): case for case in payload.get("classification_cases", [])}
    for case_id, expected in EXPECTED_CASES.items():
        case = report_cases.get(case_id)
        if not case:
            failures.append(f"report missing case: {case_id}")
            continue
        if case.get("expected_match") is not expected:
            failures.append(f"{case_id} report expected_match mismatch")
        if case.get("passed") is not True:
            failures.append(f"{case_id} report did not pass")

    summary = payload.get("summary", {})
    expected_summary = {
        "positive_case_count": 1,
        "negative_case_count": 9,
        "classification_case_count": 10,
        "classification_pass_count": 10,
        "classification_failure_count": 0,
        "user_approval_collected_by_this_slice": False,
        "old_slice_writes_applied": 0,
        "executor_write_allowed_now": False,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            failures.append(f"summary mismatch for {key}: expected {expected!r}, got {summary.get(key)!r}")

    authority = payload.get("authority_flags", {})
    for key in [
        "approval_collected",
        "fixture_match_is_user_approval",
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

    failure_payload = load_json(FAILURES) if FAILURES.exists() else {"failure_cases": []}
    failure_ids = {case.get("case_id") for case in failure_payload.get("failure_cases", [])}
    missing_failure_cases = EXPECTED_FAILURE_CASES - failure_ids
    if missing_failure_cases:
        failures.append(f"missing failure case records: {sorted(missing_failure_cases)}")

    md_text = (SLICE_ROOT / "artifact" / "exact_approval_classifier_hardening.md").read_text(encoding="utf-8") if (SLICE_ROOT / "artifact" / "exact_approval_classifier_hardening.md").exists() else ""
    html_text = (SLICE_ROOT / "artifact" / "exact_approval_classifier_hardening.html").read_text(encoding="utf-8") if (SLICE_ROOT / "artifact" / "exact_approval_classifier_hardening.html").exists() else ""
    for needle in ["positive_case_count: 1", "negative_case_count: 9", "user_approval_collected_by_this_slice: false"]:
        if needle not in md_text:
            failures.append(f"markdown missing: {needle}")
    for needle in ["Exact Approval Classifier", "Approval collected now", "false"]:
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
            "positive_case_count": summary.get("positive_case_count"),
            "negative_case_count": summary.get("negative_case_count"),
            "classification_pass_count": summary.get("classification_pass_count"),
            "classification_failure_count": summary.get("classification_failure_count"),
            "approval_collected": authority.get("approval_collected"),
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
