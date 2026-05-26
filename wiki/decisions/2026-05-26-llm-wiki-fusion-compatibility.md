---
type: decision
status: accepted
created: 2026-05-26
decision_scope:
  - llm_wiki
  - knowledge_graph
  - verified_vault
  - agent_api
related_sources:
  - raw/repos/2026-05-26-llm-wiki-source.md
related_patterns:
  - purpose-md-as-wiki-mission-layer
  - four-signal-graph-relevance
  - graph-insights-health-check
  - local-verified-vault-api
  - async-review-queue-for-ai-ingest
  - provenance-safe-source-lifecycle
confidence: high
---

# 决策：llm_wiki 提炼设计的融合兼容性

## 结论

`llm_wiki` 提炼出的设计点和我们当前资料库架构不冲突，但必须分层采用，不能一次性融合成完整 App。

当前采用策略：

- 立即采用：使命层、来源字段、验证标签、review 思路。
- 轻量适配：四信号关系评分、图谱健康检查、来源生命周期。
- 中期观察：本地 API / context pack。
- 暂不采用：完整 Tauri 桌面 App、复杂 ingest queue、LanceDB/vector search、完整图谱 UI。

## 兼容性矩阵

| 设计点 | 和当前架构是否冲突 | 处理方式 | 原因 |
|---|---|---|---|
| `purpose.md` 使命层 | 不冲突 | 立即采用 | 补足 vault 为什么存在，不改变现有目录 |
| `schema.md` / 结构契约 | 不冲突 | 后续增强 | 可和现有模板并存，负责规则而不是内容 |
| 四信号关系评分 | 不冲突，但依赖元数据质量 | 轻量适配 | 必须先有干净的 `sources[]`、`type`、links |
| 图谱健康检查 | 不冲突 | 轻量适配 | 作为 `outputs/health/` 输出层，不侵入核心 |
| Local Verified Vault API | 不冲突，但不宜过早 | 中期观察 | 需要等节点和调用需求足够多 |
| 异步 review 队列 | 不冲突 | 立即采用轻量版 | 保护资料库不被未验证信息污染 |
| 来源生命周期 | 不冲突 | 轻量适配 | 先做 stale/review，不做自动删除 |
| Louvain 社区检测 | 不冲突，但暂时过重 | 暂缓 | 节点数量不足时收益不大 |
| Vector search / LanceDB | 不冲突，但暂时过重 | 暂缓 | 当前先用索引、链接、frontmatter |
| 完整桌面 App | 有阶段冲突 | 暂不采用 | 会过早固化还没验证的流程 |

## 和我们现有模板的关系

当前模板不冲突，分工如下：

- `source-record`：记录资料来源和可信度。
- `library-review`：分析一个库整体有什么价值。
- `design-pattern`：沉淀可复用优秀设计。
- `claim-record`：沉淀可验证主张。
- `anti-pattern`：记录不可行路线和踩坑。
- `decision-record`：记录是否采用、怎么融合、为什么。
- `purpose.md`：提供全局方向。

这些不是重复，而是从不同角度描述同一套知识编译流程。

## 融合边界

必须坚持三层边界：

```text
Verified Vault
  用户确认、来源可追溯、带验证状态的知识

Graph / Index / API
  检索、关系、上下文打包层

Agent gbrain
  Agent 自己的世界模型、任务经验、推理结构
```

不能把三者混成一锅。尤其不能让 Agent 把未验证资料直接写成高置信知识。

## 潜在冲突与解决方式

### 冲突 1：图谱评分可能放大垃圾来源

解决：

- 评分前必须先有 source quality gate。
- 高分关系必须展示支撑来源。
- 自动链接先进入 review。

### 冲突 2：API 可能让 Agent 误用未验证资料

解决：

- API / context pack 必须返回 `verification_status`、`evidence_level`、`confidence`。
- 默认不返回 rejected / deprecated 内容，除非明确查询反模式。

### 冲突 3：完整 App 可能过早锁死结构

解决：

- 当前只做 Markdown-first。
- 等节点数量、字段结构、调用方式稳定后再考虑 App/API。

### 冲突 4：不同库的模板风格可能不一致

解决：

- 不直接复制任何库的模板。
- 所有外部设计都先转成我们的 `pattern / claim / anti-pattern / decision` 格式。
- 后续统一设计时只融合通过验证的模式。

## 当前融合路线

阶段 1：

- 保持当前 vault 目录。
- 已加入 `purpose.md`。
- 继续用 source / pattern / claim / anti-pattern 记录资料。

阶段 2：

- 做第一版 health report。
- 检查孤岛节点、冲突主张、低证据高引用、待 review 项。

阶段 3：

- 做四信号关系评分脚本。
- 输出高信号关系，而不是做 UI。

阶段 4：

- 做 context pack generator。
- 再决定是否升级到本地 API / MCP。

## 最终判断

这些借鉴点可以融合，但必须按“低耦合、可回退、先验证、后自动化”的顺序推进。

`llm_wiki` 给我们的不是要照搬的产品，而是一组经过工程验证的设计候选。我们吸收它的机制，不吸收它的全部复杂度。

## 2026-05-26 追加：是否直接使用或 fork

进一步阅读当前源码后，采用策略明确为：

- 不直接替代当前资料库。
- 可以把 `llm_wiki` 当辅助 App 或工程参考。
- 中期可以 fork，但 fork 目标不是做普通 LLM Wiki，而是改成 `Verified Knowledge` 模板。
- fork 第一刀只改模板和 ingest prompt，不急着改 UI。

原因：

- `llm_wiki` 的工程能力强，尤其是 ingest / cache / queue / graph / search / local API。
- 但它默认 schema 偏 wiki 页面组织，不足以表达本资料库需要的 evidence level、verification status、confidence、negative evidence、risk、adoption stage。
- 直接使用会降低可信知识治理密度。
- 完全不用又会浪费成熟工程轮子。

因此当前路线是：

```text
短期：吸收设计，保留 Markdown-first 资料库。
中期：如需自动化，再 fork llm_wiki 做 verified template。
长期：把 local API 升级成带证据和风险字段的 context pack resolver。
```
