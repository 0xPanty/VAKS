from __future__ import annotations

from pathlib import Path

from brief_common import (
    DECISION_OPTIONS,
    REQUIRED_NON_CLAIMS,
    ROOT,
    SLICE_ID,
    SOURCE_SLICE_ID,
    TRUTH_BOUNDARY,
    default_brief,
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
    base = default_brief("operator-decision-brief")
    write_json(ROOT / "fixtures" / "valid-decision-brief.json", base)
    compact = default_brief("compact-verdict")
    compact["operator_note"] = "Compact answer to: product-grade sandbox, but not enterprise production or formal authority."
    write_json(ROOT / "fixtures" / "valid-compact-verdict.json", compact)
    approval = default_brief("approval-boundary-view")
    approval["operator_note"] = "Shows which actions require separate user approval."
    write_json(ROOT / "fixtures" / "valid-approval-boundary-view.json", approval)
    cases = make_failure_cases(base)
    write_json(ROOT / "artifact" / "failure-case-oracle.json", {"slice_id": SLICE_ID, "cases": cases})
    lines = [f"# Failure Case Oracle", "", f"Slice: `{SLICE_ID}`", "", f"Total cases: {len(cases)}", ""]
    for name, expected in cases.items():
        lines.append(f"- `{name}` -> `{', '.join(expected)}`")
    write_text(ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines))


def build_contract() -> None:
    non_claims = "\n".join(f"- {item}" for item in REQUIRED_NON_CLAIMS)
    options = "\n".join(f"- `{item['id']}` -> `{item['decision']}`" for item in DECISION_OPTIONS)
    write_text(
        ROOT / "artifact" / "sandbox-operator-decision-brief-contract.md",
        f"""
# Sandbox Operator Decision Brief Contract

Slice: `{SLICE_ID}`

Source slice: `{SOURCE_SLICE_ID}`

Truth boundary: `{TRUTH_BOUNDARY}`.

This sandbox turns the product-grade rollup into a human operator decision brief. It is not formal vault approval, reviewed knowledge, evidence support, action basis, execution permission, mainline readiness, promotion approval, commit approval, push approval, or Obsidian sync approval.

## Decision Options

{options}

## Required Non-Claims

{non_claims}

## Reuse Rule

Use this brief only as a sandbox operator surface. Any promotion, formal vault work, commit, push, sync, or movement into `templates/` or `tools/` needs separate explicit user approval.
""",
    )


def build_packets() -> None:
    brief = default_brief()
    approvals = "\n".join(f"- {item}" for item in brief["required_separate_approvals"])
    write_text(
        ROOT / "brief-packets" / "operator-decision-readout.md",
        f"""
# Operator Decision Readout

Plain verdict: `{brief['plain_verdict']}`

Completed sandbox slices: `{brief['safe_summary']['completed_sandbox_slices']}`

Product-grade sandbox slices: `{brief['safe_summary']['product_grade_sandbox_slices']}`

Verified sandbox slices: `{brief['safe_summary']['verified_sandbox_slices']}`

Revision-history slices: `{brief['safe_summary']['revision_history_slices']}`

Required separate approvals:

{approvals}

This readout is not formal vault approval, reviewed knowledge, evidence support, action basis, execution permission, or mainline readiness.
""",
    )


def build_prototype() -> None:
    brief = default_brief()
    prototype = ROOT / "prototype" / "sandbox-operator-decision-brief"
    option_cards = "\n".join(
        f"<article class=\"option\" data-decision-option=\"{item['id']}\"><strong>{item['id']}</strong><span>{item['decision']}</span><p>{item['reason']}</p></article>"
        for item in brief["decision_options"]
    )
    write_text(
        prototype / "index.html",
        f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sandbox Operator Decision Brief</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fb; color: #17202a; }}
    main {{ max-width: 1040px; margin: 0 auto; padding: 28px 18px 44px; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    .summary {{ color: #465667; max-width: 780px; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 20px 0; }}
    .card, .option {{ background: #ffffff; border: 1px solid #d9e1ec; border-radius: 8px; padding: 14px; }}
    .card span {{ color: #526273; font-size: 13px; }}
    .card strong {{ display: block; margin-top: 8px; font-size: 24px; }}
    .options {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }}
    .option span {{ display: block; color: #226348; margin: 8px 0; }}
    .notice {{ margin-top: 16px; border-left: 4px solid #2f6fed; background: #edf4ff; padding: 12px 14px; color: #1f3150; }}
  </style>
</head>
<body>
  <main>
    <h1>Sandbox Operator Decision Brief</h1>
    <p class="summary">{brief['plain_verdict']}</p>
    <section class="cards">
      <article class="card"><span>Completed sandbox slices</span><strong>{brief['safe_summary']['completed_sandbox_slices']}</strong></article>
      <article class="card"><span>Product-grade sandbox slices</span><strong>{brief['safe_summary']['product_grade_sandbox_slices']}</strong></article>
      <article class="card"><span>Verified sandbox slices</span><strong>{brief['safe_summary']['verified_sandbox_slices']}</strong></article>
      <article class="card"><span>Revision-history slices</span><strong>{brief['safe_summary']['revision_history_slices']}</strong></article>
    </section>
    <section class="options">
      {option_cards}
    </section>
    <section class="notice">not formal vault approval; not action basis; not mainline readiness; not reviewed knowledge; not evidence support.</section>
  </main>
  <script src="app.js"></script>
</body>
</html>
""",
    )
    write_text(prototype / "app.js", 'document.documentElement.dataset.decisionBriefReady = "true";')
    receipt = default_brief("prototype-receipt")
    receipt.update(
        {
            "record_kind": "sandbox_operator_decision_brief_prototype_receipt",
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
    brief = default_brief()
    write_json(ROOT / "artifact" / "decision-brief.json", brief)
    write_text(
        ROOT / "slice-plan.md",
        frontmatter("built_pending_review")
        + f"""
# Slice Plan

## Slice

`{SLICE_ID}`

## Objective

Build a read-only operator decision brief from `{SOURCE_SLICE_ID}`.

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

Source rollup:

- `{brief['source_snapshot']['rollup_data_path']}`
- `{brief['source_snapshot']['product_report_path']}`

Source facts:

- Product status: `{brief['source_snapshot']['source_product_status']}`
- Source slices: `{brief['source_snapshot']['source_slice_count']}`
- Product PASS slices: `{brief['source_snapshot']['product_pass_count']}`
- Verification files: `{brief['source_snapshot']['verification_present_count']}`
- Revision-history slices: `{brief['source_snapshot']['revision_slice_count']}`

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
python -B .\\outputs\\review\\vaks-implementation-sandbox\\2026-06-15-p2-41-sandbox-operator-decision-brief-sandbox\\artifact\\verify_decision_brief.py --rebuild
```

Expected local result:

- Primary `artifact/decision-brief.json` validates.
- Positive fixtures pass.
- Failure cases match the oracle.
- Prototype exposes decision options and non-claims without command, form, link, or formal-vault affordances.

Final gate command after reviews:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\2026-06-15-p2-41-sandbox-operator-decision-brief-sandbox\\artifact\\verify_decision_brief.py --final-gate
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
