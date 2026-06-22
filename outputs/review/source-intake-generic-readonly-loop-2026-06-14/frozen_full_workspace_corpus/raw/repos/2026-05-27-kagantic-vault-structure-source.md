---
type: source
record_kind: source_card
status: source-captured
title: "Asim00740/Kagantic-vault-structure source review"
source_url: "https://github.com/Asim00740/Kagantic-vault-structure"
source_type: repo
captured_at: 2026-05-27
captured_by: Codex
raw_location: "temporary clone: %TEMP%/codex-kagantic-vault-structure"
review_priority: normal
review_owner: Codex
formalization_status: candidate-generated
topics:
  - Obsidian
  - vault-template
  - index-navigation
  - agent-context
  - memory-tier
projects:
  - verified-action-knowledge-system
source_family: obsidian-vault-template
verification_status: single-source
candidate_relation_suggestions:
  - target: "[[2026-05-27-kagantic-vault-structure-architecture-review]]"
    type: derived_from
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-kagantic-vault-structure-source]]"
    rationale: "This source record anchors the Kagantic vault structure review and extracted patterns."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - source
  - repo
  - obsidian
  - vault-template
  - context-briefing
  - source-hygiene
knowledge_status: raw
processing_tier: light
source_id: "https://github.com/Asim00740/Kagantic-vault-structure"
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
# Source Record: Asim00740/Kagantic-vault-structure

## Why captured

User asked to inspect `Asim00740/Kagantic-vault-structure` with the same requirements as the previous library reviews: understand the design logic, preserve source/template anchors, extract reusable ideas for the large verified-action architecture and the current memory-tier / dev-context branch, and record risks.

## Source information

- Publisher: GitHub
- Repo URL: https://github.com/Asim00740/Kagantic-vault-structure
- Capture method: `git clone --depth 1`
- Checked commit: `e8890eafa4639f85078e208631839c6d514396af`
- Commit time: `2026-05-27 11:15:52 +0500`
- Commit message: `Update README.md`
- Local clone used for review: `%TEMP%/codex-kagantic-vault-structure`

## Repo character

This repo is a small Obsidian vault example/template, not a plugin or application runtime.

It contains:

```text
README.md
example vault/Main Index.md
example vault/Product/Product Index.md
example vault/Product/Feature Specs/Feature Specs Index.md
example vault/Product/Feature Specs/Feature X - User Mention Alerts.md
example vault/Product/User Research/User Research Index.md
example vault/Product/User Research/Interview Notes - Notification Preferences.md
example vault/Engineering/Engineering Index.md
example vault/Engineering/Architecture Overview.md
example vault/Engineering/Notification Infrastructure Overview.md
example vault/Operations/Operations Index.md
example vault/Operations/Onboarding Playbook.md
example vault/Operations/Remote Work Policy.md
example vault/Operations/vault_Kagantic_structure_3.4.zip
```

## Source / template map

The Markdown vault is organized as:

```text
Main Index
  Product Index
    Feature Specs Index
      Feature X - User Mention Alerts
    User Research Index
      Interview Notes - Notification Preferences
  Engineering Index
    Architecture Overview
    Notification Infrastructure Overview
  Operations Index
    Onboarding Playbook
    Remote Work Policy
```

Each index page includes:

```text
short purpose statement
agent navigation instruction
tags
links to child notes or child indexes
backlink to parent index
```

Each content note includes:

```text
title
Summary section
inline Tags line
body sections
Links section
```

## Source anchor matrix

Use this table for later复盘.

