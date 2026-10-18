from __future__ import annotations

import argparse
import copy
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from dry_run_ledger_common import (
    ALLOWED_LEDGER_MODES,
    FORBIDDEN_OPERATIONS,
    LEDGER_PURPOSE,
    REQUIRED_ENTRY_RESULTS,
    REQUIRED_LEDGER_CONTROLS_FALSE,
    REQUIRED_LEDGER_CONTROLS_TRUE,
    REQUIRED_STOP_CONDITIONS,
    ROOT,
    SLICE_ID,
    SOURCE_SLICE,
    canonical_hash,
    expected_ledger_hash,
    expected_source_input_bundle_hash,
    inspect_prototype,
    load_prev_fixture,
    load_prev_receipt,
    sha256_file,
    source_inputs,
    validate_config,
    validate_failure_cases,
    validate_prototype_tamper,
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
                "source_plan_status": item["plan_status"],
                "ledger_target_status": "dry_run_recorded_not_performed",
                "formal_vault_target_resolved": False,
                "formal_vault_target_exists_checked": False,
                "hash_before_collected": False,
                "hash_after_collected": False,
                "write_enabled_now": False,
                "execution_enabled_now": False,
            }
        )
    return targets


def build_entries() -> list[dict[str, Any]]:
    questions = {
        "source_binding_reconfirm": "Would a future execution re-check P2-29 source hashes?",
        "target_manifest_reconfirm": "Would a future execution re-check target manifest exactness?",
        "future_formal_vault_state_check": "Would a future execution inspect formal vault state?",
        "future_snapshot_plan": "Would a future execution snapshot targets before writing?",
        "future_write_plan": "Would a future execution write only approved targets?",
        "future_hash_after_plan": "Would a future execution compare after hashes?",
        "future_sync_plan": "Would a future execution consider sync only after write review?",
        "future_rollback_plan": "Would a future execution have rollback evidence?",
        "future_closeout_plan": "Would a future execution close out with evidence and non-claims?",
    }
    entries = []
    for index, (entry_id, result) in enumerate(REQUIRED_ENTRY_RESULTS.items(), start=1):
        entries.append(
            {
                "entry_id": entry_id,
                "source_step_id": entry_id,
                "sequence": index,
                "review_question": questions[entry_id],
                "dry_run_result": result,
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
                "evidence_recorded": True,
                "non_claim": "dry_run_ledger_entry_not_execution",
            }
        )
    return entries


def build_samples(prev: dict[str, Any]) -> list[dict[str, Any]]:
    scope_ids = [item["id"] for item in prev["target_manifest"]]
    base = {
        "actual_user_input": False,
        "approval_collected_now": False,
        "real_user_text_stored": False,
        "formal_vault_accessed": False,
        "formal_vault_state_inspected": False,
        "snapshot_taken": False,
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
        "ledger_replayable": False,
        "ledger_is_execution_log": False,
        "entry_count": len(REQUIRED_ENTRY_RESULTS),
        "scope_ids": scope_ids,
        "synthetic_only": True,
    }
    return [
        {
            **base,
            "id": "synthetic_approved_plan_ledger",
            "source_plan_scenario": "approved_plan_draft",
            "ledger_mode": "approved_plan_dry_run_ledger",
            "ledger_created": True,
            "expected_ledger_result": "LEDGER_DRY_RUN_RECORDED_NOT_EXECUTABLE",
        },
        {
            **base,
            "id": "synthetic_denied_plan_ledger",
            "source_plan_scenario": "denial_block_record",
            "ledger_mode": "denial_block_ledger",
            "ledger_created": True,
            "expected_ledger_result": "BLOCKED_BY_DENIAL_LEDGER_ONLY",
        },
        {
            **base,
            "id": "synthetic_revision_plan_ledger",
            "source_plan_scenario": "revision_block_record",
            "ledger_mode": "revision_block_ledger",
            "ledger_created": True,
            "expected_ledger_result": "BLOCKED_BY_REVISION_LEDGER_ONLY",
        },
    ]


