from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

P2_75 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request.json"
P2_76 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-76-old-file-status-normalization-executor-preflight-sandbox/artifact/old_file_status_normalization_executor_preflight.json"
CONTRACT = SLICE_ROOT / "artifact/old_file_status_normalization_executor_readiness_gate_contract.json"

OUT_JSON = SLICE_ROOT / "artifact/old_file_status_normalization_executor_readiness_gate.json"
OUT_MD = SLICE_ROOT / "artifact/old_file_status_normalization_executor_readiness_gate.md"
OUT_HTML = SLICE_ROOT / "artifact/old_file_status_normalization_executor_readiness_gate.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(WORKSPACE)).replace("\\", "/")


def normalized(text: str) -> str:
    return " ".join(text.split())


def phrase_matches(text: str, exact_phrase: str) -> bool:
    return normalized(text) == normalized(exact_phrase)


def decide_readiness(approval_phrase_matched: bool, preflight_clean: bool) -> dict:
    if not approval_phrase_matched:
        readiness = "blocked_no_exact_approval"
        blocked_reason = "Current continuation text is not the exact p2-75 approval phrase."
    elif not preflight_clean:
        readiness = "blocked_preflight_drift"
        blocked_reason = "Exact approval cannot override preflight drift."
    else:
        readiness = "ready_for_executor_prewrite_confirmation"
        blocked_reason = "Future executor must still re-run preflight and stop before write."
    return {
        "readiness": readiness,
        "approval_phrase_matched": approval_phrase_matched,
        "preflight_clean": preflight_clean,
        "executor_write_allowed": False,
        "old_slice_writes_applied": 0,
        "blocked_reason": blocked_reason,
    }


def build_gate() -> dict:
    approval = load_json(P2_75)
    preflight = load_json(P2_76)
    contract = load_json(CONTRACT)
    exact_phrase = approval["request"]["exact_approval_phrase"]
    current_text = contract["current_user_text"]
    current_match = phrase_matches(current_text, exact_phrase)
    preflight_summary = preflight["summary"]
    preflight_clean = (
        preflight_summary["target_change_count"] == 75
        and preflight_summary["missing_target_count"] == 0
        and preflight_summary["current_status_mismatch_count"] == 0
        and preflight_summary["rollback_entry_count"] == 75
        and preflight_summary["old_slice_writes_applied"] == 0
    )
    current_decision = decide_readiness(current_match, preflight_clean)
    future_exact = contract["future_if_exact_approval_present"]
    drift_decision = decide_readiness(True, False)
    return {
        "record_kind": "sandbox_old_file_status_normalization_executor_readiness_gate",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_75_approval_request_json": rel(P2_75),
            "p2_76_executor_preflight_json": rel(P2_76),
        },
        "current_user_text": current_text,
        "exact_approval_phrase_ref": {
            "source": rel(P2_75),
            "exact_phrase_sha256_hint": "not_computed_in_this_slice",
            "phrase_text": exact_phrase,
        },
        "preflight_summary": {
            "target_change_count": preflight_summary["target_change_count"],
            "target_file_count": preflight_summary["target_file_count"],
            "target_old_slice_count": preflight_summary["target_old_slice_count"],
            "preflight_missing_target_count": preflight_summary["missing_target_count"],
            "preflight_status_mismatch_count": preflight_summary["current_status_mismatch_count"],
            "rollback_entry_count": preflight_summary["rollback_entry_count"],
        },
        "current_decision": current_decision,
        "future_exact_approval_scenario": {
            "input_kind": "future_user_message_exact_phrase",
            "approval_phrase_matched": True,
            "readiness": future_exact["readiness"],
            "still_requires_fresh_preflight": future_exact["still_requires_fresh_preflight"],
            "still_requires_boundary_audit": future_exact["still_requires_boundary_audit"],
            "still_requires_stop_before_write": future_exact["still_requires_stop_before_write"],
            "executor_write_allowed_immediately": False,
        },
        "future_exact_approval_preflight_drift_scenario": {
            "input_kind": "future_user_message_exact_phrase_with_drifted_preflight",
            "approval_phrase_matched": drift_decision["approval_phrase_matched"],
            "preflight_clean": drift_decision["preflight_clean"],
            "representative_drift": {
                "missing_target_count": 1,
                "current_status_mismatch_count": 1,
            },
            "readiness": drift_decision["readiness"],
            "executor_write_allowed": drift_decision["executor_write_allowed"],
            "old_slice_writes_applied": drift_decision["old_slice_writes_applied"],
            "blocked_reason": drift_decision["blocked_reason"],
        },
        "generic_language_scenarios": [
            {"input_text": text, "approval_phrase_matched": False, "readiness": "blocked_no_exact_approval"}
            for text in ["继续", "全部落地", "可以", "go ahead", "complete the goal"]
        ],
        "authority_flags": contract["authority_flags"],
    }


