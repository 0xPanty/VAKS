---
type: summary
status: summary-draft
created: 2026-05-27
updated: 2026-05-27
sources:
  - "[[2026-05-27-kepano-obsidian-source]]"
topics:
  - Obsidian
  - bottom-up-notes
  - properties
  - Bases
  - memory-tier
  - dev-context
verification_status: single-source
evidence_level: secondary
confidence: medium
last_verified: 2026-05-27
next_review: 2026-06-03
relations:
  - target: "[[MEMORY_TIER]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-kepano-obsidian-source]]"
    rationale: "Kepano's metadata and Bases approach suggests view-first activation rather than folder-based heat."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[DEV_CONTEXT]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-kepano-obsidian-source]]"
    rationale: "Related.base provides a concrete way to discover Support context through link overlap, backlinks, and tag overlap."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[derived-relatedness-as-truth-signal]]"
    type: risk_of
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-kepano-obsidian-source]]"
    rationale: "Derived relatedness signals are useful for recall but must not become truth or reviewed relations."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - summary
  - obsidian
  - kepano
  - memory-tier
  - dev-context
---

# Kepano Obsidian Architecture Review

## AI-readable preamble

This review treats `kepano/kepano-obsidian` as a personal vault template and view-system reference.

Its useful alpha for our system is view-first activation: use metadata, links, and Bases to surface working context without moving files.

It should not replace the verified-action truth layer, reviewed relations, or decision evidence model.

## What it solves

Kepano's vault solves a different problem from PARA.

PARA asks:

```text
Where is this item likely needed next?
```

Kepano asks:

```text
How can I capture lazily and let useful structure emerge through links, properties, templates, and views?
```

This is valuable for our activation layer because it reduces the need to physically move notes between folders.

## Core design

The repo is organized around a few stable surfaces:

```text
Categories:
  top-level dashboard notes with embedded .base views.

References:
  notes about external things.

Clippings:
  external writing saved into the vault.

Notes:
  personal notes, projects, evergreen notes, analysis examples.

Daily:
  date anchor notes, not heavy content buckets.

Templates:
  property-bearing templates and .base view definitions.
```

The linked article explains the philosophy:

```text
few folders
bottom-up organization
categories property instead of folder taxonomy
profuse internal links
random revisit
fractal journaling
reusable property vocabulary
```

## Source / code extraction

Key implementation surfaces:

```text
.obsidian/types.json:
  reusable property type registry.

Templates/*.md:
  category-specific but small templates.

Templates/Bases/*.base:
  dynamic dashboards and related views.

Categories/*.md:
  notes that embed the matching Bases views.
```

Most important `.base` file for our current branch:

```text
Templates/Bases/Related.base
```

It derives related notes using:

```text
link overlap
backlinks
tag overlap
```

This is a concrete candidate mechanism for dev context Support discovery.

## What is worth extracting

### 1. Property-driven context workbench

Use metadata and view files to surface context, instead of moving files between folders.

This supports our earlier decision:

```text
Do not create 01-Hot / 02-Warm / 03-Cold folders first.
```

### 2. Link-overlap related context surface

Use shared links, backlinks, and tags to find related notes.

This can suggest:

```text
Support files
Cold references worth opening
missing relations
candidate point collisions
```

But it cannot decide truth.

### 3. Random revisit / fractal review

Old notes can be reactivated through deliberate review, not only by explicit project demand.

This adds a new path to `archive-first lazy reactivation`:

```text
project/query reactivation
random revisit reactivation
periodic review reactivation
```

### 4. Reusable property vocabulary

Short, reusable properties let many views work across categories.

For our system, this supports:

```text
memory_tier
scope_key
activation_reason
last_activated
query_intent
review_status
```

But fields must stay governed by `SCHEMA.md`.

## What not to absorb

Do not adopt:

```text
organic links as reviewed relations
ratings as truth confidence
categories as verified node types
bottom-up emergence as decision authority
personal style rules as universal schema
random revisit as automatic promotion
```

## Fit with main architecture

Kepano fits as:

```text
viewer / Obsidian workbench layer
activation layer
capture template reference
related context discovery reference
maintenance/revisit workflow reference
```

It does not fit as:

```text
truth layer
review gate
claim schema
decision schema
agent write protocol
```

## Fit with memory-tier branch

Strong fit:

```text
metadata-first activation
dynamic views instead of folders
related context from links/backlinks/tags
random cold-memory revisit
```

New alpha candidate:

```text
Support context can be discovered from derived relatedness,
but promoted only through review or explicit dev-context selection.
```

## Fusion judgment

Conclusion: `adapt`

Use it to refine:

```text
MEMORY_TIER.md:
  view-first activation, random revisit, metadata-first heat.

DEV_CONTEXT.md:
  link-overlap suggestions for Support, but Risk/Core remain reviewed and task-scoped.

memory-tier-reference-index.md:
  add as a second collision source against PARA.
```

Do not use it to replace:

```text
SCHEMA.md
review queue
verified relations
context pack evidence envelope
```
