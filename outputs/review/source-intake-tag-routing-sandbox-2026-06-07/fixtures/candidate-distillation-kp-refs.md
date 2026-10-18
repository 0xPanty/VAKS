---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from: fixture-source-confirmed-metadata
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
routing_hint:
  - retrieval
  - source-intake
possible_project_refs:
  - VAKS
point_anchor_refs:
  - snapshot_ref: fixture-source-confirmed-metadata
    selector_type: section
    selector_value: metadata-filtering
candidate_points:
  - kp_ref: KP-001
    point_text: "Business boundaries should be filtered before semantic ranking."
    point_type: pattern
    source_anchor_ref: fixture-source-confirmed-metadata#metadata-filtering
    review_route: instance_check
    routing_hint:
      - retrieval
      - metadata-filter
    uncertainty: "Needs VAKS local retrieval pressure test before promotion."
  - kp_ref: KP-002
    point_text: "Authority-like tags can cause candidate material to look reviewed."
    point_type: risk
    source_anchor_ref: fixture-source-confirmed-metadata#tag-risk
    review_route: risk_check
    routing_hint:
      - tag-policy
    uncertainty: "Strongly aligned with VAKS boundaries but still candidate."
tags:
  - candidate
  - provisional
---

# Fixture: Candidate Distillation With KP Refs

## Boundary

The candidate points can help routing and review.

They are not:

```text
reviewed knowledge
formal pattern
action basis
truth confidence
project borrow verdict
```

## Candidate Points

### KP-001

Business boundaries should be filtered before semantic ranking.

### KP-002

Authority-like tags can cause candidate material to look reviewed.
