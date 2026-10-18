from __future__ import annotations

from pathlib import Path

from evidence_common import (
    IMPROVEMENTS,
    PLAN_ITEMS,
    REQUIRED_NON_CLAIMS,
    ROOT,
    SLICE_ID,
    TRUTH_BOUNDARY,
    default_ledger,
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
    base = default_ledger("full-evidence-ledger")
    write_json(ROOT / "fixtures" / "valid-evidence-ledger.json", base)
    plain = default_ledger("plain-answer-view")
    plain["operator_note"] = "Plain answer view for whether the sandbox work landed, was tested, improved the system, and remains non-production."
    write_json(ROOT / "fixtures" / "valid-plain-answer-view.json", plain)
    boundary = default_ledger("boundary-non-production-view")
    boundary["operator_note"] = "Boundary view emphasizing that sandbox product grade is not enterprise production or mainline authority."
    write_json(ROOT / "fixtures" / "valid-boundary-non-production-view.json", boundary)
    cases = make_failure_cases(base)
    write_json(ROOT / "artifact" / "failure-case-oracle.json", {"slice_id": SLICE_ID, "cases": cases})
    lines = ["# Failure Case Oracle", "", f"Slice: `{SLICE_ID}`", "", f"Total cases: {len(cases)}", ""]
    for name, expected in cases.items():
        lines.append(f"- `{name}` -> `{', '.join(expected)}`")
    write_text(ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines))


def build_contract() -> None:
    non_claims = "\n".join(f"- {item}" for item in REQUIRED_NON_CLAIMS)
    write_text(
        ROOT / "artifact" / "sandbox-evidence-ledger-contract.md",
        f"""
# Sandbox Evidence Ledger Contract

Slice: `{SLICE_ID}`

Truth boundary: `{TRUTH_BOUNDARY}`.

This ledger answers four operator questions using current sandbox file evidence:

- Did the original P0/P1/P1.5/P2 plan items land in sandbox?
- Do the current sandbox slices have verification and Product Acceptance evidence?
- Are the changes positive improvements inside sandbox?
- Is this enterprise production ready?

The answer is intentionally split: sandbox product-grade evidence can be positive while enterprise production, mainline, formal vault, reviewed knowledge, evidence support, and action-basis authority remain false.

## Required Non-Claims

{non_claims}
""",
    )


def build_packets() -> None:
    ledger = default_ledger()
    improvements = "\n".join(
        f"- {item['label']}: {item['summary']}" for item in ledger["positive_improvements"]
    )
    write_text(
        ROOT / "ledger-packets" / "plain-answer.md",
        f"""
# Plain Answer

all original plan items landed in sandbox: `{ledger['plain_answer']['all_original_plan_items_landed_in_sandbox']}`

all current sandbox slices have verification: `{ledger['plain_answer']['all_current_sandbox_slices_have_verification']}`

all current sandbox slices have Product PASS: `{ledger['plain_answer']['all_current_sandbox_slices_product_pass']}`

positive improvement is supported: `{ledger['plain_answer']['positive_improvement_supported']}`

enterprise product experience: `{ledger['plain_answer']['enterprise_product_experience']}`

This means sandbox product-grade operator experience, not enterprise production, not mainline ready, not formal vault approval, not reviewed knowledge, not evidence support, and not action basis.

## Positive Improvements

{improvements}
""",
    )


