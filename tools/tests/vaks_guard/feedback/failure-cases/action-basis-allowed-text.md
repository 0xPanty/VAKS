---
record_kind: feedback_event
feedback_id: FB-FAIL-028
expected_failure_reason: FB_ACTION_BASIS_ALLOWED
event_type: answer_helpful
feedback_type: useful
polarity: positive
project_ref: vaks
observed_in_context:
review_pressure_effect: none
review_due: false
effect_affects: [usefulness]
direct_mutations: []
never_affects_directly: [truth_confidence, verification_status, source_reliability]
source_reliability_mutation_allowed: false
reviewed_note_mutation_allowed: false
mutates_reviewed_note: false
mutates_reviewed_relation: false
action_basis_allowed: yes for this action
warning_code: feedback_not_truth
global_negative_knowledge: false
review_completed: false
creates_reviewed_relation: false
promotes_reviewed_knowledge: false
---

# Failure

`action_basis_allowed` carries text rather than boolean true.