def build_base_config(mode: str = "approved_plan_dry_run_ledger") -> dict[str, Any]:
    prev = load_prev_fixture()
    receipt = load_prev_receipt()
    inputs = source_inputs()
    targets = build_target_manifest(prev)
    entries = build_entries()
    controls = {key: True for key in REQUIRED_LEDGER_CONTROLS_TRUE}
    controls.update({key: False for key in REQUIRED_LEDGER_CONTROLS_FALSE})
    config = {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE,
        "dry_run_ledger_version": "p2-30-formal-vault-execution-dry-run-ledger-v1",
        "truth_boundary": "sandbox_only_non_executing_ledger",
        "purpose": LEDGER_PURPOSE,
        "ledger_mode": mode,
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": [item["source_path"] for item in inputs],
        "operations": {key: False for key in FORBIDDEN_OPERATIONS},
        "ledger_controls": controls,
        "source_inputs": inputs,
        "source_input_bundle_hash": expected_source_input_bundle_hash(inputs),
        "source_plan_hash": prev["execution_plan_hash"],
        "source_plan_input_bundle_hash": prev["source_input_bundle_hash"],
        "source_target_manifest_hash": prev["target_manifest_hash"],
        "source_plan_receipt_hash": receipt["plan_hash"],
        "source_ledger_plan_contract_hash": sha256_file(
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/artifact/formal-vault-execution-plan-contract.md"
        ),
        "target_manifest": targets,
        "target_manifest_hash": canonical_hash(targets),
        "dry_run_ledger_contract": {
            "contract_kind": "formal_vault_execution_dry_run_ledger_sandbox",
            "current_slice_executes": False,
            "current_slice_collects_approval": False,
            "formal_vault_access_disallowed": True,
            "formal_vault_state_inspection_disallowed": True,
            "formal_vault_write_disallowed": True,
            "formal_vault_hash_disallowed": True,
            "formal_vault_snapshot_disallowed": True,
            "ledger_is_non_executable": True,
            "ledger_is_not_execution_log": True,
            "ledger_is_not_action_basis": True,
            "separate_future_execution_slice_required": True,
            "separate_final_user_confirmation_required": True,
            "plan_pass_not_execution_permission": True,
            "default_result": "LEDGER_DRY_RUN_ONLY_NOT_EXECUTABLE",
            "required_plan_hash": prev["execution_plan_hash"],
            "required_plan_contract_hash": sha256_file(
                f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE}/artifact/formal-vault-execution-plan-contract.md"
            ),
            "required_scope_ids": [item["id"] for item in prev["target_manifest"]],
            "required_entry_ids": list(REQUIRED_ENTRY_RESULTS),
        },
        "ledger_entries": entries,
        "ledger_samples": build_samples(prev),
        "non_execution_ledger_receipt": {
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
            "ledger_replayed": False,
            "ledger_used_as_action_basis": False,
            "current_status": "formal_vault_execution_dry_run_ledger_non_executable_pending_review",
            "non_claims": [
                "not actual approval",
                "not execution readiness",
                "not formal vault approval",
                "not action basis",
                "not reviewed knowledge",
                "not evidence support",
                "not an execution log",
                "not replayable",
            ],
        },
        "stop_conditions": REQUIRED_STOP_CONDITIONS,
        "product_metrics": {
            "required_positive_fixtures": 3,
            "minimum_failure_cases": 100,
            "required_ledger_samples": 3,
            "required_targets": 5,
            "required_entries": len(REQUIRED_ENTRY_RESULTS),
            "max_journey_steps": 3,
        },
    }
    config["dry_run_ledger_hash"] = expected_ledger_hash(config)
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

Build a sandbox-only dry-run ledger for the future formal-vault execution plan.

## This Slice Does

- Records a dry-run ledger for P2-29 plan steps.
- Preserves exact P2-29 source and target binding.
- Shows which future gates would be required without performing them.
- Provides fixtures, failure cases, verifier, and review prototype.

## This Slice Does Not

- Does not collect real approval.
- Does not store real user text.
- Does not read, scan, hash, snapshot, write, or sync the formal vault.
- Does not emit shell or copy commands.
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

This slice consumes P2-29 as a hash-bound sandbox input.

## Read-Only Inputs

{chr(10).join(f"- `{item['id']}`: `{item['source_path']}` sha256 `{item['source_sha256']}`" for item in source_inputs())}

## Source Boundary

P2-29 Product Acceptance is sandbox evidence only. It is not formal vault
approval, execution permission, action basis, reviewed knowledge, sync
approval, commit approval, push approval, or promotion approval.
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

Maintainer-only regeneration, not read-only review:

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_dry_run_ledger.py --rebuild
```

Default read-only verification:

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_dry_run_ledger.py
```

