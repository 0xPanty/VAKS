import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-104-post-opus-user-approval-decision-packet-sandbox"
OUTCOME_SLICE_ID = "2026-06-19-p2-103-opus-outcome-action-gate-matrix-sandbox"
EXACT_APPROVAL_PHRASE = (
    "I explicitly approve post-Opus mainline consideration for VAKS sandbox closeout: "
    "prepare a separate merge proposal only; do not merge, promote, commit, push, sync, "
    "or write reviewed knowledge/action basis without my next explicit approval."
)

HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

OUTCOME_MATRIX_PATH = (
    REPO_ROOT / "outputs" / "review" / "vaks-implementation-sandbox" / OUTCOME_SLICE_ID / "artifact" / "opus-outcome-action-gate-matrix.json"
)
PACKET_PATH = ARTIFACT_DIR / "post-opus-user-approval-decision-packet.md"
CONTROL_CARD_PATH = ARTIFACT_DIR / "post-opus-user-approval-control-card.json"


def rel_repo(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def base_decision_record() -> dict:
    return {
        "record_kind": "post_opus_user_approval_decision_dry_run",
        "dry_run_only": True,
        "actual_opus_result_present": False,
        "validated_opus_pass_present": False,
        "user_approval_present": False,
        "exact_approval_phrase": EXACT_APPROVAL_PHRASE,
        "user_message": "",
        "allowed_next_state": "not_ready_for_mainline_consideration",
        "authority_flags": {
            "mainline_merge_allowed": False,
            "promotion_allowed": False,
            "reviewed_knowledge_write_allowed": False,
            "evidence_support_write_allowed": False,
            "action_basis_allowed": False,
            "commit_allowed": False,
            "push_allowed": False,
            "sync_allowed": False,
            "goal_complete_now": False,
        },
    }


def build() -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    matrix = json.loads(OUTCOME_MATRIX_PATH.read_text(encoding="utf-8"))
    pass_gate = matrix["outcomes"]["OPUS_PASS_SANDBOX_CLOSEOUT"]

    packet = f"""# Post-Opus User Approval Decision Packet

## Purpose

Use this packet only after a real `OPUS_PASS_SANDBOX_CLOSEOUT` result has been retained and validated in a sandbox-only result-intake slice.

## Current Dry-Run State

- actual_opus_result_present: false
- validated_opus_pass_present: false
- user_approval_present: false
- mainline_merge_allowed: false
- promotion_allowed: false
- reviewed_knowledge_write_allowed: false
- evidence_support_write_allowed: false
- action_basis_allowed: false
- commit_push_sync_allowed: false
- goal_complete_now: false

## Exact Future Approval Phrase

The future user message must exactly match:

```text
{EXACT_APPROVAL_PHRASE}
```

## Boundary

Opus PASS is not user approval. This packet is not merge, promotion, reviewed knowledge, evidence support, action basis, commit, push, sync, or goal completion.

## Allowed After Exact Future Approval

Prepare a separate merge proposal only. The proposal must still be separately reviewed and explicitly approved before any mainline edit, promotion, commit, push, sync, or truth/action write.
"""
    write_text(PACKET_PATH, packet)

    control_card = {
        "record_kind": "post_opus_user_approval_control_card",
        "slice_id": SLICE_ID,
        "outcome_matrix_path": rel_repo(OUTCOME_MATRIX_PATH),
        "packet_path": rel_repo(PACKET_PATH),
        "required_preconditions": {
            "actual_opus_result_present": True,
            "validated_opus_pass_present": True,
            "exact_user_approval_present": True,
        },
        "current_state": {
            "dry_run_only": True,
            "actual_opus_result_present": False,
            "validated_opus_pass_present": False,
            "user_approval_present": False,
            "ready_for_merge_proposal": False,
            "mainline_merge_allowed": False,
            "goal_complete_now": False,
        },
        "exact_approval_phrase": EXACT_APPROVAL_PHRASE,
        "p2_103_pass_gate": {
            "allowed_next_actions": pass_gate["allowed_next_actions"],
            "required_user_state": pass_gate["required_user_state"],
            "mainline_actions_require_separate_user_approval": pass_gate["authority_flags"]["mainline_actions_require_separate_user_approval"],
        },
        "post_exact_approval_allowed_state": {
            "prepare_merge_proposal_only": True,
            "mainline_merge_allowed": False,
            "promotion_allowed": False,
            "reviewed_knowledge_write_allowed": False,
            "evidence_support_write_allowed": False,
            "action_basis_allowed": False,
            "commit_allowed": False,
            "push_allowed": False,
            "sync_allowed": False,
            "goal_complete_now": False,
        },
    }
    write_json(CONTROL_CARD_PATH, control_card)

    fixtures = {
        "dry-run-no-opus-no-user-approval.json": base_decision_record(),
        "validated-opus-pass-no-user-approval.json": base_decision_record()
        | {
            "actual_opus_result_present": True,
            "validated_opus_pass_present": True,
            "allowed_next_state": "await_exact_user_approval",
        },
        "validated-opus-pass-exact-user-approval.json": base_decision_record()
        | {
            "actual_opus_result_present": True,
            "validated_opus_pass_present": True,
            "user_approval_present": True,
            "user_message": EXACT_APPROVAL_PHRASE,
            "allowed_next_state": "prepare_merge_proposal_only",
        },
    }
    for filename, payload in fixtures.items():
        write_json(FIXTURES_DIR / filename, payload)

    authority_failure_cases = [
        {
            "id": f"exact_user_approval_claims_{flag}",
            "record": base_decision_record() | {
                "actual_opus_result_present": True,
                "validated_opus_pass_present": True,
                "user_approval_present": True,
                "user_message": EXACT_APPROVAL_PHRASE,
                "authority_flags": base_decision_record()["authority_flags"] | {flag: True},
            },
            "expected_failure": f"authority_flag_overclaim:{flag}",
        }
        for flag in [
            "mainline_merge_allowed",
            "promotion_allowed",
            "reviewed_knowledge_write_allowed",
            "evidence_support_write_allowed",
            "action_basis_allowed",
            "commit_allowed",
            "push_allowed",
            "sync_allowed",
            "goal_complete_now",
        ]
    ]

    failures = {
        "record_kind": "post_opus_user_approval_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "id": "user_approval_without_opus_pass",
                "record": base_decision_record() | {
                    "user_approval_present": True,
                    "user_message": EXACT_APPROVAL_PHRASE,
                },
                "expected_failure": "user_approval_before_validated_opus_pass",
            },
            {
                "id": "opus_pass_without_exact_user_phrase",
                "record": base_decision_record() | {
                    "actual_opus_result_present": True,
                    "validated_opus_pass_present": True,
                    "user_approval_present": True,
                    "user_message": "approved",
                },
                "expected_failure": "exact_approval_phrase_mismatch",
            },
            {
                "id": "opus_pass_claims_merge_allowed",
                "record": base_decision_record() | {
                    "actual_opus_result_present": True,
                    "validated_opus_pass_present": True,
                    "authority_flags": base_decision_record()["authority_flags"] | {"mainline_merge_allowed": True},
                },
                "expected_failure": "authority_flag_overclaim:mainline_merge_allowed",
            },
        ]
        + authority_failure_cases,
    }
    write_json(FAILURE_DIR / "post-opus-user-approval-failures.json", failures)

    return {
        "written": True,
        "summary": {
            "fixture_count": len(fixtures),
            "failure_case_count": len(failures["failure_cases"]),
            "actual_opus_result_present": False,
            "validated_opus_pass_present": False,
            "user_approval_present": False,
            "ready_for_merge_proposal": False,
            "mainline_merge_allowed": False,
            "goal_complete_now": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
