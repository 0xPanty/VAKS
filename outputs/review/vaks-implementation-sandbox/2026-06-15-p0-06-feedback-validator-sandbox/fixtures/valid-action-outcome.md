---
record_kind: feedback_event
feedback_id: FB-FIX-003
event_type: action_outcome
feedback_type: stale
polarity: negative
project_ref: vaks
observed_in_context: action-outcome-example
review_pressure_effect: review_due
review_due: true
review_due_ref: review_due_candidate_FB_FIX_003
effect_affects: [usefulness, scope_fit, review_due, implementation_note_candidate]
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
---

# Valid Action Outcome

An action outcome can create review_due and future routing calibration. It does
not become truth.

