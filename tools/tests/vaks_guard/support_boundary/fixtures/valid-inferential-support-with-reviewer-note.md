---
record_kind: support_boundary_check
fixture_kind: positive
fixture_id: valid-inferential-support-with-reviewer-note
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
reviewer_note: Reviewer must explain why this code anchor supports the relation before promotion.
rank_counted_as_support: false
score_counted_as_support: false
graph_rank_as_trust: false
retrieval_rank_as_trust: false
feedback_used_as_support: false
source_summary_self_support: false
claim_note_self_support: false
legacy_raw_metadata_used_as_support: false
expected_result: pass
---

# Fixture: Valid Inferential Support With Reviewer Note

This passes the boundary check because the support is anchored and inferential
support has a reviewer note.
