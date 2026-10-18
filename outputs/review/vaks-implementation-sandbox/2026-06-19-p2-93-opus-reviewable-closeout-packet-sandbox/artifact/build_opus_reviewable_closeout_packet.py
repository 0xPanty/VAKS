from __future__ import annotations

import html
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-93-opus-reviewable-closeout-packet-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = ROOT / "outputs/review/vaks-implementation-sandbox"
SLICE_DIR = SANDBOX_ROOT / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

P2_80_REPORT = (
    SANDBOX_ROOT
    / "2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json"
)
P2_91_REPORT = (
    SANDBOX_ROOT
    / "2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox/artifact/old_file_status_normalization_executor_apply.json"
)
P2_91_ATTRIBUTION = (
    SANDBOX_ROOT
    / "2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox/artifact/write_attribution_audit.json"
)
P2_92_REPORT = (
    SANDBOX_ROOT
    / "2026-06-19-p2-92-post-apply-current-strict-closeout-audit-sandbox/artifact/post_apply_current_strict_closeout_audit.json"
)
P2_92_SLICE = SANDBOX_ROOT / "2026-06-19-p2-92-post-apply-current-strict-closeout-audit-sandbox"


STRICT_REPORT_STATUSES = {
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


def inventory_sandbox_dirs() -> list[dict]:
    rows = []
    for path in sorted(p for p in SANDBOX_ROOT.iterdir() if p.is_dir()):
        if path.name == SLICE_ID:
            continue
        report_statuses = {
            name: read_status(path / name)
            for name in [
                "verification.md",
                "reviewer-report.md",
                "boundary-audit.md",
                "product-acceptance-report.md",
                "next-step.md",
            ]
        }
        rows.append(
            {
                "slice_id": path.name,
                "path": rel(path),
                "report_statuses": report_statuses,
                "has_product_acceptance": report_statuses["product-acceptance-report.md"] == "pass_product_grade",
                "has_boundary_pass": report_statuses["boundary-audit.md"] == "pass_boundary",
                "has_reviewer_pass": report_statuses["reviewer-report.md"] == "review_pass_no_blocker",
            }
        )
    return rows


def p2_92_final_gate_statuses() -> dict:
    return {name: read_status(P2_92_SLICE / name) for name in STRICT_REPORT_STATUSES}


def build_packet() -> dict:
    p2_80 = load_json(P2_80_REPORT)
    p2_91 = load_json(P2_91_REPORT)
    p2_91_attribution = load_json(P2_91_ATTRIBUTION)
    p2_92 = load_json(P2_92_REPORT)
    sandbox_inventory = inventory_sandbox_dirs()
    p2_92_statuses = p2_92_final_gate_statuses()

    original_item_ids = sorted({item["old_slice_id"] for item in p2_92["operation_results"]})
    operation_status_counts = Counter(item["current_status"] for item in p2_92["operation_results"])
    p2_92_gate_complete = all(p2_92_statuses.get(name) == expected for name, expected in STRICT_REPORT_STATUSES.items())

    summary = {
        "prior_sandbox_slice_count": len(sandbox_inventory),
        "original_item_count": len(original_item_ids),
        "status_operation_count": len(p2_92["operation_results"]),
        "p2_80_transaction_operation_count": p2_80["summary"]["transaction_operation_count"],
        "p2_91_old_slice_writes_applied": p2_91["summary"]["old_slice_writes_applied"],
        "p2_91_protected_path_writes": p2_91["summary"]["protected_path_writes"],
        "p2_92_current_strict_status_operation_count": p2_92["summary"][
            "current_strict_status_operation_count"
        ],
        "p2_92_current_file_hash_match_count": p2_92["summary"]["current_file_hash_match_count"],
        "p2_92_body_unchanged_count": p2_92["summary"]["body_unchanged_count"],
        "p2_92_non_status_frontmatter_unchanged_count": p2_92["summary"][
            "non_status_frontmatter_unchanged_count"
        ],
        "p2_92_current_strict_complete_original_item_count": p2_92["summary"][
            "current_strict_complete_original_item_count"
        ],
        "p2_92_old_slice_writes_applied": p2_92["summary"]["p2_92_old_slice_writes_applied"],
        "p2_92_protected_path_writes": p2_92["summary"]["p2_92_protected_path_writes"],
        "p2_92_final_gate_statuses_complete": p2_92_gate_complete,
        "external_review_packet_ready": False,
        "opus_approval_claimed": False,
        "mainline_ready": False,
        "promotion_ready": False,
        "reviewed_knowledge_ready": False,
        "evidence_support_ready": False,
        "action_basis_ready": False,
        "goal_complete_now": False,
    }
    summary["external_review_packet_ready"] = (
        summary["original_item_count"] == 20
        and summary["status_operation_count"] == 75
        and summary["p2_80_transaction_operation_count"] == 75
        and summary["p2_91_old_slice_writes_applied"] == 75
        and summary["p2_91_protected_path_writes"] == 0
        and summary["p2_92_current_strict_status_operation_count"] == 75
        and summary["p2_92_current_file_hash_match_count"] == 75
        and summary["p2_92_body_unchanged_count"] == 75
        and summary["p2_92_non_status_frontmatter_unchanged_count"] == 75
        and summary["p2_92_current_strict_complete_original_item_count"] == 20
        and summary["p2_92_old_slice_writes_applied"] == 0
        and summary["p2_92_protected_path_writes"] == 0
        and summary["p2_92_final_gate_statuses_complete"]
    )

    return {
        "record_kind": "opus_reviewable_closeout_packet",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_80_transaction_package": rel(P2_80_REPORT),
            "p2_91_executor_apply": rel(P2_91_REPORT),
            "p2_91_write_attribution_audit": rel(P2_91_ATTRIBUTION),
            "p2_92_post_apply_current_strict_audit": rel(P2_92_REPORT),
            "p2_92_slice_reports": rel(P2_92_SLICE),
        },
        "summary": summary,
        "original_item_ids": original_item_ids,
        "operation_status_counts": dict(operation_status_counts),
        "p2_92_final_gate_statuses": p2_92_statuses,
        "p2_91_execution_summary": p2_91["summary"],
        "p2_91_attribution_summary": {
            "audit_scope": p2_91_attribution["audit_scope"],
            "allowed_write_classes": p2_91_attribution["allowed_write_classes"],
            "allowed_target_count": p2_91_attribution["allowed_target_count"],
            "protected_path_status_attribution": p2_91_attribution["protected_path_status_attribution"],
        },
        "p2_92_audit_summary": p2_92["summary"],
        "sandbox_inventory": sandbox_inventory,
        "opus_review_checklist": [
            "Verify p2-91 exact approval scope: old-file frontmatter status-only normalization, 75 targets.",
            "Inspect p2-91 executor report for prewrite hash match, status match, and post-apply status match.",
            "Inspect p2-92 audit report for 75/75 current strict statuses and 20/20 original groups complete.",
            "Confirm body and non-status frontmatter hashes remain unchanged for 75/75 files.",
            "Confirm p2-92 wrote zero old slice files and zero protected paths.",
            "Confirm the packet does not claim mainline merge, reviewed knowledge, evidence support, action basis, or Opus approval.",
            "Decide separately whether the user wants any future mainline integration; no integration is implied here.",
        ],
        "authority_flags": {
            "review_packet_only": True,
            "opus_approval_claimed": False,
            "mainline_merge": False,
            "promotion": False,
            "reviewed_knowledge": False,
            "evidence_support": False,
            "action_basis": False,
            "user_mainline_approval": False,
            "commit_push_sync": False,
        },
    }


