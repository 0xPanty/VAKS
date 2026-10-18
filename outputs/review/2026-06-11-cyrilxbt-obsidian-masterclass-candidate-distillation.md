---
record_kind: candidate_distillation
status: candidate
title: "CyrilXBT Obsidian Masterclass：从空 Vault 到 AI 第二大脑的使用面借鉴"
created_at: "2026-06-11 04:02:34 +08:00"
created_by: Codex
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/articles/2026-06-11-cyrilxbt-obsidian-masterclass-source.md
  - raw/articles/2026-06-11-cyrilxbt-obsidian-masterclass-source/pasted-text.txt
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
  - obsidian-user-surface
  - daily-intake
  - claude-md-operating-manual
  - visible-ai-compound-output
  - vault-maintenance-lint
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - snapshot_ref: raw/articles/2026-06-11-cyrilxbt-obsidian-masterclass-source/pasted-text.txt
    selector_type: section_heading
    selector_value: "Part 2: The Philosophy Before the Architecture"
  - snapshot_ref: raw/articles/2026-06-11-cyrilxbt-obsidian-masterclass-source/pasted-text.txt
    selector_type: section_heading
    selector_value: "Part 6: The CLAUDE.md"
  - snapshot_ref: raw/articles/2026-06-11-cyrilxbt-obsidian-masterclass-source/pasted-text.txt
    selector_type: section_heading
    selector_value: "Part 8: The Daily Note System"
  - snapshot_ref: raw/articles/2026-06-11-cyrilxbt-obsidian-masterclass-source/pasted-text.txt
    selector_type: section_heading
    selector_value: "Part 11: The Intelligence Layer"
  - snapshot_ref: raw/articles/2026-06-11-cyrilxbt-obsidian-masterclass-source/pasted-text.txt
    selector_type: section_heading
    selector_value: "Part 12: The Six Core Claude Prompts"
  - snapshot_ref: raw/articles/2026-06-11-cyrilxbt-obsidian-masterclass-source/pasted-text.txt
    selector_type: section_heading
    selector_value: "Part 14: The Three-Month Build Plan"
borrow_value: strong
borrow_order: P1
evidence_strength: high_for_usage_design_low_for_truth
dev_context_hint:
  default_layer: support
  core_only_when: "future task is specifically about VAKS Obsidian user surface, daily intake, root operating manual, or vault audit prompts"
  support_when: "designing Obsidian home, source-intake UX, candidate synthesis folders, maintenance lint, or agent-facing vault instructions"
  risk_when: "system drifts toward automatic truth mutation, broad scheduled automation, or whole-vault AI authority"
  cold_references:
    - raw/articles/2026-06-11-cyrilxbt-obsidian-masterclass-source.md
    - raw/articles/2026-06-11-cyrilxbt-obsidian-masterclass-source/pasted-text.txt
tags:
  - candidate
  - provisional
  - obsidian
  - second-brain
  - ai-vault
  - source-distillation
---

# 候选蒸馏：CyrilXBT Obsidian Masterclass

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 一句话

这篇长文对 VAKS 是 `P1 / strong` 的使用面参考：它把 Obsidian + AI vault 讲成了普通用户能执行的完整操作系统；但它不是证据型来源，不能替代 VAKS 的 source / candidate / reviewed / action-basis 边界。

## 和 VAKS 已有架构的关系

VAKS 已经有主干：

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

这篇文章补的不是新真理，而是“用户怎么每天真的用起来”：

```text
daily note as front door
-> root operating manual
-> explicit retrieval and linking habits
-> visible AI-generated outputs
-> manual query prompts
-> periodic vault audit
-> staged build plan
```

对我们最有价值的是把现有边界翻译成 Obsidian 工作台、首页、模板、提示词和审计面，而不是复制作者的整个 folder taxonomy。

## Candidate Points

### 1. Retrieval-first 比分类-first 更适合长期 vault

候选判断：未来 VAKS 的 Obsidian 使用面应该让用户按“以后怎么找回来、怎么用于回答/决策”来组织入口，而不是只强调当前应该放在哪个文件夹。

可借鉴到：

```text
source intake UI
query mode
MOC / Base views
context-pack preparation
```

边界：检索便利不等于证据支持；命中、链接、图谱、Base 视图都不能生成 truth confidence。

### 2. Root operating manual 是 AI vault 的关键入口

文章里的 `CLAUDE.md` 值得强借鉴，但对 VAKS 应理解为“agent-facing operating manual”，不是让任何 agent 自动拥有写入权。

可借鉴字段：

- vault purpose
- active projects
- active theses
- decision context
- content standards
- navigation map
- synthesis / pattern / connection rules
- update schedule

VAKS 现有 `AGENTS.md`、`DEV_CONTEXT.md`、`SOURCE_INTAKE.md` 已经有类似职责。未来若做 Obsidian 首页或 agent workbench，可以把这些压成一个更友好的 read-first surface。

