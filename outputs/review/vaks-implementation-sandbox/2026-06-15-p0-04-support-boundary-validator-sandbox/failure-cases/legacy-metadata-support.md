---
record_kind: support_boundary_check
fixture_kind: failure_case
failure_id: legacy-metadata-support
target_ref: wiki/claims/example-claim.md#claim
proposed_support_ref: raw/articles/example-source.md#legacy-metadata
proposed_support_record_kind: legacy_raw_metadata
proposed_support_authority_bucket: raw_anchor
pack_role: support
support_claimed: true
evidence_role: direct_support
independent_anchor_ref:
anchor_type: none
anchor_selector:
legacy_raw_metadata_used_as_support: true
expected_result: blocked
expected_failure_reason: legacy_metadata_support
---

# Failure: Legacy Metadata Support

Legacy raw metadata can help provenance repair but cannot count as support.
