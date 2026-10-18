---
record_type: query-run
status: archived
created:
updated:
query_id:
session_id:
turn_id:
question_summary:
verbatim_input:
model_interpretation:
query_intent: answer | decision | implementation | research | source_inspection | audit_history
query_scope:
  project:
  domain:
  version:
  time_range:
scope_key:
query_understanding:
  action_facing: false
  project_scope:
  source_type_filter:
  time_or_version_scope:
  extracted_topics: []
  extracted_entities: []
  query_time_filters: []
hard_filters:
  knowledge_status_allowed: []
  retrieval_policy_allowed: []
  overlay_state_allowed: []
  action_basis_required: false
  review_pressure_allowed: []
  path_roles_allowed: []
  path_roles_excluded: []
retrieval_mode:
authority_bucket:
rrf_scope: same_authority_bucket_only
retrieval_lanes:
  reviewed: []
  candidate_orientation: []
  raw_drilldown: []
  active_project_overlay: []
  audit_evidence: []
included_sources: []
excluded_candidates: []
diagnostic_signals:
  tag_hits: []
  facet_counts: []
  retrieval_scores: []
  graph_centrality: []
  dashboard_prominence: []
  feedback_clicks: []
overlay_suggestions:
  - target_ref:
    project_ref:
    overlay_state: suggested
    persistent_overlay_allowed: false
    default_retrieval_allowed: false
    action_basis_allowed: false
    warning_code: overlay_unconfirmed
answer_path: []
warnings: []
gaps: []
tags:
  - query-run
---

# Query Run

## What Was Asked

- Verbatim input:
- Model interpretation:

## Query Understanding

```yaml
action_facing:
project_scope:
extracted_topics: []
extracted_entities: []
query_time_filters: []
```

## Hard Filters

Hard filters run before tag/topic/entity/BM25/vector/rerank.

```yaml
knowledge_status_allowed: []
retrieval_policy_allowed: []
overlay_state_allowed: []
action_basis_required:
path_roles_excluded: []
```

## Retrieval Lanes

```yaml
reviewed: []
candidate_orientation: []
raw_drilldown: []
active_project_overlay: []
audit_evidence: []
```

## Diagnostics

Diagnostic signals explain activation and ranking.

They cannot become evidence support, confidence, or action basis.

## Warnings / Gaps


