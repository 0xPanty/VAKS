import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-103-opus-outcome-action-gate-matrix-sandbox"
INTAKE_SLICE_ID = "2026-06-19-p2-96-opus-result-intake-skeleton-sandbox"
VALIDATOR_SLICE_ID = "2026-06-19-p2-102-opus-result-intake-dry-run-validator-sandbox"

HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

INTAKE_SCHEMA_PATH = (
    REPO_ROOT / "outputs" / "review" / "vaks-implementation-sandbox" / INTAKE_SLICE_ID / "artifact" / "opus-result-intake-schema.json"
)
DRY_RUN_MANIFEST_PATH = (
    REPO_ROOT / "outputs" / "review" / "vaks-implementation-sandbox" / VALIDATOR_SLICE_ID / "artifact" / "opus-result-intake-dry-run-manifest.json"
)

MATRIX_PATH = ARTIFACT_DIR / "opus-outcome-action-gate-matrix.json"
RUNBOOK_PATH = ARTIFACT_DIR / "opus-outcome-action-gate-runbook.md"

UNSAFE_ACTION_FLAGS = {
    "mainline_merge_allowed": False,
    "promotion_allowed": False,
    "reviewed_knowledge_write_allowed": False,
    "evidence_support_write_allowed": False,
    "action_basis_allowed": False,
    "commit_allowed": False,
    "push_allowed": False,
    "sync_allowed": False,
    "goal_complete_now": False,
}


