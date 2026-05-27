---
type: anti-pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
domain: knowledge-system-architecture
failure_mode: "Treating link overlap, backlinks, tags, ratings, or recency as truth evidence"
severity: 4
likelihood: 4
complexity_cost: 3
cross_validated_with:
  - "[[algorithmic-graph-scoring-without-source-quality]]"
  - "[[generic-concept-schema-as-truth-layer]]"
related_projects:
  - verified-action-knowledge-system
replacement:
  - "[[link-overlap-related-context-surface]]"
  - "[[context-pack-evidence-envelope]]"
  - "[[semantic-relation-edge-schema]]"
verification_status: single-source
evidence_level: secondary
confidence: medium
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Needs comparison against more graph/view based vaults."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-kepano-obsidian-source]]"
    observation: "Kepano's vault uses link overlap, backlinks, tags, ratings, and recency to surface context, but it is not a verification system."
    effect: supports
    confidence: medium
relations:
  - target: "[[SCHEMA]]"
    type: risk_of
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-kepano-obsidian-source]]"
    rationale: "Derived relatedness can be mistaken for verified semantic relations if the schema boundary is weak."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[link-overlap-related-context-surface]]"
    type: risk_of
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-kepano-obsidian-source]]"
    rationale: "The pattern is useful only when kept as recall, not verification."
    created: 2026-05-27
    last_verified: 2026-05-27
decision: avoid
tags:
  - anti-pattern
  - relatedness
  - truth-layer
  - graph-score
---

# Anti-pattern: Derived Relatedness As Truth Signal

## AI-readable preamble

Link overlap, backlinks, tags, ratings, and recency are useful activation signals.

They become dangerous when treated as evidence of truth, support, or decision readiness.

Use them for recall and context discovery; use reviewed relations and sources for truth.

## Problem

Bottom-up vaults often create rich signals:

```text
links
backlinks
tags
categories
ratings
last seen dates
view formulas
```

These signals are excellent for:

```text
finding adjacent context
building dashboards
surfacing forgotten notes
suggesting Support files
```

They are not evidence.

## Why it fails

Two notes can share links because:

```text
same broad topic
same author
same project
same tag habit
same accidental wording
```

That does not prove:

```text
one supports the other
they are independently sourced
the claim is true
the decision is safe
the context should be Core
```

## Failure conditions

- Related.base or graph view is used as a truth graph.
- A high backlink count makes a claim look verified.
- Ratings become confidence.
- Recent notes become more trusted.
- Tag overlap is treated as a reviewed relation.
- Organic links bypass review queue.

## Replacement

Use derived relatedness as:

```text
candidate recall
Support suggestion
Cold Reference suggestion
missing relation candidate
review work generator
```

Use verified-action fields for truth:

```text
source provenance
source ranges
verification_status
evidence_level
confidence
negative_evidence
reviewed relations
decision rollback
```

## Follow-up

When implementing related context surfaces:

```text
show why a note was suggested
label it as candidate/support
require review before relation promotion
never let score alone enter context pack as evidence
```
