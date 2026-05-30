---
type: source-review
status: draft
created: 2026-05-30
project: verified-action-knowledge-system
source_name: zzyong24/thirdspace-dashboard
source_url: https://github.com/zzyong24/thirdspace-dashboard
checked_commit: 9c0645569c80700f3722db5414ee95819bbd237f
review_mode: read-only source/code review + Obsidian plugin ecosystem check
fusion_decision: adapt-lightly
confidence: medium-high
tags:
  - thirdspace
  - dashboard
  - obsidian
  - vault-health
  - review-queue
  - misa-codex-split
  - alpha-detail-mining
---

# ThirdSpace Dashboard Alpha Review: Vault Health Panel

## One-Line Judgment

ThirdSpace Dashboard 的聪明点不是知识验证，而是：

```text
把文件库状态投影成一个可操作的控制台。
```

Plain version:

```text
资料库不能只是一堆 Markdown。
它还需要一个地方告诉你：哪里积压、哪里有风险、哪里证据不够、哪里需要复审。
但这个面板只能提醒和导航，不能判真，不能替代 review。
```

For our architecture, this should become a small alpha:

```text
Vault Health Panel
```

中文可叫：

```text
资料库健康面板 / Verified Action Health Dashboard
```

## Source Identity

Primary repo:

```text
https://github.com/zzyong24/thirdspace-dashboard
```

Checked commit:

```text
9c0645569c80700f3722db5414ee95819bbd237f
```

Local read-only sandbox clone:

```text
C:\Users\Administrator\Documents\资料库_alpha_lab_2026-05-30\repos\thirdspace-dashboard
```

Repo self-description:

```text
ThirdSpace Dashboard - Obsidian plugin for the ThirdSpace vault system.
```

Main source anchors:

- Repo: https://github.com/zzyong24/thirdspace-dashboard
- README feature table: https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/README.md#L39-L46
- README data-source mapping: https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/README.md#L56-L62
- README workspace-index convention: https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/README.md#L89-L101
- README product-status convention: https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/README.md#L105-L116
- README integration notes: https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/README.md#L194-L202

## What This Repo Actually Builds

This is an Obsidian plugin. It registers a sidebar dashboard view, reads vault files, parses frontmatter and specific sections, then renders a compact control panel.

It does not introduce a database. It does not create a separate truth engine. It mostly projects existing Markdown state into panels.

Its panels are:

- vault stats
- activity heatmap
- workspaces
- today's worklog
- today's todos
- quick actions
- product status
- recent files

Core data-source idea:

```text
Markdown files / frontmatter / known sections
-> derived dashboard panels
-> click-through or small routine actions
```

That is the part worth stealing.

## Source And Code Anchors

### Plugin Entry

The plugin registers a custom Obsidian view, adds a ribbon icon, adds an "Open ThirdSpace Dashboard" command, and opens the view in the right sidebar.

Source:

- https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/main.ts#L5-L18
- https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/main.ts#L24-L40

Local file:

```text
C:\Users\Administrator\Documents\资料库_alpha_lab_2026-05-30\repos\thirdspace-dashboard\src\main.ts
```

Why it matters:

```text
Dashboard is a view layer. It lives beside the vault, not inside the truth chain.
```

### File-Backed Time And Skip Rules

It prefers frontmatter timestamps, then falls back to file system timestamps.

Source:

- https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/data/vault-reader.ts#L20-L27

It also excludes system-ish files and folders from ordinary stats.

Source:

- https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/data/vault-reader.ts#L38-L48

Local file:

```text
C:\Users\Administrator\Documents\资料库_alpha_lab_2026-05-30\repos\thirdspace-dashboard\src\data\vault-reader.ts
```

Alpha detail:

```text
健康面板要读业务字段，不要把 README / AGENTS / 系统目录的活动误算成知识质量。
```

For us, this becomes:

```text
review_due / evidence_status / review_status / agent_source
-> dashboard signals

file modified time
-> weak activity signal only
```

### Workspace Index

It reads `.thirdspace/workspace-index.yaml` to learn the vault's workspace layout.

Source:

- https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/data/vault-reader.ts#L70-L93

Why it matters:

```text
The dashboard should not hard-code all directories.
It should read a small routing map.
```

