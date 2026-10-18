from __future__ import annotations

from pathlib import Path

from rollup_common import (
    REQUIRED_NON_CLAIMS,
    ROOT,
    SLICE_ID,
    TRUTH_BOUNDARY,
    default_rollup,
    make_failure_cases,
    reset_generated,
    write_json,
)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def frontmatter(status: str) -> str:
    return f"---\nstatus: {status}\nslice_id: {SLICE_ID}\n---\n"


def build_fixtures() -> None:
    reset_generated()
    base = default_rollup("operator-rollup")
    write_json(ROOT / "fixtures" / "valid-rollup-dashboard.json", base)
    compact = default_rollup("compact-status")
    compact["operator_note"] = "Compact view for answering whether sandbox slices are Product PASS."
    write_json(ROOT / "fixtures" / "valid-compact-status-rollup.json", compact)
    audit = default_rollup("boundary-audit-rollup")
    audit["operator_note"] = "Boundary-focused view for showing what is still not formal authority."
    write_json(ROOT / "fixtures" / "valid-boundary-audit-rollup.json", audit)
    cases = make_failure_cases(base)
    write_json(ROOT / "artifact" / "failure-case-oracle.json", {"slice_id": SLICE_ID, "cases": cases})
    lines = [f"# Failure Case Oracle", "", f"Slice: `{SLICE_ID}`", "", f"Total cases: {len(cases)}", ""]
    for name, expected in cases.items():
        lines.append(f"- `{name}` -> `{', '.join(expected)}`")
    write_text(ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines))


def build_contract() -> None:
    non_claims = "\n".join(f"- {item}" for item in REQUIRED_NON_CLAIMS)
    write_text(
        ROOT / "artifact" / "sandbox-product-grade-rollup-contract.md",
        f"""
# Sandbox Product-Grade Rollup Contract

Slice: `{SLICE_ID}`

Truth boundary: `{TRUTH_BOUNDARY}`.

This sandbox builds a read-only operator rollup over completed sandbox slices. It is status evidence for sandbox review only. It is not formal vault approval, reviewed knowledge, evidence support, action basis, execution permission, mainline readiness, promotion approval, commit approval, push approval, or Obsidian sync approval.

## Inputs

- Read-only report files from earlier directories under `outputs/review/vaks-implementation-sandbox/`.

## Outputs

- `artifact/rollup-data.json`
- `prototype/sandbox-product-grade-rollup-dashboard/`
- `fixtures/`
- `failure-cases/`
- review and acceptance reports

## Required Non-Claims

{non_claims}

## Reuse Rule

Use this rollup only as a sandbox operator surface. Do not move it into `templates/`, `tools/`, formal vault, or main architecture without separate user approval.
""",
    )


def build_packets() -> None:
    rollup = default_rollup()
    write_text(
        ROOT / "rollup-packets" / "operator-readout.md",
        f"""
# Operator Readout

Source slices scanned: `{rollup['source_slice_count']}`

Product PASS slices: `{rollup['product_pass_count']}`

Slices with verification files: `{rollup['verification_present_count']}`

Revision-history slices: `{len(rollup['revision_slices'])}`

This readout is sandbox status evidence only. It is not mainline readiness, formal vault approval, reviewed knowledge, evidence support, or action basis.
""",
    )


