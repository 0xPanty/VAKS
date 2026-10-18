---
record_type: query-run
status: archived
created: 2026-06-07
query_id: fixture-action-review-query
question_summary: "Can this metadata-filtering design be used as action basis?"
query_intent: decision
query_scope:
  project: VAKS
scope_key: VAKS/source-intake
query_understanding:
  action_facing: true
  project_scope: VAKS
  source_type_filter:
  time_or_version_scope:
  extracted_topics:
    - retrieval
    - source-intake
  extracted_entities:
    - Qdrant
    - Haystack
  query_time_filters:
    - action_facing=true
hard_filters:
  knowledge_status_allowed:
    - reviewed
  retrieval_policy_allowed:
    - reviewed_support_only
  overlay_state_allowed: []
  action_basis_required: true
  excluded_path_roles:
    - candidate_distillation
    - sandbox_baseline
    - zip_package
    - archived_overlay
retrieval_lanes:
  reviewed:
    - "No reviewed support fixture in this sandbox."
  candidate_orientation:
    - fixtures/candidate-distillation-kp-refs.md
  raw_drilldown:
    - fixtures/source-card-confirmed-metadata.md
  active_project_overlay:
    - fixtures/project-overlay-confirmed.md
  audit_evidence: []
diagnostic_signals:
  tag_hits:
    - retrieval
  facet_counts:
    retrieval: 2
  retrieval_scores:
    fixtures/candidate-distillation-kp-refs.md: 0.94
  graph_centrality: []
  feedback_clicks: []
answer_path:
  - "Candidate can orient."
  - "Raw can provide provenance."
  - "No reviewed/action support exists, so action basis is not ready."
warnings:
  - candidate_not_action_basis
  - raw_is_provenance_only
gaps:
  - "Need reviewed evidence packet or reviewed decision before action basis."
---

# Fixture: Correct Action Review Query

## Expected Result

The query finds relevant candidate and raw material, but blocks action-ready
support because the allowed reviewed lane is empty.
