---
record_kind: heavy_review_note
status: fixture_candidate_only
truth_boundary: passing anchor fixture only; not reviewed knowledge; not action basis
lifecycle_state: heavy_review_open
processing_tier: heavy
knowledge_status: candidate
review_pressure: review_due
claim: "A future action-facing answer must anchor to raw source material."
evidence_anchors:
  - anchor_kind: raw_snapshot
    target_ref: raw/articles/example-source.md
    selector_type: text_quote
    selector_value: "Example source sentence."
    snapshot_ref_or_source_date: user_pasted_text_2026-06-06
non_circular_warrant: "The raw source sentence is the object being checked, not the candidate summary."
scope: sandbox anchor rule fixture
gaps: []
residual_risk:
  - "Fixture only; no real promotion."
review_status: open_not_passed
retrieval_policy:
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: heavy_review_not_passed
---

# Action-Facing Anchor Pass Fixture

This fixture demonstrates selector-grade anchor shape.

It is still not action basis because review has not passed.

