---
record_kind: intake_metadata_suggestion
status: suggested
knowledge_status: candidate
processing_tier: light
persistent_main_note_allowed: false
default_retrieval_allowed: false
target_ref:
created_at:
suggested_topics: []
suggested_entities: []
suggested_content_form:
suggested_language:
suggested_version_or_time_scope:
suggested_routing_hint: []
suggested_query_time_filters: []
confirmation_required_for:
  - write_to_source_card
  - project_overlay_ref
  - candidate_point_keep
  - borrow_non_borrow
  - reviewed_or_action_use
---

# Intake Metadata Suggestion Sidecar

## Boundary

This record stores model-suggested metadata before confirmation.

It should not enter default retrieval and should not be treated as confirmed
source metadata.

## Suggested Metadata

```yaml
suggested_topics: []
suggested_entities: []
suggested_content_form:
suggested_language:
suggested_version_or_time_scope:
suggested_routing_hint: []
suggested_query_time_filters: []
```

## Confirmation Required

```text
write_to_source_card
project_overlay_ref
candidate_point_keep
borrow_non_borrow
reviewed_or_action_use
```
