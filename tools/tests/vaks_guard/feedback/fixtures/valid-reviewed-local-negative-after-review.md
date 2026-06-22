---
record_kind: feedback_event
feedback_id: FB-FIX-004
event_type: scope_mismatch
feedback_type: wrong_scope
polarity: negative
project_ref: vaks
observed_in_context:
review_pressure_effect: review_due
review_due: true
review_due_ref: review_due_candidate_FB_FIX_004
effect_affects: [scope_fit, review_due, scope_mismatch_candidate]
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
review_completed: true
creates_reviewed_relation: false
promotes_reviewed_knowledge: false
---

# Valid Scoped Negative Feedback After Review

Even when a related review has completed elsewhere, the feedback event itself
stays scoped and does not carry global negative knowledge.
