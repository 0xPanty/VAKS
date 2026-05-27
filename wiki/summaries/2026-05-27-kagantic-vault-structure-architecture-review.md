---
type: summary
status: summary-draft
created: 2026-05-27
updated: 2026-05-27
sources:
  - "[[2026-05-27-kagantic-vault-structure-source]]"
topics:
  - Obsidian
  - vault-template
  - index-navigation
  - context-briefing
  - memory-tier
verification_status: single-source
evidence_level: secondary
confidence: medium
last_verified: 2026-05-27
next_review: 2026-06-03
relations:
  - target: "[[DEV_CONTEXT]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-kagantic-vault-structure-source]]"
    rationale: "The repo demonstrates index-first routing before opening individual notes, which refines dev context discovery."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[token-efficient-context-briefing]]"
    type: supports
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-kagantic-vault-structure-source]]"
    rationale: "The vault's Main Index asks agents to prefer summaries and tags before reading full content."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[binary-vault-template-download-as-trusted-source]]"
    type: risk_of
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-kagantic-vault-structure-source]]"
    rationale: "The repository's advertised zip artifact contains a cmd file and exe, not a Markdown vault archive."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - summary
  - obsidian
  - index-routing
  - context-briefing
  - source-hygiene
---

# Kagantic Vault Structure Architecture Review

## AI-readable preamble

This review treats `Asim00740/Kagantic-vault-structure` as a small Obsidian vault template.

Its useful idea is simple:

```text
index pages can act as agent-readable context routers.
```

It is not a verified knowledge architecture and not a runtime.

The zip artifact in the repo is a source-hygiene risk and should not be executed or treated as a trusted vault source.

## What it solves

The repo solves a basic navigation problem:

```text
where should a human or agent start reading?
which domain should a query enter?
which file should be opened after the index?
```

It does this with:

```text
Main Index
domain indexes
note summaries
inline tags
links/backlinks
```

## Core design

The core routing tree:

```text
Main Index
-> Product Index
-> Engineering Index
-> Operations Index
```

Each domain index points to a small set of child notes or sub-indexes.

The most important line for our system appears in `Main Index.md`:

```text
Start from this page and follow the links into sub-indexes before opening individual notes.
```

And the agent instruction says:

```text
Prefer files whose summaries and tags match the query before reading full content.
```

This is a small-vault version of context briefing.

## Source / template extraction

Important template surfaces:

```text
example vault/Main Index.md:
  top-level entrypoint and agent navigation rule.

example vault/Product/Product Index.md:
  product domain routing.

example vault/Engineering/Engineering Index.md:
  engineering domain routing.

example vault/Operations/Operations Index.md:
  operations domain routing.

content notes:
  Summary, Tags, body, Links.
```

The implementation is Markdown-only.

There is no:

```text
plugin
script
database
MCP server
schema validation
review gate
agent runtime
```

## What is worth extracting

### 1. Hierarchical index context routing

Index pages can be treated as a low-cost routing layer:

```text
read Main Index
select matching domain index
read summaries/tags
open selected full notes
```

This is useful before a dev context pack is built.

It is especially useful when there is no SQLite/FTS layer yet.

### 2. Index pages as agent entrypoints

The repo writes agent instructions directly into `Main Index.md`.

This supports a simple design for our own project indexes:

```text
AI-readable preamble
when to start here
what this index routes to
what not to treat as truth
```

### 3. Summary/tag pre-read

Each content note has a Summary and Tags line.

For our system, this supports:

```text
context briefing without runtime
manual / Obsidian-first triage
dev context candidate selection
```

### 4. Known failure modes as Risk candidates

The notification infrastructure note has a `Known Failure Modes` section.

This supports our Risk layer:

```text
known failure modes should be pulled into Risk checkpoints when relevant to a dev context.
```

## What not to absorb

Do not adopt:

```text
folder hierarchy as truth
inline tags as verified relations
summary as evidence
generic README claims as source proof
binary zip artifacts as vault source
```

## Fit with main architecture

Fits as:

```text
index/view/workbench layer
manual context briefing reference
small vault onboarding pattern
dev context discovery helper
```

Does not fit as:

```text
truth schema
review queue
verification model
feedback model
runtime retrieval layer
agent access layer
```

## Fit with memory-tier branch

Moderate fit:

```text
index-first routing can help choose what becomes Core/Support/Cold References
summary/tag pre-read can reduce full reads
domain indexes can act as scope selectors
```

But it does not provide:

```text
hot/warm/cold lifecycle
cooldown rules
feedback weights
SQL cache
project closeout
```

## Collision with previous libraries

PARA:

```text
where is this likely needed next?
```

Kepano:

```text
surface context through metadata/views/links without moving files.
```

knowledge-base-server:

```text
brief first through a runtime retrieval layer, then full-read selectively.
```

Kagantic:

```text
brief first through human-readable index pages, then full-read selectively.
```

Fusion:

```text
Runtime briefing is not required for v0.1.
Markdown indexes can be the first briefing layer.
```

## Source hygiene finding

The advertised zip artifact is not a normal Markdown vault archive.

Zip listing:

```text
Application.cmd
package.txt
unit.exe
```

`Application.cmd` starts `unit.exe package.txt`.

This is a strong reason to keep source capture traceability strict:

```text
review git-tracked Markdown
do not execute binary artifacts
do not trust download bundles as sources without inspection
```

## Direct judgment

Do not fork or adopt this as a main architecture.

Extract only:

```text
hierarchical index context routing
index pages as agent entrypoints
summary/tag pre-read
known-failure-mode-to-Risk extraction
source hygiene warning
```
