from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

P2_73 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-73-original-20-current-strict-sidecar-closeout-ledger-sandbox/artifact/original_20_current_strict_sidecar_closeout_ledger.json"
P2_75 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request.json"
P2_76 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-76-old-file-status-normalization-executor-preflight-sandbox/artifact/old_file_status_normalization_executor_preflight.json"
P2_77 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-77-old-file-status-normalization-executor-readiness-gate-sandbox/artifact/old_file_status_normalization_executor_readiness_gate.json"

OUT_JSON = SLICE_ROOT / "artifact/goal_completion_gap_ledger.json"
OUT_MD = SLICE_ROOT / "artifact/goal_completion_gap_ledger.md"
OUT_HTML = SLICE_ROOT / "artifact/goal_completion_gap_ledger.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(WORKSPACE)).replace("\\", "/")


def build_ledger() -> dict:
    p2_73 = load_json(P2_73)
    p2_75 = load_json(P2_75)
    p2_76 = load_json(P2_76)
    p2_77 = load_json(P2_77)

    sidecar_summary = p2_73["summary"]
    preflight_summary = p2_76["summary"]
    readiness = p2_77["current_decision"]
    future_exact = p2_77["future_exact_approval_scenario"]

    summary = {
        "original_items": sidecar_summary["original_items_covered"],
        "legacy_product_acceptance_evidence_count": sidecar_summary["source_product_acceptance_evidence_count"],
        "legacy_core_pass_evidence_count": sidecar_summary["source_core_pass_evidence_count"],
        "sidecar_closeout_passed_count": sidecar_summary["sidecar_closeout_passed_count"],
        "old_slice_current_strict_final_gate_count": sidecar_summary["source_old_slice_current_strict_final_gate_count"],
        "pending_status_change_count": p2_75["dry_run_manifest_digest"]["status_change_count"],
        "preflight_missing_target_count": preflight_summary["missing_target_count"],
        "preflight_status_mismatch_count": preflight_summary["current_status_mismatch_count"],
        "preflight_rollback_entry_count": preflight_summary["rollback_entry_count"],
        "old_slice_writes_applied": readiness["old_slice_writes_applied"],
    }

    goal_complete_now = (
        summary["old_slice_current_strict_final_gate_count"] == summary["original_items"]
        and summary["pending_status_change_count"] == 0
        and readiness["executor_write_allowed"] is False
        and summary["old_slice_writes_applied"] == 0
    )

    completion_state = "complete_current_strict" if goal_complete_now else "not_complete_current_strict"
    blockers = {
        "exact_p2_75_approval_required": True,
        "current_text_matches_exact_approval": readiness["approval_phrase_matched"],
        "generic_language_is_not_approval": bool(p2_75["request"]["generic_language_is_not_approval"]),
        "executor_write_allowed": readiness["executor_write_allowed"],
        "future_exact_approval_requires_fresh_preflight": future_exact["still_requires_fresh_preflight"],
        "future_exact_approval_requires_boundary_audit": future_exact["still_requires_boundary_audit"],
        "future_exact_approval_requires_stop_before_write": future_exact["still_requires_stop_before_write"],
    }

    return {
        "record_kind": "sandbox_goal_completion_gap_ledger",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_73_sidecar_closeout_ledger": rel(P2_73),
            "p2_75_approval_request": rel(P2_75),
            "p2_76_executor_preflight": rel(P2_76),
            "p2_77_executor_readiness_gate": rel(P2_77),
        },
        "summary": summary,
        "goal_verdict": {
            "goal_complete_now": goal_complete_now,
            "completion_state": completion_state,
            "claim_all_original_20_current_strict_complete_allowed": False,
            "claim_all_original_20_product_grade_in_legacy_sense_allowed": True,
            "claim_current_strict_ready_to_merge_allowed": False,
            "plain_language": "The original 20 have legacy Product Acceptance/pass evidence and p2-73 sidecar closeout, but the old slice files are not current strict final-gate complete.",
        },
        "completion_ladder": [
            {
                "state": "legacy_product_acceptance_evidence",
                "count": summary["legacy_product_acceptance_evidence_count"],
                "verdict": "present",
                "not_equal_to": "current_strict_old_file_final_gate",
            },
            {
                "state": "sidecar_current_strict_closeout",
                "count": summary["sidecar_closeout_passed_count"],
                "verdict": "present",
                "not_equal_to": "old_file_status_normalization",
            },
            {
                "state": "old_slice_current_strict_final_gate",
                "count": summary["old_slice_current_strict_final_gate_count"],
                "verdict": "not_complete",
                "required_before_all_done_claim": True,
            },
            {
                "state": "old_file_status_normalization_executor",
                "readiness": readiness["readiness"],
                "verdict": "blocked",
                "blocked_reason": readiness["blocked_reason"],
            },
        ],
        "blocking_gates": blockers,
        "safe_next_work": [
            "sandbox_only_gap_ledgers",
            "sandbox_only_operator_surfaces",
            "sandbox_only_product_screens",
            "wait_for_exact_p2_75_approval_phrase",
        ],
        "forbidden_next_work_without_exact_approval": [
            "old_slice_status_normalization_from_generic_continuation",
            "mainline_merge",
            "promotion",
            "templates_tools_edit",
            "obsidian_sync",
        ],
        "forbidden_claims": [
            "all_original_20_current_strict_final_gate_complete",
            "p2_75_request_packet_is_approval",
            "p2_76_clean_preflight_is_approval",
            "p2_77_readiness_gate_executed_normalization",
            "sandbox_gap_ledger_is_reviewed_knowledge",
            "validator_pass_is_product_acceptance",
            "product_acceptance_is_user_approval_for_old_file_write",
        ],
        "authority_flags": {
            "gap_ledger_only": True,
            "old_slice_write_allowed": False,
            "old_slice_writes_applied": summary["old_slice_writes_applied"],
            "normalization_applied": False,
            "approval_collected": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": goal_complete_now,
        },
    }


