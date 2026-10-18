from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

AUDIT_PATH = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-16-p2-71-original-slice-closeout-normalization-audit-sandbox/artifact/original_slice_closeout_normalization_audit.json"
DECISION_PACKET_PATH = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-72-original-slice-normalization-decision-packet-sandbox/artifact/original_slice_normalization_decision_packet.json"
CONTRACT_PATH = SLICE_ROOT / "artifact/original_20_current_strict_sidecar_closeout_contract.json"

LEDGER_JSON = SLICE_ROOT / "artifact/original_20_current_strict_sidecar_closeout_ledger.json"
LEDGER_MD = SLICE_ROOT / "artifact/original_20_current_strict_sidecar_closeout_ledger.md"
LEDGER_HTML = SLICE_ROOT / "artifact/original_20_current_strict_sidecar_closeout_ledger.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_item(source_item: dict, required_final_gate_statuses: dict) -> dict:
    evidence_ok = all(
        bool(source_item.get(key))
        for key in [
            "verification_pass_evidence",
            "reviewer_pass_evidence",
            "boundary_pass_evidence",
            "product_acceptance_evidence",
            "core_reports_have_pass_evidence",
        ]
    )
    old_strict = bool(source_item.get("current_strict_final_gate"))
    return {
        "plan_key": source_item["plan_key"],
        "label": source_item["label"],
        "old_slice_id": source_item["slice_id"],
        "old_slice_path": source_item["path"],
        "source_report_statuses": source_item.get("statuses", {}),
        "source_evidence": {
            "verification_pass_evidence": bool(source_item.get("verification_pass_evidence")),
            "reviewer_pass_evidence": bool(source_item.get("reviewer_pass_evidence")),
            "boundary_pass_evidence": bool(source_item.get("boundary_pass_evidence")),
            "product_acceptance_evidence": bool(source_item.get("product_acceptance_evidence")),
            "core_reports_have_pass_evidence": bool(source_item.get("core_reports_have_pass_evidence")),
        },
        "old_slice_current_strict_final_gate": old_strict,
        "sidecar_closeout_passed": evidence_ok and not old_strict,
        "sidecar_closeout_basis": "legacy pass evidence is recorded in p2-71; this sidecar records current-strict evidence without editing old slice files",
        "required_final_gate_statuses_for_future_closeout": required_final_gate_statuses,
        "old_slice_modified": False,
        "old_slice_status_normalized": False,
        "requires_explicit_user_approval_for_old_slice_edit": True,
        "allowed_use": [
            "future recovery",
            "status reporting",
            "operator explanation",
            "input to a separately approved normalization or recloseout slice",
        ],
        "forbidden_use": [
            "claim old slice files are current strict final-gate complete",
            "claim user approved old-slice edits",
            "claim mainline readiness",
            "claim promotion readiness",
            "claim reviewed knowledge",
            "claim evidence support",
            "claim action basis",
        ],
    }


