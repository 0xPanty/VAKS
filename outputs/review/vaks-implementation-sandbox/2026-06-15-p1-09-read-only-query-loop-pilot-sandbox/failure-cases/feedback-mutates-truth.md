---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_FEEDBACK_MUTATES_TRUTH]
scenario_id: ql-fail-feedback-mutates-truth
story_kind: feedback_correction
query_mode: review
requested_authority_bucket: feedback
included_buckets: [feedback]
selected_authority_buckets: [feedback]
selected_pack_roles: [review_input]
review_due_envelope_emitted: true
truth_mutation_attempted: true
feedback_changes_truth_confidence: true
reviewed_note_modified: false
---

# Failure: Feedback Mutates Truth

Feedback correction directly changes truth confidence.
