---
type: source
status: source-captured
title: Metadata Filters For Knowledge Intake
source_id: fixture-source-confirmed-metadata
source_url: https://example.invalid/metadata-filters
source_type: article
captured_at: 2026-06-07
raw_location: raw/articles/fixture-source-confirmed-metadata.md
processing_tier: light
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
topics:
  - retrieval
  - source-intake
content_form: article
language: en
version_or_time_scope: captured-2026-06-07
entities:
  - Qdrant
  - Haystack
aliases:
  - metadata filter
entity_refs: []
tags:
  - retrieval
  - pkm
---

# Fixture: Source Card With Confirmed Metadata

## Expected Behavior

This file may be found by topics, entities, or lexical search.

It remains raw provenance:

```text
not reviewed
not adopted
not action basis
not project borrowing verdict
```

## Bad Interpretation To Block

```text
Because this has topic `retrieval`, it is action-ready.
```

Expected block:

```text
knowledge_status: raw
retrieval_policy.warning_code: raw_is_provenance_only
action_basis_allowed: false
```
