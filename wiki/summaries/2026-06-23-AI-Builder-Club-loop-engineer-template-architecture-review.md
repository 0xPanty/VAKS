---
type: library_review
status: draft
library_name: "loop-engineer-template"
repo_url: "https://github.com/AI-Builder-Club/loop-engineer-template"
source_url: "raw/repos/2026-06-23-AI-Builder-Club-loop-engineer-template-source.md"
checked_commit: a2267355209713a2184eaeef3b276ec680219d2b
commit_time: 2026-06-18T23:59:11+10:00
source_status: active
reviewed_at: 2026-06-23
domain:
  - agentic-loops
  - loop-engineer
  - file-based-agent-memory
  - codebase-harness
  - verify-before-pr
related_projects:
  - verified-action-knowledge-system
current_branch: "VAKS source-intake/operator-loop design and future MISA execution workflows"
extracted_patterns:
  - file-based-loop-substrate
  - artifact-kind-domain-field-split
  - append-only-timeline-plus-global-log
  - legible-executable-verifiable-harness
  - independent-verifier-before-pr
  - defer-unearned-artifact-kinds
fusion_decision: adapt
confidence: medium
evidence_count: 13
cross_validated_with:
  - "VAKS raw/candidate/reviewed/action-basis boundary"
  - "VAKS Source Annotation Sidecar locator-only boundary"
  - "Prior Agent-Loop-Skills candidate distillation"
negative_evidence:
  - "No Claude Code skills or workflows were executed during this intake."
  - "No loop test run was performed by Codex."
  - "The repo is a starter template and teaching artifact, not an empirical validation report."
  - "The simplified signal/doc model does not encode VAKS authority layers."
extension_potential: "High as a candidate operational substrate and code-harness reference; low as a replacement knowledge authority model."
relations: []
tags:
  - architecture-review
  - loop-engineer
  - agentic-loops
  - codebase-harness
---

# 库分析：AI-Builder-Club/loop-engineer-template

## 它解决什么问题

它解决的不是“知识如何被审定为真”，而是：

```text
一个长期运行的 agent loop
应该住在哪些文件里
如何记录每轮发生了什么
如何把一个代码库改造成 agent 能执行、验证、发 PR 的环境
```

说人话：它是 loop engineer 的项目模板和工作底盘。

## 核心架构

仓库把系统分成两层：

```text
knowledge substrate:
  ARCHITECTURE.md
  CLAUDE.md
  LOG.md
  signals/
  docs/
  domains/

codebase harness:
  .claude/skills/dev-local-setup
  .claude/skills/e2e-setup
  .claude/skills/pr
  .claude/skills/setup-codebase-harness
  .claude/workflows/ship-change.js
```

### Knowledge Substrate

```text
artifacts are global by kind
domain is a frontmatter field
domain folder holds only loop state and machinery
body says what is true now
Timeline says what happened
LOG.md says what work bulk shipped or was ingested
metrics jsonl are written by deterministic collectors
```

This is a clean operating substrate for long-lived loops, but it is not an authority model.

### Codebase Harness

```text
legible:
  map-not-manual root context
  docs as system of record
  custom lints for hard invariants

executable:
  dev-local launcher
  reachable logs
  app drivable

verifiable:
  e2e gate
  video/trace proof
  independent feature verifier
  regression sweep before PR
```

