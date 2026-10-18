---
type: source
status: source-captured
title: Bad Fixture With Authority Tags
source_id: fixture-source-forbidden-authority-tags
source_url: https://example.invalid/bad-tags
source_type: article
captured_at: 2026-06-07
raw_location: raw/articles/fixture-source-forbidden-authority-tags.md
processing_tier: light
knowledge_status: raw
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
topics:
  - retrieval
content_form: article
language: en
version_or_time_scope: captured-2026-06-07
entities:
  - Obsidian
tags:
  - reviewed
  - action-basis
  - best-practice
---

# Fixture: Forbidden Authority Tags

## Expected Behavior

This fixture must fail lint.

The bad tags are:

```text
reviewed
action-basis
best-practice
```

Reason:

```text
authority cannot live in ordinary tags.
```
