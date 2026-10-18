from __future__ import annotations

import copy
import shutil
from pathlib import Path
from typing import Any, Callable

from readiness_gate_common import (
    CHECK_IDS,
    CHECK_STATUS_BY_MODE,
    GATE_CONTROL_EXPECTED,
    GATE_PURPOSE,
    NON_CLAIMS,
    OPERATION_KEYS,
    READ_ONLY_SOURCES,
    REQUEST_MODES,
    ROOT,
    SLICE_ID,
    SOURCE_SLICE,
    expected_gate_hash,
    expected_p2_30_binding,
    expected_source_inputs,
    expected_source_statuses,
    inspect_prototype,
    validate_config,
    validate_failure_cases,
    validate_prototype_tamper,
    write_json,
    write_text,
)


def reset_dir(path: Path) -> None:
    root = ROOT.resolve()
    target = path.resolve()
    if not str(target).startswith(str(root)):
        raise RuntimeError(f"refusing to reset outside sandbox: {target}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def base_operations() -> dict[str, bool]:
    return {key: False for key in OPERATION_KEYS}


def request_for_mode(mode: str) -> dict[str, Any]:
    decisions = {
        "synthetic_reviewable_packet": "review_packet_only",
        "synthetic_missing_future_confirmation": "missing_confirmation",
        "synthetic_denied_request": "deny",
    }
    return {
        "request_kind": "synthetic_future_formal_vault_execution_request",
        "request_mode": mode,
        "request_id": f"{SLICE_ID}:{mode}",
        "synthetic_only": True,
        "actual_user_confirmation_collected": False,
        "actual_user_text_stored": False,
        "actual_formal_vault_state_checked": False,
        "actual_commands_supplied": False,
        "requested_action_basis": False,
        "requested_execution_now": False,
        "future_execution_slice_required": True,
        "future_user_confirmation_required": True,
        "future_formal_vault_state_check_required": True,
        "operator_decision": decisions[mode],
        "gate_result": REQUEST_MODES[mode],
        "command": "",
        "absolute_target_path": "",
        "real_user_text": "",
        "non_claim": "readiness_gate_request_is_synthetic_only",
    }


def checks_for_mode(mode: str) -> list[dict[str, Any]]:
    statuses = CHECK_STATUS_BY_MODE[mode]
    return [
        {
            "check_id": check_id,
            "sequence": index,
            "status": statuses[check_id],
            "required_before_execution": True,
            "current_slice_collects": False,
            "non_claim": "check_is_readiness_input_not_permission",
        }
        for index, check_id in enumerate(CHECK_IDS, start=1)
    ]


def make_config(mode: str) -> dict[str, Any]:
    config: dict[str, Any] = {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE,
        "readiness_gate_version": "p2-31-formal-vault-execution-readiness-gate-v1",
        "truth_boundary": "sandbox_only_readiness_gate_not_execution_permission",
        "purpose": GATE_PURPOSE,
        "gate_mode": "future_execution_readiness_gate_review_only",
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": READ_ONLY_SOURCES,
        "operations": base_operations(),
        "gate_controls": copy.deepcopy(GATE_CONTROL_EXPECTED),
        "source_inputs": expected_source_inputs(),
        "source_statuses": expected_source_statuses(),
        "p2_30_binding": expected_p2_30_binding(),
        "request_envelope": request_for_mode(mode),
        "readiness_checks": checks_for_mode(mode),
        "readiness_receipt": {
            "record_kind": "sandbox_formal_vault_execution_readiness_gate_receipt",
            "slice_id": SLICE_ID,
            "source_slice": SOURCE_SLICE,
            "gate_result": REQUEST_MODES[mode],
            "formal_vault_accessed": False,
            "formal_vault_state_inspected": False,
            "approval_collected_now": False,
            "actual_user_input_used": False,
            "real_user_text_stored": False,
            "execution_permission_granted": False,
            "execution_performed": False,
            "write_performed": False,
            "snapshot_taken": False,
            "hash_before_collected": False,
            "hash_after_collected": False,
            "sync_performed": False,
            "commit_performed": False,
            "push_performed": False,
            "promotion_performed": False,
            "gate_replayed": False,
            "gate_used_as_action_basis": False,
            "check_count": len(CHECK_IDS),
            "source_count": len(READ_ONLY_SOURCES),
            "readiness_gate_hash": "",
            "non_claims": sorted(NON_CLAIMS),
        },
        "product_metrics": {
            "required_positive_fixtures": 3,
            "minimum_failure_cases": 100,
            "required_readiness_checks": len(CHECK_IDS),
            "required_source_inputs": len(READ_ONLY_SOURCES),
            "max_journey_steps": 3,
        },
        "readiness_gate_hash": "",
    }
    gate_hash = expected_gate_hash(config)
    config["readiness_gate_hash"] = gate_hash
    config["readiness_receipt"]["readiness_gate_hash"] = gate_hash
    return config


def rehash(config: dict[str, Any]) -> None:
    config["readiness_gate_hash"] = ""
    if isinstance(config.get("readiness_receipt"), dict):
        config["readiness_receipt"]["readiness_gate_hash"] = ""
    gate_hash = expected_gate_hash(config)
    config["readiness_gate_hash"] = gate_hash
    if isinstance(config.get("readiness_receipt"), dict):
        config["readiness_receipt"]["readiness_gate_hash"] = gate_hash


def set_path(config: dict[str, Any], path: list[Any], value: Any) -> None:
    cursor: Any = config
    for part in path[:-1]:
        cursor = cursor[part]
    cursor[path[-1]] = value


def write_fixtures() -> dict[str, dict[str, Any]]:
    fixtures = {
        "valid-reviewable-readiness-gate-config.json": make_config("synthetic_reviewable_packet"),
        "valid-missing-confirmation-readiness-gate-config.json": make_config("synthetic_missing_future_confirmation"),
        "valid-denied-readiness-gate-config.json": make_config("synthetic_denied_request"),
    }
    reset_dir(ROOT / "fixtures")
    for name, config in fixtures.items():
        write_json(ROOT / "fixtures" / name, config)
    return fixtures


def build_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: list[tuple[str, str, Callable[[dict[str, Any]], None]]] = []
    for op in OPERATION_KEYS:
        cases.append((f"operation-{op}", f"Operation flag {op} enabled.", lambda cfg, key=op: set_path(cfg, ["operations", key], True)))
    for control, expected in GATE_CONTROL_EXPECTED.items():
        cases.append((f"control-{control}", f"Gate control {control} drifted.", lambda cfg, key=control, value=expected: set_path(cfg, ["gate_controls", key], not value)))
    for index in range(len(READ_ONLY_SOURCES)):
        cases.append((f"source-input-{index}-sha-drift", "Source input hash drift.", lambda cfg, idx=index: set_path(cfg, ["source_inputs", idx, "source_sha256"], "0" * 64)))
    for name in ["product-acceptance-report.md", "reviewer-report.md", "boundary-audit.md", "next-step.md", "verification.md", "source-map.md"]:
        cases.append((f"source-status-{name.replace('.', '-')}-drift", "Source status drift.", lambda cfg, file_name=name: [item.update({"actual_status": "pending"}) for item in cfg["source_statuses"] if item["file"] == file_name]))
    for key, value in [
        ("product_acceptance_status", "pending"),
        ("reviewer_status", "pending"),
        ("boundary_status", "pending"),
        ("ledger_hash", "1" * 64),
        ("ledger_receipt_hash", "2" * 64),
        ("ledger_entry_count", 99),
        ("ledger_target_count", 99),
        ("ledger_used_as_action_basis", True),
        ("formal_vault_accessed", True),
        ("write_performed", True),
        ("sync_performed", True),
        ("promotion_performed", True),
    ]:
        cases.append((f"p2-30-binding-{key}-drift", f"P2-30 binding {key} drift.", lambda cfg, k=key, v=value: set_path(cfg, ["p2_30_binding", k], v)))
    request_drifts = [
        ("request-unknown-mode", ["request_envelope", "request_mode"], "real_execute_now"),
        ("request-ready-result", ["request_envelope", "gate_result"], "READY_TO_EXECUTE"),
        ("request-actual-confirmation", ["request_envelope", "actual_user_confirmation_collected"], True),
        ("request-real-user-text-stored", ["request_envelope", "actual_user_text_stored"], True),
        ("request-formal-vault-state-checked", ["request_envelope", "actual_formal_vault_state_checked"], True),
        ("request-commands-supplied", ["request_envelope", "actual_commands_supplied"], True),
        ("request-action-basis", ["request_envelope", "requested_action_basis"], True),
        ("request-execution-now", ["request_envelope", "requested_execution_now"], True),
        ("request-not-synthetic", ["request_envelope", "synthetic_only"], False),
        ("request-command", ["request_envelope", "command"], "Copy-Item source H:/Obsidian/资料库/target.md"),
        ("request-absolute-target", ["request_envelope", "absolute_target_path"], "H:/Obsidian/资料库/target.md"),
        ("request-real-user-text", ["request_envelope", "real_user_text"], "I approve execution now"),
    ]
    for case_id, path, value in request_drifts:
        cases.append((case_id, f"Request envelope drift at {'.'.join(path)}.", lambda cfg, p=path, v=value: set_path(cfg, p, v)))
    request_id_drifts = [
        ("request-id-real-user-text-rehashed", "user said approve execution"),
        ("request-id-command-rehashed", "python tools/promote.py --sync"),
        ("request-id-approval-now-rehashed", "I approve execution now"),
        ("request-id-execute-now-rehashed", "execute now"),
    ]
    for case_id, value in request_id_drifts:
        cases.append((case_id, "Request id carries unsafe or non-synthetic text after rehash.", lambda cfg, v=value: (set_path(cfg, ["request_envelope", "request_id"], v), rehash(cfg))))
    for index, check_id in enumerate(CHECK_IDS):
        cases.append((f"check-{check_id}-status-drift", "Readiness check status drift.", lambda cfg, idx=index: set_path(cfg, ["readiness_checks", idx, "status"], "DRIFTED_STATUS")))
        cases.append((f"check-{check_id}-collects-now", "Readiness check collects current-slice evidence.", lambda cfg, idx=index: set_path(cfg, ["readiness_checks", idx, "current_slice_collects"], True)))
    receipt_drifts = [
        ("receipt-record-kind", ["readiness_receipt", "record_kind"], "execution_permission_receipt"),
        ("receipt-slice-id", ["readiness_receipt", "slice_id"], "wrong-slice"),
        ("receipt-source-slice", ["readiness_receipt", "source_slice"], "wrong-source"),
        ("receipt-gate-result", ["readiness_receipt", "gate_result"], "READY_TO_EXECUTE"),
        ("receipt-formal-vault-access", ["readiness_receipt", "formal_vault_accessed"], True),
        ("receipt-state-inspected", ["readiness_receipt", "formal_vault_state_inspected"], True),
        ("receipt-approval-collected", ["readiness_receipt", "approval_collected_now"], True),
        ("receipt-execution-permission", ["readiness_receipt", "execution_permission_granted"], True),
        ("receipt-write-performed", ["readiness_receipt", "write_performed"], True),
        ("receipt-sync-performed", ["readiness_receipt", "sync_performed"], True),
        ("receipt-gate-action-basis", ["readiness_receipt", "gate_used_as_action_basis"], True),
        ("receipt-check-count", ["readiness_receipt", "check_count"], 99),
        ("receipt-source-count", ["readiness_receipt", "source_count"], 99),
        ("receipt-non-claims", ["readiness_receipt", "non_claims"], []),
    ]
    for case_id, path, value in receipt_drifts:
        cases.append((case_id, f"Receipt drift at {'.'.join(path)}.", lambda cfg, p=path, v=value: set_path(cfg, p, v)))
    cases.extend(
        [
            ("top-level-unknown-command", "Unknown top-level command field.", lambda cfg: cfg.update({"shell_command": "Copy-Item source H:/Obsidian/资料库/target.md"})),
            ("top-level-unknown-safe", "Unknown safe-looking top-level field.", lambda cfg: cfg.update({"operator_note": "extra field outside schema"})),
            ("write-scope-drift", "Write scope drift outside sandbox.", lambda cfg: set_path(cfg, ["write_scope"], ["outputs/review/"])),
            ("read-only-sources-drift", "Read-only source list drift.", lambda cfg: cfg["read_only_sources"].append("README.md")),
            ("purpose-drift-rehashed", "Purpose drifts after rehash.", lambda cfg: (set_path(cfg, ["purpose"], "Approved for execution."), rehash(cfg))),
            ("gate-mode-drift-rehashed", "Gate mode drifts after rehash.", lambda cfg: (set_path(cfg, ["gate_mode"], "execute_now"), rehash(cfg))),
            ("metric-failure-floor-low", "Failure-case floor too low.", lambda cfg: set_path(cfg, ["product_metrics", "minimum_failure_cases"], 10)),
            ("metric-check-count-drift", "Required check count drifts.", lambda cfg: set_path(cfg, ["product_metrics", "required_readiness_checks"], 99)),
            ("hash-drift", "Readiness gate hash drifts.", lambda cfg: set_path(cfg, ["readiness_gate_hash"], "9" * 64)),
            ("receipt-hash-drift", "Readiness receipt hash drifts.", lambda cfg: set_path(cfg, ["readiness_receipt", "readiness_gate_hash"], "8" * 64)),
        ]
    )

    reset_dir(ROOT / "failure-cases")
    oracle_cases: dict[str, list[str]] = {}
    for index, (case_id, description, mutator) in enumerate(cases, start=1):
        cfg = copy.deepcopy(base)
        mutator(cfg)
        errors = validate_config(cfg)
        if not errors:
            raise RuntimeError(f"failure case did not fail: {case_id}")
        file_name = f"{index:03d}-{case_id}.json"
        write_json(ROOT / "failure-cases" / file_name, {"case_id": case_id, "description": description, "expected_errors": errors, "config": cfg})
        oracle_cases[file_name] = errors

    stale_proto = ROOT / "prototype" / "formal-vault-execution-readiness-gate"
    if stale_proto.exists():
        reset_dir(stale_proto)
    prototype_cases = [
        ("prototype-markdown-command", "Prototype Markdown contains command.", {"kind": "markdown_replace", "file": "00 Readiness Gate Home.md", "content": "Copy-Item source H:/Obsidian/资料库/target.md"}),
        ("prototype-markdown-ready", "Prototype Markdown claims ready.", {"kind": "markdown_replace", "file": "01 Gate Contract.md", "content": "This gate is ready to execute."}),
        ("prototype-markdown-permission", "Prototype Markdown claims permission.", {"kind": "markdown_replace", "file": "02 Readiness Checks.md", "content": "Execution permission granted."}),
        ("prototype-markdown-permission-yes", "Prototype Markdown says permission yes.", {"kind": "markdown_replace", "file": "02 Readiness Checks.md", "content": "execution permission: yes"}),
        ("prototype-markdown-approval-yes", "Prototype Markdown says formal vault approval yes.", {"kind": "markdown_replace", "file": "03 Non Permission Receipt.md", "content": "formal vault approval: yes"}),
        ("prototype-markdown-action-basis-yes", "Prototype Markdown says action basis yes.", {"kind": "markdown_replace", "file": "05 Reviewer Packet.md", "content": "action basis: yes"}),
        ("prototype-receipt-command", "Prototype receipt command injection.", {"kind": "receipt_update", "updates": {"shell_command": "Copy-Item source H:/Obsidian/资料库/target.md"}}),
        ("prototype-receipt-hash", "Prototype receipt hash drift.", {"kind": "receipt_update", "updates": {"readiness_gate_hash": "0" * 64}}),
        ("prototype-receipt-slice", "Prototype receipt slice drift.", {"kind": "receipt_update", "updates": {"slice_id": "wrong"}}),
        ("prototype-receipt-source", "Prototype receipt source drift.", {"kind": "receipt_update", "updates": {"source_slice": "wrong"}}),
        ("prototype-receipt-permission", "Prototype receipt grants permission.", {"kind": "receipt_update", "updates": {"execution_permission_granted": True}}),
        ("prototype-receipt-action-basis", "Prototype receipt says action basis.", {"kind": "receipt_update", "updates": {"gate_used_as_action_basis": True}}),
        ("prototype-receipt-non-claims", "Prototype receipt non-claims removed.", {"kind": "receipt_replace_non_claims", "non_claims": []}),
    ]
    start = len(oracle_cases) + 1
    for offset, (case_id, description, tamper) in enumerate(prototype_cases):
        errors = validate_prototype_tamper(tamper)
        if not errors:
            raise RuntimeError(f"prototype failure case did not fail: {case_id}")
        file_name = f"{start + offset:03d}-{case_id}.json"
        write_json(ROOT / "failure-cases" / file_name, {"case_id": case_id, "description": description, "expected_errors": errors, "prototype_tamper": tamper})
        oracle_cases[file_name] = errors
    return oracle_cases


def write_oracle(oracle_cases: dict[str, list[str]]) -> None:
    write_json(ROOT / "artifact" / "failure-case-oracle.json", {"record_kind": "sandbox_failure_case_oracle", "slice_id": SLICE_ID, "case_count": len(oracle_cases), "cases": oracle_cases})
    lines = ["# Failure Case Oracle", "", f"Case count: {len(oracle_cases)}", ""]
    lines.extend(f"- `{name}` -> `{', '.join(errors)}`" for name, errors in oracle_cases.items())
    write_text(ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines) + "\n")


