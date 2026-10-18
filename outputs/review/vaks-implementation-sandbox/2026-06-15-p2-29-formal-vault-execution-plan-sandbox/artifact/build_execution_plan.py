from __future__ import annotations

import argparse
import copy
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from execution_plan_common import (
    FORBIDDEN_OPERATIONS,
    PLAN_PURPOSE,
    REQUIRED_PLAN_CONTROLS_FALSE,
    REQUIRED_PLAN_CONTROLS_TRUE,
    REQUIRED_STEP_IDS,
    REQUIRED_STOP_CONDITIONS,
    ROOT,
    SLICE_ID,
    SOURCE_SLICE,
    canonical_hash,
    expected_plan_hash,
    expected_source_input_bundle_hash,
    inspect_prototype,
    load_prev_fixture,
    load_prev_receipt,
    source_inputs,
    validate_config,
    validate_failure_cases,
    write_json,
    write_text,
)


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def build_target_manifest(prev: dict[str, Any]) -> list[dict[str, Any]]:
    targets = []
    for item in prev["target_manifest"]:
        targets.append(
            {
                "id": item["id"],
                "relative_target": item["relative_target"],
                "source_path": item["source_path"],
                "source_sha256": item["source_sha256"],
                "content_binding": item["content_binding"],
                "planned_action": "future_copy_from_sandbox_source_to_relative_target",
                "plan_status": "planned_future_only_not_executable",
                "target_path_relative_only": True,
                "formal_vault_target_resolved": False,
                "formal_vault_target_exists_checked": False,
                "snapshot_taken": False,
                "hash_before_collected": False,
                "hash_after_collected": False,
                "write_enabled_now": False,
                "execution_enabled_now": False,
                "dry_run_only": True,
            }
        )
    return targets


def build_steps() -> list[dict[str, Any]]:
    labels = {
        "source_binding_reconfirm": "Reconfirm P2-28 and P2-25 source bindings before any future execution.",
        "target_manifest_reconfirm": "Reconfirm exact relative target manifest before any future execution.",
        "future_formal_vault_state_check": "Future-only check of formal vault target state.",
        "future_snapshot_plan": "Future-only snapshot plan before write.",
        "future_write_plan": "Future-only write plan; no command is emitted here.",
        "future_hash_after_plan": "Future-only post-write hash comparison plan.",
        "future_sync_plan": "Future-only sync consideration; no sync permission here.",
        "future_rollback_plan": "Future-only rollback route if later execution fails.",
        "future_closeout_plan": "Future-only closeout record and review handoff.",
    }
    steps = []
    for step_id in REQUIRED_STEP_IDS:
        steps.append(
            {
                "step_id": step_id,
                "label": labels[step_id],
                "status": "planned_future_only",
                "perform_now": False,
                "writes_now": False,
                "formal_vault_access_now": False,
                "formal_vault_state_check_now": False,
                "hash_now": False,
                "snapshot_now": False,
                "sync_now": False,
                "commit_now": False,
                "push_now": False,
                "promotion_now": False,
                "requires_future_user_confirmation": True,
                "requires_future_execution_slice": True,
                "command": "",
                "absolute_target_path": "",
                "copy_tool": "none",
            }
        )
    return steps


