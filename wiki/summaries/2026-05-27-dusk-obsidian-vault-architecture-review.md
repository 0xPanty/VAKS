---
type: summary
status: summary-draft
created: 2026-05-27
updated: 2026-05-27
sources:
  - "[[2026-05-27-dusk-obsidian-vault-source]]"
topics:
  - Obsidian
  - vault-template
  - PARA
  - Zettelkasten
  - context-workbench
  - memory-tier
verification_status: single-source
evidence_level: primary
confidence: medium
last_verified: 2026-05-27
next_review: 2026-06-03
relations:
  - target: "[[DEV_CONTEXT]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-dusk-obsidian-vault-source]]"
    rationale: "The Area Family template demonstrates a live scope dashboard that gathers related notes, projects, meetings, and tasks."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[scope-dashboard-live-context-surface]]"
    type: supports
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-dusk-obsidian-vault-source]]"
    rationale: "The source directly implements an area-level context dashboard through Dataview and Tasks queries."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[all-in-one-vault-runtime-before-modular-contracts]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-dusk-obsidian-vault-source]]"
    rationale: "The README says the GitHub all-in-one vault is legacy and the current direction is modular components."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - summary
  - obsidian
  - dev-context
  - context-workbench
  - modularity
---

# Dusk Obsidian Vault Architecture Review

## AI-readable preamble

This review treats `DuskWasHere/dusk-obsidian-vault` as a legacy Obsidian vault package.

It is not worth adopting as a whole system.

Its value is:

```text
1. Scope dashboards can gather live project/area context.
2. Page-level tasks and monthly review can feed closeout/cooling.
3. The repo's own evolution from all-in-one to modular validates our modular boundary.
```

## What it is

In plain terms:

```text
Dusk is a ready-made Obsidian workspace.
It combines navigation pages, PARA folders, Zettelkasten folders, dashboards, task inboxes, templates, and many plugins.
```

The GitHub version is explicitly legacy.

The README says the current version moved to modular components, faster performance, and "choose only what you need."

That is the most important architecture signal.

## Core design

Legacy Dusk organizes the vault into:

```text
HUB:
  homepage, map of content, mailbox.

PARA:
  projects, areas, resources, archives, workstation.

ZETA:
  permanent, literature, fleeting notes.

DAILY:
  daily/weekly/monthly notes.

STICKY:
  disposable brainstorming notes.

SYSTEM:
  templates, media, mobile hub, plugin/config surfaces.
```

This is an integrated second-brain environment rather than a verified knowledge architecture.

## Strongest usable design

### Scope dashboard as live context surface

The strongest piece is the `template_area.md` file.

An Area Family page pulls:

```text
area components
connected projects
connected documentation
workstation notes
scheduled meetings
ongoing tasks
completed tasks
```

This is very close to what our `DEV_CONTEXT.md` needs, but with one important difference:

```text
Dusk makes an Obsidian area page a live dashboard.
Our system should make a dev context pack a governed temporary working set.
```

So we absorb the view idea, not the whole vault.

## Secondary usable designs

### Page-level task mailbox

The Mail Box file tracks:

```text
incomplete tasks
unchecked page tasks
unattended meetings
completed tasks
closed timestamp
```

This is useful for future workbench design because it treats a note itself as an actionable item.

For our architecture, this can feed:

```text
query-run follow-up
feedback-event
cooling / closeout
blocked project visibility
```

But the implementation is plugin-heavy and write-capable, so it should not enter v0.1 core.

### Monthly review as cooling surface

The monthly template aggregates:

```text
open tasks
completed tasks
meetings
projects due this month
areas
goals
summary
reflections
next-month plan
```

This supports our cooling/reheating question:

```text
after work ends, what stays warm, what cools, what becomes risk, and what is planned next?
```

Again, use the lifecycle idea, not the plugin stack.

## What it validates

### Supports

It supports our current direction:

```text
metadata and dashboards can surface context without physical file movement
scope-specific pages can gather project-relevant materials
operational state can be separate from truth confidence
closeout/review surfaces are needed for memory cooling
```

### Refines

It refines `DEV_CONTEXT.md` with a practical surface:

```text
project or area scope dashboard
-> candidate Core / Support / Risk / Task surfaces
-> temporary dev context pack
-> implementation
-> closeout / cooldown
```

### Contradicts / warns

It warns against:

```text
copying a full Obsidian vault runtime
making dozens of plugins required for core architecture
turning dashboard state into verified truth
assuming PARA/ZETA folders are the main schema
```

## Collision with previous libraries

PARA:

```text
actionability routing asks where material will be needed next.
```

Kepano:

```text
properties/views surface context without moving files.
```

knowledge-base-server:

```text
runtime retrieval gives briefing before full reads.
```

Kagantic:

```text
Markdown indexes route agents before full reads.
```

Dusk:

```text
scope dashboards gather live related work, meetings, and tasks for an area.
```

Fusion:

```text
Index tells the agent where to start.
Dashboard tells the agent what is active in a scope.
Briefing tells the agent what deserves full reading.
Dev context pack governs what is loaded for development.
Review gate decides what becomes truth.
```

## Fit with main architecture

Fits as:

```text
workbench/view inspiration
scope dashboard reference
operational queue reference
cooling/closeout reference
anti-overbundle evidence
```

Does not fit as:

```text
truth schema
review queue
verification model
source ingest model
MCP/API architecture
formal feedback model
core runtime dependency
```

## Fit with memory-tier branch

Good fit, but only in the view/workbench layer.

Use it to improve:

```text
DEV_CONTEXT discovery surfaces
project/area dashboards
task and meeting awareness
cooling and closeout scans
```

Do not use it to replace:

```text
MEMORY_TIER contract
Core / Support / Risk / Cold References split
traceability-first verification
review gate
schema relations
```

## Source hygiene note

The Dusk zip packages include bundled community plugin JavaScript.

This is not the same risk profile as Kagantic's executable payload, but it is still not something to run during architecture review.

Review mode should stay:

```text
read README
read plain templates
list zip entries
read selected Markdown entries from zip
do not execute/load plugin bundle
```

## Direct judgment

Do not fork.

Do not adopt the whole vault.

Extract:

```text
scope dashboard live context surface
page-level operational task queue as future workbench idea
monthly closeout/cooling surface
all-in-one-to-modular warning
```

The alpha point is not "use Dusk."

The alpha point is:

```text
A scope page can be a living context dashboard, but the authority still belongs to the dev context pack and review gate.
```