def write_fixtures(packet: dict) -> None:
    s = packet["summary"]
    write_json(
        FIXTURES_DIR / "p2-91-status-normalization-applied.json",
        {
            "case_id": "p2-91-status-normalization-applied",
            "p2_91_old_slice_writes_applied": s["p2_91_old_slice_writes_applied"],
            "p2_91_protected_path_writes": s["p2_91_protected_path_writes"],
            "passed": s["p2_91_old_slice_writes_applied"] == 75 and s["p2_91_protected_path_writes"] == 0,
        },
    )
    write_json(
        FIXTURES_DIR / "p2-92-original-20-current-strict-complete.json",
        {
            "case_id": "p2-92-original-20-current-strict-complete",
            "original_item_count": s["original_item_count"],
            "current_strict_complete_original_item_count": s[
                "p2_92_current_strict_complete_original_item_count"
            ],
            "passed": s["original_item_count"] == 20
            and s["p2_92_current_strict_complete_original_item_count"] == 20,
        },
    )
    write_json(
        FIXTURES_DIR / "p2-92-hash-and-body-preservation.json",
        {
            "case_id": "p2-92-hash-and-body-preservation",
            "current_file_hash_match_count": s["p2_92_current_file_hash_match_count"],
            "body_unchanged_count": s["p2_92_body_unchanged_count"],
            "non_status_frontmatter_unchanged_count": s["p2_92_non_status_frontmatter_unchanged_count"],
            "passed": s["p2_92_current_file_hash_match_count"] == 75
            and s["p2_92_body_unchanged_count"] == 75
            and s["p2_92_non_status_frontmatter_unchanged_count"] == 75,
        },
    )
    write_json(
        FIXTURES_DIR / "external-review-boundary-clean.json",
        {
            "case_id": "external-review-boundary-clean",
            "p2_92_old_slice_writes_applied": s["p2_92_old_slice_writes_applied"],
            "p2_92_protected_path_writes": s["p2_92_protected_path_writes"],
            "external_review_packet_ready": s["external_review_packet_ready"],
            "passed": s["p2_92_old_slice_writes_applied"] == 0
            and s["p2_92_protected_path_writes"] == 0
            and s["external_review_packet_ready"],
        },
    )
    write_json(
        FIXTURES_DIR / "opus-pending-not-claimed.json",
        {
            "case_id": "opus-pending-not-claimed",
            "opus_approval_claimed": s["opus_approval_claimed"],
            "mainline_ready": s["mainline_ready"],
            "reviewed_knowledge_ready": s["reviewed_knowledge_ready"],
            "evidence_support_ready": s["evidence_support_ready"],
            "action_basis_ready": s["action_basis_ready"],
            "passed": not any(
                [
                    s["opus_approval_claimed"],
                    s["mainline_ready"],
                    s["reviewed_knowledge_ready"],
                    s["evidence_support_ready"],
                    s["action_basis_ready"],
                ]
            ),
        },
    )


