---
record_kind: heavy_review_note
status: fixture_expected_fail
truth_boundary: failing anchor fixture only; not reviewed knowledge; not action basis
lifecycle_state: heavy_review_open
processing_tier: heavy
knowledge_status: candidate
review_pressure: blocked
claim: "A future action-facing answer can cite candidate distillation as final support."
evidence_anchors:
  - anchor_kind: candidate_distillation
    target_ref: outputs/review/source-intake-control-flow-sandbox-2026-06-06/fixtures/candidate-distillation-medium.md
    selector_type: heading
    selector_value: "Candidate Points"
non_circular_warrant:
scope: sandbox negative fixture
gaps:
  - "Final support anchor points to candidate distillation instead of raw source or stable representation."
residual_risk:
  - "Would let polished candidate text replace source evidence."
review_status: blocked
retrieval_policy:
  pack_allowed: false
  action_basis_allowed: false
  warning_code: invalid_final_support_anchor
---

# Action-Facing Anchor Fail Fixture

This fixture is expected to be blocked.

It intentionally uses a candidate distillation as final support.