This is the stronger VAKS/MISA engineering borrow.

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:3-6` | Starter template for agents that are triggered, ship work, verify, and log learning. | Loop engineer as recurring system, not per-task prompting. | README framing, not execution proof. |
| `README.md:12-26` | Loop wakes on trigger, writes shared memory, many loops read/write same folders. | Shared brain, many loops. | Shared folder does not create truth authority. |
| `README.md:51-54` | Knowledge base is shared memory; codebase harness makes repo legible, executable, verifiable. | Clean two-layer split. | No local run performed. |
| `ARCHITECTURE.md:16-25` | Artifacts global by kind; domains are loops that link artifacts. | Good anti-duplication model. | VAKS should preserve stricter layer boundaries. |
| `ARCHITECTURE.md:39-52` | New kinds are earned only with status machine, query fields, and distinct body shape. | Strong anti-premature-taxonomy rule. | Needs local volume evidence before adoption. |
| `ARCHITECTURE.md:61-83` | Body plus optional Timeline, LOG.md, metrics jsonl, collectors write data, agents write knowledge. | Strong operational memory and deterministic-data split. | Timelines/logs are traces, not evidence packets. |
| `ARCHITECTURE.md:87-99` | Trigger, threads, entity kinds, derived indexes, reconcile daemons, guardrails deferred. | Good deferral discipline. | VAKS already needs some guardrails upfront due authority risk. |
| `CLAUDE.md:42-64` | Recurring agent context includes substrate model, reuse-before-create, LOG grammar. | Tight recurring context. | `CLAUDE.md` semantics are host-specific. |
| `CLAUDE.md:66-79` | Worktree discipline and worker output contract. | Parallel code agent containment. | Requires host/tool adaptation in Codex. |
| `.claude/skills/setup-codebase-harness/SKILL.md:13-24` | Harness makes repo legible, executable, verifiable. | Best concise harness thesis. | Scaffold guidance, not proof. |
| `.claude/skills/e2e-setup/SKILL.md:23-49` | Real flows, video/trace, stable selectors, fresh data. | Strong verification hygiene. | Test evidence stays operational. |
| `.claude/skills/pr/SKILL.md:11-24` | Fresh verifier handles feature proof; orchestrator handles objective checks. | Good split between intent proof and regression checks. | Feature verifier is not reviewed knowledge. |
| `.claude/workflows/ship-change.js:1-14` | End-to-end scoped code workflow phases. | Good workflow spine. | Claude workflow runtime not tested here. |

## 当前支线价值

当前支线：

```text
VAKS source-intake/operator-loop design and future MISA execution workflows
```

它对当前支线：

```text
refines
```

具体价值：

- Gives VAKS a concrete loop workspace substrate to compare against future `loop_run` or operator-cockpit designs.
- Gives MISA a practical repo harnessing checklist before delegating repeated code work.
- Gives source-intake a minimal "what happened vs what is true now" page convention.
- Gives future review windows a clean distinction between subjective feature proof and objective regression checks.
- Gives architecture work a useful warning against prebuilding many artifact kinds before the status machine is real.

## 与 VAKS 的关键差异

| Zone | Template position | VAKS position | Borrow verdict |
|---|---|---|---|
| Source authority | signal/doc minimal model | raw/candidate/reviewed/action-basis separated | Borrow deferral discipline, not layer model |
| Loop state | domain README | project/loop sidecars with authority boundaries | Adapt carefully |
| Logs | Timeline and LOG.md | provenance and audit traces plus review gates | Borrow as trace only |
| Metrics | deterministic collectors write jsonl | diagnostics cannot become truth | Compatible with warning |
| Code shipping | dev-local, e2e, verifier, PR proof | evidence/action gates still separate | Borrow as engineering harness |
| Host runtime | Claude Code skills and workflows | Codex and local tools need explicit adaptation | Do not assume portability |

## 值得提炼的模式

### Pattern 1: Artifact Kind Vs Domain Field

```text
storage home = what the thing is
domain tag = which loop cares
```

This prevents "workstream folder sprawl" and supports cross-cutting retrieval.

### Pattern 2: Earn New Kinds

```text
add kind only if:
  status machine exists
  queryable fields exist
  body shape is distinct
```

Good for VAKS schema discipline. It should become a design question before any new candidate/review artifact class.

### Pattern 3: Timeline As Run Trace

```text
body = current statement
Timeline = dated operational history
LOG.md = global short feed
git = mechanical diff
```

This is useful for operator memory, but cannot replace evidence packets.

### Pattern 4: Legible, Executable, Verifiable

```text
legible before delegation
executable before autonomy
verifiable before shipping
```

This should be a default checklist before future MISA/VAKS code agents are asked to run loops.

### Pattern 5: Feature Proof Before Regression Sweep

```text
fresh verifier drives the app
orchestrator runs objective checks
PR body leads with proof
```

This is a strong anti-false-done pattern for agent coding.

## Risk

- The template can make a weak knowledge system feel organized without any evidence review.
- `signal/doc` is too coarse for VAKS truth/action boundaries.
- Claude Code skills can seduce Codex work into assuming unavailable runtime affordances.
- LOG/TIMELINE can become a false source of authority if surfaced without warning labels.
- PR proof and e2e video can prove observed behavior, not policy correctness or action basis.

## Fusion Decision

```yaml
fusion_decision: adapt
borrow_layer: operational_substrate_and_engineering_harness
do_not_borrow_as:
  - truth_layer
  - reviewed_knowledge_model
  - evidence_support
  - action_basis_validator
  - universal_agent_runtime
```

