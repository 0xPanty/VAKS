---
type: implementation-note
status: active
created: 2026-05-28
updated: 2026-05-28
project: verified-action-knowledge-system
scope:
  - source-intake
  - processing-tier
  - ux
  - provenance
related_files:
  - "[[SCHEMA]]"
  - "[[IMPLEMENTATION_BLUEPRINT]]"
  - "[[DEV_CONTEXT]]"
  - "[[MEMORY_TIER]]"
  - "[[REFERENCE_REVIEW_PROTOCOL]]"
verification_status: active
evidence_level: synthetic
confidence: high
last_verified: 2026-05-28
next_review: 2026-06-04
tags:
  - source-intake
  - processing-tier
  - karpathy-simple
  - source-provenance
---

# SOURCE_INTAKE.md v0.1

## AI-readable preamble

This file defines how incoming material should be handled without making everyday use heavy.

The rule is:

```text
Karpathy for normal intake.
Dusk-style dashboard for project use.
Verified-action strictness only for strong sources and action-bearing knowledge.
```

Do not run the full verified-action process on every note.

## 1. Core Judgment

Not all material deserves the same processing depth.

Use three levels:

```text
light:
  capture and keep findable.

medium:
  summarize and route.

heavy:
  preserve provenance, extract points, compare, review, and write durable patterns/decisions/risks.
```

The goal is to avoid both extremes:

```text
too light:
  AI summaries become untraceable and unreliable.

too heavy:
  every ordinary note becomes paperwork.
```

## 2. Processing Levels

### Light Processing

Use for:

```text
ordinary articles
interesting but unproven ideas
temporary references
small notes
low-impact links
material saved for possible future lookup
```

Minimum record:

```text
source link or file path
title
author/publisher if obvious
captured_at
why saved
short note or summary
current status
```

Do not require:

```text
confidence
evidence_level
relations
negative_evidence
formal review
pattern extraction
```

### Medium Processing

Use for:

```text
material likely to be reused
project background
useful references for a current question
docs that may enter a dev context
sources with clear but not architecture-changing ideas
```

Add:

```text
structured summary
tags/topics
source status
possible related files
candidate points
open questions
whether it belongs in a scope dashboard or dev context
```

Medium processing can feed:

```text
index
scope dashboard
context briefing
DEV_CONTEXT support or cold references
```

It still does not create truth.

### Heavy Processing

Use only for strong sources:

```text
papers
valuable repositories
official specs/docs
high-signal technical articles
important design discussions
materials that can validate or falsify our architecture
sources that affect project direction
risks, anti-patterns, failure reports
sources likely to become action basis
```

Add:

```text
full provenance
author / organization
published_at / updated_at
captured_at
version / commit / DOI / release
source_status: active | legacy | deprecated | unknown
timeline notes
files or sections reviewed
source/code anchors
candidate points
supports / contradicts / refines / risk_of / derived_from relations
what we adopt
what we reject
risk and anti-pattern extraction
fit with current branch
fit with whole architecture
```

Heavy processing can create:

```text
source record
architecture review
pattern
anti-pattern
decision
implementation-note
index update
handoff update
```

## 3. What "Preserve Source" Means

Preserving source means giving important knowledge an identity card.

For a repository:

```yaml
source_url:
owner:
repo:
checked_commit:
commit_time:
captured_at:
source_status: active | legacy | deprecated | unknown
files_reviewed:
source_anchor_matrix:
why_captured:
extracted_points:
not_adopted:
timeline_notes:
```

For a paper:

```yaml
title:
authors:
published_at:
venue:
doi_or_arxiv:
version:
captured_at:
key_sections_reviewed:
main_claims:
limitations:
later_updates:
fit_to_our_architecture:
```

Plain rule:

```text
Do not let an AI summary become detached from who said it, when, where, and in what version.
```

## 4. User Experience Modes

### Normal Question Mode

Use:

```text
Karpathy-simple
```

Flow:

```text
search/read enough
answer
optionally save light note if valuable
```

Do not create:

```text
dev context pack
full review
pattern/anti-pattern
feedback-event
```

unless the material proves important.

### Project Development Mode

Use:

```text
Dusk-style scope dashboard + DEV_CONTEXT
```

Flow:

```text
project goal
-> scope dashboard / related-material briefing
-> DEV_CONTEXT Core / Support / Risk / Cold References
-> development
-> closeout
```

The dashboard is a workbench.

It is not truth.

### Strong Source / Decision Mode

Use:

```text
verified-action strictness
```

Flow:

```text
source record
-> candidate points
-> collision / comparison
-> review
-> pattern / anti-pattern / decision
-> index / handoff
```

Use this mode when the source may affect future action.

## 5. When To Upgrade Processing

Upgrade light to medium when:

```text
the source is reused
the user asks about it again
it becomes relevant to a project
it appears in search/context briefing repeatedly
```

Upgrade medium to heavy when:

```text
it changes architecture
it validates or contradicts a design
it becomes a development constraint
it exposes a risk or failure mode
it should be cited as action basis
```

Downgrade or cool after use when:

```text
it was one-off evidence
it no longer fits the active project
its value is only historical
it has been superseded
```

## 6. Non-negotiable Boundaries

```text
Capture must stay easy.
Strong sources must remain traceable.
Dashboard state is not truth.
Retrieval rank is not trust.
Repeated appearance is a signal, not proof.
Heavy review is for promotion and action, not ordinary saving.
```

## 7. First Implementation

Do not write automation first.

First prove this manually with real material:

```text
1 light source
1 medium project reference
1 heavy repo/paper review
1 scope dashboard or dev context pack
1 closeout update
```

Only after the manual loop works should scripts or CLI commands be written.