def build_ledger() -> dict:
    audit = load_json(AUDIT_PATH)
    decision_packet = load_json(DECISION_PACKET_PATH)
    contract = load_json(CONTRACT_PATH)
    required_final_gate_statuses = contract["required_final_gate_statuses"]
    source_summary = audit["summary"]
    decision_summary = decision_packet["summary"]
    items = [build_item(item, required_final_gate_statuses) for item in audit["items"]]
    sidecar_passed_count = sum(1 for item in items if item["sidecar_closeout_passed"])
    authority_flags = dict(contract["authority_flags"])
    return {
        "record_kind": "sandbox_original_20_current_strict_sidecar_closeout_ledger",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_71_audit_json": str(AUDIT_PATH.relative_to(WORKSPACE)).replace("\\", "/"),
            "p2_72_decision_packet_json": str(DECISION_PACKET_PATH.relative_to(WORKSPACE)).replace("\\", "/"),
        },
        "summary": {
            "original_items_covered": len(items),
            "source_product_acceptance_evidence_count": source_summary.get("product_acceptance_evidence_count"),
            "source_core_pass_evidence_count": source_summary.get("core_reports_have_pass_evidence_count"),
            "source_old_slice_current_strict_final_gate_count": source_summary.get("current_strict_final_gate_count"),
            "sidecar_closeout_passed_count": sidecar_passed_count,
            "dry_run_status_change_count_from_p2_72": decision_summary.get("dry_run_status_change_count"),
            "old_slice_writes_applied": 0,
            "normalization_applied": False,
            "user_approval_collected": False,
            "claim_old_slices_current_strict_complete": False,
        },
        "authority_flags": authority_flags,
        "required_final_gate_statuses": required_final_gate_statuses,
        "decision_packet_guard": {
            "approve_status_only_normalization_allowed_now": False,
            "status_only_normalization_requires_separate_user_approval": True,
            "rerun_recloseout_without_old_slice_edits_allowed_now": True,
        },
        "items": items,
    }


def render_markdown(ledger: dict) -> str:
    summary = ledger["summary"]
    lines = [
        "# Original 20 Current-Strict Sidecar Closeout Ledger",
        "",
        "Sandbox-only sidecar ledger. It does not edit old slice reports.",
        "",
        "## Summary",
        "",
        f"- original items covered: `{summary['original_items_covered']}`",
        f"- source Product Acceptance evidence: `{summary['source_product_acceptance_evidence_count']}`",
        f"- source core pass evidence: `{summary['source_core_pass_evidence_count']}`",
        f"- old slice current strict final-gate count: `{summary['source_old_slice_current_strict_final_gate_count']}`",
        f"- sidecar closeout passed count: `{summary['sidecar_closeout_passed_count']}`",
        f"- dry-run status changes from p2-72: `{summary['dry_run_status_change_count_from_p2_72']}`",
        f"- old slice writes applied: `{summary['old_slice_writes_applied']}`",
        "",
        "## Authority Boundary",
        "",
        "- This is sidecar evidence only.",
        "- It does not normalize old slice frontmatter.",
        "- It does not claim the old slice files are current strict final-gate complete.",
        "- It does not create mainline readiness, promotion readiness, reviewed knowledge, evidence support, action basis, or user approval.",
        "",
        "## Item Ledger",
        "",
        "| Plan | Slice | Sidecar passed | Old strict final-gate | Old slice modified |",
        "|---|---|---:|---:|---:|",
    ]
    for item in ledger["items"]:
        lines.append(
            "| {plan} | `{sid}` | {passed} | {old_strict} | {modified} |".format(
                plan=item["plan_key"],
                sid=item["old_slice_id"],
                passed=str(item["sidecar_closeout_passed"]),
                old_strict=str(item["old_slice_current_strict_final_gate"]),
                modified=str(item["old_slice_modified"]),
            )
        )
    lines.extend(
        [
            "",
            "## Next Decision",
            "",
            "A future old-slice status-only normalization remains blocked until the user separately and explicitly approves that write scope.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_html(markdown: str) -> str:
    escaped = html.escape(markdown)
    return (
        "<!doctype html>\n"
        "<html><head><meta charset=\"utf-8\"><title>p2-73 Sidecar Closeout Ledger</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1100px;margin:32px auto;line-height:1.5}"
        "pre{white-space:pre-wrap;background:#f6f8fa;padding:16px;border-radius:6px}</style></head>"
        f"<body><pre>{escaped}</pre></body></html>\n"
    )


def main() -> None:
    ledger = build_ledger()
    markdown = render_markdown(ledger)
    LEDGER_JSON.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    LEDGER_MD.write_text(markdown, encoding="utf-8")
    LEDGER_HTML.write_text(render_html(markdown), encoding="utf-8")
    print(json.dumps({"written": [str(LEDGER_JSON), str(LEDGER_MD), str(LEDGER_HTML)]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
