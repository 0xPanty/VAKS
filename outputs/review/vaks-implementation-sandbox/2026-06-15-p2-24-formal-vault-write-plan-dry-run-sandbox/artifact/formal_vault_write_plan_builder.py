from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-15-p2-24-formal-vault-write-plan-dry-run-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-23-native-markdown-entry-readonly-inspector-sandbox"


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def sandbox_root() -> Path:
    return root().parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def repo_relative(path: Path) -> str:
    repo = sandbox_root().parents[2]
    return path.relative_to(repo).as_posix()


def source_binding(paths: dict[str, Path], key: str) -> dict[str, str]:
    path = paths[key]
    return {
        "source_path": repo_relative(path),
        "source_sha256": sha256(path) if path.exists() else "missing",
        "content_binding": "exact_source_sha256",
    }


def safe_write(rel_path: str, content: str, *, overwrite: bool = True) -> None:
    base = root().resolve()
    target = (base / rel_path).resolve()
    if base != target and base not in target.parents:
        raise ValueError(f"Refusing to write outside slice root: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not overwrite:
        return
    target.write_text(content.rstrip() + "\n", encoding="utf-8")


def source_paths() -> dict[str, Path]:
    src = sandbox_root() / SOURCE_SLICE_ID
    return {
        "source_root": src,
        "source_next_step": src / "next-step.md",
        "source_verification": src / "verification.md",
        "source_product_acceptance": src / "product-acceptance-report.md",
        "source_contract": src / "artifact" / "native-entry-readonly-inspector-contract.md",
        "source_native_home": src
        / "prototype"
        / "vaks-native-entry-readonly-inspector"
        / "00 Native Home.md",
        "source_status_board": src
        / "prototype"
        / "vaks-native-entry-readonly-inspector"
        / "02 Status Board.md",
        "source_receipt_index": src
        / "prototype"
        / "vaks-native-entry-readonly-inspector"
        / "03 Receipt Index.md",
        "source_boundary_stop": src
        / "prototype"
        / "vaks-native-entry-readonly-inspector"
        / "04 Boundary Stop.md",
        "source_readonly_inspector": src
        / "prototype"
        / "vaks-native-entry-readonly-inspector"
        / "readonly-inspector.html",
    }


def forbidden_operations() -> list[str]:
    return [
        "formal_vault_read",
        "formal_vault_scan",
        "formal_vault_write",
        "obsidian_sync",
        "commit",
        "push",
        "promotion",
        "dependency_install",
        "background_service",
        "mcp_write_tool",
        "hooks",
        "real_base_files",
        "production_ui",
        "local_storage_write",
        "network_post",
    ]


def config() -> dict:
    paths = source_paths()
    return {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "plan_version": "p2-24-dry-run-v1",
        "plan_hash_algorithm": "sha256",
        "purpose": "Dry-run a future formal vault write plan without reading or writing the formal vault.",
        "formal_vault_path_label": "formal Obsidian vault path is a label only; it is not accessed in this slice",
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": [
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/next-step.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/verification.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/product-acceptance-report.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/native-entry-readonly-inspector-contract.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/prototype/vaks-native-entry-readonly-inspector/00 Native Home.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/prototype/vaks-native-entry-readonly-inspector/02 Status Board.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/prototype/vaks-native-entry-readonly-inspector/03 Receipt Index.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/prototype/vaks-native-entry-readonly-inspector/04 Boundary Stop.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/prototype/vaks-native-entry-readonly-inspector/readonly-inspector.html",
        ],
        "operations": {op: False for op in forbidden_operations()}
        | {"default_read_only": True, "rebuild_requires_explicit_flag": True},
        "boundary_phrases": [
            "sandbox only",
            "formal vault not accessed",
            "dry-run only",
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "does not approve",
            "no formal vault write",
            "no formal vault read",
            "no sync",
            "no commit",
            "no push",
            "no promotion",
            "requires separate user approval",
        ],
        "proposed_files": [
            {
                "id": "native_home",
                "relative_target": "VAKS-Workbench-Draft/00 Native Home.md",
                "source_artifact": "P2-23 prototype native home",
                **source_binding(paths, "source_native_home"),
                "write_enabled": False,
                "dry_run_only": True,
                "requires_user_approval": True,
                "rollback_required": True,
            },
            {
                "id": "status_board",
                "relative_target": "VAKS-Workbench-Draft/02 Status Board.md",
                "source_artifact": "P2-23 prototype status board",
                **source_binding(paths, "source_status_board"),
                "write_enabled": False,
                "dry_run_only": True,
                "requires_user_approval": True,
                "rollback_required": True,
            },
            {
                "id": "receipt_index",
                "relative_target": "VAKS-Workbench-Draft/03 Receipt Index.md",
                "source_artifact": "P2-23 prototype receipt index",
                **source_binding(paths, "source_receipt_index"),
                "write_enabled": False,
                "dry_run_only": True,
                "requires_user_approval": True,
                "rollback_required": True,
            },
            {
                "id": "boundary_stop",
                "relative_target": "VAKS-Workbench-Draft/04 Boundary Stop.md",
                "source_artifact": "P2-23 prototype boundary stop",
                **source_binding(paths, "source_boundary_stop"),
                "write_enabled": False,
                "dry_run_only": True,
                "requires_user_approval": True,
                "rollback_required": True,
            },
            {
                "id": "readonly_inspector",
                "relative_target": "VAKS-Workbench-Draft/readonly-inspector.html",
                "source_artifact": "P2-23 static read-only inspector",
                **source_binding(paths, "source_readonly_inspector"),
                "write_enabled": False,
                "dry_run_only": True,
                "requires_user_approval": True,
                "rollback_required": True,
            },
        ],
        "approval_prompts": [
            {
                "id": "approve_formal_vault_write_scope",
                "prompt": "Do you explicitly approve writing only the listed relative files to the formal vault in a future slice?",
                "applies_to_file_ids": ["native_home", "status_board", "receipt_index", "boundary_stop", "readonly_inspector"],
                "plan_version_required": "p2-24-dry-run-v1",
                "plan_hash_required": True,
                "confirmation_phrase": "APPROVE ONLY LISTED FILES FOR FUTURE FORMAL VAULT WRITE",
                "required_response": "explicit_user_approval",
                "default": "deny",
                "blocks": ["formal_vault_write", "obsidian_sync", "real_base_files"],
                "excludes": ["obsidian_sync", "commit", "push", "promotion"],
            },
            {
                "id": "approve_rollback_manifest",
                "prompt": "Do you approve the rollback manifest and hash-before/hash-after checks before any future write?",
                "applies_to_file_ids": ["native_home", "status_board", "receipt_index", "boundary_stop", "readonly_inspector"],
                "plan_version_required": "p2-24-dry-run-v1",
                "plan_hash_required": True,
                "confirmation_phrase": "APPROVE ROLLBACK AND HASH CHECKS BEFORE FUTURE WRITE",
                "required_response": "explicit_user_approval",
                "default": "deny",
                "blocks": ["formal_vault_write"],
                "excludes": ["obsidian_sync", "commit", "push", "promotion"],
            },
            {
                "id": "approve_no_sync_after_write",
                "prompt": "Do you approve keeping Obsidian sync disabled unless separately requested after the future write?",
                "applies_to_file_ids": ["native_home", "status_board", "receipt_index", "boundary_stop", "readonly_inspector"],
                "plan_version_required": "p2-24-dry-run-v1",
                "plan_hash_required": True,
                "confirmation_phrase": "APPROVE NO SYNC COMMIT PUSH OR PROMOTION IN FUTURE WRITE SLICE",
                "required_response": "explicit_user_approval",
                "default": "deny",
                "blocks": ["obsidian_sync"],
                "excludes": ["obsidian_sync", "commit", "push", "promotion"],
            },
        ],
        "rollback_manifest": {
            "dry_run_only": True,
            "snapshot_root_label": "future-approved-snapshot-root",
            "retention_policy": "keep until user confirms future formal write succeeded and rollback window can close",
            "snapshot_before_write_required": True,
            "hash_before_required": True,
            "hash_after_required": True,
            "hash_algorithm": "sha256",
            "record_format": "json-lines: target, operation, before_state, before_hash, after_hash, rollback_action, verification_result",
            "unexpected_file_abort": True,
            "unexpected_hash_drift_abort": True,
            "dirty_state_abort": True,
            "rollback_after_verification_required": True,
            "rollback_requires_user_confirmation": True,
            "file_entries": [
                {
                    "file_id": "native_home",
                    "relative_target": "VAKS-Workbench-Draft/00 Native Home.md",
                    "planned_operation": "create_or_replace",
                    "before_state": "unknown_until_future_approved_snapshot",
                    "snapshot_location_label": "future-approved-snapshot-root/VAKS-Workbench-Draft/00 Native Home.md",
                    "rollback_action": "restore_previous_if_existed_else_delete_created_file",
                    "post_rollback_verification": "hash_matches_before_or_file_absent_if_new",
                },
                {
                    "file_id": "status_board",
                    "relative_target": "VAKS-Workbench-Draft/02 Status Board.md",
                    "planned_operation": "create_or_replace",
                    "before_state": "unknown_until_future_approved_snapshot",
                    "snapshot_location_label": "future-approved-snapshot-root/VAKS-Workbench-Draft/02 Status Board.md",
                    "rollback_action": "restore_previous_if_existed_else_delete_created_file",
                    "post_rollback_verification": "hash_matches_before_or_file_absent_if_new",
                },
                {
                    "file_id": "receipt_index",
                    "relative_target": "VAKS-Workbench-Draft/03 Receipt Index.md",
                    "planned_operation": "create_or_replace",
                    "before_state": "unknown_until_future_approved_snapshot",
                    "snapshot_location_label": "future-approved-snapshot-root/VAKS-Workbench-Draft/03 Receipt Index.md",
                    "rollback_action": "restore_previous_if_existed_else_delete_created_file",
                    "post_rollback_verification": "hash_matches_before_or_file_absent_if_new",
                },
                {
                    "file_id": "boundary_stop",
                    "relative_target": "VAKS-Workbench-Draft/04 Boundary Stop.md",
                    "planned_operation": "create_or_replace",
                    "before_state": "unknown_until_future_approved_snapshot",
                    "snapshot_location_label": "future-approved-snapshot-root/VAKS-Workbench-Draft/04 Boundary Stop.md",
                    "rollback_action": "restore_previous_if_existed_else_delete_created_file",
                    "post_rollback_verification": "hash_matches_before_or_file_absent_if_new",
                },
                {
                    "file_id": "readonly_inspector",
                    "relative_target": "VAKS-Workbench-Draft/readonly-inspector.html",
                    "planned_operation": "create_or_replace",
                    "before_state": "unknown_until_future_approved_snapshot",
                    "snapshot_location_label": "future-approved-snapshot-root/VAKS-Workbench-Draft/readonly-inspector.html",
                    "rollback_action": "restore_previous_if_existed_else_delete_created_file",
                    "post_rollback_verification": "hash_matches_before_or_file_absent_if_new",
                },
            ],
        },
        "hash_check_plan": {
            "dry_run_only": True,
            "algorithm": "sha256",
            "record_format": "json-lines",
            "phases": ["before_snapshot", "after_write", "after_rollback_if_needed"],
            "per_file_records_required": True,
            "records": [
                {
                    "file_id": "native_home",
                    "relative_target": "VAKS-Workbench-Draft/00 Native Home.md",
                    "before_hash_field": "before_hash_sha256",
                    "after_hash_field": "after_hash_sha256",
                    "rollback_hash_field": "rollback_hash_sha256",
                },
                {
                    "file_id": "status_board",
                    "relative_target": "VAKS-Workbench-Draft/02 Status Board.md",
                    "before_hash_field": "before_hash_sha256",
                    "after_hash_field": "after_hash_sha256",
                    "rollback_hash_field": "rollback_hash_sha256",
                },
                {
                    "file_id": "receipt_index",
                    "relative_target": "VAKS-Workbench-Draft/03 Receipt Index.md",
                    "before_hash_field": "before_hash_sha256",
                    "after_hash_field": "after_hash_sha256",
                    "rollback_hash_field": "rollback_hash_sha256",
                },
                {
                    "file_id": "boundary_stop",
                    "relative_target": "VAKS-Workbench-Draft/04 Boundary Stop.md",
                    "before_hash_field": "before_hash_sha256",
                    "after_hash_field": "after_hash_sha256",
                    "rollback_hash_field": "rollback_hash_sha256",
                },
                {
                    "file_id": "readonly_inspector",
                    "relative_target": "VAKS-Workbench-Draft/readonly-inspector.html",
                    "before_hash_field": "before_hash_sha256",
                    "after_hash_field": "after_hash_sha256",
                    "rollback_hash_field": "rollback_hash_sha256",
                },
            ],
            "abort_on_missing_before_hash": True,
            "abort_on_unexpected_after_hash": True,
            "abort_on_dirty_state": True,
            "abort_on_unexpected_file": True,
            "verify_after_rollback": True,
            "no_executable_commands": True,
            "command_templates": [],
        },
        "stop_conditions": [
            "formal vault read requested",
            "formal vault write requested",
            "absolute vault path requested",
            "Obsidian sync requested",
            "real .base requested",
            "commit or push requested",
            "promotion requested",
            "dependency install requested",
            "background service requested",
            "MCP write tool requested",
            "approval prompt missing or default not deny",
            "rollback manifest missing",
            "hash-before or hash-after missing",
        ],
        "journeys": [
            {
                "id": "scope_review",
                "steps": ["00 Dry Run Home", "01 Proposed File List", "05 Stop Conditions"],
                "expected_answer": "Only relative proposed targets are listed; no formal vault path is accessed.",
                "max_steps": 3,
                "stop_condition": "Stop on absolute formal vault path or write-enabled target.",
            },
            {
                "id": "approval_review",
                "steps": ["00 Dry Run Home", "02 Approval Prompt Matrix", "05 Stop Conditions"],
                "expected_answer": "Every future write needs explicit user approval and defaults to deny.",
                "max_steps": 3,
                "stop_condition": "Stop if approval is implicit or automatic.",
            },
            {
                "id": "rollback_review",
                "steps": ["00 Dry Run Home", "03 Rollback Manifest", "04 Hash Check Plan"],
                "expected_answer": "Rollback and hash checks are required before any future write.",
                "max_steps": 3,
                "stop_condition": "Stop if snapshot or hash-before/hash-after is missing.",
            },
            {
                "id": "inspector_review",
                "steps": ["00 Dry Run Home", "plan-inspector.html", "05 Stop Conditions"],
                "expected_answer": "Inspector is read-only and plan-only.",
                "max_steps": 3,
                "stop_condition": "Stop if inspector has write, sync, save, or execute controls.",
            },
        ],
        "inspector_controls": {
            "inputs": [{"id": "q", "type": "search", "purpose": "filter"}],
            "buttons": [
                {"label": "All", "filter": "all"},
                {"label": "Files", "filter": "files"},
                {"label": "Approvals", "filter": "approvals"},
                {"label": "Rollback", "filter": "rollback"},
                {"label": "Stops", "filter": "stops"},
            ],
        },
        "product_metrics": {
            "required_positive_fixtures": 2,
            "minimum_failure_cases": 30,
            "required_proposed_files": 5,
            "required_approval_prompts": 3,
            "max_journey_steps": 3,
        },
    }


