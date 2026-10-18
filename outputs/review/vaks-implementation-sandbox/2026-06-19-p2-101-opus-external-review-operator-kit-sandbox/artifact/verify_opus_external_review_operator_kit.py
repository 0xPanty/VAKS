import hashlib
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-19-p2-101-opus-external-review-operator-kit-sandbox"
TRANSFER_SLICE_ID = "2026-06-19-p2-100-opus-review-transfer-package-sandbox"
INTAKE_SLICE_ID = "2026-06-19-p2-96-opus-result-intake-skeleton-sandbox"

HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

TRANSFER_DIR = REPO_ROOT / "outputs" / "review" / "vaks-implementation-sandbox" / TRANSFER_SLICE_ID
INTAKE_DIR = REPO_ROOT / "outputs" / "review" / "vaks-implementation-sandbox" / INTAKE_SLICE_ID

TRANSFER_MANIFEST_PATH = TRANSFER_DIR / "artifact" / "opus-review-transfer-package-manifest.json"
TRANSFER_SHA_PATH = TRANSFER_DIR / "artifact" / "opus-review-transfer-package-sha256.txt"
INTAKE_SCHEMA_PATH = INTAKE_DIR / "artifact" / "opus-result-intake-schema.json"

RUNBOOK_PATH = ARTIFACT_DIR / "opus-external-review-operator-runbook.md"
SUBMISSION_MESSAGE_PATH = ARTIFACT_DIR / "opus-external-review-submission-message.md"
INTAKE_TEMPLATE_PATH = ARTIFACT_DIR / "opus-result-intake-template.md"
CONTROL_CARD_PATH = ARTIFACT_DIR / "opus-external-review-operator-control-card.json"
FAILURE_CASE_PATH = FAILURE_DIR / "opus-external-review-operator-kit-failures.json"