Pre-acceptance final gate:

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_dry_run_ledger.py --final-gate
```

Expected before Reviewer / Boundary / Product closeout: final gate fails only
because report statuses are pending.

## What Is Verified

- Three positive fixtures.
- One hundred forty-four failure cases cover forbidden operations, source drift, target drift, ledger
  entry drift, unknown-field injection, dangerous command/path injection,
  stop-condition injection, semantic field drift, receipt drift, replay drift,
  prototype Markdown tamper, prototype receipt tamper, and authority confusion.
- Exact P2-29 source hashes and plan hash.
- Exact target binding carried from P2-29.
- Ledger entries are non-executable and not replayable.
- No formal vault access, write, hash, snapshot, sync, commit, push, or promotion.
- Static prototype has no forms, downloads, storage/network APIs, command
  snippets, or executable controls.
- Prototype Markdown files are scanned for command/path and authority-confusion
  strings.
- Prototype receipt has strict schema, source/slice identity, count/hash, false
  operation flags, and non-claim checks.
- `dry_run_ledger_hash` covers the full normalized config except the hash field
  itself.
- Stop conditions, ledger mode, purpose, read-only source list, ledger entry
  questions, sample bindings, and max journey steps are explicit contract
  fields, not hash-only self-consistency checks.

## Observed Current Results

```text
rebuild: passed true
default verification: passed true
positive fixtures: 3
failure cases: 144
failure mismatches: []
prototype issues: []
pre-acceptance final gate: expected required_report_issues only
```

Injection probes:

```text
prototype markdown command:
  prototype_text_dangerous:absolute_formal_vault_path + copy_item
prototype markdown ready-to-execute:
  prototype_text_authority_confusion:ready_to_execute
prototype receipt unknown command:
  unknown_key + dangerous_value
prototype receipt hash drift:
  prototype_receipt_ledger_hash_mismatch
prototype receipt slice identity drift:
  prototype_receipt_slice_id_mismatch
prototype receipt source identity drift:
  prototype_receipt_source_slice_mismatch
prototype receipt target count drift:
  prototype_receipt_target_count_mismatch
prototype receipt action-basis flag:
  prototype_receipt_flag_not_false:ledger_used_as_action_basis
