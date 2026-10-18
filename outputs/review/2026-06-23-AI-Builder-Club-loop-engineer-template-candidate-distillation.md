---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
source_ref: raw/repos/2026-06-23-AI-Builder-Club-loop-engineer-template-source.md
derived_from:
  - raw/repos/2026-06-23-AI-Builder-Club-loop-engineer-template-source.md
  - raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
  - wiki/summaries/2026-06-23-AI-Builder-Club-loop-engineer-template-architecture-review.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - agentic-loop-design
  - loop-engineer-template
  - file-based-agent-memory
  - codebase-harness
  - verify-before-pr
possible_project_refs:
  - verified-action-knowledge-system
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-loop-shared-memory-substrate.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-artifact-kind-domain-field.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-timeline-log-operational-memory.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-codebase-harness-legible-executable-verifiable.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-verify-before-pr-fresh-verifier.md
point_anchor_refs:
  - "README.md:3-6"
  - "README.md:12-26"
  - "README.md:51-54"
  - "ARCHITECTURE.md:16-25"
  - "ARCHITECTURE.md:39-52"
  - "ARCHITECTURE.md:61-83"
  - "ARCHITECTURE.md:87-99"
  - "CLAUDE.md:42-64"
  - "CLAUDE.md:66-79"
  - ".claude/skills/setup-codebase-harness/SKILL.md:13-24"
  - ".claude/skills/pr/SKILL.md:11-24"
  - ".claude/workflows/ship-change.js:1-14"
borrow_value: strong
borrow_order: P1_support
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "An approved task is specifically designing a bounded loop-engineer substrate, source-intake loop, operator workflow, MISA work-order loop, or code-shipping agent harness."
  support_when: "Agent workflow design, file-based agent memory, loop domain templates, repo harnessing, dev-local/e2e/PR verification, and operator logging."
  risk_when: "A domain README, Timeline, LOG entry, PR proof, or e2e result is being treated as reviewed knowledge, evidence support, or action basis."
  cold_references:
    - raw/repos/2026-06-23-AI-Builder-Club-loop-engineer-template-source.md
    - raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
avoid:
  - "Do not collapse VAKS raw/candidate/reviewed/action-basis layers into the template's minimal signal/doc model."
  - "Do not treat a domain Timeline or LOG.md entry as truth, review, evidence support, or action basis."
  - "Do not assume Claude Code skills/workflows transfer directly to Codex without explicit runtime adaptation."
  - "Do not use GitHub stars, course marketing, README examples, or template popularity as proof of quality."
tags:
  - candidate
  - provisional
  - loop-engineer
  - agentic-loops
  - codebase-harness
---

# 候选蒸馏：AI-Builder-Club/loop-engineer-template

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话结论

这个仓库值得入库，和刚才的 `Agent-Loop-Skills` 不是重复关系：

```text
Agent-Loop-Skills = loop 作为可安装 skill / 方法库
loop-engineer-template = loop engineer 的项目骨架 / 运行底盘 / 代码发版 harness
```

它最值得 VAKS 借的不是 `signals/docs/domains` 这三个名字，而是背后的工程原则：

```text
agent loop 要能长期运行
就需要：
1. 一个可写、可 diff、可审查的共享记忆
2. 一个明确的 loop 状态文件
3. 一个短日志和每个 artifact 的 Timeline
4. 一个能把代码库变成 legible/executable/verifiable 的 harness
5. 一个 verify-before-ship 的闭环
```

## Source

```yaml
derived_from:
  - raw/repos/2026-06-23-AI-Builder-Club-loop-engineer-template-source.md
  - raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
source_annotation_refs:
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-loop-shared-memory-substrate.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-artifact-kind-domain-field.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-timeline-log-operational-memory.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-codebase-harness-legible-executable-verifiable.md
  - outputs/review/source_annotations/2026-06-23-AI-Builder-Club-loop-engineer-template/let-verify-before-pr-fresh-verifier.md
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
    selector_type: file_line
    selector_value: README.md:12-26
  - snapshot_ref: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
    selector_type: file_line
    selector_value: ARCHITECTURE.md:16-25
  - snapshot_ref: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
    selector_type: file_line
    selector_value: .claude/skills/setup-codebase-harness/SKILL.md:13-24
  - snapshot_ref: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
    selector_type: file_line
    selector_value: .claude/skills/pr/SKILL.md:11-24
```

## Candidate Points

### Candidate Point 1: Loop Engineer Is A Project Substrate, Not A Prompt Habit

The repo defines a loop engineer as an agent that wakes on a trigger, does work, verifies, and writes what it learned into shared file memory.

The interesting part for VAKS is not the marketing phrase. It is the substrate:

