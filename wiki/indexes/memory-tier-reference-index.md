---
type: implementation-note
status: draft
created: 2026-05-27
updated: 2026-05-27
project: verified-action-knowledge-system
scope:
  - memory-tier
  - dev-context
  - context-engineering
  - activation
related_files:
  - "[[MEMORY_TIER]]"
  - "[[DEV_CONTEXT]]"
  - "[[2026-05-27-memory-tier-and-publishing-pipeline-draft]]"
verification_status: draft
evidence_level: synthetic
confidence: medium
last_verified: 2026-05-27
next_review: 2026-06-03
tags:
  - memory-tier
  - reference-index
  - collision-validation
  - alpha-design
---

# Memory Tier Reference Index

## AI-readable preamble

This index groups external libraries and design references related to memory tier, dev context, activation, and context engineering.

It is a fusion workbench, not a truth layer.

Source records stay in `raw/`; reviews, patterns, anti-patterns, and decisions stay in their normal folders. This index collects their relationships so later design synthesis can compare them.

## Purpose

Use this file to track:

```text
which libraries influenced the memory-tier branch
what exact design idea was borrowed
what source/code evidence supports it
what conflicts or risks appeared
whether the idea supports, contradicts, refines, or replaces our current skeleton
```

## Current Branch Scope

Current branch:

```text
MEMORY_TIER.md
DEV_CONTEXT.md
templates/dev-context-pack.md
```

Current design question:

```text
How should a large verified knowledge vault decide what an agent should load now, what stays nearby, what remains cold, and how project working memory cools down after use?
```

## Reference Library Table

| Library / Source | Source Record | Review | Main Borrowed Idea | Relation To Current Skeleton | Status |
|---|---|---|---|---|---|
| byarbrough/obsidian-para | [[2026-05-27-obsidian-para-source]] | [[2026-05-27-obsidian-para-architecture-review]] | Actionability routing; archive-first lazy reactivation; project goal gate; project closeout scan | refines `MEMORY_TIER` and `DEV_CONTEXT`; warns against folder taxonomy as truth layer | adapted |
| kepano/kepano-obsidian | [[2026-05-27-kepano-obsidian-source]] | [[2026-05-27-kepano-obsidian-architecture-review]] | Property-driven context workbench; link-overlap related context; random revisit cold-memory maintenance | refines view-first activation and Support discovery; warns against derived relatedness as truth | adapted |
| willynikes2/knowledge-base-server | [[2026-05-27-knowledge-base-server-source]] | [[2026-05-27-knowledge-base-server-architecture-review]] | Token-efficient context briefing; shared agent retrieval layer; session/fix capture; incremental vault index | refines runtime retrieval and dev-context briefing; warns against auto-promotion without review | adapted |
| Asim00740/Kagantic-vault-structure | [[2026-05-27-kagantic-vault-structure-source]] | [[2026-05-27-kagantic-vault-structure-architecture-review]] | Hierarchical index context routing; summary/tag pre-read; source hygiene warning | refines Markdown-only context briefing before SQL/MCP; warns against trusting binary vault downloads | adapted-with-caution |
| DuskWasHere/dusk-obsidian-vault | [[2026-05-27-dusk-obsidian-vault-source]] | [[2026-05-27-dusk-obsidian-vault-architecture-review]] | Scope dashboard live context surface; page-task mailbox; monthly closeout; all-in-one-to-modular warning | refines dev context workbench and cooling; warns against copying plugin-heavy vault runtime | adapted-with-caution |

## Extracted Patterns