def build_samples(prev: dict[str, Any]) -> list[dict[str, Any]]:
    scope_ids = [item["id"] for item in prev["target_manifest"]]
    base_flags = {
        "actual_user_input": False,
        "approval_collected_now": False,
        "real_user_text_stored": False,
        "formal_vault_accessed": False,
        "formal_vault_state_inspected": False,
        "snapshot_taken": False,
        "rollback_executed": False,
        "hash_before_collected": False,
        "hash_after_collected": False,
        "execution_performed": False,
        "formal_vault_write_allowed_now": False,
        "action_basis_created": False,
        "reviewed_knowledge_created": False,
        "sync_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "promotion_allowed": False,
        "scope_ids": scope_ids,
        "synthetic_only": True,
    }
    samples = [
        {
            **base_flags,
            "id": "synthetic_approved_preflight_plan",
            "source_preflight_sample": "synthetic_approved_reference_preflight",
            "decision_verdict": "APPROVED_REFERENCE_SYNTHETIC",
            "preflight_result": "PREFLIGHT_DRY_RUN_COMPLETE_NOT_EXECUTABLE",
            "plan_draft_created": True,
            "executable_plan_created": False,
            "expected_plan_result": "PLAN_DRAFT_READY_FOR_FUTURE_REVIEW_NOT_EXECUTABLE",
            "next_gate": "future_separately_approved_execution_slice_required",
        },
        {
            **base_flags,
            "id": "synthetic_denied_preflight_plan",
            "source_preflight_sample": "synthetic_denied_reference_preflight",
            "decision_verdict": "DENIED_BY_USER",
            "preflight_result": "BLOCKED_BY_DENIAL_NOT_EXECUTED",
            "plan_draft_created": False,
            "executable_plan_created": False,
            "expected_plan_result": "BLOCKED_BY_DENIAL_NO_PLAN",
            "next_gate": "stop_and_record_denial_only",
        },
        {
            **base_flags,
            "id": "synthetic_revision_preflight_plan",
            "source_preflight_sample": "synthetic_revision_reference_preflight",
            "decision_verdict": "NEEDS_REVISION",
            "preflight_result": "BLOCKED_PENDING_PACKET_REVISION_NOT_EXECUTED",
            "plan_draft_created": False,
            "executable_plan_created": False,
            "expected_plan_result": "BLOCKED_BY_REVISION_NO_PLAN",
            "next_gate": "revise_packet_in_future_sandbox_only",
        },
        {
            **base_flags,
            "id": "synthetic_dirty_state_plan_block",
            "source_preflight_sample": "synthetic_dirty_state_preflight_block",
            "decision_verdict": "APPROVED_REFERENCE_SYNTHETIC",
            "preflight_result": "BLOCKED_BY_DIRTY_STATE_ACK_MISSING_NOT_EXECUTED",
            "plan_draft_created": False,
            "executable_plan_created": False,
            "expected_plan_result": "BLOCKED_BY_DIRTY_STATE_NO_PLAN",
            "next_gate": "stop_until_future_dirty_state_ack",
        },
    ]
    return samples


def build_base_config(scenario_mode: str = "approved_plan_draft") -> dict[str, Any]:
    prev = load_prev_fixture()
    prev_receipt = load_prev_receipt()
    inputs = source_inputs()
    targets = build_target_manifest(prev)
    controls = {key: True for key in REQUIRED_PLAN_CONTROLS_TRUE}
    controls.update({key: False for key in REQUIRED_PLAN_CONTROLS_FALSE})
    config = {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE,
        "execution_plan_version": "p2-29-formal-vault-execution-plan-v1",
        "truth_boundary": "sandbox_only_non_executing_plan",
        "purpose": PLAN_PURPOSE,
        "scenario_mode": scenario_mode,
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": [item["source_path"] for item in inputs],
        "operations": {key: False for key in FORBIDDEN_OPERATIONS},
        "plan_controls": controls,
        "source_inputs": inputs,
        "source_input_bundle_hash": expected_source_input_bundle_hash(inputs),
        "source_preflight_hash": prev["preflight_hash"],
        "source_preflight_input_bundle_hash": prev["source_input_bundle_hash"],
        "source_packet_hash": prev["source_packet_hash"],
        "source_packet_scope_hash": prev["source_packet_scope_hash"],
        "source_target_manifest_hash": prev["target_manifest_hash"],
        "source_required_preflight_hash": prev["preflight_contract"]["required_preflight_hash"],
        "source_receipt_preflight_hash": prev_receipt["preflight_hash"],
        "target_manifest": targets,
        "target_manifest_hash": canonical_hash(targets),
        "execution_plan_contract": {
            "contract_kind": "formal_vault_execution_plan_sandbox",
            "current_slice_executes": False,
            "current_slice_collects_approval": False,
            "formal_vault_access_disallowed": True,
            "formal_vault_state_inspection_disallowed": True,
            "formal_vault_write_disallowed": True,
            "formal_vault_hash_disallowed": True,
            "formal_vault_snapshot_disallowed": True,
            "plan_is_non_executable": True,
            "separate_future_execution_slice_required": True,
            "separate_final_user_confirmation_required": True,
            "preflight_pass_not_execution_permission": True,
            "approved_reference_not_executable_here": True,
            "deny_blocks_plan": True,
            "revise_blocks_plan": True,
            "dirty_state_blocks_plan": True,
            "default_result": "PLAN_DRAFT_ONLY_NOT_EXECUTABLE",
            "required_preflight_hash": prev["preflight_hash"],
            "required_target_manifest_hash": prev["target_manifest_hash"],
            "required_scope_ids": [item["id"] for item in prev["target_manifest"]],
        },
        "execution_plan_steps": build_steps(),
        "plan_samples": build_samples(prev),
        "non_execution_plan_receipt": {
            "approval_collected_now": False,
            "actual_user_input_used": False,
            "real_user_text_stored": False,
            "formal_vault_accessed": False,
            "formal_vault_state_inspected": False,
            "execution_performed": False,
            "snapshot_taken": False,
            "hash_before_collected": False,
            "hash_after_collected": False,
            "write_performed": False,
            "sync_performed": False,
            "commit_performed": False,
            "push_performed": False,
            "promotion_performed": False,
            "current_status": "formal_vault_execution_plan_draft_non_executable_pending_review",
            "non_claims": [
                "not actual approval",
                "not execution readiness",
                "not formal vault approval",
                "not action basis",
                "not reviewed knowledge",
                "not evidence support",
                "not a write command",
            ],
        },
        "stop_conditions": REQUIRED_STOP_CONDITIONS,
        "product_metrics": {
            "required_positive_fixtures": 3,
            "minimum_failure_cases": 85,
            "required_plan_samples": 4,
            "required_targets": 5,
            "max_journey_steps": 3,
        },
    }
    config["execution_plan_hash"] = expected_plan_hash(config)
    return config