For us, this maps to:

```text
AGENTS.md / wiki indexes / review queues / source intake folders
-> dashboard routing map
```

But we should not copy ThirdSpace's workspace taxonomy wholesale.

### Workspace Stats And Recent Files

It counts Markdown files by workspace and computes recent activity from frontmatter-aware modified times.

Source:

- https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/data/vault-reader.ts#L95-L145

Our adoption:

```text
Good as navigation and freshness hints.
Bad as evidence quality or truth confidence.
```

This must stay a weak operational signal.

### Product Status Parser

It parses `04-项目/product-status.md` and shows product states.

Source:

- https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/data/vault-reader.ts#L147-L172

Our adoption:

```text
We can use the same idea for review status files:

outputs/review
REVIEW_QUEUE.md
FEEDBACK.md
SOURCE_INTAKE.md
context-pack/action-basis records
```

But product status is not our core object. Our core object is:

```text
source
-> candidate point
-> evidence-aware review
-> reviewed node / relation
-> context pack / action basis
-> action
-> feedback / review_due
```

### Today Todo / Worklog Parser

It reads and writes todo items inside the current day's worklog.

Source:

- Read today's todos: https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/data/vault-reader.ts#L174-L198
- Add todo to worklog: https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/data/vault-reader.ts#L200-L223
- Today worklog entries: https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/data/vault-reader.ts#L267-L309

Our adoption:

```text
Use the pattern, not the content model.
```

Meaning:

```text
Instead of today's todos:
  show pending review_due / candidate points / Misa feedback.

Instead of worklog timeline:
  show latest evidence-packet reviews / context-pack uses / action outcomes.
```

### Parallel Panel Loading

The dashboard loads core data in parallel before rendering panels.

Source:

- https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/view.ts#L63-L83

Why it matters:

```text
A health dashboard should be cheap to open.
It should not run a full evidence review just to show the user the queue.
```

For us:

```text
Dashboard reads existing records.
Dashboard does not recompute truth.
```

### Panel Composition

It renders separate panels for workspaces, todos, today, quick actions, recent, and products.

Source:

- https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/view.ts#L120-L159

For us, equivalent panels should be:

- Review Due
- Evidence Gaps
- Candidate Points
- Candidate Relations
- Misa Feedback Inbox
- Recent Context Packs
- Action Outcome Calibration
- Source Anchor Debt

### Quick Actions

It offers quick actions for new note, today's log, todo, search, and inbox.

Source:

- https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/view.ts#L327-L341
- https://github.com/zzyong24/thirdspace-dashboard/blob/9c0645569c80700f3722db5414ee95819bbd237f/src/view.ts#L370-L408

Our adoption:

```text
Quick actions are allowed only for low-risk capture and navigation.
```

Allowed examples:

- open review queue item
- open source record
- create candidate feedback event
- create candidate point shell
- open evidence packet template
- open latest context pack trace

Not allowed:

- promote reviewed truth
- increase confidence
- create reviewed relation
- mark evidence sufficient
- clear review_due without review

## Alpha We Can Absorb

### Alpha Name

```text
Vault Health Panel
```

### Short Definition

```text
A file-backed dashboard that surfaces review pressure, evidence gaps, stale action basis records, and agent feedback waiting for human/Codex review.
```

### Where It Fits

Outer architecture:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
                                      ^                 |
                                      |                 v
                              Vault Health Panel <- feedback / review_due
