---
type: source
status: source-captured
title: "DuskWasHere/dusk-obsidian-vault source review"
source_url: "https://github.com/DuskWasHere/dusk-obsidian-vault"
source_type: repo
captured_at: 2026-05-27
captured_by: Codex
raw_location: "temporary clone: %TEMP%/codex-dusk-obsidian-vault"
processing_mode: immediate
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - Obsidian
  - vault-template
  - PARA
  - Zettelkasten
  - context-workbench
  - memory-tier
projects:
  - verified-action-knowledge-system
source_family: obsidian-vault-template
verification_status: single-source
relations:
  - target: "[[2026-05-27-dusk-obsidian-vault-architecture-review]]"
    type: derived_from
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-dusk-obsidian-vault-source]]"
    rationale: "This source record anchors the Dusk vault architecture review and extracted patterns."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - source
  - repo
  - obsidian
  - vault-template
  - dev-context
  - modularity
---

# Source Record: DuskWasHere/dusk-obsidian-vault

## Why captured

User asked to inspect `DuskWasHere/dusk-obsidian-vault` with the same requirements as prior library reviews: understand the design logic, preserve source/template anchors, extract reusable ideas for the larger verified-action architecture and the current memory-tier / dev-context branch, and avoid forced adoption.

## Source information

- Publisher: GitHub
- Repo URL: https://github.com/DuskWasHere/dusk-obsidian-vault
- Capture method: existing temp clone plus `git ls-remote` verification
- Checked commit: `69fd1e725e21557b9eb7d706ccaa0834288085cb`
- Remote HEAD checked: `69fd1e725e21557b9eb7d706ccaa0834288085cb`
- Commit time: `2025-07-20 12:40:28 +0800`
- Commit message: `Update README.md`
- Local clone used for review: `%TEMP%/codex-dusk-obsidian-vault`

## Repo character

This repo is a legacy Obsidian vault package, not the current maintained system.

The README states that:

```text
GitHub repo = legacy full vault system
Current version = Discord-only modular components, faster performance, choose only what you need
```

This matters because the repo itself validates a migration away from all-in-one vault shipping.

Top-level source surfaces:

```text
README.md
LICENSE
Media/
if you have the older zip file just update these/
Dusk.zip
Dusk_empty.zip
Dusk_light.zip
Dusk_light_empty.zip
```

The update folder includes plain Markdown templates:

```text
template_area.md
template_area_note.md
template_area_note_sub.md
template_monthly_note.md
Mail Box.md
Mobile Mail Box.md
```

The zip files contain full Obsidian vaults, including `.obsidian/plugins/*` JavaScript bundles. I inspected zip listings and selected Markdown entries only. I did not extract, run, or load the vault in Obsidian.

## Source / template map

Relevant inspected surfaces:

```text
README.md:
  legacy/current status, PARA + Zettelkasten vault structure, feature list.

if you have the older zip file just update these/template_area.md:
  Area Family dashboard: components, projects, other docs, meetings, ongoing tasks, completed tasks.

if you have the older zip file just update these/template_area_note.md:
  area_note frontmatter and automatic area tag.

if you have the older zip file just update these/template_area_note_sub.md:
  area_note_sub frontmatter and automatic area tag.

if you have the older zip file just update these/template_monthly_note.md:
  monthly review dashboard for tasks, meetings, projects, areas, goals, reflections, next month.

if you have the older zip file just update these/Mail Box.md:
  Datacore JSX inbox for incomplete tasks, unchecked page tasks, unattended meetings, completed tasks.

Dusk_empty.zip selected entries:
  HUB/Homepage.md
  HUB/Map of Content.md
  HUB/Mail Box.md
  SYSTEM/GETTING STARTED/Vault Onboarding Part 2 - Structure Concept.md
  SYSTEM/GETTING STARTED/Vault Onboarding Part 3 - Main Features.md
  PARA/PROJECTS/README DO NOT DELETE.md
```

## Source anchor matrix

Use this table for later review.