| Source anchor | What exists in source | Design extraction | Our boundary |
|---|---|---|---|
| `README.md` | Describes a ready-to-use Obsidian vault with hierarchy, index files, semantic tags, structured summaries, and AI-friendly navigation | Small-vault index-first context design | README claims are secondary; use actual vault files as evidence |
| `example vault/Main Index.md` | Agent instructions: start here, choose sub-index, prefer files whose summaries/tags match before reading full content | Index as agent entrypoint; local context briefing before full reads | Index routes recall, not truth |
| `example vault/Product/Product Index.md` | Product domain index with feature spec and user research sub-indexes | Domain-scoped routing | Folder/domain does not imply verification |
| `example vault/Engineering/Engineering Index.md` | Engineering domain index for architecture/infrastructure/runbooks | Technical context routing | High-level index cannot replace source-level evidence |
| `example vault/Operations/Operations Index.md` | Operations domain index for policies/playbooks | Process/policy context routing | Policy notes still need ownership and freshness metadata |
| `example vault/Engineering/Architecture Overview.md` | Summary, tags, system components table, flow, links | Content note summary as mini-briefing | Summary is loading aid, not evidence envelope |
| `example vault/Engineering/Notification Infrastructure Overview.md` | Summary, pipeline, integrations, known failure modes, links | Notes can include risk/failure modes inline | Risk should become first-class in our dev context |
| `example vault/Product/Feature Specs/Feature X - User Mention Alerts.md` | User stories, acceptance criteria, edge cases, known limitations, follow-up ideas | Product spec structure can support task context | Product scope is not decision authority by itself |
| `example vault/Product/User Research/Interview Notes - Notification Preferences.md` | Research summary, themes, participant table, links to feature spec | Cross-link research to product decisions | Research synthesis needs source detail before verification |
| `example vault/Operations/vault_Kagantic_structure_3.4.zip` | Zip entries are `Application.cmd`, `package.txt`, `unit.exe`, not Markdown vault files | Distribution/source hygiene risk | Do not execute; do not trust binary artifact as vault source |

## Zip artifact inspection

The repository README points users to download `example vault/Operations/vault_Kagantic_structure_3.4.zip`.

I inspected the zip listing only and did not execute anything.

Observed entries:

```text
Application.cmd
package.txt
unit.exe
```

`Application.cmd` content:

```text
start unit.exe package.txt
```

`package.txt` begins with obfuscated code-like text. This is not a normal Obsidian vault archive.

Source hygiene conclusion:

```text
Treat the Markdown files in the git repo as the reviewable source.
Do not treat the zip artifact as a trustworthy vault template.
Do not execute or unpack binary payloads from a knowledge-template repo.
```

## Candidate points

- Hierarchical index pages can act as a lightweight context briefing surface.
- Agent instructions can be embedded directly into index pages.
- Summary + tags before full reads is a small-vault equivalent of `kb_context`.
- Domain indexes route user queries to Product / Engineering / Operations without SQL or MCP.
- Content notes with `Summary`, `Tags`, and `Links` are easy for both humans and agents to scan.
- Known failure modes inside content notes should be split into Risk when used for development context.
- Download artifacts in knowledge-template repos need source hygiene checks.

## Direct value for MEMORY_TIER / DEV_CONTEXT

Can absorb:

```text
Index-first context routing:
  start from Main Index or project index before opening individual notes.

Summary/tag pre-read:
  summaries and tags decide whether a note deserves full reading.

Domain-scoped routing:
  Product / Engineering / Operations indexes are simple scope routers.

Backlinks to parent indexes:
  keep local navigation recoverable.
```

Cannot absorb as core:

```text
folder hierarchy as truth
inline tags as verified relations
summary as evidence envelope
zip download artifact as trusted source
binary payload as vault template
```

## Next step

- Created architecture review: `wiki/summaries/2026-05-27-kagantic-vault-structure-architecture-review.md`
- Created pattern:
  - `wiki/patterns/hierarchical-index-context-routing.md`
- Created anti-pattern:
  - `wiki/anti-patterns/binary-vault-template-download-as-trusted-source.md`
- Updated `wiki/indexes/memory-tier-reference-index.md`, `wiki/indexes/knowledge-graph-index.md`, and handoff.
