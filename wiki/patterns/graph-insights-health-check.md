---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - nashsu/llm_wiki
related_concepts:
  - second-brain-knowledge-graph
  - negative-evidence-and-avoidance
  - evidence-backed-design-validation
related_projects:
  - verified-vault
adoption_status: adapt
tags:
  - health-check
  - knowledge-graph
  - blind-spot
  - lint
evidence_count: 3
confidence: high
negative_evidence:
  - algorithmic-graph-scoring-without-source-quality
replaces:
superseded_by:
extension_points:
  - weekly health report
  - graph metrics dashboard
---

# 设计模式：图谱洞察式健康检查

## 一句话定义

知识库体检不只查“有没有摘要”，还要查图谱结构：孤岛节点、低内聚社区、桥接节点、意外连接。

## 解决的问题

笔记库会腐烂，不只是因为内容没整理，也因为关系结构失真：重要节点没人链接、某个主题内部没有互相解释、关键桥接概念太薄、跨领域连接没被意识到。

## 适用场景

- 已经有几十个以上的概念、模式、来源、主张。
- 想做第二大脑或 Agent context pack。
- 想发现知识盲区，而不是只做收藏整理。

## 不适用场景

- 早期只有少量资料。
- 关系图主要靠 AI 自动乱连。
- 没有 sources/evidence 字段，无法判断结构是否可信。

## 反例与避坑

- 失败条件：把图谱指标当作内容质量本身。
- 相似反模式：追求图很漂亮，而不是结论更可靠。
- 复杂度风险：Louvain、ForceAtlas2、图可视化太早引入。
- 替代方案：先输出 Markdown 健康报告。

## 来源证据

`nashsu/llm_wiki` 的 `graph-insights.ts` 中包含：

- surprising connections：跨社区、跨类型、边缘节点连到 hub、弱但存在的边。
- knowledge gaps：degree <= 1 的孤岛节点。
- sparse communities：cohesion < 0.15 且节点数 >= 3。
- bridge nodes：连接 3 个以上 community 的节点。

## 标签与量化

- domain: knowledge_base_health
- problem: knowledge_decay
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 4
- evidence_strength: 5
- reversibility: 5

## 交叉验证

- 相似来源：Karpathy 的 lint / health check。
- 历史项目影子：用户要求记录不可行、踩坑、待验证资料，避免资料库变垃圾。
- 支持证据：`llm_wiki` 已有实现代码。
- 反例：指标只能提示，不等于自动修复。

## 最小实现方式

在每周 `outputs/health/` 加四个段落：

- 孤岛节点：入链出链都少于 2。
- 低证据节点：confidence 低但被多次引用。
- 桥接节点：同时连接多个领域。
- 冲突节点：同一 claim 有支持和反对来源。

## 项目融合建议

短期先做 Markdown 版 health check，不急着做图可视化。等节点多了再引入社区发现和可视化。

## 可拓展性

- 可以通过什么接口/适配层接入：weekly health script、Agent API `/health`、Obsidian Bases。
- 未来可能被什么替代：完整图数据库/知识图谱仪表盘。
- 替换或升级成本：低。
- 回退方式：健康报告只是输出层，不影响源文件。

## 验证指标

- 每周是否能发现至少一个真实盲区或冲突。
- 修复健康报告里的问题后，检索和回答是否更准。
- Agent 调用 context pack 时是否减少无关资料。