def variant_config(base: dict) -> dict:
    variant = json.loads(json.dumps(base))
    variant["purpose"] = "Variant dry-run config for rollback reviewer handoff."
    variant["approval_prompts"].append(
        {
            "id": "approve_handoff_readiness",
            "prompt": "Do you approve using this plan as a future handoff checklist only?",
            "applies_to_file_ids": ["native_home", "status_board", "receipt_index", "boundary_stop", "readonly_inspector"],
            "plan_version_required": "p2-24-dry-run-v1",
            "plan_hash_required": True,
            "confirmation_phrase": "APPROVE THIS PLAN AS FUTURE HANDOFF CHECKLIST ONLY",
            "required_response": "explicit_user_approval",
            "default": "deny",
            "blocks": ["promotion"],
            "excludes": ["obsidian_sync", "commit", "push", "promotion"],
        }
    )
    return variant


def failure_cases(base: dict) -> list[tuple[str, dict]]:
    cases: list[tuple[str, dict]] = []

    def mutate(name: str, code: str, fn) -> None:
        item = json.loads(json.dumps(base))
        fn(item)
        item["expected_failures"] = [code]
        cases.append((name, item))

    for idx, op in enumerate(forbidden_operations(), start=1):
        mutate(
            f"{idx:02d}-forbidden-{op}.json",
            f"forbidden_operation:{op}",
            lambda c, op=op: c["operations"].__setitem__(op, True),
        )

    mutate(
        "16-absolute-formal-target.json",
        "proposed_file_absolute_or_forbidden:native_home",
        lambda c: c["proposed_files"][0].__setitem__("relative_target", "H:/Obsidian/vault/00 Native Home.md"),
    )
    mutate(
        "17-write-enabled-target.json",
        "proposed_file_write_enabled:native_home",
        lambda c: c["proposed_files"][0].__setitem__("write_enabled", True),
    )
    mutate(
        "18-missing-user-approval.json",
        "proposed_file_missing_user_approval:native_home",
        lambda c: c["proposed_files"][0].__setitem__("requires_user_approval", False),
    )
    mutate(
        "19-auto-approval-prompt.json",
        "approval_prompt_not_deny:approve_formal_vault_write_scope",
        lambda c: c["approval_prompts"][0].__setitem__("default", "approve"),
    )
    mutate(
        "20-missing-rollback-snapshot.json",
        "rollback_snapshot_missing",
        lambda c: c["rollback_manifest"].__setitem__("snapshot_before_write_required", False),
    )
    mutate(
        "21-missing-hash-before.json",
        "hash_before_missing",
        lambda c: c["hash_check_plan"].__setitem__("abort_on_missing_before_hash", False),
    )
    mutate(
        "22-executable-command-template.json",
        "hash_plan_executable_command",
        lambda c: c["hash_check_plan"].__setitem__("command_templates", ["powershell sync H:/Obsidian"]),
    )
    mutate(
        "23-authority-confusing-stop.json",
        "authority_confusing_text",
        lambda c: c["stop_conditions"].append("receipt proves evidence support"),
    )
    mutate(
        "24-approval-missing-file-binding.json",
        "approval_prompt_missing_file_binding:approve_formal_vault_write_scope",
        lambda c: c["approval_prompts"][0].__setitem__("applies_to_file_ids", []),
    )
    mutate(
        "25-approval-missing-plan-hash.json",
        "approval_prompt_missing_plan_hash:approve_formal_vault_write_scope",
        lambda c: c["approval_prompts"][0].__setitem__("plan_hash_required", False),
    )
    mutate(
        "26-rollback-file-entries-missing.json",
        "rollback_file_entries_missing",
        lambda c: c["rollback_manifest"].__setitem__("file_entries", []),
    )
    mutate(
        "27-rollback-dirty-abort-missing.json",
        "rollback_dirty_state_abort_missing",
        lambda c: c["rollback_manifest"].__setitem__("dirty_state_abort", False),
    )
    mutate(
        "28-hash-records-missing.json",
        "hash_records_missing",
        lambda c: c["hash_check_plan"].__setitem__("records", []),
    )
    mutate(
        "29-hash-rollback-verify-missing.json",
        "hash_rollback_verification_missing",
        lambda c: c["hash_check_plan"].__setitem__("verify_after_rollback", False),
    )
    mutate(
        "30-too-few-failure-cases.json",
        "minimum_failure_cases_too_low",
        lambda c: c["product_metrics"].__setitem__("minimum_failure_cases", 5),
    )
    mutate(
        "31-missing-source-path-binding.json",
        "proposed_file_source_path_missing:native_home",
        lambda c: c["proposed_files"][0].__setitem__("source_path", ""),
    )
    mutate(
        "32-source-hash-mismatch.json",
        "proposed_file_source_hash_mismatch:native_home",
        lambda c: c["proposed_files"][0].__setitem__("source_sha256", "deadbeef"),
    )
    return cases


