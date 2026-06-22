---
record_kind: support_boundary_check
fixture_kind: failure_case
failure_id: url-only-direct-support
target_ref: wiki/claims/example-claim.md#claim
proposed_support_ref: https://example.com/source
proposed_support_record_kind: source_url
proposed_support_authority_bucket: raw_anchor
pack_role: support
support_claimed: true
evidence_role: direct_support
independent_anchor_ref: https://example.com/source
anchor_type: url_only
anchor_selector:
url_only: true
expected_result: blocked
expected_failure_reason: url_only_direct_support
---

# Failure: URL-Only Direct Support

URL-only provenance is not direct support.
