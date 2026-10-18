---
record_kind: sandbox_decision_rules
slice_id: 2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
---

# Decision Rules

| Rule | Value |
| --- | --- |
| `synthetic_only` | `True` |
| `actual_user_input_disallowed` | `True` |
| `actual_approval_collection_disallowed` | `True` |
| `approved_outcome_not_actionable` | `True` |
| `requires_packet_hash` | `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3` |
| `requires_source_bundle_hash` | `4e7f8cdc4042a6858fcf42796843821391fe6c44e0e55e9e11206eda653f95ad` |
| `requires_scope_hash` | `f5ec5589dc4e983bda3b274bae47766bc58424a98e40363a6437e94b93f5b4e2` |
| `deny_always_blocks_write` | `True` |
| `revise_always_blocks_write` | `True` |
| `extra_files_always_block` | `True` |
| `sync_commit_push_promotion_always_block` | `True` |
| `dirty_state_blocks_write` | `True` |
| `rollback_and_hash_ack_required_for_approved` | `True` |

## Required Question IDs For Synthetic Approval

- `future_approve_exact_scope`
- `future_approve_source_bindings`
- `future_approve_rollback_hash_checks`
- `future_approve_no_sync_commit_push_promotion`

## Boundary

The rules classify synthetic scenarios only. They do not ask the user and do
not approve any formal vault operation.