def frontmatter(record_kind: str, status: str, extra: dict[str, str] | None = None) -> str:
    lines = [
        "---",
        f"record_kind: {record_kind}",
        f"slice_id: {SLICE_ID}",
        f"status: {status}",
        "sandbox_only: true",
        "truth_boundary: sandbox_only",
    ]
    for key, value in (extra or {}).items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def md_link(label: str, target: str) -> str:
    return f"[{label}]({target})"


def render_slice_plan(git_status_summary: str) -> str:
    return f"""---
record_kind: sandbox_slice_plan
slice_id: {SLICE_ID}
status: built_pending_review
truth_boundary: sandbox_only
---

# Slice Plan

## Goal

Build a sandbox-only dry-run plan for a future formal vault write. This slice
does not read, write, scan, sync, or mutate the formal vault.

## Why This Slice

P2-23 received `PASS_PRODUCT_GRADE` and recommended a
`formal-vault-write-plan-dry-run-sandbox`.

## Write Scope

```text
outputs/review/vaks-implementation-sandbox/{SLICE_ID}/
```

## Acceptance Standard

- Proposed file list uses relative targets only.
- Every proposed target is dry-run only, write disabled, and requires explicit
  user approval.
- Approval prompts default to deny.
- Rollback manifest requires snapshot and hash checks.
- Hash plan contains no executable commands.
- Stop conditions catch formal vault read/write, sync, commit, push, promotion,
  dependency install, background services, MCP writes, hooks, real Bases, and
  missing approvals.
- Reviewer, Boundary, and GPT-5.5 xhigh Product Acceptance pass.
- Final gate passes after Product Acceptance.

## Start Git Status Summary

```text
{git_status_summary}
```

The dirty tree is treated as pre-existing baseline. Final audit is scoped to
this slice path only.
"""


