---
record_kind: sandbox_approval_prompt_matrix
slice_id: 2026-06-15-p2-24-formal-vault-write-plan-dry-run-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
---

# Approval Prompt Matrix

| Prompt ID | Required Phrase | Applies To | Default | Excludes | Blocks |
| --- | --- | --- | --- | --- | --- |
| `approve_formal_vault_write_scope` | `APPROVE ONLY LISTED FILES FOR FUTURE FORMAL VAULT WRITE` | native_home, status_board, receipt_index, boundary_stop, readonly_inspector | `deny` | obsidian_sync, commit, push, promotion | formal_vault_write, obsidian_sync, real_base_files |
| `approve_rollback_manifest` | `APPROVE ROLLBACK AND HASH CHECKS BEFORE FUTURE WRITE` | native_home, status_board, receipt_index, boundary_stop, readonly_inspector | `deny` | obsidian_sync, commit, push, promotion | formal_vault_write |
| `approve_no_sync_after_write` | `APPROVE NO SYNC COMMIT PUSH OR PROMOTION IN FUTURE WRITE SLICE` | native_home, status_board, receipt_index, boundary_stop, readonly_inspector | `deny` | obsidian_sync, commit, push, promotion | obsidian_sync |

## Boundary

Approval prompts are future gates only. They are not current approval, not
mainline approval, and not permission to write, sync, commit, push, or promote.
Every approval must cite plan version `p2-24-dry-run-v1` and a future
plan hash before it can be considered in a later approved slice.

## Next

- [[03 Rollback Manifest]]
- [[05 Stop Conditions]]
