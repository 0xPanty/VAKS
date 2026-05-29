---
type: source
status: source-captured
title: "Graphiti / Zep Temporal Validity Windows"
source_id: 2026-05-29-graphiti-zep-temporal-validity-source
source_uri: https://help.getzep.com/facts
source_url: https://help.getzep.com/facts
source_type: docs
version_or_commit: Zep / Graphiti docs captured 2026-05-29
captured_at: 2026-05-29
captured_by: Codex
processing_mode: immediate
processing_level: heavy
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - temporal-knowledge-graph
  - applicability
  - scope-fit
  - provenance
projects:
  - verified-action-knowledge-system
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - graphiti
  - zep
  - temporal-validity
  - scope-fit
---

# Graphiti / Zep Temporal Validity Source Record

## Why Captured

Graphiti / Zep is a conceptual reference for hardening the vault's `scope_fit` into a structured Temporal Applicability Check.

The adopted wording is:

```text
Truth is source-backed.
Applicability is time-, version-, and scope-bound.
```

## Source Identity

- Zep facts documentation: https://help.getzep.com/facts
- Graphiti documentation: https://help.getzep.com/graphiti/getting-started/welcome
- Zep graph concepts: https://help.getzep.com/v2/understanding-the-graph
- Zep paper: https://arxiv.org/abs/2501.13956

## Extracted Architecture Point

Graphiti / Zep records temporal facts with validity windows such as `valid_at` and `invalid_at`, while preserving source episodes / raw data as provenance.

For this vault, the useful point is not automatic graph construction.
The useful point is:

```text
reviewed facts and relations should carry applicability windows.
```

## Adopt

```text
valid_from / valid_until
supersedes / superseded_by
invalidated_by
applies_to project / version / environment / timeframe / conditions
episode / raw-source traceability as provenance discipline
```

## Do Not Adopt

```text
automatic graph construction as reviewed knowledge
automatic invalidation as truth update
graph database runtime as Markdown source of truth
agent memory platform as core architecture
```

## Fit To Current Architecture

Place in:

```text
Schema / reviewed node fields
Qualification / scope fit
Context Pack / Action Basis
Evidence Sufficiency Gate inputs
Use Ledger review_due triggers
```

Do not place in:

```text
automatic truth update
automatic conflict resolution
runtime graph as system of record
```

## Review Notes

This source should be presented to Pro review as supplement 10.

The intended absorption is intentionally small:

```text
Temporal Applicability Check:
  truth remains source-backed;
  action use must check time, version, scope, and supersession.
```
