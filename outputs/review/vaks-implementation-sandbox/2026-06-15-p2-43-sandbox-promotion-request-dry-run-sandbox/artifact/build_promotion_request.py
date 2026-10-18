from __future__ import annotations

from pathlib import Path

from promotion_common import (
    PRECONDITIONS,
    REQUEST_ITEMS,
    REQUIRED_NON_CLAIMS,
    ROOT,
    SLICE_ID,
    SOURCE_SLICE_ID,
    TRUTH_BOUNDARY,
    default_packet,
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
    base = default_packet("promotion-request-dry-run")
    write_json(ROOT / "fixtures" / "valid-promotion-request-dry-run.json", base)
    approval = default_packet("approval-requirements-view")
    approval["operator_note"] = "Approval-focused view. Still not approval."
    write_json(ROOT / "fixtures" / "valid-approval-requirements-view.json", approval)
    boundary = default_packet("boundary-stop-view")
    boundary["operator_note"] = "Boundary-focused view. Stop before all listed actions."
    write_json(ROOT / "fixtures" / "valid-boundary-stop-view.json", boundary)
    cases = make_failure_cases(base)
    write_json(ROOT / "artifact" / "failure-case-oracle.json", {"slice_id": SLICE_ID, "cases": cases})
    lines = [f"# Failure Case Oracle", "", f"Slice: `{SLICE_ID}`", "", f"Total cases: {len(cases)}", ""]
    for name, expected in cases.items():
        lines.append(f"- `{name}` -> `{', '.join(expected)}`")
    write_text(ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines))


def build_contract() -> None:
    non_claims = "\n".join(f"- {item}" for item in REQUIRED_NON_CLAIMS)
    requests = "\n".join(f"- {item['label']}: {item['request_intent']}" for item in REQUEST_ITEMS)
    write_text(
        ROOT / "artifact" / "sandbox-promotion-request-dry-run-contract.md",
        f"""
# Sandbox Promotion Request Dry-Run Contract

Slice: `{SLICE_ID}`

Source slice: `{SOURCE_SLICE_ID}`

Truth boundary: `{TRUTH_BOUNDARY}`.

This sandbox drafts a request packet only. It does not submit a request, collect approval, capture user wording, promote, merge, commit, push, sync, move files into templates or tools, or access the formal vault.

## Request Items

{requests}

## Required Non-Claims

{non_claims}
""",
    )


def build_packets() -> None:
    packet = default_packet()
    requests = "\n".join(
        f"- {item['label']}: {item['request_intent']} Required approval: yes. Authorized now: no."
        for item in REQUEST_ITEMS
    )
    preconditions = "\n".join(
        f"- {item['label']}: {item['reason']} Satisfied now: no."
        for item in PRECONDITIONS
    )
    write_text(
        ROOT / "request-packets" / "promotion-request-dry-run.md",
        f"""
# Promotion Request Dry-Run

Status: `{packet['request_status']}`

This is not approval, not promotion, not mainline merge, not formal vault approval, and not action basis.

## Request Items

{requests}

## Preconditions Not Satisfied

{preconditions}

## Separate User Approval Required

No listed request is authorized now. The safe next action is to ask the user for separate explicit approval before any boundary-crossing path.
""",
    )


