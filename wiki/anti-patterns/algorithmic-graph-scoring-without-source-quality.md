---
type: anti_pattern
status: active
created: 2026-05-26
domain: knowledge_graph
failure_mode: false_confidence
severity: 5
likelihood: 3
complexity_cost: 4
cross_validated_with:
  - nashsu/llm_wiki
  - source-verification-and-trust-model
related_projects:
  - verified-vault
replacement: source-quality-gated graph scoring
decision: avoid
---

# 反模式 / 踩坑：没有来源质量就做图谱算法打分

## 问题描述

图谱算法会给人一种“很科学”的感觉，但如果节点来源不可信、`sources[]` 错、type 乱、双链是 AI 胡乱补的，那么打分越精细，误导越强。

## 为什么不可行

四信号评分依赖输入质量：

- direct link 依赖链接质量。
- source overlap 依赖 source id 准确。
- common neighbor 依赖整体图结构。
- type affinity 依赖页面类型一致。

输入是垃圾，关系分数就是高置信垃圾。

## 失败条件

- 未验证资料直接进入 wiki。
- 自动链接未经 review。
- source_url/source_id 缺失。
- 同一来源多种命名，导致 overlap 失真。

## 标签与量化

- domain: knowledge_graph
- failure_mode: false_confidence
- severity: 5
- likelihood: 3
- complexity_cost: 4
- evidence_strength: 4
- reversibility: 3

## 交叉验证

- 相似失败来源：RAG 和知识图谱常见问题都是检索结果看似相关但来源不可靠。
- 历史项目证据：用户明确要求已验证/未验证/消息来源/负面证据。
- 支持证据：`llm_wiki` 的四信号模型本身依赖 frontmatter 和 wikilinks。
- 是否可能只是局部失败：如果 source metadata 很干净，算法分数会有价值。

## 应该避开什么

- 把算法分数等同于事实可靠性。
- 为了提高图谱连通度乱加链接。
- 没有人工 review 就让 Agent 自动采纳高分方向。

## 替代方案

先做来源质量门槛：

- source_id 稳定。
- verification_status 明确。
- evidence_level 明确。
- 自动链接进入 review。
- 高分关系必须显示支撑来源。

## 后续是否需要复测

需要。等我们有足够节点后，用人工抽样检查高分关系准确率。
