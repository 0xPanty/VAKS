---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - gbrain prior audit
  - current knowledge vault design
related_concepts:
  - "[[source-verification-and-trust-model]]"
  - "[[second-brain-knowledge-graph]]"
  - "[[evolvable-design-system]]"
related_projects:
  - 资料库
  - AI短剧
adoption_status: candidate
tags:
  - pattern/knowledge-api
  - pattern/agent-context
  - pattern/gbrain
evidence_count: 3
confidence: medium
negative_evidence:
  - "[[do-not-blindly-merge-vault-and-agent-brain]]"
replaces:
superseded_by:
extension_points:
  - search-api
  - graph-api
  - context-pack-api
  - evidence-api
---

# 设计模式：Verified Vault API for Agent Brain

## 一句话定义

把已经提炼、验证、打标签的资料库做成一个只读优先的知识 API，让 agent 按需调用，再和自己的 gbrain / world model / session context 组合分析。

## 解决的问题

Agent 自己的 gbrain 可以记录关系、世界模型和行动经验，但它不应该独自承担所有事实来源和证据治理。

资料库负责：

- 高质量来源。
- 验证状态。
- 证据等级。
- 设计点。
- 反模式。
- 历史项目关键判断。

Agent/gbrain 负责：

- 当前任务理解。
- 关系推理。
- 路由和上下文组合。
- 行动策略。
- 和当前 session 的即时目标融合。

中间用 API 连接，可以避免把两者混成一锅。

## 适用场景

- Agent 需要读取用户长期资料库。
- 用户已经有结构化 concepts / patterns / claims / anti-patterns。
- 资料库需要支持多个 agent 或多个项目。
- 需要把可信度、来源、反例一起传给 agent。

## 不适用场景

- 资料库还没有基本结构和来源标注。
- agent 只需要一次性读取少量文件。
- API 变成提前过度工程，反而拖慢资料积累。

## 反例与避坑

- 失败条件：API 返回内容不带来源、置信度、反例和更新时间。
- 相似反模式：直接把整个 vault 塞给 agent 或直接把资料库全部灌进 gbrain。
- 复杂度风险：过早做完整后端、向量库、权限系统。
- 替代方案：先用 Markdown index + CLI/search 脚本模拟 API。

## 来源证据

- 当前资料库已经建立 `Source` / `Claim` / `Pattern` / `Anti-pattern` 和可信度字段。
- gbrain  prior audit 中的高价值模式包括 brain-vs-memory-vs-session layering、compiled truth、resolver/skill routing、安全边界。
- Karpathy / Heinrich / Yanhua 系列都支持“索引优先、按需注入、AI 操作、人的判断”的方向。

## 标签与量化

- domain: agent-memory / knowledge-runtime
- problem: trustworthy context retrieval
- maturity: emerging
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：gbrain compiled truth + resolver、Karpathy raw/wiki/outputs、Heinrich vault index、当前 source verification model。
- 历史项目影子：用户长期多项目开发，需要新窗口/agent 能拿到完整关系和证据。
- 支持证据：资料库已经落地 concepts、patterns、claims、anti-patterns、qa、handoff。
- 反例：没有验证元数据的 API 只会把垃圾信息更快喂给 agent。

## 最小实现方式

先不做复杂服务。第一阶段用文件协议/脚本模拟 API：

```text
query: 关键词/主题/项目
  -> 读取 vault-index
  -> 返回相关 concepts / patterns / claims / anti-patterns
  -> 每条都带 source_status / evidence_level / confidence / last_verified
  -> 生成 context pack
```

建议接口形态：

```text
GET /search?q=
GET /node/{id}
GET /related/{id}
GET /claims?topic=
GET /anti-patterns?topic=
POST /context-pack
```

返回必须包含：

```text
node_id
type
summary
links
sources
verification_status
evidence_level
confidence
negative_evidence
last_verified
```

## 项目融合建议

采用为中期方向。短期先不搭服务，先把 Markdown 节点和索引质量做好。

## 可拓展性

- 可以通过什么接口/适配层接入：CLI、MCP server、本地 HTTP API、Obsidian plugin、RAG。
- 未来可能被什么替代：专用 knowledge runtime 或 graph database。
- 替换或升级成本：低到中，前提是 Markdown 和 metadata 保持干净。
- 回退方式：直接让 agent 读 Markdown index 和相关文件。

## 验证指标

- Agent 是否能通过 API 找到正确资料。
- 返回内容是否包含来源、置信度和反例。
- 是否减少重复解释历史背景。
- 是否提升跨项目分析完整度。
- 是否避免未验证资料污染 agent 判断。

## 2026-05-26 交叉验证：nashsu/llm_wiki

`nashsu/llm_wiki` 提供了一个本地 `127.0.0.1:19828` API，支持 project/files/search/graph/source rescan。这强力验证了本模式：已编译资料库可以作为 Agent 的外部知识接口。

需要注意的边界：

- 它的 Rust API chat endpoint 尚未实现，不能把它当作完整 Agent 对话后端。
- API 是读取和检索层，不应该吞并 Agent gbrain。
- API 返回的知识仍应带 sources、verification_status、confidence。

新增关联：

- [[local-verified-vault-api]]
- [[four-signal-graph-relevance]]
- [[graph-insights-health-check]]
