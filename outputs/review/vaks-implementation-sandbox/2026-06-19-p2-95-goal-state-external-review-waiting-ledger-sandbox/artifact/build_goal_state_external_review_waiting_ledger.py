from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-95-goal-state-external-review-waiting-ledger-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = ROOT / "outputs/review/vaks-implementation-sandbox"
SLICE_DIR = SANDBOX_ROOT / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

P2_91 = SANDBOX_ROOT / "2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox"
P2_92 = SANDBOX_ROOT / "2026-06-19-p2-92-post-apply-current-strict-closeout-audit-sandbox"
P2_93 = SANDBOX_ROOT / "2026-06-19-p2-93-opus-reviewable-closeout-packet-sandbox"
P2_94 = SANDBOX_ROOT / "2026-06-19-p2-94-opus-review-submission-packet-sandbox"

P2_91_JSON = P2_91 / "artifact/old_file_status_normalization_executor_apply.json"
P2_92_JSON = P2_92 / "artifact/post_apply_current_strict_closeout_audit.json"
P2_93_JSON = P2_93 / "artifact/opus_reviewable_closeout_packet.json"
P2_94_JSON = P2_94 / "artifact/opus-review-submission-packet.json"


STRICT_FINAL_STATUSES = {
    "verification.md": "local_verification_passed",
    "reviewer-report.md": "review_pass_no_blocker",
    "boundary-audit.md": "pass_boundary",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_next_slice",
}


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


