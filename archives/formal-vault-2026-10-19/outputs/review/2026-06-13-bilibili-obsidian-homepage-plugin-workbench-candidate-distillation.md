---
type: review_output
record_kind: video_candidate_distillation
status: candidate_only
created_at: 2026-06-13
created_by: Codex
source_title: 我的 Obsidian 首页搭建：5 个模块 + 动态显示
source_record: raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source.md
source_url: https://www.bilibili.com/video/BV1btEi6vEtz/
author: jz21a
platform: bilibili
transcript_method: local_asr
asr_engine: openai-whisper
asr_model: small
processing_tier: heavy
knowledge_status: candidate
overlay_state: candidate_only
review_pressure: review_due
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: normal
borrow_value: strong
borrow_order: P2_candidate_for_workbench_ui
fit_layers:
  - Capture
  - Activation
  - Dev Context
  - Context Pack
  - Use Ledger / Feedback
  - UI / Workbench
blocked_layers:
  - Reviewed Knowledge
  - Reviewed Relation
  - Action Basis
tags:
  - vaks-distill-candidate
  - obsidian-homepage
  - plugin-composition
  - workbench-homepage
  - quick-action-capture
  - dynamic-queue-view
  - template-launcher
  - activity-heatmap
  - dashboard-not-truth
---

# Obsidian Homepage 插件组合强蒸馏

## 说人话结论

你说“好像都是插件部分”，对，这条主要就是插件组合。但它不是那种“插件越多越好”的资料；它真正可借鉴的是怎么把一堆零散功能收成一个低摩擦首页。

作者的首页是一个普通 Markdown 文件，加 5 个插件和一段 CSS，做成 5 个模块：

- 快捷操作：今日笔记、周总结、task、project、导入书籍/电影、快速记录。
- 分场景导航：阅读、项目、常用页面。
- 动态任务和笔记：最近新建、近期任务、项目总览、任务总览。
- 常用模板：把需要经常优化的模板放到首页。
- 热力图：文件数量热力图 + 字数热力图，看持续输出。

对 VAKS 来说，这不是核心架构，不是 reviewed knowledge；它更像一个 `VAKS Workbench Homepage` 的候选 UI 参考。我们可以借“入口聚合、低摩擦 capture、动态队列、模板入口、活动指标”，但不能借“dashboard 等于知识质量”。

## VAKS 有没有类似思路？

有一部分，但偏后端/文档，不像这个视频这么工作台化。

VAKS 现有类似逻辑：

- `DEV_CONTEXT`：当前任务的工作记忆包。
- `REVIEW_QUEUE`：候选点、冲突、缺证据、review_due 的队列。
- `SOURCE_INTAKE`：source intake 的 light / medium / heavy 流程。
- `Use Ledger / Feedback`：记录使用反馈和后续复查压力。
- `Activation Tier`：哪些资料当前应该 hot/warm/cold。

这条视频补的是入口层：

- 一打开就知道今天该从哪里开始。
- 常用动作不用翻目录。
- 最近任务/笔记/项目自动浮出来。
- 常用模板可以随手优化。
- 活跃度指标提醒自己有没有持续输出。

所以它和 VAKS 对应的是 `UI / Workbench / Dev Context landing page`，不是 truth core。

## Source Anchors

- `raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source/segments.md` 00:06-00:41：页面散在各处，找文件会打断快速记录；核心是减少记录摩擦。
- `raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source/segments.md` 00:46-01:20：快捷操作区打开/新建今日笔记、本周总结、task、project、导入书籍/电影、快速记录。
- `raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source/segments.md` 01:36-01:56：作者曾用 Dataview 动态显示项目，但打开慢，改为静态页面。
- `raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source/segments.md` 02:24-02:36：常用模板也放进首页，因为模板需要经常点进去优化。
- `raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source/segments.md` 02:37-03:14：文件数量热力图和字数热力图结合，看持续输出。
- `raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source/segments.md` 03:14-04:41：插件栈是 Homepage、Dataview、Templater、Contribution Graph、Obsidian Echarts、MCL Multi Column CSS。
- `raw/videos/2026-06-13-bilibili-bv1btei6vetz-obsidian-homepage-source/segments.md` 05:05-05:20：首页是普通 Markdown + 插件 + CSS，不依赖第三方主题私有接口。

## 最值得借鉴的点

### 1. Workbench Homepage, Not Knowledge Layer

首页是操作入口，不是知识本体。这个边界很适合 VAKS：

```text
homepage = launch surface + queue view + status view
not = truth store / review engine / action basis
```

VAKS 如果做首页，应该显示入口和队列，不直接创建 truth。

### 2. Quick Action Capture

作者把高频动作放在第一屏：今日笔记、周总结、task、project、导入书籍、导入电影、快速记录。它解决的是“还没找到入口，灵感已经没了”。

VAKS 可借成：

