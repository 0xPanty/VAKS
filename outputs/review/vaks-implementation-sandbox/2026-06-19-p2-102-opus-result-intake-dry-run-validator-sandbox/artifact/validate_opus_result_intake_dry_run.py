import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-19-p2-102-opus-result-intake-dry-run-validator-sandbox"

HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

MANIFEST_PATH = ARTIFACT_DIR / "opus-result-intake-dry-run-manifest.json"
FAILURE_CASE_PATH = FAILURE_DIR / "opus-result-intake-dry-run-failures.json"

EXPECTED_FINAL_STATUSES = {
    "verification.md": "local_verification_passed",
    "reviewer-report.md": "review_pass_no_blocker",
    "boundary-audit.md": "pass_boundary",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_next_slice",
}

SUPPORTED_EVIDENCE_PREFIXES = (
    "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox/",
    "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-101-opus-external-review-operator-kit-sandbox/",
    "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-96-opus-result-intake-skeleton-sandbox/",
)

TOP_LEVEL_FALSE_FIELDS = (
    "opus_review_performed",
    "mainline_approval",
    "mainline_merge",
    "promotion",
    "promotion_ready",
    "reviewed_knowledge",
    "reviewed_knowledge_ready",
    "evidence_support",
    "evidence_support_ready",
    "action_basis",
    "action_basis_ready",
    "commit_push_sync",
    "commit_push_sync_ready",
    "opus_approval_claimed",
    "user_mainline_approval",
    "mainline_ready",
    "goal_complete_now",
)


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


def validate_record(record: dict, allowed_tokens: list[str], required_fields: list[str]) -> list[str]:
    failures: list[str] = []
    if record.get("record_kind") != "opus_result_intake_dry_run_record":
        failures.append("record_kind_not_allowed")
    for field in required_fields:
        if field not in record:
            failures.append(f"missing_required_field:{field}")
    if record.get("dry_run_only") is not True:
        failures.append("dry_run_only_not_true")
    if record.get("actual_opus_result_present") is not False:
        failures.append("actual_opus_result_present_not_false")
    for key in TOP_LEVEL_FALSE_FIELDS:
        if record.get(key) is not False:
            failures.append(f"top_level_boundary_overclaim:{key}")
    if record.get("raw_conclusion_token") not in allowed_tokens:
        failures.append("raw_conclusion_token_not_allowed")
    if "reviewed_evidence" in record:
        evidence = record.get("reviewed_evidence")
        if not isinstance(evidence, list):
            failures.append("reviewed_evidence_not_list")
        elif not evidence:
            failures.append("reviewed_evidence_empty")
        else:
            for item in evidence:
                if not isinstance(item, str) or not item.strip():
                    failures.append("reviewed_evidence_item_empty")
                    continue
                normalized = item.strip().replace("\\", "/")
                if normalized.startswith("/") or ":" in normalized.split("/", 1)[0] or ".." in normalized.split("/"):
                    failures.append("reviewed_evidence_path_unsafe")
                if not normalized.startswith(SUPPORTED_EVIDENCE_PREFIXES):
                    failures.append("reviewed_evidence_unsupported")
    if record.get("boundary_verdict") != "not_mainline_approval":
        failures.append("boundary_verdict_not_allowed")
    if "raw_response_path" in record:
        raw_path = str(record.get("raw_response_path", "")).strip().replace("\\", "/")
        if not raw_path:
            failures.append("raw_response_path_empty")
        elif raw_path.startswith("/") or ":" in raw_path.split("/", 1)[0] or ".." in raw_path.split("/"):
            failures.append("raw_response_path_unsafe")
        elif not raw_path.startswith("artifact/"):
            failures.append("raw_response_path_not_artifact_relative")
    flags = record.get("authority_flags", {})
    for key in [
        "opus_approval_claimed",
        "mainline_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
        "action_basis_ready",
        "commit_push_sync_ready",
        "goal_complete_now",
    ]:
        if flags.get(key) is not False:
            failures.append(f"authority_flag_overclaim:{key}")
    return failures


