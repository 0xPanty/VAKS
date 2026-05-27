---
type: anti-pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
domain: knowledge-system-architecture
failure_mode: "Using PARA folders as the verified truth layer"
severity: 4
likelihood: 3
complexity_cost: 3
cross_validated_with:
  - "[[generic-concept-schema-as-truth-layer]]"
  - "[[direct-compile-to-truth-layer-without-review]]"
related_projects:
  - verified-action-knowledge-system
replacement:
  - "[[MEMORY_TIER]]"
  - "[[DEV_CONTEXT]]"
  - "[[actionability-based-memory-routing]]"
verification_status: single-source
evidence_level: secondary
confidence: medium
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Needs comparison against more PARA implementations and AI agent vault systems."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-obsidian-para-source]]"
    observation: "PARA organizes by actionability categories but does not define evidence, confidence, review status, or source provenance."
    effect: supports
    confidence: medium
relations:
  - target: "[[SCHEMA]]"
    type: risk_of
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-obsidian-para-source]]"
    rationale: "Replacing raw/wiki/outputs/products with PARA folders would collapse storage layout and verified truth schema."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[MEMORY_TIER]]"
    type: risk_of
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-obsidian-para-source]]"
    rationale: "Folder categories can be useful activation hints, but they must not own truth or confidence."
    created: 2026-05-27
    last_verified: 2026-05-27
decision: avoid
tags:
  - anti-pattern
  - para
  - truth-layer
  - folder-taxonomy
---

# 反模式 / 踩坑：PARA Folder Taxonomy As Truth Layer

## AI-readable preamble

PARA is useful as an actionability and lifecycle routing model.

It becomes dangerous if adopted as the verified truth layer.

Use it to inform activation metadata and dev context packs, not to replace schema, provenance, review, or relations.

## 问题描述

把 PARA 的四个文件夹：

```text
Projects
Areas
Resources
Archive
```

直接当成本资料库的主架构，会把两个问题混在一起：

```text
Where should I use this next?
Is this verified enough to become truth or action basis?
```

前者是 activation。

后者是 verification。

## 为什么不可行

本资料库的核心链路是：

```text
raw source
-> candidate
-> reviewed node
-> verified knowledge graph
-> context pack / decision / action
-> feedback
```

PARA folder taxonomy 没有内置：

```text
source provenance
source ranges
evidence level
truth confidence
negative evidence
review queue
semantic relations
decision rollback
feedback timeline
```

如果直接替代 `raw/`、`wiki/`、`outputs/`、`products/`，会让资料库变成行动文件夹系统，而不是 verified-action knowledge system。

## 失败条件

- 看到 PARA 很清爽，就想重构顶层目录。
- 把 Archive 理解成低质量资料。
- 把 Projects 理解成可信度更高的资料。
- 把文件夹位置当成 context pack 排序依据的第一原则。
- 用手工搬文件替代 query-run / feedback-event / activation_reason。

## 标签与量化

- domain: knowledge-architecture
- failure_mode: folder-taxonomy-overreach
- severity: 4
- likelihood: 3
- complexity_cost: 3
- evidence_strength: 3
- reversibility: 3

## 交叉验证

- 相似失败来源：`[[generic-concept-schema-as-truth-layer]]`
- 历史项目证据：本资料库已经确定 Markdown/YAML truth layer 和 review gate。
- 支持证据：`[[2026-05-27-obsidian-para-source]]`
- 是否可能只是局部失败：是。PARA 作为 activation/lifecycle 层可用；失败点是把它升级为 truth layer。

## 应该避开什么

不要改成：

```text
1. Projects/
2. Areas/
3. Resources/
4. Archive/
```

作为资料库顶层主结构。

不要让：

```text
folder name
```

替代：

```text
verification_status
evidence_level
confidence
relations
review_status
```

## 替代方案

吸收 PARA 的动作规则，但落在现有框架：

```text
memory_tier:
  hot / warm / cold

scope_key:
  project / task / domain

DEV_CONTEXT:
  Core / Support / Risk / Cold References

feedback/query-run:
  actual use creates activation evidence
```

## 后续是否需要复测

需要。

下一步应拿一个真实项目跑：

```text
old cold source
-> dev context cold reference
-> support/core reactivation
-> project exit scan
-> warm writeback or cold return
```
