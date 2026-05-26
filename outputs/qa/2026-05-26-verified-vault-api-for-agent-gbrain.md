---
type: qa
status: captured
asked_at: 2026-05-26
question: "资料库做好后，是否可以给 agent 一个 API 调用我们的知识库，再结合它自己的 gbrain 分析？"
related:
  - "[[verified-vault-api-for-agent-brain]]"
  - "[[verified-vault-api-should-stay-separate-from-agent-gbrain]]"
  - "[[do-not-blindly-merge-vault-and-agent-brain]]"
source_status: user-insight
confidence: 4
---

# Verified Vault API for Agent + gbrain

## TL;DR

合理，而且是高信号中期方向。资料库应该作为已提炼、已打标签、可验证的知识源，通过 API 或 resolver 给 agent 提供 context pack；agent 再结合自己的 gbrain、关系图谱和当前 session 目标做分析。

## 关键边界

不要把资料库和 gbrain 直接混成一锅。

```text
资料库
  = 用户确认、来源可追溯、带验证状态的 compiled knowledge

gbrain
  = agent 自己的关系图谱、世界模型、任务经验和推理结构

session
  = 当前任务的短期上下文和目标
```

三者应该通过 API / resolver / context pack 连接。

## 合理架构

```text
用户问题
  -> agent 判断需要哪些知识
  -> 调用资料库 API
  -> 返回相关 concepts / patterns / claims / anti-patterns
  -> 每条带来源、置信度、验证状态、反例
  -> agent 和自己的 gbrain 合并推理
  -> 输出结论
  -> 新洞察回写 outputs/qa 或 candidate claim
```

## 为什么合理

- 资料库解决可信来源和验证问题。
- gbrain 解决关系推理和长期认知问题。
- API 解决按需调用和边界问题。
- context pack 解决上下文污染问题。

## API 不应该只返回正文

返回内容必须带：

- `node_id`
- `type`
- `summary`
- `sources`
- `verification_status`
- `evidence_level`
- `confidence`
- `related_nodes`
- `negative_evidence`
- `last_verified`

## 当前建议

短期不要急着搭完整 API。

先做：

- `vault-index.md`
- 干净的 metadata。
- concepts / patterns / claims / anti-patterns。
- 用脚本或 agent 读 Markdown 模拟 API。

中期再考虑：

- 本地 HTTP API。
- MCP server。
- Graph query。
- RAG/embedding。

## 风险

- API 如果没有可信度字段，会放大垃圾信息。
- 如果允许 agent 直接写核心资料库，会污染已验证知识。
- 如果过早上复杂后端，会拖慢资料沉淀。

## 当前结论

高信号，进入中期架构候选。