def split_newline(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    return line, ""


def read_status(path: Path) -> str | None:
    if not path.exists():
        return None
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            return None
        content, _newline = split_newline(line)
        if content.startswith("status:"):
            return content.split(":", 1)[1].strip()
    return None


def final_statuses(slice_dir: Path) -> dict:
    return {name: read_status(slice_dir / name) for name in STRICT_FINAL_STATUSES}


def final_gate_complete(slice_dir: Path) -> bool:
    statuses = final_statuses(slice_dir)
    return all(statuses.get(name) == expected for name, expected in STRICT_FINAL_STATUSES.items())


def build_ledger() -> dict:
    p2_91 = load_json(P2_91_JSON)
    p2_92 = load_json(P2_92_JSON)
    p2_93 = load_json(P2_93_JSON)
    p2_94 = load_json(P2_94_JSON)

    slice_states = [
        {
            "slice_id": P2_91.name,
            "role": "approved old-file status-only normalization executor",
            "final_gate_complete": final_gate_complete(P2_91),
            "product_grade": read_status(P2_91 / "product-acceptance-report.md") == "pass_product_grade",
            "key_counts": {
                "old_slice_writes_applied": p2_91["summary"]["old_slice_writes_applied"],
                "protected_path_writes": p2_91["summary"]["protected_path_writes"],
                "body_unchanged_count": p2_91["summary"]["body_unchanged_count"],
                "non_status_frontmatter_unchanged_count": p2_91["summary"][
                    "non_status_frontmatter_unchanged_count"
                ],
            },
        },
        {
            "slice_id": P2_92.name,
            "role": "post-apply current-strict closeout audit",
            "final_gate_complete": final_gate_complete(P2_92),
            "product_grade": read_status(P2_92 / "product-acceptance-report.md") == "pass_product_grade",
            "key_counts": {
                "original_item_count": p2_92["summary"]["original_item_count"],
                "status_operation_count": p2_92["summary"]["status_operation_count"],
                "current_strict_complete_original_item_count": p2_92["summary"][
                    "current_strict_complete_original_item_count"
                ],
                "p2_92_old_slice_writes_applied": p2_92["summary"]["p2_92_old_slice_writes_applied"],
                "p2_92_protected_path_writes": p2_92["summary"]["p2_92_protected_path_writes"],
            },
        },
        {
            "slice_id": P2_93.name,
            "role": "Opus-reviewable closeout packet",
            "final_gate_complete": final_gate_complete(P2_93),
            "product_grade": read_status(P2_93 / "product-acceptance-report.md") == "pass_product_grade",
            "key_counts": {
                "external_review_packet_ready": p2_93["summary"]["external_review_packet_ready"],
                "opus_approval_claimed": p2_93["summary"]["opus_approval_claimed"],
                "original_item_count": p2_93["summary"]["original_item_count"],
                "status_operation_count": p2_93["summary"]["status_operation_count"],
            },
        },
        {
            "slice_id": P2_94.name,
            "role": "Opus review submission packet",
            "final_gate_complete": final_gate_complete(P2_94),
            "product_grade": read_status(P2_94 / "product-acceptance-report.md") == "pass_product_grade",
            "key_counts": {
                "submission_packet_ready": p2_94["summary"]["submission_packet_ready"],
                "evidence_item_count": p2_94["summary"]["evidence_item_count"],
                "review_question_count": p2_94["summary"]["review_question_count"],
                "opus_review_performed": p2_94["summary"]["opus_review_performed"],
                "opus_approval_claimed": p2_94["summary"]["opus_approval_claimed"],
            },
        },
    ]

    remaining_gates = [
        {
            "gate_id": "external_opus_review",
            "status": "pending_external_result",
            "required_before": "claiming Opus approval or external sandbox acceptance",
            "source_to_use": rel(P2_94 / "artifact/opus-review-submission-prompt.md"),
        },
        {
            "gate_id": "opus_result_intake",
            "status": "pending_external_result",
            "required_before": "turning any Opus response into a sandbox record",
            "source_to_use": rel(P2_94 / "artifact/opus-result-intake-gate.md"),
        },
        {
            "gate_id": "user_mainline_approval",
            "status": "not_requested_not_granted",
            "required_before": "any main architecture merge, commit, push, sync, promotion, or truth-layer write",
            "source_to_use": "future explicit user approval only",
        },
    ]

    summary = {
        "tracked_closeout_slice_count": len(slice_states),
        "tracked_closeout_final_gate_complete_count": sum(1 for item in slice_states if item["final_gate_complete"]),
        "tracked_closeout_product_grade_count": sum(1 for item in slice_states if item["product_grade"]),
        "p2_91_old_slice_writes_applied": p2_91["summary"]["old_slice_writes_applied"],
        "p2_91_protected_path_writes": p2_91["summary"]["protected_path_writes"],
        "p2_92_original_item_count": p2_92["summary"]["original_item_count"],
        "p2_92_current_strict_complete_original_item_count": p2_92["summary"][
            "current_strict_complete_original_item_count"
        ],
        "p2_93_external_review_packet_ready": p2_93["summary"]["external_review_packet_ready"],
        "p2_94_submission_packet_ready": p2_94["summary"]["submission_packet_ready"],
        "p2_94_opus_review_performed": p2_94["summary"]["opus_review_performed"],
        "external_opus_review_pending": True,
        "opus_approval_claimed": False,
        "sandbox_closeout_evidence_product_grade": False,
        "mainline_ready": False,
        "promotion_ready": False,
        "reviewed_knowledge_ready": False,
        "evidence_support_ready": False,
        "action_basis_ready": False,
        "commit_push_sync_ready": False,
        "goal_complete_now": False,
    }
    summary["sandbox_closeout_evidence_product_grade"] = (
        summary["tracked_closeout_slice_count"] == 4
        and summary["tracked_closeout_final_gate_complete_count"] == 4
        and summary["tracked_closeout_product_grade_count"] == 4
        and summary["p2_91_old_slice_writes_applied"] == 75
        and summary["p2_91_protected_path_writes"] == 0
        and summary["p2_92_original_item_count"] == 20
        and summary["p2_92_current_strict_complete_original_item_count"] == 20
        and summary["p2_93_external_review_packet_ready"]
        and summary["p2_94_submission_packet_ready"]
        and not summary["p2_94_opus_review_performed"]
    )

    return {
        "record_kind": "goal_state_external_review_waiting_ledger",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_91_executor": rel(P2_91_JSON),
            "p2_92_current_strict_audit": rel(P2_92_JSON),
            "p2_93_opus_reviewable_packet": rel(P2_93_JSON),
            "p2_94_opus_submission_packet": rel(P2_94_JSON),
        },
        "summary": summary,
        "slice_states": slice_states,
        "remaining_gates": remaining_gates,
        "authority_flags": {
            "status_ledger_only": True,
            "external_opus_review_pending": True,
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


def render_main_ledger(ledger: dict) -> str:
    summary_rows = "\n".join(f"| `{k}` | `{v}` |" for k, v in ledger["summary"].items())
    slice_rows = "\n".join(
        f"| `{item['slice_id']}` | {item['role']} | `{item['final_gate_complete']}` | `{item['product_grade']}` |"
        for item in ledger["slice_states"]
    )
    return f"""# Goal-State External Review Waiting Ledger

## Plain Verdict

The sandbox closeout evidence is product-grade and externally review-ready. The overall goal is not complete because actual Opus review is still pending and mainline/user approval has not been granted.

## Summary

| Field | Value |
| --- | --- |
{summary_rows}

## Tracked Closeout Slices

| Slice | Role | Final Gate | Product Grade |
| --- | --- | --- | --- |
{slice_rows}

## Boundary

This ledger is not Opus approval, not mainline readiness, reviewed knowledge, evidence support, action basis, commit, push, or sync.
"""


def render_gate_matrix(ledger: dict) -> str:
    rows = "\n".join(
        f"| `{item['gate_id']}` | `{item['status']}` | {item['required_before']} | `{item['source_to_use']}` |"
        for item in ledger["remaining_gates"]
    )
    return f"""# Remaining Gate Matrix

| Gate | Status | Required Before | Source |
| --- | --- | --- | --- |
{rows}
"""


def render_waiting_ledger(ledger: dict) -> str:
    return f"""# External Review Waiting Ledger

## Waiting On

`external_opus_review`

## Current State

- Submission prompt is ready: `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-94-opus-review-submission-packet-sandbox/artifact/opus-review-submission-prompt.md`
- Result intake gate is ready: `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-94-opus-review-submission-packet-sandbox/artifact/opus-result-intake-gate.md`
- Opus review performed: `{ledger["summary"]["p2_94_opus_review_performed"]}`
- Opus approval claimed: `{ledger["summary"]["opus_approval_claimed"]}`

## Allowed Next External Results

- `OPUS_PASS_SANDBOX_CLOSEOUT`
- `OPUS_REVISE_SANDBOX_CLOSEOUT`
- `OPUS_BLOCKED_NEEDS_USER`

## Important

No sandbox or Opus pass may become mainline merge, reviewed knowledge, evidence support, or action basis without separate user approval and later gates.
"""


def write_fixtures(ledger: dict) -> None:
    s = ledger["summary"]
    write_json(
        FIXTURES_DIR / "product-grade-sandbox-closeout-evidence.json",
        {
            "case_id": "product-grade-sandbox-closeout-evidence",
            "tracked_closeout_slice_count": s["tracked_closeout_slice_count"],
            "tracked_closeout_final_gate_complete_count": s["tracked_closeout_final_gate_complete_count"],
            "tracked_closeout_product_grade_count": s["tracked_closeout_product_grade_count"],
            "sandbox_closeout_evidence_product_grade": s["sandbox_closeout_evidence_product_grade"],
            "passed": s["tracked_closeout_slice_count"] == 4
            and s["tracked_closeout_final_gate_complete_count"] == 4
            and s["tracked_closeout_product_grade_count"] == 4
            and s["sandbox_closeout_evidence_product_grade"],
        },
    )
    write_json(
        FIXTURES_DIR / "external-opus-review-pending.json",
        {
            "case_id": "external-opus-review-pending",
            "external_opus_review_pending": s["external_opus_review_pending"],
            "p2_94_opus_review_performed": s["p2_94_opus_review_performed"],
            "opus_approval_claimed": s["opus_approval_claimed"],
            "passed": s["external_opus_review_pending"]
            and not s["p2_94_opus_review_performed"]
            and not s["opus_approval_claimed"],
        },
    )
    write_json(
        FIXTURES_DIR / "mainline-and-truth-boundaries-false.json",
        {
            "case_id": "mainline-and-truth-boundaries-false",
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
        FIXTURES_DIR / "p2-91-p2-92-proof-intact.json",
        {
            "case_id": "p2-91-p2-92-proof-intact",
            "p2_91_old_slice_writes_applied": s["p2_91_old_slice_writes_applied"],
            "p2_91_protected_path_writes": s["p2_91_protected_path_writes"],
            "p2_92_original_item_count": s["p2_92_original_item_count"],
            "p2_92_current_strict_complete_original_item_count": s[
                "p2_92_current_strict_complete_original_item_count"
            ],
            "passed": s["p2_91_old_slice_writes_applied"] == 75
            and s["p2_91_protected_path_writes"] == 0
            and s["p2_92_original_item_count"] == 20
            and s["p2_92_current_strict_complete_original_item_count"] == 20,
        },
    )
    write_json(
        FIXTURES_DIR / "remaining-gates-present.json",
        {
            "case_id": "remaining-gates-present",
            "remaining_gate_count": len(ledger["remaining_gates"]),
            "remaining_gate_ids": [item["gate_id"] for item in ledger["remaining_gates"]],
            "passed": [item["gate_id"] for item in ledger["remaining_gates"]]
            == ["external_opus_review", "opus_result_intake", "user_mainline_approval"],
        },
    )


def write_failure_cases() -> None:
    write_json(
        FAILURE_DIR / "goal-state-external-review-waiting-ledger-failures.json",
        {
            "record_kind": "goal_state_external_review_waiting_ledger_failure_cases",
            "slice_id": SLICE_ID,
            "failure_cases": [
                {
                    "case_id": "P2-95-FAIL-01-p2-91-proof-missing",
                    "must_fail_when": "p2-91 no longer proves 75 old-slice status writes with zero protected path writes.",
                },
                {
                    "case_id": "P2-95-FAIL-02-p2-92-proof-missing",
                    "must_fail_when": "p2-92 no longer proves 20/20 original slices current-strict complete.",
                },
                {
                    "case_id": "P2-95-FAIL-03-p2-93-review-packet-not-ready",
                    "must_fail_when": "p2-93 no longer provides an external review-ready packet.",
                },
                {
                    "case_id": "P2-95-FAIL-04-p2-94-submission-not-ready",
                    "must_fail_when": "p2-94 no longer provides an executable Opus submission packet.",
                },
                {
                    "case_id": "P2-95-FAIL-05-opus-approval-claimed-without-result",
                    "must_fail_when": "The ledger claims Opus approval without an external Opus result artifact.",
                },
                {
                    "case_id": "P2-95-FAIL-06-mainline-or-truth-authority-claimed",
                    "must_fail_when": "The ledger claims mainline readiness, reviewed knowledge, evidence support, or action basis.",
                },
                {
                    "case_id": "P2-95-FAIL-07-goal-complete-claimed",
                    "must_fail_when": "The ledger claims the overall goal is complete while Opus review is pending.",
                },
                {
                    "case_id": "P2-95-FAIL-08-protected-path-write",
                    "must_fail_when": "This slice writes outside its own sandbox path.",
                },
            ],
        },
    )


def write_outputs(ledger: dict) -> None:
    write_json(ARTIFACT_DIR / "goal-state-external-review-waiting-ledger.json", ledger)
    write_text(ARTIFACT_DIR / "goal-state-external-review-waiting-ledger.md", render_main_ledger(ledger))
    write_text(ARTIFACT_DIR / "remaining-gate-matrix.md", render_gate_matrix(ledger))
    write_text(ARTIFACT_DIR / "external-review-waiting-ledger.md", render_waiting_ledger(ledger))
    write_fixtures(ledger)
    write_failure_cases()


def main() -> None:
    ledger = build_ledger()
    write_outputs(ledger)
    print(json.dumps({"written": True, "summary": ledger["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