def write_failure_cases() -> None:
    write_json(
        FAILURE_DIR / "opus-reviewable-closeout-packet-failures.json",
        {
            "record_kind": "opus_reviewable_closeout_packet_failure_cases",
            "slice_id": SLICE_ID,
            "failure_cases": [
                {
                    "case_id": "P2-93-FAIL-01-p2-91-normalization-not-applied",
                    "must_fail_when": "p2-91 does not prove 75 approved status-only writes with zero protected path writes.",
                },
                {
                    "case_id": "P2-93-FAIL-02-p2-92-current-strict-not-complete",
                    "must_fail_when": "p2-92 does not prove 75/75 current strict statuses and 20/20 original groups complete.",
                },
                {
                    "case_id": "P2-93-FAIL-03-hash-or-body-preservation-missing",
                    "must_fail_when": "p2-92 does not prove 75/75 current hash match, body preservation, and non-status frontmatter preservation.",
                },
                {
                    "case_id": "P2-93-FAIL-04-p2-92-final-gate-incomplete",
                    "must_fail_when": "p2-92 report statuses do not show local verification, review, boundary, product acceptance, and next-step pass labels.",
                },
                {
                    "case_id": "P2-93-FAIL-05-opus-approval-claimed",
                    "must_fail_when": "The packet claims Opus approval instead of presenting review input for later Opus review.",
                },
                {
                    "case_id": "P2-93-FAIL-06-mainline-or-truth-authority-claimed",
                    "must_fail_when": "The packet claims mainline merge, promotion, reviewed knowledge, evidence support, or action basis.",
                },
                {
                    "case_id": "P2-93-FAIL-07-protected-path-write",
                    "must_fail_when": "This slice writes outside its own sandbox path or reports protected path writes.",
                },
                {
                    "case_id": "P2-93-FAIL-08-checklist-missing-review-actions",
                    "must_fail_when": "The packet lacks a concrete external reviewer checklist.",
                },
            ],
        },
    )


