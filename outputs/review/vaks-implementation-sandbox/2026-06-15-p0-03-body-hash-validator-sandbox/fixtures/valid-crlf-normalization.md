---
record_kind: review_candidate
fixture_kind: positive
fixture_id: valid-crlf-normalization
candidate_body_location: bodies/crlf-normalization-body.md
review_object_state: fixed_for_review
writeback_ready: false
body_hash: 2f9ce0b72be8c99f2560d28081f32ace70d5ff46c732191ea75ca22158af8e3e
approval_integrity:
  approved_by:
  checked_body_hash:
expected_result: pass
---

# Fixture: Valid CRLF Normalization

The stored file uses repository line endings, and verification additionally
checks that an equivalent CRLF string hashes to the same value.
