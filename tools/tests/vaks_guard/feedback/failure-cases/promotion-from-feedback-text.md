---
record_kind: feedback_event
feedback_id: FB-FAIL-030
expected_failure_reason: FB_PROMOTION_FROM_FEEDBACK
event_type: explicit_correction
feedback_type: contradicted
polarity: negative
project_ref: vaks
observed_in_context:
review_pressure_effect: review_due
review_due: true
effect_affects: [review_due]
direct_mutations: []
never_affects_directly: [truth_confidence, verification_status, source_reliability]
source_reliability_mutation_allowed: false
reviewed_note_mutation_allowed: false
mutates_reviewed_note: false
mutates_reviewed_relation: false
action_basis_allowed: false
warning_code: feedback_not_truth
global_negative_knowledge: false
review_completed: false
creates_reviewed_relation: create reviewed relation now
promotes_reviewed_knowledge: false
---

# Failure

`creates_reviewed_relation` carries text rather than boolean true.