def build_prototype() -> None:
    ledger = default_ledger()
    prototype = ROOT / "prototype" / "sandbox-evidence-ledger"
    plan_rows = "\n".join(
        f"<tr data-plan-item=\"{item['item_id']}\"><td>{item['item_id']}</td><td>{item['phase']}</td><td>{item['label']}</td><td>{item['product_pass']}</td><td>{item['verification_present']}</td></tr>"
        for item in ledger["original_plan_coverage"]
    )
    source_rows = "\n".join(
        f"<tr data-source-slice=\"{item['slice_id']}\"><td>{item['slice_id']}</td><td>{item['product_pass']}</td><td>{item['verification_present']}</td><td>{item['reviewer_pass']}</td><td>{item['boundary_pass']}</td></tr>"
        for item in ledger["source_slices"]
    )
    improvements = "\n".join(
        f"<article class=\"card\" data-improvement=\"{item['id']}\"><strong>{item['label']}</strong><span>{item['summary']}</span></article>"
        for item in ledger["positive_improvements"]
    )
    write_text(
        prototype / "index.html",
        f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sandbox Evidence Ledger</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fb; color: #17202a; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 28px 18px 44px; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    .summary {{ color: #455565; max-width: 840px; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; margin: 20px 0; }}
    .card {{ background: #ffffff; border: 1px solid #d9e1ec; border-radius: 8px; padding: 14px; }}
    .card span {{ display: block; margin-top: 8px; color: #526273; font-size: 13px; }}
    .card strong {{ display: block; font-size: 18px; }}
    .metric strong {{ margin-top: 8px; font-size: 24px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 14px; background: #ffffff; border: 1px solid #d9e1ec; }}
    th, td {{ text-align: left; border-bottom: 1px solid #e5ebf2; padding: 8px 10px; font-size: 13px; }}
    th {{ background: #eef3f9; }}
    .notice {{ margin-top: 16px; border-left: 4px solid #2f6fed; background: #edf4ff; padding: 12px 14px; color: #1f3150; }}
  </style>
</head>
<body>
  <main>
    <h1>Sandbox Evidence Ledger</h1>
    <p class="summary">Evidence view for whether the sandbox work landed, was tested, improved the system, and remains non-production.</p>
    <section class="cards">
      <article class="card metric"><span>Source slices</span><strong>{ledger['source_slice_count']}</strong></article>
      <article class="card metric"><span>Product PASS</span><strong>{ledger['product_pass_count']}</strong></article>
      <article class="card metric"><span>Verification</span><strong>{ledger['verification_present_count']}</strong></article>
      <article class="card metric"><span>Original plan PASS</span><strong>{ledger['original_plan_product_pass_count']}</strong></article>
    </section>
    <section class="cards">{improvements}</section>
    <h2>Original Plan Coverage</h2>
    <table><thead><tr><th>ID</th><th>Phase</th><th>Slice</th><th>Product PASS</th><th>Verification</th></tr></thead><tbody>{plan_rows}</tbody></table>
    <h2>Current Sandbox Slices</h2>
    <table><thead><tr><th>Slice</th><th>Product PASS</th><th>Verification</th><th>Reviewer</th><th>Boundary</th></tr></thead><tbody>{source_rows}</tbody></table>
    <section class="notice">Sandbox product-grade operator experience only: not enterprise production, not mainline ready, not action basis.</section>
  </main>
  <script src="app.js"></script>
</body>
</html>
""",
    )
    write_text(prototype / "app.js", 'document.documentElement.dataset.evidenceLedgerReady = "true";')
    receipt = {
        "record_kind": "sandbox_evidence_ledger_prototype_receipt",
        "slice_id": SLICE_ID,
        "source_slice_count": ledger["source_slice_count"],
        "enterprise_production_ready": False,
        "mainline_ready": False,
        "formal_vault_accessed": False,
        "sync_performed": False,
        "commit_performed": False,
        "push_performed": False,
        "promotion_performed": False,
        "action_basis_created": False,
        "reviewed_knowledge_created": False,
        "evidence_support_created": False,
        "auto_advanced": False,
        "required_non_claims": REQUIRED_NON_CLAIMS,
    }
    write_json(prototype / "receipt.json", receipt)


def build_reports() -> None:
    ledger = default_ledger()
    write_json(ROOT / "artifact" / "evidence-ledger.json", ledger)
    write_text(
        ROOT / "slice-plan.md",
        frontmatter("built_pending_review")
        + f"""
# Slice Plan

## Slice

`{SLICE_ID}`

## Objective

Create a read-only evidence ledger that answers whether the sandbox implementation plan landed, was tested, produced positive improvements, and remains non-production.

## Only Write Path

`outputs/review/vaks-implementation-sandbox/{SLICE_ID}/`

## Non-Goals

- No promotion.
- No formal vault access.
- No Obsidian sync.
- No commit or push.
- No edits to protected architecture, template, tool, or wiki truth paths.
""",
    )
    source_lines = "\n".join(
        f"- `{item['slice_id']}`: Product PASS `{item['product_pass']}`, verification `{item['verification_present']}`"
        for item in ledger["source_slices"]
    )
    write_text(
        ROOT / "source-map.md",
        frontmatter("built_pending_review")
        + f"""
# Source Map

Read-only source root: `{ledger['source_root']}`

Source slices scanned: `{ledger['source_slice_count']}`

Original plan items mapped: `{ledger['original_plan_item_count']}`

Sources:

{source_lines}

These are sandbox status records only. They are not evidence support, reviewed truth, action basis, formal vault approval, or mainline readiness.
""",
    )
    write_text(
        ROOT / "verification.md",
        frontmatter("local_verification_passed_pending_review")
        + f"""
# Verification

Default read-only verification command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_evidence_ledger.py
```

Expected local result:

- Primary `artifact/evidence-ledger.json` validates against current sandbox file evidence.
- Positive fixtures pass.
- Failure cases match the oracle.
- Prototype/readout show plan coverage, testing evidence, positive improvements, and non-production boundaries.

Builder-only regeneration command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_evidence_ledger.py --rebuild
```

`--rebuild` deletes and regenerates slice-local generated directories. It is not a read-only reviewer command.

Final gate command after reviews:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_evidence_ledger.py --final-gate
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
