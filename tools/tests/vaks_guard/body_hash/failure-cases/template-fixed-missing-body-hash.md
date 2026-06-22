---
record_kind: review_candidate
fixture_kind: failure_case
failure_id: template-fixed-missing-body-hash
candidate_body_location: "# Candidate Body"
review_object_state: fixed_for_review
writeback_ready: false
body_hash:
approval_integrity:
  approved_by:
  checked_body_hash:
expected_result: blocked
expected_failure_reason: fixed_or_approved_missing_body_hash
---

# Review Candidate Fixture

# Candidate Body

This template-shaped fixed candidate is missing its body hash.
