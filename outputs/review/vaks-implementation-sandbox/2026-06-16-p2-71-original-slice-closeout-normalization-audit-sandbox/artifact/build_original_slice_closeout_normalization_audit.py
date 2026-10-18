from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


SLICE_ID = "2026-06-16-p2-71-original-slice-closeout-normalization-audit-sandbox"
SOURCE_INDEX_SLICE_ID = "2026-06-16-p2-70-product-grade-coverage-index-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
SOURCE_INDEX = SANDBOX_ROOT / SOURCE_INDEX_SLICE_ID / "artifact" / "product_grade_coverage_index.json"
ARTIFACT = ROOT / "artifact"

OUTPUT_JSON = ARTIFACT / "original_slice_closeout_normalization_audit.json"
OUTPUT_MD = ARTIFACT / "original_slice_closeout_normalization_audit.md"
OUTPUT_HTML = ARTIFACT / "original_slice_closeout_normalization_audit.html"

CANONICAL = {
    "verification": "local_verification_passed",
    "reviewer": "review_pass_no_blocker",
    "boundary": "pass_boundary",
    "product": "pass_product_grade",
    "next_step": "pass_product_grade_pending_next_slice",
}

LEGACY_PASS_PREFIXES = {
    "verification": ["pass", "local_verification_pass", "local_verification_reviewer_boundary_product_acceptance_passed"],
    "reviewer": ["pass", "review_pass", "reviewer_pass", "review_pass_no_blocker"],
    "boundary": ["pass", "boundary_pass", "pass_boundary"],
}


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def relative(path: Path) -> str:
    return path.relative_to(WORKSPACE).as_posix()


def status_values(scanned_item: dict) -> dict:
    statuses = scanned_item.get("statuses", {})
    return {name: statuses.get(name, {}).get("status") for name in CANONICAL}


def classify_statuses(statuses: dict) -> dict:
    core_reports_current_canonical = (
        statuses.get("verification") == CANONICAL["verification"]
        and statuses.get("reviewer") == CANONICAL["reviewer"]
        and statuses.get("boundary") == CANONICAL["boundary"]
    )
    verification_status = statuses.get("verification")
    reviewer_status = statuses.get("reviewer")
    boundary_status = statuses.get("boundary")
    verification_pass_evidence = isinstance(verification_status, str) and any(
        verification_status.startswith(prefix) for prefix in LEGACY_PASS_PREFIXES["verification"]
    )
    reviewer_pass_evidence = isinstance(reviewer_status, str) and any(
        reviewer_status.startswith(prefix) for prefix in LEGACY_PASS_PREFIXES["reviewer"]
    )
    boundary_pass_evidence = isinstance(boundary_status, str) and any(
        boundary_status.startswith(prefix) for prefix in LEGACY_PASS_PREFIXES["boundary"]
    )
    core_reports_have_pass_evidence = verification_pass_evidence and reviewer_pass_evidence and boundary_pass_evidence
    product_status = statuses.get("product")
    product_acceptance_evidence = isinstance(product_status, str) and product_status.startswith("pass_product_grade")
    legacy_product_status = product_acceptance_evidence and product_status != CANONICAL["product"]
    current_strict_final_gate = (
        core_reports_current_canonical
        and product_status == CANONICAL["product"]
        and statuses.get("next_step") == CANONICAL["next_step"]
    )
    next_step_normalization_needed = statuses.get("next_step") != CANONICAL["next_step"]
    blockers = []
    if not core_reports_have_pass_evidence:
        blockers.append("missing_core_report_pass_evidence")
    if not product_acceptance_evidence:
        blockers.append("missing_product_acceptance_evidence")
    if current_strict_final_gate:
        recommendation = "no_normalization_needed"
    elif core_reports_have_pass_evidence and product_acceptance_evidence:
        recommendation = "user_approved_status_normalization_candidate"
    else:
        recommendation = "requires_re_review_or_reacceptance"
    return {
        "core_reports_current_canonical": core_reports_current_canonical,
        "core_reports_have_pass_evidence": core_reports_have_pass_evidence,
        "verification_pass_evidence": verification_pass_evidence,
        "reviewer_pass_evidence": reviewer_pass_evidence,
        "boundary_pass_evidence": boundary_pass_evidence,
        "product_acceptance_evidence": product_acceptance_evidence,
        "legacy_product_status": legacy_product_status,
        "next_step_normalization_needed": next_step_normalization_needed,
        "current_strict_final_gate": current_strict_final_gate,
        "true_blockers": blockers,
        "recommendation": recommendation,
    }