```text
trigger
-> work
-> verification
-> shared file memory
-> next run reads memory
-> loops compound through same folders
```

For VAKS, this maps to a future "operator loop substrate" only if bounded by:

```text
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
explicit stop / budget / review gate
```

### Candidate Point 2: Minimal Knowledge Model, Strong Anti-Premature-Taxonomy Rule

The repo's knowledge model starts with two artifact kinds:

```text
signal = feedback / idea / observation, deduped and frequency-counted
doc = analysis / decision / durable thing learned
```

Domains are not storage owners. A domain is a loop state:

```text
domains/<x>/README.md:
  charter
  cadence
  current focus
  backlog
  evidence links
  optional metrics
  Timeline
```

This is useful because it resists the common failure mode:

```text
every new workstream creates its own folder tree
-> cross-cutting artifacts duplicate
-> retrieval and review fragment
```

VAKS should not literally shrink to `signal/doc`, but it should borrow the deferral discipline:

```text
do not add a new artifact kind
unless it has:
1. its own status machine
2. queryable frontmatter fields
3. a distinct body shape
```

### Candidate Point 3: Timeline + LOG.md Is Operational Memory, Not Truth

The repo has two log surfaces:

```text
per-artifact ## Timeline
root LOG.md
```

This is elegant for long-running agent work because it gives:

```text
what is true now = body
what happened = Timeline
what shipped / ingested = LOG.md
git diff = mechanical history
```

VAKS should borrow this as operational trace design, not as authority:

```text
Timeline proves a statement was recorded
LOG proves a work bulk was logged
neither proves the statement is true
neither grants review or action basis
```

### Candidate Point 4: Codebase Harness Is The Real Agent Productivity Layer

The most practical part of the repo is the harness skill:

```text
legible
executable
verifiable
```

Meaning:

```text
legible:
  root agent doc is a map, not a manual
  details live in docs/
  golden rules become custom lints with remediation messages

executable:
  one-command dev stack
  logs reachable
  app drivable

verifiable:
  real e2e gate
  video/trace proof
  independent verifier before PR
```

For VAKS/MISA, this is a high-value candidate for engineering lanes:

```text
before asking an agent to repeatedly ship,
make the repo legible, executable, and verifiable.
```

### Candidate Point 5: Verify-Before-PR Separates Feature Proof From Regression Checks

The `/pr` skill's best distinction:

```text
feature proof = fresh verifier sub-agent drives the real app
objective checks = orchestrator runs type/lint/unit/e2e
PR only after proof
```

This avoids a common false finish:

```text
green tests
but the requested feature was never actually exercised
```

VAKS can borrow the split:

```text
subjective/intent fit -> independent verifier
objective regression -> codified checks
final action -> only after both are represented
```

But this remains operational verification. It is not a knowledge review verdict.

## Comparison With Agent-Loop-Skills

| Dimension | Agent-Loop-Skills | loop-engineer-template | VAKS borrowing verdict |
|---|---|---|---|
| Primary shape | Skill library of loop patterns | Starter repo and Claude Code harness | Use both, but for different layers |
| Core abstraction | Program + artifact + signal + ledger + stop | Shared memory + domain loop state + codebase harness | Complementary |
| Best for | Designing reusable bounded loop behaviors | Bootstrapping long-lived loop engineer workspaces | Strong support |
| Strongest VAKS borrow | Verification-gated keep/revert, loop ledgers | Minimal substrate, Timeline/LOG, legible/executable/verifiable harness | P1 support |
| Main risk | Metrics/judges/ledgers mistaken for truth | Minimal signal/doc model mistaken for VAKS authority model | Keep boundaries visible |

说人话：

```text
Agent-Loop-Skills 告诉你 loop 怎么跑。
loop-engineer-template 告诉你 loop 住在哪、怎么记账、怎么把代码库改成 agent 能长期工作的场。
```

## Candidate Borrow Shape For VAKS

```yaml
loop_workspace:
  knowledge_status: candidate
  source_ref: raw/repos/2026-06-23-AI-Builder-Club-loop-engineer-template-source.md
  substrate:
    - loop_state_readme
    - per_artifact_timeline
    - global_log
    - deterministic_metrics_collectors
  harness:
    - map_not_manual
    - custom_lints_with_remediation
    - dev_local_launcher
    - e2e_gate
    - independent_verifier_before_ship
  boundary:
    action_basis_allowed: false
    truth_mutation_allowed: false
```

## Avoid

Do not borrow:

```text
signal/doc as replacement for VAKS layers
domain README as reviewed state
LOG.md as truth ledger
e2e proof as action basis
Claude Code workflow semantics as Codex defaults
marketing/course claims as technical evidence
```

## Not Promoted

This note does not promote the source to reviewed knowledge, evidence support, a VAKS decision, or action basis.

