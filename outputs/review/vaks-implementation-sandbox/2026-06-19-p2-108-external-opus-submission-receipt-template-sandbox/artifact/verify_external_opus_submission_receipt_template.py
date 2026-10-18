import copy
import hashlib
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-19-p2-108-external-opus-submission-receipt-template-sandbox"
HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

RECEIPT_JSON = ARTIFACT_DIR / "external-opus-submission-receipt-template.json"
RECEIPT_MD = ARTIFACT_DIR / "external-opus-submission-receipt-template.md"
FAILURE_CASE_PATH = FAILURE_DIR / "external-opus-submission-receipt-template-failures.json"

EXPECTED_VALIDATOR = "2026-06-19-p2-102-opus-result-intake-dry-run-validator-sandbox"
REQUIRED_FIELDS = [
    "submitted_at",
    "submitted_by",
    "submission_surface",
    "surface_url_or_identifier",
    "attachment_zip_path",
    "attachment_zip_sha256",
    "brief_path",
    "dispatch_message_path",
    "raw_response_received",
    "raw_response_path",
    "expected_intake_route",
    "expected_validator",
]
FALSE_AUTHORITY_KEYS = [
    "external_submission_performed",
    "raw_opus_response_present",
    "actual_opus_result_present",
    "validated_opus_pass_present",
    "user_approval_present",
    "mainline_ready",
    "mainline_merge_allowed",
    "promotion_allowed",
    "reviewed_knowledge_ready",
    "evidence_support_ready",
    "action_basis_ready",
    "commit_push_sync_ready",
    "goal_complete_now",
]
FINAL_STATUSES = {
    "verification.md": "local_verification_passed",
    "reviewer-report.md": "review_pass_no_blocker",
    "boundary-audit.md": "pass_boundary",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_next_slice",
}


def load_json(path: Path, failures: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"json_load_failed:{path.name}:{exc}")
        return {}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dotted_get(payload: dict, dotted_path: str):
    current = payload
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


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


def validate(receipt: dict, template_text: str) -> list[str]:
    failures = []
    if receipt.get("record_kind") != "external_opus_submission_receipt_template":
        failures.append("record_kind_mismatch")
    if receipt.get("slice_id") != SLICE_ID:
        failures.append("slice_id_mismatch")
    sources = receipt.get("source_inputs", {})
    hashes = receipt.get("source_hashes", {})
    template = receipt.get("receipt_template", {})
    authority = receipt.get("authority_flags", {})

    for key in ["manual_submission_json", "manual_submission_brief", "response_capture_card"]:
        source = sources.get(key)
        if not source:
            failures.append(f"source_missing:{key}")
            continue
        source_path = REPO_ROOT / source
        if not source_path.exists():
            failures.append(f"source_file_missing:{key}")
            continue
        expected_hash = hashes.get(f"{key}_sha256")
        if expected_hash != sha256_file(source_path):
            failures.append(f"source_hash_mismatch:{key}")
    if hashes.get("manual_submission_brief_sha256") != hashes.get("expected_manual_submission_brief_sha256"):
        failures.append("source_hash_mismatch:manual_submission_brief")
    if hashes.get("response_capture_card_sha256") != hashes.get("expected_response_capture_card_sha256"):
        failures.append("source_hash_mismatch:response_capture_card")
    if template.get("template_ready") is not True:
        failures.append("template_not_ready")
    if template.get("submission_performed") is not False:
        failures.append("submission_performed")
    if template.get("raw_response_received") is not False:
        failures.append("raw_response_received")
    if template.get("expected_validator") != EXPECTED_VALIDATOR:
        failures.append("expected_validator_mismatch")
    for field in REQUIRED_FIELDS:
        if field not in template.get("required_fields", []):
            failures.append(f"required_field_missing:{field}")
    for key in FALSE_AUTHORITY_KEYS:
        if authority.get(key) is not False:
            failures.append(f"authority_overclaim:{key}")
    for phrase in [
        "not an Opus result",
        "not Opus approval",
        "not validated Opus PASS",
        "not user approval",
        "not mainline readiness",
        "not reviewed knowledge",
        "not evidence support",
        "not action basis",
        "not goal completion",
        "new sandbox-only intake slice",
    ]:
        if phrase not in template_text:
            failures.append(f"template_missing_phrase:{phrase}")
    return failures


