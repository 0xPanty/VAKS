---
record_type: query-run
status: failed_fixture
created: 2026-06-07
query_id: fixture-tag-first-failure
question_summary: "Find retrieval best practices by tag first."
query_intent: implementation
query_understanding:
  action_facing: true
  project_scope: VAKS
  extracted_topics:
    - retrieval
  extracted_entities: []
  query_time_filters:
    - tag=retrieval
bad_pipeline:
  - "Search all files by tag/topic first."
  - "Merge raw, candidate, overlay, and audit evidence into one ranked list."
  - "Treat top result as action basis."
hard_filters:
  knowledge_status_allowed: []
  retrieval_policy_allowed: []
  action_basis_required: true
retrieval_lanes:
  mixed_global_list:
    - fixtures/source-card-forbidden-authority-tags.md
    - fixtures/candidate-distillation-kp-refs.md
    - fixtures/project-overlay-confirmed.md
diagnostic_signals:
  tag_hits:
    - retrieval
    - best-practice
  retrieval_scores:
    fixtures/source-card-forbidden-authority-tags.md: 0.98
warnings:
  - tag_first_pipeline
  - forbidden_authority_tag
  - mixed_authority_bucket
  - action_basis_without_reviewed_support
expected_block:
  - "Fail lint."
  - "Do not use as action basis."
  - "Re-run with hard filters first."
---

# Fixture: Tag-First Failure

## Expected Behavior

This fixture must fail.

It intentionally does the bad thing:

```text
tag search first
mixed authority bucket
top result as action basis
```
