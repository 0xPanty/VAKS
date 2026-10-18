---
type: source
record_kind: source_card
status: source-captured
title: "W3C Web Annotation Data Model"
source_id: 2026-05-30-w3c-web-annotation-source
source_uri: https://www.w3.org/TR/annotation-model/
source_url: https://www.w3.org/TR/annotation-model/
source_type: standard
version_or_commit: W3C Recommendation 23 February 2017; checked 2026-05-30
captured_at: 2026-05-30
captured_by: Codex
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - source-anchor
  - text-quote-selector
  - provenance
  - web-annotation
projects:
  - verified-action-knowledge-system
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - w3c
  - web-annotation
  - source-anchor
knowledge_status: raw
processing_tier: light
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
---

# W3C Web Annotation Source Record

## Why Captured

This source supports the v0.3 Source Anchor mini-profile.

The useful design point is not the full Web Annotation model. The useful point is the Text Quote Selector shape:

```text
exact quote
prefix
suffix
optional position
```

## Source Identity

```text
Spec: W3C Web Annotation Data Model
Section: 4.2.4 Text Quote Selector
URL: https://www.w3.org/TR/annotation-model/#text-quote-selector
Checked: 2026-05-30
```

## Source Anchor

Short exact source wording:

```text
"Text Quote Selector"
"copying it"
"including some of the text immediately before"
"after"
"exact"
"prefix"
"suffix"
```

Extracted point:

```text
A stable text anchor should not only name a source. It should preserve the selected text and nearby context so the reviewer can re-find the evidence span.
```

Readable source context:

```text
The W3C selector describes a text span by preserving the selected text plus nearby before/after context. Its model names the selected text `exact`, with `prefix` and `suffix` as surrounding snippets.
```

## Adopt

```text
source_anchor:
  url_or_path
  exact_quote
  prefix
  suffix
  captured_at

heavy optional:
  position
  content_hash
  archived_url
  checked_latest_at
  source_changed
```

## Do Not Adopt

```text
full W3C JSON-LD model
annotation server
RDF serialization
all selector types as required fields
browser annotation runtime
```

## Fit To This Vault

Place in:

```text
SOURCE_INTAKE
SCHEMA evidence_packet
REVIEW_QUEUE evidence items
templates/review-candidate.md
```

Boundary:

```text
source_anchor is provenance.
source_anchor is not evidence support by itself.
```
