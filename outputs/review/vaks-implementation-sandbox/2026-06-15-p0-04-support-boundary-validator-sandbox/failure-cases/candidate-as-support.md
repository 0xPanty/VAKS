---
record_kind: support_boundary_check
fixture_kind: failure_case
failure_id: candidate-as-support
target_ref: wiki/claims/example-claim.md#claim
proposed_support_ref: outputs/review/example-candidate-distillation.md
proposed_support_record_kind: candidate_distillation
proposed_support_authority_bucket: candidate
pack_role: support
support_claimed: true
evidence_role: direct_support
independent_anchor_ref:
anchor_type: none
anchor_selector:
url_only: false
expected_result: blocked
expected_failure_reason: candidate_as_support
---

# Failure: Candidate As Support

Candidate material can be review input, but it cannot be final support.