def render_markdown(packet: dict) -> str:
    s = packet["summary"]
    summary_rows = "\n".join(f"| `{k}` | `{v}` |" for k, v in s.items())
    checklist = "\n".join(f"- {item}" for item in packet["opus_review_checklist"])
    original_items = "\n".join(f"- `{item}`" for item in packet["original_item_ids"])
    return f"""# Opus-Reviewable Closeout Packet

## Plain Verdict

The sandbox closeout evidence is ready for external Opus review. This packet does not claim Opus approval, mainline merge, reviewed knowledge, evidence support, or action basis. It is not mainline.

## Summary

| Field | Value |
| --- | --- |
{summary_rows}

## Original 20 Sandbox Slices

{original_items}

## Review Checklist

{checklist}

## Evidence Inputs

```json
{json.dumps(packet["source_inputs"], ensure_ascii=False, indent=2)}
```

## Authority Boundary

This is a review packet only. Any later mainline integration, promotion, reviewed knowledge change, evidence-support use, action-basis use, commit, push, or Obsidian sync still requires separate user approval and separate gates.
"""


def render_checklist(packet: dict) -> str:
    checklist = "\n".join(f"- [ ] {item}" for item in packet["opus_review_checklist"])
    return f"""# Opus Review Checklist

Use this checklist for external review of the VAKS sandbox closeout packet.

{checklist}

## Required External Conclusion

Opus should produce its own explicit conclusion. This packet itself does not contain or imply Opus approval.
"""


def render_html(packet: dict) -> str:
    rows = "\n".join(
        f"<tr><td>{html.escape(key)}</td><td><code>{html.escape(str(value))}</code></td></tr>"
        for key, value in packet["summary"].items()
    )
    checklist = "\n".join(f"<li>{html.escape(item)}</li>" for item in packet["opus_review_checklist"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(SLICE_ID)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; line-height: 1.45; color: #202124; }}
    table {{ border-collapse: collapse; width: 100%; max-width: 1100px; }}
    td, th {{ border: 1px solid #c8cdd3; padding: 6px 8px; text-align: left; }}
    code {{ background: #f1f3f4; padding: 1px 3px; border-radius: 3px; }}
  </style>
</head>
<body>
  <h1>Opus-Reviewable Closeout Packet</h1>
  <p>Ready for external review input. This page does not claim Opus approval or mainline integration; it is not mainline.</p>
  <table>
    <thead><tr><th>Field</th><th>Value</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>
  <h2>Review Checklist</h2>
  <ul>
{checklist}
  </ul>
</body>
</html>
"""


def write_outputs(packet: dict) -> None:
    write_json(ARTIFACT_DIR / "opus_reviewable_closeout_packet.json", packet)
    write_text(ARTIFACT_DIR / "opus_reviewable_closeout_packet.md", render_markdown(packet))
    write_text(ARTIFACT_DIR / "opus-review-checklist.md", render_checklist(packet))
    write_text(ARTIFACT_DIR / "opus_reviewable_closeout_packet.html", render_html(packet))
    write_fixtures(packet)
    write_failure_cases()


def main() -> None:
    packet = build_packet()
    write_outputs(packet)
    print(json.dumps({"written": True, "summary": packet["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
