---
type: implementation-note
status: draft
created: 2026-05-27
updated: 2026-05-28
project: verified-action-knowledge-system
related_files:
  - "[[SCHEMA]]"
  - "[[IMPLEMENTATION_BLUEPRINT]]"
  - "[[DEV_CONTEXT]]"
  - "[[2026-05-27-memory-tier-and-publishing-pipeline-draft]]"
  - "[[2026-05-27-obsidian-para-architecture-review]]"
  - "[[actionability-based-memory-routing]]"
  - "[[archive-first-lazy-reactivation]]"
  - "[[memory-tier-reference-index]]"
  - "[[2026-05-27-kepano-obsidian-architecture-review]]"
  - "[[property-driven-context-workbench]]"
  - "[[random-revisit-cold-memory-maintenance]]"
  - "[[2026-05-27-knowledge-base-server-architecture-review]]"
  - "[[token-efficient-context-briefing]]"
  - "[[incremental-vault-index-retrieval-cache]]"
verification_status: draft
evidence_level: synthetic
confidence: medium
last_verified: 2026-05-28
next_review: 2026-06-03
tags:
  - memory-tier
  - activation
  - context-engineering
  - working-set
---

# Activation Tier / MEMORY_TIER.md v0.1

## AI-readable preamble

Activation Tier is an activation layer, not a truth layer.

This file keeps the historical filename `MEMORY_TIER.md`, but the public concept name is Activation Tier.

hot / warm / cold describe what to read first for a scope, not what is more true.

Strong public wording:

```text
The vault has activation tiers, not truth tiers.
Hot means read early, not believe more.
```

MemGPT supports the fast / slow context-management intuition, but this vault uses it only for activation priority.

It tells a human or agent what to read first, what to keep nearby, and what to leave in the archive unless needed.

It must stay lightweight during normal knowledge capture. Heavy context locking happens in `DEV_CONTEXT.md`, not here.

## 1. Core Judgment

The vault needs two different mechanisms:

```text
base activation tier:
  long-lived, lightweight activation signal for ordinary knowledge management

temporary dev context:
  short-lived working set built for one project or task
```

Do not merge them.

Base activation tier answers:

```text
Should this note be surfaced early by default?
```

Temporary dev context answers:

```text
Should this note be loaded for this exact project or task right now?
```

## 2. Core Rule

Activation tier controls activation priority only.

It does not control:

```text
truth confidence
verification_status
source reliability
decision authority
workflow stage
published status
```

Hard boundary:

```text
hot does not mean true
warm does not mean verified
cold does not mean useless
```

Retrieval activation is not truth.

Vector similarity, graph-neighborhood hits, rerank score, repeated retrieval,
and evaluation score may improve routing or create review_due pressure only.
They must not automatically create a queue item, evidence support, truth
confidence, reviewed relation, action readiness, or action basis.

## 3. Base Tiers

### hot

Meaning:

```text
Current work, active route, active project, current trial, or high-priority item that should be read first.
```

Use hot sparingly.

Examples:

```text
current handoff
current implementation blueprint
active project state
current trial specification
decision that directly governs today's work
```

### warm

Meaning:

```text
Stable reusable context that is often useful but should not be loaded by default every time.
```

Examples:

```text
reviewed patterns
common decisions
stable point clusters
reference library summaries
frequently reused operating rules
```

### cold

Meaning:

```text
Traceable archive material that should remain findable but not automatically occupy attention.
```

Examples:

```text
raw sources
old query runs
historical feedback
archived drafts
old source snapshots
```

Cold material can become relevant again. It should be reactivated through a project scope or dev context, not permanently promoted just because it was used once.

## 4. Required Fields

Use these fields only where they help activation.

```yaml
memory_tier: hot | warm | cold
activation_status: active | dormant | archived
scope_key:
last_activated:
activation_reason:
```

Field meaning:

```text
memory_tier:
  default activation priority

activation_status:
  whether the item is currently active, dormant, or archived

scope_key:
  project, question, domain, or workflow where the activation applies

last_activated:
  last date this item was intentionally surfaced

activation_reason:
  short reason why this item is hot/warm/cold for this scope
```

## 5. Scope Rule

Prefer scoped activation over global activation.

Better:

```yaml
memory_tier: hot
scope_key: verified-action-knowledge-system
activation_reason: "Current implementation target for memory tier design."
```

Risky:

```yaml
memory_tier: hot
activation_reason: "Important."
```

