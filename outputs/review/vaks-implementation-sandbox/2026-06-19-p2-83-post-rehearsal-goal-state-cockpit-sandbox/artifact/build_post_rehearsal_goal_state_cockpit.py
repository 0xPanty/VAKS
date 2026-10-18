from __future__ import annotations

import hashlib
import html
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT_DIR = SLICE_ROOT / "artifact"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURE_DIR = SLICE_ROOT / "failure-cases"


SOURCE_PATHS = {
    "p2_74_operator_surface": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-74-original-20-operator-status-surface-sandbox/artifact/original_20_operator_status_surface.json",
    "p2_75_approval_request": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request.json",
    "p2_77_readiness_gate": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-77-old-file-status-normalization-executor-readiness-gate-sandbox/artifact/old_file_status_normalization_executor_readiness_gate.json",
    "p2_78_gap_ledger": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-78-goal-completion-gap-ledger-sandbox/artifact/goal_completion_gap_ledger.json",
    "p2_80_transaction_package": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json",
    "p2_82_copy_rehearsal": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-82-old-file-status-normalization-sandbox-copy-executor-rehearsal-sandbox/artifact/sandbox_copy_executor_rehearsal.json",
    "p2_82_product_acceptance_report": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-82-old-file-status-normalization-sandbox-copy-executor-rehearsal-sandbox/product-acceptance-report.md",
}


def repo_path(rel: str) -> Path:
    return REPO_ROOT / rel


def read_json(rel: str) -> dict:
    return json.loads(repo_path(rel).read_text(encoding="utf-8"))


