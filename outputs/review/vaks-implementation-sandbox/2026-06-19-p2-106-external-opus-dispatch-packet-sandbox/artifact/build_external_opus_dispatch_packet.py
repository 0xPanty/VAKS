import hashlib
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-106-external-opus-dispatch-packet-sandbox"
HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

P2_100 = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox"
P2_101 = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-101-opus-external-review-operator-kit-sandbox"
P2_105 = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-105-external-review-chain-readiness-preflight-sandbox"

TRANSFER_MANIFEST = P2_100 / "artifact/opus-review-transfer-package-manifest.json"
TRANSFER_ZIP = P2_100 / "artifact/opus-review-transfer-package.zip"
TRANSFER_SHA = P2_100 / "artifact/opus-review-transfer-package-sha256.txt"
OPERATOR_CARD = P2_101 / "artifact/opus-external-review-operator-control-card.json"
SUBMISSION_SOURCE = P2_101 / "artifact/opus-external-review-submission-message.md"
READINESS_COCKPIT = P2_105 / "artifact/external-review-chain-readiness-cockpit.json"

OUT_PACKET = ARTIFACT_DIR / "external-opus-dispatch-packet.json"
OUT_MESSAGE = ARTIFACT_DIR / "external-opus-dispatch-message.md"
OUT_CHECKLIST = ARTIFACT_DIR / "external-opus-dispatch-checklist.md"

TOKENS = [
    "OPUS_PASS_SANDBOX_CLOSEOUT",
    "OPUS_REVISE_SANDBOX_CLOSEOUT",
    "OPUS_BLOCKED_NEEDS_USER",
]


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def build_message(base_message: str, zip_path: str, zip_sha: str) -> str:
    return "\n".join([
        "# External Opus Dispatch Message",
        "",
        "Send this message with the transfer ZIP attached.",
        "",
        "## Attachment",
        "",
        f"- ZIP path: `{zip_path}`",
        f"- ZIP SHA256: `{zip_sha}`",
        "",
        "## Message Body",
        "",
        base_message.strip(),
        "",
        "## Dispatch Boundary",
        "",
        "This dispatch packet is not an Opus response, not Opus approval, not user approval, not mainline readiness, not reviewed knowledge, not evidence support, not action basis, not commit, not push, not sync, and not goal completion.",
        "",
    ]) + "\n"


def build_checklist(zip_path: str, zip_sha: str) -> str:
    return "\n".join([
        "# External Opus Dispatch Checklist",
        "",
        "- Verify the ZIP exists before upload.",
        f"- Verify ZIP path: `{zip_path}`",
        f"- Verify ZIP SHA256: `{zip_sha}`",
        "- Send `external-opus-dispatch-message.md` as the message body.",
        "- Attach the ZIP file to the external Opus review surface.",
        "- Require exactly one conclusion token in the response.",
        "- Preserve the raw Opus response in a later sandbox-only intake slice.",
        "- Validate the raw response with p2-102 before any user approval or merge discussion.",
        "- Do not edit old slices, main architecture docs, wiki truth layers, templates, tools, or Obsidian vault during dispatch.",
        "",
    ]) + "\n"


