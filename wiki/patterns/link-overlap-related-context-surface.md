---
type: pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - kepano/kepano-obsidian
related_concepts:
  - "[[DEV_CONTEXT]]"
  - "[[MEMORY_TIER]]"
  - "[[four-signal-graph-relevance]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adapt
verification_status: single-source
evidence_level: secondary
evidence_count: 1
confidence: medium
negative_evidence:
  - "Link overlap and tag overlap can surface related items but cannot prove evidence or truth."
replaces:
superseded_by:
extension_points:
  - dev-context
  - query
  - Obsidian Bases
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Needs comparison with graph/BM25/vector relatedness systems and a real dev-context trial."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-kepano-obsidian-source]]"
    observation: "Related.base computes related notes using link overlap, backlinks, and tag overlap."
    effect: supports
    confidence: medium
relations:
  - target: "[[DEV_CONTEXT]]"
    type: refines
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-kepano-obsidian-source]]"
    rationale: "Derived relatedness can suggest Support candidates for a dev context pack."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[derived-relatedness-as-truth-signal]]"
    type: risk_of
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-kepano-obsidian-source]]"
    rationale: "The same relatedness signal becomes dangerous if used as verification or truth confidence."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - dev-context
  - relatedness
  - activation
---

# Link-Overlap Related Context Surface

## AI-readable preamble

Use link overlap, backlinks, and tag overlap to suggest related context.

This helps build Support and Cold Reference candidates for dev context.

It must remain a recall signal, not a truth signal.

## One-line definition

Notes that share links, backlinks, or tags can be surfaced as related context candidates.

## Problem solved

When creating a dev context pack, broad search can miss structurally related notes.

Kepano's `Related.base` shows a lightweight mechanism:

```text
notes that share links
notes linking to the current note
notes linked from the current note
notes with overlapping tags
```

This can reveal useful adjacent material without a vector database.

## Applicable scenarios

- Finding Support candidates for `DEV_CONTEXT.md`.
- Finding Cold References worth checking.
- Spotting missing relations or candidate point collisions.
- Building a lightweight Obsidian workbench.

## Not applicable

- Setting truth confidence.
- Promoting candidates.
- Replacing reviewed `relations`.
- Deciding that two claims support each other.

## Evidence

- `[[2026-05-27-kepano-obsidian-source]]`
- `Templates/Bases/Related.base` derives related notes from shared links, backlinks, and tag overlap.

## Tags and scores

- domain: context-discovery
- problem: support-context-selection
- maturity: emerging
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 3
- reversibility: 5

## Minimum implementation

For a candidate dev context file:

```text
1. Get outgoing links.
2. Get backlinks.
3. Find notes sharing important links or tags.
4. Rank as Support candidates.
5. Require human/Codex selection before Core.
6. Keep evidence/truth decisions in verified relations, not this score.
```

## Fusion suggestion

Add to `DEV_CONTEXT.md` as candidate discovery:

```text
Relatedness can propose Support.
Only task necessity can make Core.
Only review can make truth.
```

## Verification metrics

- Support suggestions include useful files not found by filename search.
- Irrelevant related notes are easy to reject.
- No answer cites derived relatedness as evidence.
- Missing reviewed relations become visible for later review.
