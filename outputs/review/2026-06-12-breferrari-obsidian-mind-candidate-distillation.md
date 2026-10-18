---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from: "raw/repos/2026-06-12-breferrari-obsidian-mind-source.md"
source_id: "github:breferrari/obsidian-mind@9ae6860d01c4bb563dfe972dae89515866f4fbff"
snapshot_ref: "raw/repos/_snapshots/2026-06-12-breferrari-obsidian-mind-9ae6860d01c4-source.zip"
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
borrow_value: strong
borrow_order:
  - "P1: lifecycle hooks as thin routing/lint/cache refresh, not truth authority"
  - "P1: manifest-centered runtime contract for QMD/MCP/hooks/install boundaries"
  - "P2: QMD/MCP typed retrieval surface after VAKS authority buckets and source hashes"
  - "P2: Obsidian Bases as review/workbench views over structured Markdown"
  - "P3: ShardMind clone-equivalent packaging and module gating for future distribution"
avoid:
  - "agent autonomous durable memory as reviewed truth"
  - "QMD or MCP search result as evidence support"
  - "performance/backlink evidence trail as VAKS action basis"
  - "installing hooks or ShardMind into formal vault before a sandbox pilot"
routing_hint:
  - agent-access
  - obsidian-use-surface
  - retrieval-cache
  - context-pack-preparation
  - project-workbench
  - agent-memory-quarantine
possible_project_refs:
  - "ARCHITECTURE_PRINCIPLES.md"
  - "SOURCE_INTAKE.md"
  - "DEV_CONTEXT.md"
  - "MEMORY_TIER.md"
  - "REVIEW_QUEUE.md"
  - "wiki/indexes/knowledge-graph-index.md"
point_anchor_refs:
  - "README.md:171-177"
  - "ARCHITECTURE.md:56-58"
  - "ARCHITECTURE.md:86-116"
  - "ARCHITECTURE.md:165-169"
  - "ARCHITECTURE.md:173-225"
  - "ARCHITECTURE.md:286-317"
  - ".claude/scripts/qmd-mcp.mjs:7-21"
  - ".claude/scripts/lib/frontmatter.ts:58-79"
tags:
  - candidate
  - provisional
  - vaks/agent-access
  - vaks/retrieval-cache
  - vaks/obsidian-workbench
  - risk/agent-memory-pollution
---

# Candidate Distillation: breferrari/obsidian-mind

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 说人话

这个仓库最值得我们看的不是“它也是 Obsidian vault”，而是它把 agent 工作流拆得比较干净：

```text
Markdown vault 负责长期可见记录
hooks 负责启动、分类、校验、刷新检索
QMD/MCP 负责找东西
agent 负责判断和写内容
Bases 负责让人看见状态
```

对 VAKS 的价值是：以后如果我们要做 agent 入口、Obsidian 工作台、检索缓存、session context injection，它有很多可以直接借的工程边界。危险也很清楚：它是 personal agent memory，不是 verified truth system；如果照搬“agent handles the rest”，会污染 VAKS 的 review/truth/action basis 边界。

## Source

```yaml
derived_from: raw/repos/2026-06-12-breferrari-obsidian-mind-source.md
source_id: github:breferrari/obsidian-mind@9ae6860d01c4bb563dfe972dae89515866f4fbff
snapshot_ref: raw/repos/_snapshots/2026-06-12-breferrari-obsidian-mind-9ae6860d01c4-source.zip
evidence_granularity: table_or_code_anchor
```

## Candidate Points

### CP1. Manifest-centered runtime contract

`vault-manifest.json` is used to coordinate template version, QMD index/context, infrastructure vs user content, scaffold replacement, and required frontmatter.

Anchors:

- `ARCHITECTURE.md:86-116`
- `vault-manifest.json:1-178`
- `scripts/qmd-bootstrap.ts:1-31`

VAKS fit:

```text
Strong for future runtime/derived-index contracts.
```

Potential VAKS adaptation:

```text
VAKS manifest should not define truth.
It can define derived stores, authority buckets, adapter versions, source roots, and allowed write surfaces.
```

Review question:

```text
Should future VAKS derived retrieval/cache have one manifest contract that declares index name, authority buckets, source roots, and stale-index policy?
```

### CP2. Lifecycle hooks should inject and validate, not decide

The repo's lifecycle hooks do lightweight automation:

- `SessionStart` injects a small context.
- `UserPromptSubmit` classifies user messages.
- `PostToolUse` validates frontmatter/wikilinks.
- `PreCompact` backs up transcripts.
- `Stop` prints a checklist.
- QMD refresh is detached/debounced.

Anchors:

- `README.md:179-189`
- `ARCHITECTURE.md:122-169`
- `.claude/settings.json:3-62`
- `.codex/hooks.json:3-51`
- `.gemini/settings.json:3-65`
- `.claude/scripts/classify-message.ts:3-39`
- `.claude/scripts/validate-write.ts:3-58`
- `.claude/scripts/qmd-refresh.ts:3-24`

VAKS fit:

```text
Strong for future Agent Tool Safety and workbench/runtime surfaces.
```

Adaptation:

```text
Hook output can create routing hints, lint warnings, candidate records, or feedback-event candidates.
Hook output must not create reviewed claims, reviewed relations, truth confidence, or action basis.
```

### CP3. QMD/MCP is a useful retrieval surface only after VAKS filters

