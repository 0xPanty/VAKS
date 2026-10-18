---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint: []
possible_project_refs: []
point_anchor_refs: []
candidate_points:
  - kp_ref: KP-001
    point_text:
    point_type:
    source_anchor_ref:
    review_route:
    routing_hint: []
    uncertainty:
tags:
  - candidate
  - provisional
---

# Candidate Distillation

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, and suggest project overlays.

It is not:

```text
reviewed knowledge
decision
formal pattern
action basis
truth confidence
project borrowing verdict
```

## Source

```yaml
derived_from:
point_anchor_refs:
  - snapshot_ref:
    selector_type:
    selector_value:
```

## Candidate Points

Use stable local IDs:

```yaml
- kp_ref: KP-002
  point_text:
  point_type:
  source_anchor_ref:
  review_route:
  routing_hint: []
  uncertainty:
```

Do not convert candidate points into source tags.

## Open Questions


## Routing Hint


## Forbidden

```text
project_borrow_scope
project_non_borrow_scope
decision outcome
formal pattern
action basis
truth confidence
reviewed/adopted/action-basis tags
```