| Pattern | Source | Design Meaning | Current Use |
|---|---|---|---|
| [[actionability-based-memory-routing]] | [[2026-05-27-obsidian-para-source]] | Activate by likely next use, not generic importance | `activation_reason`, Core selection, scoped hot |
| [[archive-first-lazy-reactivation]] | [[2026-05-27-obsidian-para-source]] | Old material starts cold and reheats through real use | cold default, scoped reactivation, warm only after reuse |
| [[property-driven-context-workbench]] | [[2026-05-27-kepano-obsidian-source]] | Surface context through metadata and dashboards instead of file movement | hot/warm/cold views, scope dashboards, dev context candidate lists |
| [[link-overlap-related-context-surface]] | [[2026-05-27-kepano-obsidian-source]] | Use shared links, backlinks, and tags to suggest related context | Support and Cold Reference candidates for dev context |
| [[random-revisit-cold-memory-maintenance]] | [[2026-05-27-kepano-obsidian-source]] | Bounded revisit of old notes can surface forgotten context and missing links | cold-memory maintenance and reactivation candidates |
| [[token-efficient-context-briefing]] | [[2026-05-27-knowledge-base-server-source]] | Return summaries and metadata before full reads | dev context discovery, query-run briefing, context pack budget control |
| [[shared-agent-memory-retrieval-layer]] | [[2026-05-27-knowledge-base-server-source]] | Multiple agents can share retrieval while writes stay governed | future MCP/API access with strict write boundaries |
| [[operational-session-capture-loop]] | [[2026-05-27-knowledge-base-server-source]] | Capture sessions and fixes as operational memory | closeout writeback, feedback-event candidates, warm/risk candidates |
| [[incremental-vault-index-retrieval-cache]] | [[2026-05-27-knowledge-base-server-source]] | Hash-index Markdown into a rebuildable retrieval cache | future SQLite/FTS dashboard and context briefing cache |
| [[hierarchical-index-context-routing]] | [[2026-05-27-kagantic-vault-structure-source]] | Use index pages as agent-readable maps before full note reads | Markdown-only context briefing, project/domain entrypoints, dev context discovery |
| [[scope-dashboard-live-context-surface]] | [[2026-05-27-dusk-obsidian-vault-source]] | Use a project/area dashboard to gather live related notes, tasks, meetings, and references | dev context candidate surface, workbench view, closeout/cooling scan |

## Extracted Anti-patterns

| Anti-pattern | Source | Warning | Boundary |
|---|---|---|---|
| [[para-folder-taxonomy-as-truth-layer]] | [[2026-05-27-obsidian-para-source]] | Folder categories can help actionability but cannot decide truth | Do not replace `raw/wiki/outputs/products`, review gate, provenance, or relations |
| [[derived-relatedness-as-truth-signal]] | [[2026-05-27-kepano-obsidian-source]] | Link overlap, tags, ratings, and recency can suggest context but cannot prove truth | Use as recall/support candidates only; reviewed relations own truth |
| [[auto-promotion-without-review-gate]] | [[2026-05-27-knowledge-base-server-source]] | Automated classify/summarize/promote/writeback can blur candidate and verified layers | Automation creates candidates; review owns promotion |
| [[binary-vault-template-download-as-trusted-source]] | [[2026-05-27-kagantic-vault-structure-source]] | Downloadable vault archive contains executable payload rather than Markdown vault files | Inspect artifacts; prefer git-tracked Markdown; never execute unknown binaries |
| [[all-in-one-vault-runtime-before-modular-contracts]] | [[2026-05-27-dusk-obsidian-vault-source]] | A plugin-heavy full vault package can overload the architecture before contracts stabilize | Extract modular workbench ideas; do not copy the full runtime |

## Collision Questions

For each future library, compare against these questions:

```text
1. Does it support scoped hot/warm/cold activation?
2. Does it rely on folders, metadata, query logs, or runtime memory?
3. Does it treat old material as archive/cold, or does it keep everything active?
4. Does it separate risk/negative evidence from positive support?
5. Does it have a project-mode or task-mode working context?
6. Does it define a clear exit/cooldown step after work ends?
7. Does it confuse usefulness with truth?
8. Does it provide a smarter alpha than our current Core / Support / Risk / Cold References split?
9. Does it provide a view/dashboard mechanism that avoids physical file movement?
10. Does it have a bounded way to revisit cold material without automatic promotion?
11. Does it provide a low-token briefing before full document reads?
12. Does it separate derived retrieval/cache from human source of truth?
13. Does it expose a scope dashboard, and is that dashboard kept separate from truth authority?
```

