---
record_kind: candidate_distillation
status: fixture_candidate_only
truth_boundary: fixture only; not reviewed knowledge; not action basis
lifecycle_state: candidate_provisional
processing_tier: medium
knowledge_status: candidate
overlay_state: none
review_pressure: none
derived_from: raw/articles/example-source.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
v0_2_13_trigger: no
routing_hint:
  - retrieval_query_contract
possible_project_refs:
  - VAKS
point_anchor_refs:
  - snapshot_ref: raw/articles/example-source.md
    selector_type: text_quote
    selector_value: "Example quote used only as candidate anchor."
---

# Medium Candidate Distillation Fixture

## Candidate Points

```text
candidate point:
  Query intake should separate orientation from action-facing support.
```

## Boundary

This file does not say what VAKS should borrow.

It only says this candidate might route to retrieval/query design.
