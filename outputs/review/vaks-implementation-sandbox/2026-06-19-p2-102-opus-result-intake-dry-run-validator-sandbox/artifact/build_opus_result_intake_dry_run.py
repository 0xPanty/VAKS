import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-102-opus-result-intake-dry-run-validator-sandbox"
INTAKE_SLICE_ID = "2026-06-19-p2-96-opus-result-intake-skeleton-sandbox"
OPERATOR_SLICE_ID = "2026-06-19-p2-101-opus-external-review-operator-kit-sandbox"

HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

INTAKE_SCHEMA_PATH = (
    REPO_ROOT
    / "outputs"
    / "review"
    / "vaks-implementation-sandbox"
    / INTAKE_SLICE_ID
    / "artifact"
    / "opus-result-intake-schema.json"
)
OPERATOR_CONTROL_CARD_PATH = (
    REPO_ROOT
    / "outputs"
    / "review"
    / "vaks-implementation-sandbox"
    / OPERATOR_SLICE_ID
    / "artifact"
    / "opus-external-review-operator-control-card.json"
)

MANIFEST_PATH = ARTIFACT_DIR / "opus-result-intake-dry-run-manifest.json"


def rel_repo(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def valid_record(token: str) -> dict:
    return {
        "record_kind": "opus_result_intake_dry_run_record",
        "dry_run_only": True,
        "actual_opus_result_present": False,
        "opus_review_performed": False,
        "mainline_approval": False,
        "mainline_merge": False,
        "promotion": False,
        "promotion_ready": False,
        "reviewed_knowledge": False,
        "reviewed_knowledge_ready": False,
        "evidence_support": False,
        "evidence_support_ready": False,
        "action_basis": False,
        "action_basis_ready": False,
        "commit_push_sync": False,
        "commit_push_sync_ready": False,
        "opus_approval_claimed": False,
        "user_mainline_approval": False,
        "mainline_ready": False,
        "goal_complete_now": False,
        "raw_conclusion_token": token,
        "reviewed_evidence": [
            "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox/artifact/opus-review-transfer-package.zip",
            "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox/artifact/opus-review-transfer-package-sha256.txt",
        ],
        "boundary_verdict": "not_mainline_approval",
        "raw_response_path": "artifact/raw-opus-result.md",
        "blocking_issues": [] if token == "OPUS_PASS_SANDBOX_CLOSEOUT" else ["dry_run_sample_issue"],
        "recommended_next_action": "create sandbox-only result intake slice after real Opus response",
        "authority_flags": {
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "commit_push_sync_ready": False,
            "goal_complete_now": False,
        },
    }


def build() -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    schema = json.loads(INTAKE_SCHEMA_PATH.read_text(encoding="utf-8"))
    control_card = json.loads(OPERATOR_CONTROL_CARD_PATH.read_text(encoding="utf-8"))
    allowed = schema["allowed_conclusion_tokens"]

    fixture_map = {
        "OPUS_PASS_SANDBOX_CLOSEOUT": "valid-opus-pass-result.json",
        "OPUS_REVISE_SANDBOX_CLOSEOUT": "valid-opus-revise-result.json",
        "OPUS_BLOCKED_NEEDS_USER": "valid-opus-blocked-result.json",
    }
    for token, filename in fixture_map.items():
        write_json(FIXTURES_DIR / filename, valid_record(token))

    failure_cases = {
        "record_kind": "opus_result_intake_dry_run_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "id": "bad_token",
                "record": valid_record("OPUS_APPROVED"),
                "expected_failure": "raw_conclusion_token_not_allowed",
            },
            {
                "id": "missing_reviewed_evidence",
                "record": {k: v for k, v in valid_record("OPUS_PASS_SANDBOX_CLOSEOUT").items() if k != "reviewed_evidence"},
                "expected_failure": "missing_required_field:reviewed_evidence",
            },
            {
                "id": "empty_reviewed_evidence",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"reviewed_evidence": []},
                "expected_failure": "reviewed_evidence_empty",
            },
            {
                "id": "missing_raw_response_path",
                "record": {k: v for k, v in valid_record("OPUS_PASS_SANDBOX_CLOSEOUT").items() if k != "raw_response_path"},
                "expected_failure": "missing_required_field:raw_response_path",
            },
            {
                "id": "bad_boundary_verdict",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"boundary_verdict": "mainline_approved"},
                "expected_failure": "boundary_verdict_not_allowed",
            },
            {
                "id": "opus_approval_overclaim",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"authority_flags": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT")["authority_flags"] | {"opus_approval_claimed": True}},
                "expected_failure": "authority_flag_overclaim:opus_approval_claimed",
            },
            {
                "id": "mainline_ready_overclaim",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"authority_flags": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT")["authority_flags"] | {"mainline_ready": True}},
                "expected_failure": "authority_flag_overclaim:mainline_ready",
            },
            {
                "id": "goal_complete_overclaim",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"authority_flags": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT")["authority_flags"] | {"goal_complete_now": True}},
                "expected_failure": "authority_flag_overclaim:goal_complete_now",
            },
            {
                "id": "not_dry_run",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"dry_run_only": False},
                "expected_failure": "dry_run_only_not_true",
            },
            {
                "id": "actual_result_present",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"actual_opus_result_present": True},
                "expected_failure": "actual_opus_result_present_not_false",
            },
            {
                "id": "wrong_record_kind",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"record_kind": "opus_result"},
                "expected_failure": "record_kind_not_allowed",
            },
            {
                "id": "unsafe_raw_response_path",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"raw_response_path": "../../README.md"},
                "expected_failure": "raw_response_path_unsafe",
            },
            {
                "id": "blank_reviewed_evidence_item",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"reviewed_evidence": ["   "]},
                "expected_failure": "reviewed_evidence_item_empty",
            },
            {
                "id": "unsupported_reviewed_evidence",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"reviewed_evidence": ["outputs/review/unrelated.md"]},
                "expected_failure": "reviewed_evidence_unsupported",
            },
            {
                "id": "p2_96_boundary_true_overclaim",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {
                    "mainline_approval": True,
                    "reviewed_knowledge": True,
                    "evidence_support": True,
                    "action_basis": True,
                    "commit_push_sync": True,
                },
                "expected_failure": "top_level_boundary_overclaim:mainline_approval",
            },
            {
                "id": "top_level_opus_approval_overclaim",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"opus_approval_claimed": True},
                "expected_failure": "top_level_boundary_overclaim:opus_approval_claimed",
            },
            {
                "id": "top_level_mainline_ready_overclaim",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"mainline_ready": True},
                "expected_failure": "top_level_boundary_overclaim:mainline_ready",
            },
            {
                "id": "top_level_goal_complete_overclaim",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"goal_complete_now": True},
                "expected_failure": "top_level_boundary_overclaim:goal_complete_now",
            },
            {
                "id": "top_level_ready_authority_overclaim",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {
                    "reviewed_knowledge_ready": True,
                    "evidence_support_ready": True,
                    "action_basis_ready": True,
                    "commit_push_sync_ready": True,
                },
                "expected_failure": "top_level_boundary_overclaim:reviewed_knowledge_ready",
            },
            {
                "id": "top_level_promotion_overclaim",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {
                    "mainline_merge": True,
                    "promotion": True,
                    "promotion_ready": True,
                    "user_mainline_approval": True,
                },
                "expected_failure": "top_level_boundary_overclaim:mainline_merge",
            },
            {
                "id": "top_level_opus_review_performed_overclaim",
                "record": valid_record("OPUS_PASS_SANDBOX_CLOSEOUT") | {"opus_review_performed": True},
                "expected_failure": "top_level_boundary_overclaim:opus_review_performed",
            },
        ],
    }
    write_json(FAILURE_DIR / "opus-result-intake-dry-run-failures.json", failure_cases)

    manifest = {
        "record_kind": "opus_result_intake_dry_run_manifest",
        "slice_id": SLICE_ID,
        "schema_source": rel_repo(INTAKE_SCHEMA_PATH),
        "operator_control_card_source": rel_repo(OPERATOR_CONTROL_CARD_PATH),
        "allowed_conclusion_tokens": allowed,
        "required_fields_when_result_exists": schema["required_fields_when_result_exists"],
        "operator_transfer_zip_sha256": control_card["transfer_package"]["zip_sha256"],
        "summary": {
            "dry_run_validator_ready": True,
            "valid_fixture_count": len(fixture_map),
            "failure_case_count": len(failure_cases["failure_cases"]),
            "actual_opus_result_present": False,
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
        },
        "authority_flags": {
            "dry_run_only": True,
            "actual_opus_result_present": False,
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "commit_push_sync_ready": False,
            "goal_complete_now": False,
        },
    }
    write_json(MANIFEST_PATH, manifest)

    return {"written": True, "summary": manifest["summary"]}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
