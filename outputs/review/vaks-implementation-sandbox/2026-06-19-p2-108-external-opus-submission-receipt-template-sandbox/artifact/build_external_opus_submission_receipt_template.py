import hashlib
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-108-external-opus-submission-receipt-template-sandbox"
HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

P2_107 = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-107-external-opus-manual-submission-brief-sandbox"
P2_107_JSON = P2_107 / "artifact/external-opus-manual-submission-brief.json"
P2_107_BRIEF = P2_107 / "artifact/external-opus-manual-submission-brief.md"
P2_107_CAPTURE = P2_107 / "artifact/external-opus-response-capture-card.md"

OUT_JSON = ARTIFACT_DIR / "external-opus-submission-receipt-template.json"
OUT_MD = ARTIFACT_DIR / "external-opus-submission-receipt-template.md"


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def build() -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    p2_107 = json.loads(P2_107_JSON.read_text(encoding="utf-8"))
    manual = p2_107["manual_submission"]

    template_text = "\n".join([
        "# External Opus Submission Receipt Template",
        "",
        "Status: not submitted yet.",
        "",
        "Fill this template only after a real external Opus submission has been performed. Do not use this receipt as an Opus response.",
        "",
        "## Submission Event",
        "",
        "- `submitted_at`: ",
        "- `submitted_by`: ",
        "- `submission_surface`: ",
        "- `surface_url_or_identifier`: ",
        "- `attachment_zip_path`: `" + manual["zip_path"] + "`",
        "- `attachment_zip_sha256`: `" + manual["zip_sha256"] + "`",
        "- `brief_path`: `" + manual["brief_path"] + "`",
        "- `dispatch_message_path`: `" + manual["dispatch_message_path"] + "`",
        "",
        "## Response Status",
        "",
        "- `raw_response_received`: false",
        "- `raw_response_path`: ",
        "- `expected_intake_route`: new sandbox-only intake slice",
        "- `expected_validator`: `" + manual["post_response_validator_slice"] + "`",
        "",
        "## Boundary",
        "",
        "This receipt is not an Opus result, not Opus approval, not validated Opus PASS, not user approval, not mainline readiness, not mainline merge, not promotion, not reviewed knowledge, not evidence support, not action basis, not commit, not push, not sync, and not goal completion.",
        "",
    ]) + "\n"
    write_text(OUT_MD, template_text)

    receipt = {
        "record_kind": "external_opus_submission_receipt_template",
        "slice_id": SLICE_ID,
        "source_inputs": {
            "manual_submission_json": rel(P2_107_JSON),
            "manual_submission_brief": rel(P2_107_BRIEF),
            "response_capture_card": rel(P2_107_CAPTURE),
        },
        "source_hashes": {
            "manual_submission_json_sha256": sha256_file(P2_107_JSON),
            "manual_submission_brief_sha256": sha256_file(P2_107_BRIEF),
            "response_capture_card_sha256": sha256_file(P2_107_CAPTURE),
            "expected_manual_submission_brief_sha256": manual["brief_sha256"],
            "expected_response_capture_card_sha256": manual["response_capture_card_sha256"],
        },
        "receipt_template": {
            "template_ready": True,
            "receipt_template_path": rel(OUT_MD),
            "receipt_template_sha256": sha256_file(OUT_MD),
            "submission_performed": False,
            "raw_response_received": False,
            "required_fields": [
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
            ],
            "attachment_zip_path": manual["zip_path"],
            "attachment_zip_sha256": manual["zip_sha256"],
            "brief_path": manual["brief_path"],
            "dispatch_message_path": manual["dispatch_message_path"],
            "expected_validator": manual["post_response_validator_slice"],
            "expected_intake_route": "new sandbox-only intake slice",
        },
        "authority_flags": {
            "receipt_template_only": True,
            "external_submission_performed": False,
            "raw_opus_response_present": False,
            "actual_opus_result_present": False,
            "validated_opus_pass_present": False,
            "user_approval_present": False,
            "mainline_ready": False,
            "mainline_merge_allowed": False,
            "promotion_allowed": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "commit_push_sync_ready": False,
            "goal_complete_now": False,
        },
    }
    write_json(OUT_JSON, receipt)

    fixtures = {
        "valid-template-ready-no-submission.json": {
            "fixture": "valid-template-ready-no-submission",
            "checks": {
                "receipt_template.template_ready": True,
                "receipt_template.submission_performed": False,
                "receipt_template.raw_response_received": False,
            },
            "expected": True,
        },
        "valid-source-hash-binding.json": {
            "fixture": "valid-source-hash-binding",
            "checks": {
                "source_hashes.manual_submission_brief_sha256": receipt["source_hashes"]["expected_manual_submission_brief_sha256"],
                "source_hashes.response_capture_card_sha256": receipt["source_hashes"]["expected_response_capture_card_sha256"],
            },
            "expected": True,
        },
        "valid-required-fields.json": {
            "fixture": "valid-required-fields",
            "required_field_count": len(receipt["receipt_template"]["required_fields"]),
            "expected": True,
        },
        "valid-no-authority.json": {
            "fixture": "valid-no-authority",
            "checks": {
                "authority_flags.external_submission_performed": False,
                "authority_flags.raw_opus_response_present": False,
                "authority_flags.validated_opus_pass_present": False,
                "authority_flags.user_approval_present": False,
                "authority_flags.mainline_merge_allowed": False,
                "authority_flags.action_basis_ready": False,
                "authority_flags.goal_complete_now": False,
            },
            "expected": True,
        },
    }
    for filename, payload in fixtures.items():
        write_json(FIXTURES_DIR / filename, payload)

    failures = {
        "record_kind": "external_opus_submission_receipt_template_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {"id": "brief_hash_drift", "mutation": "brief_hash_drift", "expected_failure": "source_hash_mismatch:manual_submission_brief"},
            {"id": "capture_hash_drift", "mutation": "capture_hash_drift", "expected_failure": "source_hash_mismatch:response_capture_card"},
            {"id": "missing_required_field", "mutation": "missing_required_field", "expected_failure": "required_field_missing:submitted_at"},
            {"id": "wrong_validator", "mutation": "wrong_validator", "expected_failure": "expected_validator_mismatch"},
            {"id": "claims_submission", "mutation": "external_submission_performed_true", "expected_failure": "authority_overclaim:external_submission_performed"},
            {"id": "claims_raw_response", "mutation": "raw_opus_response_present_true", "expected_failure": "authority_overclaim:raw_opus_response_present"},
            {"id": "claims_opus_result", "mutation": "actual_opus_result_present_true", "expected_failure": "authority_overclaim:actual_opus_result_present"},
            {"id": "claims_validated_pass", "mutation": "validated_opus_pass_present_true", "expected_failure": "authority_overclaim:validated_opus_pass_present"},
            {"id": "claims_user_approval", "mutation": "user_approval_present_true", "expected_failure": "authority_overclaim:user_approval_present"},
            {"id": "allows_mainline_merge", "mutation": "mainline_merge_allowed_true", "expected_failure": "authority_overclaim:mainline_merge_allowed"},
            {"id": "allows_promotion", "mutation": "promotion_allowed_true", "expected_failure": "authority_overclaim:promotion_allowed"},
            {"id": "claims_reviewed_knowledge", "mutation": "reviewed_knowledge_ready_true", "expected_failure": "authority_overclaim:reviewed_knowledge_ready"},
            {"id": "claims_evidence_support", "mutation": "evidence_support_ready_true", "expected_failure": "authority_overclaim:evidence_support_ready"},
            {"id": "claims_action_basis", "mutation": "action_basis_ready_true", "expected_failure": "authority_overclaim:action_basis_ready"},
            {"id": "allows_commit_push_sync", "mutation": "commit_push_sync_ready_true", "expected_failure": "authority_overclaim:commit_push_sync_ready"},
            {"id": "claims_goal_complete", "mutation": "goal_complete_now_true", "expected_failure": "authority_overclaim:goal_complete_now"},
            {"id": "template_claims_result", "mutation": "template_claims_result", "expected_failure": "template_missing_phrase:not an Opus result"},
            {"id": "template_missing_intake_route", "mutation": "template_missing_intake_route", "expected_failure": "template_missing_phrase:new sandbox-only intake slice"},
        ],
    }
    write_json(FAILURE_DIR / "external-opus-submission-receipt-template-failures.json", failures)
    return {
        "written": True,
        "summary": {
            "template_ready": True,
            "fixture_count": len(fixtures),
            "failure_case_count": len(failures["failure_cases"]),
            **receipt["authority_flags"],
        },
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
