import hashlib
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-107-external-opus-manual-submission-brief-sandbox"
HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

P2_106 = REPO_ROOT / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-106-external-opus-dispatch-packet-sandbox"
DISPATCH_PACKET = P2_106 / "artifact/external-opus-dispatch-packet.json"
DISPATCH_MESSAGE = P2_106 / "artifact/external-opus-dispatch-message.md"
DISPATCH_CHECKLIST = P2_106 / "artifact/external-opus-dispatch-checklist.md"

OUT_JSON = ARTIFACT_DIR / "external-opus-manual-submission-brief.json"
OUT_BRIEF = ARTIFACT_DIR / "external-opus-manual-submission-brief.md"
OUT_CAPTURE = ARTIFACT_DIR / "external-opus-response-capture-card.md"


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build() -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    dispatch_packet = read_json(DISPATCH_PACKET)
    message_text = DISPATCH_MESSAGE.read_text(encoding="utf-8")
    checklist_text = DISPATCH_CHECKLIST.read_text(encoding="utf-8")
    dispatch = dispatch_packet["dispatch"]
    authority = dispatch_packet["authority_flags"]

    brief_text = "\n".join([
        "# External Opus Manual Submission Brief",
        "",
        "Use this as the operator-facing one-page brief for external Opus submission.",
        "",
        "## Attach",
        "",
        f"- ZIP: `{dispatch['zip_path']}`",
        f"- ZIP SHA256: `{dispatch['zip_sha256']}`",
        f"- Dispatch message: `{dispatch['dispatch_message_path']}`",
        "",
        "## Required Opus Result Token",
        "",
        "- `OPUS_PASS_SANDBOX_CLOSEOUT`",
        "- `OPUS_REVISE_SANDBOX_CLOSEOUT`",
        "- `OPUS_BLOCKED_NEEDS_USER`",
        "",
        "## Required Response Fields",
        "",
        "- `raw_conclusion_token`",
        "- `reviewed_evidence`",
        "- `boundary_verdict`",
        "- `blocking_issues`",
        "- `recommended_next_action`",
        "",
        "## After Opus Responds",
        "",
        "Preserve the raw Opus response in a new sandbox-only intake slice. Validate it with p2-102 before any user approval or merge discussion.",
        "",
        "## Boundary",
        "",
        "This manual brief is not external submission, not an Opus response, not Opus approval, not user approval, not mainline readiness, not mainline merge, not promotion, not reviewed knowledge, not evidence support, not action basis, not commit, not push, not sync, and not goal completion.",
        "",
    ]) + "\n"
    write_text(OUT_BRIEF, brief_text)

    capture_text = "\n".join([
        "# External Opus Response Capture Card",
        "",
        "Status: raw response not yet present.",
        "",
        "When Opus responds, create a new sandbox-only intake slice and preserve the exact raw response there. Do not paste a response into this p2-107 slice.",
        "",
        "Required capture fields:",
        "",
        "- `raw_response_path`",
        "- `raw_conclusion_token`",
        "- `reviewed_evidence`",
        "- `boundary_verdict`",
        "- `blocking_issues`",
        "- `recommended_next_action`",
        "",
        "Allowed conclusion tokens:",
        "",
        "- `OPUS_PASS_SANDBOX_CLOSEOUT`",
        "- `OPUS_REVISE_SANDBOX_CLOSEOUT`",
        "- `OPUS_BLOCKED_NEEDS_USER`",
        "",
        "Boundary: raw Opus response is external review evidence only. It is not user approval, not mainline readiness, not reviewed knowledge, not evidence support, not action basis, not commit, not push, and not sync.",
        "",
    ]) + "\n"
    write_text(OUT_CAPTURE, capture_text)

    packet = {
        "record_kind": "external_opus_manual_submission_brief",
        "slice_id": SLICE_ID,
        "source_inputs": {
            "dispatch_packet": rel(DISPATCH_PACKET),
            "dispatch_message": rel(DISPATCH_MESSAGE),
            "dispatch_checklist": rel(DISPATCH_CHECKLIST),
        },
        "source_hashes": {
            "dispatch_packet_sha256": sha256_file(DISPATCH_PACKET),
            "dispatch_message_sha256": sha256_file(DISPATCH_MESSAGE),
            "dispatch_checklist_sha256": sha256_file(DISPATCH_CHECKLIST),
            "expected_dispatch_message_sha256": dispatch["dispatch_message_sha256"],
            "expected_dispatch_checklist_sha256": dispatch["dispatch_checklist_sha256"],
        },
        "manual_submission": {
            "brief_ready": True,
            "brief_path": rel(OUT_BRIEF),
            "brief_sha256": sha256_file(OUT_BRIEF),
            "response_capture_card_path": rel(OUT_CAPTURE),
            "response_capture_card_sha256": sha256_file(OUT_CAPTURE),
            "zip_path": dispatch["zip_path"],
            "zip_sha256": dispatch["zip_sha256"],
            "dispatch_message_path": dispatch["dispatch_message_path"],
            "required_conclusion_tokens": dispatch["required_conclusion_tokens"],
            "post_response_validator_slice": dispatch["post_response_validator_slice"],
            "raw_response_present": False,
            "new_sandbox_intake_required": True,
        },
        "authority_flags": {
            "manual_submission_brief_only": True,
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
        "dispatch_authority_snapshot": authority,
    }
    write_json(OUT_JSON, packet)

    fixtures = {
        "valid-one-page-brief-ready.json": {
            "fixture": "valid-one-page-brief-ready",
            "checks": {
                "manual_submission.brief_ready": True,
                "manual_submission.raw_response_present": False,
                "manual_submission.new_sandbox_intake_required": True,
            },
            "expected": True,
        },
        "valid-source-hash-binding.json": {
            "fixture": "valid-source-hash-binding",
            "checks": {
                "source_hashes.dispatch_message_sha256": packet["source_hashes"]["expected_dispatch_message_sha256"],
                "source_hashes.dispatch_checklist_sha256": packet["source_hashes"]["expected_dispatch_checklist_sha256"],
            },
            "expected": True,
        },
        "valid-response-capture-boundary.json": {
            "fixture": "valid-response-capture-boundary",
            "checks": {
                "manual_submission.post_response_validator_slice": "2026-06-19-p2-102-opus-result-intake-dry-run-validator-sandbox",
                "authority_flags.raw_opus_response_present": False,
                "authority_flags.validated_opus_pass_present": False,
            },
            "expected": True,
        },
        "valid-no-mainline-authority.json": {
            "fixture": "valid-no-mainline-authority",
            "checks": {
                "authority_flags.user_approval_present": False,
                "authority_flags.mainline_merge_allowed": False,
                "authority_flags.promotion_allowed": False,
                "authority_flags.action_basis_ready": False,
                "authority_flags.goal_complete_now": False,
            },
            "expected": True,
        },
    }
    for filename, payload in fixtures.items():
        write_json(FIXTURES_DIR / filename, payload)

    failures = {
        "record_kind": "external_opus_manual_submission_brief_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {"id": "dispatch_message_hash_drift", "mutation": "dispatch_message_hash_drift", "expected_failure": "source_hash_mismatch:dispatch_message"},
            {"id": "dispatch_checklist_hash_drift", "mutation": "dispatch_checklist_hash_drift", "expected_failure": "source_hash_mismatch:dispatch_checklist"},
            {"id": "missing_required_token", "mutation": "missing_required_token", "expected_failure": "required_tokens_mismatch"},
            {"id": "wrong_validator_slice", "mutation": "wrong_validator_slice", "expected_failure": "post_response_validator_mismatch"},
            {"id": "claims_external_submission", "mutation": "external_submission_performed_true", "expected_failure": "authority_overclaim:external_submission_performed"},
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
            {"id": "brief_missing_boundary", "mutation": "brief_missing_boundary", "expected_failure": "brief_missing_phrase:not an Opus response"},
            {"id": "capture_missing_new_sandbox", "mutation": "capture_missing_new_sandbox", "expected_failure": "capture_missing_phrase:new sandbox-only intake slice"},
        ],
    }
    write_json(FAILURE_DIR / "external-opus-manual-submission-brief-failures.json", failures)
    return {
        "written": True,
        "summary": {
            "brief_ready": True,
            "fixture_count": len(fixtures),
            "failure_case_count": len(failures["failure_cases"]),
            **packet["authority_flags"],
        },
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
