---
record_kind: sandbox_validator_contract
slice_id: 2026-06-15-p0-06-feedback-validator-sandbox
artifact: artifact/feedback_validator_sandbox.py
truth_boundary: validator_contract_for_sandbox_only
---

# Validator Contract

## Purpose

The validator blocks feedback-event records that directly mutate truth,
verification, source reliability, reviewed notes, reviewed relations, action
basis, or promotion state.

It is a negative boundary validator. It does not decide that feedback is correct,
does not create review_due by itself, does not write feedback logs, and does not
promote reviewed knowledge.

## Input

One Markdown file with flat frontmatter:

```yaml
record_kind: feedback_event
feedback_id: FB-001
event_type: explicit_correction | answer_helpful | action_outcome | decision_outcome | scope_mismatch | stale
feedback_type: useful | irrelevant | misleading | wrong_scope | stale | missing | contradicted | incomplete | too_weak | too_broad
polarity: positive | negative | neutral
project_ref:
observed_in_context:
review_pressure_effect: none | review_due | blocked | needs_review
review_due: true | false
review_due_ref:
affects: [usefulness, scope_fit, activation_ranking, review_due]
effect_affects: [usefulness, scope_fit, activation_ranking, review_due]
direct_mutations: []
never_affects_directly: [truth_confidence, verification_status, source_reliability]
truth_confidence_delta:
confidence_delta:
truth_confidence:
verification_status_delta:
verification_status:
source_reliability_delta:
source_reliability:
source_reliability_mutation_allowed: false
reviewed_note_mutation_allowed: false
mutates_reviewed_note: false
mutates_reviewed_relation: false
reviewed_relation_strength_delta:
action_basis_allowed: false
warning_code: feedback_not_truth
global_negative_knowledge: false
review_completed: false
creates_reviewed_relation: false
promotes_reviewed_knowledge: false
```

Required structural fields:

```text
record_kind or record_type
feedback_id
event_type or event_kind
project_ref or observed_in_context
```

Allowed direct effects in either `affects` or `effect_affects`:

```text
usefulness
scope_fit
activation_ranking
review_due
future_recommendation
risk_calibration
option_framing
missing_point_candidate
missing_evidence_candidate
scope_mismatch_candidate
implementation_note_candidate
decision_follow_up_candidate
```

Forbidden direct effects:

```text
truth_confidence
truth_confidence_delta
truth_score
confidence_delta
verification_status
verification_status_delta
source_reliability
source_reliability_delta
decision_outcome
reviewed_note
reviewed_note_mutation
reviewed_relation
reviewed_relation_strength
reviewed_relation_strength_delta
reviewed_relation_mutation
```

`affects` is the canonical field from `FEEDBACK.md`; `effect_affects` is accepted
as a sandbox-flat alias. The validator checks both and treats them as one effect
set.

## Output

Text mode:

```text
PASS feedback_event <path>
```

or:

```text
FAIL feedback_event <path>
<CODE>: <message>
```

JSON mode:

```json
{
  "status": "pass",
  "record": "path",
  "feedback_id": "FB-001",
  "issues": []
}
```

## Blocking Codes

```text
FB_FORBIDDEN_DIRECT_EFFECT
FB_TRUTH_CONFIDENCE_MUTATION
FB_VERIFICATION_STATUS_MUTATION
FB_SOURCE_RELIABILITY_MUTATION
FB_REVIEWED_NOTE_MUTATION
FB_REVIEWED_RELATION_MUTATION
FB_EXPLICIT_CORRECTION_WITHOUT_REVIEW_DUE
FB_NEGATIVE_WITHOUT_REVIEW_PRESSURE
FB_ACTION_BASIS_ALLOWED
FB_MISSING_FEEDBACK_NOT_TRUTH_WARNING
FB_GLOBAL_NEGATIVE_KNOWLEDGE_FROM_LOCAL_FEEDBACK
FB_MISSING_SCOPE_BINDING
FB_PROMOTION_FROM_FEEDBACK
FB_UNKNOWN_EFFECT
FB_INCOMPLETE_NEVER_AFFECTS_DIRECTLY
```

## Authority Boundary

Validator pass means only:

```text
no modeled P0-06 feedback boundary blocker was found in this record
```

Validator pass does not mean:

```text
feedback correctness
review_due approval
truth mutation approval
source reliability change
reviewed note/relation mutation
evidence support
reviewed knowledge
action basis
mainline readiness
permission to write
```

`global_negative_knowledge: true` is always invalid on a feedback-event record.
If review later creates negative knowledge, that state belongs in a review or
decision artifact, not in the feedback event.

Dangerous authority fields are fail-closed: any non-empty value other than
`false`, `no`, `0`, `none`, or `null` counts as enabled and is blocked. This
applies to fields such as `source_reliability_mutation_allowed`,
`mutates_reviewed_note`, `mutates_reviewed_relation`, `action_basis_allowed`,
`global_negative_knowledge`, `creates_reviewed_relation`, and
`promotes_reviewed_knowledge`.
