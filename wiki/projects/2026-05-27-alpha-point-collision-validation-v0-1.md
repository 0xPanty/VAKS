---
type: implementation-note
status: active
created: 2026-05-27
updated: 2026-05-27
project: verified-action-knowledge-system
related_decisions:
  - "[[2026-05-27-traceability-first-graduated-verification]]"
related_patterns:
  - "[[accumulated-source-cross-validation]]"
  - "[[review-gated-compile-queue]]"
  - "[[claim-level-provenance-source-ranges]]"
sources:
  - "[[2026-05-27-alpha-point-collision-research]]"
  - "[[REVIEW_QUEUE]]"
verification_status: active
evidence_level: synthetic
confidence: high
validated_by:
  - "external research"
  - "subagent review"
rollback_path:
  - "Disable collision promotion and keep only provenance-first candidate records."
last_verified: 2026-05-27
next_review: 2026-06-03
relations:
  - target: "[[REVIEW_QUEUE]]"
    type: implements
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-alpha-point-collision-validation-v0-1]]"
    rationale: "This note defines the alpha mechanism that REVIEW_QUEUE operationalizes."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - alpha
  - point-collision
  - implementation-note
---

# Alpha Point Collision Validation v0.1

## AI-readable preamble

This is the first implementation plan for the vault's alpha validation mechanism.

It keeps source capture lightweight, then uses recurring source-backed points to create reviewed support, contradiction, refinement, and replacement signals.

This is not automatic truth discovery. It is review-gated promotion support.

## Core Mechanism

```text
source
-> candidate point
-> point collision signal
-> point cluster
-> promoted claim / pattern / anti-pattern / decision
```

## Plain-Language Version

Every useful source leaves small traceable points behind.

When future sources say something similar, those points collide.

The collision can mean:

```text
same idea
supports old idea
contradicts old idea
adds conditions
replaces old idea
looks similar but is actually unrelated
```

Only reviewed collisions affect promotion.

## Why This Is The Right First Alpha

It solves the main tension:

```text
capture must stay easy
truth must not be cheap
```

Instead of forcing every source through heavy validation, the vault lets evidence accumulate.

The more sources it holds, the more it can notice:

```text
recurring points
source families
contradictions
stale claims
stable patterns
```

## Minimal Implementation

No heavy vector database required.

v0.1 can use:

```text
Markdown records
rg / keyword search
topic tags
source refs
manual Codex review
```

Optional later:

```text
BM25
embeddings
source-family detector
cluster dashboard
probabilistic scoring
```

## Data Objects

Use the contract in [[REVIEW_QUEUE]]:

```text
source trace
candidate point
collision signal
point cluster
```

Do not create new truth node types for v0.1.

Formal truth nodes remain:

```text
claim
pattern
anti-pattern
decision
implementation-note
context pack
```

## First Trial

Run against 10 sources that are already in this vault or next provided by the user.

Procedure:

```text
1. Extract 2-8 candidate points per source.
2. Search existing points/patterns/claims for similar terms.
3. Create pending collision signals.
4. Review only the high-signal collisions.
5. Create 3-8 clusters.
6. Promote at most 1 claim or pattern candidate.
```

## Metrics

Good signs:

```text
recurring points become visible
contradictions become visible
source independence is explicit
promotion feels easier than reading all source notes manually
```

Bad signs:

```text
clusters are noisy
points are too broad
same-origin copies inflate support
contradictions disappear
review queue becomes a second junk drawer
```

## Hard Boundaries

Never do this in v0.1:

```text
auto promote
auto confidence increase
auto merge points
auto resolve contradictions
count same-origin copies as independent support
count AI summaries as independent sources
```

## Adoption Recommendation

Adopt as the first alpha mechanism.

Not because it is mathematically complete, but because it gives the vault a practical path from loose source collection to reviewed knowledge growth.
