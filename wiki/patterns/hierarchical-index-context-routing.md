---
type: pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - Asim00740/Kagantic-vault-structure
related_concepts:
  - "[[DEV_CONTEXT]]"
  - "[[MEMORY_TIER]]"
  - "[[token-efficient-context-briefing]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adapt
verification_status: single-source
evidence_level: secondary
evidence_count: 1
confidence: medium
negative_evidence:
  - "The source repo is a small example vault and does not provide verification or lifecycle management."
extension_points:
  - dev-context
  - project-index
  - context-briefing
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Needs trial against a real project context pack."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-kagantic-vault-structure-source]]"
    observation: "Main Index tells agents to start at the index, choose a sub-index, and prefer summaries/tags before reading full notes."
    effect: supports
    confidence: medium
relations:
  - target: "[[DEV_CONTEXT]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-kagantic-vault-structure-source]]"
    rationale: "A dev context builder can start from project/domain indexes before reading full files."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[token-efficient-context-briefing]]"
    type: supports
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-kagantic-vault-structure-source]]"
    rationale: "Index pages provide a Markdown-only briefing layer."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - context-routing
  - index
  - dev-context
---

# Hierarchical Index Context Routing

## AI-readable preamble

Use human-readable index pages as a first-pass context router before opening individual notes.

This is a lightweight context briefing pattern. It does not decide truth.

## One-line definition

Start from an index, choose the matching sub-index, then open full notes only after summaries/tags match the task.

## Problem solved

Without routing, agents do this:

```text
search broadly
open too many notes
mix domains
miss the intended entrypoint
```

An index-first flow gives the agent a map.

## Source evidence

`Asim00740/Kagantic-vault-structure` includes:

```text
Main Index
Product Index
Engineering Index
Operations Index
Feature Specs Index
User Research Index
```

`Main Index.md` tells agents:

```text
start here
choose the most relevant sub-index
prefer summaries and tags before full content
```

## Applicable scenarios

- Small vaults before SQL/FTS exists.
- Project-specific dev context discovery.
- Onboarding a new agent into a domain.
- Building a first context pack.
- Narrowing Product / Engineering / Operations scope.

## Not applicable

- Replacing review queue.
- Proving a claim.
- Ranking truth.
- Replacing source provenance.
- Handling very large vaults without additional retrieval support.

## Minimum implementation

Each project/domain index should include:

```markdown
# Index Name

## AI-readable preamble

When to start here:

What this index routes to:

What not to infer:

## Routes

- [[Child Note]] - why open it

## Risk / Known Failure Modes

- [[Risk Note]] - when to check it
```

## Fusion suggestion

Use before `DEV_CONTEXT.md` pack creation:

```text
project goal
-> read project/domain index
-> inspect summaries/tags
-> create context briefing
-> select Core / Support / Risk / Cold References
```

Use with `MEMORY_TIER.md`:

```text
index links suggest candidates
memory_tier and scope_key still control activation priority
review still controls truth
```

## Boundary

Indexes are maps.

They are not evidence.