obsidian-mind scopes QMD through a named index in `vault-manifest.json`; MCP tools and CLI fallback read the same index. The wrapper handles Windows and a qmd MCP index bug.

Anchors:

- `README.md:127-153`
- `ARCHITECTURE.md:173-225`
- `CLAUDE.md:14-19`
- `.mcp.json:1-7`
- `.claude/scripts/qmd-mcp.mjs:7-21`
- `.claude/scripts/qmd-mcp.mjs:181-190`

VAKS fit:

```text
Strong for derived retrieval/cache and context-pack preparation.
```

Required VAKS guard:

```text
authority bucket filter
source hash / freshness filter
scope/project filter
review status filter
then retrieval ranking
```

Do not borrow:

```text
MCP query result as evidence support.
QMD rank as confidence.
Semantic similarity as reviewed relation.
```

### CP4. Vault-first memory is useful, but VAKS needs memory quarantine

obsidian-mind keeps durable agent memory in `brain/` and treats Claude's private memory file as a pointer/index.

Anchors:

- `README.md:171-177`
- `ARCHITECTURE.md:286-317`
- `AGENTS.md:33-48`
- `CLAUDE.md:260-286`

VAKS fit:

```text
Strong as a visibility principle.
Risky as truth policy.
```

VAKS adaptation:

```text
agent memory writes may create candidate notes, feedback events, routing hints, or source cards.
They cannot directly mutate reviewed truth, confidence, reviewed relations, or decisions.
```

### CP5. Bases are a good workbench surface, not authority

The repo ships `.base` views for work dashboard, people directory, incidents, 1:1 history, review evidence, competency map, and templates.

Anchors:

- `README.md:303-314`
- `bases/Review Evidence.base:1-25`
- `bases/Work Dashboard.base`
- `Home.md`

VAKS fit:

```text
Strong for Obsidian use surface and review queue visibility.
```

Adaptation:

```text
Use Bases to show source cards, candidate distillations, review_due, missing evidence, stale anchors, and project overlays.
Do not let Bases define schema or prove truth.
```

### CP6. Backlinks can organize evidence trails, but are not evidence support

obsidian-mind uses work notes, competency notes, PR evidence, brag docs, and backlinks to prepare review season.

Anchors:

- `README.md:287-299`
- `README.md:235`
- `CLAUDE.md:179-236`

VAKS fit:

```text
Medium. Useful as a workbench/evidence-navigation metaphor.
```

Boundary:

```text
Backlink trails can point to evidence.
They cannot count as direct source-span support without independent anchor review.
```

### CP7. ShardMind packaging is future distribution infrastructure

ShardMind adds a wizard, optional modules, sidecar metadata, and three-way upgrade while preserving clone equivalence under defaults.

Anchors:

- `README.md:100-115`
- `ARCHITECTURE.md:370-378`
- `.shardmind/shard.yaml:1-30`
- `.shardmind/shard-schema.yaml:45-86`

VAKS fit:

```text
Watch / P3.
```

Possible future use:

```text
If VAKS ever becomes a distributable template, borrow clone-equivalent install and optional modules.
```

Do not borrow now:

```text
Do not package or install VAKS before the manual source -> candidate -> review -> action basis loop is stable.
```

## Borrow Gradient

```yaml
borrow_value: strong
borrow_order:
  - "P1: thin lifecycle hooks as process aids"
  - "P1: manifest-centered runtime contract"
  - "P2: QMD/MCP typed retrieval surface after VAKS authority filtering"
  - "P2: Bases as review/workbench views"
  - "P3: ShardMind packaging / update sidecar"
avoid:
  - "agent autonomous memory as reviewed truth"
  - "retrieval result as evidence support"
  - "performance review backlink trail as VAKS action basis"
  - "installing hooks/runtime into formal vault before sandbox validation"
```

## Dev Context Hint

```yaml
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "User explicitly approves work on VAKS agent-access hooks, Obsidian use surface, QMD/MCP retrieval, or template packaging."
  support_when: "Designing session context injection, Bases dashboards, review queue workbench, derived retrieval cache, or agent memory quarantine."
  risk_when: "Any proposal lets agent memory, retrieval rank, hook classification, or dashboard state mutate truth/reviewed relations/action basis."
  cold_references:
    - raw/repos/2026-06-12-breferrari-obsidian-mind-source.md
    - raw/repos/_snapshots/2026-06-12-breferrari-obsidian-mind-9ae6860d01c4-source.zip
```

## Open Questions

1. Should VAKS eventually have a `vault-manifest.json`-style derived-runtime manifest, separate from SCHEMA truth contracts?
2. Which hook events are safe for VAKS: session context injection, write lint, and source-card candidate creation only?
3. Would QMD be enough as an early retrieval backend if VAKS adds authority-bucket filters before query/ranking?
4. Should Obsidian Bases be the first official review queue dashboard surface?
5. Is ShardMind relevant only after VAKS becomes a distributable template?

## Routing Hint

Route this source to:

- `agent-access`
- `agent-memory-quarantine`
- `obsidian-use-surface`
- `retrieval-cache`
- `context-pack-preparation`
- `review-queue-workbench`
- `template-packaging-watch`

## Forbidden

```text
project_borrow_scope in generic candidate as adoption conclusion
decision outcome
formal pattern
action basis
truth confidence
```
