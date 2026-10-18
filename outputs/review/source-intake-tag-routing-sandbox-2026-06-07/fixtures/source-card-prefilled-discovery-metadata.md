---
type: source
status: source-captured
title: "Prefilled Discovery Metadata Fixture"
source_id: fixture-source-prefilled-discovery-metadata
source_url: https://example.invalid/prefilled-discovery
source_type: article
captured_at: 2026-06-07
raw_location: raw/articles/fixture-source-prefilled-discovery-metadata.md
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
  - metadata-routing
  - context-pack
content_form: article
language: en
version_or_time_scope: captured-2026-06-07
entities:
  - DataChain
aliases:
  - registry-before-recompute
entity_refs: []
tags:
  - retrieval
---

# Fixture: Prefilled Discovery Metadata

This fixture has useful discovery metadata in frontmatter.

The body intentionally stays generic so retrieval can prove the frontmatter adds
findability.

Boundary:

```text
metadata helps find this source.
metadata does not make it reviewed, adopted, or action-ready.
```