def render_markdown(ledger: dict) -> str:
    summary = ledger["summary"]
    verdict = ledger["goal_verdict"]
    blockers = ledger["blocking_gates"]
    lines = [
        "# Goal Completion Gap Ledger",
        "",
        "Sandbox-only ledger. It does not normalize old slice files.",
        "",
        "## Verdict",
        "",
        f"- goal_complete_now: `{str(verdict['goal_complete_now']).lower()}`",
        f"- completion_state: `{verdict['completion_state']}`",
        f"- current strict all-done claim allowed: `{str(verdict['claim_all_original_20_current_strict_complete_allowed']).lower()}`",
        f"- legacy product-grade evidence claim allowed: `{str(verdict['claim_all_original_20_product_grade_in_legacy_sense_allowed']).lower()}`",
        f"- current strict ready-to-merge claim allowed: `{str(verdict['claim_current_strict_ready_to_merge_allowed']).lower()}`",
        "",
        verdict["plain_language"],
        "",
        "## Counts",
        "",
        f"- original_items: `{summary['original_items']}`",
        f"- legacy_product_acceptance_evidence_count: `{summary['legacy_product_acceptance_evidence_count']}`",
        f"- legacy_core_pass_evidence_count: `{summary['legacy_core_pass_evidence_count']}`",
        f"- sidecar_closeout_passed_count: `{summary['sidecar_closeout_passed_count']}`",
        f"- old_slice_current_strict_final_gate_count: `{summary['old_slice_current_strict_final_gate_count']}`",
        f"- pending_status_change_count: `{summary['pending_status_change_count']}`",
        f"- preflight_missing_target_count: `{summary['preflight_missing_target_count']}`",
        f"- preflight_status_mismatch_count: `{summary['preflight_status_mismatch_count']}`",
        f"- old_slice_writes_applied: `{summary['old_slice_writes_applied']}`",
        "",
        "## Blocking Gates",
        "",
        f"- exact_p2_75_approval_required: `{str(blockers['exact_p2_75_approval_required']).lower()}`",
        f"- current_text_matches_exact_approval: `{str(blockers['current_text_matches_exact_approval']).lower()}`",
        f"- generic_language_is_not_approval: `{str(blockers['generic_language_is_not_approval']).lower()}`",
        f"- executor_write_allowed: `{str(blockers['executor_write_allowed']).lower()}`",
        f"- future_exact_approval_requires_fresh_preflight: `{str(blockers['future_exact_approval_requires_fresh_preflight']).lower()}`",
        f"- future_exact_approval_requires_boundary_audit: `{str(blockers['future_exact_approval_requires_boundary_audit']).lower()}`",
        f"- future_exact_approval_requires_stop_before_write: `{str(blockers['future_exact_approval_requires_stop_before_write']).lower()}`",
        "",
        "## Safe Next Work",
        "",
    ]
    for item in ledger["safe_next_work"]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Forbidden Claims", ""])
    for item in ledger["forbidden_claims"]:
        lines.append(f"- `{item}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This ledger is not reviewed knowledge.",
            "- This ledger is not evidence support.",
            "- This ledger is not action basis.",
            "- This ledger is not old-file normalization approval.",
            "- This ledger is not a merge or promotion signal.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_html(markdown: str) -> str:
    escaped = html.escape(markdown)
    return (
        "<!doctype html>\n"
        "<html><head><meta charset=\"utf-8\"><title>p2-78 Goal Gap Ledger</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1100px;margin:32px auto;line-height:1.5}"
        "pre{white-space:pre-wrap;background:#f6f8fa;padding:16px;border-radius:6px}</style></head>"
        f"<body><pre>{escaped}</pre></body></html>\n"
    )


def main() -> None:
    ledger = build_ledger()
    markdown = render_markdown(ledger)
    OUT_JSON.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown, encoding="utf-8")
    OUT_HTML.write_text(render_html(markdown), encoding="utf-8")
    print(json.dumps({"written": [str(OUT_JSON), str(OUT_MD), str(OUT_HTML)]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