def rel_repo(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def outcome_record(token: str, allowed_next_actions: list[str], required_user_state: str, stop_state: str) -> dict:
    return {
        "token": token,
        "allowed_next_actions": allowed_next_actions,
        "required_user_state": required_user_state,
        "stop_state": stop_state,
        "authority_flags": UNSAFE_ACTION_FLAGS | {
            "external_opus_result_required": True,
            "mainline_actions_require_separate_user_approval": True,
            "sandbox_only": True,
        },
        "prohibited_actions": [
            "automatic_mainline_merge",
            "automatic_promotion",
            "write_reviewed_knowledge",
            "write_evidence_support",
            "create_action_basis",
            "commit",
            "push",
            "obsidian_sync",
        ],
    }


def build() -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    schema = json.loads(INTAKE_SCHEMA_PATH.read_text(encoding="utf-8"))
    dry_run_manifest = json.loads(DRY_RUN_MANIFEST_PATH.read_text(encoding="utf-8"))
    allowed_tokens = schema["allowed_conclusion_tokens"]

    outcomes = {
        "OPUS_PASS_SANDBOX_CLOSEOUT": outcome_record(
            "OPUS_PASS_SANDBOX_CLOSEOUT",
            [
                "retain_raw_opus_result_in_sandbox",
                "run_result_intake_validator",
                "prepare_user_approval_decision_packet",
            ],
            "explicit_user_mainline_approval_still_required",
            "await_user_decision_after_validated_opus_pass",
        ),
        "OPUS_REVISE_SANDBOX_CLOSEOUT": outcome_record(
            "OPUS_REVISE_SANDBOX_CLOSEOUT",
            [
                "retain_raw_opus_result_in_sandbox",
                "create_revision_slice_in_sandbox",
                "rerun_reviewer_boundary_product_acceptance",
            ],
            "no_mainline_approval",
            "stay_in_current_sandbox_program",
        ),
        "OPUS_BLOCKED_NEEDS_USER": outcome_record(
            "OPUS_BLOCKED_NEEDS_USER",
            [
                "retain_raw_opus_result_in_sandbox",
                "stop_and_ask_user",
            ],
            "user_input_required_before_next_action",
            "blocked_needs_user",
        ),
    }

    matrix = {
        "record_kind": "opus_outcome_action_gate_matrix",
        "slice_id": SLICE_ID,
        "inputs": {
            "intake_schema_path": rel_repo(INTAKE_SCHEMA_PATH),
            "dry_run_manifest_path": rel_repo(DRY_RUN_MANIFEST_PATH),
        },
        "allowed_conclusion_tokens": allowed_tokens,
        "dry_run_validator_summary": dry_run_manifest["summary"],
        "outcomes": outcomes,
        "global_invariants": {
            "automatic_mainline_merge": False,
            "automatic_promotion": False,
            "reviewed_knowledge_write": False,
            "evidence_support_write": False,
            "action_basis": False,
            "commit_push_sync": False,
            "goal_complete_now": False,
            "external_opus_result_is_not_user_mainline_approval": True,
        },
        "summary": {
            "outcome_count": len(outcomes),
            "allowed_token_count": len(allowed_tokens),
            "all_outcomes_have_user_gate": True,
            "pass_does_not_authorize_merge": True,
            "actual_opus_result_present": False,
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "goal_complete_now": False,
        },
    }
    write_json(MATRIX_PATH, matrix)

    runbook = """# Opus Outcome Action Gate Runbook

## Purpose

Use this matrix after a real external Opus result has been retained and validated in a sandbox-only intake slice.

## Outcome Rules

- `OPUS_PASS_SANDBOX_CLOSEOUT`: retain the raw result, validate it, then prepare a user approval decision packet. It does not authorize automatic mainline merge.
- `OPUS_REVISE_SANDBOX_CLOSEOUT`: retain the raw result and create a revision slice in sandbox. Do not advance to the next program stage.
- `OPUS_BLOCKED_NEEDS_USER`: retain the raw result and stop for user input.

## Global Invariants

No Opus outcome authorizes automatic merge, promotion, reviewed knowledge writes, evidence support writes, action basis, commit, push, sync, or goal completion.
"""
    write_text(RUNBOOK_PATH, runbook)

    for token, record in outcomes.items():
        write_json(FIXTURES_DIR / f"valid-{token.lower().replace('_', '-')}.json", record)

    failure_cases = {
        "record_kind": "opus_outcome_action_gate_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "id": "pass_allows_mainline_merge",
                "token": "OPUS_PASS_SANDBOX_CLOSEOUT",
                "mutations": {"mainline_merge_allowed": True},
                "expected_failure": "unsafe_action_allowed:mainline_merge_allowed",
            },
            {
                "id": "pass_allows_promotion",
                "token": "OPUS_PASS_SANDBOX_CLOSEOUT",
                "mutations": {"promotion_allowed": True},
                "expected_failure": "unsafe_action_allowed:promotion_allowed",
            },
            {
                "id": "pass_allows_reviewed_knowledge",
                "token": "OPUS_PASS_SANDBOX_CLOSEOUT",
                "mutations": {"reviewed_knowledge_write_allowed": True},
                "expected_failure": "unsafe_action_allowed:reviewed_knowledge_write_allowed",
            },
            {
                "id": "pass_allows_evidence_support",
                "token": "OPUS_PASS_SANDBOX_CLOSEOUT",
                "mutations": {"evidence_support_write_allowed": True},
                "expected_failure": "unsafe_action_allowed:evidence_support_write_allowed",
            },
            {
                "id": "pass_allows_action_basis",
                "token": "OPUS_PASS_SANDBOX_CLOSEOUT",
                "mutations": {"action_basis_allowed": True},
                "expected_failure": "unsafe_action_allowed:action_basis_allowed",
            },
            {
                "id": "pass_allows_commit",
                "token": "OPUS_PASS_SANDBOX_CLOSEOUT",
                "mutations": {"commit_allowed": True},
                "expected_failure": "unsafe_action_allowed:commit_allowed",
            },
            {
                "id": "pass_allows_push",
                "token": "OPUS_PASS_SANDBOX_CLOSEOUT",
                "mutations": {"push_allowed": True},
                "expected_failure": "unsafe_action_allowed:push_allowed",
            },
            {
                "id": "pass_allows_sync",
                "token": "OPUS_PASS_SANDBOX_CLOSEOUT",
                "mutations": {"sync_allowed": True},
                "expected_failure": "unsafe_action_allowed:sync_allowed",
            },
            {
                "id": "pass_claims_goal_complete",
                "token": "OPUS_PASS_SANDBOX_CLOSEOUT",
                "mutations": {"goal_complete_now": True},
                "expected_failure": "unsafe_action_allowed:goal_complete_now",
            },
            {
                "id": "revise_claims_goal_complete",
                "token": "OPUS_REVISE_SANDBOX_CLOSEOUT",
                "mutations": {"goal_complete_now": True},
                "expected_failure": "unsafe_action_allowed:goal_complete_now",
            },
            {
                "id": "blocked_allows_next_action_without_user",
                "token": "OPUS_BLOCKED_NEEDS_USER",
                "mutations": {"mainline_actions_require_separate_user_approval": False},
                "expected_failure": "mainline_user_gate_missing",
            },
            {
                "id": "unknown_token",
                "token": "OPUS_APPROVED",
                "mutations": {},
                "expected_failure": "unknown_token",
            },
        ],
    }
    write_json(FAILURE_DIR / "opus-outcome-action-gate-failures.json", failure_cases)

    return {
        "written": True,
        "summary": matrix["summary"] | {
            "failure_case_count": len(failure_cases["failure_cases"]),
        },
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
