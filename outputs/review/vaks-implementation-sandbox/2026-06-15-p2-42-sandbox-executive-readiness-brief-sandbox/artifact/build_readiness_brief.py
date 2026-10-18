from __future__ import annotations

from pathlib import Path

from readiness_common import (
    APPROVAL_REQUIREMENTS,
    CAPABILITY_DETAILS,
    IMPROVEMENTS,
    IMPROVEMENT_DETAILS,
    LANDED_CAPABILITIES,
    NON_PRODUCTION_GAPS,
    REQUIRED_NON_CLAIMS,
    ROOT,
    SLICE_ID,
    SOURCE_SLICE_ID,
    TRUTH_BOUNDARY,
    default_readiness,
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
    base = default_readiness("executive-readiness")
    write_json(ROOT / "fixtures" / "valid-executive-readiness.json", base)
    operator = default_readiness("operator-readiness")
    operator["operator_note"] = "Operator-facing view with the same readiness boundary."
    write_json(ROOT / "fixtures" / "valid-operator-readiness.json", operator)
    approval = default_readiness("approval-readiness")
    approval["operator_note"] = "Approval-focused view for boundary-crossing decisions."
    write_json(ROOT / "fixtures" / "valid-approval-readiness.json", approval)
    cases = make_failure_cases(base)
    write_json(ROOT / "artifact" / "failure-case-oracle.json", {"slice_id": SLICE_ID, "cases": cases})
    lines = [f"# Failure Case Oracle", "", f"Slice: `{SLICE_ID}`", "", f"Total cases: {len(cases)}", ""]
    for name, expected in cases.items():
        lines.append(f"- `{name}` -> `{', '.join(expected)}`")
    write_text(ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines))


def build_contract() -> None:
    non_claims = "\n".join(f"- {item}" for item in REQUIRED_NON_CLAIMS)
    gaps = "\n".join(f"- `{item}`" for item in NON_PRODUCTION_GAPS)
    approvals = "\n".join(f"- `{item}`" for item in APPROVAL_REQUIREMENTS)
    write_text(
        ROOT / "artifact" / "sandbox-executive-readiness-brief-contract.md",
        f"""
# Sandbox Executive Readiness Brief Contract

Slice: `{SLICE_ID}`

Source slice: `{SOURCE_SLICE_ID}`

Truth boundary: `{TRUTH_BOUNDARY}`.

This sandbox creates a compact executive/operator readiness brief. It can say what landed and what improved inside sandbox, but it cannot approve production, formal vault work, mainline merge, promotion, commit, push, sync, reviewed knowledge, evidence support, or action basis.

## Non-Production Gaps

{gaps}

## Separate Approval Requirements

{approvals}

## Required Non-Claims

{non_claims}
""",
    )


def build_packets() -> None:
    readiness = default_readiness()
    capabilities = "\n".join(
        f"- {CAPABILITY_DETAILS[item]['label']}: {CAPABILITY_DETAILS[item]['summary']}"
        for item in LANDED_CAPABILITIES
    )
    improvements = "\n".join(
        f"- {IMPROVEMENT_DETAILS[item]['label']}: {IMPROVEMENT_DETAILS[item]['summary']}"
        for item in IMPROVEMENTS
    )
    write_text(
        ROOT / "readiness-packets" / "executive-readiness-readout.md",
        f"""
# Executive Readiness Readout

Verdict: `{readiness['executive_verdict']}`

Sandbox slices completed: `{readiness['scorecard']['completed_sandbox_slices']}`

Product-grade sandbox slices: `{readiness['scorecard']['product_grade_sandbox_slices']}`

Verified sandbox slices: `{readiness['scorecard']['verified_sandbox_slices']}`

Revision-history slices: `{readiness['scorecard']['revision_history_slices']}`

Landed capability count: `{len(readiness['landed_capabilities'])}`

Landed capabilities:

{capabilities}

Positive improvement count: `{len(readiness['positive_improvements'])}`

Positive improvements:

{improvements}

Non-production gap count: `{len(readiness['non_production_gaps'])}`

This readout is not enterprise production ready, not formal vault approval, not reviewed knowledge, not evidence support, not action basis, and not mainline readiness.
""",
    )


