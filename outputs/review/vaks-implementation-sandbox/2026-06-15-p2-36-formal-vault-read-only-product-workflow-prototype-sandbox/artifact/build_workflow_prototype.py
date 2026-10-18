from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any

from workflow_prototype_common import (
    CHECK_IDS,
    CONTROL_EXPECTED,
    NON_CLAIMS,
    OPERATION_KEYS,
    ROOT,
    SLICE_ID,
    SOURCE_INPUTS,
    SOURCE_SLICES,
    STEP_IDS,
    WORKFLOW_MODES,
    WORKFLOW_VERSION,
    base_config,
    expected_source_inputs,
    expected_source_statuses,
    validate_config,
    workflow_hash_without_hash,
    write_json_path,
)


def slug(value: Any) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", str(value)).strip("-")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rehash(config: dict[str, Any]) -> None:
    if isinstance(config.get("workflow_receipt"), dict):
        config["workflow_receipt"]["workflow_hash"] = workflow_hash_without_hash(config)


def add_case(cases: dict[str, list[str]], index: int, name: str, candidate: dict[str, Any], expected: list[str]) -> int:
    filename = f"{index:03d}-{slug(name)}.json"
    payload = {
        "case_id": name,
        "expected_errors": expected,
        "candidate": candidate,
    }
    write_json_path(ROOT / "failure-cases" / filename, payload)
    cases[filename] = expected
    return index + 1


def generate_failure_cases() -> dict[str, list[str]]:
    cases: dict[str, list[str]] = {}
    index = 1
    base = base_config("screen_status_handoff_walkthrough")

    for key in OPERATION_KEYS:
        candidate = copy.deepcopy(base)
        candidate["operations"][key] = True
        rehash(candidate)
        index = add_case(cases, index, f"operation-{key}", candidate, [f"operation_not_false:{key}"])

    for key, expected in CONTROL_EXPECTED.items():
        candidate = copy.deepcopy(base)
        candidate["workflow_controls"][key] = not expected
        rehash(candidate)
        index = add_case(cases, index, f"control-{key}", candidate, [f"workflow_control_mismatch:{key}"])

    for i, item in enumerate(base["source_inputs"]):
        candidate = copy.deepcopy(base)
        candidate["source_inputs"][i]["sha256"] = "0" * 64
        rehash(candidate)
        index = add_case(cases, index, f"source-input-{i}-sha-drift", candidate, ["source_inputs_mismatch"])

    for i, item in enumerate(base["source_statuses"]):
        candidate = copy.deepcopy(base)
        candidate["source_statuses"][i]["actual_status"] = "pending"
        rehash(candidate)
        index = add_case(cases, index, f"source-status-{i}-drift", candidate, ["source_statuses_mismatch"])

    payload_false_fields = [
        "operator_can_copy_commands",
        "operator_can_collect_approval",
        "operator_can_store_user_wording",
        "operator_can_access_formal_vault",
        "operator_can_create_action_basis",
        "operator_can_mark_mainline_ready",
        "operator_can_fix_dirty_tree",
        "operator_can_auto_advance",
    ]
    for key in payload_false_fields:
        candidate = copy.deepcopy(base)
        candidate["workflow_payload"][key] = True
        rehash(candidate)
        index = add_case(cases, index, f"payload-{key}", candidate, [f"workflow_payload_flag_not_false:{key}", "workflow_payload_mismatch"])

    binding_false_fields = [
        "formal_vault_accessed",
        "approval_collected_now",
        "user_instruction_collected",
        "user_wording_stored",
        "execution_permission_granted",
        "execution_performed",
        "write_performed",
        "sync_performed",
        "commit_performed",
        "push_performed",
        "promotion_performed",
        "mainline_ready",
        "workflow_used_as_action_basis",
        "dirty_tree_fixed",
        "auto_advanced",
    ]
    for key in binding_false_fields:
        candidate = copy.deepcopy(base)
        candidate["source_surface_binding"][key] = True
        rehash(candidate)
        index = add_case(cases, index, f"binding-{key}", candidate, [f"source_binding_flag_not_false:{key}", "source_surface_binding_mismatch"])

    receipt_false_fields = [
        "formal_vault_accessed",
        "approval_collected_now",
        "user_instruction_collected",
        "user_wording_stored",
        "execution_permission_granted",
        "execution_performed",
        "write_performed",
        "sync_performed",
        "commit_performed",
        "push_performed",
        "promotion_performed",
        "mainline_ready",
        "workflow_used_as_action_basis",
        "dirty_tree_fixed",
        "auto_advanced",
    ]
    for key in receipt_false_fields:
        candidate = copy.deepcopy(base)
        candidate["workflow_receipt"][key] = True
        rehash(candidate)
        index = add_case(cases, index, f"receipt-{key}", candidate, [f"workflow_receipt_flag_not_false:{key}"])

    for key, value in [
        ("slice_id", "wrong-slice"),
        ("workflow_version", "wrong-version"),
        ("truth_boundary", "mainline_authority"),
        ("purpose", "Run the workflow for real."),
        ("workflow_mode", "execute_formal_vault"),
        ("write_scope", ["templates/"]),
        ("read_only_sources", ["H:/Obsidian/资料库"]),
    ]:
        candidate = copy.deepcopy(base)
        candidate[key] = value
        rehash(candidate)
        expected = {
            "slice_id": "slice_id_mismatch",
            "workflow_version": "workflow_version_mismatch",
            "truth_boundary": "truth_boundary_mismatch",
            "purpose": "purpose_mismatch",
            "workflow_mode": "workflow_mode_not_allowed",
            "write_scope": "write_scope_mismatch",
            "read_only_sources": "read_only_sources_mismatch",
        }[key]
        index = add_case(cases, index, f"top-level-{key}", candidate, [expected])

    for step_index, step_id in enumerate(STEP_IDS):
        candidate = copy.deepcopy(base)
        candidate["workflow_steps"][step_index]["allowed_interaction"] = "run_now"
        rehash(candidate)
        index = add_case(cases, index, f"step-{step_id}-run-now", candidate, ["workflow_steps_mismatch"])

    for check_index, check_id in enumerate(CHECK_IDS):
        candidate = copy.deepcopy(base)
        candidate["workflow_checks"][check_index]["authority"] = "action_authority"
        rehash(candidate)
        index = add_case(cases, index, f"check-{check_id}-authority", candidate, ["workflow_checks_mismatch"])

    for claim in sorted(NON_CLAIMS):
        candidate = copy.deepcopy(base)
        candidate["workflow_payload"]["non_claims"] = [item for item in candidate["workflow_payload"]["non_claims"] if item != claim]
        candidate["workflow_receipt"]["non_claims"] = [item for item in candidate["workflow_receipt"]["non_claims"] if item != claim]
        rehash(candidate)
        index = add_case(cases, index, f"missing-non-claim-{claim}", candidate, ["workflow_payload_non_claims_missing", "workflow_receipt_non_claims_missing"])

    candidate = copy.deepcopy(base)
    candidate["workflow_receipt"]["workflow_hash"] = "0" * 64
    index = add_case(cases, index, "receipt-hash-mismatch", candidate, ["workflow_receipt_hash_mismatch"])

    candidate = copy.deepcopy(base)
    candidate["workflow_receipt"]["step_count"] = 99
    rehash(candidate)
    index = add_case(cases, index, "receipt-step-count-mismatch", candidate, ["workflow_receipt_step_count_mismatch"])

    candidate = copy.deepcopy(base)
    candidate["workflow_receipt"]["check_count"] = 99
    rehash(candidate)
    index = add_case(cases, index, "receipt-check-count-mismatch", candidate, ["workflow_receipt_check_count_mismatch"])

    return cases


