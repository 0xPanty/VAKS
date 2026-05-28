---
type: implementation-note
status: active
created: 2026-05-28
updated: 2026-05-28
project: verified-action-knowledge-system
scope:
  - reference-review
  - repo-review
  - source-analysis
  - architecture-fusion
related_files:
  - "[[SOURCE_INTAKE]]"
  - "[[SCHEMA]]"
  - "[[IMPLEMENTATION_BLUEPRINT]]"
  - "[[memory-tier-reference-index]]"
  - "[[knowledge-graph-index]]"
verification_status: active
evidence_level: synthetic
confidence: high
last_verified: 2026-05-28
next_review: 2026-06-04
tags:
  - reference-review
  - repo-intake
  - architecture-fusion
  - source-anchors
---

# REFERENCE_REVIEW_PROTOCOL.md v0.1

## AI-readable preamble

This is the rule for reviewing external repositories, papers, and architecture references.

The current branch can guide what to inspect first, but it must not narrow the review too much.

Hard rule:

```text
Current branch moves forward opportunistically.
Every reference must still be checked against the whole Verified Action Knowledge System.
```

## 1. Why This Exists

External references are not only for the task of the day.

A repo may be weak for memory-tier but strong for:

```text
source ingest
review queue
schema
lint
feedback
retrieval
API
viewer
agent access
source hygiene
publishing
project workflow
```

Do not miss a main-architecture signal just because the current branch is memory-tier or dev-context.

## 2. Required Review Lenses

Every valuable repo must be reviewed through two lenses.

### Lens A: Current Branch

Ask:

```text
Does it help the branch we are currently landing?
Does it support, contradict, refine, or replace the current branch design?
Does it provide a sharper alpha for the current task?
Does it expose a risk for the current branch?
```

Example current branches:

```text
MEMORY_TIER
DEV_CONTEXT
publishing pipeline
feedback/query-run
point collision
```

### Lens B: Whole Architecture

Ask:

```text
Does it help source capture or ingest?
Does it help candidate extraction or review queue?
Does it help provenance, source ranges, or version tracking?
Does it help schema or relation edges?
Does it help lint/health checks?
Does it help context pack generation?
Does it help feedback or query learning?
Does it help retrieval, cache, API, MCP, or viewer?
Does it help agent write boundaries?
Does it reveal a source hygiene/security risk?
Does it suggest an anti-pattern?
```

## 3. Required Evidence

Do not stop at README if source/templates/config exist.

For repositories, record:

```text
repo URL
checked commit
commit time
source status: active / legacy / deprecated / unknown
files reviewed
source anchor matrix
important functions/classes/templates/configs
what was inspected but not executed
what artifacts were not trusted
```

Source/code anchors should look like:

```text
README.md:2-29
src/db.js:41
templates/context.md
config/workflow.yml
zip listing: Dusk_empty/.obsidian/plugins/dataview/main.js
```

Do not paste large copyrighted source blocks.

Use anchors and short excerpts only where needed.

## 4. Required Output Files

For strong repositories, create or update:

```text
raw/repos/YYYY-MM-DD-name-source.md
wiki/summaries/YYYY-MM-DD-name-architecture-review.md
wiki/patterns/<pattern>.md
wiki/anti-patterns/<anti-pattern>.md
wiki/decisions/<decision>.md when adoption choice is important
wiki/indexes/knowledge-graph-index.md
branch-specific index if relevant
handoff if the session state changed
```

For medium references, a source record plus review summary may be enough.

For weak references, record only if they provide:

```text
a clear negative example
a source hygiene warning
a useful small pattern
```

## 5. Review Questions

Use this checklist.

```text
1. What problem does this reference actually solve?
2. What is the main architecture?
3. What are the source/code/template anchors?
4. What can be borrowed directly?
5. What should only be adapted?
6. What should be rejected?
7. What supports our current branch?
8. What contradicts or weakens our current branch?
9. What supports the whole Verified Action Knowledge System?
10. What creates risk, source hygiene concern, or anti-pattern?
11. Is there an alpha design hidden in it?
12. Is it direct-use, fork, design-only, watch, or reject?
13. What changed in our own architecture after reading it?
```

## 6. Fusion Quality Check

After identifying useful ideas, check whether absorbing them actually improves this system.

```text
1. Is this a positive design addition for us? Why?
2. Compared with the source design, where is our fused version better and where is it weaker?
3. Does this reduce burden, improve judgment quality, or add process complexity?
4. Is there a risk of overdesign or architecture bloat?
5. What is the smallest elegant adoption? What should explicitly not be absorbed?
```

This check prevents forced borrowing.

The goal is not to make the architecture more complete.

The goal is to make it smarter, lighter, and more reliable.

## 7. Fusion Map

When reviewing, map the source to these architecture zones:

| Zone | What To Look For |
|---|---|
| Karpathy spine | raw/wiki/index/log, ingest, query, lint, simple UX |
| Dusk workbench | scope dashboard, task mailbox, project surface, closeout |
| Source ingest | adapters, URL/PDF/repo capture, hash registry, source status |
| Review queue | candidate records, approval flow, provenance gates |
| Schema/reviewed knowledge | claim/pattern/decision fields, relation edges, confidence boundaries |
| Memory/dev context | hot/warm/cold, context briefing, Core/Support/Risk/Cold |
| Feedback | query-run, feedback-event, usefulness/scope fit learning |
| Retrieval/cache | SQL/FTS/vector/BM25/rerank/cache as derived layers |
| Agent access | read/write authority, path-scoped tools, MCP/API boundaries |
| Viewer/workbench | Obsidian Bases, dashboard, graph view, human review UI |
| Publishing | source-to-draft, product outputs, post-publish feedback |
| Risk | anti-patterns, source hygiene, over-automation, stale reviewed knowledge |

## 8. Adoption Labels

Use these labels consistently:

```text
adopt:
  use the idea mostly as-is.

adapt:
  keep the principle, change implementation to fit our contracts.

watch:
  promising but not enough evidence or not needed yet.

reject:
  not useful or conflicts with core boundaries.

design-only:
  do not run/fork/use code; only extract architecture idea.
```

## 9. Direct Judgment Requirement

Every review must end with a plain-language judgment:

```text
Direct use:
Fork:
Design-only:
Reject:
Why:
Current branch value:
Whole architecture value:
Risk:
Next action:
```

No forced borrowing.

If there is no useful point, say so.

## 10. Session Rule

If the user gives a repo during a branch-focused session:

```text
1. Use the branch as the first inspection angle.
2. Then run the whole-architecture pass.
3. Record both.
4. Keep source/code anchors.
5. Update the branch index only if branch-relevant.
6. Update the main knowledge index if architecture-relevant.
```

This keeps the current work moving without losing the main system.
