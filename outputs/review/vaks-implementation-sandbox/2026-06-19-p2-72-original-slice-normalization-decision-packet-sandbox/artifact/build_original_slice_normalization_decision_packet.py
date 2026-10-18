from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


SLICE_ID = "2026-06-19-p2-72-original-slice-normalization-decision-packet-sandbox"
SOURCE_AUDIT_SLICE_ID = "2026-06-16-p2-71-original-slice-closeout-normalization-audit-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
SOURCE_AUDIT = SANDBOX_ROOT / SOURCE_AUDIT_SLICE_ID / "artifact" / "original_slice_closeout_normalization_audit.json"
ARTIFACT = ROOT / "artifact"

OUTPUT_JSON = ARTIFACT / "original_slice_normalization_decision_packet.json"
OUTPUT_MD = ARTIFACT / "original_slice_normalization_decision_packet.md"
OUTPUT_HTML = ARTIFACT / "original_slice_normalization_decision_packet.html"

CANONICAL_STATUS_BY_REPORT = {
    "verification.md": "local_verification_passed",
    "reviewer-report.md": "review_pass_no_blocker",
    "boundary-audit.md": "pass_boundary",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_next_slice",
}


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def relative(path: Path) -> str:
    return path.relative_to(WORKSPACE).as_posix()


def proposed_changes_for_item(item: dict) -> list[dict]:
    changes = []
    for filename, target_status in CANONICAL_STATUS_BY_REPORT.items():
        old_status = item["statuses"].get(
            {
                "verification.md": "verification",
                "reviewer-report.md": "reviewer",
                "boundary-audit.md": "boundary",
                "product-acceptance-report.md": "product",
                "next-step.md": "next_step",
            }[filename]
        )
        if old_status != target_status:
            changes.append(
                {
                    "slice_id": item["slice_id"],
                    "target_path": f"{item['path']}/{filename}",
                    "field": "frontmatter.status",
                    "current_status": old_status,
                    "proposed_status": target_status,
                    "change_kind": "status_only_frontmatter_normalization",
                    "applied": False,
                    "requires_explicit_user_approval": True,
                }
            )
    return changes


def decision_options() -> list[dict]:
    return [
        {
            "option_id": "approve_status_only_normalization",
            "label": "Approve old-slice status-only normalization",
            "allowed_now": False,
            "requires_separate_user_approval": True,
            "would_edit_old_slices": True,
            "normalization_applied": False,
            "meaning": "Allow a future explicitly approved slice to update only frontmatter status fields in the original 20 sandbox reports.",
        },
        {
            "option_id": "leave_audit_only",
            "label": "Leave as audit-only",
            "allowed_now": True,
            "requires_separate_user_approval": False,
            "would_edit_old_slices": False,
            "normalization_applied": False,
            "meaning": "Keep old slices unchanged and rely on p2-70/p2-71/p2-72 to explain the status vocabulary split.",
        },
        {
            "option_id": "rerun_recloseout_without_old_slice_edits",
            "label": "Rerun closeout in new sandbox evidence",
            "allowed_now": True,
            "requires_separate_user_approval": False,
            "would_edit_old_slices": False,
            "normalization_applied": False,
            "meaning": "Create additional new sandbox evidence instead of editing old slice reports.",
        },
    ]


