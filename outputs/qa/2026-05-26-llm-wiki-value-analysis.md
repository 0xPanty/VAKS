---
type: qa
question: "nashsu/llm_wiki 对我们的资料库设计有什么价值？"
asked_at: 2026-05-26
sources:
  - raw/repos/2026-05-26-llm-wiki-source.md
related:
  - wiki/summaries/2026-05-26-llm-wiki-architecture-review.md
  - wiki/patterns/four-signal-graph-relevance.md
  - wiki/patterns/local-verified-vault-api.md
  - wiki/patterns/graph-insights-health-check.md
confidence: high
---

# Q&A：llm_wiki 的价值分析

## TL;DR

有价值，而且不是普通验证。它给了我们“知识图谱 + 可信来源 + Agent API”的实现级参考。

最应该吸收的是：

1. `purpose.md` 使命层。
2. 四信号关系评分。
3. 图谱健康检查。
4. 本地 Verified Vault API。
5. 异步 human review 队列。
6. 来源生命周期和 stale 处理。

最不应该现在做的是完整复刻桌面 App。

## 它和我们已有思路怎么碰撞

我们之前确定的方向：

- 资料库不是收藏夹，而是 compiled knowledge。
- 来源要验证，主张要打标签，负面证据也要记录。
- 后续 Agent 可以通过 API 调用资料库，再结合 gbrain 推理。
- 关系图谱用于构造第二大脑。

`llm_wiki` 的贡献：

- 把“关系图谱”从抽象双链变成四信号评分。
- 把“健康检查”从自然语言建议变成图谱指标。
- 把“Agent 调用资料库”变成本地 API 设计。
- 把“AI 不要直接污染知识库”变成异步 review 队列。

## 高信号方向

### 1. 四信号图谱是高信号指标的雏形

直接链接只是一个信号。共同来源、共同邻居、类型亲和能让“相似思路”和“优秀点的影子”更可计算。

这符合用户要求：不是觉得像，而是能交叉验证。

### 2. Verified Vault API 被强力验证

我们之前提出资料库 API 给 Agent 调用，`llm_wiki` 已经在做类似方向。本地 API 只暴露项目、文件、搜索、图谱、source rescan，是合理边界。

但它的 chat API 尚未实现，所以我们不应假设它已经是完整 Agent 后端。

### 3. purpose.md 是缺失层

我们之前有 README、handoff、patterns，但还缺一个明确告诉 Agent “这个资料库为什么存在”的根文件。`purpose.md` 值得马上补。

### 4. Review 队列解决“垃圾资料进大脑”

资料库要能吸收信息，但不能直接相信信息。让 AI 把待判断项排队，人来定，是很合理的折中。

## 采纳顺序

第一阶段：

- 新建 `purpose.md`。
- 强化 `sources[]`、`evidence_level`、`verification_status`。
- 每次库分析都写 pattern/claim/anti-pattern。

第二阶段：

- 做 Markdown 版关系评分。
- 做健康报告：孤岛、低内聚、桥接、冲突、低证据高引用。

第三阶段：

- 做 context pack generator。
- 再考虑本地 API/MCP。

第四阶段：

- 节点规模足够后，再考虑图谱可视化、Louvain、vector search。

## 当前结论

`llm_wiki` 是目前为止我们看过最有工程增量的资料。Orange Book 更像指南；`llm_wiki` 更像参考实现。

但现在要吸收“规则和最小可行机制”，不是复刻“完整产品形态”。
