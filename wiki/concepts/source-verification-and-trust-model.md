---
type: concept
status: active
created: 2026-05-26
aliases:
  - 资料可信度模型
  - 来源验证
  - provenance
  - trust model
related:
  - "[[evidence-backed-design-validation]]"
  - "[[negative-evidence-and-avoidance]]"
  - "[[second-brain-knowledge-graph]]"
---

# 资料来源验证与可信度模型

## 定义

资料库不能只是收集内容，而要记录每条资料和每条结论的来源、验证状态、证据等级、置信度、适用边界和复查时间。

核心目标：

- 避免资料库变成未经验证的信息垃圾堆。
- 让 AI 调用资料时知道哪些是事实、哪些是观点、哪些只是待验证线索。
- 让后续设计采纳可以基于证据，而不是基于“看起来很有道理”。

## 基本原则

来源和主张要分开管理。

```text
Source 资料来源
  = 这篇文章/论文/播客/仓库/推文从哪里来，作者是谁，可信度如何

Claim 主张/结论
  = 这条具体说法是什么，来源有哪些，是否被验证，是否有反例
```

一个来源整体可信，不代表其中每条结论都可信。一个来源整体一般，也可能包含有价值线索。

## 来源状态

建议使用这些状态：

- `unverified`：未验证，只是收录。
- `source-captured`：来源、作者、时间、链接等元数据完整，但内容未验证。
- `single-source`：只有一个来源支持。
- `cross-checked`：至少两个独立来源支持。
- `primary-source`：来自官方文档、论文、源码、原始数据、作者一手说明。
- `field-tested`：已在用户项目、实验或真实工作流中验证过。
- `conflicted`：存在互相冲突的资料或结论。
- `deprecated`：曾经成立，但现在可能过时。
- `rejected`：已确认不采用或不可信。

## 证据等级

建议使用这些等级：

- `primary`：官方文档、源码、论文、原始数据、直接实验。
- `secondary`：高质量解读、技术博客、教程、会议整理。
- `anecdotal`：个人经验、社群讨论、推文、案例分享。
- `synthetic`：AI 总结、二手聚合、模型推断。
- `unknown`：来源不清。

## 量化字段

每条重要资料或主张可以记录：

- `source_quality`：来源质量，1 到 5。
- `evidence_strength`：证据强度，1 到 5。
- `confidence`：当前置信度，1 到 5。
- `freshness`：时效性，1 到 5。
- `relevance`：对用户当前项目/短剧生产的相关度，1 到 5。
- `cross_source_count`：独立来源数量。
- `last_verified`：上次验证日期。
- `next_review`：下次复查日期。

## 验证方式

常见验证方式：

- 查官方文档。
- 查源码或 commit。
- 查论文或原始数据。
- 找两个以上独立来源交叉确认。
- 在本地做最小实验。
- 和用户历史项目经验对照。
- 记录反例、争议和失败边界。

## Obsidian 实现

- 用 Properties 存结构化字段。
- 用 `source_status`、`evidence_level`、`confidence`、`last_verified` 等字段做 Bases 过滤。
- 用 `[[source]]` 和 `[[claim]]` 建关系。
- 用 `wiki/claims/` 存重要主张。
- 用 `raw/` 保留原始资料。
- 用 `wiki/summaries/` 存编译摘要。

## 使用原则

资料进入库时不需要立刻验证完整，但必须允许标记为未验证。

重要结论进入设计、决策或生产流程前，必须至少完成：

- 来源完整。
- 验证状态明确。
- 证据等级明确。
- 风险或反例记录。
- 可复查。

## 关键判断

一个“第二大脑”不应该只是记忆更多，而应该记得更干净。

未经来源标注、未经验证、无法复查的信息，不应该直接进入核心决策。