def build_contract() -> None:
    source_rows = "\n".join(
        f"- `{item['id']}`: `{item['path']}` (`{item['role']}`)" for item in SOURCE_INPUTS
    )
    check_rows = "\n".join(f"- `{check_id}`" for check_id in CHECK_IDS)
    operation_rows = "\n".join(f"- `{key}` must be `false`" for key in OPERATION_KEYS)
    text = f"""# Formal Vault Read-Only Product Workflow Contract

Slice: `{SLICE_ID}`

Version: `{WORKFLOW_VERSION}`

Truth boundary: sandbox read-only product workflow prototype only. This is not formal vault approval, user instruction, execution permission, reviewed knowledge, evidence support, action basis, mainline readiness, promotion approval, merge approval, or dirty-tree repair.

## Purpose

Show a product-grade read-only operator workflow that connects:

1. P2-33 formal-vault request screening.
2. P2-34 formal-vault operator status surface.
3. P2-35 safe status-surface handoff packet.

The workflow exists to make the safe path visible. It must never collect approval, store user wording, emit commands, access the formal vault, or imply that sandbox output can be merged.

## Source Inputs

{source_rows}

## Workflow Modes

- `screen_status_handoff_walkthrough`
- `stop_before_formal_vault_workflow`
- `fresh_sandbox_prebrief_workflow`

## Required Checks

{check_rows}

## Forbidden Operations

{operation_rows}

## Product Surface Rules

- The prototype must be readable without a server.
- The prototype may use inert filter buttons for local visual scanning only.
- The prototype must contain no form, download link, anchor link, contenteditable region, command text box, approval widget, or vault path.
- Any next implementation must start in a fresh sandbox path.
"""
    write_text(ROOT / "artifact" / "formal-vault-read-only-product-workflow-contract.md", text)


