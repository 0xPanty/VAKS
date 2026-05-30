---
type: source-review
status: draft
created: 2026-05-30
project: verified-action-knowledge-system
source_name: zzyong24/thirdspace-vault-template
source_url: https://github.com/zzyong24/thirdspace-vault-template
checked_commit: acf30f5a523b58e1bb41dd3ff06b5000faec86ae
review_mode: read-only source/code review
fusion_decision: adapt
confidence: medium-high
tags:
  - thirdspace
  - agent-operating-protocol
  - vault-entry
  - progressive-loading
  - agent-quarantine
  - alpha-detail-mining
---

# ThirdSpace Vault Template Alpha Review: Agent Operating Protocol

## One-Line Judgment

ThirdSpace 的聪明点不是知识验证，而是：

```text
Make the vault legible and governable for agents before agents touch files.
```

Plain version:

```text
不要让 Agent 直接进资料库乱翻乱写。
先给它一个入口、一张地图、一套路由规则和写入边界。
```

This is useful for our future Misa / Codex split:

```text
Misa = query / action / feedback caller
Codex = local reviewer / maintainer / writer
Verified Action vault = evidence-backed knowledge base
```

## Source Identity

Primary repo:

```text
https://github.com/zzyong24/thirdspace-vault-template
```

Checked commit:

```text
acf30f5a523b58e1bb41dd3ff06b5000faec86ae
```

Local read-only sandbox clone:

```text
C:\Users\Administrator\Documents\资料库_alpha_lab_2026-05-30\repos\thirdspace-vault-template
```

Repo self-description:

```text
Agent-native, self-contained, path-independent, progressive-loading vault template.
```

README anchors:

- Repo: https://github.com/zzyong24/thirdspace-vault-template
- Design principles: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/README.md#L7-L13
- Directory layout: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/README.md#L48-L64
- Skill table: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/README.md#L67-L80

## What This Repo Solves

It turns an Obsidian / Markdown vault into an agent-readable operating environment.

Core flow:

```text
agent enters anywhere
-> resolve vault root
-> read workspace index and schema
-> route intent to workspace
-> load workspace skill only when needed
-> create / update / audit according to workspace contract
-> record high-value events, not every action
```

It is not a verified knowledge framework. It does not solve:

```text
claim support
evidence warrant
reviewed relation promotion
truth confidence
action basis sufficiency
feedback-driven review_due
```

It solves:

```text
agent entry
workspace routing
progressive loading
file creation discipline
maintenance audit
high-value event capture
```

## Core Design Observed In Code And Docs

### 1. Self-Describing Vault Entry

The root marker is `.thirdspace/workspace-index.yaml`. Agents can find the vault by walking upward from the current directory.

Anchors:

- Local: `.thirdspace/workspace-index.yaml:1-L19`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/.thirdspace/workspace-index.yaml#L1-L19
- Local: `AGENTS.md:3-L13`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/AGENTS.md#L3-L13
- Resolver implementation: `00-系统/Skills/thirdspace-vault/scripts/thirdspace-vault.mjs:941-L955`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/00-%E7%B3%BB%E7%BB%9F/Skills/thirdspace-vault/scripts/thirdspace-vault.mjs#L941-L955

Design extraction:

```text
An agent-facing knowledge base should have one canonical machine-readable entry point.
```

Possible fit for our system:

```text
Verified Action Vault Manifest
or
Knowledge Gateway Manifest
```

Boundary:

```text
The manifest tells agents where and how to enter.
It does not decide what is true.
```

### 2. Progressive Loading Protocol

The repo makes a staged loading rule:

```text
root skill
-> workspace index
-> schema
-> current workspace WORKSPACE.md
-> workspace skill
-> domain skill only when intent matches
```

Anchors:

- Root skill progressive loading: `00-系统/Skills/thirdspace-vault/SKILL.md:28-L40`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/00-%E7%B3%BB%E7%BB%9F/Skills/thirdspace-vault/SKILL.md#L28-L40
- Tool/skill mapping: `.thirdspace/schema/workspace-tools.yaml:8-L69`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/.thirdspace/schema/workspace-tools.yaml#L8-L69
- Skill index progressive protocol: `00-系统/Skills/README.md:94-L102`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/00-%E7%B3%BB%E7%BB%9F/Skills/README.md#L94-L102