def verify(final_gate: bool = False) -> dict:
    failures: list[str] = []
    manifest = load_json(MANIFEST_PATH, failures) if MANIFEST_PATH.exists() else None
    failure_payload = load_json(FAILURE_CASE_PATH, failures) if FAILURE_CASE_PATH.exists() else None

    if not manifest:
        failures.append("missing_manifest")
        allowed_tokens = []
        required_fields = []
    else:
        if manifest.get("record_kind") != "opus_result_intake_dry_run_manifest":
            failures.append("manifest_record_kind_mismatch")
        if manifest.get("slice_id") != SLICE_ID:
            failures.append("manifest_slice_id_mismatch")
        allowed_tokens = manifest.get("allowed_conclusion_tokens", [])
        required_fields = manifest.get("required_fields_when_result_exists", [])
        if allowed_tokens != [
            "OPUS_PASS_SANDBOX_CLOSEOUT",
            "OPUS_REVISE_SANDBOX_CLOSEOUT",
            "OPUS_BLOCKED_NEEDS_USER",
        ]:
            failures.append("allowed_tokens_mismatch")
        summary = manifest.get("summary", {})
        if summary.get("dry_run_validator_ready") is not True:
            failures.append("dry_run_validator_not_ready")
        for key in [
            "actual_opus_result_present",
            "opus_approval_claimed",
            "mainline_ready",
            "reviewed_knowledge_ready",
            "evidence_support_ready",
            "action_basis_ready",
            "goal_complete_now",
        ]:
            if summary.get(key) is not False:
                failures.append(f"manifest_summary_overclaim:{key}")

    fixture_files = sorted(FIXTURES_DIR.glob("valid-*.json"))
    expected_fixture_names = {
        "valid-opus-pass-result.json",
        "valid-opus-revise-result.json",
        "valid-opus-blocked-result.json",
    }
    if {path.name for path in fixture_files} != expected_fixture_names:
        failures.append("valid_fixture_set_mismatch")
    for fixture in fixture_files:
        record = load_json(fixture, failures)
        if record:
            record_failures = validate_record(record, allowed_tokens, required_fields)
            if record_failures:
                failures.append(f"valid_fixture_failed:{fixture.name}:{'|'.join(record_failures)}")

    failure_case_count = 0
    expected_failure_hits = 0
    if not failure_payload:
        failures.append("missing_failure_payload")
    else:
        cases = failure_payload.get("failure_cases", [])
        failure_case_count = len(cases)
        if failure_case_count < 10:
            failures.append(f"failure_case_count_too_low:{failure_case_count}")
        for case in cases:
            record = case.get("record", {})
            expected_failure = case.get("expected_failure")
            actual_failures = validate_record(record, allowed_tokens, required_fields)
            if expected_failure not in actual_failures:
                failures.append(f"failure_case_not_caught:{case.get('id')}:{expected_failure}:{actual_failures}")
            else:
                expected_failure_hits += 1

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
        "valid_fixture_count": len(fixture_files),
        "failure_case_count": failure_case_count,
        "expected_failure_hits": expected_failure_hits,
        "allowed_token_count": len(allowed_tokens),
        "dry_run_validator_ready": bool(manifest and manifest.get("summary", {}).get("dry_run_validator_ready")),
        "actual_opus_result_present": bool(manifest and manifest.get("summary", {}).get("actual_opus_result_present")),
        "opus_approval_claimed": bool(manifest and manifest.get("summary", {}).get("opus_approval_claimed")),
        "mainline_ready": bool(manifest and manifest.get("summary", {}).get("mainline_ready")),
        "goal_complete_now": bool(manifest and manifest.get("summary", {}).get("goal_complete_now")),
        "final_gate": final_gate,
    }
    return {"passed": not failures, "failures": failures, "summary": summary}


if __name__ == "__main__":
    result = verify(final_gate="--final-gate" in sys.argv)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["passed"] else 1)