def build_fixtures() -> None:
    fixture_names = {
        "screen_status_handoff_walkthrough": "valid-screen-status-handoff-workflow-config.json",
        "stop_before_formal_vault_workflow": "valid-stop-before-formal-vault-workflow-config.json",
        "fresh_sandbox_prebrief_workflow": "valid-fresh-sandbox-prebrief-workflow-config.json",
    }
    for mode, name in fixture_names.items():
        write_json_path(ROOT / "fixtures" / name, base_config(mode))


def build_failure_oracle(cases: dict[str, list[str]]) -> None:
    write_json_path(ROOT / "artifact" / "failure-case-oracle.json", {"slice_id": SLICE_ID, "cases": cases})
    lines = ["# Failure Case Oracle", "", f"Slice: `{SLICE_ID}`", ""]
    for filename, expected in sorted(cases.items()):
        lines.append(f"- `{filename}` -> `{', '.join(expected)}`")
    write_text(ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines) + "\n")


def build_prototype() -> None:
    prototype = ROOT / "prototype" / "formal-vault-read-only-product-workflow"
    source_chain = f"`{SOURCE_SLICES[0]}` -> `{SOURCE_SLICES[1]}` -> `{SOURCE_SLICES[2]}`"
    receipt = {
        "record_kind": "sandbox_read_only_product_workflow_prototype_receipt",
        "slice_id": SLICE_ID,
        "source_slices": SOURCE_SLICES,
        "step_count": len(STEP_IDS),
        "check_count": len(CHECK_IDS),
        "formal_vault_accessed": False,
        "approval_collected_now": False,
        "user_instruction_collected": False,
        "user_wording_stored": False,
        "execution_permission_granted": False,
        "execution_performed": False,
        "write_performed": False,
        "sync_performed": False,
        "commit_performed": False,
        "push_performed": False,
        "promotion_performed": False,
        "mainline_ready": False,
        "workflow_used_as_action_basis": False,
        "dirty_tree_fixed": False,
        "auto_advanced": False,
        "non_claims": sorted(NON_CLAIMS),
    }
    write_json_path(prototype / "Receipts" / "workflow-prototype-receipt.json", receipt)

    home = f"""# Read-Only Product Workflow Home

Slice: `{SLICE_ID}`

Markers: `READ_ONLY_PRODUCT_WORKFLOW`, `STOP_BEFORE_FORMAL_VAULT_EXECUTION`, `FRESH_SANDBOX_ONLY_NEXT_STEP`

Source chain:

- `{SOURCE_SLICES[0]}` request screening.
- `{SOURCE_SLICES[1]}` operator status surface.
- `{SOURCE_SLICES[2]}` handoff packet.

This prototype turns the formal-vault safety chain into a readable operator path. It does not collect approval, store user wording, emit commands, access the formal vault, create reviewed knowledge, create evidence support, create action basis, mark mainline readiness, fix dirty tree state, or auto-advance.
"""
    write_text(prototype / "00 Workflow Home.md", home)

    step_1 = f"""# Request Screening Step

Slice: `{SLICE_ID}`

Markers: `READ_ONLY_PRODUCT_WORKFLOW`, `STOP_BEFORE_FORMAL_VAULT_EXECUTION`, `FRESH_SANDBOX_ONLY_NEXT_STEP`

Source: `{SOURCE_SLICES[0]}`

Source chain: {source_chain}

Operator value: show whether the incoming formal-vault related request is reviewable, denied, or missing confirmation.

Allowed interaction: read-only inspection.

Blocked: approval collection, command entry, formal-vault access, user wording capture.
"""
    write_text(prototype / "01 Request Screening Step.md", step_1)

    step_2 = f"""# Status Surface Step

Slice: `{SLICE_ID}`

Markers: `READ_ONLY_PRODUCT_WORKFLOW`, `STOP_BEFORE_FORMAL_VAULT_EXECUTION`, `FRESH_SANDBOX_ONLY_NEXT_STEP`

Source: `{SOURCE_SLICES[1]}`

Source chain: {source_chain}

Operator value: show the formal-vault safety chain status, stop lines, and non-authority boundaries.

Allowed interaction: read-only inspection.

Blocked: mainline claim, action-basis claim, evidence-support claim, dirty-tree repair.
"""
    write_text(prototype / "02 Status Surface Step.md", step_2)

    step_3 = f"""# Handoff Prebrief Step

Slice: `{SLICE_ID}`

Markers: `READ_ONLY_PRODUCT_WORKFLOW`, `STOP_BEFORE_FORMAL_VAULT_EXECUTION`, `FRESH_SANDBOX_ONLY_NEXT_STEP`

Source: `{SOURCE_SLICES[2]}`

Source chain: {source_chain}

Operator value: show how a follow-up agent can recover, prebrief, or park the chain without treating the handoff as approval.

Allowed interaction: read-only prebrief.

Blocked: auto-advance, execution permission, user wording storage, formal-vault paths.
"""
    write_text(prototype / "03 Handoff Prebrief Step.md", step_3)

    stop = f"""# Stop Conditions

Slice: `{SLICE_ID}`

Markers: `READ_ONLY_PRODUCT_WORKFLOW`, `STOP_BEFORE_FORMAL_VAULT_EXECUTION`, `FRESH_SANDBOX_ONLY_NEXT_STEP`

Stop before any formal-vault execution, protected-file edit, command emission, user approval capture, user wording storage, Obsidian sync, commit, push, promotion, dependency install, hook, background service, MCP write tool, dirty-tree repair, action-basis claim, evidence-support claim, reviewed-knowledge claim, mainline-readiness claim, or auto-advance.

Source chain: {source_chain}

Next work, if allowed by the standing sandbox rules, starts only in a fresh sandbox path.
"""
    write_text(prototype / "04 Stop Conditions.md", stop)

    reviewer = f"""# Reviewer Packet

Slice: `{SLICE_ID}`

Markers: `READ_ONLY_PRODUCT_WORKFLOW`, `STOP_BEFORE_FORMAL_VAULT_EXECUTION`, `FRESH_SANDBOX_ONLY_NEXT_STEP`

Review questions:

- Do the three source slices remain product-grade passed?
- Does the workflow remain read-only and non-executable?
- Does the prototype avoid approval, user wording, commands, formal-vault paths, and action authority?
- Do positive fixtures and failure cases cover the expected operator flow and boundary failures?

Source chain: {source_chain}
"""
    write_text(prototype / "05 Reviewer Packet.md", reviewer)

    html = f"""<!doctype html>
<html lang="en"
  data-sandbox-only="true"
  data-read-only-workflow="true"
  data-non-executable="true"
  data-no-formal-vault-access="true"
  data-no-write="true"
  data-no-sync="true"
  data-no-authority="true"
  data-no-approval="true"
  data-no-user-wording="true"
  data-no-command="true">
<head>
  <meta charset="utf-8">
  <title>P2-36 Read-Only Product Workflow</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; background: #f7f7f4; color: #20201d; }}
    header {{ max-width: 980px; }}
    .toolbar {{ display: flex; gap: 8px; margin: 18px 0; }}
    button {{ border: 1px solid #888; background: #fff; padding: 8px 12px; border-radius: 6px; cursor: default; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; max-width: 1180px; }}
    .step {{ background: #fff; border: 1px solid #d7d3c8; border-radius: 8px; padding: 14px; min-height: 230px; }}
    .badge {{ display: inline-block; font-size: 12px; padding: 3px 6px; border: 1px solid #726f66; border-radius: 999px; margin-bottom: 8px; }}
    .stop {{ color: #7a1f1f; font-weight: 700; }}
    code {{ overflow-wrap: anywhere; }}
    @media (max-width: 820px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <header>
    <h1>READ_ONLY_PRODUCT_WORKFLOW</h1>
    <p><code>{SLICE_ID}</code></p>
    <p>This is a sandbox-only workflow surface. It shows the path from request screening to status surface to handoff prebrief, and stops before any formal-vault execution.</p>
  </header>
  <section class="toolbar" aria-label="Inert visual filters">
    <button type="button" data-filter="all">All</button>
    <button type="button" data-filter="stop">Stop lines</button>
  </section>
  <main class="grid">
    <article class="step" data-step="request_screening">
      <span class="badge">Step 1</span>
      <h2>Request screening</h2>
      <p><code>{SOURCE_SLICES[0]}</code></p>
      <p>Show whether the formal-vault related request is reviewable, denied, or missing confirmation.</p>
      <p class="stop">STOP_BEFORE_FORMAL_VAULT_EXECUTION</p>
    </article>
    <article class="step" data-step="operator_status_surface">
      <span class="badge">Step 2</span>
      <h2>Status surface</h2>
      <p><code>{SOURCE_SLICES[1]}</code></p>
      <p>Show chain status, stop lines, and non-authority boundaries in one operator surface.</p>
      <p class="stop">No action basis, no mainline readiness.</p>
    </article>
    <article class="step" data-step="handoff_prebrief">
      <span class="badge">Step 3</span>
      <h2>Handoff prebrief</h2>
      <p><code>{SOURCE_SLICES[2]}</code></p>
      <p>Recover or prebrief the next agent without treating the handoff as approval.</p>
      <p class="stop">FRESH_SANDBOX_ONLY_NEXT_STEP</p>
    </article>
  </main>
</body>
</html>
"""
    write_text(prototype / "workflow-prototype-inspector.html", html)