```text
quick actions:
  - quick source card
  - quick candidate note
  - quick review_due
  - quick project context
  - quick feedback event
  - quick video/repo/article intake
```

这些按钮只是开入口，不自动 promotion。

### 3. Dynamic Queue View With Static Fallback

视频里最务实的一点：作者发现动态项目列表打开慢，就从 Dataview 改成静态页面。这个对 VAKS 很重要。

可借规则：

```text
dynamic where useful
static where speed matters
cache where repeated
manual override when query is slow/noisy
```

VAKS 的 review queue、recent work、active project 可以动态显示，但首页不能因为查询太重而拖慢启动。

### 4. Templates As First-Class Workflow Assets

作者把常用模板放到首页，因为模板需要经常优化。VAKS 也一样：source card、candidate distillation、review packet、context pack、feedback event 这些模板不该埋在目录里。

首页可以有一个 `Templates / Start Here` 区：

```text
source template
candidate distill template
review queue item
evidence packet
context pack manifest
feedback event
```

### 5. Activity Heatmap As Motivation, Not Truth

文件数量和字数热力图能提醒“有没有持续输出”。但它只能是活动指标。

VAKS 边界：

```text
activity heatmap -> use/output signal
not -> source quality
not -> truth confidence
not -> review readiness
not -> action basis
```

## Candidate Points

### CP1 - VAKS 可以有 Workbench Homepage

VAKS 的日常使用可以有一个首页，把 capture、review queue、dev context、recent outputs、templates、health hints 聚合起来。

```yaml
candidate_status: review_due
fit: high
layer: UI / Workbench
schema_change_now: no
```

### CP2 - 快捷入口降低 capture 摩擦

很多 capture 失败不是因为流程不会，而是入口太远。首页按钮可以显著降低记录摩擦。

```yaml
candidate_status: review_due
fit: high
layer: Capture
boundary: launch_only_no_auto_promotion
```

### CP3 - 动态队列适合显示 review pressure

Dataview 类动态查询可以显示 review_due、missing_evidence、recent candidate、active project，但必须保留静态 fallback。

```yaml
candidate_status: review_due
fit: medium_high
layer: Review Queue / Activation
risk: slow_dashboard
```

### CP4 - 模板入口是工作流维护入口

模板不是杂物，是 VAKS 的操作协议。首页可暴露常用模板和维护入口。

```yaml
candidate_status: review_due
fit: high
layer: Workflow / Templates
```

### CP5 - 活跃度热力图只能做 Use Ledger 辅助

热力图可以帮助用户看持续输出，但不能用于判断知识可靠性。

```yaml
candidate_status: review_due
fit: medium
layer: Use Ledger / Feedback
hard_boundary: dashboard_not_truth
```

## Suggested Labels For VAKS

```yaml
architecture_tags:
  - workbench-homepage
  - quick-action-capture
  - dynamic-queue-view
  - static-fallback-for-speed
  - template-launcher
  - active-project-dashboard
  - review-queue-dashboard
  - recent-work-surface
  - activity-heatmap-not-truth
  - ordinary-markdown-plus-plugins
  - theme-independent-ui

vaks_layers:
  - Capture
  - Activation
  - Dev Context
  - Context Pack
  - Review Queue
  - Use Ledger / Feedback
  - UI / Workbench

risk_tags:
  - dashboard-not-truth
  - plugin-dependency-risk
  - slow-dataview-query
  - pretty-dashboard-bloat
  - metric-overinterpretation
```

## Adoption Judgment

```yaml
borrow_value: strong
borrow_order: P2_candidate_for_workbench_ui
adoption_now: candidate_only
schema_change_now: no
recommended_shape:
  - optional VAKS Workbench Homepage
  - quick action area
  - active project / dev context area
  - review queue / review_due area
  - recent source/candidate outputs
  - template launcher
  - vault activity / health hints
must_not_do:
  - do not make homepage a truth authority
  - do not let heatmaps imply quality
  - do not require plugin stack for core VAKS correctness
  - do not slow down ordinary capture/query
```

## Minimal Absorption Suggestion

先不改主架构。未来可以在 sandbox 里做一个候选首页：

```text
VAKS Workbench Homepage
  1. Quick Capture
     - article / repo / video / paper / quick note
  2. Active Project
     - current dev context
     - core/support/risk/cold references
  3. Review Queue
     - review_due
     - missing_evidence
     - synthesis_needed
  4. Recent Outputs
     - latest source cards
     - latest candidate distillations
  5. Templates
     - source card
     - candidate distillation
     - evidence packet
     - feedback event
  6. Activity / Health
     - recent capture count
     - review queue count
     - stale/review_due hints
```

注意，这个首页只是 `view / workbench`，不是 schema、truth core、review engine 或 action basis。

## Boundary Statement

本文件是候选蒸馏，不是 reviewed knowledge。它可以用于后续讨论 VAKS 首页/工作台/插件组合方案，但不能作为正式架构变更、truth 判断、插件采纳决策或 action basis。
