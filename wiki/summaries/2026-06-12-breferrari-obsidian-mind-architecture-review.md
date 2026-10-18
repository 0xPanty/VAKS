---
type: architecture_review
record_kind: architecture_review
status: candidate
title: "breferrari/obsidian-mind architecture review"
source_ref: "raw/repos/2026-06-12-breferrari-obsidian-mind-source.md"
distillation_ref: "outputs/review/2026-06-12-breferrari-obsidian-mind-candidate-distillation.md"
source_id: "github:breferrari/obsidian-mind@9ae6860d01c4bb563dfe972dae89515866f4fbff"
source_url: "https://github.com/breferrari/obsidian-mind"
checked_commit: "9ae6860d01c4bb563dfe972dae89515866f4fbff"
commit_time: "2026-06-02T00:26:28Z"
reviewed_at: "2026-06-12T05:31:19+08:00"
created_by: Codex
knowledge_status: candidate
processing_tier: heavy
truth_status: not_reviewed
action_basis_allowed: false
truth_mutation_allowed: false
retrieval_policy:
  policy_kind: candidate_review_summary
  pack_allowed: context_with_warning
  action_basis_allowed: false
  warning_code: architecture_review_not_adoption
borrow_value: strong
fusion_decision: adapt
current_branch: answer-boundary-agent-workbench-retrieval-surface
project_fit:
  verified_action_knowledge_system: strong_runtime_workbench_fit
  truth_layer: reject_direct
  review_layer: medium_workbench_fit
  activation_layer: strong_fit
  agent_access_layer: strong_fit
  context_pack_layer: medium_fit
assessment:
  domain: obsidian-agent-memory-workbench
  maturity: emerging
  complexity: medium_high
  problem_fit_agent_access: 5
  problem_fit_truth_review: 2
  reuse_value: 4
  implementation_cost: 3
  integration_fit: 4
  evidence_strength: 4
  reversibility: 4
tags:
  - architecture-review
  - candidate
  - vaks/agent-access
  - vaks/obsidian-workbench
  - vaks/retrieval-cache
  - vaks/agent-memory-quarantine
  - risk/authority-pollution
---

# breferrari/obsidian-mind Architecture Review

## One-Line Judgment

`obsidian-mind` is a strong design-only / adapt reference for VAKS's future agent-access, Obsidian workbench, session-context, and derived retrieval surfaces; it should not be used as VAKS's truth system, review authority, or action-basis engine.

## 它解决什么问题

它解决的是：coding agent 每次 session 都失忆，个人工作知识、决策、项目状态、1:1、incident、绩效证据和工作模式不能跨 session 复用。

它的答案是：

```text
Obsidian vault as durable visible memory
+ CLAUDE/AGENTS/GEMINI manuals
+ lifecycle hooks
+ QMD semantic search / MCP
+ slash commands
+ subagents
+ Bases dashboards
+ ShardMind installer/update sidecar
```

这和 VAKS 的问题相邻但不相同。VAKS 要解决的是 verified action knowledge：source -> candidate -> review -> reviewed relation -> context/action basis。`obsidian-mind` 更像 agent workbench + personal work memory。

## 核心设计

### Architecture shape

```text
human + coding agent
-> Obsidian Markdown vault
-> lifecycle hooks
-> QMD/MCP retrieval
-> agent commands/subagents
-> Bases/workbench views
-> personal work/performance memory
```

### Load-bearing split

The most important design split is:

```text
procedural code owns environment
agent owns content judgment
```

This is the part VAKS should most seriously borrow. It prevents every behavior from becoming prompt-only, but it also avoids turning hook code into a silent content authority.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `ARCHITECTURE.md:13-17` | Vault, hook pipeline, QMD layer. | Three-layer runtime around Markdown. | Missing VAKS truth/review gates. |
| `ARCHITECTURE.md:56-58` | Procedural code owns environment; agent owns content. | Thin automation boundary. | Agent content still requires review. |
| `ARCHITECTURE.md:70-82` | Graph-first, vault-first memory, progressive disclosure, agent-agnostic core. | Good operating principles for agent workbench. | Not enough for evidence support. |
| `ARCHITECTURE.md:86-116` | Manifest coordinates version, QMD, infra/user content, frontmatter. | Manifest-centered runtime contract. | Manifest must not become truth authority. |
| `ARCHITECTURE.md:122-169` | Lifecycle hook sequence and design choices. | Inject-not-load, classify-not-route, detached refresh. | Process hints only. |
| `ARCHITECTURE.md:173-225` | QMD + MCP contract. | Typed retrieval interface, per-vault index, wrapper. | VAKS needs buckets and source hashes. |
| `ARCHITECTURE.md:247-278` | Multi-agent portability. | Event-name adapters around shared scripts. | Agent hook APIs may drift. |
| `ARCHITECTURE.md:286-317` | Vault-first memory. | Durable visible `brain/`, private memory as pointer. | VAKS reviewed truth cannot be agent memory. |
| `ARCHITECTURE.md:323-330` | Skills, commands, subagents. | Operational workflow surface. | Commands can over-automate if ungated. |
| `ARCHITECTURE.md:370-378` | ShardMind install contract. | Clone-equivalence and sidecar updates. | Future packaging only. |
| `README.md:194-206` | Token efficiency tiers. | Small startup context + on-demand retrieval. | Needs VAKS coverage/risk warnings. |
| `.claude/scripts/session-start.ts:73-92` | Detached QMD update. | Nonblocking index refresh. | Needs stale-index receipts for VAKS. |
| `.claude/scripts/classify-message.ts:3-39` | Prompt signal classification. | Routing hint channel. | Not intent confirmation. |
| `.claude/scripts/lib/frontmatter.ts:58-79` | Frontmatter and wikilink validation. | Simple write lint. | Not promotion lint. |
| `.claude/scripts/qmd-mcp.mjs:7-21` | Cross-platform MCP launcher. | Practical MCP wrapper pattern. | Version-specific workaround. |
| `.github/workflows/test.yml:1-27` | Cross-platform Node 22/24 test matrix. | Hooks have contract tests. | Test pass is diagnostic only. |

