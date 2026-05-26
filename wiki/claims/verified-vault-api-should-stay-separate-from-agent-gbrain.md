---
type: claim
status: cross-checked
claim: "A verified knowledge vault API should stay separate from the agent's own gbrain while providing context packets on demand."
created: 2026-05-26
topics:
  - knowledge-api
  - gbrain
  - agent-context
related_projects:
  - 资料库
  - AI短剧
sources:
  - current user insight
  - gbrain prior audit memory
  - "[[source-verification-and-trust-model]]"
supporting_sources:
  - "gbrain brain-vs-memory-vs-session layering"
  - "current source verification model"
  - "Karpathy / Heinrich index-first context loading"
conflicting_sources:
evidence_level: secondary
verification_status: cross-checked
confidence: 4
impact: 5
last_verified: 2026-05-26
next_review:
tags:
  - claim/high-signal
  - agent/context
  - gbrain/boundary
---

# 主张：Verified vault API should stay separate from agent gbrain

## 主张

资料库可以作为一个经过提炼和验证的知识 API，供 agent 调用；但它应该和 agent 自己的 gbrain 保持边界。Agent 需要时获取 context pack，再结合自己的关系图谱和 session 目标分析。

## 为什么重要

如果直接把资料库混进 gbrain，agent 的自我认知、世界模型、任务记忆和用户验证知识会混淆。这样会降低可追溯性，也更难判断某个结论是用户确认过的资料，还是 agent 自己推断出来的。

## 支持证据

- gbrain prior audit 中最可借鉴的是 brain / memory / session 分层、compiled truth、resolver/skill routing 和安全边界。
- 当前资料库已经建立 source verification、claims、patterns、anti-patterns。
- Karpathy / Heinrich 的索引优先模式支持按需注入，而不是全量融合。

## 反例 / 冲突证据

- 如果 API 太薄，agent 仍然需要自己大量读文件。
- 如果 API 太复杂，早期会过度工程。
- 如果 metadata 不干净，API 会放大垃圾信息。

## 标签与量化

- evidence_level: secondary
- verification_status: cross-checked
- confidence: 4
- impact: 5
- relevance: 5

## 验证方式

先用 Markdown index + 脚本模拟 API，测试 agent 是否能通过查询获取高质量 context pack，并正确引用来源和反例。

## 当前结论

高信号。适合作为中期架构方向，但短期不要急着搭完整 API 服务。

## 复查计划

当资料库有 100+ 节点、至少 20 条 claim/pattern/anti-pattern 时，复查是否需要本地 HTTP API 或 MCP。