def frontmatter_status(rel: str) -> str | None:
    text = repo_path(rel).read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    for line in lines[1:]:
        if line == "---":
            break
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return None


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_payload() -> dict:
    p2_74 = read_json(SOURCE_PATHS["p2_74_operator_surface"])
    p2_75 = read_json(SOURCE_PATHS["p2_75_approval_request"])
    p2_77 = read_json(SOURCE_PATHS["p2_77_readiness_gate"])
    p2_78 = read_json(SOURCE_PATHS["p2_78_gap_ledger"])
    p2_80 = read_json(SOURCE_PATHS["p2_80_transaction_package"])
    p2_82 = read_json(SOURCE_PATHS["p2_82_copy_rehearsal"])
    p2_82_pa_status = frontmatter_status(SOURCE_PATHS["p2_82_product_acceptance_report"])

    summary = {
        "original_items": p2_78["summary"]["original_items"],
        "legacy_product_acceptance_evidence_count": p2_78["summary"]["legacy_product_acceptance_evidence_count"],
        "legacy_core_pass_evidence_count": p2_78["summary"]["legacy_core_pass_evidence_count"],
        "sidecar_closeout_passed_count": p2_78["summary"]["sidecar_closeout_passed_count"],
        "old_slice_current_strict_final_gate_count": p2_78["summary"]["old_slice_current_strict_final_gate_count"],
        "pending_status_change_count": p2_78["summary"]["pending_status_change_count"],
        "transaction_operation_count": p2_80["summary"]["transaction_operation_count"],
        "p2_82_fixture_copy_count": p2_82["summary"]["fixture_copy_count"],
        "p2_82_fixture_apply_write_count": p2_82["summary"]["fixture_apply_write_count"],
        "p2_82_fixture_rollback_write_count": p2_82["summary"]["fixture_rollback_write_count"],
        "p2_82_final_copy_byte_hash_restored_count": p2_82["summary"]["final_copy_byte_sha_match_count"],
        "old_slice_writes_applied": p2_82["summary"]["old_slice_writes_applied"],
        "goal_complete_now": p2_78["goal_verdict"]["goal_complete_now"],
        "p2_82_product_acceptance_status": p2_82_pa_status,
    }

    approval_phrase = p2_75["request"]["exact_approval_phrase"]
    cockpit = {
        "record_kind": "sandbox_post_rehearsal_goal_state_cockpit",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": SOURCE_PATHS,
        "source_digest": {
            key: hashlib.sha256(repo_path(rel).read_bytes()).hexdigest()
            for key, rel in SOURCE_PATHS.items()
        },
        "status_summary": summary,
        "plain_answer": {
            "all_done_product_grade": False,
            "short_answer": "No. p2-82 is product-grade, but the whole original-20 old-file closeout is not current strict complete.",
            "what_is_product_grade_now": [
                "p2-82 sandbox-copy executor rehearsal",
                "p2-73 sidecar closeout for the original 20 items",
                "the no-write transaction package and readiness evidence as sandbox artifacts",
            ],
            "what_is_not_done": [
                "the original 20 old slice files are still 0/20 current strict final-gate complete",
                "the 75 old-file status-only changes are still unapplied",
                "the exact p2-75 approval phrase has not been collected",
            ],
        },
        "operator_cards": [
            {
                "card_id": "sandbox_product_grade_evidence",
                "label": "Sandbox proof is strong",
                "state": "product_grade_for_sandbox_artifacts",
                "count": 20,
                "evidence": "p2-73 sidecar closeout and p2-82 byte-safe rehearsal",
                "limit": "Not old-file strict completion and not mainline approval.",
            },
            {
                "card_id": "old_file_strict_completion",
                "label": "Old files are still not strict-complete",
                "state": "not_complete",
                "count": 0,
                "evidence": "p2-78 reports old_slice_current_strict_final_gate_count=0",
                "limit": "Do not claim all original 20 are current strict final-gate complete.",
            },
            {
                "card_id": "normalization_backlog",
                "label": "Normalization backlog is known",
                "state": "blocked_pending_exact_approval",
                "count": 75,
                "evidence": "p2-80 transaction operations and p2-82 sandbox-copy rehearsal",
                "limit": "No old-file writes without exact p2-75 approval and fresh checks.",
            },
            {
                "card_id": "write_authority",
                "label": "Write authority is absent",
                "state": "not_authorized",
                "count": 0,
                "evidence": "p2-75 user_approval_collected=false and p2-77 blocked_no_exact_approval",
                "limit": "Generic continuation language is not approval.",
            },
        ],
        "decision_matrix": {
            "can_continue_sandbox_only": True,
            "can_claim_all_done": False,
            "can_execute_old_file_normalization_now": False,
            "can_merge_mainline_now": False,
            "can_treat_retrieval_as_evidence_support": False,
            "can_treat_product_acceptance_as_user_write_approval": False,
            "requires_exact_p2_75_phrase_for_old_file_write": True,
            "exact_phrase_sha256": sha256_text(approval_phrase),
        },
        "next_action_router": [
            {
                "if_user_says": "generic continuation such as continue or all done",
                "route": "continue sandbox-only productization or report blocked old-file normalization",
                "old_file_write_allowed": False,
            },
            {
                "if_user_says": "the exact p2-75 approval phrase",
                "route": "start a new executor slice with fresh hash preflight and stop-before-write",
                "old_file_write_allowed_immediately": False,
            },
            {
                "if_user_requests": "merge, promotion, Obsidian sync, or mainline edit",
                "route": "stop and ask for separate explicit approval",
                "old_file_write_allowed": False,
            },
        ],
        "product_experience_lift": [
            {
                "dimension": "clarity",
                "improvement": "A future operator can answer whether all work is done without reading 10 prior slices.",
            },
            {
                "dimension": "auditability",
                "improvement": "The cockpit ties every headline number to a source artifact and hash digest.",
            },
            {
                "dimension": "safety",
                "improvement": "The UI and machine contract keep old-file writes blocked until exact approval and fresh checks.",
            },
            {
                "dimension": "maintainability",
                "improvement": "The decision matrix is small enough for later agents to reuse without reinterpreting policy.",
            },
            {
                "dimension": "authority hygiene",
                "improvement": "The cockpit separates product acceptance, sandbox evidence, user approval, reviewed knowledge, and action basis.",
            },
        ],
        "authority_flags": {
            "cockpit_only": True,
            "approval_collected": False,
            "executor_write_allowed": False,
            "old_slice_write_allowed_now": False,
            "old_slice_writes_applied": 0,
            "normalization_applied": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
        },
    }
    return cockpit