Design extraction:

```text
Do not load the whole vault for every task.
Load the smallest relevant rule set and context.
```

Possible fit for our system:

```text
Misa query:
  read gateway manifest
  route query type
  load only context pack / action basis / reviewed evidence needed

Codex local work:
  read AGENTS.md
  read relevant architecture/schema/review docs by task
  write only after explicit user direction
```

Boundary:

```text
Progressive loading is a context economy rule.
It must not hide known challenges, risks, or review_due when action basis is requested.
```

### 3. Workspace As Autonomous Subsystem

ThirdSpace treats each top-level workspace as a subsystem with:

```text
boundary
input
output
status
rules
skill
audit
repair
```

Anchors:

- Design spec: `00-系统/规范/07_自治子系统设计规范.md:13-L26`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/00-%E7%B3%BB%E7%BB%9F/%E8%A7%84%E8%8C%83/07_%E8%87%AA%E6%B2%BB%E5%AD%90%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1%E8%A7%84%E8%8C%83.md#L13-L26
- Machine-readable subsystem contracts: `.thirdspace/schema/subsystems.yaml:1-L78`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/.thirdspace/schema/subsystems.yaml#L1-L78
- Knowledge workspace skill: `00-系统/Skills/workspace-knowledge/SKILL.md:1-L52`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/00-%E7%B3%BB%E7%BB%9F/Skills/workspace-knowledge/SKILL.md#L1-L52

Design extraction:

```text
Folders are not just folders. For agents, each major area needs a contract.
```

Possible fit for our system:

```text
raw/
  source records only

wiki/claims/
  reviewed or review-ready claim notes

outputs/review/
  external-source review outputs, candidate-only by default

templates/
  reusable schema / review / intake templates

00_handoff/
  recovery state and next-window continuity
```

Boundary:

```text
Directory contract is operational hygiene.
It must not create a new truth tier.
```

### 4. Maintenance Action Tiers

ThirdSpace distinguishes repair levels:

```text
automatic repair
semi-automatic repair
trace repair
human confirmation
```

Anchors:

- Maintenance tiers: `00-系统/规范/07_自治子系统设计规范.md:55-L70`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/00-%E7%B3%BB%E7%BB%9F/%E8%A7%84%E8%8C%83/07_%E8%87%AA%E6%B2%BB%E5%AD%90%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1%E8%A7%84%E8%8C%83.md#L55-L70
- Project audit confidence / human confirmation: `00-系统/Skills/workspace-projects/SKILL.md:46-L65`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/00-%E7%B3%BB%E7%BB%9F/Skills/workspace-projects/SKILL.md#L46-L65
- Project audit implementation: `00-系统/Skills/thirdspace-vault/scripts/thirdspace-vault.mjs:1301-L1325`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/00-%E7%B3%BB%E7%BB%9F/Skills/thirdspace-vault/scripts/thirdspace-vault.mjs#L1301-L1325

Design extraction:

```text
Not every maintenance action has the same risk.
Low-risk metadata repair and high-risk knowledge changes need different gates.
```

Possible fit for our system:

```yaml
maintenance_action_tier:
  auto_hygiene:
    examples: [formatting, missing index link, typo in non-truth metadata]
  manifest_required:
    examples: [bulk move, template migration, source reclassification]
  review_due_required:
    examples: [support challenge, stale claim, bad action result]
  human_confirmation_required:
    examples: [delete reviewed node, replace reviewed relation, change architecture principle]
```

Boundary:

```text
Maintenance tier is about edit risk.
It is not a confidence score.
```

### 5. High-Value Event Capture

ThirdSpace records high-value events instead of every action:

```text
git commit facts
major file writes
task completion
completion keywords
summary / why / how / changed files
optional decision / risk
```

Anchors:

- Event capture schema: `.thirdspace/schema/event-capture.yaml:8-L43`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/.thirdspace/schema/event-capture.yaml#L8-L43
- Agent Hook design: `00-系统/规范/08_全局路由与Hook事件采集规范.md:96-L150`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/00-%E7%B3%BB%E7%BB%9F/%E8%A7%84%E8%8C%83/08_%E5%85%A8%E5%B1%80%E8%B7%AF%E7%94%B1%E4%B8%8EHook%E4%BA%8B%E4%BB%B6%E9%87%87%E9%9B%86%E8%A7%84%E8%8C%83.md#L96-L150
- Git commit capture implementation: `00-系统/Skills/thirdspace-vault/scripts/thirdspace-vault.mjs:1132-L1150`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/00-%E7%B3%BB%E7%BB%9F/Skills/thirdspace-vault/scripts/thirdspace-vault.mjs#L1132-L1150
- Agent event capture implementation: `00-系统/Skills/thirdspace-vault/scripts/thirdspace-vault.mjs:1153-L1165`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/00-%E7%B3%BB%E7%BB%9F/Skills/thirdspace-vault/scripts/thirdspace-vault.mjs#L1153-L1165

Design extraction:

```text
Record meaningful use and decisions, not every low-level step.
```

Possible fit for our system:

```text
Use Ledger / Feedback should record:
  context pack used
  action taken
  result
  decision / reason
  failure / review_due trigger
```

For Misa:

```text
Do not log every query.
Log when a context pack was used for action,
when the action failed,
or when Misa proposes a review_due / candidate point.
```

Boundary:

```text
Event capture is memory of use.
It cannot mutate truth.
```

### 6. Route-Create With Trace Fields

The repo's route-create writes trace metadata:

```text
origin_cwd
route_intent
route_reason
route_id
```

Anchors:

- Route-create implementation: `00-系统/Skills/thirdspace-vault/scripts/thirdspace-vault.mjs:975-L1015`
- GitHub: https://github.com/zzyong24/thirdspace-vault-template/blob/acf30f5a523b58e1bb41dd3ff06b5000faec86ae/00-%E7%B3%BB%E7%BB%9F/Skills/thirdspace-vault/scripts/thirdspace-vault.mjs#L975-L1015

Design extraction:

```text
When an agent creates or routes content, the route decision should be auditable.
```

Possible fit for our system:

```yaml
agent_submission_trace:
  submitted_by: misa | codex | human
  origin_context:
  request_type:
  route_reason:
  allowed_write_target: candidate | feedback | review_due_proposal | none
```

Boundary:

```text
Route reason explains why an artifact landed in a candidate/feedback lane.
It is not evidence support.
```

## Candidate Alpha To Absorb

### Alpha Name

```text
Agent Operating Protocol
```

### Plain-English Definition

Before an external agent uses the knowledge base, route it through a controlled entry:

```text
What are you trying to do?
What context are you allowed to read?
What output are you allowed to submit?
What must be handed to Codex / human review?
```

For our future Misa split:

```text
Misa can query.
Misa can use returned context.
Misa can submit feedback / candidate proposals.
Misa cannot write reviewed truth.
Codex performs local review and writeback.
```

### Minimal Schema Sketch

This should be a gateway discipline, not a new truth layer.

```yaml
agent_operating_protocol:
  entry_manifest:
    repo_role: verified_action_knowledge_base
    public_chain: Capture -> Understand -> Review -> Connect -> Act and Learn
    agent_roles:
      misa:
        read_allowed:
          - context_pack
          - action_basis
          - reviewed_node
          - reviewed_relation
          - source_anchor
        write_allowed:
          - feedback_event
          - use_ledger_event
          - candidate_point_proposal
          - review_due_proposal
        write_forbidden:
          - reviewed_node
          - reviewed_relation
          - confidence_change
          - architecture_principle_change
      codex_local:
        read_allowed: [all_project_files]
        write_allowed_after_user_confirmation:
          - review_output
          - schema_doc
          - architecture_doc
          - templates
          - handoff
  query_router:
    request_types:
      - ordinary_lookup
      - source_lookup
      - context_pack_request
      - action_basis_request
      - feedback_submission
      - candidate_submission
      - review_due_submission
  response_contract:
    must_label:
      - reviewed_support
      - auxiliary_context
      - uncertainty
      - scope_limit
      - review_due
```

### Trigger Boundary

Use this for:

```text
Misa / VPS access to the knowledge base
API or local gateway design
agent memory writes
feedback submissions
candidate point submissions
action-basis queries
```

Do not use it for:

```text
ordinary local human reading
simple local Codex research windows
manual source reviews already controlled by AGENTS.md
```

## How It Fits Our Fixed Chain

Current fixed chain remains:

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