def render_markdown(gate: dict) -> str:
    decision = gate["current_decision"]
    summary = gate["preflight_summary"]
    future = gate["future_exact_approval_scenario"]
    drift = gate["future_exact_approval_preflight_drift_scenario"]
    lines = [
        "# Old-File Status Normalization Executor Readiness Gate",
        "",
        "Sandbox-only readiness gate. It does not execute old-file writes.",
        "",
        "## Current Decision",
        "",
        f"- readiness: `{decision['readiness']}`",
        f"- approval phrase matched: `{str(decision['approval_phrase_matched']).lower()}`",
        f"- preflight clean: `{str(decision['preflight_clean']).lower()}`",
        f"- executor write allowed: `{str(decision['executor_write_allowed']).lower()}`",
        f"- old slice writes applied: `{decision['old_slice_writes_applied']}`",
        f"- blocked reason: {decision['blocked_reason']}",
        "",
        "## Preflight Summary",
        "",
        f"- target changes: `{summary['target_change_count']}`",
        f"- target files: `{summary['target_file_count']}`",
        f"- old slices: `{summary['target_old_slice_count']}`",
        f"- missing targets: `{summary['preflight_missing_target_count']}`",
        f"- status mismatches: `{summary['preflight_status_mismatch_count']}`",
        f"- rollback entries: `{summary['rollback_entry_count']}`",
        "",
        "## Future Exact Approval Scenario",
        "",
        f"- readiness after exact phrase: `{future['readiness']}`",
        f"- still requires fresh preflight: `{str(future['still_requires_fresh_preflight']).lower()}`",
        f"- still requires boundary audit: `{str(future['still_requires_boundary_audit']).lower()}`",
        f"- still requires stop before write: `{str(future['still_requires_stop_before_write']).lower()}`",
        f"- executor write allowed immediately: `{str(future['executor_write_allowed_immediately']).lower()}`",
        "",
        "## Future Exact Approval With Preflight Drift",
        "",
        f"- readiness: `{drift['readiness']}`",
        f"- approval phrase matched: `{str(drift['approval_phrase_matched']).lower()}`",
        f"- preflight clean: `{str(drift['preflight_clean']).lower()}`",
        f"- executor write allowed: `{str(drift['executor_write_allowed']).lower()}`",
        f"- old slice writes applied: `{drift['old_slice_writes_applied']}`",
        f"- blocked reason: {drift['blocked_reason']}",
        "",
        "## Generic Language Rejected",
        "",
    ]
    for scenario in gate["generic_language_scenarios"]:
        lines.append(f"- `{scenario['input_text']}` -> `{scenario['readiness']}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Current goal continuation is not approval.",
            "- p2-75 request packet is not approval.",
            "- p2-76 preflight pass is not approval.",
            "- No old slice write, normalization, rollback, mainline merge, promotion, reviewed knowledge, evidence support, or action basis is authorized.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_html(markdown: str) -> str:
    escaped = html.escape(markdown)
    return (
        "<!doctype html>\n"
        "<html><head><meta charset=\"utf-8\"><title>p2-77 Readiness Gate</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1100px;margin:32px auto;line-height:1.5}"
        "pre{white-space:pre-wrap;background:#f6f8fa;padding:16px;border-radius:6px}</style></head>"
        f"<body><pre>{escaped}</pre></body></html>\n"
    )


def main() -> None:
    gate = build_gate()
    markdown = render_markdown(gate)
    OUT_JSON.write_text(json.dumps(gate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown, encoding="utf-8")
    OUT_HTML.write_text(render_html(markdown), encoding="utf-8")
    print(json.dumps({"written": [str(OUT_JSON), str(OUT_MD), str(OUT_HTML)]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