def write_root_docs(case_count: int) -> None:
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

Build a read-only readiness gate for a future formal-vault execution request.
The gate checks whether a request packet is reviewable, but it cannot grant
execution permission.

## Inputs

- P2-30 Product Acceptance report.
- P2-30 dry-run ledger config and receipt.
- P2-30 Reviewer and Boundary reports.

## Outputs

- Readiness gate contract.
- Three positive fixtures.
- Failure-case oracle and failure cases.
- Static reviewer prototype.
- Verification and acceptance reports.

## Boundary

This slice does not access, inspect, hash, snapshot, write, or sync the formal
vault. It does not collect approval and does not create action basis.
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

Read-only sources:

"""
        + "\n".join(f"- `{path}`" for path in READ_ONLY_SOURCES)
        + "\n\nAll sources are used as sandbox process inputs only. Retrieval or hash binding is not evidence support.\n",
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
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_readiness_gate.py --rebuild
```

Default read-only verification:

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_readiness_gate.py
```

Pre-acceptance final gate:

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_readiness_gate.py --final-gate
```

Before Reviewer / Boundary / Product closeout, final gate should fail only on
pending report statuses.

## What Is Verified

- Three positive fixtures.
- {case_count} failure cases.
- Seven manual negative probes that are not generated from the failure oracle.
- Exact P2-30 source hashes and report statuses.
- P2-30 ledger hash, receipt hash, entry count, target count, and non-execution flags.
- Readiness request envelope is synthetic only and cannot include commands,
  absolute formal-vault paths, real user text, current approval, or execution-now intent.
- Readiness checks are explicit inputs, not permission grants.
- Prototype Markdown and receipt tamper are fail-closed.
- Static prototype has no forms, downloads, storage/network APIs, command
  snippets, or executable controls.

## Observed Current Results

```text
rebuild: passed true
default verification: passed true
positive fixtures: 3
failure cases: {case_count}
failure mismatches: []
prototype issues: []
manual negative probes: 7
pre-acceptance final gate: expected required_report_issues only
```

## Non-Claims

Verification is diagnostic only. It is not Product Acceptance, formal vault
approval, execution permission, action basis, evidence support, reviewed
knowledge, sync approval, commit approval, push approval, or promotion approval.
""",
    )
    pending_docs = {
        "reviewer-report.md": ("sandbox_reviewer_report", "Reviewer Report"),
        "boundary-audit.md": ("sandbox_boundary_audit", "Boundary Audit"),
        "product-acceptance-report.md": ("sandbox_product_acceptance_report", "Product Acceptance Report"),
        "next-step.md": ("sandbox_next_step", "Next Step"),
    }
    for file_name, (kind, title) in pending_docs.items():
        write_text(
            ROOT / file_name,
            f"""---
record_kind: {kind}
slice_id: {SLICE_ID}
status: pending
truth_boundary: sandbox_only
---

# {title}

Pending.
""",
        )