def write_root_reports() -> None:
    write_text(
        ROOT / "slice-plan.md",
        f"""---
record_kind: sandbox_slice_plan
slice_id: {SLICE_ID}
status: built_pending_review
truth_boundary: sandbox_only
---

# Slice Plan

## Goal

Build a sandbox-only formal-vault execution plan shape after P2-28 preflight.

## This Slice Does

- Defines a non-executable plan contract.
- Carries P2-28 source and target bindings forward by hash.
- Provides positive fixtures for approved, denied, and revision scenarios.
- Provides failure cases for forbidden operations, target drift, source drift,
  executable steps, real-vault access, and authority confusion.
- Provides a static prototype for operator review.

## This Slice Does Not

- Does not collect real approval.
- Does not store real user text.
- Does not read, scan, hash, snapshot, write, or sync the formal vault.
- Does not emit commands.
- Does not create reviewed knowledge, evidence support, action basis, or
  mainline approval.
""",
    )
    write_text(
        ROOT / "source-map.md",
        f"""---
record_kind: sandbox_source_map
slice_id: {SLICE_ID}
status: built_pending_review
truth_boundary: sandbox_only
---

# Source Map

This slice consumes P2-28 as a hash-bound sandbox input.

## Read-Only Inputs

{chr(10).join(f"- `{item['id']}`: `{item['source_path']}` sha256 `{item['source_sha256']}`" for item in source_inputs())}

## Source Boundary

P2-28 Product Acceptance is treated only as sandbox evidence that the preflight
dry-run artifact was product-grade. It is not formal vault approval, execution
approval, reviewed knowledge, evidence support, action basis, sync approval,
commit approval, push approval, or promotion approval.
""",
    )
    write_text(
        ROOT / "verification.md",
        f"""---
record_kind: sandbox_verification
slice_id: {SLICE_ID}
status: local_verification_passed_pending_review
truth_boundary: sandbox_only
---

# Verification

## Commands

Explicit rebuild:

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_execution_plan.py --rebuild
```

Default verification:

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_execution_plan.py
```

Pre-acceptance final gate:

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_execution_plan.py --final-gate
```

Expected before Reviewer / Boundary / Product closeout: final gate fails only
because report statuses are pending.

## What Is Verified

- Three positive fixtures.
- At least eighty-five failure cases.
- Exact P2-28 source hashes and preflight hashes.
- Exact target binding carried from P2-28.
- Non-executable plan controls.
- No formal vault access, write, hash, snapshot, sync, commit, push, or promotion.
- Static prototype has no forms, downloads, storage/network APIs, command
  snippets, or executable controls.

## Non-Claims

Verification is diagnostic only. It is not Product Acceptance, formal vault
approval, execution readiness, action basis, evidence support, reviewed
knowledge, sync approval, commit approval, push approval, or promotion approval.
""",
    )
    for name, record_kind in [
        ("reviewer-report.md", "sandbox_reviewer_report"),
        ("boundary-audit.md", "sandbox_boundary_audit"),
        ("product-acceptance-report.md", "sandbox_product_acceptance_report"),
        ("next-step.md", "sandbox_next_step"),
    ]:
        title = name.removesuffix(".md").replace("-", " ").title()
        write_text(
            ROOT / name,
            f"""---
record_kind: {record_kind}
slice_id: {SLICE_ID}
status: pending
truth_boundary: sandbox_only
---

# {title}

Pending.
""",
        )


def write_contract() -> None:
    write_text(
        ROOT / "artifact" / "formal-vault-execution-plan-contract.md",
        """# Formal Vault Execution Plan Sandbox Contract

This artifact defines a future execution plan shape only.

Hard boundaries:

- It is sandbox-only.
- It is non-executable.
- It does not collect approval.
- It does not store real user text.
- It does not read, scan, hash, snapshot, write, or sync the formal vault.
- It does not emit shell commands or copy commands.
- It does not create reviewed knowledge, evidence support, or action basis.

The plan can only be used as review input for a separate future slice.
""",
    )


