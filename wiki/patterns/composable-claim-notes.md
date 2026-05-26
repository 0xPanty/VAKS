---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - "[[2026-01-thinking-os-with-ai-vault-source]]"
related_concepts:
  - "[[second-brain-knowledge-graph]]"
  - "[[source-verification-and-trust-model]]"
related_projects:
  - 资料库
adoption_status: candidate
tags:
  - pattern/note-design
  - pattern/knowledge-graph
evidence_count: 2
confidence: medium
negative_evidence:
replaces:
superseded_by:
extension_points:
---

# 设计模式：Composable Claim Notes

## 一句话定义

把重要笔记写成可独立理解、可被链接复用的“主张型节点”，标题尽量表达一个判断，而不是泛泛的主题。

## 解决的问题

泛主题笔记容易变成杂货箱；从链接跳进去时需要大量上下文。主张型标题可以直接嵌入句子，链接本身成为推理路径的一部分。

## 适用场景

- 概念节点。
- 设计模式。
- 决策依据。
- 反模式和避坑。
- AI 需要沿链接理解推理关系的 vault。

## 不适用场景

- 原始资料存档。
- 长篇文献摘要。
- 需要保留完整上下文的会议记录或播客转录。

## 反例与避坑

- 失败条件：为了 claim 化而把标题写得太长或太绝对。
- 相似反模式：所有笔记都叫“关于 X 的想法”。
- 复杂度风险：过度原子化导致碎片太多。
- 替代方案：source/summary 保留长文，concept/pattern/claim 使用主张型节点。

## 来源证据

- 本文建议标题从 topic 转成 claim，例如从“thoughts on ai slop”到“quality is the hard part”。
- Zettelkasten 实践也强调笔记应 atomic、self-contained、include sources and links。

## 标签与量化

- domain: note-design
- problem: composability
- maturity: proven
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 4
- reversibility: 4

## 交叉验证

- 相似来源：Zettelkasten atomic notes、本文 claim-style titles。
- 历史项目影子：用户需要跨项目复用关键判断，而不是找一堆长聊天。
- 支持证据：当前已建立 `wiki/claims/`。
- 反例：并非所有文件都应 claim 化，raw/source 不适合。

## 最小实现方式

重要结论写入 `wiki/claims/`，标题使用短判断句，例如：

```text
vault-index-guides-context-loading.md
each-vault-needs-purpose-specific-philosophy.md
```

## 项目融合建议

采用，用于 claims、patterns、anti-patterns，不强制 raw。

## 可拓展性

- 可以通过什么接口/适配层接入：Obsidian links、Bases、LLM link suggestion。
- 未来可能被什么替代：更严格 ontology 或 graph schema。
- 替换或升级成本：中。
- 回退方式：保留标题别名和 redirects。

## 验证指标

- 链接能否自然嵌入句子。
- 从任意链接进入是否能独立理解。
- 是否增加有效入链/出链。