```

Internal chain:

```text
source
-> candidate point
-> calibration / point collision
-> evidence-aware review
-> reviewed node / reviewed relation
-> context pack / action basis
-> action
-> use ledger / feedback / review_due
-> Vault Health Panel
```

Important:

```text
Vault Health Panel is a projection of state, not a new state authority.
```

It can help decide what to inspect next. It cannot decide what is true.

## What We Should Build Eventually

Not now, and not as a new core subsystem.

First version should be boring and file-backed:

```text
Obsidian Bases or Dataview table
-> filtered views over existing Markdown metadata
-> no custom plugin until repeated use proves the need
```

Candidate views:

### 1. Review Pressure

Shows:

- `review_due: true`
- stale reviewed nodes
- contradicted candidate points
- low-confidence claims used recently

Purpose:

```text
What deserves attention first?
```

### 2. Evidence Gaps

Shows:

- evidence packet missing source anchor
- evidence item with background citation only
- warrant missing
- omission check required but absent
- challenge kind unresolved

Purpose:

```text
Where is the system pretending to know more than it has proven?
```

### 3. Candidate Queue

Shows:

- new candidate points
- point collisions
- candidate relation suggestions
- synthesis-needed items

Purpose:

```text
What is waiting for review?
```

### 4. Misa Feedback Inbox

Shows:

- feedback from Misa
- failed or low-use context packs
- user corrections from API use
- action outcomes that need calibration

Purpose:

```text
Misa can report signals. Codex/human decides what gets reviewed or changed.
```

### 5. Source Anchor Debt

Shows:

- source records without anchor mini-profile
- important claims with URL-only citation
- long sources without source structure map
- imported repo reviews without code anchors

Purpose:

```text
Make provenance debt visible before it leaks into action.
```

### 6. Context Pack / Action Audit

Shows:

- recent context packs
- context pack trace completeness
- action basis records without outcome calibration
- decisions affected by superseded material

Purpose:

```text
Can we replay why an answer/action happened?
```

## Minimal Fields For A Future View

Do not add all of these everywhere. This is the shared field vocabulary for records that already need them.

```yaml
type: candidate_point | evidence_packet | feedback_event | action_basis | source_record
review_status: pending | reviewed | blocked
evidence_status: missing | weak | sufficient
review_due: true | false
agent_source: human | codex | misa
risk_level: low | medium | high
last_used: YYYY-MM-DD
outcome_status: unknown | useful | failed | superseded
source_anchor_count: 0
context_pack_id:
```

The dashboard should read these fields. It should not invent confidence.

## Misa / Codex Split

This repo supports our two-lane future:

```text
Misa on VPS:
  query / API caller / user-facing assistant / feedback reporter

Local Mac or Windows:
  Codex reviewer / file editor / source miner / maintenance worker
```

Dashboard role:

```text
Local-only operations cockpit for user + Codex.
```

Misa should not need the Obsidian dashboard. Misa can query approved context packs and return feedback. The dashboard helps the local reviewer see what Misa has surfaced.

Correct boundary:

```text
Misa can create:
  feedback_event
  candidate_point
  candidate_relation_suggestion
  failed_use signal

Misa cannot create:
  reviewed truth
  reviewed relation
  confidence increase
  evidence sufficiency judgment
  promotion
