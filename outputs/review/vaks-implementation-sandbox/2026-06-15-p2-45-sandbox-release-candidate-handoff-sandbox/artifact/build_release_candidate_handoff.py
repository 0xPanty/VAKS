from __future__ import annotations

from pathlib import Path

from handoff_common import (
    APPROVAL_REQUIREMENTS,
    REQUIRED_NON_CLAIMS,
    ROOT,
    SLICE_ID,
    STOP_CONDITIONS,
    USER_QUESTIONS,
    default_handoff,
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
    base = default_handoff("release-candidate-handoff")
    write_json(ROOT / "fixtures" / "valid-release-candidate-handoff.json", base)
    plain = default_handoff("plain-user-answer")
    plain["operator_note"] = "Plain user-facing answer view. Still sandbox only."
    write_json(ROOT / "fixtures" / "valid-plain-user-answer.json", plain)
    agent = default_handoff("follow-up-agent-runbook")
    agent["operator_note"] = "Follow-up agent runbook view. Still sandbox only, with no approval or execution."
    write_json(ROOT / "fixtures" / "valid-follow-up-agent-runbook.json", agent)
    cases = make_failure_cases(base)
    write_json(ROOT / "artifact" / "failure-case-oracle.json", {"slice_id": SLICE_ID, "cases": cases})
    lines = ["# Failure Case Oracle", "", f"Slice: `{SLICE_ID}`", "", f"Total cases: {len(cases)}", ""]
    for name, expected in cases.items():
        lines.append(f"- `{name}` -> `{', '.join(expected)}`")
    write_text(ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines))


def build_contract() -> None:
    non_claims = "\n".join(f"- {item}" for item in REQUIRED_NON_CLAIMS)
    approvals = "\n".join(f"- {item}" for item in APPROVAL_REQUIREMENTS)
    write_text(
        ROOT / "artifact" / "sandbox-release-candidate-handoff-contract.md",
        f"""
# Sandbox Release-Candidate Handoff Contract

Slice: `{SLICE_ID}`

This package is a sandbox release-candidate handoff only. It makes the evidence ledger easier to read and rerun. It does not release, promote, merge, sync, commit, push, or approve action-basis use.

## Approval Requirements

{approvals}

## Required Non-Claims

{non_claims}
""",
    )


def build_packets() -> None:
    handoff = default_handoff()
    answers = "\n".join(f"- {item['label']}: {item['answer']}" for item in USER_QUESTIONS)
    stops = "\n".join(f"- {item}" for item in STOP_CONDITIONS)
    write_text(
        ROOT / "handoff-packets" / "release-candidate-handoff.md",
        f"""
# Release Candidate Handoff

Status: sandbox release candidate only.

Source slices: `{handoff['source_snapshot']['source_slice_count']}`

Original plan items: `{handoff['source_snapshot']['original_plan_item_count']}`

Product PASS slices: `{handoff['source_snapshot']['product_pass_count']}`

Verification slices: `{handoff['source_snapshot']['verification_present_count']}`

## Plain Answers

{answers}

## Follow-Up Agent Rule

Run the default verifier first:

```powershell
{handoff['follow_up_agent_runbook']['default_verification_command']}
```

If the next step would cross any stop condition, stop and ask for separate explicit user approval.

## Stop Conditions

{stops}

This handoff is not enterprise production, not mainline ready, not formal vault approval, not reviewed knowledge, not evidence support, and not action basis.
""",
    )


def build_prototype() -> None:
    handoff = default_handoff()
    prototype = ROOT / "prototype" / "sandbox-release-candidate-handoff"
    answer_cards = "\n".join(
        f"<article class=\"card\" data-user-question=\"{item['id']}\"><strong>{item['label']}</strong><span>{item['answer']}</span></article>"
        for item in USER_QUESTIONS
    )
    stops = "\n".join(f"<li data-stop-condition=\"{item}\">{item}</li>" for item in STOP_CONDITIONS)
    write_text(
        prototype / "index.html",
        f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sandbox Release-Candidate Handoff</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fb; color: #17202a; }}
    main {{ max-width: 1040px; margin: 0 auto; padding: 28px 18px 44px; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    .summary {{ color: #465667; max-width: 820px; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin: 20px 0; }}
    .card, .panel {{ background: #ffffff; border: 1px solid #d9e1ec; border-radius: 8px; padding: 14px; }}
    .card span {{ display: block; margin-top: 8px; color: #526273; }}
    li {{ margin: 8px 0; }}
    .notice {{ margin-top: 16px; border-left: 4px solid #2f6fed; background: #edf4ff; padding: 12px 14px; color: #1f3150; }}
  </style>
</head>
<body>
  <main>
    <h1>Sandbox Release-Candidate Handoff</h1>
    <p class="summary">sandbox release candidate only. Source slices {handoff['source_snapshot']['source_slice_count']}; original plan items {handoff['source_snapshot']['original_plan_item_count']}; not enterprise production; not mainline ready; not action basis.</p>
    <section class="cards">{answer_cards}</section>
    <section class="panel"><h2>Stop conditions</h2><ul>{stops}</ul></section>
    <section class="notice">No release is approved. No promotion, sync, commit, push, or action-basis use is authorized.</section>
  </main>
  <script src="app.js"></script>
</body>
</html>
""",
    )
    write_text(prototype / "app.js", 'document.documentElement.dataset.releaseCandidateHandoffReady = "true";')
    receipt = {
        "record_kind": "sandbox_release_candidate_handoff_prototype_receipt",
        "slice_id": SLICE_ID,
        "release_approved": False,
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
    handoff = default_handoff()
    write_json(ROOT / "artifact" / "release-candidate-handoff.json", handoff)
    write_text(
        ROOT / "slice-plan.md",
        frontmatter("built_pending_review")
        + f"""
# Slice Plan

## Slice

`{SLICE_ID}`

## Objective

Build a user-readable and follow-up-agent-readable sandbox release-candidate handoff package from p2-44 evidence.

## Only Write Path

`outputs/review/vaks-implementation-sandbox/{SLICE_ID}/`

## Non-Goals

- No release approval.
- No promotion.
- No formal vault access or sync.
- No commit or push.
- No edits to protected architecture, template, tool, or wiki truth paths.
""",
    )
    write_text(
        ROOT / "source-map.md",
        frontmatter("built_pending_review")
        + f"""
# Source Map

Source ledger:

- `{handoff['source_snapshot']['ledger_path']}`
- `{handoff['source_snapshot']['product_report_path']}`

Source counts:

- source slices: `{handoff['source_snapshot']['source_slice_count']}`
- Product PASS slices: `{handoff['source_snapshot']['product_pass_count']}`
- verification slices: `{handoff['source_snapshot']['verification_present_count']}`
- original plan items: `{handoff['source_snapshot']['original_plan_item_count']}`

These are sandbox status records only. They are not release approval, evidence support, reviewed truth, action basis, formal vault approval, or mainline readiness.
""",
    )
    write_text(
        ROOT / "verification.md",
        frontmatter("local_verification_passed_pending_review")
        + f"""
# Verification

Default read-only verification command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_release_candidate_handoff.py
```

Expected local result:

- Primary `artifact/release-candidate-handoff.json` validates against p2-44 evidence.
- Positive fixtures pass.
- Failure cases match the oracle.
- Prototype/readout show plain answers, stop conditions, and non-production boundaries.

Builder-only regeneration command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_release_candidate_handoff.py --rebuild
```

`--rebuild` deletes and regenerates slice-local generated directories. It is not a read-only reviewer command.

Final gate command after reviews:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_release_candidate_handoff.py --final-gate
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
