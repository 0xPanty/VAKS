---
type: anti-pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
domain: knowledge-system-architecture
failure_mode: "Automatic classification, synthesis, or promotion writes directly into verified knowledge"
severity: 5
likelihood: 4
complexity_cost: 4
cross_validated_with:
  - "[[direct-compile-to-truth-layer-without-review]]"
  - "[[automated-brief-as-truth-without-review]]"
  - "[[auto-compiled-concept-wiki-as-verified-truth-layer]]"
related_projects:
  - verified-action-knowledge-system
replacement:
  - "[[review-gated-compile-queue]]"
  - "[[self-contained-review-candidate-record]]"
  - "[[token-efficient-context-briefing]]"
verification_status: single-source
evidence_level: secondary
confidence: medium
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Needs testing once this vault has an actual classify/promote script."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-knowledge-base-server-source]]"
    observation: "The repo includes auto-classification, summarization, promotion, and kb_write surfaces that can write into the vault."
    effect: supports
    confidence: medium
relations:
  - target: "[[SCHEMA]]"
    type: risk_of
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-knowledge-base-server-source]]"
    rationale: "Classifier output and promoted notes can blur raw/candidate/verified boundaries if adopted directly."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[REVIEW_QUEUE]]"
    type: supports
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-knowledge-base-server-source]]"
    rationale: "The risk reinforces the need for review-gated promotion."
    created: 2026-05-27
    last_verified: 2026-05-27
decision: avoid
tags:
  - anti-pattern
  - auto-promotion
  - review-gate
  - truth-layer
---

# Anti-pattern: Auto Promotion Without Review Gate

## AI-readable preamble

Automated classification, summarization, synthesis, and promotion are useful.

They become dangerous when their output writes directly into verified knowledge or decisions.

Use automation to create candidates. Use review to promote truth.

## Problem

AI memory systems often want to improve automatically:

```text
classify raw notes
summarize documents
promote sources into lessons
synthesize weekly insights
write back to vault
```

This is useful for recall.

It is unsafe for verified-action knowledge if the output skips review.

## Why it fails

Classifier output can be wrong:

```text
wrong type
wrong project
overconfident summary
missing negative evidence
invented implication
thin citation
wrong promotion target
```

Synthesis output can be useful but still unverified:

```text
pattern-looking coincidence
old assumption repeated
one-off event generalized
missing contradiction
```

If these go straight into verified notes, the vault becomes fluent but less trustworthy.

## Failure conditions

- `confidence` from an LLM classifier becomes `confidence` in the verified schema.
- A weekly synthesis note becomes a decision.
- A promoted lesson bypasses review queue.
- `kb_write` or an equivalent tool writes directly into formal wiki paths.
- Retrieval rank controls promotion.
- Agent-created summaries replace source ranges.

## Replacement

Use automated tools for:

```text
raw capture
candidate classification
candidate summary
candidate point extraction
candidate relation suggestions
candidate dev context briefing
```

Then require:

```text
review queue
source provenance
evidence_level
negative evidence check
relation review
decision readiness check
```

## Fusion suggestion

For this vault:

```text
auto classify -> candidate metadata
auto summarize -> briefing metadata
auto synthesize -> review candidate
auto promote -> review queue item
agent write -> raw/candidate only unless explicitly approved
```

## Boundary

Automation can make work visible.

Review decides what becomes trusted.