def build() -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    transfer = read_json(TRANSFER_MANIFEST)
    operator = read_json(OPERATOR_CARD)
    readiness = read_json(READINESS_COCKPIT)
    base_message = SUBMISSION_SOURCE.read_text(encoding="utf-8")

    expected_zip_sha = transfer["summary"]["zip_sha256"]
    actual_zip_sha = sha256_file(TRANSFER_ZIP)
    sha_file_text = TRANSFER_SHA.read_text(encoding="utf-8").strip()
    source_message_sha = sha256_text(base_message)
    expected_source_message_sha = operator["sha256"]["submission_message"]

    zip_path = transfer["summary"]["zip_path"]
    message_text = build_message(base_message, zip_path, expected_zip_sha)
    checklist_text = build_checklist(zip_path, expected_zip_sha)
    write_text(OUT_MESSAGE, message_text)
    write_text(OUT_CHECKLIST, checklist_text)

    packet = {
        "record_kind": "external_opus_dispatch_packet",
        "slice_id": SLICE_ID,
        "source_inputs": {
            "transfer_manifest": rel(TRANSFER_MANIFEST),
            "transfer_zip": rel(TRANSFER_ZIP),
            "transfer_sha_file": rel(TRANSFER_SHA),
            "operator_control_card": rel(OPERATOR_CARD),
            "operator_submission_message": rel(SUBMISSION_SOURCE),
            "readiness_cockpit": rel(READINESS_COCKPIT),
        },
        "dispatch": {
            "dispatch_ready": True,
            "external_submission_performed": False,
            "zip_path": zip_path,
            "zip_exists": TRANSFER_ZIP.is_file(),
            "zip_sha256": expected_zip_sha,
            "actual_zip_sha256": actual_zip_sha,
            "zip_hash_verified": actual_zip_sha == expected_zip_sha and expected_zip_sha in sha_file_text,
            "zip_size_bytes": TRANSFER_ZIP.stat().st_size,
            "source_message_sha256": source_message_sha,
            "source_message_hash_verified": source_message_sha == expected_source_message_sha,
            "dispatch_message_path": rel(OUT_MESSAGE),
            "dispatch_message_sha256": sha256_text(message_text),
            "dispatch_checklist_path": rel(OUT_CHECKLIST),
            "dispatch_checklist_sha256": sha256_text(checklist_text),
            "required_conclusion_tokens": TOKENS,
            "post_response_validator_slice": "2026-06-19-p2-102-opus-result-intake-dry-run-validator-sandbox",
            "required_next_action": "Submit the ZIP and dispatch message to external Opus, then retain the raw response in a later sandbox-only intake slice.",
        },
        "readiness_inputs": {
            "transfer_ready": transfer["summary"]["transfer_ready"],
            "operator_ready_to_submit": operator["operator_state"]["ready_to_submit_to_opus"],
            "chain_ready_to_submit_external_opus": readiness["summary"]["ready_to_submit_external_opus"],
            "chain_final_gates_true": readiness["summary"]["all_final_gates_true"],
            "chain_product_grade": readiness["summary"]["all_product_grade"],
        },
        "authority_flags": {
            "dispatch_packet_only": True,
            "external_submission_performed": False,
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
    write_json(OUT_PACKET, packet)

    fixtures = {
        "valid-transfer-zip-hash-bound.json": {
            "fixture": "valid-transfer-zip-hash-bound",
            "checks": {
                "dispatch.zip_hash_verified": True,
                "dispatch.source_message_hash_verified": True,
            },
            "expected": True,
        },
        "valid-ready-not-submitted.json": {
            "fixture": "valid-ready-not-submitted",
            "checks": {
                "dispatch.dispatch_ready": True,
                "dispatch.external_submission_performed": False,
                "authority_flags.actual_opus_result_present": False,
                "authority_flags.user_approval_present": False,
            },
            "expected": True,
        },
        "valid-opus-token-contract.json": {
            "fixture": "valid-opus-token-contract",
            "expected_tokens": TOKENS,
            "expected": True,
        },
        "valid-no-mainline-authority.json": {
            "fixture": "valid-no-mainline-authority",
            "checks": {
                "authority_flags.mainline_merge_allowed": False,
                "authority_flags.promotion_allowed": False,
                "authority_flags.reviewed_knowledge_ready": False,
                "authority_flags.evidence_support_ready": False,
                "authority_flags.action_basis_ready": False,
                "authority_flags.goal_complete_now": False,
            },
            "expected": True,
        },
    }
    for filename, payload in fixtures.items():
        write_json(FIXTURES_DIR / filename, payload)

    failures = {
        "record_kind": "external_opus_dispatch_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {"id": "zip_hash_mismatch", "mutation": "zip_hash_mismatch", "expected_failure": "zip_hash_not_verified"},
            {"id": "source_message_hash_mismatch", "mutation": "source_message_hash_mismatch", "expected_failure": "source_message_hash_not_verified"},
            {"id": "source_message_sha_field_mismatch", "mutation": "source_message_sha_field_mismatch", "expected_failure": "source_message_sha_mismatch"},
            {"id": "wrong_operator_message_path", "mutation": "wrong_operator_message_path", "expected_failure": "source_input_path_mismatch:operator_submission_message"},
            {"id": "wrong_readiness_cockpit_path", "mutation": "wrong_readiness_cockpit_path", "expected_failure": "source_input_path_mismatch:readiness_cockpit"},
            {"id": "wrong_post_response_validator", "mutation": "wrong_post_response_validator", "expected_failure": "post_response_validator_mismatch"},
            {"id": "dispatch_not_ready", "mutation": "dispatch_not_ready", "expected_failure": "dispatch_not_ready"},
            {"id": "chain_not_ready", "mutation": "chain_not_ready", "expected_failure": "readiness_input_not_true:chain_ready_to_submit_external_opus"},
            {"id": "missing_required_token", "mutation": "remove_required_token", "expected_failure": "required_tokens_mismatch"},
            {"id": "prompt_missing_boundary", "mutation": "prompt_missing_boundary", "expected_failure": "message_missing_phrase:not an Opus response"},
            {"id": "claims_external_submission", "mutation": "external_submission_performed_true", "expected_failure": "authority_overclaim:external_submission_performed"},
            {"id": "claims_actual_opus_result", "mutation": "actual_opus_result_present_true", "expected_failure": "authority_overclaim:actual_opus_result_present"},
            {"id": "claims_validated_opus_pass", "mutation": "validated_opus_pass_present_true", "expected_failure": "authority_overclaim:validated_opus_pass_present"},
            {"id": "claims_user_approval", "mutation": "user_approval_present_true", "expected_failure": "authority_overclaim:user_approval_present"},
            {"id": "claims_mainline_ready", "mutation": "mainline_ready_true", "expected_failure": "authority_overclaim:mainline_ready"},
            {"id": "allows_merge", "mutation": "mainline_merge_allowed_true", "expected_failure": "authority_overclaim:mainline_merge_allowed"},
            {"id": "allows_promotion", "mutation": "promotion_allowed_true", "expected_failure": "authority_overclaim:promotion_allowed"},
            {"id": "claims_reviewed_knowledge", "mutation": "reviewed_knowledge_ready_true", "expected_failure": "authority_overclaim:reviewed_knowledge_ready"},
            {"id": "claims_evidence_support", "mutation": "evidence_support_ready_true", "expected_failure": "authority_overclaim:evidence_support_ready"},
            {"id": "claims_action_basis", "mutation": "action_basis_ready_true", "expected_failure": "authority_overclaim:action_basis_ready"},
            {"id": "allows_commit_push_sync", "mutation": "commit_push_sync_ready_true", "expected_failure": "authority_overclaim:commit_push_sync_ready"},
            {"id": "claims_goal_complete", "mutation": "goal_complete_now_true", "expected_failure": "authority_overclaim:goal_complete_now"},
        ],
    }
    write_json(FAILURE_DIR / "external-opus-dispatch-failures.json", failures)
    return {
        "written": True,
        "summary": {
            "dispatch_ready": packet["dispatch"]["dispatch_ready"],
            "zip_hash_verified": packet["dispatch"]["zip_hash_verified"],
            "source_message_hash_verified": packet["dispatch"]["source_message_hash_verified"],
            "failure_case_count": len(failures["failure_cases"]),
            **packet["authority_flags"],
        },
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