## Alpha Candidates

Current alpha candidates from this branch:

```text
1. Use creates activation:
   old/cold material only heats up when a real query or project needs it.

2. Likely-needed-next beats generic importance:
   hot means "needed next for this scope", not "important forever".

3. Risk is a separate working-memory layer:
   negative evidence and anti-patterns should be checked before decisions, not mixed into support context.

4. Project closeout scan:
   after development, reusable knowledge warms; one-off evidence cools; new failure routes become anti-patterns.

5. View-first activation:
   hot/warm/cold should surface through properties, query, and dashboards before folder movement.

6. Derived relatedness for Support:
   links/backlinks/tag overlap can propose Support files, but cannot create Core or truth.

7. Random revisit for cold maintenance:
   deliberate revisit can produce reactivation/review candidates without making old material permanently hot.

8. Briefing before full read:
   summaries and metadata decide what to open; full notes are read only after selection.

9. Derived retrieval cache:
   SQLite/FTS/vector indexes can accelerate activation, but Markdown/YAML remains source of truth.

10. Operational capture loop:
   session/fix logs feed feedback, warm pattern candidates, and risk records after review.

11. Skill plus tool contract:
   retrieval tools need operating instructions; otherwise agents may search/read/write inefficiently.

12. Access surface separation:
   local/admin access, remote access, and external OpenAPI access should expose different write authority.

13. Code map as briefing:
   for code repositories, structural maps can act like context briefings before raw file reads.

14. Markdown index as briefing:
   before SQL/MCP exists, project/domain index pages can provide the first context route.

15. Scope dashboard as candidate surface:
   a project/area page can gather live related notes, tasks, meetings, and references before a dev context pack selects what to load.
```

## Current Collision Synthesis v0.3

PARA, Kepano, knowledge-base-server, Kagantic, and Dusk agree on the most important boundary:

```text
Do not keep everything equally active.
```

They emphasize different mechanisms:

```text
PARA:
  move or place material by likely next action.

Kepano:
  avoid moving material; use properties, links, templates, and views to surface it.

knowledge-base-server:
  index the vault into a derived retrieval layer and brief agents before full reads.

Kagantic:
  use human-readable index pages as a Markdown-only briefing route before full reads.

Dusk:
  gather live scope context through an area/project dashboard that includes related notes, tasks, meetings, and status.
```

Current fusion:

```text
Use PARA for the question:
  Why should this material be activated now?

Use Kepano for the mechanism:
  How can this material surface without file movement?

Use knowledge-base-server for runtime:
  How can an agent retrieve a compact briefing before loading full files?

Use Kagantic for the no-runtime baseline:
  How can Markdown indexes route an agent before SQL/MCP exists?

Use Dusk for the workbench surface:
  How can a scope page show what is currently live without becoming truth authority?

Use verified-action schema for authority:
  Can this material be trusted or used for action?
```

What this validates in our current skeleton:

```text
1. Hot/warm/cold should be metadata and view logic, not physical folders.
2. Dev context should be temporary projection, not permanent relocation.
3. Core / Support / Risk / Cold References remains useful.
4. Risk must stay separate from positive support.
5. Activation/retrieval signals must not change truth confidence.
6. Context briefing should sit between search and full reads.
7. SQLite/FTS/vector belongs in a rebuildable derived layer.
8. Session/fix capture can support cooling, reheating, feedback, and risk discovery.
9. Markdown indexes can provide the first context briefing before runtime retrieval exists.
10. Scope dashboards can gather live context candidates before a dev context pack locks the working set.
```

What this rejects or lowers priority:

```text
1. 01-Hot / 02-Warm / 03-Cold folders as the first implementation.
2. PARA folders as the vault's truth architecture.
3. Link overlap / backlinks / tags as verified relations.
4. Ratings / recency / view rank as confidence.
5. Auto-classification as verified node type.
6. Auto-promotion into formal wiki without review.
7. Retrieval rank as trust or decision authority.
8. Binary vault downloads as trusted source artifacts.
9. Plugin-heavy all-in-one vault runtimes as the starting architecture.
10. Dashboard state as verified truth.
```