```

The health panel is where Misa's pending signals become visible without becoming truth.

## Obsidian Plugin Ecosystem Check

The user asked whether Obsidian already has dashboard / kanban / health-view style plugins. Yes. We should use existing pieces first.

### Obsidian Bases

Source:

- https://obsidian.md/help/bases/views

What it gives:

```text
Native views over note properties: table, list, cards, map, filter, sort, search, displayed properties.
```

Use for us:

```text
Best first choice for review_due, evidence_status, review_status, and agent_source views.
```

Why:

```text
Our health panel is mostly filtered metadata over Markdown records.
```

### Dataview

Source:

- https://github.com/blacksmithgu/obsidian-dataview

What it gives:

```text
Markdown metadata index and query language.
```

Use for us:

```text
Good for dynamic tables/lists if Bases cannot express the view.
```

Example fit:

```text
TABLE review_status, evidence_status, risk_level
FROM "wiki" OR "outputs"
WHERE review_due = true
```

Boundary:

```text
Dataview output is a query result, not reviewed knowledge.
```

### Tasks

Source:

- https://github.com/obsidian-tasks-group/obsidian-tasks

What it gives:

```text
Vault-wide task queries, due dates, recurrence, filtering, and source-file updates.
```

Use for us:

```text
Only useful if some review_due items are represented as Markdown tasks.
```

Boundary:

```text
Completing a task cannot clear review_due unless a review record exists.
```

### Metadata Menu

Source:

- https://community.obsidian.md/plugins/metadata-menu

What it gives:

```text
Metadata editing, typed fields, preset values, autocompletion, Dataview table integration.
```

Use for us:

```text
Useful to reduce frontmatter drift on fields like review_status, evidence_status, risk_level, agent_source.
```

Boundary:

```text
Metadata hygiene helps maintenance. It does not validate evidence.
```

### Linter

Source:

- https://platers.github.io/obsidian-linter/

What it gives:

```text
Rules for YAML frontmatter, headings, markdown formatting, and spacing.
```

Use for us:

```text
Useful later for keeping record files parseable.
```

Boundary:

```text
Formatting consistency is not knowledge correctness.
```

### Kanban

Source:

- https://github.com/obsidian-community/obsidian-kanban

What it gives:

```text
Markdown-backed Kanban boards inside Obsidian.
```

Use for us:

```text
Optional for human-friendly queue lanes such as pending / reviewing / blocked / done.
```

Why it is not first choice:

```text
Our health view is query-driven. Bases or Dataview fits better than drag-and-drop cards.
```

Kanban is useful only if we want a visual work queue, not as the source of truth.

## Comparison With Our Current Architecture

ThirdSpace Dashboard:

```text
Strong at operational visibility.
Weak at evidence discipline.
```

Verified Action Knowledge System:

```text
Strong at truth boundary, provenance, review, action trace.
Weak at visible daily maintenance pressure.
```

So the relationship is complementary.

It does not replace our architecture. It fills a missing ergonomics layer:

```text
What should I look at next?
What is risky right now?
What has Misa surfaced?
What evidence is incomplete?
What action basis needs outcome calibration?
```

## What To Adopt

Adopt:

- file-backed projection over existing Markdown records
- health panels for review pressure and evidence debt
- frontmatter-driven filters
- click-through navigation to source/review records
- quick actions only for low-risk capture and candidate shells
- Bases/Dataview-first implementation

Do not adopt:

- activity streak as quality signal
- file count as knowledge value
- worklog/todo structure as core model
- dashboard as truth authority
- custom plugin before we have repeated local need
- quick actions that promote truth

## No Conflict With Current Spine

This alpha does not change the fixed spine:

```text
source
-> candidate point
-> calibration / point collision
-> evidence-aware review
-> reviewed node / reviewed relation
-> context pack / action basis
-> action
-> use ledger / feedback / review_due
```

It only adds a lens over existing states:

```text
use ledger / feedback / review_due
-> dashboard visibility
-> human/Codex chooses next review target
```

Therefore:

```text
dashboard = activation / maintenance / triage
dashboard != truth / evidence / confidence / relation
```

## Practical Recommendation

Do not build a plugin now.

First step should be one or two Obsidian Bases or Dataview views:

```text
View 1: Review Due
View 2: Evidence Gaps
View 3: Misa Feedback Inbox
```

Only build a custom plugin if:

- these views become daily-use tools
- Bases/Dataview cannot express the needed grouping
- quick navigation becomes annoying enough to justify code
- the schema stabilizes after v0.3/v0.4

## Adoption Status

Recommended alpha:

```text
Vault Health Panel
```

Recommended adoption level:

```text
Keep as candidate design pattern.
Implement later as Bases/Dataview view before custom plugin.
```

Recommended mainline wording if adopted:

```text
The vault may expose health views over review_due, evidence gaps, feedback, and action-basis records. These views are operational projections only. They can prioritize review work and navigation, but cannot create reviewed truth, reviewed relations, evidence sufficiency judgments, or confidence changes.
```

## Questions For Opus Review

1. Is `Vault Health Panel` the right name, or should the public wording be `Maintenance View` / `Review Health View`?
2. Should this stay entirely in Obsidian Bases/Dataview for v0.3/v0.4?
3. Which three fields are worth standardizing first: `review_due`, `evidence_status`, `agent_source`, `outcome_status`, or `risk_level`?
4. Should Misa feedback be shown in the same panel as human/Codex review_due, or separated to avoid agent-signal inflation?
5. Should dashboard quick actions be forbidden from writing anything except candidate/feedback shells?

## Final Fusion Judgment

This repo gives us a small but useful alpha:

```text
Make health and review pressure visible from files.
```

It is not a new knowledge layer. It is not a replacement for review. It is a local cockpit for maintenance.

Best absorption:

```text
Vault Health Panel
-> implemented first as Obsidian Bases / Dataview views
-> later maybe custom plugin
-> always read-only toward truth
```