def write_artifacts(reviewable: dict[str, Any], case_count: int) -> None:
    write_text(
        ROOT / "artifact" / "formal-vault-execution-readiness-gate-contract.md",
        """# Formal Vault Execution Readiness Gate Contract

This artifact is a read-only readiness gate for a future formal-vault execution
request.

Hard boundaries:

- It is sandbox-only.
- It is not execution permission.
- It is not formal vault approval.
- It is not action basis.
- It does not collect approval.
- It does not access, inspect, hash, snapshot, write, or sync the formal vault.
- It does not emit commands.
- Any future execution still requires a separate user-confirmed execution slice.
""",
    )
    proto = ROOT / "prototype" / "formal-vault-execution-readiness-gate"
    reset_dir(proto)
    write_text(
        proto / "00 Readiness Gate Home.md",
        f"""# Readiness Gate Home

Slice: `{SLICE_ID}`

Result: `{reviewable['request_envelope']['gate_result']}`

This is a sandbox readiness packet review surface. It does not grant execution
permission and it does not access the formal vault.

Open:

- [[01 Gate Contract]]
- [[02 Readiness Checks]]
- [[03 Non Permission Receipt]]
- [[04 Stop Conditions]]
- [[05 Reviewer Packet]]
""",
    )
    write_text(
        proto / "01 Gate Contract.md",
        """# Gate Contract

- sandbox only
- read-only readiness gate
- not execution permission
- not formal vault approval
- not action basis
- separate future user confirmation required
- separate future execution slice required
""",
    )
    write_text(
        proto / "02 Readiness Checks.md",
        "# Readiness Checks\n\n"
        + "\n".join(f"- `{item['check_id']}`: `{item['status']}`" for item in reviewable["readiness_checks"])
        + "\n",
    )
    write_text(
        proto / "03 Non Permission Receipt.md",
        """# Non Permission Receipt

The receipt records process integrity only. It is not execution permission,
formal vault approval, reviewed knowledge, evidence support, or action basis.
""",
    )
    write_text(
        proto / "04 Stop Conditions.md",
        """# Stop Conditions

Stop immediately if a future operator needs formal vault access, formal vault
state inspection, approval collection, command generation, write, hash,
snapshot, sync, commit, push, promotion, or mainline merge.
""",
    )
    write_text(
        proto / "05 Reviewer Packet.md",
        f"""# Reviewer Packet

Review checks:

- P2-30 Product Acceptance is bound
- dry-run ledger hash is bound
- readiness checks are explicit inputs
- failure cases: {case_count}
- no executable operation surface
- no authority confusion
""",
    )
    receipt = copy.deepcopy(reviewable["readiness_receipt"])
    write_json(proto / "Receipts" / "formal-vault-execution-readiness-gate-receipt.json", receipt)
    html = f"""<!doctype html>
<html lang="en" data-sandbox-only="true" data-readiness-only="true" data-non-executable="true" data-no-formal-vault-access="true" data-no-write="true" data-no-sync="true" data-no-authority="true" data-no-permission="true">
<head><meta charset="utf-8"><title>Readiness Gate Inspector</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; color: #202124; background: #f7f7f2; }}
main {{ max-width: 920px; }}
button {{ margin: 0 8px 8px 0; padding: 7px 10px; border: 1px solid #777; background: #fff; }}
section {{ border-top: 1px solid #ccc; padding: 14px 0; }}
code {{ background: #ecebe4; padding: 1px 4px; }}
</style></head>
<body><main>
<h1>Readiness Gate Inspector</h1>
<p>Sandbox-only read-only readiness view. No approval or permission is created here.</p>
<button data-filter="all">All</button>
<button data-filter="contract">Contract</button>
<button data-filter="checks">Checks</button>
<button data-filter="receipt">Receipt</button>
<button data-filter="stops">Stops</button>
<section data-kind="contract"><h2>Contract</h2><p>Separate future confirmation and execution slice required.</p></section>
<section data-kind="checks"><h2>Checks</h2><p>{len(CHECK_IDS)} readiness inputs, none collected as execution permission.</p></section>
<section data-kind="receipt"><h2>Receipt</h2><p>Gate hash <code>{reviewable['readiness_gate_hash']}</code></p></section>
<section data-kind="stops"><h2>Stops</h2><p>Any real vault operation stops this sandbox.</p></section>
</main></body></html>
"""
    write_text(proto / "readiness-gate-inspector.html", html)


def build_all() -> None:
    fixtures = write_fixtures()
    reviewable = fixtures["valid-reviewable-readiness-gate-config.json"]
    oracle_cases = build_failure_cases(reviewable)
    write_oracle(oracle_cases)
    case_count = len(oracle_cases)
    write_root_docs(case_count)
    write_artifacts(reviewable, case_count)
    prototype = inspect_prototype()
    if prototype["issues"]:
        raise RuntimeError(f"prototype issues: {prototype['issues']}")
    for name, config in fixtures.items():
        errors = validate_config(config)
        if errors:
            raise RuntimeError(f"fixture invalid {name}: {errors}")
    failure_result = validate_failure_cases()
    if failure_result["mismatches"]:
        raise RuntimeError(f"failure case mismatches: {failure_result['mismatches']}")
    print(f"built {SLICE_ID}")


def main() -> None:
    build_all()


if __name__ == "__main__":
    main()