EXPECTED_FINAL_STATUSES = {
    "verification.md": "local_verification_passed",
    "reviewer-report.md": "review_pass_no_blocker",
    "boundary-audit.md": "pass_boundary",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_next_slice",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def verify(final_gate: bool = False) -> dict:
    failures: list[str] = []
    required = [
        RUNBOOK_PATH,
        SUBMISSION_MESSAGE_PATH,
        INTAKE_TEMPLATE_PATH,
        CONTROL_CARD_PATH,
        FAILURE_CASE_PATH,
        TRANSFER_MANIFEST_PATH,
        TRANSFER_SHA_PATH,
        INTAKE_SCHEMA_PATH,
    ]
    for path in required:
        if not path.exists():
            failures.append(f"missing_required_file:{path}")

    transfer_manifest = load_json(TRANSFER_MANIFEST_PATH, failures) if TRANSFER_MANIFEST_PATH.exists() else None
    intake_schema = load_json(INTAKE_SCHEMA_PATH, failures) if INTAKE_SCHEMA_PATH.exists() else None
    control_card = load_json(CONTROL_CARD_PATH, failures) if CONTROL_CARD_PATH.exists() else None
    failure_payload = load_json(FAILURE_CASE_PATH, failures) if FAILURE_CASE_PATH.exists() else None

    zip_sha256 = None
    allowed_tokens = []
    if transfer_manifest:
        summary = transfer_manifest.get("summary", {})
        zip_sha256 = summary.get("zip_sha256")
        if summary.get("transfer_ready") is not True:
            failures.append("transfer_not_ready")
        for key in ["actual_opus_result_present", "opus_approval_claimed", "mainline_ready", "goal_complete_now"]:
            if summary.get(key) is not False:
                failures.append(f"transfer_summary_overclaim:{key}")
        zip_path = summary.get("zip_path")
        if zip_path:
            zip_abs = REPO_ROOT / zip_path
            if not zip_abs.exists():
                failures.append(f"transfer_zip_missing:{zip_path}")
            elif zip_sha256 and sha256_file(zip_abs) != zip_sha256:
                failures.append("transfer_zip_byte_hash_mismatch")

    if intake_schema:
        allowed_tokens = intake_schema.get("allowed_conclusion_tokens", [])
        expected_tokens = [
            "OPUS_PASS_SANDBOX_CLOSEOUT",
            "OPUS_REVISE_SANDBOX_CLOSEOUT",
            "OPUS_BLOCKED_NEEDS_USER",
        ]
        if allowed_tokens != expected_tokens:
            failures.append("allowed_tokens_mismatch")
        for key, expected in {
            "mainline_approval": False,
            "reviewed_knowledge": False,
            "evidence_support": False,
            "action_basis": False,
            "commit_push_sync": False,
        }.items():
            if intake_schema.get("boundary_requirements", {}).get(key) is not expected:
                failures.append(f"intake_boundary_mismatch:{key}")

    if zip_sha256 and TRANSFER_SHA_PATH.exists():
        sha_text = TRANSFER_SHA_PATH.read_text(encoding="utf-8")
        if zip_sha256 not in sha_text:
            failures.append("transfer_sha_file_missing_zip_hash")

    texts = {}
    for path in [RUNBOOK_PATH, SUBMISSION_MESSAGE_PATH, INTAKE_TEMPLATE_PATH]:
        if path.exists():
            texts[path.name] = path.read_text(encoding="utf-8")

    combined_text = "\n".join(texts.values())
    for token in allowed_tokens:
        if token not in combined_text:
            failures.append(f"missing_allowed_token:{token}")
    if zip_sha256 and zip_sha256 not in combined_text:
        failures.append("missing_zip_sha_in_operator_text")
    for phrase in [
        "not an Opus result",
        "not Opus approval",
        "not mainline readiness",
        "not reviewed knowledge",
        "not evidence support",
        "not action basis",
        "not goal completion",
        "later sandbox-only intake slice",
    ]:
        if phrase not in combined_text:
            failures.append(f"missing_boundary_phrase:{phrase}")
    for forbidden in [
        "commit the result",
        "push the result",
        "sync Obsidian",
        "edit old slices directly",
        "merge into main architecture",
    ]:
        if forbidden in combined_text:
            failures.append(f"forbidden_instruction:{forbidden}")

    if control_card:
        if control_card.get("record_kind") != "opus_external_review_operator_control_card":
            failures.append("control_card_record_kind_mismatch")
        if control_card.get("slice_id") != SLICE_ID:
            failures.append("control_card_slice_id_mismatch")
        if control_card.get("transfer_slice_id") != TRANSFER_SLICE_ID:
            failures.append("control_card_transfer_slice_mismatch")
        if control_card.get("intake_schema_slice_id") != INTAKE_SLICE_ID:
            failures.append("control_card_intake_slice_mismatch")
        package = control_card.get("transfer_package", {})
        if zip_sha256 and package.get("zip_sha256") != zip_sha256:
            failures.append("control_card_zip_sha_mismatch")
        if package.get("zip_hash_matches_sha_file") is not True:
            failures.append("control_card_zip_sha_not_matched")
        state = control_card.get("operator_state", {})
        if state.get("ready_to_submit_to_opus") is not True:
            failures.append("operator_state_not_ready_to_submit")
        for key in [
            "actual_opus_result_present",
            "opus_approval_claimed",
            "mainline_ready",
            "reviewed_knowledge_ready",
            "evidence_support_ready",
            "action_basis_ready",
            "goal_complete_now",
        ]:
            if state.get(key) is not False:
                failures.append(f"operator_state_overclaim:{key}")
        hashes = control_card.get("sha256", {})
        expected_hash_paths = {
            "runbook": RUNBOOK_PATH,
            "submission_message": SUBMISSION_MESSAGE_PATH,
            "intake_template": INTAKE_TEMPLATE_PATH,
        }
        for key, path in expected_hash_paths.items():
            if path.exists() and hashes.get(key) != sha256_file(path):
                failures.append(f"control_card_hash_mismatch:{key}")

    fixture_files = sorted(FIXTURES_DIR.glob("*.json"))
    if len(fixture_files) != 5:
        failures.append(f"fixture_count_mismatch:{len(fixture_files)}")
    for fixture_file in fixture_files:
        fixture = load_json(fixture_file, failures)
        if fixture and fixture.get("expected") is not True:
            failures.append(f"fixture_not_positive:{fixture_file.name}")

    failure_case_count = 0
    if failure_payload:
        failure_case_count = len(failure_payload.get("failure_cases", []))
        if failure_case_count < 10:
            failures.append(f"failure_case_count_too_low:{failure_case_count}")

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
        "allowed_token_count": len(allowed_tokens),
        "zip_sha256": zip_sha256,
        "ready_to_submit_to_opus": bool(control_card and control_card.get("operator_state", {}).get("ready_to_submit_to_opus")),
        "actual_opus_result_present": bool(control_card and control_card.get("operator_state", {}).get("actual_opus_result_present")),
        "opus_approval_claimed": bool(control_card and control_card.get("operator_state", {}).get("opus_approval_claimed")),
        "mainline_ready": bool(control_card and control_card.get("operator_state", {}).get("mainline_ready")),
        "goal_complete_now": bool(control_card and control_card.get("operator_state", {}).get("goal_complete_now")),
        "final_gate": final_gate,
    }
    return {"passed": not failures, "failures": failures, "summary": summary}


if __name__ == "__main__":
    result = verify(final_gate="--final-gate" in sys.argv)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["passed"] else 1)
