---
type: implementation-note
status: draft
created: 2026-05-27
updated: 2026-06-14
project: verified-action-knowledge-system
related_files:
  - "[[MEMORY_TIER]]"
  - "[[SCHEMA]]"
  - "[[IMPLEMENTATION_BLUEPRINT]]"
  - "[[FEEDBACK]]"
  - "[[2026-05-27-obsidian-para-architecture-review]]"
  - "[[actionability-based-memory-routing]]"
  - "[[archive-first-lazy-reactivation]]"
  - "[[memory-tier-reference-index]]"
  - "[[2026-05-27-kepano-obsidian-architecture-review]]"
  - "[[link-overlap-related-context-surface]]"
  - "[[derived-relatedness-as-truth-signal]]"
  - "[[2026-05-27-knowledge-base-server-architecture-review]]"
  - "[[token-efficient-context-briefing]]"
  - "[[operational-session-capture-loop]]"
  - "[[auto-promotion-without-review-gate]]"
  - "[[2026-05-27-kagantic-vault-structure-architecture-review]]"
  - "[[hierarchical-index-context-routing]]"
  - "[[2026-05-27-dusk-obsidian-vault-architecture-review]]"
  - "[[scope-dashboard-live-context-surface]]"
  - "[[all-in-one-vault-runtime-before-modular-contracts]]"
verification_status: draft
evidence_level: synthetic
confidence: medium
last_verified: 2026-05-28
next_review: 2026-06-03
tags:
  - dev-context
  - context-engineering
  - working-set
  - risk-layer
---

# DEV_CONTEXT.md v0.1

## AI-readable preamble

Dev context is a temporary development-mode working set.

It is created after broad discovery and before implementation. It tells the agent which files are on the desk, which files are supporting references, which risks must be checked, and which sources remain in the archive.

It is not a permanent reviewed knowledge layer and does not replace `MEMORY_TIER.md`.

## 0. Legacy Development Sticky Marker

Legacy marker: this development context/workbench area may still contain old
project-tag or sticky-note language.

From 2026-06-14 onward, do not add new loose "this is useful for VAKS" notes
here for source-level insights.

Use the new route instead:

```text
source-level useful span -> Source Annotation Sidecar
project-level borrow / non-borrow -> Project Overlay
review or action support -> Evidence Packet
```

Existing legacy notes are historical working material. Do not bulk-delete them
until the new annotation workflow is fully landed. When an old sticky note is
touched again, either convert it to `source_annotation`, move project-level scope
into Project Overlay, or mark it as missing source anchor.

## 1. Core Judgment

When the user starts a project, do not load the whole vault into the agent's attention.

Instead:

```text
discover broadly
select relevant materials
build a temporary dev context pack
ask for confirmation to enter development mode
work primarily from the pack
expand only when needed
```

This converts a large knowledge vault into a controlled working memory.

## 2. Dev Context Layers

### Core

Meaning:

```text
Must read and must obey for this task.
```

Use for:

```text
current handoff
current project spec
active architecture decision
active schema or contract
current implementation target
```

Rule:

```text
Core should be small enough to actually load and reason over.
```

Project gate:

```text
Core requires a task, goal, or stop condition.
```

A file is not Core just because it is relevant. It is Core when the current task cannot safely proceed without it.

### Support

Meaning:

```text
Relevant background that can help when design or implementation choices appear.
```

Use for:

```text
reference library reviews
related patterns
prior QA
adjacent implementation notes
similar project examples
```

Rule:

```text
Do not read all support files by default. Expand by need.
```

### Risk

Meaning:

```text
Negative evidence, anti-patterns, failure modes, contradictions, and scope warnings that must not be forgotten.
```

Use for:

```text
anti-patterns
known failure routes
do-not-build-first rules
conflicted claims
wrong-scope warnings
review gates
```

Rule:

```text
Risk is not noise. It is a decision checkpoint.
```

Every high-impact dev context should include at least a minimal risk layer.

PARA does not provide this as a first-class layer.

Keep Risk as a verified-action extension:

```text
PARA tells us where useful material may belong.
Risk tells us what must not be forgotten before action.
```

### Cold References

Meaning:

```text
Original sources and historical records that should remain traceable but not loaded unless evidence is needed.
```

Use for:

```text
raw source files
old query-runs
archived feedback
long source snapshots
external articles or repos
```

Rule:

```text
Keep links and reasons. Open only when tracing evidence, checking history, or resolving conflict.
```

## 3. Development Mode Flow

### Step 1: Discovery

The agent searches the vault for relevant files and signals.

Inputs:

```text
project goal
current task
scope boundaries
known files
known exclusions
```

Output:

```text
candidate context list
```

Candidate discovery signals:

```text
explicit user files
project/domain index pages
scope dashboards / area dashboards
matching scope_key / memory_tier
reviewed relations
source provenance
link overlap
backlinks
tag/category overlap
recent activation
```

Derived relatedness can suggest Support or Cold References.

It cannot make a file Core by itself.

Context briefing:

```text
Before opening full files, produce a compact briefing:
  summaries
  metadata
  memory_tier
  why_suggested
  suggested layer
  source pointers
```

Then choose what to fully read.

This keeps discovery broad without making development mode noisy.

Index-first routing:

```text
If a project or domain index exists, read it before opening individual notes.
Use the index as a map:
  route to likely domains
  inspect summaries/tags
  choose full reads
```

The index is a loading map, not evidence.

### Step 2: Context Pack

The agent creates a temporary context pack using:

```text
Core
Support
Risk
Cold References
Open Questions
Stop Conditions
```

For important or agent-facing packs, also preserve the context envelope:

```text
primary
neighbors
warnings
gaps
suggested_actions
```

Budget trimming may shorten context, but it must not hide critical warnings,
gaps, missing evidence, source-window loss, or action risk. If key support is
trimmed out, the pack cannot remain action-ready.

Retrieval receipts may help assemble a context-pack candidate.

They are not action basis by themselves. A pack that uses adapter output must
still expose source click-back, authority badge, usage badge, warning code, and
stale or scope warnings before it can be reviewed for action-facing use.

Those badges and warnings are preconditions for review only. They are not
enough to create action basis, evidence support, truth confidence, or reviewed
relations. In short: they are not enough to create action basis.

Template:

```text
templates/dev-context-pack.md
```

### Step 3: Confirmation

Before implementation, the agent should report:

```text
Related files are ready.
Core / Support / Risk / Cold References have been separated.
Ask whether to enter development mode.
```

The user can approve, add files, remove files, or ask for a broader scan.

### Step 4: Development

During development:

```text
default to Core
expand to Support when making design choices
check Risk before decisions and writes
open Cold References only for evidence, history, or contradictions
```

### Step 5: Exit

At the end:

```text
write durable outcome back to the vault
record changed assumptions
cool temporary context if no longer active
keep reusable decisions/patterns warm
archive one-off references
```

Project closeout scan:

```text
Core or Support item became reusable:
  write back as warm pattern / decision / implementation note.

Item was only evidence for this task:
  return to cold reference.

Item exposed a failure route:
  write or update Risk / anti-pattern.
```

## 4. Relationship To Base Activation Tier

Base activation tier:

```text
long-term activation hygiene
metadata on notes
lightweight and persistent
```

The historical field name is `memory_tier`, but the concept should be explained as Activation Tier:

```text
The vault has activation tiers, not truth tiers.
Hot means read early, not believe more.
```

Dev context:

```text
short-term project working memory
generated for a task
can include hot, warm, and cold base materials
```

A cold source can be inside a hot dev context as a cold reference.

That means:

```text
it is relevant to the project
but should not be loaded unless evidence is needed
```

PARA mapping for this system:

```text
Projects:
  can inspire Dev Context Core, but only when there is a concrete task/goal.

Areas:
  usually map to Support or durable operating context.

Resources:
  usually map to Support or warm reference material.

Archive:
  usually maps to Cold References.

Risk:
  remains our added layer for anti-patterns, contradictions, and boundaries.
```

This mapping is advisory. It does not change truth status.

Kepano mapping for this system:

```text
categories / Bases:
  can help gather Support candidates and dashboards.

links / backlinks / tag overlap:
  can suggest related context.

templates:
  can keep capture structured without forcing folder movement.

random revisit:
  can create reactivation candidates for old material.
```

These are recall and maintenance signals. They do not replace review.

knowledge-base-server mapping for this system:

```text
kb_context:
  inspires context briefing before full read.

kb_search / kb_search_smart:
  inspires candidate discovery through keyword and semantic retrieval.

SQLite / FTS / embeddings:
  inspire derived retrieval cache, not truth storage.

kb_capture_session / kb_capture_fix:
  inspire closeout writeback and feedback-event candidates.

kb_classify / kb_promote / kb_write:
  useful only behind raw/candidate/review boundaries.
```

These runtime tools help agents find and remember work. They do not replace verified-action promotion.

Dusk mapping for this system:

```text
Area Family / scope dashboard:
  can gather live candidate context: related notes, projects, meetings, tasks, and completed work.

Mail Box / page task:
  can inspire an operational queue for follow-up and closeout.

Monthly note:
  can inspire cooling/reheating review after a work period.

Legacy all-in-one vault:
  warns against making a plugin-heavy full vault the starting architecture.
```

These are workbench and lifecycle ideas. They do not replace the dev context pack or review gate.

## 5. Anti-Drift Rules

Do not let a dev context become stale.

Refresh when:

```text
project goal changes
scope changes
new source invalidates an assumption
implementation moves to a new phase
the user asks for global re-evaluation
```

Do not use a dev context when:

```text
the user asks a general question
the user asks for unrelated exploration
the context pack was built for another project
```

## 6. Minimum Dev Context Pack Fields

```yaml
record_type: dev-context-pack
context_id:
project:
task:
scope_key:
created:
updated:
created_by:
status: active | paused | completed | archived
mode: discovery | development | audit | handoff
core: []
support: []
risk: []
cold_references: []
open_questions: []
stop_conditions: []
refresh_triggers: []
writeback_targets: []
```

## 7. v0.1 Stop Point

This file defines how development-mode working memory should operate.

Not implemented yet:

```text
automatic context pack builder
context freshness scoring
Obsidian Bases view
agent command wrapper
context briefing generator
```

Next concrete step:

```text
Create the first real dev context pack for a project after the user provides the next reference materials.
```
