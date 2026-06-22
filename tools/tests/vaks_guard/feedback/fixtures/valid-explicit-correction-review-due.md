---
record_kind: feedback_event
feedback_id: FB-FIX-002
event_type: explicit_correction
feedback_type: contradicted
polarity: negative
project_ref:
observed_in_context: p0-06-sandbox-verification
review_pressure_effect: review_due
review_due: true
review_due_ref: review_due_candidate_FB_FIX_002
effect_affects: [review_due, activation_ranking, missing_evidence_candidate]
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

# Valid Explicit Correction

The correction creates review pressure and candidate follow-up, not truth
mutation.