### 3. Daily note 是 capture front door，但不是 promotion gate

每日笔记作为低摩擦入口很适合借鉴：当天捕获、当天决策、open loops、次日延续都可以自然进一个日常面板。

VAKS 需要补上的边界：

```text
daily capture
-> raw / inbox
-> candidate comprehension
-> review_due when needed
-> later evidence-aware review
```

不要让 evening processor 自动创建 reviewed knowledge、reviewed relation 或 action basis。

### 4. AI-generated compound output 应该可见、可追踪、候选化

文章把 connection notes、pattern reports、monthly syntheses 放成可见文件，这点很适合 VAKS。

更适合 VAKS 的落点：

```text
outputs/review/
outputs/qa/
outputs/feedback/
candidate synthesis folder
```

不适合的落点：

```text
wiki/claims/
wiki/patterns/
wiki/decisions/
```

除非后续 evidence-aware review 通过。

### 5. Manual prompts 可以变成 query modes

文章给出的 connection finder、question answerer、decision support、writing activator、thinking partner、vault audit 都可借鉴为 VAKS 的人工触发模式。

VAKS 版本应保留 authority bucket：

```text
orientation mode: candidate allowed but marked
answer/action mode: reviewed support or independent anchors required
source inspection mode: raw + candidate
project exploration mode: confirmed overlay for active project only
```

### 6. Vault audit 是 maintenance lint，不是自动修复

很值得借鉴的审计问题：

- permanent notes 是否缺连接
- 主题是否需要 MOC
- active theses 是否过期
- 最多连接的 note 暴露了什么真实兴趣
- compound outputs 是否真的产生新综合

VAKS 要保持的边界：审计发现只产生 lint、review pressure、workbench todo 或候选修订；不能自动改 reviewed knowledge。

### 7. 三个月搭建计划提示我们先做 habit，再做 automation

这篇文章的实施节奏比具体 folder 更有价值。VAKS 未来如果做用户侧 Obsidian 套件，应该先跑通：

```text
folder / home / templates
daily capture habit
manual review and permanent-note habit
agent read-only or constrained read
manual prompts
then scheduled automation
```

这比一开始就做自动化编译、全量调度或大 MCP 权限更稳。

## Borrow Gradient

```yaml
borrow_value: strong
borrow_order: P1
P1:
  - root operating manual / CLAUDE.md as agent-facing vault contract
  - daily note as low-friction capture front door
  - visible candidate-only AI compound outputs
  - manual prompts as reusable query modes
  - vault audit as maintenance lint
P2:
  - retrieval-first language for user education
  - maps of content as navigation layer
  - staged three-month rollout as product onboarding
P3:
  - folder taxonomy and filename convention as comparative reference only
avoid:
  - copying the exact 00-10 folder structure into VAKS
  - treating AI summaries or compound outputs as reviewed knowledge
  - starting scheduled automation from this source alone
  - installing plugin stack or connecting Filesystem MCP without permission design
  - treating "Claude reads the whole vault" as safe or action-ready by default
```

## 对 VAKS 的具体借鉴

| VAKS 区域 | 可借鉴点 | 不要越界 |
|---|---|---|
| Capture | Daily note / inbox as front door | 不让 daily processor 直接 promotion |
| Understand | AI summaries and briefs as candidate comprehension | summary 不是 evidence support |
| Review | vault audit prompts and thesis contradiction checks | audit/lint 不等于 review pass |
| Connect | MOC and explicit links improve navigation | links/backlinks 不等于 reviewed relation |
| Act and Learn | decision prompts and output principle | decision support still needs action-facing gates |
| Dev Context | root manual + active projects as context surface | agent context 不等于 write authority |

## Open Questions

- VAKS 是否需要一个 Obsidian HOME，把 `AGENTS.md`、`SOURCE_INTAKE.md`、`DEV_CONTEXT.md` 的日常入口压缩成人能用的导航页？
- `CLAUDE.md` 的 active theses 概念，是否应映射到 VAKS 的 claims / decisions / review_due，而不是另建一套 truth lane？
- Daily note 应该只是个人入口，还是未来也作为 project use ledger 的轻入口？
- AI compound output 文件夹应使用 `outputs/review`，还是未来在 Obsidian vault 内提供一个更友好的 candidate synthesis 区？
- 哪些 audit prompt 能变成 Bases/dashboard，而不变成自动修复？

## Judgment

```yaml
direct_use: no
fork: no
design_only: yes
fusion_decision: adapt
architecture_change: no
workflow_ux_value: strong
current_branch_value: medium
whole_architecture_value: medium
implementation_cost: low_to_medium
reversibility: high
action_readiness: not_ready
```

## Forbidden

```text
project_borrow_scope
project_non_borrow_scope
decision outcome
formal pattern
action basis
truth confidence
```

Project-specific borrowing is recorded separately in the project overlay.
