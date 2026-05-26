---
type: pattern
status: draft
created: 2026-05-26
source_libraries:
  - garrytan/gbrain
related_concepts:
  - compiled-truth
  - evidence-backed-design-validation
related_projects:
  - verified-knowledge-system
adoption_status: adapt
tags:
  - compiled-truth
  - timeline
  - evidence
evidence_count: 1
confidence: high
negative_evidence:
replaces:
superseded_by:
extension_points:
  - claim-record
  - decision-record
  - health-check
---

# 设计模式：Compiled truth + append-only timeline

## 一句话定义

把“当前最可信结论”和“历史证据流水”分开：结论可以被重写，证据 timeline 只能追加或标记状态。

## 解决的问题

一个知识库会不断吸收新资料。如果只追加笔记，用户每次都要自己综合；如果只改最终结论，又会丢失证据和判断过程。

## 适用场景

- claim、pattern、decision 需要持续更新。
- 资料之间可能互相支持或冲突。
- 需要知道“现在采用什么”和“为什么当时这么判断”。

## 不适用场景

- 临时草稿、一次性资料摘要。
- 完全没有复查价值的低重要性记录。

## 反例与避坑

- 失败条件：compiled truth 写得像最终真理，没有 evidence timeline。
- 相似反模式：只保留聊天结论，不保留原始来源。
- 复杂度风险：timeline 字段太细导致维护成本过高。
- 替代方案：早期用简单 `Evidence Log` 小节，不先做数据库表。

## 来源证据

- gbrain `docs/guides/compiled-truth.md` 把页面顶部 current synthesis 和 timeline evidence trail 分离。
- gbrain synthesize phase 会提示子 agent 看到旧 contradictions 时应更新 compiled truth 或标记历史冲突。

## 标签与量化

- domain: knowledge-verification
- problem: evolving-truth
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：Zettelkasten 文献笔记 -> 永久笔记；决策记录 ADR 的 superseded / amended 状态。
- 支持证据：当前项目已需要 source / claim / decision 分层。
- 反例：没有 timeline 时，后续很难复查“哪个库影响了这个设计”。

## 最小实现方式

在 `claim-record`、`design-pattern`、`decision-record` 模板中增加：

```text
## Current Synthesis
当前结论、置信度、适用边界。

## Evidence Timeline
- 日期 / 来源 / 证据类型 / 支持或反驳 / 影响。
```

## 项目融合建议

立即进入 `SCHEMA.md`。这会让我们后续融合多个库时不乱。

## 验证指标

- 每个 adopted decision 至少有一条 evidence timeline。
- 被更新的结论保留旧证据和变化原因。
- 冲突资料进入后可以标记 `conflicted` 而不是覆盖。

