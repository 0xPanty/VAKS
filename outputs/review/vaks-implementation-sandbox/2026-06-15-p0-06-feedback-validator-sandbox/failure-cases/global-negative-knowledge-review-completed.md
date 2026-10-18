---
record_kind: feedback_event
feedback_id: FB-FAIL-018
expected_failure_reason: FB_GLOBAL_NEGATIVE_KNOWLEDGE_FROM_LOCAL_FEEDBACK
event_type: scope_mismatch
feedback_type: wrong_scope
polarity: negative
project_ref: vaks
observed_in_context:
review_pressure_effect: review_due
review_due: true
effect_affects: [scope_fit, review_due]
direct_mutations: []
never_affects_directly: [truth_confidence, verification_status, source_reliability]
source_reliability_mutation_allowed: false
reviewed_note_mutation_allowed: false
mutates_reviewed_note: false
mutates_reviewed_relation: false
action_basis_allowed: false
warning_code: feedback_not_truth
global_negative_knowledge: true
review_completed: true
creates_reviewed_relation: false
promotes_reviewed_knowledge: false
---

# Failure

Review completion does not make global negative knowledge a feedback-event field.

