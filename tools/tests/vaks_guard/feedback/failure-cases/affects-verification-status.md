---
record_kind: feedback_event
feedback_id: FB-FAIL-020
expected_failure_reason: FB_FORBIDDEN_DIRECT_EFFECT
event_type: decision_outcome
feedback_type: misleading
polarity: negative
project_ref: vaks
observed_in_context:
review_pressure_effect: review_due
review_due: true
affects: [review_due, verification_status]
effect_affects: []
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

Canonical affects lists verification status.

