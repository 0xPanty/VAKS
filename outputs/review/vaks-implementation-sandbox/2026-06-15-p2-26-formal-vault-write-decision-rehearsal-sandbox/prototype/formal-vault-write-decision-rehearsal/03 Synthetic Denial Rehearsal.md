---
record_kind: sandbox_decision_rehearsal_scenario
slice_id: 2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
---

# Synthetic Denial Rehearsal

| Field | Value |
| --- | --- |
| decision_verdict | `DENIED_BY_USER` |
| synthetic_only | `True` |
| actual_user_input | `False` |
| user_approval_text_present | `False` |
| expected_result | `BLOCKED_BY_SYNTHETIC_DENIAL` |
| formal_vault_write_allowed_now | `False` |
| action_basis_created | `False` |
| reviewed_knowledge_created | `False` |
| next_gate | `stop_and_record_denial_only` |
| required_rehearsal_hash | `cfa4c69de3df0dde571a1a4912a17bcfbf75dac3a901f112a1b1b98d84bed72c` |

## Hash Claims

- packet_hash: `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3`
- source_bundle_hash: `4e7f8cdc4042a6858fcf42796843821391fe6c44e0e55e9e11206eda653f95ad`
- scope_hash: `f5ec5589dc4e983bda3b274bae47766bc58424a98e40363a6437e94b93f5b4e2`

## Confirmed Questions

- none

## Boundary

This is not actual approval, not formal vault approval, not action basis, and
not permission to write.

## Next

- [[04 Synthetic Revision Rehearsal]]
- [[07 Stop Conditions]]