def build_packet() -> dict:
    audit = read_json(SOURCE_AUDIT)
    items = audit["items"]
    changes = []
    for item in items:
        changes.extend(proposed_changes_for_item(item))
    authority_flags = {
        "decision_packet_only": True,
        "dry_run_only": True,
        "old_slice_write_allowed": False,
        "normalization_applied": False,
        "mainline_ready": False,
        "promotion_ready": False,
        "reviewed_knowledge_ready": False,
        "evidence_support_ready": False,
        "action_basis_ready": False,
        "user_approval_collected": False,
    }
    return {
        "record_kind": "sandbox_original_slice_normalization_decision_packet",
        "slice_id": SLICE_ID,
        "source_audit": {
            "source_audit_slice_id": SOURCE_AUDIT_SLICE_ID,
            "path": relative(SOURCE_AUDIT),
            "summary": audit["summary"],
        },
        "summary": {
            "original_items_covered": len(items),
            "product_acceptance_evidence_count": audit["summary"]["product_acceptance_evidence_count"],
            "core_pass_evidence_count": audit["summary"]["core_reports_have_pass_evidence_count"],
            "current_strict_final_gate_count": audit["summary"]["current_strict_final_gate_count"],
            "status_normalization_candidate_count": audit["summary"]["status_normalization_candidate_count"],
            "dry_run_status_change_count": len(changes),
            "dry_run_only": True,
            "old_slice_writes_applied": 0,
        },
        "decision_options": decision_options(),
        "dry_run_manifest": {
            "manifest_kind": "old_slice_status_normalization_dry_run",
            "applied": False,
            "requires_explicit_user_approval": True,
            "status_changes": changes,
        },
        "authority_flags": authority_flags,
        "forbidden_claims": [
            "this_packet_is_user_approval",
            "old_slices_were_normalized",
            "original_20_current_strict_final_gate_complete",
            "mainline_ready",
            "promotion_ready",
            "reviewed_knowledge_ready",
            "evidence_support_ready",
            "action_basis_ready",
        ],
    }


def render_markdown(payload: dict) -> str:
    summary = payload["summary"]
    lines = [
        "# Original Slice Normalization Decision Packet",
        "",
        "Sandbox-only decision packet. It does not edit old slices.",
        "",
        "## Summary",
        "",
        f"- original items covered: `{summary['original_items_covered']}`",
        f"- product acceptance evidence: `{summary['product_acceptance_evidence_count']}`",
        f"- core pass evidence: `{summary['core_pass_evidence_count']}`",
        f"- current strict final-gate: `{summary['current_strict_final_gate_count']}`",
        f"- status normalization candidates: `{summary['status_normalization_candidate_count']}`",
        f"- dry-run status changes: `{summary['dry_run_status_change_count']}`",
        f"- old slice writes applied: `{summary['old_slice_writes_applied']}`",
        "",
        "## Decision Options",
        "",
        "| Option | Allowed now | Would edit old slices | Requires separate approval |",
        "|---|---:|---:|---:|",
    ]
    for option in payload["decision_options"]:
        lines.append(
            f"| {option['option_id']} | {option['allowed_now']} | {option['would_edit_old_slices']} | {option['requires_separate_user_approval']} |"
        )
    lines.extend(["", "## Boundary", ""])
    lines.append("This packet is not user approval. It is not normalization, mainline readiness, promotion, reviewed knowledge, evidence support, or action basis.")
    return "\n".join(lines) + "\n"


def render_html(payload: dict) -> str:
    rows = "\n".join(
        "<tr>"
        f"<td>{option['option_id']}</td>"
        f"<td>{option['allowed_now']}</td>"
        f"<td>{option['would_edit_old_slices']}</td>"
        f"<td>{option['requires_separate_user_approval']}</td>"
        "</tr>"
        for option in payload["decision_options"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Original Slice Normalization Decision Packet</title>
  <style>
    body {{ font-family: Arial, sans-serif; color: #20242f; background: #f8f8f6; margin: 24px; }}
    main {{ max-width: 1120px; margin: 0 auto; }}
    table {{ border-collapse: collapse; width: 100%; background: #fff; }}
    th, td {{ border: 1px solid #d7d9de; padding: 8px; font-size: 14px; text-align: left; }}
    th {{ background: #eef1f5; }}
  </style>
</head>
<body>
<main>
  <h1>Original Slice Normalization Decision Packet</h1>
  <p>Dry-run only. This packet does not edit old slices or collect user approval.</p>
  <table>
    <thead><tr><th>Option</th><th>Allowed now</th><th>Would edit old slices</th><th>Requires separate approval</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    payload = build_packet()
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(payload), encoding="utf-8")
    OUTPUT_HTML.write_text(render_html(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
