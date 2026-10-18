---
record_kind: review_candidate
fixture_kind: positive
fixture_id: valid-heading-normalization
candidate_body_location: bodies/heading-normalized-body.md
review_status: fixed
writeback_ready: false
body_hash: eae10daa1abaf21f742f906f1f3222f03de23a1c85f890cf41817ddc8cdd77ee
approval_integrity:
  approved_by:
  checked_body_hash:
expected_result: pass
---

# Fixture: Valid Heading Normalization

The hash excludes the first Markdown heading and hashes the remaining canonical
body.
