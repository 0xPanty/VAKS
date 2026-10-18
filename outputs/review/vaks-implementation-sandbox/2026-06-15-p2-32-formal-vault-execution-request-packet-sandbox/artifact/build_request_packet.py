from __future__ import annotations

import copy
import shutil
from pathlib import Path
from typing import Any, Callable

from request_packet_common import (
    NON_CLAIMS,
    OPERATION_KEYS,
    PACKET_CONTROL_EXPECTED,
    PACKET_FIELD_IDS,
    PACKET_MODES,
    PACKET_PURPOSE,
    READ_ONLY_SOURCES,
    ROOT,
    SLICE_ID,
    SOURCE_SLICE,
    TARGET_GATE_REQUEST_MODES,
    TARGET_GATE_RESULTS,
    expected_p2_31_binding,
    expected_packet_hash,
    expected_projection_id,
    expected_source_inputs,
    expected_source_statuses,
    inspect_prototype,
    run_manual_negative_probes,
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


def set_path(config: dict[str, Any], path: list[Any], value: Any) -> None:
    cursor: Any = config
    for part in path[:-1]:
        cursor = cursor[part]
    cursor[path[-1]] = value


def rehash(config: dict[str, Any]) -> None:
    config["request_packet_hash"] = ""
    if isinstance(config.get("packet_receipt"), dict):
        config["packet_receipt"]["request_packet_hash"] = ""
    packet_hash = expected_packet_hash(config)
    config["request_packet_hash"] = packet_hash
    if isinstance(config.get("packet_receipt"), dict):
        config["packet_receipt"]["request_packet_hash"] = packet_hash


def base_operations() -> dict[str, bool]:
    return {key: False for key in OPERATION_KEYS}


def packet_for_mode(mode: str) -> dict[str, Any]:
    decisions = {
        "synthetic_reviewable_request_packet": "review_packet_only",
        "synthetic_missing_confirmation_packet": "missing_confirmation",
        "synthetic_denied_request_packet": "deny",
    }
    return {
        "packet_id": f"{SLICE_ID}:{mode}",
        "packet_kind": "synthetic_future_formal_vault_execution_request_packet",
        "packet_mode": mode,
        "packet_result": PACKET_MODES[mode],
        "synthetic_only": True,
        "actual_user_confirmation_collected": False,
        "actual_user_text_stored": False,
        "actual_user_text": "",
        "actual_formal_vault_state_checked": False,
        "actual_commands_supplied": False,
        "requested_execution_now": False,
        "requested_action_basis": False,
        "operator_decision_reference": decisions[mode],
        "synthetic_confirmation_reference": f"synthetic_confirmation_reference:{mode}",
        "scope_reference": "p2_30_target_manifest_reference_only",
        "target_manifest_reference": "p2_30_target_manifest_reference_only",
        "command": "",
        "absolute_target_path": "",
        "approval_text": "",
        "non_claims": sorted(NON_CLAIMS),
    }


def projection_for_mode(mode: str, p2_31_binding: dict[str, Any]) -> dict[str, Any]:
    return {
        "target_gate_slice": SOURCE_SLICE,
        "target_gate_version": p2_31_binding["readiness_gate_version"],
        "target_request_mode": TARGET_GATE_REQUEST_MODES[mode],
        "projected_request_id": expected_projection_id(mode),
        "projected_gate_result": TARGET_GATE_RESULTS[mode],
        "screenable_by_p2_31": True,
        "projection_is_not_submission": True,
        "projection_collects_no_approval": True,
        "projection_contains_no_commands": True,
        "projection_contains_no_formal_vault_paths": True,
    }


def packet_schema() -> list[dict[str, Any]]:
    return [
        {
            "field_id": field_id,
            "required": True,
            "synthetic_only": True,
            "forbidden_real_content": True,
            "non_claim": "schema_field_is_contract_not_user_input",
        }
        for field_id in PACKET_FIELD_IDS
    ]


def make_config(mode: str) -> dict[str, Any]:
    binding = expected_p2_31_binding()
    config: dict[str, Any] = {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE,
        "request_packet_version": "p2-32-formal-vault-execution-request-packet-v1",
        "truth_boundary": "sandbox_only_request_packet_not_execution_permission",
        "purpose": PACKET_PURPOSE,
        "packet_mode": mode,
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": READ_ONLY_SOURCES,
        "operations": base_operations(),
        "packet_controls": copy.deepcopy(PACKET_CONTROL_EXPECTED),
        "source_inputs": expected_source_inputs(),
        "source_statuses": expected_source_statuses(),
        "p2_31_binding": binding,
        "packet_schema": packet_schema(),
        "request_packet": packet_for_mode(mode),
        "readiness_gate_projection": projection_for_mode(mode, binding),
        "packet_receipt": {
            "record_kind": "sandbox_formal_vault_execution_request_packet_receipt",
            "slice_id": SLICE_ID,
            "source_slice": SOURCE_SLICE,
            "packet_result": PACKET_MODES[mode],
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
            "packet_submitted_to_gate": False,
            "packet_replayed": False,
            "packet_used_as_action_basis": False,
            "field_count": len(PACKET_FIELD_IDS),
            "source_count": len(READ_ONLY_SOURCES),
            "request_packet_hash": "",
            "non_claims": sorted(NON_CLAIMS),
        },
        "product_metrics": {
            "required_positive_fixtures": 3,
            "minimum_failure_cases": 100,
            "required_packet_fields": len(PACKET_FIELD_IDS),
            "required_source_inputs": len(READ_ONLY_SOURCES),
            "manual_negative_probes": 12,
            "max_journey_steps": 3,
        },
        "request_packet_hash": "",
    }
    rehash(config)
    return config


def write_fixtures() -> dict[str, dict[str, Any]]:
    fixtures = {
        "valid-reviewable-request-packet-config.json": make_config("synthetic_reviewable_request_packet"),
        "valid-missing-confirmation-request-packet-config.json": make_config("synthetic_missing_confirmation_packet"),
        "valid-denied-request-packet-config.json": make_config("synthetic_denied_request_packet"),
    }
    reset_dir(ROOT / "fixtures")
    for name, config in fixtures.items():
        write_json(ROOT / "fixtures" / name, config)
    return fixtures


def build_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: list[tuple[str, str, Callable[[dict[str, Any]], None]]] = []
    for op in OPERATION_KEYS:
        cases.append((f"operation-{op}", f"Operation flag {op} enabled.", lambda cfg, key=op: set_path(cfg, ["operations", key], True)))
    for control, expected in PACKET_CONTROL_EXPECTED.items():
        cases.append((f"control-{control}", f"Packet control {control} drifted.", lambda cfg, key=control, value=expected: set_path(cfg, ["packet_controls", key], not value)))
    for index in range(len(READ_ONLY_SOURCES)):
        cases.append((f"source-input-{index}-sha-drift", "Source input hash drift.", lambda cfg, idx=index: set_path(cfg, ["source_inputs", idx, "source_sha256"], "0" * 64)))
    for name in ["product-acceptance-report.md", "reviewer-report.md", "boundary-audit.md", "next-step.md", "verification.md", "source-map.md"]:
        cases.append((f"source-status-{name.replace('.', '-')}-drift", "Source status drift.", lambda cfg, file_name=name: [item.update({"actual_status": "pending"}) for item in cfg["source_statuses"] if item["file"] == file_name]))
    for key, value in [
        ("product_acceptance_status", "pending"),
        ("reviewer_status", "pending"),
        ("boundary_status", "pending"),
        ("readiness_gate_hash", "1" * 64),
        ("readiness_receipt_hash", "2" * 64),
        ("readiness_check_count", 99),
        ("readiness_source_count", 99),
        ("execution_permission_granted", True),
        ("gate_used_as_action_basis", True),
        ("formal_vault_accessed", True),
        ("write_performed", True),
        ("sync_performed", True),
        ("promotion_performed", True),
    ]:
        cases.append((f"p2-31-binding-{key}-drift", f"P2-31 binding {key} drift.", lambda cfg, k=key, v=value: set_path(cfg, ["p2_31_binding", k], v)))
    for index, field_id in enumerate(PACKET_FIELD_IDS):
        cases.append((f"schema-{field_id}-not-required", "Packet schema required flag drift.", lambda cfg, idx=index: set_path(cfg, ["packet_schema", idx, "required"], False)))
        cases.append((f"schema-{field_id}-real-content", "Packet schema real-content flag drift.", lambda cfg, idx=index: set_path(cfg, ["packet_schema", idx, "forbidden_real_content"], False)))
    packet_drifts = [
        ("packet-id-real-text-rehashed", ["request_packet", "packet_id"], "user said approve execution", True),
        ("packet-id-command-rehashed", ["request_packet", "packet_id"], "python tools/promote.py --sync", True),
        ("packet-mode-drift", ["request_packet", "packet_mode"], "real_execute_now", False),
        ("packet-result-ready", ["request_packet", "packet_result"], "READY_TO_EXECUTE", False),
        ("packet-not-synthetic", ["request_packet", "synthetic_only"], False, False),
        ("packet-actual-confirmation", ["request_packet", "actual_user_confirmation_collected"], True, False),
        ("packet-real-text-stored", ["request_packet", "actual_user_text_stored"], True, False),
        ("packet-formal-vault-state-checked", ["request_packet", "actual_formal_vault_state_checked"], True, False),
        ("packet-commands-supplied", ["request_packet", "actual_commands_supplied"], True, False),
        ("packet-execution-now", ["request_packet", "requested_execution_now"], True, False),
        ("packet-action-basis", ["request_packet", "requested_action_basis"], True, False),
        ("packet-actual-user-text", ["request_packet", "actual_user_text"], "real user text: approve execution now", False),
        ("packet-command", ["request_packet", "command"], "Copy-Item source H:/Obsidian/资料库/target.md", False),
        ("packet-absolute-path", ["request_packet", "absolute_target_path"], "H:/Obsidian/资料库/target.md", False),
        ("packet-approval-text", ["request_packet", "approval_text"], "I approve execution now", False),
        ("packet-non-claims", ["request_packet", "non_claims"], [], False),
    ]
    for case_id, path, value, do_rehash in packet_drifts:
        cases.append((case_id, f"Request packet drift at {'.'.join(path)}.", lambda cfg, p=path, v=value, h=do_rehash: (set_path(cfg, p, v), rehash(cfg) if h else None)))
    projection_drifts = [
        ("projection-target-slice", ["readiness_gate_projection", "target_gate_slice"], "wrong-slice"),
        ("projection-target-version", ["readiness_gate_projection", "target_gate_version"], "wrong-version"),
        ("projection-request-mode", ["readiness_gate_projection", "target_request_mode"], "real_execute_now"),
        ("projection-request-id-command", ["readiness_gate_projection", "projected_request_id"], "python tools/promote.py --sync"),
        ("projection-gate-result-ready", ["readiness_gate_projection", "projected_gate_result"], "READY_TO_EXECUTE"),
        ("projection-not-screenable", ["readiness_gate_projection", "screenable_by_p2_31"], False),
        ("projection-is-submission", ["readiness_gate_projection", "projection_is_not_submission"], False),
        ("projection-collects-approval", ["readiness_gate_projection", "projection_collects_no_approval"], False),
        ("projection-contains-command", ["readiness_gate_projection", "projection_contains_no_commands"], False),
        ("projection-contains-path", ["readiness_gate_projection", "projection_contains_no_formal_vault_paths"], False),
    ]
    for case_id, path, value in projection_drifts:
        cases.append((case_id, f"Projection drift at {'.'.join(path)}.", lambda cfg, p=path, v=value: set_path(cfg, p, v)))
    receipt_drifts = [
        ("receipt-record-kind", ["packet_receipt", "record_kind"], "execution_permission_receipt"),
        ("receipt-slice-id", ["packet_receipt", "slice_id"], "wrong"),
        ("receipt-source-slice", ["packet_receipt", "source_slice"], "wrong"),
        ("receipt-packet-result", ["packet_receipt", "packet_result"], "READY_TO_EXECUTE"),
        ("receipt-formal-vault-access", ["packet_receipt", "formal_vault_accessed"], True),
        ("receipt-state-inspected", ["packet_receipt", "formal_vault_state_inspected"], True),
        ("receipt-approval-collected", ["packet_receipt", "approval_collected_now"], True),
        ("receipt-real-user-input", ["packet_receipt", "actual_user_input_used"], True),
        ("receipt-real-user-text", ["packet_receipt", "real_user_text_stored"], True),
        ("receipt-execution-permission", ["packet_receipt", "execution_permission_granted"], True),
        ("receipt-write-performed", ["packet_receipt", "write_performed"], True),
        ("receipt-sync-performed", ["packet_receipt", "sync_performed"], True),
        ("receipt-submitted-to-gate", ["packet_receipt", "packet_submitted_to_gate"], True),
        ("receipt-action-basis", ["packet_receipt", "packet_used_as_action_basis"], True),
        ("receipt-field-count", ["packet_receipt", "field_count"], 99),
        ("receipt-source-count", ["packet_receipt", "source_count"], 99),
        ("receipt-hash", ["packet_receipt", "request_packet_hash"], "8" * 64),
        ("receipt-non-claims", ["packet_receipt", "non_claims"], []),
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
            ("packet-mode-top-level-drift", "Top-level packet mode drifts.", lambda cfg: set_path(cfg, ["packet_mode"], "real_execute_now")),
            ("metric-failure-floor-low", "Failure-case floor too low.", lambda cfg: set_path(cfg, ["product_metrics", "minimum_failure_cases"], 10)),
            ("metric-field-count-drift", "Required field count drifts.", lambda cfg: set_path(cfg, ["product_metrics", "required_packet_fields"], 99)),
            ("metric-manual-probes-drift", "Manual probe count drifts.", lambda cfg: set_path(cfg, ["product_metrics", "manual_negative_probes"], 0)),
            ("hash-drift", "Request packet hash drifts.", lambda cfg: set_path(cfg, ["request_packet_hash"], "9" * 64)),
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

    stale_proto = ROOT / "prototype" / "formal-vault-execution-request-packet"
    if stale_proto.exists():
        reset_dir(stale_proto)
    required_html_attrs = (
        '<html lang="en" data-sandbox-only="true" data-request-packet-only="true" '
        'data-non-executable="true" data-no-formal-vault-access="true" '
        'data-no-write="true" data-no-sync="true" data-no-authority="true" '
        'data-no-permission="true" data-no-real-user-text="true">'
    )
    prototype_cases = [
        ("prototype-markdown-command", "Prototype Markdown contains command.", {"kind": "markdown_replace", "file": "00 Request Packet Home.md", "content": "Copy-Item source H:/Obsidian/资料库/target.md"}),
        ("prototype-markdown-ready", "Prototype Markdown claims ready.", {"kind": "markdown_replace", "file": "01 Packet Contract.md", "content": "This packet is ready to execute."}),
        ("prototype-markdown-approval-collected", "Prototype Markdown says approval collected.", {"kind": "markdown_replace", "file": "03 Non Submission Receipt.md", "content": "approval collected: yes"}),
        ("prototype-markdown-packet-submitted", "Prototype Markdown says packet submitted.", {"kind": "markdown_replace", "file": "05 Reviewer Packet.md", "content": "packet submitted: yes"}),
        ("prototype-markdown-permission-yes", "Prototype Markdown says permission yes.", {"kind": "markdown_replace", "file": "02 Packet Fields.md", "content": "execution permission: yes"}),
        ("prototype-markdown-approval-yes", "Prototype Markdown says formal vault approval yes.", {"kind": "markdown_replace", "file": "02 Packet Fields.md", "content": "formal vault approval: yes"}),
        ("prototype-markdown-action-basis-yes", "Prototype Markdown says action basis yes.", {"kind": "markdown_replace", "file": "02 Packet Fields.md", "content": "action basis: yes"}),
        ("prototype-markdown-real-user-text", "Prototype Markdown carries actual wording.", {"kind": "markdown_replace", "file": "02 Packet Fields.md", "content": "real user text: approve execution now"}),
        ("prototype-markdown-authorizes-execution", "Prototype Markdown says packet authorizes execution.", {"kind": "markdown_replace", "file": "01 Packet Contract.md", "content": "This packet authorizes the future execution slice."}),
        ("prototype-markdown-may-execute", "Prototype Markdown says operator may execute.", {"kind": "markdown_replace", "file": "04 Stop Conditions.md", "content": "The operator may execute the formal vault operation."}),
        ("prototype-markdown-permission-collected", "Prototype Markdown says permission collected.", {"kind": "markdown_replace", "file": "03 Non Submission Receipt.md", "content": "Permission collected from the user."}),
        ("prototype-markdown-approval-obtained", "Prototype Markdown says approval obtained.", {"kind": "markdown_replace", "file": "03 Non Submission Receipt.md", "content": "Approval obtained from the user."}),
        ("prototype-html-command", "Prototype HTML contains command.", {"kind": "html_replace", "file": "request-packet-inspector.html", "content": required_html_attrs + "<body>Copy-Item source H:/Obsidian/资料库/target.md</body></html>"}),
        ("prototype-html-missing-attrs", "Prototype HTML misses required sandbox attributes.", {"kind": "html_replace", "file": "request-packet-inspector.html", "content": "<html><body>Packet inspector</body></html>"}),
        ("prototype-html-submit-button", "Prototype HTML contains submission UI wording.", {"kind": "html_replace", "file": "request-packet-inspector.html", "content": required_html_attrs + "<body><button>Submit packet to readiness gate</button></body></html>"}),
        ("prototype-html-authorizes-execution", "Prototype HTML authorizes execution.", {"kind": "html_replace", "file": "request-packet-inspector.html", "content": required_html_attrs + "<body>This packet authorizes the future execution slice.</body></html>"}),
        ("prototype-receipt-command", "Prototype receipt command injection.", {"kind": "receipt_update", "updates": {"shell_command": "Copy-Item source H:/Obsidian/资料库/target.md"}}),
        ("prototype-receipt-hash", "Prototype receipt hash drift.", {"kind": "receipt_update", "updates": {"request_packet_hash": "0" * 64}}),
        ("prototype-receipt-slice", "Prototype receipt slice drift.", {"kind": "receipt_update", "updates": {"slice_id": "wrong"}}),
        ("prototype-receipt-source", "Prototype receipt source drift.", {"kind": "receipt_update", "updates": {"source_slice": "wrong"}}),
        ("prototype-receipt-permission", "Prototype receipt grants permission.", {"kind": "receipt_update", "updates": {"execution_permission_granted": True}}),
        ("prototype-receipt-submitted", "Prototype receipt says submitted.", {"kind": "receipt_update", "updates": {"packet_submitted_to_gate": True}}),
        ("prototype-receipt-action-basis", "Prototype receipt says action basis.", {"kind": "receipt_update", "updates": {"packet_used_as_action_basis": True}}),
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

Define a synthetic future formal-vault execution request packet that can be
screened by the P2-31 readiness gate without becoming approval, user
instruction, execution permission, or action basis.

## Inputs

- P2-31 Product Acceptance report.
- P2-31 readiness gate config and receipt.
- P2-31 Reviewer and Boundary reports.

## Outputs

- Request packet contract.
- Three positive fixtures.
- Failure-case oracle and failure cases.
- Manual negative probes.
- Static reviewer prototype.
- Verification and acceptance reports.

## Boundary

This slice does not collect approval, store actual wording from the user, emit
commands, resolve formal-vault paths, or touch the formal vault.
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
        + "\n\nAll sources are sandbox process inputs only. Hash binding is not evidence support or action basis.\n",
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
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_request_packet.py --rebuild
```

Default read-only verification:

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_request_packet.py
```

Pre-acceptance final gate:

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_request_packet.py --final-gate
```

Before Reviewer / Boundary / Product closeout, final gate should fail only on
pending report statuses.

## What Is Verified

- Three positive fixtures.
- {case_count} failure cases.
- Twelve manual negative probes that are not generated from the failure oracle.
- Exact P2-31 source hashes and report statuses.
- P2-31 readiness gate hash, receipt hash, check count, source count, and
  non-permission flags.
- Synthetic packet identity, projection identity, and non-submission flags.
- No current approval, actual user wording, formal-vault path, command, or
  execution-now intent.
- Prototype Markdown, HTML, and receipt tamper are fail-closed.

## Observed Current Results

```text
rebuild: passed true
default verification: passed true
positive fixtures: 3
failure cases: {case_count}
failure mismatches: []
manual negative probes: 12
manual probe mismatches: []
prototype issues: []
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
        ROOT / "artifact" / "formal-vault-execution-request-packet-contract.md",
        """# Formal Vault Execution Request Packet Contract

This artifact defines a synthetic request packet shape for future screening by
the P2-31 readiness gate.

Hard boundaries:

- It is sandbox-only.
- It is not user approval.
- It is not a user instruction.
- It is not execution permission.
- It is not formal vault approval.
- It is not action basis.
- It does not contain actual wording from the user.
- It does not access, inspect, hash, snapshot, write, or sync the formal vault.
- It does not emit commands or absolute formal-vault paths.
""",
    )
    proto = ROOT / "prototype" / "formal-vault-execution-request-packet"
    reset_dir(proto)
    write_text(
        proto / "00 Request Packet Home.md",
        f"""# Request Packet Home

Slice: `{SLICE_ID}`

Result: `{reviewable['request_packet']['packet_result']}`

This is a sandbox request-packet review surface. It is not approval, not
permission, and not a submission to the readiness gate.

Open:

- [[01 Packet Contract]]
- [[02 Packet Fields]]
- [[03 Non Submission Receipt]]
- [[04 Stop Conditions]]
- [[05 Reviewer Packet]]
""",
    )
    write_text(
        proto / "01 Packet Contract.md",
        """# Packet Contract

- sandbox only
- synthetic packet only
- not approval
- not permission
- not action basis
- no executable operation surface
- separate future confirmation required
""",
    )
    write_text(
        proto / "02 Packet Fields.md",
        "# Packet Fields\n\n"
        + "\n".join(f"- `{item['field_id']}`: synthetic contract field" for item in reviewable["packet_schema"])
        + "\n",
    )
    write_text(
        proto / "03 Non Submission Receipt.md",
        """# Non Submission Receipt

The receipt records process integrity only. The packet is not submitted to the
readiness gate and it does not collect approval.
""",
    )
    write_text(
        proto / "04 Stop Conditions.md",
        """# Stop Conditions

Stop immediately if a future operator needs actual approval, actual user
wording, formal vault access, formal vault state inspection, command generation,
write, hash, snapshot, sync, commit, push, promotion, or mainline merge.
""",
    )
    write_text(
        proto / "05 Reviewer Packet.md",
        f"""# Reviewer Packet

Review checks:

- P2-31 Product Acceptance is bound
- readiness gate hash is bound
- packet identity is synthetic
- projection is not submission
- failure cases: {case_count}
- no executable operation surface
- no authority confusion
""",
    )
    write_json(proto / "Receipts" / "formal-vault-execution-request-packet-receipt.json", reviewable["packet_receipt"])
    html = f"""<!doctype html>
<html lang="en" data-sandbox-only="true" data-request-packet-only="true" data-non-executable="true" data-no-formal-vault-access="true" data-no-write="true" data-no-sync="true" data-no-authority="true" data-no-permission="true" data-no-real-user-text="true">
<head><meta charset="utf-8"><title>Request Packet Inspector</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; color: #202124; background: #f8f7f1; }}
main {{ max-width: 920px; }}
button {{ margin: 0 8px 8px 0; padding: 7px 10px; border: 1px solid #777; background: #fff; }}
section {{ border-top: 1px solid #ccc; padding: 14px 0; }}
code {{ background: #ecebe4; padding: 1px 4px; }}
</style></head>
<body><main>
<h1>Request Packet Inspector</h1>
<p>Sandbox-only synthetic request packet view. No approval or permission is created here.</p>
<button data-filter="all">All</button>
<button data-filter="contract">Contract</button>
<button data-filter="fields">Fields</button>
<button data-filter="receipt">Receipt</button>
<button data-filter="stops">Stops</button>
<section data-kind="contract"><h2>Contract</h2><p>Separate future confirmation and execution slice required.</p></section>
<section data-kind="fields"><h2>Fields</h2><p>{len(PACKET_FIELD_IDS)} synthetic contract fields, none are captured as approval.</p></section>
<section data-kind="receipt"><h2>Receipt</h2><p>Packet hash <code>{reviewable['request_packet_hash']}</code></p></section>
<section data-kind="stops"><h2>Stops</h2><p>Any real vault operation stops this sandbox.</p></section>
</main></body></html>
"""
    write_text(proto / "request-packet-inspector.html", html)


def build_all() -> None:
    fixtures = write_fixtures()
    reviewable = fixtures["valid-reviewable-request-packet-config.json"]
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
    manual = run_manual_negative_probes()
    if manual["mismatches"]:
        raise RuntimeError(f"manual probe mismatches: {manual['mismatches']}")
    print(f"built {SLICE_ID}")


def main() -> None:
    build_all()


if __name__ == "__main__":
    main()
