---
type: qa
status: captured
asked_at: 2026-05-26
question: "资料库是否也应该像设计点一样打标签、验证来源、标记已验证/未验证，避免变成垃圾信息堆？"
related:
  - "[[source-verification-and-trust-model]]"
  - "[[evidence-backed-design-validation]]"
  - "[[second-brain-knowledge-graph]]"
sources_checked:
  - "Obsidian Properties/Bases official docs"
  - "Zettelkasten literature/permanent note practices"
  - "Knowledge graph provenance and claim verification papers"
---

# 资料来源验证与可信度治理

## TL;DR

是。资料库也必须有可信度治理。不能只收集资料，还要记录来源、验证状态、证据等级、置信度、时效性和复查计划。

## 用户判断

用户认为：自己的第二大脑不能是一堆未经验证的垃圾信息。资料库需要像工程系统一样，区分已验证、未验证、来源、消息质量、证据强度，并用标签和量化方式管理。

这个判断合理，而且应该作为资料库底层规则。

## 关键设计

把 `Source` 和 `Claim` 分开：

```text
Source = 一篇文章、论文、仓库、播客、推文、官方文档
Claim  = 从来源里提取出来的某条具体主张或结论
```

原因：

- 一个来源可信，不代表每句话都可信。
- 一个来源一般，也可能有值得追踪的线索。
- 决策真正依赖的是具体主张，而不是来源整体印象。

## 状态字段

资料和主张都需要记录：

- `source_status`
- `evidence_level`
- `verification_status`
- `confidence`
- `source_quality`
- `freshness`
- `relevance`
- `cross_source_count`
- `last_verified`
- `next_review`

## 状态示例

- `unverified`：未验证，只是收录。
- `single-source`：只有一个来源。
- `cross-checked`：多个独立来源支持。
- `primary-source`：官方、源码、论文、原始数据。
- `field-tested`：已在项目或实验中验证。
- `conflicted`：有冲突证据。
- `deprecated`：可能过时。
- `rejected`：确认不可信或不采用。

## 原则

资料可以先进入未验证状态，但重要结论进入设计、决策或生产流程前，必须完成基本验证。

第二大脑不是记得越多越好，而是记得更干净、更可追溯、更可复查。