def build_markdown(payload: dict) -> str:
    s = payload["status_summary"]
    lines = [
        "---",
        f"slice_id: {SLICE_ID}",
        "status: generated",
        "---",
        "",
        "# Post-Rehearsal Goal State Cockpit",
        "",
        "## Plain Answer",
        "",
        payload["plain_answer"]["short_answer"],
        "",
        "## Key Numbers",
        "",
        f"- original items: {s['original_items']}",
        f"- legacy Product Acceptance evidence: {s['legacy_product_acceptance_evidence_count']}",
        f"- sidecar closeout passed: {s['sidecar_closeout_passed_count']}",
        f"- old-file current strict final-gate complete: {s['old_slice_current_strict_final_gate_count']}",
        f"- pending old-file status changes: {s['pending_status_change_count']}",
        f"- p2-82 byte-safe fixture rollback: {s['p2_82_final_copy_byte_hash_restored_count']}/75",
        f"- old slice writes applied: {s['old_slice_writes_applied']}",
        f"- goal complete now: {str(s['goal_complete_now']).lower()}",
        "",
        "## Operator Cards",
        "",
    ]
    for card in payload["operator_cards"]:
        lines.extend(
            [
                f"### {card['label']}",
                "",
                f"- state: {card['state']}",
                f"- count: {card['count']}",
                f"- evidence: {card['evidence']}",
                f"- limit: {card['limit']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Decision Matrix",
            "",
            f"- can continue sandbox-only: {str(payload['decision_matrix']['can_continue_sandbox_only']).lower()}",
            f"- can claim all done: {str(payload['decision_matrix']['can_claim_all_done']).lower()}",
            f"- can execute old-file normalization now: {str(payload['decision_matrix']['can_execute_old_file_normalization_now']).lower()}",
            f"- can merge mainline now: {str(payload['decision_matrix']['can_merge_mainline_now']).lower()}",
            "",
            "## Authority Boundary",
            "",
            "This cockpit is a sandbox status surface only. It does not authorize old-file writes, reviewed knowledge, evidence support, action basis, promotion, merge, sync, commit, or push.",
            "",
        ]
    )
    return "\n".join(lines)


