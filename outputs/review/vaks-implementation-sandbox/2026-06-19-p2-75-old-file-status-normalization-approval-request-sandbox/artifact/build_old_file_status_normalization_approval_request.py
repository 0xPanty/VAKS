from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

P2_72 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-72-original-slice-normalization-decision-packet-sandbox/artifact/original_slice_normalization_decision_packet.json"
P2_73 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-73-original-20-current-strict-sidecar-closeout-ledger-sandbox/artifact/original_20_current_strict_sidecar_closeout_ledger.json"
P2_74 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-74-original-20-operator-status-surface-sandbox/artifact/original_20_operator_status_surface.json"
CONTRACT = SLICE_ROOT / "artifact/old_file_status_normalization_approval_request_contract.json"

OUT_JSON = SLICE_ROOT / "artifact/old_file_status_normalization_approval_request.json"
OUT_MD = SLICE_ROOT / "artifact/old_file_status_normalization_approval_request.md"
OUT_HTML = SLICE_ROOT / "artifact/old_file_status_normalization_approval_request.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(WORKSPACE)).replace("\\", "/")


def approval_classifier(text: str, exact_phrase: str) -> dict:
    normalized = " ".join(text.split())
    exact_normalized = " ".join(exact_phrase.split())
    return {
        "input_text": text,
        "is_exact_required_phrase": normalized == exact_normalized,
        "would_count_as_explicit_approval_in_future": normalized == exact_normalized,
        "current_packet_collects_approval": False,
    }


def build_request() -> dict:
    decision = load_json(P2_72)
    sidecar = load_json(P2_73)
    status_surface = load_json(P2_74)
    contract = load_json(CONTRACT)
    dry_run_changes = decision["dry_run_manifest"]["status_changes"]
    exact_phrase = contract["exact_approval_phrase"]
    non_approval_examples = contract["non_approval_examples"]
    return {
        "record_kind": "sandbox_old_file_status_normalization_approval_request",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_72_decision_packet_json": rel(P2_72),
            "p2_73_sidecar_ledger_json": rel(P2_73),
            "p2_74_operator_status_surface_json": rel(P2_74),
        },
        "current_state": {
            "original_items": status_surface["numbers"]["original_items"],
            "status_changes": len(dry_run_changes),
            "old_file_current_strict_final_gate": status_surface["numbers"]["old_file_current_strict_final_gate"],
            "sidecar_closeout_passed": sidecar["summary"]["sidecar_closeout_passed_count"],
            "old_slice_writes_applied": 0,
            "normalization_applied": False,
            "user_approval_collected": False,
        },
        "request": {
            "question": "Do you explicitly approve old-file status-only normalization for the original 20 sandbox slice reports?",
            "exact_approval_phrase": exact_phrase,
            "approval_status_now": "not_collected",
            "generic_language_is_not_approval": True,
            "non_approval_examples": non_approval_examples,
        },
        "future_if_approved_scope": contract["future_if_approved_scope"],
        "dry_run_manifest_digest": {
            "source": rel(P2_72),
            "status_change_count": len(dry_run_changes),
            "all_changes_unapplied": all(change.get("applied") is False for change in dry_run_changes),
            "all_changes_require_explicit_user_approval": all(change.get("requires_explicit_user_approval") is True for change in dry_run_changes),
            "target_paths_sample": [change["target_path"] for change in dry_run_changes[:5]],
        },
        "approval_classifier_examples": [
            approval_classifier(exact_phrase, exact_phrase),
            *[approval_classifier(example, exact_phrase) for example in non_approval_examples],
        ],
        "authority_flags": contract["authority_flags"],
    }


def render_markdown(packet: dict) -> str:
    state = packet["current_state"]
    request = packet["request"]
    scope = packet["future_if_approved_scope"]
    lines = [
        "# Old-File Status Normalization Approval Request",
        "",
        "Sandbox-only request packet. It asks for a future decision; it is not approval.",
        "",
        "## Current State",
        "",
        f"- original items: `{state['original_items']}`",
        f"- p2-72 dry-run status changes: `{state['status_changes']}`",
        f"- old-file current strict final-gate: `{state['old_file_current_strict_final_gate']}`",
        f"- p2-73 sidecar closeout passed: `{state['sidecar_closeout_passed']}`",
        f"- old slice writes applied now: `{state['old_slice_writes_applied']}`",
        f"- user approval collected now: `{str(state['user_approval_collected']).lower()}`",
        "",
        "## Exact Approval Phrase",
        "",
        "Only this exact phrase would count as explicit approval in a future turn:",
        "",
        "```text",
        request["exact_approval_phrase"],
        "```",
        "",
        "## Generic Language That Is Not Approval",
        "",
    ]
    for example in request["non_approval_examples"]:
        lines.append(f"- `{example}`")
    lines.extend(
        [
            "",
            "## Future Scope If Approved",
            "",
            f"- allowed edit kind: `{scope['allowed_edit_kind']}`",
            f"- allowed field: `{scope['allowed_field']}`",
            f"- expected change count: `{scope['expected_change_count']}`",
            f"- body content edits allowed: `{str(scope['body_content_edits_allowed']).lower()}`",
            f"- artifact edits allowed: `{str(scope['artifact_edits_allowed']).lower()}`",
            f"- mainline edits allowed: `{str(scope['mainline_edits_allowed']).lower()}`",
            f"- templates/tools edits allowed: `{str(scope['templates_tools_edits_allowed']).lower()}`",
            f"- wiki truth-layer edits allowed: `{str(scope['wiki_truth_layer_edits_allowed']).lower()}`",
            f"- Obsidian sync allowed: `{str(scope['obsidian_sync_allowed']).lower()}`",
            f"- commit/push allowed: `{str(scope['commit_push_allowed']).lower()}`",
            "",
            "## Current Boundary",
            "",
            "- This request packet does not collect approval.",
            "- It does not allow old slice writes now.",
            "- It does not apply normalization.",
            "- It does not create mainline readiness, promotion, reviewed knowledge, evidence support, or action basis.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_html(markdown: str) -> str:
    escaped = html.escape(markdown)
    return (
        "<!doctype html>\n"
        "<html><head><meta charset=\"utf-8\"><title>p2-75 Approval Request</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1120px;margin:32px auto;line-height:1.5}"
        "pre{white-space:pre-wrap;background:#f6f8fa;padding:16px;border-radius:6px}</style></head>"
        f"<body><pre>{escaped}</pre></body></html>\n"
    )


def main() -> None:
    packet = build_request()
    markdown = render_markdown(packet)
    OUT_JSON.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown, encoding="utf-8")
    OUT_HTML.write_text(render_html(markdown), encoding="utf-8")
    print(json.dumps({"written": [str(OUT_JSON), str(OUT_MD), str(OUT_HTML)]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
