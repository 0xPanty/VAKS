---
type: source
record_kind: source_card
status: source-captured
title: "kepano/kepano-obsidian source review"
source_url: "https://github.com/kepano/kepano-obsidian"
source_type: repo
captured_at: 2026-05-27
captured_by: Codex
raw_location: "temporary clone: %TEMP%/codex-kepano-obsidian"
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - Obsidian
  - bottom-up-notes
  - memory-tier
  - dev-context
  - Bases
  - properties
projects:
  - verified-action-knowledge-system
source_family: obsidian-vault-template
upstream_sources:
  - "https://stephango.com/vault"
verification_status: single-source
candidate_relation_suggestions:
  - target: "[[2026-05-27-kepano-obsidian-architecture-review]]"
    type: derived_from
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-kepano-obsidian-source]]"
    rationale: "This source record anchors the architecture review and extracted patterns."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - source
  - repo
  - obsidian
  - kepano
  - memory-tier
  - bases
knowledge_status: raw
processing_tier: light
source_id: "https://github.com/kepano/kepano-obsidian"
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
---
# Source Record: kepano/kepano-obsidian

## Why captured

User asked to inspect `kepano/kepano-obsidian` with the same source-level rigor as the PARA review: understand its design logic, preserve source/code anchors, extract what can strengthen the whole architecture, and specifically compare against the current memory-tier / dev-context branch.

## Source information

- Author: Steph Ango / kepano
- Publisher: GitHub
- Repo URL: https://github.com/kepano/kepano-obsidian
- Linked design article: https://stephango.com/vault
- Repo description on GitHub: personal Obsidian vault template with a bottom-up approach to note-taking and organizing interests.
- Capture method: GitHub page + design article + `git clone --depth 1`
- Checked commit: `473697347a0eaac790a6596229c741b3915f3b77`
- Commit time: `2026-01-08T16:01:50-08:00`
- Commit message: `Update attachments`
- GitHub page observed: 149 commits, 3.3k stars, 251 forks, latest release `2.2.0` dated `2025-10-06`.

## Source / Vault Template Map

This repo is not an Obsidian plugin or application runtime. It is a substantial Obsidian vault template with examples, templates, Bases views, and core Obsidian config.

Top-level structure:

```text
.obsidian/
Attachments/
Categories/
Clippings/
Daily/
Notes/
References/
Templates/
.gitignore
LICENSE
Readme.md
```

File count from checked clone:

```text
total tracked files: 142
.obsidian: 6
Attachments: 1
Categories: 21
Clippings: 3
Daily: 2
Notes: 5
References: 19
Templates: 82
```

Important config files:

```text
.obsidian/types.json:
  declares reusable property types such as categories, created, topics, rating, start, end, author, loc, monthly-uses.

.obsidian/core-plugins.json:
  enables bases, daily-notes, templates, random-note, graph, backlinks, bookmarks, canvas, zk-prefixer, etc.

.obsidian/daily-notes.json:
  folder = Daily
  template = Templates/Daily Note Template

.obsidian/zk-prefixer.json:
  format = YYYY-MM-DD HHmm
  folder = /
  template = Templates/Journal Template

.obsidian/app.json:
  attachmentFolderPath = Attachments
  alwaysUpdateLinks = true
```

Important vault files:

```text
Categories/*.md:
  top-level category notes, mostly embedding matching Bases views.

Templates/Bases/*.base:
  database-like views by category, links, backlinks, ratings, recency, images, maps, products, etc.

Templates/*.md:
  category-specific templates with reusable properties.

References/:
  notes about external things such as books, places, people, media, topics.

Clippings/:
  saved external writing.

Notes/:
  example personal notes, projects, evergreen notes, and analysis notes.

Daily/:
  date anchor notes, mostly embedding Daily.base.
```

## Design article observations

The linked article describes the system as:

```text
bottom-up
embraces chaos and laziness
file over app
few folders
categories property + Bases views
heavy internal linking
fractal journaling
random revisit
templates with reusable properties
```

The most relevant design statement for this project:

```text
Use folders lightly; let properties, links, templates, and views create organization over time.
```

## Initial takeaways

1. Kepano is almost the opposite of PARA: less action-folder taxonomy, more bottom-up note capture and view-layer organization.
2. The repo strongly validates metadata-first organization: `categories` property + `.base` views can replace manual folder movement for many workflows.
3. `Related.base` is directly useful for dev-context support discovery: it derives related notes from link overlap, backlinks, and tag overlap.
4. Random revisit and fractal journaling provide a second reactivation path beyond project/query use: old material can be revived by deliberate maintenance/serendipity.
5. Templates make capture lazy but structured. They add just enough metadata to make future views and retrieval work.

## Obvious limits

- This is a personal vault template, not a verified knowledge system.
- It has no review gate, evidence-level contract, truth confidence, negative evidence, or decision rollback model.
- Its organic links and categories are good activation signals, but they cannot replace reviewed relations.
- Ratings and recency are usefulness/experience signals, not truth signals.
- Bottom-up chaos is useful for capture, but dangerous if allowed to govern decisions without verification.

## Candidate points

- Metadata-first view surfaces: use properties and Bases to surface notes instead of moving files.
- Link-overlap related context: use shared links/backlinks/tags as a candidate relatedness signal.
- Fractal review / random revisit: periodically revisit old/cold material to create missing links and reheat useful context.
- Reusable property vocabulary: use consistent, composable property names so views work across categories.
- Category notes as dashboards: category pages are not folders; they are query/view surfaces.
- Daily notes as temporal anchors: daily notes can be indexes into dated entries, not necessarily content stores.

## Direct value for MEMORY_TIER / DEV_CONTEXT

Can absorb:

```text
View-first activation:
  surface hot/warm/cold through metadata and Bases, not folder moves.

Relatedness candidate surface:
  use links/backlinks/tag overlap to suggest Support context, not final truth.

Random revisit:
  scheduled/manual exploration can reheat cold material and create missing links.

Template-backed capture:
  lazy capture can still create useful activation metadata if templates stay small and composable.
```

Cannot absorb as core:

```text
organic links as reviewed relations
ratings as truth confidence
categories as verified node type
bottom-up emergence as decision authority
personal vault style guide as universal schema
```

## Next step

- Created architecture review: `wiki/summaries/2026-05-27-kepano-obsidian-architecture-review.md`
- Created patterns:
  - `wiki/patterns/property-driven-context-workbench.md`
  - `wiki/patterns/link-overlap-related-context-surface.md`
  - `wiki/patterns/random-revisit-cold-memory-maintenance.md`
- Created anti-pattern:
  - `wiki/anti-patterns/derived-relatedness-as-truth-signal.md`
- Updated `MEMORY_TIER.md`, `DEV_CONTEXT.md`, `wiki/indexes/memory-tier-reference-index.md`, `wiki/indexes/knowledge-graph-index.md`, and handoff.