def build_audit() -> dict:
    index = read_json(SOURCE_INDEX)
    scanned_by_id = {item["slice_id"]: item for item in index.get("scanned_slices", [])}
    items = []
    for planned in index.get("planned_items", []):
        slice_id = planned.get("slice_id")
        scanned = scanned_by_id.get(slice_id, {})
        statuses = status_values(scanned)
        classification = classify_statuses(statuses)
        items.append(
            {
                "plan_key": planned.get("plan_key"),
                "label": planned.get("label"),
                "slice_id": slice_id,
                "path": scanned.get("path"),
                "statuses": statuses,
                **classification,
                "old_slice_edit_allowed": False,
                "normalization_applied": False,
                "required_user_decision": (
                    "separate approval required before editing old slice reports"
                    if classification["recommendation"] == "user_approved_status_normalization_candidate"
                    else "none for this audit"
                ),
            }
        )
    counts = {
        "total_original_items": len(items),
        "product_acceptance_evidence_count": sum(1 for item in items if item["product_acceptance_evidence"]),
        "current_strict_final_gate_count": sum(1 for item in items if item["current_strict_final_gate"]),
        "status_normalization_candidate_count": sum(
            1 for item in items if item["recommendation"] == "user_approved_status_normalization_candidate"
        ),
        "requires_re_review_or_reacceptance_count": sum(
            1 for item in items if item["recommendation"] == "requires_re_review_or_reacceptance"
        ),
        "legacy_product_status_count": sum(1 for item in items if item["legacy_product_status"]),
        "next_step_normalization_needed_count": sum(1 for item in items if item["next_step_normalization_needed"]),
        "core_reports_have_pass_evidence_count": sum(1 for item in items if item["core_reports_have_pass_evidence"]),
        "core_reports_current_canonical_count": sum(1 for item in items if item["core_reports_current_canonical"]),
    }
    return {
        "record_kind": "sandbox_original_slice_closeout_normalization_audit",
        "slice_id": SLICE_ID,
        "source_index": {
            "source_index_slice_id": SOURCE_INDEX_SLICE_ID,
            "path": relative(SOURCE_INDEX),
            "source_summary": index.get("summary", {}),
        },
        "rules": {
            "product_evidence_counts_as_current_strict_gate": False,
            "legacy_product_status_counts_as_current_strict_gate": False,
            "pending_next_step_counts_as_current_strict_gate": False,
            "old_slice_edit_requires_separate_user_approval": True,
        },
        "authority_flags": {
            "old_slice_edit_allowed": False,
            "normalization_applied": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "user_approval_collected": False,
        },
        "summary": {
            **counts,
            "all_original_items_found": counts["total_original_items"] == 20,
            "all_original_items_have_product_acceptance_evidence": counts["product_acceptance_evidence_count"] == 20,
            "all_original_items_current_strict_pass": counts["current_strict_final_gate_count"] == 20,
            "audit_only_no_old_slice_writes": True,
        },
        "items": items,
        "next_action_options": [
            {
                "option_id": "audit_only_stop",
                "allowed_now": True,
                "description": "Keep this as a status audit only.",
            },
            {
                "option_id": "future_user_approved_old_slice_status_normalization",
                "allowed_now": False,
                "description": "Would require separate user approval because it edits old slice reports.",
            },
            {
                "option_id": "claim_original_20_current_strict_complete",
                "allowed_now": False,
                "description": "Not supported by current evidence.",
            },
        ],
    }


def render_markdown(payload: dict) -> str:
    summary = payload["summary"]
    lines = [
        "# Original Slice Closeout Normalization Audit",
        "",
        "Sandbox-only audit. No old slice was modified.",
        "",
        "## Summary",
        "",
        f"- original items: `{summary['total_original_items']}`",
        f"- product acceptance evidence: `{summary['product_acceptance_evidence_count']}`",
        f"- core report pass evidence: `{summary['core_reports_have_pass_evidence_count']}`",
        f"- core report current canonical: `{summary['core_reports_current_canonical_count']}`",
        f"- current strict final-gate pass: `{summary['current_strict_final_gate_count']}`",
        f"- status normalization candidates: `{summary['status_normalization_candidate_count']}`",
        f"- requires re-review/reacceptance: `{summary['requires_re_review_or_reacceptance_count']}`",
        f"- legacy product status count: `{summary['legacy_product_status_count']}`",
        f"- next-step normalization needed: `{summary['next_step_normalization_needed_count']}`",
        "",
        "## Items",
        "",
        "| Plan | Slice | Product evidence | Current strict pass | Recommendation |",
        "|---|---|---:|---:|---|",
    ]
    for item in payload["items"]:
        lines.append(
            f"| {item['plan_key']} | {item['slice_id']} | {item['product_acceptance_evidence']} | "
            f"{item['current_strict_final_gate']} | {item['recommendation']} |"
        )
    lines.extend(["", "## Boundary", ""])
    lines.append("This audit is not permission to edit old slices, merge mainline, promote artifacts, create reviewed knowledge, evidence support, action basis, or infer user approval.")
    return "\n".join(lines) + "\n"


def render_html(payload: dict) -> str:
    rows = "\n".join(
        "<tr>"
        f"<td>{item['plan_key']}</td>"
        f"<td>{item['slice_id']}</td>"
        f"<td>{item['product_acceptance_evidence']}</td>"
        f"<td>{item['current_strict_final_gate']}</td>"
        f"<td>{item['recommendation']}</td>"
        "</tr>"
        for item in payload["items"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Original Slice Closeout Normalization Audit</title>
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
  <h1>Original Slice Closeout Normalization Audit</h1>
  <p>Audit-only. No old slice edits, no promotion, no action basis.</p>
  <table>
    <thead><tr><th>Plan</th><th>Slice</th><th>Product evidence</th><th>Strict pass</th><th>Recommendation</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    payload = build_audit()
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(payload), encoding="utf-8")
    OUTPUT_HTML.write_text(render_html(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
