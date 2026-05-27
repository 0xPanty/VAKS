---
type: decision
status: active
created: 2026-05-27
updated: 2026-05-27
decision: "Adopt traceability-first, graduated verification: raw capture only needs provenance, while strict verification applies only when content is promoted or used for action."
decision_scope:
  - schema
  - ingest
  - review
  - ux
  - implementation-blueprint
related_projects:
  - verified-action-knowledge-system
based_on:
  - "[[SCHEMA]]"
  - "[[ARCHITECTURE_PRINCIPLES]]"
  - "[[IMPLEMENTATION_BLUEPRINT]]"
  - "[[2026-05-27-karpathy-simple-verified-strict-ux-principle]]"
  - "[[2026-05-27-codex-mediated-ingest-and-review-gate]]"
patterns:
  - "[[source-adapter-ingest-contract]]"
  - "[[review-gated-compile-queue]]"
  - "[[claim-level-provenance-source-ranges]]"
  - "[[accumulated-source-cross-validation]]"
anti_patterns:
  - "[[direct-compile-to-truth-layer-without-review]]"
outcome: adopted
verification_status: active
evidence_level: synthetic
evidence_strength: high
confidence: high
negative_evidence:
  - "If every raw source or candidate must fill decision-grade verification fields, capture becomes too slow and the system turns into paperwork."
  - "If validation is removed entirely, AI-generated notes can be mistaken for action-ready truth."
replaces:
superseded_by:
migration_path:
  - "Keep raw/source records lightweight and provenance-first."
  - "Make candidate records traceable and reviewable, not fully verified by default."
  - "Require strict evidence, confidence, negative evidence, relation rationale, rollback, and feedback fields only for promoted claim, pattern, anti-pattern, decision, implementation-note, or context-pack outputs."
rollback_path:
  - "If lightweight intake allows too much low-quality material into formal nodes, re-tighten promotion lint without making raw capture heavier."
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: decision
gaps:
  - "REVIEW_QUEUE.md is not created yet, so the lighter candidate contract still needs to be written."
  - "No lint script currently enforces graduated severity by node type."
evidence_timeline:
  - date: 2026-05-27
    source: "architecture review discussion"
    observation: "The user judged provenance as necessary but heavy validation as too cumbersome for everyday capture."
    effect: refines
    confidence: high
relations:
  - target: "[[SCHEMA]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-traceability-first-graduated-verification]]"
    rationale: "SCHEMA should separate low-friction provenance capture from strict promotion requirements."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[IMPLEMENTATION_BLUEPRINT]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-traceability-first-graduated-verification]]"
    rationale: "The blueprint should implement a lightweight raw/candidate path before strict action-grade verification."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[2026-05-27-karpathy-simple-verified-strict-ux-principle]]"
    type: implements
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-traceability-first-graduated-verification]]"
    rationale: "Traceability-first preserves the Karpathy-simple outside while keeping strict verification inside promotion gates."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - decision
  - traceability-first
  - graduated-verification
  - schema
  - review-gate
---

# Traceability First, Graduated Verification

## AI-readable preamble

This decision reduces validation friction.

Raw capture and source records only need enough provenance to find the original material again. Strict verification is still required for promoted claims, patterns, decisions, context packs, and action basis.

The system should be easy to feed and strict only when a conclusion becomes reusable or actionable.

## Decision

Adopt this rule:

```text
Traceability first.
Verification only when it matters.
```

In plain terms:

```text
raw / inbox:
  keep source, URL/path, captured date, why saved, and processing status

candidate:
  keep source refs, source ranges, extracted points, uncertainties, and promotion target

claim / pattern / anti-pattern:
  add evidence level, confidence, gaps, negative evidence, and key relations

decision / context pack / implementation note:
  add risks, preconditions, rollback, success metric, feedback source, and next review
```

## Why

The previous schema risked pushing too much verification work onto ordinary capture.

That creates the wrong incentive:

```text
If saving a source feels like paperwork, sources will not be saved.
```

The minimum useful invariant is provenance:

```text
Can we trace this note back to the original source?
Can we see whether it is raw, candidate, or promoted?
Can we prevent unreviewed content from becoming action basis?
```

If yes, the system can stay useful without forcing every source to become a mini decision record.

The deeper reason is accumulation:

```text
One source is often weak.
Many traceable sources can be compared.
Similar points can support, refine, or contradict each other.
```

The vault should become more logically self-checking as it grows, because repeated points, contradictions, and source overlap become visible. This does not make the vault automatically true, but it gives Codex and the user stronger signals for promotion.

## What Changes

Raw/source records become lightweight.

Candidate records become reviewable, not fully verified.

Strict verification fields move to promotion and action use:

```text
claim
pattern
anti-pattern
decision
implementation-note
context pack
```

## What Does Not Change

Unreviewed content still cannot become truth.

Retrieval still cannot decide what is true.

Context packs still need warnings and gaps.

Decisions still need risk and rollback.

## Practical Rule

Use this severity model:

```text
capture lint:
  missing source path / URL / captured date

candidate lint:
  missing source refs / source ranges / extracted point / uncertainty

promotion lint:
  missing evidence / confidence / negative evidence / relation rationale

action lint:
  missing risk / preconditions / rollback / success metric / feedback path
```

This keeps intake light and action strict.
