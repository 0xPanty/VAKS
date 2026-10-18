---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p0-02-operation-receipt-template-sandbox
status: ready_for_reviewer
truth_boundary: validator_fixture_guidance_only
---

# Failure Case Oracle

This oracle maps each failure case to one expected primary failure reason. It is
for future validator pilots and reviewer inspection. It is not a validator and
does not approve any operation.

| Failure case | Expected primary failure reason |
|---|---|
| `read-only-actor-write.md` | `read_only_actor_cannot_write` |
| `suggest-only-actor-write.md` | `suggest_only_actor_cannot_perform_write` |
| `reviewed-write-missing-approval-hash.md` | `reviewed_write_missing_checked_body_hash` |
| `checked-body-hash-mismatch.md` | `checked_body_hash_mismatch` |
| `schema-change-without-owner-final.md` | `schema_change_requires_owner_final` |
| `destructive-delete-without-rollback.md` | `destructive_operation_missing_rollback_plan` |
| `missing-intent-confirmation.md` | `required_intent_confirmation_missing` |
| `candidate-ref-as-action-basis.md` | `candidate_ref_used_as_action_basis` |
| `receipt-claims-truth-or-approval.md` | `operation_receipt_claims_authority` |

## Isolation Note

The files are still readable as boundary stories, but the frontmatter now gives
future validators a single expected primary reason. If a later validator reports
additional warnings, those warnings should be treated as secondary unless they
prevent the primary reason from being tested.