def mutate(receipt: dict, mutation: str) -> tuple[dict, str]:
    mutated = copy.deepcopy(receipt)
    text = RECEIPT_MD.read_text(encoding="utf-8") if RECEIPT_MD.exists() else ""
    if mutation == "brief_hash_drift":
        mutated["source_hashes"]["manual_submission_brief_sha256"] = "bad"
    elif mutation == "capture_hash_drift":
        mutated["source_hashes"]["response_capture_card_sha256"] = "bad"
    elif mutation == "missing_required_field":
        mutated["receipt_template"]["required_fields"] = [
            field for field in mutated["receipt_template"]["required_fields"] if field != "submitted_at"
        ]
    elif mutation == "wrong_validator":
        mutated["receipt_template"]["expected_validator"] = "wrong-validator"
    elif mutation == "template_claims_result":
        text = text.replace("not an Opus result", "an Opus result")
    elif mutation == "template_missing_intake_route":
        text = text.replace("new sandbox-only intake slice", "later storage")
    elif mutation.endswith("_true"):
        key = mutation[:-5]
        mutated["authority_flags"][key] = True
    return mutated, text


def verify(final_gate: bool = False) -> dict:
    failures = []
    receipt = load_json(RECEIPT_JSON, failures) if RECEIPT_JSON.exists() else {}
    template_text = RECEIPT_MD.read_text(encoding="utf-8") if RECEIPT_MD.exists() else ""
    if not template_text:
        failures.append("missing_receipt_template")
    failures.extend(validate(receipt, template_text))

    fixtures = sorted(FIXTURES_DIR.glob("*.json"))
    if len(fixtures) != 4:
        failures.append(f"fixture_count_mismatch:{len(fixtures)}")
    for fixture_path in fixtures:
        fixture = load_json(fixture_path, failures)
        if fixture.get("expected") is not True:
            failures.append(f"fixture_not_positive:{fixture_path.name}")
        for key, expected in fixture.get("checks", {}).items():
            actual = dotted_get(receipt, key)
            if actual != expected:
                failures.append(f"fixture_check_failed:{fixture_path.name}:{key}:expected={expected}:actual={actual}")
        if fixture_path.name == "valid-required-fields.json" and fixture.get("required_field_count") != len(REQUIRED_FIELDS):
            failures.append("fixture_required_field_count_mismatch")

    failure_payload = load_json(FAILURE_CASE_PATH, failures) if FAILURE_CASE_PATH.exists() else {}
    cases = failure_payload.get("failure_cases", [])
    expected_failure_hits = 0
    if len(cases) < 18:
        failures.append(f"failure_case_count_too_low:{len(cases)}")
    for case in cases:
        mutated_receipt, mutated_text = mutate(receipt, case.get("mutation"))
        actual = validate(mutated_receipt, mutated_text)
        if case.get("expected_failure") in actual:
            expected_failure_hits += 1
        else:
            failures.append(f"failure_case_not_caught:{case.get('id')}:{case.get('expected_failure')}:{actual}")

    if final_gate:
        for filename, expected in FINAL_STATUSES.items():
            path = SLICE_DIR / filename
            if not path.exists():
                failures.append(f"final_gate_missing_report:{filename}")
                continue
            actual = frontmatter_status(path)
            if actual != expected:
                failures.append(f"final_gate_status:{filename}:expected={expected}:actual={actual}")

    summary = {
        "template_ready": bool(receipt.get("receipt_template", {}).get("template_ready")),
        "fixture_count": len(fixtures),
        "failure_case_count": len(cases),
        "expected_failure_hits": expected_failure_hits,
        "external_submission_performed": bool(receipt.get("authority_flags", {}).get("external_submission_performed")),
        "raw_opus_response_present": bool(receipt.get("authority_flags", {}).get("raw_opus_response_present")),
        "validated_opus_pass_present": bool(receipt.get("authority_flags", {}).get("validated_opus_pass_present")),
        "user_approval_present": bool(receipt.get("authority_flags", {}).get("user_approval_present")),
        "mainline_ready": bool(receipt.get("authority_flags", {}).get("mainline_ready")),
        "goal_complete_now": bool(receipt.get("authority_flags", {}).get("goal_complete_now")),
        "final_gate": final_gate,
    }
    return {"passed": not failures, "failures": failures, "summary": summary}


if __name__ == "__main__":
    result = verify(final_gate="--final-gate" in sys.argv)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["passed"] else 1)
