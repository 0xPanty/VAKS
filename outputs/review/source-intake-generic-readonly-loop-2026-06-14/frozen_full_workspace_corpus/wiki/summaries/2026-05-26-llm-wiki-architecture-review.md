---
type: library_review
status: reviewed
library_name: nashsu/llm_wiki
repo_url: https://github.com/nashsu/llm_wiki
source_url: https://github.com/nashsu/llm_wiki
reviewed_at: 2026-05-26
domain: ai_knowledge_base
related_projects:
  - verified-vault
  - second-brain
  - ai-short-drama
extracted_patterns:
  - purpose-md-as-wiki-mission-layer
  - four-signal-graph-relevance
  - graph-insights-health-check
  - local-verified-vault-api
  - async-review-queue-for-ai-ingest
  - provenance-safe-source-lifecycle
fusion_decision: adapt
confidence: high
evidence_count: 7
cross_validated_with:
  - Karpathy LLM Wiki pattern
  - Heinrich thinking OS vault
  - Yanhua Obsidian Claude content factory
  - Verified Vault API for Agent gbrain
negative_evidence:
  - full-app-overengineering-before-clean-markdown-vault
  - algorithmic-graph-scoring-without-source-quality
extension_potential: high
---

# 库分析：nashsu/llm_wiki

## 一句话结论

这次不是单纯验证我们的思路。`llm_wiki` 有真实增量，而且有几个可以进入候选 alpha design：四信号关系图谱、本地 Agent API、`purpose.md` 使命层、图谱健康检查、异步人工 review 队列。

## 它解决什么问题

它想解决普通 RAG 的问题：每次提问都重新检索和拼答案，知识没有沉淀。它把资料先编译成一个持续增长的 wiki，再让查询、图谱、健康检查、Agent API 都围绕这个 compiled wiki 工作。

## 核心设计

- `raw/sources/`：不可变原始资料。
- `wiki/`：LLM 生成和维护的结构化知识。
- `purpose.md`：知识库为什么存在、研究范围、关键问题、演化方向。
- `schema.md`：知识库怎么组织、页面类型、命名、链接和 frontmatter 规则。
- `index.md`：LLM 进入知识库时的导航入口。
- `log.md`：按时间记录 ingest/query/lint。
- `overview.md`：全局综合视图，随 ingest 更新。
- `.llm-wiki/`：应用内部状态，不应成为我们长期知识源头。

## 值得提炼的模式

1. `purpose.md` 和 `schema.md` 分离：`purpose.md` 管方向，`schema.md` 管结构。
2. 四信号关系图谱：直接链接、共同来源、共同邻居、类型亲和共同决定相关性。
3. 图谱健康检查：孤岛节点、低内聚社区、桥接节点、意外连接都可以变成知识库体检指标。
4. Local Verified Vault API：本地 `127.0.0.1` API 给 Agent 提供 search/file/graph/source rescan。
5. 异步 review 队列：LLM 可以先提取疑点、建议、人类判断项，但不直接把一切当真。
6. 来源生命周期：`raw/sources/` 自动 watch，新增/修改/删除都进入一致的 ingest/delete cleanup。

## 标签与量化

- domain: personal_knowledge_base / agent_context / knowledge_graph
- problem: compiled_knowledge / context_retrieval / evidence_validation
- pattern: graph_scoring / local_api / human_review / purpose_layer
- maturity: emerging
- complexity: high
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 4
- integration_fit: 4
- evidence_strength: 5
- reversibility: 3

## 交叉验证

- Karpathy：`raw -> wiki -> schema`、LLM 维护 wiki、index/log、lint。
- Heinrich：vault index 作为上下文路由器，每个 vault 需要自己的 philosophy。
- Yanhua：Obsidian + Claude + Skills，把知识库变成行动系统。
- 我们已确定方向：Verified Vault API 和 gbrain 分层连接。

`llm_wiki` 的价值在于把这些想法进一步工程化：图谱可以算、API 可以调、健康检查可以出指标、review 可以排队。

## 对当前项目的适配点

短期立刻借鉴：

- 给我们的 vault 增加 `purpose.md`。
- 在每条 pattern/claim/source 中强化 `sources[]` 和 evidence 字段。
- 用四信号关系模型作为“高信号指标”的初版评分框架。
- 把健康检查从自然语言检查升级成结构指标。
- 把 `POST /context-pack` 之类 API 设为中期接口目标。

中期再考虑：

- Louvain 社区发现。
- 图谱可视化。
- 本地 HTTP API。
- 混合搜索和向量检索。

暂不照搬：

- 完整 Tauri 桌面 app。
- 复杂 ingest queue。
- LanceDB/vector search。
- 多 provider deep research。

## 不可行点 / 避坑

- 不要在 Markdown 资料库结构还没稳定时，先做完整 App。
- 不要把算法打分当真理。frontmatter 和链接质量差时，图谱分数会放大噪声。
- 不要把 `.llm-wiki/` 这类应用状态当长期知识源头。
- 不要一上来做向量数据库。先用索引、frontmatter、链接和脚本跑通。

## 融合判断

- 结论：adapt。
- 理由：设计增量高，但直接照搬成本也高。
- 最小验证方式：先做 Markdown-only 版本的 `purpose.md + sources[] + 四信号评分脚本 + health report`。

## 后续行动

- 新增 `purpose.md` 模板。
- 后续库分析开始给每条 pattern 打 relation score。
- 健康检查模板加入孤岛节点、低内聚主题、桥接节点、冲突主张。
- 中期设计一个本地只读 API 或 MCP resolver。

## 2026-05-26 追加复核：和 verified knowledge system 的关系

本轮进一步读了当前仓库的 README、模板、ingest、cache、queue、graph、search、API server、review、source lifecycle、file watcher、vectorstore 等核心模块。结论没有改变，但边界更清楚：

`llm_wiki` 的强项是工程化知识编译机，不是可信真值系统。

它适合解决：

- 原始资料怎么自动导入。
- AI 怎么把资料编译成 wiki。
- wiki 怎么维护 index / log / overview。
- 页面之间怎么用链接、共同来源、共同邻居、类型亲和计算关系。
- 大量来源怎么用 queue / cache / watcher / lifecycle 管起来。
- Agent 怎么通过本地 API 查询 wiki。

它不直接解决：

- 某条 claim 是否可信。
- 某个 pattern 是否值得采纳。
- 反例和失败条件是否充分。
- source quality 会不会污染图谱分数。
- 设计点进入 decision 前是否经过证据、风险、回退判断。

所以它和当前资料库不是替代关系，而是互补关系：

```text
llm_wiki
  = 自动知识编译机 / 工程发动机 / 操作台参考

本资料库
  = Verified Knowledge Graph / 可信知识判断体系 / 采纳规则
```

当前最佳路线不是直接迁移，也不是重造所有轮子，而是：

1. 短期吸收 `purpose.md`、`schema.md`、two-step ingest、source lifecycle、review queue、graph health 的设计。
2. 保留本资料库的 `claim / pattern / anti-pattern / decision / evidence / confidence / risk` 真值层。
3. 中期可以 fork `llm_wiki`，增加 `Verified Knowledge` 模板和更严格的 ingest prompt。
4. 未来如果做 API，应返回 context pack，而不是只返回普通搜索结果。

实现级防错点已单独记录到 `outputs/qa/2026-05-26-llm-wiki-implementation-extraction.md`，包括 ingest parser、cache、queue、project identity、source lifecycle、graph score、search、API、file watcher、vectorstore 等模块的不变量。
