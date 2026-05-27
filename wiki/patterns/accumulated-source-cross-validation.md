---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - "local architecture discussion"
sources:
  - "[[2026-05-27-traceability-first-graduated-verification]]"
  - "[[SCHEMA]]"
  - "[[IMPLEMENTATION_BLUEPRINT]]"
related_concepts:
  - "[[source-verification-and-trust-model]]"
  - "[[semantic-relation-edge-schema]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adopted
verification_status: active
evidence_level: synthetic
evidence_count: 1
confidence: high
negative_evidence:
  - "Corpus repetition can amplify shared rumors or copied sources, so source independence still matters."
  - "Cross-validation signals cannot replace provenance or review for action-critical decisions."
replaces:
superseded_by:
extension_points:
  - lint rule packs
  - compile strategies
  - context pack modes
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "No automated source-cluster or source-independence scorer exists yet."
  - "REVIEW_QUEUE.md has not yet defined how repeated candidate points are grouped."
evidence_timeline:
  - date: 2026-05-27
    source: "architecture review discussion"
    observation: "The user identified that stored source material can support later cross-validation, reducing the need for heavy one-by-one verification at capture time."
    effect: supports
    confidence: high
relations:
  - target: "[[2026-05-27-traceability-first-graduated-verification]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[accumulated-source-cross-validation]]"
    rationale: "Traceability-first works because later similar sources can be compared and clustered before promotion."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[SCHEMA]]"
    type: refines
    strength: 4
    confidence: high
    evidence:
      - "[[accumulated-source-cross-validation]]"
    rationale: "SCHEMA should treat cross-source recurrence as a promotion signal, not a capture burden."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - cross-validation
  - traceability-first
  - provenance
---

# Accumulated Source Cross-Validation

## AI-readable preamble

This pattern explains why raw capture should stay lightweight.

The vault does not need to fully verify every source when it arrives. It needs to preserve provenance well enough that later similar sources can support, weaken, or contradict each other.

Accumulated agreement is a promotion signal, not automatic truth.

## Problem

Verifying every incoming source one by one is too expensive.

If capture requires heavy evidence fields, users will stop saving material. But if sources are saved with clear provenance, the vault can compare future materials against earlier ones.

## Pattern

Use this flow:

```text
capture many sources with provenance
-> extract candidate points
-> group similar points over time
-> mark support / contradiction / refinement
-> promote only stable high-signal points
```

The useful unit is not only a single note. It is a recurring point across multiple traceable sources.

## Why It Helps

When the vault grows, it can answer better questions:

```text
Have we seen this claim before?
Which sources say the same thing?
Are those sources independent or copied from one another?
Which source contradicts this?
Is this still just a repeated anecdote, or has it become a reliable pattern?
```

This reduces the need for heavy verification at intake.

## Required Minimum

Every captured source should preserve:

```text
source path or URL
captured date
source type
why saved
raw location or excerpt range
processing status
```

Every candidate point should preserve:

```text
source refs
source ranges
extracted point
uncertainty
possible related points
```

## Promotion Signals

A candidate becomes stronger when:

```text
multiple independent sources support it
different source types support it
the same point appears across time
it explains several related cases
contradictions are checked and bounded
negative evidence is recorded
```

## Failure Boundary

Do not confuse repetition with truth.

Bad signals:

```text
many pages copying the same original source
social posts repeating an unverified rumor
AI summaries reinforcing each other
search similarity without source independence
```

For action-critical decisions, cross-validation is only one evidence signal. Decisions still need risk, rollback, and feedback.

## Fit In This Vault

This pattern supports the current architecture:

```text
raw/source:
  capture and preserve provenance

candidate:
  extract and group points

claim/pattern:
  promote recurring, supported, bounded points

decision/context pack:
  use only reviewed points, with warnings and gaps
```
