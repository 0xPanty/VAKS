from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-96-opus-result-intake-skeleton-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = ROOT / "outputs/review/vaks-implementation-sandbox"
SLICE_DIR = SANDBOX_ROOT / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

P2_94_PACKET = (
    SANDBOX_ROOT
    / "2026-06-19-p2-94-opus-review-submission-packet-sandbox/artifact/opus-review-submission-packet.json"
)
P2_94_GATE = (
    SANDBOX_ROOT
    / "2026-06-19-p2-94-opus-review-submission-packet-sandbox/artifact/opus-result-intake-gate.md"
)
P2_95_LEDGER = (
    SANDBOX_ROOT
    / "2026-06-19-p2-95-goal-state-external-review-waiting-ledger-sandbox/artifact/goal-state-external-review-waiting-ledger.json"
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_schema(allowed_tokens: list[str]) -> dict:
    return {
        "record_kind": "opus_result_intake_schema",
        "slice_id": SLICE_ID,
        "allowed_conclusion_tokens": allowed_tokens,
        "required_fields_when_result_exists": [
            "raw_conclusion_token",
            "reviewed_evidence",
            "boundary_verdict",
            "raw_response_path",
        ],
        "boundary_requirements": {
            "mainline_approval": False,
            "reviewed_knowledge": False,
            "evidence_support": False,
            "action_basis": False,
            "commit_push_sync": False,
        },
    }


def build_status() -> dict:
    p2_94 = load_json(P2_94_PACKET)
    p2_95 = load_json(P2_95_LEDGER)
    allowed_tokens = p2_94["allowed_external_conclusions"]
    status = {
        "record_kind": "opus_result_intake_status",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_94_submission_packet": rel(P2_94_PACKET),
            "p2_94_result_intake_gate": rel(P2_94_GATE),
            "p2_95_goal_state_ledger": rel(P2_95_LEDGER),
        },
        "summary": {
            "allowed_conclusion_token_count": len(allowed_tokens),
            "raw_result_placeholder_present": True,
            "actual_opus_result_present": False,
            "opus_review_performed": False,
            "opus_approval_claimed": False,
            "result_intake_ready": True,
            "p2_95_external_opus_review_pending": p2_95["summary"]["external_opus_review_pending"],
            "p2_95_goal_complete_now": p2_95["summary"]["goal_complete_now"],
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "commit_push_sync_ready": False,
            "goal_complete_now": False,
        },
        "allowed_conclusion_tokens": allowed_tokens,
        "expected_future_result_record": {
            "raw_conclusion_token": "<one allowed token>",
            "reviewed_evidence": ["<paths Opus says it inspected>"],
            "blockers": [],
            "boundary_verdict": "not_mainline_approval",
            "raw_response_path": "artifact/raw-opus-result.md",
        },
        "authority_flags": {
            "skeleton_only": True,
            "actual_opus_result_present": False,
            "opus_review_performed": False,
            "opus_approval_claimed": False,
            "mainline_merge": False,
            "promotion": False,
            "reviewed_knowledge": False,
            "evidence_support": False,
            "action_basis": False,
            "user_mainline_approval": False,
            "commit_push_sync": False,
            "goal_complete_now": False,
        },
    }
    return status


def write_placeholder() -> None:
    write_text(
        ARTIFACT_DIR / "raw-opus-result-placeholder.md",
        """# Raw Opus Result Placeholder

No external Opus result has been received yet.

When Opus responds, do not overwrite this file silently. Create a later sandbox-only intake slice and store the raw response there.

Allowed first-line conclusion tokens:

- `OPUS_PASS_SANDBOX_CLOSEOUT`
- `OPUS_REVISE_SANDBOX_CLOSEOUT`
- `OPUS_BLOCKED_NEEDS_USER`

This placeholder is not Opus approval and not mainline approval.
""",
    )


def render_status_md(status: dict) -> str:
    rows = "\n".join(f"| `{key}` | `{value}` |" for key, value in status["summary"].items())
    tokens = "\n".join(f"- `{token}`" for token in status["allowed_conclusion_tokens"])
    return f"""# Opus Result Intake Status

## Plain Verdict

The result intake skeleton is ready, but no actual Opus result exists. This file is not Opus approval.

## Summary

| Field | Value |
| --- | --- |
{rows}

## Allowed Tokens

{tokens}

## Boundary

Even `OPUS_PASS_SANDBOX_CLOSEOUT` is sandbox closeout only. It is not mainline approval, reviewed knowledge, evidence support, action basis, commit, push, or sync.
"""