## 当前支线价值

当前支线可以理解为：

```text
answer boundary / Obsidian use surface / future agent access / retrieval cache
```

它对当前支线：

```text
refines / supports / risk_of
```

具体价值：

- Refines how future VAKS agent hooks should behave: context injection, routing hints, lint warnings, detached cache refresh.
- Supports Obsidian Bases as a low-friction workbench and dashboard layer.
- Supports per-vault retrieval index scoping via manifest.
- Supports multi-agent manuals/configs rather than one Claude-only prompt.
- Gives a tested TypeScript hook pattern with 527 local tests passing in this intake run.

风险：

- It makes durable agent memory feel normal; VAKS must quarantine that memory.
- It is not evidence-aware review, source support, or action basis.
- It encourages natural conversation auto-capture; VAKS requires explicit intake/write boundary.

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Strong fit: Markdown vault, index files, lightweight capture, lint hooks. | adapt |
| Dusk workbench | Strong fit: Home, Bases, work dashboards, wrap-up/checklist. | adapt |
| source ingest | Medium: frontmatter and templates help, but source provenance is too weak for VAKS. | adapt cautiously |
| review queue | Medium-low: routes decisions/wins/incidents, but no candidate/review/promotion gate. | adapt only routing hints |
| schema / reviewed knowledge | Reject direct: personal memory notes are not reviewed truth. | reject direct |
| memory / dev context | Strong: vault-first memory, brain topics, SessionStart progressive disclosure. | adapt with quarantine |
| feedback | Medium: brag/win/review feedback surfaces, but not truth-safe by VAKS standards. | adapt carefully |
| retrieval / cache | Strong: QMD named index, MCP wrapper, refresh hooks. | adapt behind bucket filters |
| API / MCP / agent access | Strong: typed MCP retrieval and agent-agnostic hook configs. | adapt after sandbox |
| viewer / workbench | Strong: Bases and Home dashboards. | adapt |
| publishing | Low: not primarily a publishing system. | watch |
| risk / anti-pattern | High: shows the exact risk of agent memory becoming too authoritative. | borrow as warning |

## 值得提炼的模式

### Thin lifecycle hook boundary

Borrow as:

```text
hooks can inject context, classify, validate, refresh derived indexes, and remind closeout
hooks cannot decide truth, review, adoption, confidence, or action readiness
```

### Manifest-centered derived runtime

Borrow as:

```text
one runtime manifest declares derived index names, adapter versions, allowed roots, infra/user content, and stale-index behavior
```

VAKS-specific guard:

```text
SCHEMA/Markdown remains truth contract
runtime manifest remains operational contract
```

### MCP retrieval as typed contract

Borrow as:

```text
MCP gives agents a typed retrieval path instead of shelling out everywhere
```

VAKS-specific guard:

```text
MCP output returns candidates/context envelopes
not evidence support
not reviewed relations
not action basis
```

### Obsidian Bases as operator workbench

Borrow as:

```text
source cards, candidate distillations, review_due, stale anchors, overlays, and missing evidence can be shown in Bases
```

Do not borrow as:

```text
Base view defines schema or truth
```

## 标签与量化

- domain: obsidian-agent-memory-workbench
- problem: persistent context for coding agents and work memory
- pattern: lifecycle hooks + manifest + derived retrieval + visible vault memory
- maturity: emerging
- complexity: medium-high
- problem_fit: 4/5 for VAKS runtime/workbench, 2/5 for truth/review
- reuse_value: 4/5
- implementation_cost: 3/5
- integration_fit: 4/5 if sandboxed
- evidence_strength: 4/5 for code existence/test suite, 2/5 for product effectiveness claims
- reversibility: 4/5 if used as sidecar/runtime only

## 交叉验证

