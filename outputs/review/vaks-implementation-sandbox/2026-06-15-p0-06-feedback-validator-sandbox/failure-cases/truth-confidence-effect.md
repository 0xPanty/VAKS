---
record_kind: feedback_event
feedback_id: FB-FAIL-002
expected_failure_reason: FB_FORBIDDEN_DIRECT_EFFECT
event_type: answer_helpful
feedback_type: useful
polarity: positive
project_ref: vaks
observed_in_context:
review_pressure_effect: none
review_due: false
effect_affects: [usefulness, truth_confidence]
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
creates_reviewed_relation: false
promotes_reviewed_knowledge: false
---

# Failure

Feedback lists truth confidence as a direct effect.