def write_fixtures(status: dict) -> None:
    s = status["summary"]
    write_json(
        FIXTURES_DIR / "pending-result-not-approval.json",
        {
            "case_id": "pending-result-not-approval",
            "actual_opus_result_present": s["actual_opus_result_present"],
            "opus_review_performed": s["opus_review_performed"],
            "opus_approval_claimed": s["opus_approval_claimed"],
            "passed": not s["actual_opus_result_present"]
            and not s["opus_review_performed"]
            and not s["opus_approval_claimed"],
        },
    )
    write_json(
        FIXTURES_DIR / "allowed-conclusion-tokens.json",
        {
            "case_id": "allowed-conclusion-tokens",
            "allowed_conclusion_tokens": status["allowed_conclusion_tokens"],
            "passed": status["allowed_conclusion_tokens"]
            == [
                "OPUS_PASS_SANDBOX_CLOSEOUT",
                "OPUS_REVISE_SANDBOX_CLOSEOUT",
                "OPUS_BLOCKED_NEEDS_USER",
            ],
        },
    )
    write_json(
        FIXTURES_DIR / "intake-ready-with-opus-pending.json",
        {
            "case_id": "intake-ready-with-opus-pending",
            "result_intake_ready": s["result_intake_ready"],
            "p2_95_external_opus_review_pending": s["p2_95_external_opus_review_pending"],
            "passed": s["result_intake_ready"] and s["p2_95_external_opus_review_pending"],
        },
    )
    write_json(
        FIXTURES_DIR / "authority-boundaries-false.json",
        {
            "case_id": "authority-boundaries-false",
            "mainline_ready": s["mainline_ready"],
            "reviewed_knowledge_ready": s["reviewed_knowledge_ready"],
            "evidence_support_ready": s["evidence_support_ready"],
            "action_basis_ready": s["action_basis_ready"],
            "commit_push_sync_ready": s["commit_push_sync_ready"],
            "goal_complete_now": s["goal_complete_now"],
            "passed": not any(
                [
                    s["mainline_ready"],
                    s["reviewed_knowledge_ready"],
                    s["evidence_support_ready"],
                    s["action_basis_ready"],
                    s["commit_push_sync_ready"],
                    s["goal_complete_now"],
                ]
            ),
        },
    )
    write_json(
        FIXTURES_DIR / "future-result-record-contract.json",
        {
            "case_id": "future-result-record-contract",
            "required_keys": sorted(status["expected_future_result_record"].keys()),
            "passed": sorted(status["expected_future_result_record"].keys())
            == ["blockers", "boundary_verdict", "raw_conclusion_token", "raw_response_path", "reviewed_evidence"],
        },
    )


def write_failure_cases() -> None:
    write_json(
        FAILURE_DIR / "opus-result-intake-skeleton-failures.json",
        {
            "record_kind": "opus_result_intake_skeleton_failure_cases",
            "slice_id": SLICE_ID,
            "failure_cases": [
                {
                    "case_id": "P2-96-FAIL-01-invalid-opus-token",
                    "must_fail_when": "A future result uses a conclusion token outside the three p2-94 allowed tokens.",
                },
                {
                    "case_id": "P2-96-FAIL-02-approval-without-result",
                    "must_fail_when": "The skeleton claims Opus approval while no actual Opus response exists.",
                },
                {
                    "case_id": "P2-96-FAIL-03-mainline-approval-confusion",
                    "must_fail_when": "A sandbox or Opus pass is treated as mainline approval.",
                },
                {
                    "case_id": "P2-96-FAIL-04-truth-authority-confusion",
                    "must_fail_when": "A sandbox or Opus pass is treated as reviewed knowledge, evidence support, or action basis.",
                },
                {
                    "case_id": "P2-96-FAIL-05-missing-reviewed-evidence-list",
                    "must_fail_when": "A future result lacks a list of evidence files Opus says it reviewed.",
                },
                {
                    "case_id": "P2-96-FAIL-06-missing-boundary-verdict",
                    "must_fail_when": "A future result lacks a boundary verdict.",
                },
                {
                    "case_id": "P2-96-FAIL-07-result-overwrites-placeholder",
                    "must_fail_when": "A real Opus result overwrites this placeholder instead of a later sandbox intake slice.",
                },
                {
                    "case_id": "P2-96-FAIL-08-protected-path-write",
                    "must_fail_when": "This slice writes outside its own sandbox path.",
                },
            ],
        },
    )


def write_outputs() -> dict:
    status = build_status()
    schema = build_schema(status["allowed_conclusion_tokens"])
    write_placeholder()
    write_json(ARTIFACT_DIR / "opus-result-intake-schema.json", schema)
    write_json(ARTIFACT_DIR / "opus-result-intake-status.json", status)
    write_text(ARTIFACT_DIR / "opus-result-intake-status.md", render_status_md(status))
    write_fixtures(status)
    write_failure_cases()
    return status


def main() -> None:
    status = write_outputs()
    print(json.dumps({"written": True, "summary": status["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

