---
type: anti-pattern
status: active
created: 2026-05-27
updated: 2026-05-27
tags:
  - anti-pattern/schema
  - anti-pattern/truth-layer
  - verified-knowledge-system
sources:
  - "[[2026-05-26-llm-wiki-compiler-source]]"
  - "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
verification_status: cross-checked
evidence_level: synthetic
confidence: high
last_verified: 2026-05-27
next_review: 2026-06-03
domain: verified-knowledge-system
failure_mode: "Using generic wiki page kinds as the formal truth schema."
severity: 5
likelihood: 4
complexity_cost: 4
cross_validated_with:
  - "[[direct-compile-to-truth-layer-without-review]]"
related_projects:
  - verified-knowledge-system
replacement: "[[SCHEMA]]"
decision: avoid
relations:
  - target: "[[SCHEMA]]"
    type: contradicts
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
    rationale: "Generic concept/entity/comparison/overview page kinds cannot express verified claim, pattern, anti-pattern, decision, and actionability flow."
    created: 2026-05-27
    last_verified: 2026-05-27
---

# 反模式 / 踩坑：Generic Concept Schema As Truth Layer

## 问题描述

把 `concept/entity/comparison/overview` 这类普通 wiki page kind 直接当成可信知识系统的核心 schema。

## 为什么不可行

这种 schema 适合浏览和整理，但不适合判断：

- claim 是否被证据支持。
- pattern 是否值得采纳。
- anti-pattern 是否要避开。
- decision 是否可行动。
- action 是否有风险、前提和回退。

## 失败条件

- 所有内容都变成 concept page。
- 反例、风险、回退和 actionability 被塞进正文而不是结构字段。
- Agent 只能按相似度读“相关概念”，不知道哪些能行动。
- query/save 生成的答案直接进入 formal wiki。

## 替代方案

保留 generic page kind 作为普通 wiki/view 层，但 truth layer 必须使用：

```text
source
summary
claim
pattern
anti-pattern
decision
qa
implementation-note
```

## 后续是否需要复测

需要。等我们设计 node schema packs 时，可以允许 domain-specific page kind，但不能削弱 core node flow。
