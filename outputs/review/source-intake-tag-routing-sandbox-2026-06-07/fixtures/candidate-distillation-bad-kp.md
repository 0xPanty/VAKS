---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
candidate_points:
  - kp_ref: KP-reviewed-001
    point_text: "Bad ID encodes authority."
    point_type: pattern
    source_anchor_ref: fixture#bad
    review_route: instance_check
  - kp_ref: KP-reviewed-001
    point_text: "Duplicate ID."
    point_type: risk
    source_anchor_ref: fixture#bad-duplicate
    review_route: risk_check
tags:
  - candidate
---

# Fixture: Bad KP IDs

## Expected Behavior

This file must fail KP lint because:

```text
KP-reviewed-001 contains authority wording.
KP-reviewed-001 appears twice.
```
