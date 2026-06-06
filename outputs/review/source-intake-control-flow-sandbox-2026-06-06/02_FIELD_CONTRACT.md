---
type: sandbox_field_contract
status: candidate_only
created_at: 2026-06-06
scope: source intake field contract
truth_boundary: candidate field contract only
---

# 02 Field Contract

## Source Card

Required:

```yaml
record_kind:
source_type:
source_url:
raw_location:
captured_at:
snapshot_ref_or_source_date:
topics:
why_saved:
knowledge_status: raw
processing_tier:
```

Forbidden:

```text
adopt/reject verdict
confidence
truth score
```

## Candidate Distillation

Required:

```yaml
record_kind:
derived_from:
knowledge_status: candidate
processing_tier: medium
retrieval_policy: orientation_only
promotion_gate: v0_2_13_required
```

Optional:

```yaml
candidate_points:
open_questions:
routing_hint:
possible_project_refs:
point_anchor_refs:
```

Forbidden:

```text
architecture decision
action basis
formal pattern
borrow_scope as project conclusion
project_non_borrow_scope as project conclusion
```

## Project Overlay Note

Required:

```yaml
record_kind: project_overlay
project_id:
target_ref:
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
project_borrow_scope:
project_non_borrow_scope:
project_reopen_trigger:
target_hint:
promotion_gate: v0_2_13_required
last_checked_at:
```

Forbidden:

```text
decision outcome
confidence
residual risk
review verdict
universal ban
global default retrieval
```

## Heavy Review Note

Required:

```yaml
claim:
evidence_anchors:
non_circular_warrant:
scope:
gaps:
residual_risk:
review_status:
```

Forbidden:

```text
auto-pass
truth score
action-facing anchor to candidate distillation
action-facing anchor to project overlay
action-facing anchor to retrieval score / evaluator / feedback event
```

## Feedback Event

Required:

```yaml
record_kind:
target_ref:
event_kind:
observed_in_context:
event_time:
review_pressure_effect:
project_ref:
```

Forbidden:

```text
truth_confidence_delta
source_reliability_delta
auto_mutate_reviewed_note
```

## Naming Repairs

```text
authority -> knowledge_status
retrieval_warning -> retrieval_policy
promotion_required -> promotion_gate
non_borrow_scope -> project_non_borrow_scope
borrow_scope -> project_borrow_scope
reopen_trigger -> project_reopen_trigger
```
