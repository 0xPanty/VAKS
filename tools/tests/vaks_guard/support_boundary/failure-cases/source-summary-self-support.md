---
record_kind: support_boundary_check
fixture_kind: failure_case
failure_id: source-summary-self-support
target_ref: wiki/claims/example-source-summary-claim.md#claim
proposed_support_ref: wiki/summaries/example-source-summary.md
proposed_support_record_kind: source_summary
proposed_support_authority_bucket: reviewed
pack_role: support
support_claimed: true
evidence_role: direct_support
independent_anchor_ref:
anchor_type: none
anchor_selector:
source_summary_self_support: true
expected_result: blocked
expected_failure_reason: source_summary_self_support
---

# Failure: Source Summary Self-Support

A summary cannot replace inspected source anchors or support its own conclusion.
