---
record_kind: review_candidate
fixture_kind: failure_case
failure_id: fixed-approved-missing-body-hash
candidate_body_location: bodies/missing-hash-body.md
review_status: approved
writeback_ready: false
body_hash:
approval_integrity:
  approved_by: reviewer-example
  checked_body_hash:
expected_result: blocked
expected_failure_reason: fixed_or_approved_missing_body_hash
---

# Failure: Fixed Or Approved Missing Body Hash

An approved object must have a fixed body hash.