Current best alpha:

```text
Heat is not where a file lives.
Heat is how strongly a file is projected into the current task.

Context is not full reading first.
Context is a briefing that tells the agent what deserves full reading.

Runtime briefing is not required for v0.1.
Markdown indexes can be the first briefing layer.

Dashboards are not the final context.
Dashboards are candidate surfaces before the dev context pack.
```

Practical rule:

```text
Support can be suggested by relatedness.
Core requires task necessity.
Truth requires review.
Full read requires a reason.
```

## Current Non-negotiable Boundaries

```text
Activation does not change truth.
Folders do not replace schema.
Usefulness does not equal verification.
Cold does not mean useless.
Dev context does not become permanent memory by default.
Risk layer stays first-class.
Derived relatedness remains recall, not verification.
Context briefing remains loading plan, not evidence.
Derived DB/cache remains rebuildable, not authoritative.
Automated promotion remains candidate generation, not truth promotion.
Tools need an operating contract before they are useful at scale.
Remote agent access must be narrower than local/admin access.
Repository marketing is not source proof.
Download artifacts must be inspected before trust or ingest.
Workbench dashboards do not become truth authority.
All-in-one vault packages should be decomposed into modular patterns.
```

## Dusk Second-Pass Notes

Dusk adds a useful workbench layer and a strong anti-overbundle lesson:

```text
Useful:
  Area Family page as live context dashboard.
  Mail Box as note-level action queue.
  Monthly note as closeout/cooling surface.

This means:
  a scope page can show live candidates before a dev context pack selects Core / Support / Risk / Cold References.

Risk:
  the GitHub repo is explicitly legacy all-in-one, while current development moved to modular components.
  the zip vault includes many bundled community plugin JS files.

This means:
  do not fork the vault or make its plugin stack core architecture.
```

Alpha phrasing:

```text
Index tells the agent where to start.
Dashboard tells the agent what is live.
Briefing tells the agent what deserves full reading.
Dev context pack decides what is loaded.
Review gate decides what is true.
```

## Kagantic Second-Pass Notes

Kagantic is small, but it adds one useful baseline and one strong source-hygiene warning:

```text
Useful:
  Main Index -> Domain Index -> summaries/tags -> selected full reads.

This means:
  context briefing can start as Markdown index routing before SQL/MCP exists.

Risk:
  the advertised zip artifact contains Application.cmd, package.txt, and unit.exe.

This means:
  git-tracked Markdown can be reviewed, but binary download artifacts must not be trusted or executed.
```

## knowledge-base-server Second-Pass Notes

Additional points from the second pass:

```text
Already absorbed:
  SQL/FTS/vector as derived retrieval cache.
  context briefing before full reads.
  operational session/fix capture.
  shared agent memory with governed writes.

Useful later:
  MCP HTTP session isolation and TTL.
  admin-only tool filtering.
  OpenAPI and llms.txt as external agent surfaces.
  skill/SKILL.md plus MCP split: tools are engine, skill is driving policy.
  CODEMAP.md as a codebase briefing before reading or indexing raw code.

Do not adopt now:
  full hosted server stack.
  dashboard/auth/OAuth/deployment machinery.
  direct auto-promotion loop.
```

Alpha phrasing:

```text
Search is not enough.
The agent also needs a retrieval habit.

Tools are not enough.
The tool surface needs an access contract.

Code ingestion is not enough.
The agent should first read a code map, then selectively open files.
```

## Parking Lot For Future Libraries

Add future sources here before synthesis:

| Library / Source | Expected Relevance | First Check |
|---|---|---|
|  |  |  |

## Next Synthesis Step

After 3-5 relevant libraries are recorded:

```text
compare repeated design signals
mark supports / contradicts / refines / replaces
promote stable repeated signals into stronger patterns
keep one-off ideas as watch/candidate
write an updated MEMORY_TIER / DEV_CONTEXT v0.2 proposal
```