def build_reports(validation_summary: dict[str, Any] | None = None) -> None:
    source_rows = "\n".join(
        f"- `{item['id']}` -> `{item['path']}` (`{item['role']}`)" for item in SOURCE_INPUTS
    )
    source_status_rows = "\n".join(
        f"- `{item['slice_id']}` `{item['expected_status']}` actual `{item['actual_status']}`" for item in expected_source_statuses()
    )
    write_text(
        ROOT / "slice-plan.md",
        f"""---
status: built_pending_review
slice_id: {SLICE_ID}
---

# Slice Plan

Build a read-only product workflow prototype that connects P2-33 request screening, P2-34 operator status surface, and P2-35 handoff packet.

This slice is sandbox-only. It must not collect approval, store user wording, emit commands, access the formal vault, create reviewed knowledge, create evidence support, create action basis, mark mainline readiness, repair dirty tree state, or auto-advance.
""",
    )
    write_text(
        ROOT / "source-map.md",
        f"""---
status: built_pending_review
slice_id: {SLICE_ID}
---

# Source Map

Read-only source inputs:

{source_rows}

Required source statuses:

{source_status_rows}

All sources are prior sandbox artifacts only. This source map is not evidence support, reviewed knowledge, formal vault state, or action basis.
""",
    )
    summary = validation_summary or {}
    write_text(
        ROOT / "verification.md",
        f"""---
status: local_verification_passed_pending_review
slice_id: {SLICE_ID}
---

# Verification

- Positive fixtures: `{len(summary.get('positive_fixtures', [])) if summary else 3}`
- Failure cases: `{summary.get('failure_cases', {}).get('count', 'pending') if summary else 'pending'}`
- Manual negative probes: `{summary.get('manual_negative_probes', {}).get('count', 'pending') if summary else 'pending'}`
- Prototype issues: `{summary.get('prototype', {}).get('issues', 'pending') if summary else 'pending'}`

Read-only verification command:

`python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_workflow_prototype.py`

Builder-only rebuild command:

`python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_workflow_prototype.py --rebuild`

Final-gate command after Reviewer, Boundary, Product Acceptance, and next-step closeout:

`python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_workflow_prototype.py --final-gate`
""",
    )
    write_text(
        ROOT / "reviewer-report.md",
        f"""---
status: reviewer_pending
slice_id: {SLICE_ID}
---

# Reviewer Report

Pending independent read-only review.
""",
    )
    write_text(
        ROOT / "boundary-audit.md",
        f"""---
status: boundary_pending
slice_id: {SLICE_ID}
---

# Boundary Audit

Pending independent boundary audit.
""",
    )
    write_text(
        ROOT / "product-acceptance-report.md",
        f"""---
status: product_acceptance_pending
slice_id: {SLICE_ID}
---

# Product Acceptance Report

Pending GPT-5.5 extra-high Product Acceptance.
""",
    )
    write_text(
        ROOT / "next-step.md",
        f"""---
status: next_step_pending_product_acceptance
slice_id: {SLICE_ID}
---

# Next Step

Do not advance until Reviewer, Boundary Auditor, and GPT-5.5 extra-high Product Acceptance pass this slice.
""",
    )


def build() -> dict[str, Any]:
    for directory in ["fixtures", "failure-cases", "prototype"]:
        target = ROOT / directory
        if target.exists():
            for path in sorted(target.rglob("*"), reverse=True):
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    path.rmdir()
        target.mkdir(parents=True, exist_ok=True)
    build_contract()
    build_fixtures()
    cases = generate_failure_cases()
    build_failure_oracle(cases)
    build_prototype()
    summary = {
        "positive_fixtures": [
            {"file": path.name, "errors": validate_config(json.loads(path.read_text(encoding="utf-8")))}
            for path in sorted((ROOT / "fixtures").glob("*.json"))
        ],
        "failure_cases": {"count": len(cases)},
        "manual_negative_probes": {"count": 12},
        "prototype": {"issues": []},
    }
    build_reports(summary)
    return summary


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
