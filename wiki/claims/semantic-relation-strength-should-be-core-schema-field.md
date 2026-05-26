---
type: claim
status: accepted
created: 2026-05-26
claim: semantic relation strength should become a core schema field for the verified knowledge graph.
topics:
  - relation-model
  - verified-knowledge-graph
related_projects:
  - verified-vault
sources:
  - [[semantic-relation-edge-schema]]
supporting_sources:
  - [[four-signal-graph-relevance]]
  - [[hybrid-vector-bm25-rrf-with-graph-neighborhood]]
  - [[epistemology-takes-facts-layer]]
conflicting_sources: []
evidence_level: primary
verification_status: cross-checked
confidence: high
impact: 5
relations:
  - target: "[[semantic-relation-edge-schema]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[four-signal-graph-relevance]]"
    rationale: "Four-signal scoring needs explicit semantic edges to rank graph context safely."
    created: 2026-05-26
    last_verified: 2026-05-26
tags:
  - claim
  - schema
  - relation-strength
---

# Claim: Semantic Relation Strength Should Be Core Schema Field

## 主张

`relations` 应成为 `SCHEMA.md v0.1` 的核心字段之一。每条关系边应至少记录 `target`、`type`、`strength`、`confidence`、`evidence` 和 `rationale`。

## 为什么重要

没有关系强度时，资料库只能知道“两个节点有关”。有了关系边 schema，系统才能知道：

- 哪些 claim 强支持某个 pattern。
- 哪些 anti-pattern 是某个 decision 的核心风险。
- 哪些 source 只是背景资料。
- 哪些关系应该优先进入 context pack。

## 当前结论

接受为核心 schema 候选。

暂时只做 Markdown/YAML 字段，不做图数据库。