def build_prototype() -> None:
    readiness = default_readiness()
    prototype = ROOT / "prototype" / "sandbox-executive-readiness-brief"
    capability_rows = "\n".join(
        f"<li data-capability=\"{item}\"><strong>{CAPABILITY_DETAILS[item]['label']}</strong><span>{CAPABILITY_DETAILS[item]['summary']}</span></li>"
        for item in LANDED_CAPABILITIES
    )
    improvement_rows = "\n".join(
        f"<li data-improvement=\"{item}\"><strong>{IMPROVEMENT_DETAILS[item]['label']}</strong><span>{IMPROVEMENT_DETAILS[item]['summary']}</span></li>"
        for item in IMPROVEMENTS
    )
    gap_rows = "\n".join(f"<li data-gap=\"{item}\">{item}</li>" for item in NON_PRODUCTION_GAPS)
    approval_rows = "\n".join(f"<li data-approval=\"{item}\">{item}</li>" for item in APPROVAL_REQUIREMENTS)
    write_text(
        prototype / "index.html",
        f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sandbox Executive Readiness Brief</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fb; color: #17202a; }}
    main {{ max-width: 1040px; margin: 0 auto; padding: 28px 18px 44px; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    .summary {{ color: #465667; max-width: 800px; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin: 20px 0; }}
    .card, .panel {{ background: #ffffff; border: 1px solid #d9e1ec; border-radius: 8px; padding: 14px; }}
    .card span {{ color: #526273; font-size: 13px; }}
    .card strong {{ display: block; margin-top: 8px; font-size: 24px; }}
    .columns {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }}
    li {{ margin: 7px 0; }}
    .notice {{ margin-top: 16px; border-left: 4px solid #2f6fed; background: #edf4ff; padding: 12px 14px; color: #1f3150; }}
  </style>
</head>
<body>
  <main>
    <h1>Sandbox Executive Readiness Brief</h1>
    <p class="summary">{readiness['executive_verdict']} - not enterprise production ready.</p>
    <section class="cards">
      <article class="card"><span>Completed sandbox slices</span><strong>{readiness['scorecard']['completed_sandbox_slices']}</strong></article>
      <article class="card"><span>Product-grade sandbox slices</span><strong>{readiness['scorecard']['product_grade_sandbox_slices']}</strong></article>
      <article class="card"><span>Verified sandbox slices</span><strong>{readiness['scorecard']['verified_sandbox_slices']}</strong></article>
      <article class="card"><span>Revision-history slices</span><strong>{readiness['scorecard']['revision_history_slices']}</strong></article>
      <article class="card"><span>Landed capabilities</span><strong>{len(LANDED_CAPABILITIES)}</strong></article>
    </section>
    <section class="columns">
      <article class="panel"><h2>Landed capabilities</h2><ul>{capability_rows}</ul></article>
      <article class="panel"><h2>Positive improvements</h2><ul>{improvement_rows}</ul></article>
      <article class="panel"><h2>Non-production gaps</h2><ul>{gap_rows}</ul></article>
      <article class="panel"><h2>Separate approvals</h2><ul>{approval_rows}</ul></article>
    </section>
    <section class="notice">not formal vault approval; not action basis; not mainline readiness; not reviewed knowledge; not evidence support.</section>
  </main>
  <script src="app.js"></script>
</body>
</html>
""",
    )
    write_text(prototype / "app.js", 'document.documentElement.dataset.executiveReadinessReady = "true";')
    receipt = default_readiness("prototype-receipt")
    receipt.update(
        {
            "record_kind": "sandbox_executive_readiness_prototype_receipt",
            "formal_vault_accessed": False,
            "sync_performed": False,
            "write_performed": False,
            "commit_performed": False,
            "push_performed": False,
            "promotion_performed": False,
            "mainline_ready": False,
            "enterprise_production_ready": False,
            "action_basis_created": False,
            "reviewed_knowledge_created": False,
            "evidence_support_created": False,
            "auto_advanced": False,
            "non_claims": REQUIRED_NON_CLAIMS,
        }
    )
    write_json(prototype / "receipt.json", receipt)


def build_reports() -> None:
    readiness = default_readiness()
    write_json(ROOT / "artifact" / "executive-readiness-brief.json", readiness)
    write_text(
        ROOT / "slice-plan.md",
        frontmatter("built_pending_review")
        + f"""
# Slice Plan

## Slice

`{SLICE_ID}`

## Objective

Build a compact executive/operator readiness brief from `{SOURCE_SLICE_ID}`.

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
    write_text(
        ROOT / "source-map.md",
        frontmatter("built_pending_review")
        + f"""
# Source Map

Source decision brief:

- `{readiness['source_snapshot']['decision_brief_path']}`
- `{readiness['source_snapshot']['product_report_path']}`

Source facts:

- Product status: `{readiness['source_snapshot']['source_product_status']}`
- Completed sandbox slices: `{readiness['source_snapshot']['completed_sandbox_slices']}`
- Product-grade sandbox slices: `{readiness['source_snapshot']['product_grade_sandbox_slices']}`
- Verified sandbox slices: `{readiness['source_snapshot']['verified_sandbox_slices']}`
- Revision-history slices: `{readiness['source_snapshot']['revision_history_slices']}`

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
python -B .\\outputs\\review\\vaks-implementation-sandbox\\2026-06-15-p2-42-sandbox-executive-readiness-brief-sandbox\\artifact\\verify_readiness_brief.py --rebuild
```

Expected local result:

- Primary `artifact/executive-readiness-brief.json` validates.
- Positive fixtures pass.
- Failure cases match the oracle.
- Prototype exposes readiness, gaps, and approval requirements without command, form, link, or formal-vault affordances.

Final gate command after reviews:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\2026-06-15-p2-42-sandbox-executive-readiness-brief-sandbox\\artifact\\verify_readiness_brief.py --final-gate
```
""",
    )
    write_text(ROOT / "reviewer-report.md", frontmatter("reviewer_pending") + "# Reviewer Report\n\nPending independent read-only review.\n")
    write_text(ROOT / "boundary-audit.md", frontmatter("boundary_pending") + "# Boundary Audit\n\nPending independent boundary audit.\n")
    write_text(ROOT / "product-acceptance-report.md", frontmatter("product_acceptance_pending") + "# Product Acceptance Report\n\nPending GPT-5.5 extra-high Product Acceptance.\n")
    write_text(ROOT / "next-step.md", frontmatter("next_step_pending_product_acceptance") + "# Next Step\n\nDo not advance until Product Acceptance passes this slice.\n")


def build() -> None:
    build_fixtures()
    build_contract()
    build_packets()
    build_prototype()
    build_reports()


if __name__ == "__main__":
    build()
