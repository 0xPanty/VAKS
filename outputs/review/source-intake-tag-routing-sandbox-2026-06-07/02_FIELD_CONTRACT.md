---
type: sandbox_field_contract
status: candidate_only
created_at: 2026-06-07
scope: source intake metadata field contract
truth_boundary: candidate field contract only
---

# Field Contract

## Source Card

Required hard boundary fields:

```yaml
source_type:
captured_at:
source_url:
raw_location:
processing_tier:
knowledge_status: raw
retrieval_policy:
promotion_gate:
```

Recommended confirmed discovery fields:

```yaml
topics: []
content_form:
language:
version_or_time_scope:
entities: []
aliases: []
entity_refs: []
tags: []
```

Allowed meaning:

```text
findability
filtering
routing
source inspection
context-pack preparation
```

Forbidden meaning:

```text
reviewed
approved
adopted
truth
safe
action basis
decision
project borrowing verdict
source reliability
confidence
```

## Candidate Distillation

Required boundary fields:

```yaml
record_kind: candidate_distillation
provisional: true
knowledge_status: candidate
processing_tier: medium
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
```

Recommended knowledge-point fields:

```yaml
candidate_points:
  - kp_ref: KP-001
    point_text:
    point_type:
    source_anchor_ref:
    review_route:
    routing_hint: []
    uncertainty:
```

Forbidden:

```text
project_borrow_scope
project_non_borrow_scope
reviewed/adopted/action basis wording
truth confidence
formal pattern
decision outcome
authority tags
```

## Project Overlay

Required project-scoped fields:

```yaml
record_kind: project_overlay
knowledge_status: candidate
overlay_state: confirmed
overlay_scope: project_sidecar_only
retrieval_scope: active_project_only
project_id:
target_ref:
project_borrow_scope:
project_non_borrow_scope:
project_reopen_trigger:
target_hint:
```

Forbidden:

```text
universal ban
review verdict
truth confidence
action basis
decision outcome
generic source-card rewrite
```

## Query Run

Query run records dynamic understanding and retrieval trace.

```yaml
query_understanding:
  action_facing:
  project_scope:
  extracted_topics: []
  extracted_entities: []
  source_type_filter:
  time_or_version_scope:
  query_time_filters: []
hard_filters:
  knowledge_status_allowed: []
  retrieval_policy_allowed: []
  project_scope_required:
  overlay_state_allowed: []
  excluded_path_roles: []
retrieval_lanes:
  reviewed: []
  candidate_orientation: []
  raw_drilldown: []
  active_project_overlay: []
  audit_evidence: []
diagnostic_signals:
  tag_hits: []
  facet_counts: []
  retrieval_scores: []
  graph_centrality: []
  dashboard_prominence: []
  feedback_clicks: []
```

Rule:

```text
Query-time filters and diagnostics are trace, not authority.
They may explain why an item was activated.
They cannot create support, confidence, reviewed relations, or action basis.
```

## Topic / Hub / MOC

High-value topics may have a topic retrieval pack.

```yaml
record_kind: topic_retrieval_pack
topic_id:
truth_boundary: navigation_only
default_include_path_roles: []
default_exclude_path_roles: []
lanes:
  mainline:
  candidate:
  raw:
  overlay:
  audit:
```

Rule:

```text
Topic packs route reading.
They do not decide truth.
```
