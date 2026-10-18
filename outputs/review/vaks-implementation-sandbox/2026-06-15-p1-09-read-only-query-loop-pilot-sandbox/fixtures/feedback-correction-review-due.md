---
record_kind: read_only_query_scenario
expected_valid: true
expected_outcome: review_due_envelope_truth_unchanged
expected_codes: []
scenario_id: ql-valid-feedback-correction
story_kind: feedback_correction
query_mode: review
requested_authority_bucket: feedback
included_buckets: [feedback]
selected_authority_buckets: [feedback]
selected_pack_roles: [review_input]
selected_action_basis_allowed: false
review_due_envelope_emitted: true
truth_mutation_attempted: false
feedback_changes_truth_confidence: false
reviewed_note_modified: false
---

# Feedback Correction Review Due

Explicit correction emits a sandbox review_due envelope while truth remains
unchanged.
