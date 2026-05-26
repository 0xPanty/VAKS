---
type: anti_pattern
status: active
created: 2026-05-26
domain: knowledge_base
failure_mode: overengineering
severity: 4
likelihood: 4
complexity_cost: 5
cross_validated_with:
  - nashsu/llm_wiki
  - Karpathy LLM Wiki pattern
related_projects:
  - verified-vault
replacement: markdown-first contracts before app shell
decision: avoid
---

# 反模式 / 踩坑：Markdown 结构没稳就先做完整 App

## 问题描述

看到 `llm_wiki` 这种完整桌面应用，很容易马上想做 Tauri、图谱 UI、API、vector search、队列、review 系统。但如果我们的 Markdown 契约、source 字段、claim 状态、pattern 结构还没稳定，先做 App 会把不成熟流程固化。

## 为什么不可行

完整 App 会把复杂度前置，而我们现在真正需要验证的是：

- 哪些字段必须有。
- 哪些资料值得进入 wiki。
- 哪些 pattern 会被多源验证。
- Agent 需要什么 context pack。
- 健康检查应该怎么判断知识腐烂。

这些没跑通时，App 只是漂亮壳。

## 失败条件

- 节点少于 50 个。
- source/claim/pattern 模板还经常变化。
- 没有稳定 ingest 和 review 规则。
- API 需求还没被真实 Agent 调用验证。

## 标签与量化

- domain: knowledge_base
- failure_mode: premature_app_building
- severity: 4
- likelihood: 4
- complexity_cost: 5
- evidence_strength: 4
- reversibility: 2

## 交叉验证

- 相似失败来源：很多知识库项目从工具开始，最后资料质量没有提高。
- 历史项目证据：用户强调不要糊弄，要科学采纳，不是堆功能。
- 支持证据：`llm_wiki` 是高复杂度实现，适合作参考，不适合当前直接复刻。
- 是否可能只是局部失败：当 vault 足够大、流程稳定后，App 可能有价值。

## 应该避开什么

- 现在就做完整桌面应用。
- 现在就上向量库和图数据库。
- 现在就追求酷炫图谱 UI。

## 替代方案

先做 Markdown-first：

- `purpose.md`
- `sources[]`
- pattern/claim/anti-pattern 模板
- health report
- context pack 输出

## 后续是否需要复测

需要。等资料库有稳定节点和真实调用需求后复查。
