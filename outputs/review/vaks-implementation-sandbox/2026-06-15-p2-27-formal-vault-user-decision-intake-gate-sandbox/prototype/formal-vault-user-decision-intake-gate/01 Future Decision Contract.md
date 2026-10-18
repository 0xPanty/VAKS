---
record_kind: sandbox_future_decision_contract
slice_id: 2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Future Decision Contract

| Rule | Value |
| --- | --- |
| `contract_kind` | `future_user_decision_intake_gate` |
| `current_slice_collects_approval` | `False` |
| `future_user_turn_required` | `True` |
| `actual_user_input_disallowed_in_this_slice` | `True` |
| `real_user_text_storage_disallowed_in_this_slice` | `True` |
| `future_user_exact_text_reference_required` | `True` |
| `exact_confirmation_phrases_required_for_approve` | `True` |
| `hash_match_required` | `True` |
| `deny_blocks_write` | `True` |
| `revise_blocks_write` | `True` |
| `extra_files_block_write` | `True` |
| `sync_commit_push_promotion_blocked` | `True` |
| `dirty_state_ack_required_for_approve` | `True` |
| `rollback_and_hash_ack_required_for_approve` | `True` |
| `approved_outcome_not_actionable_in_this_slice` | `True` |
| `separate_future_execution_slice_required` | `True` |
| `default_verdict` | `NEEDS_REVISION` |
| `required_packet_hash` | `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3` |
| `required_source_bundle_hash` | `4e7f8cdc4042a6858fcf42796843821391fe6c44e0e55e9e11206eda653f95ad` |
| `required_scope_hash` | `f5ec5589dc4e983bda3b274bae47766bc58424a98e40363a6437e94b93f5b4e2` |
| `required_rehearsal_hash` | `cfa4c69de3df0dde571a1a4912a17bcfbf75dac3a901f112a1b1b98d84bed72c` |
| `required_intake_gate_hash` | `f9f0f7a0ac4fc75bae06c492e82a38646d1ae88b1c99829b478f5ca10ce5cf96` |

## Required Hashes

- packet_hash: `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3`
- source_bundle_hash: `4e7f8cdc4042a6858fcf42796843821391fe6c44e0e55e9e11206eda653f95ad`
- scope_hash: `f5ec5589dc4e983bda3b274bae47766bc58424a98e40363a6437e94b93f5b4e2`
- rehearsal_hash: `cfa4c69de3df0dde571a1a4912a17bcfbf75dac3a901f112a1b1b98d84bed72c`
- intake_gate_hash: `f9f0f7a0ac4fc75bae06c492e82a38646d1ae88b1c99829b478f5ca10ce5cf96`

## Boundary

The contract is a gate definition only. It does not collect approval and does
not open any write path. A separate future execution slice is required before
any formal-vault write could be considered.