- 相似设计来源：VAKS already has boundaries for QMD/retrieval, Obsidian Bases, agent memory quarantine, workbench vs truth.
- 本地支持：`ARCHITECTURE_PRINCIPLES.md:63-65`, `ARCHITECTURE_PRINCIPLES.md:149-151`, `ARCHITECTURE_PRINCIPLES.md:230`, `SOURCE_INTAKE.md` project overlay and retrieval bucket policies.
- 反例或失败边界：agent memory as reviewed memory; retrieval score as support; dashboard state as truth.
- 最小验证方式：future sandbox only, with a mock VAKS vault and fake candidate/source files; hook outputs must only create receipts/hints, never mutate reviewed files.

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed / Core Boundary | Calibration Output | Review Question |
|---|---|---|---|
| Lifecycle hooks can automate context injection and lint. | VAKS allows runtime/workbench layers but blocks unreviewed truth mutation. | candidate_relation | Which hook events are allowed to write candidate-only records? |
| QMD/MCP can provide per-vault retrieval. | Retrieval is activation, not truth. | refines_candidate | What exact bucket/source-hash filters must precede QMD ranking? |
| `brain/` vault-first memory is visible and portable. | Agent memory is not reviewed memory. | scope_mismatch | Should VAKS agent memory writes go to feedback-event or candidate-only inbox? |
| Bases dashboards make work visible. | Workbench views do not decide truth. | candidate_relation | Which first VAKS Bases are safe: source cards, review queue, stale anchors? |
| ShardMind packages vault templates safely. | Automation/packaging is parked until manual loop works. | watch | Is packaging relevant only after VAKS stabilizes v0.3+? |

## Support / Challenge Review

What supports the candidate value:

- Source code and docs show actual hook configs for Claude, Codex, and Gemini.
- `npm test` passed locally: 527 tests, 0 failures, Node v24.11.0.
- Architecture document is explicit about procedural code vs agent content judgment.
- QMD/MCP integration has concrete wrapper code and tests.

What challenges it:

- Personal work memory is a different problem from verified action knowledge.
- It does not implement evidence-aware review, source support checks, sufficiency gates, or action-basis boundaries.
- The strongest README claims are product/experience claims, not independently verified outcomes.
- Auto-capture and people/performance workflows may be privacy-sensitive.

Challenge severity:

```text
major for direct adoption
minor for design-only borrowing
```

Scope limits:

```text
Use as runtime/workbench/retrieval/agent-access reference only.
Do not use as VAKS truth/review/action architecture.
```

Action readiness:

```text
not_ready for implementation
ready only as candidate reference / project overlay
```

## 对当前项目的适配点

Smallest elegant adoption for VAKS:

```text
1. Keep this as Support/Risk reference.
2. Borrow "hook as hint/lint/receipt" as future Agent Tool Safety posture.
3. Borrow manifest-scoped derived retrieval design only after authority bucket policy is explicit.
4. Use Bases first for read-only review queue/workbench dashboards.
5. Keep agent memory writes quarantined to candidate/feedback-event.
```

No immediate direct code adoption.

## 复杂度和风险

Risks for VAKS:

- Agent auto-capture can silently over-persist ordinary conversation.
- QMD retrieval can look more authoritative than it is.
- Hook routing hints can be mistaken for user intent confirmation.
- `brain/` memory can become a shortcut around reviewed knowledge.
- Bases can become seductive UI truth if badges/boundaries are missing.
- Installing hooks into the formal vault could create surprising writes.

## 不可行点 / 避坑

Do not:

- Fork obsidian-mind as VAKS.
- Use it as the VAKS schema.
- Let `brain/` memory become reviewed memory.
- Let QMD/MCP answers support claims.
- Treat backlinked performance evidence as source-span evidence support.
- Enable Slack/people scanners by default.
- Run ShardMind, QMD bootstrap, or lifecycle hooks inside VAKS main vault without a sandbox and explicit approval.

## 融合判断

- 结论：adapt as design-only candidate.
- 理由：它 cleanly separates hook runtime, agent content judgment, manifest, retrieval, and workbench; these are exactly useful to VAKS runtime surfaces.
- 验证方式：future sandbox with read-only source cards/candidate files, checking hook outputs and derived retrieval receipts.

## 直接判断

- Direct use: no.
- Fork: no.
- Design-only: yes, strong.
- Reject: reject as truth/review/action-basis architecture.
- Current branch value: strong for Obsidian use surface, agent access, retrieval/cache, session context injection.
- Whole architecture value: strong runtime/workbench reference; weak truth/review reference.
- Risk: agent memory pollution, retrieval-as-truth, hook-overreach, privacy.
- Next action: keep candidate-only; use project overlay for future agent-workbench/retrieval tasks.

## 后续行动

If the user later asks to implement an Obsidian/VAKS workbench:

1. Start with read-only Bases dashboards over existing candidate/review files.
2. Then prototype hook/lint receipts in a sandbox folder only.
3. Only after that consider QMD/MCP retrieval, with authority buckets before ranking.
4. Never allow runtime to write reviewed truth without promotion gate.
