---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "AI 学习日课：窄入口、人工 Review、少量沉淀"
created_at: "2026-06-08"
created_by: Codex
processing_tier: medium
knowledge_status: candidate
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
derived_from:
  - raw/articles/2026-06-08-xhs-codex-obsidian-ai-daily-course-source.md
  - raw/articles/2026-06-08-xhs-codex-obsidian-ai-daily-course-source/image-index.md
projects:
  - verified-action-knowledge-system
topics:
  - source-intake
  - ai-learning
  - human-review
  - daily-ritual
  - knowledge-base-ux
borrow_value: medium
borrow_order: P2
evidence_strength: medium_for_workflow_framing_low_for_architecture
tags:
  - candidate-only
  - source-distillation
  - xiaohongshu
  - design-only
provisional: true
---

# 候选蒸馏：AI 学习日课

## 一句话

这条图文可以蒸馏，但对 VAKS 是 `P2 / medium`：它不是新架构，不改变 VAKS 的 raw / candidate / reviewed / action-basis 边界；它适合作为“日常信息入口怎么跑得住”的 UX 和流程借鉴。

## 我们 VAKS 已经有的部分

VAKS 已经有这条图文最核心的边界：

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

本地 `SOURCE_INTAKE.md` 也已经把材料分成 light / medium / heavy，并要求候选材料不能直接变成 truth 或 action basis。

所以这条不是“补架构洞”，而是把已有架构翻译成更容易执行的日课：

```text
固定信息源
-> AI 压缩成少量摘要
-> 人工 Review
-> 只沉淀能改变判断的少数内容
-> 每条都写自己的判断
```

## Candidate Points

### 1. 入口宽度比自动化能力更重要

AI 信息系统的第一风险不是“漏掉内容”，而是入口过宽导致噪音暴涨。对 VAKS 来说，这支持一个产品层做法：默认不做全网扫荡，而是让用户维护少量可信信息源、项目源、作者源或 repo 源。

### 2. AI 摘要只能作为 Review 入口

图文的关键点是：AI 可以订阅、翻译、压缩、补上下文，但摘要不能自动进入长期知识库。进入长期知识库之前，人要回到原文，看上下文、争议、反例和可转化动作。

这和 VAKS 的候选层一致：AI summary 是 candidate comprehension，不是 reviewed knowledge。

### 3. 人工 Review 要问“能否改变判断”

普通收藏看的是“这条有没有意思”；VAKS 可以借鉴的是把 Review 问题改成判断导向：

```text
这条真正讲的是什么？
周围争议是什么？
有没有反例？
放到当前项目语境里，能不能变成行动、选题或风险提示？
```

### 4. 知识库沉淀要有每日上限

这条图文最适合 VAKS 借鉴的 UX 是“少量沉淀”：每天最多保留少数条，避免资料库变成垃圾信息仓库。VAKS 可以在未来 intake UI 或 dashboard 里加入每日候选上限、review due 上限或“今日只留 1-2 条”的节奏提示。

### 5. 每条笔记必须带个人判断

可借鉴的最小字段不是复杂 schema，而是四个朴素字段：

```text
原始链接
我理解了什么
我不同意什么
它能变成什么行动或选题
```

这可以映射到 VAKS 的 source anchor、candidate point、challenge / scope note、routing hint。

## Borrow Gradient

```yaml
borrow_value: medium
borrow_order: P2
dev_context_hint:
  default_layer: support
  core_only_when: "future task is specifically about source-intake UX or daily review workflow"
  support_when: "designing VAKS dashboard, inbox, review queue, source subscription, or daily brief"
  risk_when: "system starts drifting toward all-automatic news collection or summary dumping"
  cold_references:
    - raw/articles/2026-06-08-xhs-codex-obsidian-ai-daily-course-source.md
    - raw/articles/2026-06-08-xhs-codex-obsidian-ai-daily-course-source/image-index.md
```

## 对 VAKS 的具体借鉴

| VAKS 区域 | 可借鉴点 | 不要越界 |
|---|---|---|
| Capture | 源白名单、每日摘要数量上限、固定时间 intake | 不做默认全网扫荡 |
| Understand | AI 做摘要、翻译、上下文补全 | 摘要不能直接入 reviewed knowledge |
| Review | 人工问题清单：原文、争议、反例、行动转化 | 人工 Review 也不能跳过证据支持 |
| Connect | 把少量高价值条目连到项目、选题、行动 | 不能自动生成 reviewed relation |
| Act and Learn | 每条沉淀写行动或选题 | 行动 basis 仍需后续 evidence gate |

## 不要借鉴

- 不要复制作者的信息源名单作为 VAKS 默认源。
- 不要把个人日课节奏硬套到所有项目场景。
- 不要把“AI 自动订阅”做成无边界新闻爬虫。
- 不要让摘要自动入库、自动 promotion、自动创建 reviewed relation。
- 不要把这条个人经验当成 evidence-aware review 的替代品。

## 和当前 VAKS 的关系

```text
fusion_decision: adapt
direct_use: no
architecture_change: no
workflow_ux_value: medium
current_branch_value: medium
whole_architecture_value: low_to_medium
implementation_cost: low
reversibility: high
action_readiness: not_ready
```

## Review Question

如果后面要推进成 VAKS 功能，最值得问的是：

```text
VAKS 的 inbox / daily brief 是否应该默认有“每日少量候选 + 人工 Review + 个人判断字段”的轻量入口？
```

这可以进入未来 source-intake UX 或 dashboard 设计，但现在只保留候选蒸馏。