Importance is not enough. The note must be hot for a specific current purpose.

### 5.1 Where-needed-next rule

PARA adds a useful activation question:

```text
Where will this likely be needed next?
```

Use that as the default test for `activation_reason`.

Do not mark a note hot because it is generally important. Mark it hot because it is likely needed next for a concrete scope.

Examples:

```text
Good:
  activation_reason: "Needed next for the memory tier implementation pass."

Weak:
  activation_reason: "Important knowledge."
```

This keeps activation tier aligned with actionability without turning actionability into truth.

## 6. Daily Use

Normal question:

```text
Search broadly enough to understand the question.
Prefer hot/warm if the scope matches.
Use cold when the user asks for source, history, contradiction, or deep review.
```

Current project continuation:

```text
Read matching hot items first.
Then expand to warm if needed.
Only inspect cold references when evidence or history is needed.
```

New project:

```text
Do not reuse old hot blindly.
Perform discovery, then create a temporary dev context.
```

### 6.1 View-first activation

Kepano's vault adds a second strong rule:

```text
Use metadata and views before moving files.
```

For this system:

```text
memory_tier
activation_status
scope_key
last_activated
activation_reason
```

should be enough to surface hot/warm/cold views.

Do not create physical folders just to change activation priority.

### 6.2 Briefing before full read

`knowledge-base-server` adds a runtime rule:

```text
brief first, full-read second
```

For this system:

```text
search / retrieval
-> compact context briefing
-> select Core / Support / Risk / Cold References
-> read only what the task needs
```

The briefing can include:

```text
file
title
record_type
memory_tier
scope_key
summary
key_topics
why_suggested
suggested_layer
```

This is an activation aid.

It still cannot decide:

```text
truth confidence
verification_status
decision readiness
source reliability
```

## 7. Cooling and Reheating

Cooling:

```text
hot -> warm:
  project stage completed, but the note remains reusable

warm -> cold:
  note is no longer commonly activated, but remains traceable

hot -> cold:
  temporary item ended and has no reusable value
```

Reheating:

```text
cold/warm -> hot:
  only for a scope and reason
```

Feedback can reheat material when it creates:

```text
missing-point candidate
wrong-scope correction
contradiction warning
new project relevance
```

Feedback still cannot change truth confidence directly.

### 7.1 Archive-first lazy reactivation

Do not sort every old note upfront.

Default old or unprocessed material to cold unless there is a current scope that needs it.

Use creates activation:

```text
cold source used by a query/project
-> record scope_key and activation_reason
-> include it in dev context as Cold Reference or Support
-> promote to warm only if it proves reusable
-> mark scoped hot only if it is needed for current work
```

This rule comes from the PARA migration pattern:

```text
archive first, move/reactivate when used
```

In this vault, prefer metadata and dev context packs over physical file moves.

### 7.2 Random revisit as cold-memory maintenance

Cold material can also be reactivated through bounded maintenance, not only by project demand.

Allowed:

```text
random revisit old/cold notes
create missing-link candidates
create stale-review candidates
create scoped activation candidates
```

Not allowed:

```text
promote random notes into truth
make random old notes permanently hot
run unbounded automatic rewrite
```

## 8. What Not To Do

Do not create mandatory top-level folders first:

```text
01-Hot/
02-Warm/
03-Cold/
```

Reason:

```text
Manual file movement will become busywork.
Temperature should start as metadata and query/dashboard logic.
Folders can come later only if they reduce friction.
```

Do not rebuild this vault as PARA top-level folders:

```text
1. Projects/
2. Areas/
3. Resources/
4. Archive/
```

Reason:

```text
PARA is useful for actionability routing.
It is not a reviewed knowledge schema.
```

Do not mark everything relevant as hot.

Use:

```text
hot:
  read first

warm:
  expand when useful

cold:
  trace when needed
```

## 9. Relationship To Dev Context

Base activation tier is the vault's long-term activation hygiene.

Dev context is the short-term project working table.

When a project starts:

```text
base vault
-> broad discovery
-> temporary dev context
-> project work
-> useful outcomes written back to base vault
```

The dev context may temporarily activate cold material without changing its base tier.

## 10. v0.1 Stop Point

This file defines the contract only.

Not implemented yet:

```text
dashboard
auto scoring
bulk tier migration
SQLite cache
context briefing builder
scheduled cooling
```

Next concrete step:

```text
Use `templates/dev-context-pack.md` to create one temporary development context from real vault materials.
```
