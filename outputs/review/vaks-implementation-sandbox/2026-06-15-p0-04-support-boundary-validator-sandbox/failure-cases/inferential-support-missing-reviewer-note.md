---
record_kind: support_boundary_check
fixture_kind: failure_case
failure_id: inferential-support-missing-reviewer-note
target_ref: wiki/patterns/example-pattern.md#relation
proposed_support_ref: raw/repos/example-repo/file.py#L10-L22
proposed_support_record_kind: code_anchor
proposed_support_authority_bucket: raw_anchor
pack_role: support
support_claimed: true
evidence_role: inferential_support
independent_anchor_ref: raw/repos/example-repo/file.py#L10-L22
anchor_type: code_line
anchor_selector: L10-L22
url_only: false
reviewer_note:
rank_counted_as_support: false
score_counted_as_support: false
graph_rank_as_trust: false
retrieval_rank_as_trust: false
feedback_used_as_support: false
source_summary_self_support: false
claim_note_self_support: false
legacy_raw_metadata_used_as_support: false
expected_result: blocked
expected_failure_reason: inferential_support_missing_reviewer_note
---

# Failure: Inferential Support Missing Reviewer Note

Inferential support needs a reviewer explanation before it can count as support.
