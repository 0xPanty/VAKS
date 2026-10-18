import hashlib
import json
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


def rel_repo(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def build() -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    transfer_manifest = json.loads(TRANSFER_MANIFEST_PATH.read_text(encoding="utf-8"))
    intake_schema = json.loads(INTAKE_SCHEMA_PATH.read_text(encoding="utf-8"))

    transfer_summary = transfer_manifest["summary"]
    zip_path = transfer_summary["zip_path"]
    zip_sha256 = transfer_summary["zip_sha256"]
    sha_text = TRANSFER_SHA_PATH.read_text(encoding="utf-8").strip()
    allowed_tokens = intake_schema["allowed_conclusion_tokens"]

    runbook = f"""# Opus External Review Operator Runbook

## Purpose

Use this runbook to submit the p2-100 transfer package to external Opus review and preserve the result for a later sandbox-only intake slice.

## Pre-Submission Checks

- Confirm transfer ZIP path: `{zip_path}`
- Confirm transfer ZIP SHA256: `{zip_sha256}`
- Confirm SHA256 file contains the same hash: `{rel_repo(TRANSFER_SHA_PATH)}`
- Confirm the transfer manifest says `transfer_ready=true`.
- Confirm the transfer manifest says `actual_opus_result_present=false`, `opus_approval_claimed=false`, `mainline_ready=false`, and `goal_complete_now=false`.

## Submission

Send the ZIP file and SHA256 to the external Opus review surface. Use `opus-external-review-submission-message.md` as the message body.

## Required Opus Result Tokens

The raw Opus response must include exactly one of:

- `OPUS_PASS_SANDBOX_CLOSEOUT`
- `OPUS_REVISE_SANDBOX_CLOSEOUT`
- `OPUS_BLOCKED_NEEDS_USER`

## Post-Response Intake

After Opus responds, do not edit old slices or main architecture. Create a later sandbox-only intake slice and preserve the raw response using `opus-result-intake-template.md` as the capture shape.

## Boundary

This operator kit is not an Opus result, not Opus approval, not mainline readiness, not reviewed knowledge, not evidence support, not action basis, and not goal completion.
"""
    write_text(RUNBOOK_PATH, runbook)

    submission_message = f"""# External Opus Review Submission Message

Please perform an external review of the attached VAKS sandbox closeout evidence transfer package.

Attached package:

- ZIP path in local workspace: `{zip_path}`
- ZIP SHA256: `{zip_sha256}`

Review task:

1. Inspect the transfer package contents, especially the p2-98 dossier snapshot and the p2-91/p2-92/p2-94/p2-96/p2-97 evidence snapshots included through p2-99.
2. Judge whether the sandbox closeout evidence is sufficient to treat the original 20 sandbox slices as current-strict sandbox closeout complete.
3. Check that the package does not imply mainline merge, reviewed knowledge, evidence support, action basis, or user approval.
4. Return exactly one conclusion token:
   - `OPUS_PASS_SANDBOX_CLOSEOUT`
   - `OPUS_REVISE_SANDBOX_CLOSEOUT`
   - `OPUS_BLOCKED_NEEDS_USER`

Required response fields:

- `raw_conclusion_token`
- `reviewed_evidence`
- `boundary_verdict`
- `blocking_issues`
- `recommended_next_action`

Boundary reminder:

Your review result is external review evidence only. It does not itself merge the sandbox into the main architecture, create reviewed knowledge, create evidence support, create action basis, commit, push, or sync.
"""
    write_text(SUBMISSION_MESSAGE_PATH, submission_message)

    intake_template = f"""# Opus Result Intake Template

## Source Transfer Package

- transfer_slice_id: `{TRANSFER_SLICE_ID}`
- transfer_zip_path: `{zip_path}`
- transfer_zip_sha256: `{zip_sha256}`
- operator_kit_slice_id: `{SLICE_ID}`

## Raw Opus Response

Paste or link the raw Opus response in the later intake slice. Do not summarize it as approval before validation.

```text
<RAW_OPUS_RESPONSE_GOES_HERE>
```

## Required Parsed Fields

- raw_conclusion_token: one of `{allowed_tokens[0]}`, `{allowed_tokens[1]}`, `{allowed_tokens[2]}`
- reviewed_evidence:
- boundary_verdict:
- raw_response_path:
- blocking_issues:
- recommended_next_action:

## Boundary Requirements

- mainline_approval: false
- reviewed_knowledge: false
- evidence_support: false
- action_basis: false
- commit_push_sync: false
"""
    write_text(INTAKE_TEMPLATE_PATH, intake_template)

    control_card = {
        "record_kind": "opus_external_review_operator_control_card",
        "slice_id": SLICE_ID,
        "transfer_slice_id": TRANSFER_SLICE_ID,
        "intake_schema_slice_id": INTAKE_SLICE_ID,
        "inputs": {
            "transfer_manifest_path": rel_repo(TRANSFER_MANIFEST_PATH),
            "transfer_sha_path": rel_repo(TRANSFER_SHA_PATH),
            "intake_schema_path": rel_repo(INTAKE_SCHEMA_PATH),
        },
        "outputs": {
            "runbook_path": rel_repo(RUNBOOK_PATH),
            "submission_message_path": rel_repo(SUBMISSION_MESSAGE_PATH),
            "intake_template_path": rel_repo(INTAKE_TEMPLATE_PATH),
        },
        "transfer_package": {
            "zip_path": zip_path,
            "zip_sha256": zip_sha256,
            "sha_file_text": sha_text,
            "zip_hash_matches_sha_file": zip_sha256 in sha_text,
            "transfer_ready": transfer_summary["transfer_ready"],
            "actual_opus_result_present": transfer_summary["actual_opus_result_present"],
            "opus_approval_claimed": transfer_summary["opus_approval_claimed"],
            "mainline_ready": transfer_summary["mainline_ready"],
            "goal_complete_now": transfer_summary["goal_complete_now"],
        },
        "intake_schema": {
            "allowed_conclusion_tokens": allowed_tokens,
            "required_fields_when_result_exists": intake_schema["required_fields_when_result_exists"],
            "boundary_requirements": intake_schema["boundary_requirements"],
        },
        "operator_state": {
            "ready_to_submit_to_opus": True,
            "actual_opus_result_present": False,
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
        },
        "sha256": {
            "runbook": sha256_file(RUNBOOK_PATH),
            "submission_message": sha256_file(SUBMISSION_MESSAGE_PATH),
            "intake_template": sha256_file(INTAKE_TEMPLATE_PATH),
        },
    }
    write_json(CONTROL_CARD_PATH, control_card)

    fixtures = {
        "ready-to-submit-with-zip-sha.json": {
            "fixture": "ready-to-submit-with-zip-sha",
            "zip_path": zip_path,
            "zip_sha256": zip_sha256,
            "expected": True,
        },
        "submission-message-has-required-tokens.json": {
            "fixture": "submission-message-has-required-tokens",
            "allowed_conclusion_tokens": allowed_tokens,
            "expected": True,
        },
        "result-intake-template-linked.json": {
            "fixture": "result-intake-template-linked",
            "intake_schema_path": rel_repo(INTAKE_SCHEMA_PATH),
            "required_fields": intake_schema["required_fields_when_result_exists"],
            "expected": True,
        },
        "no-approval-before-opus.json": {
            "fixture": "no-approval-before-opus",
            "operator_state": control_card["operator_state"],
            "expected": True,
        },
        "post-response-sandbox-only.json": {
            "fixture": "post-response-sandbox-only",
            "expected_next_container": "later sandbox-only intake slice",
            "expected": True,
        },
    }
    for filename, payload in fixtures.items():
        write_json(FIXTURES_DIR / filename, payload)

    failures = {
        "record_kind": "opus_external_review_operator_kit_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {"id": "missing_transfer_zip_hash", "expectation": "Verifier fails if the p2-100 ZIP hash is absent or mismatched."},
            {"id": "missing_submission_message", "expectation": "Verifier fails if the exact submission message is missing."},
            {"id": "missing_allowed_result_token", "expectation": "Verifier fails if any p2-96 allowed Opus result token is omitted."},
            {"id": "missing_intake_template", "expectation": "Verifier fails if the result intake template is missing."},
            {"id": "approval_overclaim", "expectation": "Verifier fails if the kit claims Opus approval before a raw result exists."},
            {"id": "mainline_ready_overclaim", "expectation": "Verifier fails if the kit claims mainline readiness."},
            {"id": "truth_or_action_authority_overclaim", "expectation": "Verifier fails if the kit claims reviewed knowledge, evidence support, or action basis."},
            {"id": "goal_complete_overclaim", "expectation": "Verifier fails if the kit claims the full goal is complete."},
            {"id": "old_slice_write_required", "expectation": "Verifier fails if the kit instructs operators to edit old slices directly."},
            {"id": "commit_push_sync_required", "expectation": "Verifier fails if the kit instructs commit, push, or sync."},
        ],
    }
    write_json(FAILURE_DIR / "opus-external-review-operator-kit-failures.json", failures)

    return {
        "written": True,
        "summary": {
            "ready_to_submit_to_opus": True,
            "zip_sha256": zip_sha256,
            "allowed_token_count": len(allowed_tokens),
            "fixture_count": len(fixtures),
            "failure_case_count": len(failures["failure_cases"]),
            "actual_opus_result_present": False,
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "goal_complete_now": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