def write_prototype(config: dict[str, Any]) -> None:
    proto = ROOT / "prototype" / "formal-vault-execution-plan-sandbox"
    reset_dir(proto)
    write_text(
        proto / "00 Execution Plan Home.md",
        """# Execution Plan Home

Status: sandbox-only execution plan draft.

This home page shows the future plan shape without giving permission to execute.
""",
    )
    write_text(
        proto / "01 Non Executable Plan Contract.md",
        """# Non Executable Plan Contract

The plan is not a command, not approval, and not execution readiness.

Any real formal-vault operation requires a separate user-approved future slice.
""",
    )
    write_text(
        proto / "02 Target Manifest Plan.md",
        "# Target Manifest Plan\n\n" + "\n".join(
            f"- `{target['id']}` -> `{target['relative_target']}` from `{target['source_path']}`"
            for target in config["target_manifest"]
        ) + "\n",
    )
    write_text(
        proto / "03 Future State Snapshot Hash Plan.md",
        """# Future State Snapshot Hash Plan

These are future-only requirements:

- check formal vault state
- snapshot target files
- collect before hashes
- write only after a separate future execution gate
- collect after hashes

None of those operations happens in this slice.
""",
    )
    write_text(
        proto / "04 Stop Conditions.md",
        "# Stop Conditions\n\n" + "\n".join(f"- {item}" for item in config["stop_conditions"]) + "\n",
    )
    write_text(
        proto / "05 Non Execution Receipt.md",
        """# Non Execution Receipt

The receipt records that this slice did not access, inspect, write, sync, commit,
push, promote, or execute.
""",
    )
    write_text(
        proto / "06 Reviewer Packet.md",
        """# Reviewer Packet

Reviewer checks:

- exact P2-28 source binding
- exact target binding
- non-executable controls
- no command emission
- failure matrix coverage
- authority separation
""",
    )
    receipt = {
        "record_kind": "sandbox_formal_vault_execution_plan_receipt",
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "formal_vault_accessed": False,
        "formal_vault_state_inspected": False,
        "approval_collected_now": False,
        "actual_user_input_used": False,
        "real_user_text_stored": False,
        "execution_performed": False,
        "write_performed": False,
        "snapshot_taken": False,
        "hash_before_collected": False,
        "hash_after_collected": False,
        "sync_performed": False,
        "commit_performed": False,
        "push_performed": False,
        "promotion_performed": False,
        "target_count": len(config["target_manifest"]),
        "plan_step_count": len(config["execution_plan_steps"]),
        "plan_hash": config["execution_plan_hash"],
        "non_claims": config["non_execution_plan_receipt"]["non_claims"],
    }
    write_json(proto / "Receipts" / "formal-vault-execution-plan-receipt.json", receipt)
    write_text(
        proto / "execution-plan-inspector.html",
        """<!doctype html>
<html lang="en"
  data-sandbox-only="true"
  data-plan-only="true"
  data-non-executable="true"
  data-no-formal-vault-access="true"
  data-no-write="true"
  data-no-sync="true"
  data-no-authority="true">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Formal Vault Execution Plan Sandbox</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; color: #172026; background: #f8faf7; }
    header { padding: 20px 24px; background: #1d4735; color: #fff; }
    main { padding: 18px 24px; display: grid; gap: 14px; }
    .rail { border-left: 4px solid #cc7832; padding: 10px 14px; background: #fff; }
    .toolbar { display: flex; flex-wrap: wrap; gap: 8px; }
    button { border: 1px solid #8aa096; background: #fff; padding: 7px 10px; border-radius: 6px; }
    .card { border: 1px solid #d5ded8; background: #fff; border-radius: 8px; padding: 14px; }
    .tag { font-size: 12px; color: #52645b; text-transform: uppercase; }
    input { padding: 8px 10px; border: 1px solid #8aa096; border-radius: 6px; max-width: 360px; }
  </style>
</head>
<body>
  <header>
    <h1>Formal Vault Execution Plan Sandbox</h1>
    <p>Plan draft only. No approval, no formal vault access, no write, no command.</p>
  </header>
  <main>
    <section class="rail" role="note">This surface is a review aid, not authority.</section>
    <div class="toolbar" role="toolbar" aria-label="Plan filters">
      <button type="button" data-filter="all">All</button>
      <button type="button" data-filter="contract">Contract</button>
      <button type="button" data-filter="targets">Targets</button>
      <button type="button" data-filter="future">Future</button>
      <button type="button" data-filter="receipt">Receipt</button>
      <button type="button" data-filter="stops">Stops</button>
    </div>
    <input id="q" type="search" placeholder="Filter review cards">
    <section class="card" data-kind="contract"><div class="tag">contract</div><h2>Non-executable plan</h2><p>Current slice cannot perform the plan.</p></section>
    <section class="card" data-kind="targets"><div class="tag">targets</div><h2>Exact target binding</h2><p>Targets are relative labels bound to P2-28 inputs.</p></section>
    <section class="card" data-kind="future"><div class="tag">future</div><h2>Future-only operations</h2><p>State check, snapshot, write, hash, and closeout are future gates.</p></section>
    <section class="card" data-kind="receipt"><div class="tag">receipt</div><h2>Non-execution receipt</h2><p>The receipt records no access, no write, no sync, and no promotion.</p></section>
    <section class="card" data-kind="stops"><div class="tag">stops</div><h2>Stop conditions</h2><p>Any real execution request stops this sandbox.</p></section>
  </main>
  <script>
    const cards = Array.from(document.querySelectorAll('.card'));
    const query = document.getElementById('q');
    document.querySelectorAll('button[data-filter]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const filter = btn.dataset.filter;
        cards.forEach((card) => {
          card.hidden = filter !== 'all' && card.dataset.kind !== filter;
        });
      });
    });
    query.addEventListener('input', () => {
      const needle = query.value.toLowerCase();
      cards.forEach((card) => {
        card.hidden = !card.textContent.toLowerCase().includes(needle);
      });
    });
  </script>
</body>
</html>
""",
    )