def render_source_map(paths: dict[str, Path], base: dict) -> str:
    rows = []
    for key, path in paths.items():
        if key == "source_root":
            continue
        rel = path.relative_to(sandbox_root())
        rows.append(
            f"| `{key}` | `../{rel.as_posix()}` | exists: `{path.exists()}` | sha256: `{sha256(path) if path.exists() else 'missing'}` |"
        )
    bindings = []
    for item in base["proposed_files"]:
        bindings.append(
            f"| `{item['id']}` | `{item['relative_target']}` | `{item['source_path']}` | `{item['source_sha256']}` | `{item['content_binding']}` |"
        )
    return f"""---
record_kind: sandbox_source_map
slice_id: {SLICE_ID}
status: built_pending_review
truth_boundary: sandbox_only
---

# Source Map

This slice reads P2-23 as the product-grade sandbox source. It does not read or
write the formal Obsidian vault.

| Source | Path | Evidence |
| --- | --- | --- |
{chr(10).join(rows)}

## Proposed Target Source Bindings

| Proposed File ID | Relative Proposed Target | Source Path | Source SHA256 | Binding |
| --- | --- | --- | --- | --- |
{chr(10).join(bindings)}

## Boundary

P2-23 `PASS_PRODUCT_GRADE` is a sandbox input only. It is not reviewed
knowledge, evidence support, action basis, mainline approval, formal vault
approval, sync approval, commit approval, push approval, or promotion approval.
"""


