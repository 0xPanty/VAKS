---
type: pattern
status: draft
created: 2026-05-26
source_libraries:
  - garrytan/gbrain
related_concepts:
  - source-verification-and-trust-model
  - evidence-backed-design-validation
related_projects:
  - verified-knowledge-system
adoption_status: adapt
tags:
  - epistemology
  - facts
  - claims
  - takes
evidence_count: 1
confidence: high
negative_evidence:
replaces:
superseded_by:
extension_points:
  - SCHEMA.md
  - claim-record
  - review-gate
---

# 设计模式：Epistemology layer with facts / takes

## 一句话定义

不要只记录“文本相似”，要记录“谁相信什么、什么时候说、证据是什么、置信度多高、这是事实还是观点/预测/猜测”。

## 解决的问题

普通 RAG 会把事实、观点、猜测、宣传语、反例混在同一个召回结果里。verified knowledge system 需要区分知识状态。

## 适用场景

- 多来源资料互相冲突。
- 需要决定是否采用某个架构设计。
- 资料中既有事实，也有作者观点、经验判断和预测。

## 不适用场景

- 纯全文检索。
- 完全不做采纳决策的普通阅读库。

## 反例与避坑

- 失败条件：LLM 把“某作者认为”误提升成系统事实。
- 相似反模式：只用 confidence，不记录 holder/source。
- 复杂度风险：过早建立复杂事实数据库。
- 替代方案：先在 Markdown frontmatter 和正文中手工字段化。

## 来源证据

- gbrain `docs/takes-vs-facts.md` 区分 hot facts 和 cold takes。
- gbrain `src/core/facts/extract.ts` 为 fact 抽取 kind、entity、confidence、notability、metric/value/unit/period。
- gbrain `src/core/cycle/phases/consolidate.ts` 将多条事实聚类后沉淀为 take，并保留 contributing facts。
- gbrain `src/core/schema-pack/base/gbrain-base.yaml` 的 takes kinds 包含 `fact / take / bet / hunch`。

## 标签与量化

- domain: verified-knowledge
- problem: epistemic-status
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 5
- evidence_strength: 4
- reversibility: 4

## 交叉验证

- 相似来源：claim verification / provenance / confidence 模型。
- 用户历史项目影子：用户要求 pattern/claim/anti-pattern、量化标签、交叉验证、风险记录。
- 支持证据：当前资料库已区分 source、claim、pattern、anti-pattern、decision。
- 反例：把 Grok、README、Reddit 说法直接写成决策事实会污染系统。

## 最小实现方式

在 `claim-record` 和 `design-pattern` 中明确：

```text
claim_kind: fact / take / hypothesis / bet / anti-pattern / decision
holder: author / repo / user / system / community
confidence: 1-5
evidence_level: primary / secondary / anecdotal / synthetic
verification_status: unverified / single-source / cross-checked / field-tested / conflicted / rejected
valid_from:
valid_until:
```

## 项目融合建议

立即进入 schema 设计。暂时不做自动事实抽取数据库。

## 验证指标

- 每条重要 claim 都能回答：谁说的、何时、证据是什么、我们是否采纳。
- 每个 decision 只引用已验证或明确标注 single-source 的 claim。
- opinion / hypothesis 不会被误当 fact。

