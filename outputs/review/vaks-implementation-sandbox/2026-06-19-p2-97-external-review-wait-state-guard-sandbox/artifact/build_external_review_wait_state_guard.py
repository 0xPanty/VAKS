from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-97-external-review-wait-state-guard-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = ROOT / "outputs/review/vaks-implementation-sandbox"
SLICE_DIR = SANDBOX_ROOT / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

P2_95_LEDGER = (
    SANDBOX_ROOT
    / "2026-06-19-p2-95-goal-state-external-review-waiting-ledger-sandbox/artifact/goal-state-external-review-waiting-ledger.json"
)
P2_96_STATUS = (
    SANDBOX_ROOT
    / "2026-06-19-p2-96-opus-result-intake-skeleton-sandbox/artifact/opus-result-intake-status.json"
)
P2_94_PROMPT = (
    SANDBOX_ROOT
    / "2026-06-19-p2-94-opus-review-submission-packet-sandbox/artifact/opus-review-submission-prompt.md"
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


def build_guard() -> dict:
    p2_95 = load_json(P2_95_LEDGER)
    p2_96 = load_json(P2_96_STATUS)
    summary = {
        "guard_state": "STOP_WAIT_EXTERNAL_OPUS_REVIEW",
        "sandbox_closeout_evidence_product_grade": p2_95["summary"]["sandbox_closeout_evidence_product_grade"],
        "result_intake_ready": p2_96["summary"]["result_intake_ready"],
        "actual_opus_result_present": p2_96["summary"]["actual_opus_result_present"],
        "external_opus_review_pending": p2_95["summary"]["external_opus_review_pending"],
        "opus_approval_claimed": False,
        "mainline_ready": False,
        "promotion_ready": False,
        "reviewed_knowledge_ready": False,
        "evidence_support_ready": False,
        "action_basis_ready": False,
        "commit_push_sync_ready": False,
        "goal_complete_now": False,
        "may_continue_sandbox_preparation": True,
        "may_merge_mainline": False,
        "may_claim_complete": False,
    }
    no_go_conditions = [
        "No valid external Opus result has been received.",
        "Opus approval is not claimed.",
        "User mainline approval has not been granted.",
        "Sandbox closeout evidence is not reviewed knowledge, evidence support, or action basis.",
    ]
    required_next_actions = [
        f"Run external Opus review using {rel(P2_94_PROMPT)}.",
        "When a real response exists, create a new sandbox-only result intake slice.",
        "Validate the raw response against the p2-96 intake schema and validator.",
        "Run Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance before any further claim.",
    ]
    return {
        "record_kind": "external_review_wait_state_guard",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_95_goal_state_ledger": rel(P2_95_LEDGER),
            "p2_96_opus_result_intake_status": rel(P2_96_STATUS),
            "p2_94_opus_submission_prompt": rel(P2_94_PROMPT),
        },
        "summary": summary,
        "no_go_conditions": no_go_conditions,
        "required_next_actions": required_next_actions,
        "authority_flags": {
            "stop_wait_guard": True,
            "actual_opus_result_present": False,
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


def render_guard_md(guard: dict) -> str:
    rows = "\n".join(f"| `{key}` | `{value}` |" for key, value in guard["summary"].items())
    no_go = "\n".join(f"- {item}" for item in guard["no_go_conditions"])
    actions = "\n".join(f"- {item}" for item in guard["required_next_actions"])
    return f"""# External Review Wait-State Guard

## Guard State

`STOP_WAIT_EXTERNAL_OPUS_REVIEW`

## Plain Verdict

Sandbox closeout evidence is product-grade, but this is a STOP/WAIT state. Do not merge mainline, do not claim complete, and do not treat sandbox evidence as reviewed knowledge, evidence support, or action basis.

## Summary

| Field | Value |
| --- | --- |
{rows}

## No-Go Conditions

{no_go}

## Required Next Actions

{actions}
"""


def render_no_merge_checklist(guard: dict) -> str:
    checks = [
        "Actual external Opus result exists.",
        "Opus result validates against p2-96 schema.",
        "Opus result was captured in a later sandbox-only intake slice.",
        "Boundary Auditor confirms result is not mainline approval.",
        "User separately approves any mainline integration.",
    ]
    rows = "\n".join(f"- [ ] {item}" for item in checks)
    return f"""# No-Merge Checklist

Do not merge, promote, commit, push, sync, or write truth layers unless every item below is complete.

{rows}

Current guard state: `{guard["summary"]["guard_state"]}`.
"""


def render_wait_handoff(guard: dict) -> str:
    return f"""# Wait-State Handoff

Current state: `{guard["summary"]["guard_state"]}`.

The system is waiting for a real external Opus review result. Use the p2-94 submission prompt, then intake the response through p2-96 validation in a new sandbox-only slice.

Do not claim goal completion. Do not merge mainline.
"""


def write_fixtures(guard: dict) -> None:
    s = guard["summary"]
    write_json(
        FIXTURES_DIR / "stop-wait-guard-active.json",
        {
            "case_id": "stop-wait-guard-active",
            "guard_state": s["guard_state"],
            "external_opus_review_pending": s["external_opus_review_pending"],
            "actual_opus_result_present": s["actual_opus_result_present"],
            "passed": s["guard_state"] == "STOP_WAIT_EXTERNAL_OPUS_REVIEW"
            and s["external_opus_review_pending"]
            and not s["actual_opus_result_present"],
        },
    )
    write_json(
        FIXTURES_DIR / "sandbox-product-grade-but-not-complete.json",
        {
            "case_id": "sandbox-product-grade-but-not-complete",
            "sandbox_closeout_evidence_product_grade": s["sandbox_closeout_evidence_product_grade"],
            "goal_complete_now": s["goal_complete_now"],
            "passed": s["sandbox_closeout_evidence_product_grade"] and not s["goal_complete_now"],
        },
    )
    write_json(
        FIXTURES_DIR / "no-mainline-or-truth-authority.json",
        {
            "case_id": "no-mainline-or-truth-authority",
            "mainline_ready": s["mainline_ready"],
            "reviewed_knowledge_ready": s["reviewed_knowledge_ready"],
            "evidence_support_ready": s["evidence_support_ready"],
            "action_basis_ready": s["action_basis_ready"],
            "passed": not any(
                [
                    s["mainline_ready"],
                    s["reviewed_knowledge_ready"],
                    s["evidence_support_ready"],
                    s["action_basis_ready"],
                ]
            ),
        },
    )
    write_json(
        FIXTURES_DIR / "no-commit-push-sync.json",
        {
            "case_id": "no-commit-push-sync",
            "commit_push_sync_ready": s["commit_push_sync_ready"],
            "may_merge_mainline": s["may_merge_mainline"],
            "may_claim_complete": s["may_claim_complete"],
            "passed": not s["commit_push_sync_ready"] and not s["may_merge_mainline"] and not s["may_claim_complete"],
        },
    )
    write_json(
        FIXTURES_DIR / "sandbox-preparation-may-continue.json",
        {
            "case_id": "sandbox-preparation-may-continue",
            "may_continue_sandbox_preparation": s["may_continue_sandbox_preparation"],
            "result_intake_ready": s["result_intake_ready"],
            "passed": s["may_continue_sandbox_preparation"] and s["result_intake_ready"],
        },
    )


def write_failure_cases() -> None:
    write_json(
        FAILURE_DIR / "external-review-wait-state-guard-failures.json",
        {
            "record_kind": "external_review_wait_state_guard_failure_cases",
            "slice_id": SLICE_ID,
            "failure_cases": [
                {
                    "case_id": "P2-97-FAIL-01-opus-result-present-but-guard-still-waiting",
                    "must_fail_when": "A valid Opus result exists but the guard still says wait without intake.",
                },
                {
                    "case_id": "P2-97-FAIL-02-opus-approval-claimed-without-result",
                    "must_fail_when": "Opus approval is claimed while no valid external result exists.",
                },
                {
                    "case_id": "P2-97-FAIL-03-mainline-ready-claimed",
                    "must_fail_when": "The guard claims mainline readiness.",
                },
                {
                    "case_id": "P2-97-FAIL-04-truth-authority-claimed",
                    "must_fail_when": "The guard claims reviewed knowledge, evidence support, or action basis readiness.",
                },
                {
                    "case_id": "P2-97-FAIL-05-goal-complete-claimed",
                    "must_fail_when": "The guard claims the overall goal is complete.",
                },
                {
                    "case_id": "P2-97-FAIL-06-no-merge-checklist-missing",
                    "must_fail_when": "The no-merge checklist is missing or omits user mainline approval.",
                },
                {
                    "case_id": "P2-97-FAIL-07-next-action-missing",
                    "must_fail_when": "The guard does not point to external Opus review and p2-96 intake.",
                },
                {
                    "case_id": "P2-97-FAIL-08-protected-path-write",
                    "must_fail_when": "This slice writes outside its own sandbox path.",
                },
            ],
        },
    )


def write_outputs() -> dict:
    guard = build_guard()
    write_json(ARTIFACT_DIR / "external-review-wait-state-guard.json", guard)
    write_text(ARTIFACT_DIR / "external-review-wait-state-guard.md", render_guard_md(guard))
    write_text(ARTIFACT_DIR / "no-merge-checklist.md", render_no_merge_checklist(guard))
    write_text(ARTIFACT_DIR / "wait-state-handoff.md", render_wait_handoff(guard))
    write_fixtures(guard)
    write_failure_cases()
    return guard


def main() -> None:
    guard = write_outputs()
    print(json.dumps({"written": True, "summary": guard["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