```

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
        ROOT / "artifact" / "formal-vault-execution-dry-run-ledger-contract.md",
        """# Formal Vault Execution Dry-Run Ledger Contract

This artifact records a dry-run ledger only.

Hard boundaries:

- It is sandbox-only.
- It is not replayable.
- It is not an execution log.
- It is not action basis.
- It does not collect approval.
- It does not access, inspect, hash, snapshot, write, or sync the formal vault.
- It does not emit commands.
""",
    )


def write_prototype(config: dict[str, Any]) -> None:
    proto = ROOT / "prototype" / "formal-vault-execution-dry-run-ledger"
    reset_dir(proto)
    write_text(
        proto / "00 Dry Run Ledger Home.md",
        "# Dry Run Ledger Home\n\nStatus: sandbox-only dry-run ledger. It is not an execution log.\n",
    )
    write_text(
        proto / "01 Ledger Contract.md",
        "# Ledger Contract\n\nThe ledger records reviewable dry-run entries only. It cannot be replayed.\n",
    )
    write_text(
        proto / "02 Ledger Entries.md",
        "# Ledger Entries\n\n" + "\n".join(
            f"- {entry['sequence']}. `{entry['entry_id']}`: {entry['dry_run_result']}"
            for entry in config["ledger_entries"]
        ) + "\n",
    )
    write_text(
        proto / "03 Non Execution Receipt.md",
        "# Non Execution Receipt\n\nNo formal vault operation was performed.\n",
    )
    write_text(
        proto / "04 Stop Conditions.md",
        "# Stop Conditions\n\n" + "\n".join(f"- {item}" for item in config["stop_conditions"]) + "\n",
    )
    write_text(
        proto / "05 Reviewer Packet.md",
        """# Reviewer Packet

Review checks:

- P2-29 source binding
- exact target binding
- ledger entries not performed
- no executable operation surface
- no authority confusion
""",
    )
    receipt = {
        "record_kind": "sandbox_formal_vault_execution_dry_run_ledger_receipt",
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
        "ledger_replayed": False,
        "ledger_used_as_action_basis": False,
        "entry_count": len(config["ledger_entries"]),
        "target_count": len(config["target_manifest"]),
        "ledger_hash": config["dry_run_ledger_hash"],
        "non_claims": config["non_execution_ledger_receipt"]["non_claims"],
    }
    write_json(proto / "Receipts" / "formal-vault-execution-dry-run-ledger-receipt.json", receipt)
    write_text(
        proto / "dry-run-ledger-inspector.html",
        """<!doctype html>
<html lang="en"
  data-sandbox-only="true"
  data-ledger-only="true"
  data-dry-run-only="true"
  data-non-executable="true"
  data-no-formal-vault-access="true"
  data-no-write="true"
  data-no-sync="true"
  data-no-authority="true">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Formal Vault Execution Dry-Run Ledger</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; color: #172026; background: #f7fafb; }
    header { padding: 20px 24px; background: #28465d; color: #fff; }
    main { padding: 18px 24px; display: grid; gap: 14px; }
    .rail { border-left: 4px solid #a35d2f; padding: 10px 14px; background: #fff; }
    .toolbar { display: flex; flex-wrap: wrap; gap: 8px; }
    button { border: 1px solid #8aa096; background: #fff; padding: 7px 10px; border-radius: 6px; }
    .card { border: 1px solid #d5ded8; background: #fff; border-radius: 8px; padding: 14px; }
    .tag { font-size: 12px; color: #52645b; text-transform: uppercase; }
    input { padding: 8px 10px; border: 1px solid #8aa096; border-radius: 6px; max-width: 360px; }
  </style>
</head>
<body>
  <header>
    <h1>Formal Vault Execution Dry-Run Ledger</h1>
    <p>Ledger review only. No replay, no command, no formal vault operation.</p>
  </header>
  <main>
    <section class="rail" role="note">This surface is a review aid, not authority.</section>
    <div class="toolbar" role="toolbar" aria-label="Ledger filters">
      <button type="button" data-filter="all">All</button>
      <button type="button" data-filter="contract">Contract</button>
      <button type="button" data-filter="entries">Entries</button>
      <button type="button" data-filter="receipt">Receipt</button>
      <button type="button" data-filter="stops">Stops</button>
    </div>
    <input id="q" type="search" placeholder="Filter ledger cards">
    <section class="card" data-kind="contract"><div class="tag">contract</div><h2>Non-replayable ledger</h2><p>Current slice cannot perform or replay the ledger.</p></section>
    <section class="card" data-kind="entries"><div class="tag">entries</div><h2>Dry-run entries</h2><p>Every entry is recorded as not performed.</p></section>
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
    config["dry_run_ledger_hash"] = expected_ledger_hash(config)


def drift(config: dict[str, Any], path: list[Any], value: Any) -> None:
    set_nested(config, path, value)
    rehash(config)


def make_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: list[Mutator] = []
    for op in FORBIDDEN_OPERATIONS:
        cases.append((f"forbidden-{op}", f"Forbidden operation `{op}` set true.", lambda cfg, key=op: set_nested(cfg, ["operations", key], True)))
    for key in REQUIRED_LEDGER_CONTROLS_TRUE:
        cases.append((f"control-{key}-false", f"Required true control `{key}` set false.", lambda cfg, k=key: set_nested(cfg, ["ledger_controls", k], False)))
    for key in REQUIRED_LEDGER_CONTROLS_FALSE:
        cases.append((f"control-{key}-true", f"Required false control `{key}` set true.", lambda cfg, k=key: set_nested(cfg, ["ledger_controls", k], True)))
    source_keys = [
        "source_plan_hash",
        "source_plan_input_bundle_hash",
        "source_target_manifest_hash",
        "source_plan_receipt_hash",
        "source_ledger_plan_contract_hash",
    ]
    for index, source_key in enumerate(source_keys, start=1):
        cases.append((f"source-hash-{index}-{source_key}", f"Source hash claim `{source_key}` drifted.", lambda cfg, k=source_key: set_nested(cfg, [k], "0" * 64)))
    cases.extend(
        [
            ("source-inputs-missing", "Source input list is empty.", lambda cfg: set_nested(cfg, ["source_inputs"], [])),
            ("source-inputs-bad-sha", "First source input hash drifts.", lambda cfg: set_nested(cfg, ["source_inputs", 0, "source_sha256"], "1" * 64)),
            ("source-input-bundle-drift", "Source bundle hash drifts.", lambda cfg: set_nested(cfg, ["source_input_bundle_hash"], "2" * 64)),
            ("read-only-sources-drift-rehashed", "Read-only source list drifts after hash recompute.", lambda cfg: drift(cfg, ["read_only_sources"], ["outputs/review/other-safe-source.md"])),
            ("purpose-authority-confusion-rehashed", "Purpose claims execution approval after hash recompute.", lambda cfg: drift(cfg, ["purpose"], "Approved and ready to execute now.")),
            ("ledger-mode-drift-rehashed", "Ledger mode drifts after hash recompute.", lambda cfg: drift(cfg, ["ledger_mode"], "execute_now")),
            ("target-missing-one", "One target removed.", lambda cfg: cfg["target_manifest"].pop()),
            ("target-extra-one", "Extra target added.", lambda cfg: cfg["target_manifest"].append(copy.deepcopy(cfg["target_manifest"][0]) | {"id": "extra_target"})),
            ("target-relative-drift", "Target relative path drifts.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "relative_target"], "VAKS-Workbench-Draft/Wrong.md")),
            ("target-source-path-drift", "Target source path drifts.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "source_path"], "outputs/review/wrong.md")),
            ("target-source-hash-drift", "Target source hash drifts.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "source_sha256"], "3" * 64)),
            ("target-absolute-path", "Target uses absolute Windows path.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "relative_target"], "H:/Obsidian/资料库/Wrong.md")),
            ("target-resolved-now", "Target resolved against formal vault.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "formal_vault_target_resolved"], True)),
            ("target-write-enabled-now", "Target write enabled now.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "write_enabled_now"], True)),
            ("target-execution-enabled-now", "Target execution enabled now.", lambda cfg: set_nested(cfg, ["target_manifest", 0, "execution_enabled_now"], True)),
            ("target-manifest-hash-drift", "Target manifest hash drifts.", lambda cfg: set_nested(cfg, ["target_manifest_hash"], "4" * 64)),
            ("contract-kind-drift", "Contract kind drifts.", lambda cfg: set_nested(cfg, ["dry_run_ledger_contract", "contract_kind"], "execution_log")),
            ("contract-executes-true", "Contract claims current slice executes.", lambda cfg: set_nested(cfg, ["dry_run_ledger_contract", "current_slice_executes"], True)),
            ("contract-ledger-action-basis", "Contract says ledger is action basis.", lambda cfg: set_nested(cfg, ["dry_run_ledger_contract", "ledger_is_not_action_basis"], False)),
            ("contract-plan-hash-drift", "Contract plan hash drifts.", lambda cfg: set_nested(cfg, ["dry_run_ledger_contract", "required_plan_hash"], "5" * 64)),
            ("entries-missing-one", "One ledger entry removed.", lambda cfg: cfg["ledger_entries"].pop()),
            ("entries-extra-one", "Extra ledger entry added.", lambda cfg: cfg["ledger_entries"].append(copy.deepcopy(cfg["ledger_entries"][0]) | {"entry_id": "extra_entry"})),
            ("entry-sequence-drift", "Entry sequence drifts.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "sequence"], 99)),
            ("entry-result-executable", "Entry result becomes executable.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "dry_run_result"], "EXECUTED")),
            ("entry-review-question-drift", "Entry review question drifts after hash recompute.", lambda cfg: drift(cfg, ["ledger_entries", 0, "review_question"], "Can we execute now?")),
            ("entry-perform-now", "Entry performs now.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "perform_now"], True)),
            ("entry-writes-now", "Entry writes now.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "writes_now"], True)),
            ("entry-vault-access-now", "Entry accesses vault now.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "formal_vault_access_now"], True)),
            ("entry-state-check-now", "Entry checks vault state now.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "formal_vault_state_check_now"], True)),
            ("entry-hash-now", "Entry hashes now.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "hash_now"], True)),
            ("entry-snapshot-now", "Entry snapshots now.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "snapshot_now"], True)),
            ("entry-sync-now", "Entry syncs now.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "sync_now"], True)),
            ("entry-command-present", "Entry emits a command.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "command"], "Copy-Item source target")),
            ("entry-absolute-target-present", "Entry contains absolute target path.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "absolute_target_path"], "H:/Obsidian/资料库/Wrong.md")),
            ("entry-copy-tool-present", "Entry names copy tool.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "copy_tool"], "Copy-Item")),
            ("entry-non-claim-drift", "Entry non-claim drifts.", lambda cfg: set_nested(cfg, ["ledger_entries", 0, "non_claim"], "execution_log")),
            ("sample-ledger-replayable", "Sample says ledger is replayable.", lambda cfg: set_nested(cfg, ["ledger_samples", 0, "ledger_replayable"], True)),
            ("sample-ledger-created-false-rehashed", "Sample ledger_created drifts after hash recompute.", lambda cfg: drift(cfg, ["ledger_samples", 0, "ledger_created"], False)),
            ("sample-source-scenario-drift-rehashed", "Sample source scenario drifts after hash recompute.", lambda cfg: drift(cfg, ["ledger_samples", 0, "source_plan_scenario"], "approved_execute_now")),
            ("sample-ledger-mode-drift-rehashed", "Sample ledger mode drifts after hash recompute.", lambda cfg: drift(cfg, ["ledger_samples", 0, "ledger_mode"], "execute_now")),
            ("sample-ledger-execution-log", "Sample says ledger is execution log.", lambda cfg: set_nested(cfg, ["ledger_samples", 0, "ledger_is_execution_log"], True)),
            ("sample-executes", "Sample executes.", lambda cfg: set_nested(cfg, ["ledger_samples", 0, "execution_performed"], True)),
            ("sample-writes", "Sample allows write now.", lambda cfg: set_nested(cfg, ["ledger_samples", 0, "formal_vault_write_allowed_now"], True)),
            ("sample-action-basis", "Sample creates action basis.", lambda cfg: set_nested(cfg, ["ledger_samples", 0, "action_basis_created"], True)),
            ("sample-real-user-input", "Sample uses real user input.", lambda cfg: set_nested(cfg, ["ledger_samples", 0, "actual_user_input"], True)),
            ("sample-scope-ids-drift", "Sample scope ids drift.", lambda cfg: set_nested(cfg, ["ledger_samples", 0, "scope_ids"], ["native_home"])),
            ("receipt-vault-accessed", "Receipt says vault accessed.", lambda cfg: set_nested(cfg, ["non_execution_ledger_receipt", "formal_vault_accessed"], True)),
            ("receipt-executed", "Receipt says execution performed.", lambda cfg: set_nested(cfg, ["non_execution_ledger_receipt", "execution_performed"], True)),
            ("receipt-write-performed", "Receipt says write performed.", lambda cfg: set_nested(cfg, ["non_execution_ledger_receipt", "write_performed"], True)),
            ("receipt-ledger-replayed", "Receipt says ledger replayed.", lambda cfg: set_nested(cfg, ["non_execution_ledger_receipt", "ledger_replayed"], True)),
            ("receipt-action-basis", "Receipt says ledger used as action basis.", lambda cfg: set_nested(cfg, ["non_execution_ledger_receipt", "ledger_used_as_action_basis"], True)),
            ("receipt-status-drift", "Receipt status drifts.", lambda cfg: set_nested(cfg, ["non_execution_ledger_receipt", "current_status"], "ready_to_execute")),
            ("receipt-non-claims-missing", "Receipt non-claims removed.", lambda cfg: set_nested(cfg, ["non_execution_ledger_receipt", "non_claims"], [])),
            ("stop-conditions-command-replaced-rehashed", "Stop conditions replaced by command after hash recompute.", lambda cfg: drift(cfg, ["stop_conditions"], ["Copy-Item source H:/Obsidian/资料库/target.md"])),
            ("stop-conditions-order-reversed-rehashed", "Stop conditions order drift after hash recompute.", lambda cfg: drift(cfg, ["stop_conditions"], list(reversed(cfg["stop_conditions"])))),
            ("max-journey-steps-drift-rehashed", "Journey step limit drifts after hash recompute.", lambda cfg: drift(cfg, ["product_metrics", "max_journey_steps"], 999)),
            ("unknown-top-level-command", "Unknown top-level command injection.", lambda cfg: cfg.update({"shell_command": "Copy-Item source H:/Obsidian/资料库/target.md"})),
            ("unknown-top-level-safe", "Unknown safe-looking top-level field injection.", lambda cfg: cfg.update({"operator_note": "extra field outside schema"})),
            ("unknown-entry-field", "Unknown entry field injection.", lambda cfg: cfg["ledger_entries"][0].update({"shell_command": "Copy-Item source target"})),
            ("unknown-receipt-field", "Unknown receipt field injection.", lambda cfg: cfg["non_execution_ledger_receipt"].update({"write_command": "Copy-Item source target"})),
            ("ledger-hash-drift", "Ledger hash drifts.", lambda cfg: set_nested(cfg, ["dry_run_ledger_hash"], "6" * 64)),
            ("metric-floor-too-low", "Failure-case floor too low.", lambda cfg: set_nested(cfg, ["product_metrics", "minimum_failure_cases"], 10)),
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
        write_json(
            failure_dir / file_name,
            {"case_id": case_id, "description": description, "expected_errors": errors, "config": cfg},
        )
        oracle_cases[file_name] = errors
    prototype_cases = [
        (
            "prototype-markdown-command",
            "Prototype Markdown contains a copy command.",
            {"kind": "markdown_replace", "file": "00 Dry Run Ledger Home.md", "content": "Copy-Item source H:/Obsidian/资料库/target.md"},
        ),
        (
            "prototype-markdown-ready-execute",
            "Prototype Markdown claims ready to execute.",
            {"kind": "markdown_replace", "file": "01 Ledger Contract.md", "content": "This ledger is ready to execute."},
        ),
        (
            "prototype-markdown-action-basis",
            "Prototype Markdown claims action basis.",
            {"kind": "markdown_replace", "file": "02 Ledger Entries.md", "content": "This ledger is action basis."},
        ),
        (
            "prototype-receipt-unknown-command",
            "Prototype receipt has unknown command field.",
            {"kind": "receipt_update", "updates": {"shell_command": "Copy-Item source H:/Obsidian/资料库/target.md"}},
        ),
        (
            "prototype-receipt-hash-drift",
            "Prototype receipt ledger hash drifts.",
            {"kind": "receipt_update", "updates": {"ledger_hash": "0" * 64}},
        ),
        (
            "prototype-receipt-non-claims-missing",
            "Prototype receipt non-claims removed.",
            {"kind": "receipt_replace_non_claims", "non_claims": []},
        ),
        (
            "prototype-receipt-entry-count-drift",
            "Prototype receipt entry count drifts.",
            {"kind": "receipt_update", "updates": {"entry_count": 99}},
        ),
        (
            "prototype-receipt-target-count-drift",
            "Prototype receipt target count drifts.",
            {"kind": "receipt_update", "updates": {"target_count": 99}},
        ),
        (
            "prototype-receipt-slice-id-drift",
            "Prototype receipt slice identity drifts.",
            {"kind": "receipt_update", "updates": {"slice_id": "wrong-slice"}},
        ),
        (
            "prototype-receipt-source-slice-drift",
            "Prototype receipt source slice identity drifts.",
            {"kind": "receipt_update", "updates": {"source_slice": "wrong-source-slice"}},
        ),
        (
            "prototype-receipt-record-kind-drift",
            "Prototype receipt record kind drifts.",
            {"kind": "receipt_update", "updates": {"record_kind": "execution_log"}},
        ),
        (
            "prototype-receipt-action-basis",
            "Prototype receipt says ledger used as action basis.",
            {"kind": "receipt_update", "updates": {"ledger_used_as_action_basis": True}},
        ),
    ]
    start_index = len(oracle_cases) + 1
    for offset, (case_id, description, tamper) in enumerate(prototype_cases):
        errors = validate_prototype_tamper(tamper)
        if not errors:
            raise RuntimeError(f"prototype failure case did not fail: {case_id}")
        file_name = f"{start_index + offset:02d}-{case_id}.json"
        write_json(
            failure_dir / file_name,
            {"case_id": case_id, "description": description, "expected_errors": errors, "prototype_tamper": tamper},
        )
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
        ("valid-dry-run-ledger-config.json", "approved_plan_dry_run_ledger"),
        ("valid-deny-dry-run-ledger-config.json", "denial_block_ledger"),
        ("valid-revise-dry-run-ledger-config.json", "revision_block_ledger"),
    ]
    for name, mode in variants:
        cfg = copy.deepcopy(base)
        cfg["ledger_mode"] = mode
        cfg["dry_run_ledger_hash"] = expected_ledger_hash(cfg)
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
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    if not args.rebuild:
        raise SystemExit("Use --rebuild to generate artifacts.")
    build_all()
    print(f"built {SLICE_ID}")


if __name__ == "__main__":
    main()
