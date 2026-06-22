---
record_kind: support_boundary_check
fixture_kind: failure_case
failure_id: feedback-as-support
target_ref: wiki/claims/example-claim.md#claim
proposed_support_ref: outputs/feedback/example-feedback-event.md
proposed_support_record_kind: feedback_event
proposed_support_authority_bucket: feedback
pack_role: support
support_claimed: true
evidence_role: direct_support
independent_anchor_ref:
anchor_type: none
anchor_selector:
feedback_used_as_support: true
expected_result: blocked
expected_failure_reason: feedback_as_support
---

# Failure: Feedback As Support

Feedback can create review pressure or tune activation. It cannot support truth.
