---
record_kind: review_candidate
fixture_kind: failure_case
failure_id: writeback-ready-body-changed
candidate_body_location: bodies/writeback-changed-body.md
review_status: writeback_ready
writeback_ready: true
body_hash: e1014d39422754ccdc6a5e609faf6266a8eddb9e4c6394c74685c3b4eb50932b
approval_integrity:
  approved_by: reviewer-example
  checked_body_hash:
expected_result: blocked
expected_failure_reason: writeback_ready_body_changed
---

# Failure: Writeback-Ready Body Changed

A writeback-ready record cannot keep ready status when its body no longer
matches the fixed body hash.