Mutator = tuple[str, str, Callable[[dict[str, Any]], None]]


def set_nested(config: dict[str, Any], path: list[Any], value: Any) -> None:
    node: Any = config
    for part in path[:-1]:
        node = node[part]
    node[path[-1]] = value


def rehash(config: dict[str, Any]) -> None:
    config["execution_plan_hash"] = expected_plan_hash(config)


def replace_stop_conditions_with_command(config: dict[str, Any]) -> None:
    config["stop_conditions"] = ["Copy-Item source H:/Obsidian/资料库/target.md"]
    rehash(config)


def append_stop_condition_command(config: dict[str, Any]) -> None:
    config["stop_conditions"].append("robocopy source H:/Obsidian/资料库")
    rehash(config)


def reorder_stop_conditions(config: dict[str, Any]) -> None:
    config["stop_conditions"] = list(reversed(config["stop_conditions"]))
    rehash(config)


def drift_scenario_mode(config: dict[str, Any]) -> None:
    config["scenario_mode"] = "approved_execute_now"
    rehash(config)


def drift_read_only_sources(config: dict[str, Any]) -> None:
    config["read_only_sources"] = ["outputs/review/other-safe-source.md"]
    rehash(config)


def drift_max_journey_steps(config: dict[str, Any]) -> None:
    config["product_metrics"]["max_journey_steps"] = 999
    rehash(config)


def drift_purpose_authority(config: dict[str, Any]) -> None:
    config["purpose"] = "This artifact is approved and ready to execute now."
    rehash(config)