def build_html(payload: dict) -> str:
    s = payload["status_summary"]
    cards = "\n".join(
        f"""
        <section class="card">
          <p class="label">{html.escape(card['label'])}</p>
          <p class="state">{html.escape(card['state'])}</p>
          <p class="count">{card['count']}</p>
          <p>{html.escape(card['evidence'])}</p>
          <p class="limit">{html.escape(card['limit'])}</p>
        </section>
        """
        for card in payload["operator_cards"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Post-Rehearsal Goal State Cockpit</title>
  <style>
    :root {{ color-scheme: light; font-family: Arial, sans-serif; }}
    body {{ margin: 0; background: #f6f7f9; color: #18202a; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 32px 20px 48px; }}
    h1 {{ font-size: 28px; margin: 0 0 10px; letter-spacing: 0; }}
    .answer {{ font-size: 18px; line-height: 1.45; margin: 0 0 24px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }}
    .metric, .card {{ background: #ffffff; border: 1px solid #d8dee7; border-radius: 8px; padding: 16px; }}
    .metric span {{ display: block; color: #5c6675; font-size: 13px; }}
    .metric strong {{ display: block; margin-top: 6px; font-size: 26px; }}
    .cards {{ margin-top: 22px; }}
    .label {{ margin: 0; color: #526070; font-size: 13px; }}
    .state {{ margin: 8px 0 0; font-weight: 700; }}
    .count {{ margin: 10px 0; font-size: 24px; font-weight: 700; }}
    .limit {{ color: #6e3b24; }}
    .boundary {{ margin-top: 22px; padding: 16px; border-left: 4px solid #a63d40; background: #fff4f2; }}
  </style>
</head>
<body>
  <main>
    <h1>Post-Rehearsal Goal State Cockpit</h1>
    <p class="answer">{html.escape(payload['plain_answer']['short_answer'])}</p>
    <section class="grid">
      <div class="metric"><span>Original items</span><strong>{s['original_items']}</strong></div>
      <div class="metric"><span>Sidecar closeout passed</span><strong>{s['sidecar_closeout_passed_count']}</strong></div>
      <div class="metric"><span>Old-file strict complete</span><strong>{s['old_slice_current_strict_final_gate_count']}/20</strong></div>
      <div class="metric"><span>Pending status changes</span><strong>{s['pending_status_change_count']}</strong></div>
      <div class="metric"><span>p2-82 byte-safe rollback</span><strong>{s['p2_82_final_copy_byte_hash_restored_count']}/75</strong></div>
      <div class="metric"><span>Old slice writes applied</span><strong>{s['old_slice_writes_applied']}</strong></div>
    </section>
    <section class="grid cards">
      {cards}
    </section>
    <section class="boundary">
      This cockpit is sandbox-only. It is not old-file write authority, mainline readiness, reviewed knowledge, evidence support, or action basis.
    </section>
  </main>
</body>
</html>
"""


def build_fixtures(payload: dict) -> None:
    fixtures = {
        "positive-post-rehearsal-state.json": {
            "case_id": "positive-post-rehearsal-state",
            "expected": {
                "original_items": 20,
                "sidecar_closeout_passed_count": 20,
                "old_slice_current_strict_final_gate_count": 0,
                "goal_complete_now": False,
            },
        },
        "positive-user-answer-classification.json": {
            "case_id": "positive-user-answer-classification",
            "inputs": ["continue", "all done", "go ahead", "make it product grade"],
            "expected_old_file_write_allowed": False,
            "expected_route": "continue sandbox-only or report blocked old-file normalization",
        },
        "positive-operator-decision-matrix.json": {
            "case_id": "positive-operator-decision-matrix",
            "expected": payload["decision_matrix"],
        },
        "positive-byte-safety-evidence-rollup.json": {
            "case_id": "positive-byte-safety-evidence-rollup",
            "expected": {
                "fixture_copy_count": 75,
                "fixture_apply_write_count": 75,
                "fixture_rollback_write_count": 75,
                "final_copy_byte_hash_restored_count": 75,
            },
        },
        "positive-authority-boundary-rollup.json": {
            "case_id": "positive-authority-boundary-rollup",
            "expected": {
                "approval_collected": False,
                "executor_write_allowed": False,
                "old_slice_writes_applied": 0,
                "mainline_ready": False,
                "reviewed_knowledge_ready": False,
                "action_basis_ready": False,
            },
        },
    }
    for name, fixture in fixtures.items():
        write_json(FIXTURES_DIR / name, fixture)


def build_failure_cases() -> None:
    cases = {
        "record_kind": "post_rehearsal_goal_state_cockpit_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "case_id": "P2-83-FAIL-01-all-done-overclaim",
                "must_fail_when": "The cockpit claims all original 20 are current strict final-gate complete while old_slice_current_strict_final_gate_count is 0.",
            },
            {
                "case_id": "P2-83-FAIL-02-generic-continuation-as-approval",
                "must_fail_when": "Generic continuation language is treated as exact p2-75 approval.",
            },
            {
                "case_id": "P2-83-FAIL-03-rehearsal-as-write-authority",
                "must_fail_when": "p2-82 sandbox-copy rehearsal is treated as old-file write authority.",
            },
            {
                "case_id": "P2-83-FAIL-04-missing-byte-safety-rollup",
                "must_fail_when": "The cockpit omits p2-82 byte-level final hash restoration evidence.",
            },
            {
                "case_id": "P2-83-FAIL-05-stale-pre-p2-82-status-surface",
                "must_fail_when": "The cockpit only repeats p2-74 and does not incorporate p2-82 rehearsal evidence.",
            },
            {
                "case_id": "P2-83-FAIL-06-mainline-authority-confusion",
                "must_fail_when": "The cockpit creates or implies merge, promotion, reviewed knowledge, evidence support, or action basis authority.",
            },
            {
                "case_id": "P2-83-FAIL-07-product-acceptance-confusion",
                "must_fail_when": "Product Acceptance is treated as user approval for old-file writes.",
            },
            {
                "case_id": "P2-83-FAIL-08-path-boundary-violation",
                "must_fail_when": "The slice writes outside its own sandbox root.",
            },
        ],
    }
    write_json(FAILURE_DIR / "post-rehearsal-goal-state-cockpit-failures.json", cases)


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    write_json(ARTIFACT_DIR / "post_rehearsal_goal_state_cockpit.json", payload)
    (ARTIFACT_DIR / "post_rehearsal_goal_state_cockpit.md").write_text(build_markdown(payload), encoding="utf-8")
    (ARTIFACT_DIR / "post_rehearsal_goal_state_cockpit.html").write_text(build_html(payload), encoding="utf-8")
    build_fixtures(payload)
    build_failure_cases()
    print(json.dumps({"built": True, "slice_id": SLICE_ID}, indent=2))


if __name__ == "__main__":
    main()