| Source anchor | What exists in source | Design extraction | Our boundary |
|---|---|---|---|
| `README.md:2-29` | The repo is legacy; current development moved to a modular Discord version | Strong reverse evidence against copying all-in-one vault runtime | Do not fork/adopt whole vault; extract modular patterns only |
| `README.md:42-64` | HUB, PARA, ZETA, DAILY, STICKY, SYSTEM plus features like Map of Content, Mail Box, Page Task | Shows an integrated navigation/task/context surface | Useful as UI/workbench inspiration, not verified schema |
| `template_area.md:1-7` | Area Family frontmatter: area, summary, type, created | Scope object with metadata | Metadata can route context but not decide truth |
| `template_area.md:13-38` | Area dashboard pulls components, connected projects, documentation, workstation notes | Scope dashboard as live context surface | Adapt to dev context candidate views |
| `template_area.md:40-66` | Area dashboard pulls scheduled meetings, ongoing tasks, completed tasks by area tag | Operational work context stays attached to scope | Useful for project-mode context packs and closeout |
| `template_area.md:68-74` | Templater hook auto-writes `area/<folder>` tag | Automatic scope tagging | Tags remain recall/activation hints, not evidence |
| `template_monthly_note.md:14-127` | Monthly note aggregates tasks, completed tasks, meetings, projects, and areas | Periodic review surface for cooling/reheating | Use as closeout inspiration, not as required plugin flow |
| `template_monthly_note.md:128-137` | Monthly Goals, Summary, Reflections & Learnings, Plan for Next Month | Human review and next-cycle planning | Fit for dev-context exit and writeback |
| `Mail Box.md:12-34` | Inbox settings: excluded folders, pagination, status values, file_state, closed field | Operational queue with explicit state fields | State can inform feedback/cooling, not verified truth |
| `Mail Box.md:75-98` | Display rules for incomplete tasks, unchecked tasks, unattended meetings, completed tasks | Task mailbox as action queue | Good for future workbench; not needed in v0.1 core |
| `Mail Box.md:105-126` | Checkbox rules update status, file_state, meeting_status, closed timestamp | Page-level task lifecycle | Useful pattern, but plugin-heavy and write-capable |
| `Vault Onboarding Part 2:1-35` | PARA/ZETA separation plus HUB, Map of Content, Mail Box, Archives, Workstation | Use-case separation rule and navigation shell | Separation helps routing; folder categories do not become truth |
| `Vault Onboarding Part 3:15-42` | Page Task can mark any note, project, or meeting and send it to inbox | Note-as-task operational model | Useful as candidate for feedback/work queue, not core now |
| `Vault Onboarding Part 3:72-85` | Area Family shows connected components, projects, docs, workstation notes, meetings, tasks; area file becomes topic MOC | Confirms area dashboard live context surface | Strongest memory-tier/dev-context extraction |
| `PARA/PROJECTS/README DO NOT DELETE.md:1-20` | Project note frontmatter with Priority_Level, Status, Due_Date, connections | Project fields as dashboard filters | Comparable to dev-context pack fields, but not adoption-ready |
| `Dusk_empty.zip` | 455 entries, including bundled community plugin JS files | Full vault distribution is plugin-heavy | Do not load as trusted runtime during design review |

## Zip artifact inspection

I inspected the zip listing only.

Observed in `Dusk_empty.zip`:

```text
entry_count=455
.obsidian/plugins/datacore/main.js
.obsidian/plugins/dataview/main.js
.obsidian/plugins/digitalgarden/main.js
.obsidian/plugins/quickadd/main.js
.obsidian/plugins/templater-obsidian/main.js
.obsidian/plugins/obsidian-projects/main.js
HUB/Homepage.md
HUB/Mail Box.md
HUB/Map of Content.md
SYSTEM/MOBILE HUB/Mobile Homepage.md
SYSTEM/MOBILE HUB/Mobile Mail Box.md
SYSTEM/MOBILE HUB/Mobile Map of Content.md
```

Unlike the Kagantic zip finding, this listing looked like an Obsidian vault package rather than an obvious executable payload. Still, it contains bundled plugin JavaScript, so it should not be executed or loaded during source review.

## Candidate points

- Scope dashboards can serve as live context surfaces.
- An Area Family page can gather components, connected projects, docs, meetings, and tasks without moving files.
- Page-level task status can turn notes into an operational queue.
- Monthly notes can act as closeout/cooling surfaces for tasks, meetings, projects, and reusable learnings.
- The repo's own legacy/current split validates modular components over a bundled all-in-one vault runtime.
- Plugin-heavy vault packages are useful as design references but risky as direct architecture dependencies.

## Direct value for MEMORY_TIER / DEV_CONTEXT

Can absorb:

```text
Scope dashboard:
  a project/area page can surface Core/Support/task candidates from metadata and connections.

Operational queue:
  notes with status/file_state/closed fields can feed feedback, closeout, and cooldown.

Periodic review:
  monthly review surfaces can help decide what stays warm, what cools, and what becomes Risk.

Modular migration lesson:
  a full all-in-one vault can mature into modular components; copy the boundary, not the bundle.
```

Cannot absorb as core:

```text
full vault zip
plugin-heavy runtime
PARA/ZETA folder taxonomy as truth
Datacore JSX as required dependency
automatic page-task writes as verified state
Discord-only current version as inspectable evidence
```

## Next step

- Created architecture review: `wiki/summaries/2026-05-27-dusk-obsidian-vault-architecture-review.md`
- Created pattern:
  - `wiki/patterns/scope-dashboard-live-context-surface.md`
- Created anti-pattern:
  - `wiki/anti-patterns/all-in-one-vault-runtime-before-modular-contracts.md`
- Updated `DEV_CONTEXT.md`, `wiki/indexes/memory-tier-reference-index.md`, `wiki/indexes/knowledge-graph-index.md`, and handoff.
