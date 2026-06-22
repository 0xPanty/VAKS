---
record_kind: support_boundary_check
fixture_kind: failure_case
failure_id: claim-note-self-support-loop
target_ref: wiki/claims/example-claim.md#claim
proposed_support_ref: wiki/claims/example-claim.md#claim
proposed_support_record_kind: claim_note
proposed_support_authority_bucket: reviewed
pack_role: support
support_claimed: true
evidence_role: direct_support
independent_anchor_ref:
anchor_type: none
anchor_selector:
claim_note_self_support: true
expected_result: blocked
expected_failure_reason: claim_note_self_support_loop
---

# Failure: Claim Note Self-Support Loop

A claim note cannot cite itself as support.