def build_prototype() -> None:
    prototype = ROOT / "prototype" / "sandbox-promotion-request-dry-run"
    request_cards = "\n".join(
        f"<article class=\"card\" data-request-item=\"{item['id']}\"><strong>{item['label']}</strong><span>{item['request_intent']}</span><p>Required approval: yes. Authorized now: no.</p></article>"
        for item in REQUEST_ITEMS
    )
    precondition_cards = "\n".join(
        f"<li data-precondition=\"{item['id']}\"><strong>{item['label']}</strong><span>{item['reason']}</span></li>"
        for item in PRECONDITIONS
    )
    write_text(
        prototype / "index.html",
        f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Promotion Request Dry-Run</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fb; color: #17202a; }}
    main {{ max-width: 1040px; margin: 0 auto; padding: 28px 18px 44px; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    .summary {{ color: #465667; max-width: 800px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; margin: 20px 0; }}
    .card, .panel {{ background: #ffffff; border: 1px solid #d9e1ec; border-radius: 8px; padding: 14px; }}
    .card span, li span {{ display: block; margin-top: 8px; color: #445566; }}
    li {{ margin: 10px 0; }}
    .notice {{ margin-top: 16px; border-left: 4px solid #2f6fed; background: #edf4ff; padding: 12px 14px; color: #1f3150; }}
  </style>
</head>
<body>
  <main>
    <h1>Promotion Request Dry-Run</h1>
    <p class="summary">Draft request only. not approval; not promotion; not mainline merge; not formal vault approval; not action basis.</p>
    <section class="grid">
      {request_cards}
    </section>
    <section class="panel">
      <h2>Preconditions not satisfied</h2>
      <ul>{precondition_cards}</ul>
    </section>
    <section class="notice">No request is submitted. No approval is collected. No operation is authorized now.</section>
  </main>
  <script src="app.js"></script>
</body>
</html>
""",
    )
    write_text(prototype / "app.js", 'document.documentElement.dataset.promotionDryRunReady = "true";')
    receipt = default_packet("prototype-receipt")
    receipt.update(
        {
            "record_kind": "sandbox_promotion_request_dry_run_prototype_receipt",
            "promotion_performed": False,
            "approval_collected": False,
            "formal_vault_accessed": False,
            "sync_performed": False,
            "commit_performed": False,
            "push_performed": False,
            "mainline_merged": False,
            "action_basis_created": False,
            "reviewed_knowledge_created": False,
            "evidence_support_created": False,
            "auto_advanced": False,
            "non_claims": REQUIRED_NON_CLAIMS,
        }
    )
    write_json(prototype / "receipt.json", receipt)


def build_reports() -> None:
    packet = default_packet()
    write_json(ROOT / "artifact" / "promotion-request-dry-run.json", packet)
    write_text(
        ROOT / "slice-plan.md",
        frontmatter("built_pending_review")
        + f"""
# Slice Plan

## Slice

`{SLICE_ID}`

## Objective

Draft a sandbox-only promotion request dry-run packet from `{SOURCE_SLICE_ID}`.

## Only Write Path

`outputs/review/vaks-implementation-sandbox/{SLICE_ID}/`

## Non-Goals

- No promotion.
- No formal vault access.
- No Obsidian sync.
- No commit or push.
- No mainline merge.
- No edits to protected architecture, template, tool, or wiki truth paths.
""",
    )
    write_text(
        ROOT / "source-map.md",
        frontmatter("built_pending_review")
        + f"""
# Source Map

Source readiness:

- `{packet['source_snapshot']['readiness_path']}`
- `{packet['source_snapshot']['product_report_path']}`

Source facts:

- Source Product status: `{packet['source_snapshot']['source_product_status']}`
- Completed sandbox slices: `{packet['source_snapshot']['completed_sandbox_slices']}`
- Product-grade sandbox slices: `{packet['source_snapshot']['product_grade_sandbox_slices']}`
- Enterprise production ready: `{packet['source_snapshot']['enterprise_production_ready']}`

These are sandbox status records only. They are not approval, promotion, evidence support, reviewed truth, action basis, formal vault approval, or mainline readiness.
""",
    )
    write_text(
        ROOT / "verification.md",
        frontmatter("local_verification_passed_pending_review")
        + """
# Verification

Default read-only verification command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\2026-06-15-p2-43-sandbox-promotion-request-dry-run-sandbox\\artifact\\verify_promotion_request.py
```

Expected local result:

- Primary `artifact/promotion-request-dry-run.json` validates.
- Positive fixtures pass.
- Failure cases match the oracle.
- Prototype/readout expose request items, preconditions, and non-claims without command, form, link, or formal-vault affordances.

Builder-only regeneration command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\2026-06-15-p2-43-sandbox-promotion-request-dry-run-sandbox\\artifact\\verify_promotion_request.py --rebuild
```

`--rebuild` deletes and regenerates slice-local generated directories. It is not a read-only reviewer command.

Final gate command after reviews:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\2026-06-15-p2-43-sandbox-promotion-request-dry-run-sandbox\\artifact\\verify_promotion_request.py --final-gate
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
