from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

P2_71 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-16-p2-71-original-slice-closeout-normalization-audit-sandbox/artifact/original_slice_closeout_normalization_audit.json"
P2_72 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-72-original-slice-normalization-decision-packet-sandbox/artifact/original_slice_normalization_decision_packet.json"
P2_73 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-73-original-20-current-strict-sidecar-closeout-ledger-sandbox/artifact/original_20_current_strict_sidecar_closeout_ledger.json"
CONTRACT = SLICE_ROOT / "artifact/original_20_operator_status_surface_contract.json"

OUT_JSON = SLICE_ROOT / "artifact/original_20_operator_status_surface.json"
OUT_MD = SLICE_ROOT / "artifact/original_20_operator_status_surface.md"
OUT_HTML = SLICE_ROOT / "artifact/original_20_operator_status_surface.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(WORKSPACE)).replace("\\", "/")


def build_surface() -> dict:
    audit = load_json(P2_71)
    decision = load_json(P2_72)
    ledger = load_json(P2_73)
    contract = load_json(CONTRACT)
    audit_summary = audit["summary"]
    decision_summary = decision["summary"]
    ledger_summary = ledger["summary"]

    numbers = {
        "original_items": audit_summary["total_original_items"],
        "legacy_product_acceptance_evidence": audit_summary["product_acceptance_evidence_count"],
        "legacy_core_pass_evidence": audit_summary["core_reports_have_pass_evidence_count"],
        "old_file_current_strict_final_gate": audit_summary["current_strict_final_gate_count"],
        "sidecar_closeout_passed": ledger_summary["sidecar_closeout_passed_count"],
        "dry_run_status_changes": decision_summary["dry_run_status_change_count"],
        "old_slice_writes_applied": ledger_summary["old_slice_writes_applied"],
    }

    status_cards = [
        {
            "card_id": "product_grade_sidecar_ready",
            "headline": "Sandbox sidecar is product-grade",
            "plain_language": "p2-73 gives the original 20 items a product-grade sidecar ledger.",
            "count": numbers["sidecar_closeout_passed"],
            "status": "ready_in_sandbox_sidecar",
            "authority_limit": "This is not old-file normalization or mainline readiness.",
        },
        {
            "card_id": "old_files_not_current_strict_complete",
            "headline": "Old slice files are not current strict complete",
            "plain_language": "The old 20 slice files still have 0 of 20 current strict final-gate completion.",
            "count": numbers["old_file_current_strict_final_gate"],
            "status": "not_complete_for_old_files",
            "authority_limit": "Do not claim all old files are strict complete.",
        },
        {
            "card_id": "old_file_normalization_requires_user_approval",
            "headline": "Old-file normalization needs separate approval",
            "plain_language": "The 75 proposed status-only changes remain dry-run and unapplied.",
            "count": numbers["dry_run_status_changes"],
            "status": "blocked_until_explicit_user_approval",
            "authority_limit": "Generic continuation language is not approval.",
        },
        {
            "card_id": "mainline_not_authorized",
            "headline": "Mainline is not authorized",
            "plain_language": "Nothing here merges architecture, promotes knowledge, or creates action basis.",
            "count": 0,
            "status": "not_authorized",
            "authority_limit": "Sandbox pass is not merge, promotion, reviewed knowledge, evidence support, or action basis.",
        },
    ]

    decision_options = [
        {
            "option_id": "continue_with_sidecar_recloseout",
            "allowed_now": True,
            "edits_old_files": False,
            "meaning": "Continue proving strict closeout in new sandbox sidecars without editing old files.",
        },
        {
            "option_id": "request_explicit_old_file_status_normalization_approval",
            "allowed_now": False,
            "edits_old_files": True,
            "meaning": "Ask the user for a separate explicit approval before status-only old-file edits.",
        },
        {
            "option_id": "do_not_claim_all_old_files_strict_complete",
            "allowed_now": True,
            "edits_old_files": False,
            "meaning": "Report old-file current strict final-gate as 0 of 20 until separately normalized or reclosed.",
        },
        {
            "option_id": "do_not_merge_mainline",
            "allowed_now": True,
            "edits_old_files": False,
            "meaning": "Keep all outputs sandbox-only until the user separately approves a mainline path.",
        },
    ]

    return {
        "record_kind": "sandbox_original_20_operator_status_surface",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_71_audit_json": rel(P2_71),
            "p2_72_decision_packet_json": rel(P2_72),
            "p2_73_sidecar_ledger_json": rel(P2_73),
        },
        "numbers": numbers,
        "operator_summary": {
            "one_line": "The original 20 have product-grade sidecar closeout, but the old files themselves are still 0/20 current strict final-gate complete.",
            "product_grade_now": "p2-73 sidecar ledger",
            "not_product_grade_as_old_files": "original 20 old slice files under current strict final-gate",
            "requires_user_decision": "old-file status-only normalization",
        },
        "status_cards": status_cards,
        "decision_options": decision_options,
        "authority_flags": contract["authority_flags"],
    }


