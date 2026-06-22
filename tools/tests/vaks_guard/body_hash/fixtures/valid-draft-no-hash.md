---
record_kind: review_candidate
fixture_kind: positive
fixture_id: valid-draft-no-hash
candidate_body_location: bodies/draft-body.md
review_status: draft
writeback_ready: false
body_hash:
approval_integrity:
  approved_by:
  checked_body_hash:
expected_result: pass
expected_warning: body_hash_not_required_for_draft
---

# Fixture: Valid Draft Without Hash

Draft records can exist before the object is fixed for review. The validator may
warn, but it should not block this draft.