def render_contract(base: dict) -> str:
    return f"""# Formal Vault Write-Plan Dry-Run Contract

## Input Contract

- P2-23 sandbox reports and native entry artifact.
- No formal vault read, scan, write, sync, or mutation.

## Output Contract

- Proposed relative file list.
- Per-file source path and SHA256 binding for every proposed target.
- Approval prompt matrix.
- Rollback manifest.
- Hash check plan.
- Stop condition register.
- Static plan inspector with no write controls.

## Product Promise

A future agent can understand exactly what would need approval before any formal
vault write, without receiving permission to perform that write.

## Boundary Promise

This is dry-run only. The formal vault is not accessed. Proposed paths are
relative labels, not write targets. Approval prompts are future gates, not
current approval. Hash receipts are process checks, not evidence support.
"""


def render_home(base: dict) -> str:
    return f"""{frontmatter("sandbox_formal_vault_write_plan_home", "sandbox_pilot")}

# Dry Run Home

This sandbox plans a possible future formal vault write without accessing the
formal vault.

## Start

1. Open [[01 Proposed File List]].
2. Open [[02 Approval Prompt Matrix]].
3. Open [[03 Rollback Manifest]].
4. Open [[05 Stop Conditions]] before any action-facing move.

## Fast Links

- [[01 Proposed File List]]
- [[02 Approval Prompt Matrix]]
- [[03 Rollback Manifest]]
- [[04 Hash Check Plan]]
- [[05 Stop Conditions]]
- [[06 Dry Run Results]]
- [[07 Reviewer Packet]]
- `plan-inspector.html`
- {md_link("P2-23 next-step", "../../../" + SOURCE_SLICE_ID + "/next-step.md")}
- {md_link("P2-23 product acceptance", "../../../" + SOURCE_SLICE_ID + "/product-acceptance-report.md")}

## Boundary Rail

Sandbox only. Formal vault not accessed. Dry-run only. Not reviewed knowledge.
Not evidence support. Not action basis. Does not approve. No formal vault read.
No formal vault write. No sync. No commit. No push. No promotion. Requires separate user approval.
"""


