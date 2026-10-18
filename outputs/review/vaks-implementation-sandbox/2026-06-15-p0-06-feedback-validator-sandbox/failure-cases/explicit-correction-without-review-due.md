---
record_kind: feedback_event
feedback_id: FB-FAIL-009
expected_failure_reason: FB_EXPLICIT_CORRECTION_WITHOUT_REVIEW_DUE
event_type: explicit_correction
feedback_type: missing
polarity: neutral
project_ref: vaks
observed_in_context:
review_pressure_effect: none
review_due: false
review_due_ref:
effect_affects: [activation_ranking]
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

Explicit correction lacks review_due.

