---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - nashsu/llm_wiki
related_concepts:
  - source-verification-and-trust-model
  - evidence-backed-design-validation
  - negative-evidence-and-avoidance
related_projects:
  - verified-vault
adoption_status: adapt
tags:
  - review
  - human-in-the-loop
  - ingest
  - quality-gate
evidence_count: 2
confidence: high
negative_evidence:
  - algorithmic-graph-scoring-without-source-quality
replaces:
superseded_by:
extension_points:
  - review inbox
  - claim verification queue
  - source trust queue
---

# 设计模式：AI 摄取后的异步 Review 队列

## 一句话定义

LLM 先把新资料里的疑点、冲突、待建页面、待研究问题放进 review 队列，人再按优先级判断，不让 AI 直接把所有内容写成“确定知识”。

## 解决的问题

用户明确说资料库不能是一堆未经验证的垃圾。异步 review 队列能把“AI 很会整理”和“人必须判断可信度”分开，让质量控制不阻塞摄取，也不消失。

## 适用场景

- 新资料很多，无法每次同步精读。
- 资料中有主张、争议、预测、技术选型。
- 需要保留未验证/待确认/冲突信息。

## 不适用场景

- 原始资料极少，可以直接人工读完。
- 资料只作临时参考，不会进入长期知识库。

## 反例与避坑

- 失败条件：review 队列只进不出，最后变成第二个垃圾箱。
- 相似反模式：AI 自动通过所有 review。
- 复杂度风险：一开始做复杂 UI 和状态机。
- 替代方案：先用 Markdown `outputs/review/` 或 `wiki/claims` 的状态字段。

## 来源证据

`nashsu/llm_wiki` README 描述异步 review system：LLM 在 ingest 中标记需要人类判断的项目，动作类型受限，用户之后再处理。

## 标签与量化

- domain: knowledge_quality
- problem: ai_ingest_trust
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 4
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：Karpathy 的 human curates, LLM maintains。
- 历史项目影子：用户要求已验证/未验证、消息来源、负面证据都打标签。
- 支持证据：`llm_wiki` 把 human judgment 做成产品级队列。
- 反例：没有清理节奏的 review 队列会堆积。

## 最小实现方式

先创建 `outputs/review/`，每个待判断项是一个 Markdown：

- source
- claim
- why_review_needed
- proposed_action
- evidence_status
- priority
- decision

## 项目融合建议

采用轻量版。尤其用于开源库分析、AI短剧素材、技术选型、商业信息。

## 可拓展性

- 可以通过什么接口/适配层接入：Obsidian Bases、CLI、Agent API。
- 未来可能被什么替代：正式 review UI 或任务系统。
- 替换或升级成本：低。
- 回退方式：review item 本身是 Markdown。

## 验证指标

- 未验证主张是否不会直接进入高置信 claim。
- 每周 review 队列是否能被清空或降级。
- 被 review 拦住的信息是否减少后续误用。