def build_prototype() -> None:
    rollup = default_rollup()
    prototype = ROOT / "prototype" / "sandbox-product-grade-rollup-dashboard"
    rows = "\n".join(
        f"<tr data-slice-row=\"{item['slice_id']}\"><td>{item['slice_id']}</td><td>{item['product_status']}</td><td>{item['verification_status']}</td><td>{item['revision_mentions']}</td></tr>"
        for item in rollup["source_slices"]
    )
    write_text(
        prototype / "index.html",
        f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sandbox Product Rollup</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f6f8fb; color: #17202a; }}
    main {{ max-width: 1160px; margin: 0 auto; padding: 28px 18px 44px; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    .summary {{ color: #435263; max-width: 760px; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 20px 0; }}
    .card {{ background: #ffffff; border: 1px solid #d9e1ec; border-radius: 8px; padding: 14px; }}
    .card span {{ color: #526273; font-size: 13px; }}
    .card strong {{ display: block; margin-top: 8px; font-size: 24px; }}
    table {{ width: 100%; border-collapse: collapse; background: #ffffff; border: 1px solid #d9e1ec; }}
    th, td {{ text-align: left; border-bottom: 1px solid #e5ebf2; padding: 9px 10px; font-size: 13px; }}
    th {{ background: #eef3f9; }}
    .notice {{ margin-top: 16px; border-left: 4px solid #2f6fed; background: #edf4ff; padding: 12px 14px; color: #1f3150; }}
  </style>
</head>
<body>
  <main>
    <h1>Sandbox Product-Grade Rollup</h1>
    <p class="summary">Read-only operator view for sandbox PASS status, verification presence, and revision history. This is not formal authority.</p>
    <section class="cards">
      <article class="card" data-rollup-card="source-slices"><span>Source slices</span><strong>{rollup['source_slice_count']}</strong></article>
      <article class="card" data-rollup-card="product-pass"><span>Product PASS</span><strong>{rollup['product_pass_count']}</strong></article>
      <article class="card" data-rollup-card="verification"><span>Verification files</span><strong>{rollup['verification_present_count']}</strong></article>
      <article class="card" data-rollup-card="revisions"><span>Revision history</span><strong>{len(rollup['revision_slices'])}</strong></article>
    </section>
    <table>
      <thead><tr><th>Slice</th><th>Product status</th><th>Verification status</th><th>Revision mentions</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <section class="notice">Sandbox rollup only: not formal vault approval, reviewed knowledge, evidence support, action basis, execution permission, or mainline readiness.</section>
  </main>
  <script src="app.js"></script>
</body>
</html>
""",
    )
    write_text(
        prototype / "app.js",
        """
document.documentElement.dataset.rollupReady = "true";
""",
    )
    receipt = default_rollup("prototype-receipt")
    receipt.update(
        {
            "record_kind": "sandbox_product_grade_rollup_prototype_receipt",
            "formal_vault_accessed": False,
            "sync_performed": False,
            "write_performed": False,
            "commit_performed": False,
            "push_performed": False,
            "promotion_performed": False,
            "mainline_ready": False,
            "action_basis_created": False,
            "reviewed_knowledge_created": False,
            "evidence_support_created": False,
            "auto_advanced": False,
            "non_claims": REQUIRED_NON_CLAIMS,
        }
    )
    write_json(prototype / "receipt.json", receipt)


def build_reports() -> None:
    rollup = default_rollup()
    write_json(ROOT / "artifact" / "rollup-data.json", rollup)
    write_text(
        ROOT / "slice-plan.md",
        frontmatter("built_pending_review")
        + f"""
# Slice Plan

## Slice

`{SLICE_ID}`

## Objective

Build a read-only sandbox product-grade rollup dashboard over previous sandbox slices.

## Only Write Path

`outputs/review/vaks-implementation-sandbox/{SLICE_ID}/`

## Non-Goals

- No formal vault access.
- No Obsidian sync.
- No promotion.
- No commit or push.
- No edits to protected architecture, template, tool, or wiki truth paths.
""",
    )
    source_lines = "\n".join(
        f"- `{item['slice_id']}`: product `{item['product_status']}`, verification `{item['verification_status']}`"
        for item in rollup["source_slices"]
    )
    write_text(
        ROOT / "source-map.md",
        frontmatter("built_pending_review")
        + f"""
# Source Map

Read-only source root: `{rollup['source_root']}`

Source slices scanned:

{source_lines}

These are sandbox status records only. They are not evidence support, reviewed truth, action basis, formal vault approval, or mainline readiness.
""",
    )
    write_text(
        ROOT / "verification.md",
        frontmatter("local_verification_passed_pending_review")
        + """
# Verification

Local verification command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\2026-06-15-p2-40-sandbox-product-grade-rollup-dashboard-sandbox\\artifact\\verify_rollup_dashboard.py --rebuild
```

Expected local result:

- Positive fixtures pass.
- Failure cases match the oracle.
- Source slice PASS and verification-file counts match current file evidence.
- Prototype has no form, download, contenteditable, anchor, or formal-vault path affordance.

Final gate command after reviews:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\2026-06-15-p2-40-sandbox-product-grade-rollup-dashboard-sandbox\\artifact\\verify_rollup_dashboard.py --final-gate
```
""",
    )
    write_text(ROOT / "reviewer-report.md", frontmatter("reviewer_pending") + "# Reviewer Report\n\nPending independent read-only review.\n")
    write_text(ROOT / "boundary-audit.md", frontmatter("boundary_pending") + "# Boundary Audit\n\nPending independent boundary audit.\n")
    write_text(
        ROOT / "product-acceptance-report.md",
        frontmatter("product_acceptance_pending") + "# Product Acceptance Report\n\nPending GPT-5.5 extra-high Product Acceptance.\n",
    )
    write_text(
        ROOT / "next-step.md",
        frontmatter("next_step_pending_product_acceptance") + "# Next Step\n\nDo not advance until Product Acceptance passes this slice.\n",
    )


def build() -> None:
    build_fixtures()
    build_contract()
    build_packets()
    build_prototype()
    build_reports()


if __name__ == "__main__":
    build()
