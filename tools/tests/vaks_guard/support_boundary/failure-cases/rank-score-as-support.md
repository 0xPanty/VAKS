---
record_kind: support_boundary_check
fixture_kind: failure_case
failure_id: rank-score-as-support
target_ref: wiki/claims/example-claim.md#claim
proposed_support_ref: outputs/review/example-query-result.md#rank-1
proposed_support_record_kind: retrieval_result
proposed_support_authority_bucket: raw_anchor
pack_role: support
support_claimed: true
evidence_role: direct_support
independent_anchor_ref: raw/articles/example-source.md#L20-L28
anchor_type: raw_span
anchor_selector: L20-L28
url_only: false
rank_counted_as_support: true
score_counted_as_support: true
graph_rank_as_trust: true
retrieval_rank_as_trust: true
expected_result: blocked
expected_failure_reason: rank_or_score_as_support_or_trust
---

# Failure: Rank Or Score As Support

Even with an anchor, rank and score cannot be treated as support or trust.