Narrow insertion:

```text
external agent / Misa
-> agent operating protocol
-> query router
-> context pack / action basis read
-> action
-> feedback / candidate / review_due proposal
-> Codex local review and writeback
```

Layer placement:

```text
Capture:
  external agent submissions enter as candidate or feedback records.

Understand:
  submissions can become candidate points, never reviewed truth.

Review:
  Codex/human review promotes only if evidence-aware review passes.

Connect:
  Misa can request reviewed relations but cannot create them.

Act:
  Misa can consume action basis returned by the gateway.

Feedback:
  Misa returns use result, failure, correction, review_due proposal.
```

## What It Improves Over Our Current v0.3

### 1. Makes Agent Memory Quarantine Operational

Our v0.3 already says agent memory cannot write reviewed truth.

This repo suggests the missing entrance procedure:

```text
agent enters through a manifest / router,
gets only allowed context,
and submits only allowed artifact types.
```

### 2. Makes Misa / Codex Roles Explicit

Current implicit boundary:

```text
agent feedback does not mutate truth
```

Clear future boundary:

```text
Misa queries and submits.
Codex reviews and writes.
```

### 3. Prevents Whole-Vault Overload

Progressive loading gives a future API rule:

```text
Do not send Misa the whole vault.
Return the smallest sufficient context pack with labels.
```

### 4. Adds Maintenance Risk Tiers

This is a useful complement to maintenance manifest:

```text
format repair != bulk migration != reviewed truth change
```

## Candidate Points For Review

| Candidate Point | Local Fit | Calibration Output | Review Question |
|---|---|---|---|
| External agents should enter through an explicit operating protocol. | Agent memory quarantine / future Misa gateway | refines | Should this be a named rule in DEV_CONTEXT or MEMORY_TIER? |
| Misa should be query-first and write-quarantined. | feedback / use ledger / review_due | supports existing boundary | What exact write targets are allowed? |
| Gateway responses should label reviewed support vs auxiliary context. | context pack trace / action basis | supports PageIndex + GraphRAG alpha | Should this become part of context pack template? |
| Maintenance actions need risk tiers. | maintenance manifest / review_due | refines | Do we add auto/manifest/review_due/human-confirmation tiers? |
| Event capture should be high-value only. | Use Ledger / Feedback | refines | What counts as a Misa use event worth storing? |

## Support / Challenge Review

### What Supports Adoption

```text
The repo has a clear self-describing vault root and agent read order.
```

Source anchors:

- `README.md:7-L13`
- `AGENTS.md:3-L13`
- `.thirdspace/workspace-index.yaml:1-L19`

```text
The root skill defines progressive loading and skill routing.
```

Source anchors:

- `00-系统/Skills/thirdspace-vault/SKILL.md:28-L40`
- `.thirdspace/schema/workspace-tools.yaml:8-L69`

```text
The repo models workspaces as bounded subsystems with audit and repair.
```

Source anchors:

- `00-系统/规范/07_自治子系统设计规范.md:13-L70`
- `.thirdspace/schema/subsystems.yaml:1-L78`

```text
The code implements route trace, event capture, and audit.
```

Source anchors:

- `thirdspace-vault.mjs:975-L1015`
- `thirdspace-vault.mjs:1132-L1165`
- `thirdspace-vault.mjs:1396-L1467`
- `thirdspace-vault.mjs:1550-L1628`

### What Challenges Adoption

```text
The repo is an operations template, not a verified knowledge system.
```

Mitigation:

```text
Borrow only entry/routing/loading/event discipline.
Keep our evidence-aware review as authority.
```

```text
Its frontmatter `source` is source-of-file-origin, not evidence support.
```

Mitigation:

```text
Do not merge ThirdSpace frontmatter semantics with our Evidence Packet support semantics.
```

```text
Its runtime/hooks are automation-heavy.
```

Mitigation:

```text
Do not install hooks or automations unless explicitly requested.
Use the design pattern first.
```

```text
The repo has some internal drift.
```

Observed local read-only check:

```text
node thirdspace-vault.mjs audit-subsystems --vault .
```

It reported:

```text
.thirdspace/schema/workspace-taxonomy.yaml missing
```

while the repo contains:

```text
.thirdspace/schema/taxonomy.yaml
```

Mitigation:

```text
Treat this as a useful template with drift, not a mature source of operational truth.
```

### Challenge Severity

```text
major if copying runtime / hooks / folder structure directly
minor if adopting only Agent Operating Protocol as a design rule
```

## What We Should Not Absorb

Do not absorb:

```text
full ThirdSpace directory structure
.thirdspace runtime as-is
Obsidian dashboard as knowledge quality
Git hooks / stop hooks without explicit user request
source/status frontmatter semantics as evidence semantics
agent direct write access to reviewed truth
workspace router as truth router
automation-heavy maintenance by default
```

## Direct Comparison With Our Architecture

ThirdSpace is better than our current docs at showing:

```text
how an agent discovers a vault
how an agent loads only relevant rules
how a vault exposes workspace contracts
how agent actions are routed and logged
how maintenance actions can be tiered
```

Our architecture is stronger at:

```text
source provenance
candidate point review
Evidence Packet
warrant separation
challenge taxonomy
minimal revision
reviewed node / reviewed relation
context pack / action basis
feedback without truth mutation
review_due
```

Plain comparison:

```text
ThirdSpace teaches how agents should enter and operate.
Our system decides what agents are allowed to believe and use.
```

Best fusion:

```text
Use ThirdSpace-style entry/routing/loading discipline for Misa and future agents.
Keep our verified-action chain as the truth and action authority.
```

## Proposed Minimal Adoption

Adopt only this rule:

```text
External agents must access the vault through an explicit Agent Operating Protocol.
They receive context packs / action basis through a controlled gateway.
They may submit feedback, use events, candidate points, or review_due proposals.
They may not write reviewed truth, change confidence, or create reviewed relations.
Codex performs local review and writeback.
```

Suggested place if later written into main docs:

```text
AGENTS.md:
  add future external-agent access boundary.

DEV_CONTEXT.md:
  define gateway response shape for Misa / external agents.

MEMORY_TIER.md:
  connect agent memory quarantine to query-only / candidate-only writes.

FEEDBACK.md:
  define Misa feedback event and use ledger event shapes.

SCHEMA.md:
  optional agent_submission_trace / external_agent_role.

ARCHITECTURE_PRINCIPLES.md:
  state that Agent Operating Protocol is entry discipline, not truth layer.
```

Do not write these yet without user confirmation.

## Opus Review Questions

1. Should this be named `Agent Operating Protocol`, `Knowledge Gateway`, or `External Agent Access Protocol`?
2. Should Misa ever read raw source files, or only exported context packs/action basis?
3. What exact write channels should Misa have: feedback_event, use_ledger_event, candidate_point_proposal, review_due_proposal?
4. Should gateway responses always label `reviewed_support`, `auxiliary_context`, `uncertainty`, and `scope_limit`?
5. Does maintenance action tiering belong in `FEEDBACK.md`, `SCHEMA.md`, or a separate maintenance template?
6. Should Codex local writeback require user confirmation for all mainline doc changes, or only architecture/schema/reviewed truth changes?
7. How do we prevent event capture from becoming noisy?
8. What is the smallest local prototype: static JSON export, local API, or command-line context pack exporter?

## Final Fusion Judgment

```text
fusion_decision: adapt
alpha_strength: medium-high
implementation_urgency: medium
risk_of_overdesign: medium-high
main_boundary: agent operating protocol is access control and routing, not truth
```

This is a good alpha because it makes the future Misa / Codex / local-vault split explicit without changing the verified-action truth chain.

It should add an entry and routing discipline around our existing system.

It should not replace Evidence Packet, evidence-aware review, or Agent Memory Quarantine.

## Combined Misa / Codex Plain-Language Design

```text
Misa:
  asks the knowledge base for reliable context
  uses returned action basis
  reports what happened
  proposes candidates or review_due
  never edits reviewed truth

Codex:
  reads local files
  reviews Misa submissions
  writes review outputs and approved docs
  updates mainline only when user confirms

Verified Action vault:
  stores sources, candidates, reviewed knowledge, context packs, action basis,
  use ledger, feedback, review_due
```

The clean future shape:

```text
Misa on VPS
-> Knowledge Gateway
-> context pack / action basis
-> action
-> feedback / candidate / review_due proposal
-> Codex local review
-> approved writeback to vault
```

