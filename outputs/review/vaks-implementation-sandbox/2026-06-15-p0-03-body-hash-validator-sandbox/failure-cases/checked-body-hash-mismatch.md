---
record_kind: review_candidate
fixture_kind: failure_case
failure_id: checked-body-hash-mismatch
candidate_body_location: bodies/checked-hash-mismatch-body.md
review_status: approved
writeback_ready: false
body_hash: 62be652b39aea6f9f663ad2dc541a093971e4a5ac0187bd1d6cea403def57c7a
approval_integrity:
  approved_by: reviewer-example
  checked_body_hash: e1014d39422754ccdc6a5e609faf6266a8eddb9e4c6394c74685c3b4eb50932b
expected_result: blocked
expected_failure_reason: checked_body_hash_mismatch
---

# Failure: Checked Body Hash Mismatch

The body hash is current, but the approval hash points to a different body.