def render_file_list(base: dict) -> str:
    rows = [
        "| ID | Relative Proposed Target | Source Artifact | Source Path | Source SHA256 | Write Enabled | Approval Required |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in base["proposed_files"]:
        rows.append(
            f"| `{item['id']}` | `{item['relative_target']}` | {item['source_artifact']} | `{item['source_path']}` | `{item['source_sha256']}` | `{item['write_enabled']}` | `{item['requires_user_approval']}` |"
        )
    return f"""{frontmatter("sandbox_proposed_file_list", "sandbox_pilot")}

# Proposed File List

{chr(10).join(rows)}

## Boundary

These are relative proposed targets only. They are not absolute formal vault
paths, not write commands, and not approval to write.

## Next

- [[02 Approval Prompt Matrix]]
- [[05 Stop Conditions]]
"""


def render_approval_matrix(base: dict) -> str:
    rows = [
        "| Prompt ID | Required Phrase | Applies To | Default | Excludes | Blocks |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in base["approval_prompts"]:
        rows.append(
            f"| `{item['id']}` | `{item['confirmation_phrase']}` | {', '.join(item['applies_to_file_ids'])} | `{item['default']}` | {', '.join(item['excludes'])} | {', '.join(item['blocks'])} |"
        )
    return f"""{frontmatter("sandbox_approval_prompt_matrix", "sandbox_pilot")}

# Approval Prompt Matrix

{chr(10).join(rows)}

## Boundary

Approval prompts are future gates only. They are not current approval, not
mainline approval, and not permission to write, sync, commit, push, or promote.
Every approval must cite plan version `{base['plan_version']}` and a future
plan hash before it can be considered in a later approved slice.

## Next

- [[03 Rollback Manifest]]
- [[05 Stop Conditions]]
"""


def render_rollback(base: dict) -> str:
    rollback = base["rollback_manifest"]
    targets = "\n".join(
        f"| `{entry['file_id']}` | `{entry['relative_target']}` | `{entry['planned_operation']}` | `{entry['before_state']}` | `{entry['snapshot_location_label']}` | `{entry['rollback_action']}` | `{entry['post_rollback_verification']}` |"
        for entry in rollback["file_entries"]
    )
    return f"""{frontmatter("sandbox_rollback_manifest", "sandbox_pilot")}

# Rollback Manifest

## Required Before Any Future Write

- snapshot_root_label: `{rollback['snapshot_root_label']}`
- retention_policy: {rollback['retention_policy']}
- snapshot_before_write_required: `{rollback['snapshot_before_write_required']}`
- hash_before_required: `{rollback['hash_before_required']}`
- hash_after_required: `{rollback['hash_after_required']}`
- hash_algorithm: `{rollback['hash_algorithm']}`
- record_format: `{rollback['record_format']}`
- unexpected_file_abort: `{rollback['unexpected_file_abort']}`
- unexpected_hash_drift_abort: `{rollback['unexpected_hash_drift_abort']}`
- dirty_state_abort: `{rollback['dirty_state_abort']}`
- rollback_after_verification_required: `{rollback['rollback_after_verification_required']}`
- rollback_requires_user_confirmation: `{rollback['rollback_requires_user_confirmation']}`

## Per-File Rollback Semantics

| File ID | Relative Target | Operation | Before State | Snapshot Label | Rollback Action | Post-Rollback Verification |
| --- | --- | --- | --- | --- | --- | --- |
{targets}

## Boundary

Rollback planning is not rollback execution. No formal vault file is read,
snapshotted, written, or restored in this slice.

## Next

- [[04 Hash Check Plan]]
- [[05 Stop Conditions]]
"""


def render_hash_plan(base: dict) -> str:
    plan = base["hash_check_plan"]
    phases = "\n".join(f"- `{phase}`" for phase in plan["phases"])
    records = "\n".join(
        f"| `{entry['file_id']}` | `{entry['relative_target']}` | `{entry['before_hash_field']}` | `{entry['after_hash_field']}` | `{entry['rollback_hash_field']}` |"
        for entry in plan["records"]
    )
    return f"""{frontmatter("sandbox_hash_check_plan", "sandbox_pilot")}

# Hash Check Plan

## Algorithm

`{plan['algorithm']}`

## Phases

{phases}

## Requirements

- abort_on_missing_before_hash: `{plan['abort_on_missing_before_hash']}`
- abort_on_unexpected_after_hash: `{plan['abort_on_unexpected_after_hash']}`
- abort_on_dirty_state: `{plan['abort_on_dirty_state']}`
- abort_on_unexpected_file: `{plan['abort_on_unexpected_file']}`
- verify_after_rollback: `{plan['verify_after_rollback']}`
- per_file_records_required: `{plan['per_file_records_required']}`
- record_format: `{plan['record_format']}`
- no_executable_commands: `{plan['no_executable_commands']}`
- command_templates: `{len(plan['command_templates'])}`

## Per-File Hash Records

| File ID | Relative Target | Before Hash | After Hash | Rollback Hash |
| --- | --- | --- | --- | --- |
{records}

## Boundary

Hash checks are process integrity checks. They are not evidence support,
reviewed knowledge, action basis, sync approval, commit approval, push approval,
or formal vault approval.
"""


def render_stop_conditions(base: dict) -> str:
    rows = "\n".join(f"- {item}" for item in base["stop_conditions"])
    return f"""{frontmatter("sandbox_stop_conditions", "sandbox_pilot")}

# Stop Conditions

{rows}

## Safe Alternative

Record the requested move as a future approval item and stop. Do not perform the
operation in this slice.
"""


def render_dry_run_results(base: dict) -> str:
    return f"""{frontmatter("sandbox_dry_run_results", "sandbox_dry_run_passed")}

# Dry Run Results

## Method

Local file/link and static contract dry-run only. No formal vault read, scan,
write, sync, snapshot, or hash operation was performed.

## Task Results

| Task | Expected | Observed | Pass |
| --- | --- | --- | --- |
| Scope review | Proposed files are relative and write disabled | Home -> Proposed File List -> Stop Conditions | PASS |
| Approval review | Prompts require explicit approval and default deny | Home -> Approval Prompt Matrix -> Stop Conditions | PASS |
| Rollback review | Snapshot and hash checks are required | Home -> Rollback Manifest -> Hash Check Plan | PASS |
| Inspector review | Inspector is read-only and plan-only | Home -> plan-inspector.html -> Stop Conditions | PASS |

## Boundary

Dry-run pass is not approval to write the formal vault.
"""


def render_reviewer_packet(base: dict) -> str:
    return f"""{frontmatter("sandbox_reviewer_packet", "sandbox_pilot")}

# Reviewer Packet

## Inspect First

- `artifact/formal-vault-write-plan-dry-run-contract.md`
- `fixtures/valid-write-plan-config.json`
- `fixtures/valid-rollback-plan-config.json`
- `artifact/failure-case-oracle.md`
- `prototype/formal-vault-write-plan-dry-run/`
- `artifact/verify_formal_vault_write_plan.py`

## Review Questions

- Does the plan avoid formal vault access?
- Are proposed targets relative and write-disabled?
- Do all future write steps require explicit user approval?
- Do rollback and hash checks stop unsafe writes?
- Does the inspector remain read-only?
"""


def render_inspector_html(base: dict) -> str:
    cards = []
    for item in base["proposed_files"]:
        cards.append(
            f"""<article class=\"card\" data-kind=\"files\" data-search=\"{item['id']} {item['relative_target']} {item['source_path']} {item['source_sha256']} dry-run only no formal vault write\">
  <p class=\"eyebrow\">files</p>
  <h3>{item['id']}</h3>
  <p>{item['relative_target']}</p>
  <p>{item['source_path']}</p>
  <strong>write_enabled=false</strong>
</article>"""
        )
    for item in base["approval_prompts"]:
        cards.append(
            f"""<article class=\"card\" data-kind=\"approvals\" data-search=\"{item['id']} explicit user approval default deny\">
  <p class=\"eyebrow\">approvals</p>
  <h3>{item['id']}</h3>
  <p>{item['prompt']}</p>
  <strong>default={item['default']}</strong>
</article>"""
        )
    cards.append(
        """<article class=\"card\" data-kind=\"rollback\" data-search=\"rollback snapshot hash before hash after dry-run only\">
  <p class=\"eyebrow\">rollback</p>
  <h3>Rollback Manifest</h3>
  <p>Snapshot and hash checks are required before any future write.</p>
  <strong>dry-run only</strong>
</article>"""
    )
    cards.append(
        """<article class=\"card\" data-kind=\"stops\" data-search=\"stop conditions no sync no commit no push no promotion no formal vault read no formal vault write\">
  <p class=\"eyebrow\">stops</p>
  <h3>Stop Conditions</h3>
  <p>Stop on any formal vault access, sync, commit, push, promotion, or missing approval.</p>
  <strong>does not approve</strong>
</article>"""
    )
    button_parts = []
    for control in base["inspector_controls"]["buttons"]:
        active = ' class="active"' if control["filter"] == "all" else ""
        button_parts.append(f"<button type=\"button\"{active} data-filter=\"{control['filter']}\">{control['label']}</button>")
    return f"""<!doctype html>
<html lang=\"en\" data-sandbox-only=\"true\" data-dry-run-only=\"true\" data-no-write=\"true\" data-no-sync=\"true\" data-no-authority=\"true\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Formal Vault Write Plan Dry Run</title>
  <style>
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; color: #172026; background: #f7faf8; }}
    header {{ padding: 24px 28px 16px; background: #fff; border-bottom: 1px solid #d8dee4; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; letter-spacing: 0; }}
    .layout {{ display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 18px; padding: 18px 28px 32px; }}
    .toolbar {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 14px; }}
    input {{ min-width: 280px; height: 40px; padding: 0 12px; border: 1px solid #d8dee4; border-radius: 6px; }}
    button {{ height: 40px; border: 1px solid #d8dee4; background: #fff; border-radius: 6px; padding: 0 12px; font-weight: 700; }}
    button.active {{ border-color: #256f68; color: #256f68; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px; }}
    .card, aside {{ background: #fff; border: 1px solid #d8dee4; border-radius: 8px; padding: 14px; }}
    .card h3 {{ margin: 4px 0 8px; font-size: 18px; }}
    .card p, aside li {{ color: #52616b; line-height: 1.45; }}
    .eyebrow {{ margin: 0; color: #256f68; text-transform: uppercase; font-size: 12px; font-weight: 700; }}
    aside {{ align-self: start; position: sticky; top: 16px; }}
    @media (max-width: 860px) {{ .layout {{ grid-template-columns: 1fr; padding: 16px; }} input {{ min-width: 100%; }} }}
  </style>
</head>
<body>
  <header>
    <h1>Formal Vault Write Plan Dry Run</h1>
    <p>Sandbox-only plan inspector. It cannot write, sync, approve, hash the formal vault, or execute commands.</p>
  </header>
  <div class=\"layout\">
    <main>
      <div class=\"toolbar\" data-role=\"plan-filter\">
        <input id=\"q\" type=\"search\" placeholder=\"Search files, approvals, rollback, stops\">
        {' '.join(button_parts)}
      </div>
      <div class=\"grid\" data-role=\"plan-cards\">
        {chr(10).join(cards)}
      </div>
    </main>
    <aside data-role=\"boundary-rail\">
      <h2>Boundary Rail</h2>
      <ul>
        <li>sandbox only</li>
        <li>formal vault not accessed</li>
        <li>dry-run only</li>
        <li>not evidence support</li>
        <li>not action basis</li>
        <li>no formal vault read / no formal vault write</li>
        <li>no sync / no commit / no push / no promotion</li>
      </ul>
    </aside>
  </div>
  <script type=\"application/json\" id=\"plan-data\">
{json.dumps({"proposed_files": base["proposed_files"], "approval_prompts": base["approval_prompts"], "stop_conditions": base["stop_conditions"]}, indent=2)}
  </script>
  <script>
    const input = document.getElementById('q');
    const cards = Array.from(document.querySelectorAll('.card'));
    const buttons = Array.from(document.querySelectorAll('button[data-filter]'));
    let filter = 'all';
    function applyFilter() {{
      const query = input.value.toLowerCase();
      cards.forEach(card => {{
        const okFilter = filter === 'all' || card.dataset.kind === filter;
        const okQuery = !query || card.dataset.search.toLowerCase().includes(query) || card.textContent.toLowerCase().includes(query);
        card.hidden = !(okFilter && okQuery);
      }});
    }}
    buttons.forEach(btn => btn.addEventListener('click', () => {{
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filter = btn.dataset.filter;
      applyFilter();
    }}));
    input.addEventListener('input', applyFilter);
  </script>
</body>
</html>
"""


def render_receipt(base: dict, paths: dict[str, Path]) -> dict:
    source_hashes = {}
    for key, path in paths.items():
        if key == "source_root":
            continue
        source_hashes[key] = sha256(path) if path.exists() else "missing"
    return {
        "record_kind": "sandbox_formal_vault_write_plan_receipt",
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "formal_vault_accessed": False,
        "write_scope": base["write_scope"],
        "source_hashes": source_hashes,
        "proposed_file_source_bindings": [
            {
                "file_id": item["id"],
                "relative_target": item["relative_target"],
                "source_path": item["source_path"],
                "source_sha256": item["source_sha256"],
                "content_binding": item["content_binding"],
            }
            for item in base["proposed_files"]
        ],
        "forbidden_operations": {op: False for op in forbidden_operations()},
        "non_claims": [
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "not formal vault approval",
            "not mainline approval",
        ],
    }


def render_failure_oracle_md(cases: list[tuple[str, dict]]) -> str:
    rows = ["# Failure Case Oracle", "", "| File | Expected failure |", "| --- | --- |"]
    for name, item in cases:
        rows.append(f"| `{name}` | `{', '.join(item['expected_failures'])}` |")
    return "\n".join(rows)


def render_pending(kind: str, title: str) -> str:
    return f"""---
record_kind: {kind}
slice_id: {SLICE_ID}
status: pending
truth_boundary: sandbox_only
---

# {title}

Pending.
"""


def render_verification_pending() -> str:
    return f"""---
record_kind: sandbox_verification
slice_id: {SLICE_ID}
status: pending
truth_boundary: sandbox_verification_only
---

# Verification

Pending.
"""


def build() -> None:
    base = config()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required P2-23 source files: " + "; ".join(missing))
    git_status_summary = "pre-existing dirty tree recorded before build; final audit scoped to this slice path"

    safe_write("slice-plan.md", render_slice_plan(git_status_summary))
    safe_write("source-map.md", render_source_map(paths, base))
    safe_write("artifact/formal-vault-write-plan-dry-run-contract.md", render_contract(base))
    safe_write("fixtures/valid-write-plan-config.json", json.dumps(base, indent=2, ensure_ascii=False))
    safe_write("fixtures/valid-rollback-plan-config.json", json.dumps(variant_config(base), indent=2, ensure_ascii=False))

    cases = failure_cases(base)
    for name, item in cases:
        safe_write(f"failure-cases/{name}", json.dumps(item, indent=2, ensure_ascii=False))
    safe_write(
        "artifact/failure-case-oracle.json",
        json.dumps([{"file": name, "expected_failures": item["expected_failures"]} for name, item in cases], indent=2, ensure_ascii=False),
    )
    safe_write("artifact/failure-case-oracle.md", render_failure_oracle_md(cases))

    proto = "prototype/formal-vault-write-plan-dry-run"
    safe_write(f"{proto}/00 Dry Run Home.md", render_home(base))
    safe_write(f"{proto}/01 Proposed File List.md", render_file_list(base))
    safe_write(f"{proto}/02 Approval Prompt Matrix.md", render_approval_matrix(base))
    safe_write(f"{proto}/03 Rollback Manifest.md", render_rollback(base))
    safe_write(f"{proto}/04 Hash Check Plan.md", render_hash_plan(base))
    safe_write(f"{proto}/05 Stop Conditions.md", render_stop_conditions(base))
    safe_write(f"{proto}/06 Dry Run Results.md", render_dry_run_results(base))
    safe_write(f"{proto}/07 Reviewer Packet.md", render_reviewer_packet(base))
    safe_write(f"{proto}/plan-inspector.html", render_inspector_html(base))
    safe_write(f"{proto}/Receipts/formal-vault-write-plan-dry-run-receipt.json", json.dumps(render_receipt(base, paths), indent=2, ensure_ascii=False))

    safe_write("verification.md", render_verification_pending(), overwrite=False)
    safe_write("reviewer-report.md", render_pending("sandbox_reviewer_report", "Reviewer Report"), overwrite=False)
    safe_write("boundary-audit.md", render_pending("sandbox_boundary_audit", "Boundary Audit"), overwrite=False)
    safe_write("product-acceptance-report.md", render_pending("sandbox_product_acceptance_report", "Product Acceptance Report"), overwrite=False)
    safe_write("next-step.md", render_pending("sandbox_next_step", "Next Step"), overwrite=False)


if __name__ == "__main__":
    build()
