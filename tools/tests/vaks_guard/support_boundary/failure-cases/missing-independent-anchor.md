---
record_kind: support_boundary_check
fixture_kind: failure_case
failure_id: missing-independent-anchor
target_ref: wiki/claims/example-claim.md#claim
proposed_support_ref: raw/articles/example-source.md
proposed_support_record_kind: raw_source_span
proposed_support_authority_bucket: raw_anchor
pack_role: support
support_claimed: true
evidence_role: direct_support
independent_anchor_ref:
anchor_type: none
anchor_selector:
url_only: false
rank_counted_as_support: false
score_counted_as_support: false
graph_rank_as_trust: false
retrieval_rank_as_trust: false
feedback_used_as_support: false
source_summary_self_support: false
claim_note_self_support: false
legacy_raw_metadata_used_as_support: false
expected_result: blocked
expected_failure_reason: support_claim_missing_independent_anchor
---

# Failure: Missing Independent Anchor

A direct support claim must name a current independent anchor and selector.
