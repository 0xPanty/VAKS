---
type: anti_pattern
status: avoid
created: 2026-05-26
domain: agent-memory
failure_mode: boundary collapse between verified vault and agent brain
severity: 5
likelihood: 3
complexity_cost: 4
cross_validated_with:
  - gbrain prior audit
  - source verification model
related_projects:
  - 资料库
  - AI短剧
replacement: "Keep verified vault, agent gbrain, and session context separate; connect them via resolver/API/context packets."
decision: avoid
---

# 反模式 / 踩坑：不要把资料库和 agent gbrain 盲目合并

## 问题描述

资料库是用户确认、提炼、验证过的知识系统；gbrain 是 agent 自己的关系图谱、世界模型和任务记忆。如果直接混在一起，会让来源、置信度和责任边界变模糊。

## 为什么不可行

合并后很难回答：

- 哪些是用户验证过的事实？
- 哪些是 agent 推理出来的假设？
- 哪些来自外部资料？
- 哪些是过时信息？
- 哪些可以用于决策？

这会让“第二大脑”变成高置信幻觉仓库。

## 失败条件

- 不区分 source / claim / inference。
- 不记录 verification_status。
- agent 能直接覆盖资料库核心节点。
- gbrain 自动吸收所有资料，不经过验证。

## 标签与量化

- domain: agent-memory
- failure_mode: provenance collapse
- severity: 5
- likelihood: 3
- complexity_cost: 4
- evidence_strength: 4
- reversibility: 2

## 交叉验证

- 相似失败来源：gbrain prior audit 中强调 brain-vs-memory-vs-session layering。
- 历史项目证据：用户长期强调边界、来源和可验证。
- 支持证据：当前资料库已经建立可信度治理。
- 是否可能只是局部失败：是。经过验证的 compiled knowledge 可以同步给 gbrain，但必须保留来源和状态。

## 应该避开什么

- 直接把整个 vault 灌入 gbrain。
- 让 agent 把推断结果写成已验证事实。
- API 返回内容不带证据等级。

## 替代方案

```text
Verified Vault
  -> API / resolver / context pack
  -> Agent gbrain
  -> Session reasoning
  -> 输出和新洞察回写 outputs/qa 或 candidate claims
```

## 后续是否需要复测

当建立本地 API/MCP 时，测试 read-only、writeback queue、verification gate。

