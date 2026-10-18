---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_FEEDBACK_REVIEW_DUE_MISSING]
scenario_id: ql-fail-feedback-review-due-missing
story_kind: feedback_correction
query_mode: review
requested_authority_bucket: feedback
included_buckets: [feedback]
selected_authority_buckets: [feedback]
selected_pack_roles: [review_input]
review_due_envelope_emitted: false
truth_mutation_attempted: false
feedback_changes_truth_confidence: false
---

# Failure: Feedback Review Due Missing

Explicit correction produces no review_due pressure.
