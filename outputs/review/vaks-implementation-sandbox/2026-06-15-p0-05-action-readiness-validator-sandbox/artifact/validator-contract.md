---
record_kind: sandbox_validator_contract
slice_id: 2026-06-15-p0-05-action-readiness-validator-sandbox
artifact: artifact/action_readiness_validator_sandbox.py
truth_boundary: validator_contract_for_sandbox_only
---

# Validator Contract

## Purpose

The validator blocks records that claim `action_readiness: ready` while the basis
still contains P0-05 blockers.

It is a negative boundary validator. It does not decide that an action should be
taken, does not create evidence support, does not approve writeback, and does
not promote anything to mainline architecture.

## Input

One Markdown file with flat frontmatter:

```yaml
record_kind: action_readiness_check
action_id: AR-001
action_readiness: ready | not_ready | risky | needs_review
action_basis_ready_claimed: true | false
action_mode: answer | decision | implementation | propose_write | write | delete | schema_change | deploy
operation_mode: read | suggest | propose_write | write | delete | schema_change
actor_tier: read_only | suggest_only | builder | reviewer | owner
significant_action: true | false
evidence_sufficiency: sufficient | weak | insufficient | out_of_scope | risky | unchecked
evidence_support_status: supported | unsupported | unclear | missing_anchor | not_checked | self_support_loop
temporal_applicability: current | stale | superseded | out_of_scope | unchecked
action_basis_ref:
reviewed_support_refs:
evidence_packet_ref:
replacement_basis_ref:
narrowed_scope_ref:
unresolved_risk: true | false
warnings_or_gaps_trimmed: true | false
missing_evidence_trimmed: true | false
intent_confirmation_required: true | false
intent_confirmed: true | false
success_criteria_present: true | false
basis_materials: [reviewed_support, evidence_packet]
reviewed_write: true | false
target_bucket:
approved: true | false
checked_body_hash_present: true | false
rollback_required: true | false
rollback_plan_present: true | false
owner_final: true | false
```

Only `record_kind`, `action_id`, and `action_readiness` are structurally
required. Readiness checks run only when the record claims ready by either:

```text
action_readiness: ready
action_basis_ready_claimed: true
```

## Output

Text mode:

```text
PASS action_readiness <path>
```

or:

```text
FAIL action_readiness <path>
<CODE>: <message>
```

JSON mode:

```json
{
  "status": "pass",
  "record": "path",
  "action_id": "AR-001",
  "issues": []
}
```

## Blocking Codes

```text
AR_INSUFFICIENT_EVIDENCE_READY
AR_OUT_OF_SCOPE_READY
AR_UNRESOLVED_RISK_READY
AR_EVIDENCE_SUFFICIENCY_NOT_SUFFICIENT
AR_SUPPORT_NOT_SUPPORTED_READY
AR_STALE_SUPERSEDED_WITHOUT_REPLACEMENT_READY
AR_HIDDEN_WARNING_OR_GAP_READY
AR_MISSING_INTENT_CONFIRMATION
AR_MISSING_SUCCESS_CRITERIA
AR_CANDIDATE_BASIS_READY
AR_FEEDBACK_BASIS_READY
AR_RETRIEVAL_RANK_BASIS_READY
AR_SOURCE_SUMMARY_BASIS_READY
AR_CONTEXT_PACK_ONLY_READY
AR_DIAGNOSTIC_BASIS_READY
AR_MISSING_REVIEWED_ACTION_BASIS
AR_REVIEWED_WRITE_MISSING_APPROVAL
AR_REVIEWED_WRITE_MISSING_CHECKED_BODY_HASH
AR_DESTRUCTIVE_MISSING_ROLLBACK
AR_READ_ONLY_ACTOR_WRITE
AR_SCHEMA_CHANGE_MISSING_OWNER_FINAL
```

Ready records must have:

```text
evidence_sufficiency: sufficient
intent_confirmed: true for significant action
reviewed_support, evidence_packet, action_basis_ref, reviewed_support_refs, or evidence_packet_ref
rollback_plan_present: true for delete/schema_change/hard-to-rollback actions
owner_final: true for schema_change
```

`intent_confirmation_required: false` cannot self-exempt a significant action
from intent confirmation.

## Authority Boundary

Validator pass means only:

```text
no modeled P0-05 blocker was found in this record
```

Validator pass does not mean:

```text
reviewer approval
product acceptance
evidence support
reviewed knowledge
formal action basis
mainline readiness
permission to write
```
