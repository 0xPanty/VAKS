---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - nashsu/llm_wiki
related_concepts:
  - verified-vault-api-for-agent-brain
  - second-brain-knowledge-graph
  - source-verification-and-trust-model
related_projects:
  - verified-vault
  - agent-gbrain
adoption_status: watch
tags:
  - api
  - agent-context
  - local-first
  - resolver
evidence_count: 3
confidence: high
negative_evidence:
  - do-not-blindly-merge-vault-and-agent-brain
replaces:
superseded_by:
extension_points:
  - MCP server
  - local HTTP API
  - CLI context pack generator
---

# 设计模式：Local Verified Vault API

## 一句话定义

把已经验证和结构化的资料库作为本地只读/半只读 API 提供给 Agent，让 Agent 调用知识，而不是把知识硬塞进聊天上下文。

## 解决的问题

Agent 没有长期可靠记忆。直接让 Agent 靠聊天记录会丢上下文，直接把 vault 和 gbrain 混在一起又会污染。API 是中间层：Agent 按需请求，资料库返回带来源、置信度和关系的 context pack。

## 适用场景

- 资料库已有明确 source、claim、pattern、anti-pattern。
- Agent 需要跨项目调用知识。
- 希望保持 vault 为用户确认的 source of truth。
- 希望 gbrain 保留 Agent 自己的世界模型，但不吞掉用户资料库。

## 不适用场景

- 资料库还没结构化。
- 还没有来源和验证状态。
- 当前阶段用文件读取就够了。

## 反例与避坑

- 失败条件：API 返回未验证资料，但 Agent 当成确定事实。
- 相似反模式：盲目合并 vault 与 gbrain。
- 复杂度风险：过早设计完整服务、权限、数据库、缓存。
- 替代方案：先做 CLI / Markdown index / context-pack 文件。

## 来源证据

`nashsu/llm_wiki` 提供本地 `127.0.0.1:19828` API，README 记录用途包括 hybrid search、file read、graph traversal、source rescan。源码中可见：

- `GET /api/v1/health`
- `GET /api/v1/projects`
- `GET /api/v1/projects/{id}/files`
- `GET /api/v1/projects/{id}/files/content`
- `POST /api/v1/projects/{id}/search`
- `GET /api/v1/projects/{id}/graph`
- `POST /api/v1/projects/{id}/sources/rescan`

注意：源码也显示 `POST /chat` 在 Rust API server 里尚未实现。

## 标签与量化

- domain: agent_memory
- problem: reliable_context
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 5
- evidence_strength: 5
- reversibility: 4

## 交叉验证

- 相似来源：用户提出的 Verified Vault API + gbrain。
- 历史项目影子：gbrain 需要世界认知和关系图谱，但用户资料库需要可信来源边界。
- 支持证据：`llm_wiki` 已有本地 API 实现。
- 反例：API 安全和 token 泄露需要谨慎处理。

## 最小实现方式

先不做服务。用脚本生成：

- `outputs/context-packs/<topic>.md`
- 包含 related concepts、patterns、claims、anti-patterns、sources、confidence。

后续再升级为：

- `GET /search`
- `GET /node/{id}`
- `GET /related/{id}`
- `POST /context-pack`

## 项目融合建议

中期采用。现在先强化 frontmatter 和索引，等资料库有足够节点后再实现 API。

## 可拓展性

- 可以通过什么接口/适配层接入：local HTTP、MCP、CLI。
- 未来可能被什么替代：图数据库或专用 retrieval service。
- 替换或升级成本：中。
- 回退方式：所有知识仍是 Markdown，API 只是读取层。

## 验证指标

- Agent 是否能在不读取全库的情况下拿到正确 context。
- API 返回结果是否都带来源和验证状态。
- gbrain 推理和 vault 事实是否能保持边界清晰。
