---
record_kind: operation_receipt
status: template_sandbox
template_version: p0_02_sandbox_v1
operation_id:
operation_time:
actor:
actor_tier: read_only | suggest_only | candidate_write | reviewed_write | owner_final
operation_mode: read | suggest | propose_write | write | delete | schema_change
actual_write_performed: false
intent_confirmation:
  required:
  user_confirmed:
  restated_intent:
  success_criteria: []
basis:
  context_pack_ref:
  reviewed_support_refs: []
  candidate_refs: []
  feedback_refs: []
  retrieval_receipt_refs: []
  basis_boundary:
    context_pack_is_not_action_basis: true
    candidate_refs_are_not_action_basis: true
    feedback_refs_are_not_truth_or_basis: true
    retrieval_receipts_are_not_support: true
target_paths: []
proposed_changes: []
approval:
  required:
  approved_by:
  approval_source:
  approved_at:
  checked_body_hash:
  checked_body_hash_algorithm: sha256_body_canonical_v0
  approval_scope:
rollback:
  required:
  possible:
  rollback_plan:
result:
  status: not_started | proposed_only | skipped | performed | failed | rolled_back
  performed_at:
  output_refs: []
warnings: []
gaps: []
operation_boundary:
  receipt_not_truth: true
  receipt_not_review_approval: true
  receipt_not_reviewed_knowledge: true
  receipt_not_action_basis: true
  validator_pass_not_reviewer_approval: true
  sandbox_not_mainline: true
---

# Operation Receipt Template

## Purpose

An operation receipt records an attempted or proposed operation:

- who acted;
- which permission tier they had;
- what mode the operation used;
- whether intent confirmation was required and obtained;
- what basis was available;
- which paths were targeted;
- what changes were proposed or made;
- what approval and checked body hash were required;
- whether rollback was possible;
- what happened.

It does not create truth, reviewer approval, reviewed knowledge, or ready action
basis.

## Inputs

An operation receipt expects these inputs:

- actor identity or role;
- actor tier;
- operation mode;
- user intent or task statement;
- target paths;
- proposed change summary;
- basis references;
- approval facts when required;
- rollback plan when required;
- operation result.

## Outputs

A later reviewer or validator should be able to answer:

1. Was this actor allowed to do this kind of operation?
2. Was this only a suggestion, or was a write performed?
3. Was user intent confirmed when the action was significant?
4. Did the operation rely on reviewed support or only on candidates, feedback,
   retrieval, or a context pack?
5. Which exact paths were targeted?
6. Was approval required, and was the checked body hash recorded?
7. Could the operation be rolled back?
8. What was the final status?

## Actor Tier Matrix

| Actor tier | Allowed operation modes | Write allowed | Required guard |
|---|---|---:|---|
| `read_only` | `read` | No | Must not propose or perform writes as an action. |
| `suggest_only` | `read`, `suggest`, `propose_write` | No | May describe a proposed write, but must keep `actual_write_performed: false`. |
| `candidate_write` | `read`, `suggest`, `propose_write`, `write` | Candidate/sandbox only | Target path must be in an approved candidate or sandbox scope. |
| `reviewed_write` | `write` | Reviewed target only | Requires approval and `checked_body_hash`. |
| `owner_final` | `write`, `delete`, `schema_change` | Yes, if approved | Requires explicit owner approval, intent confirmation, and rollback plan when applicable. |

## Operation Mode Rules

`read`:

- no target write;
- no approval required unless reading protected/private material outside this
  sandbox contract.

`suggest`:

- no filesystem mutation;
- may produce advisory text in the current response or analysis surface;
- if an advisory record must be written to disk, that write is a separate
  `candidate_write` operation and needs its own approved sandbox or candidate
  write scope.

`propose_write`:

- no actual target write;
- proposed target and body must be visible;
- receipt records a proposal, not approval.

`write`:

- requires an actor tier that can write to the target scope;
- significant writes require intent confirmation;
- reviewed writes require approval and checked body hash.

`delete`:

- requires `owner_final`;
- requires rollback plan unless deletion is explicitly documented as
  non-reversible and accepted by owner.

`schema_change`:

- requires `owner_final`;
- requires approval, explicit intent confirmation, and rollback or migration
  plan.

## Basis Rules

`basis.context_pack_ref` can show what was assembled for attention. It is not
action basis by itself.

`basis.reviewed_support_refs` are the only field that can point toward
action-relevant support, and only when those references are already reviewed and
fit the specific action.

`basis.candidate_refs`, `basis.feedback_refs`, and
`basis.retrieval_receipt_refs` can explain orientation or review pressure. They
must not be treated as support, approval, reviewed knowledge, or action basis.

## Approval Rules

Approval is required when the operation is:

- a reviewed write;
- a schema change;
- destructive;
- a promotion or formal writeback;
- otherwise significant or hard to roll back.

For reviewed writes, `approval.checked_body_hash` must refer to the exact body
being approved. A later body hash mismatch means the operation is not approved
for that changed body.

This template records approval facts. It does not grant approval.

## Rollback Rules

Rollback is required for:

- `delete`;
- `schema_change`;
- reviewed write where the old body could be overwritten;
- high-impact writes;
- any operation that crosses from sandbox/candidate into formal architecture.

If rollback is impossible, the receipt must say so explicitly and the operation
requires owner-final acceptance before it can proceed.

## Status Values

Use `result.status` as follows:

| Status | Meaning |
|---|---|
| `not_started` | Receipt drafted before operation. |
| `proposed_only` | Proposal recorded; no write performed. |
| `skipped` | Operation intentionally not performed. |
| `performed` | Operation completed. |
| `failed` | Operation attempted and failed. |
| `rolled_back` | Operation was performed and then reverted by rollback plan. |

## Non-Claims

This operation receipt is not:

- a mainline template;
- a validator;
- reviewer approval;
- evidence support;
- truth confidence;
- reviewed knowledge;
- action basis;
- permission to modify protected files;
- permission to commit, push, sync, or run automation.