def make_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: list[Mutator] = []
    for op in FORBIDDEN_OPERATIONS:
        cases.append((f"forbidden-{op}", f"Forbidden operation `{op}` set true.", lambda cfg, key=op: set_nested(cfg, ["operations", key], True)))
    for key in REQUIRED_PLAN_CONTROLS_TRUE:
        cases.append((f"control-{key}-false", f"Required true control `{key}` set false.", lambda cfg, k=key: set_nested(cfg, ["plan_controls", k], False)))
    for key in REQUIRED_PLAN_CONTROLS_FALSE:
        cases.append((f"control-{key}-true", f"Required false control `{key}` set true.", lambda cfg, k=key: set_nested(cfg, ["plan_controls", k], True)))
    for idx, source_key in enumerate([
        "source_preflight_hash",
        "source_preflight_input_bundle_hash",
        "source_packet_hash",
        "source_packet_scope_hash",
        "source_target_manifest_hash",
        "source_required_preflight_hash",
        "source_receipt_preflight_hash",
    ], start=1):
        cases.append((f"source-hash-{idx}-{source_key}", f"Source hash claim `{source_key}` drifted.", lambda cfg, k=source_key: set_nested(cfg, [k], "0" * 64)))
    cases.extend(
        [
            ("source-inputs-missing", "Source input list is empty.", lambda cfg: set_nested(cfg, ["source_inputs"], [])),
            ("source-inputs-bad-sha", "First source input hash drifts.", lambda cfg: set_nested(cfg, ["source_inputs", 0, "source_sha256"], "1" * 64)),
            ("source-input-bundle-drift", "Source bundle hash drifts.", lambda cfg: set_nested(cfg, ["source_input_bundle_hash"], "2" * 64)),
            ("target-missing-one", "One target removed.", lambda cfg: cfg["target_manifest"].pop()),
            ("target-extra-one", "Extra target added.", lambda cfg: cfg["target_manifest"].append(copy.deepcopy(cfg["target_manifest"][0]) | {"id": "extra_target"})),
            ("target-relative-drift", "Target relative path drifts.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "relative_target"], "VAKS-Workbench-Draft/Wrong.md")),
            ("target-source-path-drift", "Target source path drifts.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "source_path"], "outputs/review/wrong.md")),
            ("target-source-hash-drift", "Target source hash drifts.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "source_sha256"], "3" * 64)),
            ("target-content-binding-drift", "Target content binding drifts.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "content_binding"], "loose")),
            ("target-absolute-path", "Target uses absolute Windows path.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "relative_target"], "H:/Obsidian/资料库/Wrong.md")),
            ("target-parent-traversal", "Target uses parent traversal.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "relative_target"], "../Wrong.md")),
            ("target-resolved-now", "Target resolved against formal vault.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "formal_vault_target_resolved"], True)),
            ("target-exists-checked-now", "Formal vault target existence checked.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "formal_vault_target_exists_checked"], True)),
            ("target-write-enabled-now", "Target write enabled now.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "write_enabled_now"], True)),
            ("target-execution-enabled-now", "Target execution enabled now.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "execution_enabled_now"], True)),
            ("target-hash-before-collected", "Target hash-before collected.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "hash_before_collected"], True)),
            ("target-hash-after-collected", "Target hash-after collected.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "hash_after_collected"], True)),
            ("target-manifest-hash-drift", "Target manifest hash drifts.", lambda cfg: set_nested(cfg, ["target_manifest_hash"], "4" * 64)),
            ("contract-kind-drift", "Contract kind drifts.", lambda cfg: set_nested(cfg, ["execution_plan_contract", "contract_kind"], "execution_permission")),
            ("contract-executes-true", "Contract claims current slice executes.", lambda cfg: set_nested(cfg, ["execution_plan_contract", "current_slice_executes"], True)),
            ("contract-vault-access-allowed", "Contract allows vault access.", lambda cfg: set_nested(cfg, ["execution_plan_contract", "formal_vault_access_disallowed"], False)),
            ("contract-plan-executable", "Contract says plan is executable.", lambda cfg: set_nested(cfg, ["execution_plan_contract", "plan_is_non_executable"], False)),
            ("contract-preflight-hash-drift", "Contract preflight hash drifts.", lambda cfg: set_nested(cfg, ["execution_plan_contract", "required_preflight_hash"], "5" * 64)),
            ("contract-scope-ids-drift", "Contract scope ids drift.", lambda cfg: set_nested(cfg, ["execution_plan_contract", "required_scope_ids"], ["native_home"])),
            ("steps-missing-one", "One plan step removed.", lambda cfg: cfg["execution_plan_steps"].pop()),
            ("steps-extra-one", "Extra plan step added.", lambda cfg: cfg["execution_plan_steps"].append(copy.deepcopy(cfg["execution_plan_steps"][0]) | {"step_id": "extra_step"})),
            ("step-status-executable", "Step status is executable.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "status"], "ready_to_execute")),
            ("step-perform-now", "Step performs now.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "perform_now"], True)),
            ("step-writes-now", "Step writes now.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "writes_now"], True)),
            ("step-vault-access-now", "Step accesses vault now.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "formal_vault_access_now"], True)),
            ("step-state-check-now", "Step checks vault state now.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "formal_vault_state_check_now"], True)),
            ("step-hash-now", "Step hashes now.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "hash_now"], True)),
            ("step-snapshot-now", "Step snapshots now.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "snapshot_now"], True)),
            ("step-sync-now", "Step syncs now.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "sync_now"], True)),
            ("step-future-confirmation-missing", "Step drops future user confirmation.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "requires_future_user_confirmation"], False)),
            ("step-future-slice-missing", "Step drops future execution slice.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "requires_future_execution_slice"], False)),
            ("step-command-present", "Step emits a shell command.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "command"], "Copy-Item source target")),
            ("step-absolute-target-present", "Step contains absolute target path.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "absolute_target_path"], "H:/Obsidian/资料库/Wrong.md")),
            ("step-copy-tool-present", "Step names a copy tool.", lambda cfg: set_nested(cfg, ["execution_plan_steps", 0, "copy_tool"], "Copy-Item")),
            ("sample-approved-executable-plan", "Approved sample creates executable plan.", lambda cfg: set_nested(cfg, ["plan_samples", 0, "executable_plan_created"], True)),
            ("sample-approved-executes", "Approved sample executes.", lambda cfg: set_nested(cfg, ["plan_samples", 0, "execution_performed"], True)),
            ("sample-approved-writes", "Approved sample allows write now.", lambda cfg: set_nested(cfg, ["plan_samples", 0, "formal_vault_write_allowed_now"], True)),
            ("sample-approved-action-basis", "Approved sample creates action basis.", lambda cfg: set_nested(cfg, ["plan_samples", 0, "action_basis_created"], True)),
            ("sample-denied-plan-created", "Denied sample creates plan draft.", lambda cfg: set_nested(cfg, ["plan_samples", 1, "plan_draft_created"], True)),
            ("sample-denied-wrong-result", "Denied sample has wrong result.", lambda cfg: set_nested(cfg, ["plan_samples", 1, "expected_plan_result"], "PLAN_DRAFT_READY_FOR_FUTURE_REVIEW_NOT_EXECUTABLE")),
            ("sample-revision-plan-created", "Revision sample creates plan draft.", lambda cfg: set_nested(cfg, ["plan_samples", 2, "plan_draft_created"], True)),
            ("sample-dirty-plan-created", "Dirty-state sample creates plan draft.", lambda cfg: set_nested(cfg, ["plan_samples", 3, "plan_draft_created"], True)),
            ("sample-real-user-input", "Sample uses real user input.", lambda cfg: set_nested(cfg, ["plan_samples", 0, "actual_user_input"], True)),
            ("sample-real-user-text-stored", "Sample stores real user text.", lambda cfg: set_nested(cfg, ["plan_samples", 0, "real_user_text_stored"], True)),
            ("sample-vault-state-inspected", "Sample inspects vault state.", lambda cfg: set_nested(cfg, ["plan_samples", 0, "formal_vault_state_inspected"], True)),
            ("sample-scope-ids-drift", "Sample scope ids drift.", lambda cfg: set_nested(cfg, ["plan_samples", 0, "scope_ids"], ["native_home"])),
            ("receipt-approval-collected", "Receipt says approval collected.", lambda cfg: set_nested(cfg, ["non_execution_plan_receipt", "approval_collected_now"], True)),
            ("receipt-vault-accessed", "Receipt says vault accessed.", lambda cfg: set_nested(cfg, ["non_execution_plan_receipt", "formal_vault_accessed"], True)),
            ("receipt-executed", "Receipt says execution performed.", lambda cfg: set_nested(cfg, ["non_execution_plan_receipt", "execution_performed"], True)),
            ("receipt-write-performed", "Receipt says write performed.", lambda cfg: set_nested(cfg, ["non_execution_plan_receipt", "write_performed"], True)),
            ("receipt-sync-performed", "Receipt says sync performed.", lambda cfg: set_nested(cfg, ["non_execution_plan_receipt", "sync_performed"], True)),
            ("receipt-commit-performed", "Receipt says commit performed.", lambda cfg: set_nested(cfg, ["non_execution_plan_receipt", "commit_performed"], True)),
            ("receipt-promotion-performed", "Receipt says promotion performed.", lambda cfg: set_nested(cfg, ["non_execution_plan_receipt", "promotion_performed"], True)),
            ("receipt-status-drift", "Receipt status drifts.", lambda cfg: set_nested(cfg, ["non_execution_plan_receipt", "current_status"], "ready_to_execute")),
            ("receipt-non-claims-missing", "Receipt non-claims removed.", lambda cfg: set_nested(cfg, ["non_execution_plan_receipt", "non_claims"], [])),
            ("execution-plan-hash-drift", "Execution plan hash drifts.", lambda cfg: set_nested(cfg, ["execution_plan_hash"], "6" * 64)),
            ("metric-floor-too-low", "Failure-case floor too low.", lambda cfg: set_nested(cfg, ["product_metrics", "minimum_failure_cases"], 10)),
            ("unknown-top-level-command", "Unknown top-level shell command injection.", lambda cfg: cfg.update({"shell_command": "Copy-Item source H:/Obsidian/资料库/target.md"})),
            ("unknown-top-level-absolute-path", "Unknown top-level absolute vault path injection.", lambda cfg: cfg.update({"absolute_vault_path": "H:/Obsidian/资料库/target.md"})),
            ("unknown-top-level-sync-command", "Unknown top-level sync command injection.", lambda cfg: cfg.update({"formal_vault_sync_command": "robocopy source H:/Obsidian/资料库"})),
            ("unknown-target-field", "Unknown target field injection.", lambda cfg: cfg["target_manifest"][0].update({"shell_command": "Copy-Item source target"})),
            ("unknown-step-field", "Unknown step field injection.", lambda cfg: cfg["execution_plan_steps"][0].update({"formal_vault_sync_command": "robocopy source target"})),
            ("unknown-sample-field", "Unknown sample field injection.", lambda cfg: cfg["plan_samples"][0].update({"absolute_vault_path": "H:/Obsidian/资料库/target.md"})),
            ("unknown-receipt-field", "Unknown receipt field injection.", lambda cfg: cfg["non_execution_plan_receipt"].update({"write_command": "Copy-Item source target"})),
            ("unknown-safe-top-level-field", "Unknown safe-looking top-level field injection.", lambda cfg: cfg.update({"operator_note": "extra field outside schema"})),
            ("stop-conditions-command-replaced-rehashed", "Stop conditions replaced by command after hash recompute.", replace_stop_conditions_with_command),
            ("stop-conditions-command-appended-rehashed", "Stop conditions append command after hash recompute.", append_stop_condition_command),
            ("stop-conditions-order-reversed-rehashed", "Stop conditions order drift after hash recompute.", reorder_stop_conditions),
            ("scenario-mode-drift-rehashed", "Scenario mode drifts after hash recompute.", drift_scenario_mode),
            ("read-only-sources-drift-rehashed", "Read-only source list drifts after hash recompute.", drift_read_only_sources),
            ("max-journey-steps-drift-rehashed", "Journey step limit drifts after hash recompute.", drift_max_journey_steps),
            ("purpose-authority-confusion-rehashed", "Purpose claims execution approval after hash recompute.", drift_purpose_authority),
        ]
    )

    failure_dir = ROOT / "failure-cases"
    reset_dir(failure_dir)
    oracle_cases: dict[str, list[str]] = {}
    for index, (case_id, description, mutator) in enumerate(cases, start=1):
        cfg = copy.deepcopy(base)
        mutator(cfg)
        errors = validate_config(cfg)
        if not errors:
            raise RuntimeError(f"failure case did not fail: {case_id}")
        file_name = f"{index:02d}-{case_id}.json"
        payload = {
            "case_id": case_id,
            "description": description,
            "expected_errors": errors,
            "config": cfg,
        }
        write_json(failure_dir / file_name, payload)
        oracle_cases[file_name] = errors
    return oracle_cases


def write_oracle(oracle_cases: dict[str, list[str]]) -> None:
    write_json(
        ROOT / "artifact" / "failure-case-oracle.json",
        {
            "record_kind": "sandbox_failure_case_oracle",
            "slice_id": SLICE_ID,
            "case_count": len(oracle_cases),
            "cases": oracle_cases,
        },
    )
    write_text(
        ROOT / "artifact" / "failure-case-oracle.md",
        "# Failure Case Oracle\n\n"
        + f"Case count: {len(oracle_cases)}\n\n"
        + "\n".join(f"- `{name}` -> `{', '.join(errors)}`" for name, errors in oracle_cases.items())
        + "\n",
    )


def write_fixtures(base: dict[str, Any]) -> None:
    fixtures = ROOT / "fixtures"
    reset_dir(fixtures)
    variants = [
        ("valid-execution-plan-config.json", "approved_plan_draft"),
        ("valid-deny-execution-plan-config.json", "denial_block_record"),
        ("valid-revise-execution-plan-config.json", "revision_block_record"),
    ]
    for name, mode in variants:
        cfg = copy.deepcopy(base)
        cfg["scenario_mode"] = mode
        cfg["execution_plan_hash"] = expected_plan_hash(cfg)
        errors = validate_config(cfg)
        if errors:
            raise RuntimeError(f"valid fixture failed {name}: {errors}")
        write_json(fixtures / name, cfg)


def build_all() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for sub in ["artifact", "fixtures", "failure-cases", "prototype"]:
        (ROOT / sub).mkdir(parents=True, exist_ok=True)
    base = build_base_config()
    errors = validate_config(base)
    if errors:
        raise RuntimeError(f"base config failed: {errors}")
    write_contract()
    write_fixtures(base)
    oracle_cases = make_failure_cases(base)
    write_oracle(oracle_cases)
    write_prototype(base)
    write_root_reports()
    failure_result = validate_failure_cases()
    prototype_result = inspect_prototype()
    if failure_result["mismatches"]:
        raise RuntimeError(f"failure case mismatches: {failure_result['mismatches']}")
    if prototype_result["issues"]:
        raise RuntimeError(f"prototype issues: {prototype_result['issues']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the P2-29 sandbox artifacts.")
    args = parser.parse_args()
    if not args.rebuild:
        raise SystemExit("Use --rebuild to generate artifacts.")
    build_all()
    print(f"built {SLICE_ID}")


if __name__ == "__main__":
    main()
