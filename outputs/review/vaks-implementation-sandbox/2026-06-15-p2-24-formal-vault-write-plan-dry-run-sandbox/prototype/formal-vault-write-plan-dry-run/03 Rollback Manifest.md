---
record_kind: sandbox_rollback_manifest
slice_id: 2026-06-15-p2-24-formal-vault-write-plan-dry-run-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
---

# Rollback Manifest

## Required Before Any Future Write

- snapshot_root_label: `future-approved-snapshot-root`
- retention_policy: keep until user confirms future formal write succeeded and rollback window can close
- snapshot_before_write_required: `True`
- hash_before_required: `True`
- hash_after_required: `True`
- hash_algorithm: `sha256`
- record_format: `json-lines: target, operation, before_state, before_hash, after_hash, rollback_action, verification_result`
- unexpected_file_abort: `True`
- unexpected_hash_drift_abort: `True`
- dirty_state_abort: `True`
- rollback_after_verification_required: `True`
- rollback_requires_user_confirmation: `True`

## Per-File Rollback Semantics

| File ID | Relative Target | Operation | Before State | Snapshot Label | Rollback Action | Post-Rollback Verification |
| --- | --- | --- | --- | --- | --- | --- |
| `native_home` | `VAKS-Workbench-Draft/00 Native Home.md` | `create_or_replace` | `unknown_until_future_approved_snapshot` | `future-approved-snapshot-root/VAKS-Workbench-Draft/00 Native Home.md` | `restore_previous_if_existed_else_delete_created_file` | `hash_matches_before_or_file_absent_if_new` |
| `status_board` | `VAKS-Workbench-Draft/02 Status Board.md` | `create_or_replace` | `unknown_until_future_approved_snapshot` | `future-approved-snapshot-root/VAKS-Workbench-Draft/02 Status Board.md` | `restore_previous_if_existed_else_delete_created_file` | `hash_matches_before_or_file_absent_if_new` |
| `receipt_index` | `VAKS-Workbench-Draft/03 Receipt Index.md` | `create_or_replace` | `unknown_until_future_approved_snapshot` | `future-approved-snapshot-root/VAKS-Workbench-Draft/03 Receipt Index.md` | `restore_previous_if_existed_else_delete_created_file` | `hash_matches_before_or_file_absent_if_new` |
| `boundary_stop` | `VAKS-Workbench-Draft/04 Boundary Stop.md` | `create_or_replace` | `unknown_until_future_approved_snapshot` | `future-approved-snapshot-root/VAKS-Workbench-Draft/04 Boundary Stop.md` | `restore_previous_if_existed_else_delete_created_file` | `hash_matches_before_or_file_absent_if_new` |
| `readonly_inspector` | `VAKS-Workbench-Draft/readonly-inspector.html` | `create_or_replace` | `unknown_until_future_approved_snapshot` | `future-approved-snapshot-root/VAKS-Workbench-Draft/readonly-inspector.html` | `restore_previous_if_existed_else_delete_created_file` | `hash_matches_before_or_file_absent_if_new` |

## Boundary

Rollback planning is not rollback execution. No formal vault file is read,
snapshotted, written, or restored in this slice.

## Next

- [[04 Hash Check Plan]]
- [[05 Stop Conditions]]