def render_markdown(surface: dict) -> str:
    n = surface["numbers"]
    lines = [
        "# Original 20 Operator Status Surface",
        "",
        "Sandbox-only operator surface. It explains status; it does not approve or merge anything.",
        "",
        "## Plain Verdict",
        "",
        surface["operator_summary"]["one_line"],
        "",
        "## Counts",
        "",
        f"- original items: `{n['original_items']}`",
        f"- legacy Product Acceptance evidence: `{n['legacy_product_acceptance_evidence']}`",
        f"- legacy core pass evidence: `{n['legacy_core_pass_evidence']}`",
        f"- product-grade sidecar closeout: `{n['sidecar_closeout_passed']}`",
        f"- old-file current strict final-gate: `{n['old_file_current_strict_final_gate']}`",
        f"- dry-run old-file status changes: `{n['dry_run_status_changes']}`",
        f"- old slice writes applied: `{n['old_slice_writes_applied']}`",
        "",
        "## Status Cards",
        "",
    ]
    for card in surface["status_cards"]:
        lines.extend(
            [
                f"### {card['headline']}",
                "",
                f"- card id: `{card['card_id']}`",
                f"- status: `{card['status']}`",
                f"- plain language: {card['plain_language']}",
                f"- boundary: {card['authority_limit']}",
                "",
            ]
        )
    lines.extend(["## Decision Options", ""])
    for option in surface["decision_options"]:
        lines.append(
            f"- `{option['option_id']}`: allowed_now=`{str(option['allowed_now']).lower()}`, edits_old_files=`{str(option['edits_old_files']).lower()}`. {option['meaning']}"
        )
    lines.extend(
        [
            "",
            "## Do Not Say",
            "",
            "- Do not say all old files are current strict complete.",
            "- Do not say user approved old-file edits.",
            "- Do not say this is mainline-ready, promoted, reviewed knowledge, evidence support, or action basis.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_html(markdown: str) -> str:
    escaped = html.escape(markdown)
    return (
        "<!doctype html>\n"
        "<html><head><meta charset=\"utf-8\"><title>p2-74 Operator Status Surface</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1120px;margin:32px auto;line-height:1.5}"
        "pre{white-space:pre-wrap;background:#f6f8fa;padding:16px;border-radius:6px}</style></head>"
        f"<body><pre>{escaped}</pre></body></html>\n"
    )


def main() -> None:
    surface = build_surface()
    markdown = render_markdown(surface)
    OUT_JSON.write_text(json.dumps(surface, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown, encoding="utf-8")
    OUT_HTML.write_text(render_html(markdown), encoding="utf-8")
    print(json.dumps({"written": [str(OUT_JSON), str(OUT_MD), str(OUT_HTML)]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
