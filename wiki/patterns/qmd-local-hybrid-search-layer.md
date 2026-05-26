---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - tobi/qmd
related_concepts:
  - source-verification-and-trust-model
  - evidence-backed-design-validation
  - verified-vault-api-for-agent-brain
  - second-brain-knowledge-graph
related_projects:
  - verified-vault
adoption_status: watch
tags:
  - search-layer
  - hybrid-retrieval
  - qmd
  - raw-recall
  - mcp
evidence_count: 3
confidence: high
negative_evidence:
  - full-app-overengineering-before-clean-markdown-vault
---

# 设计模式：QMD 本地混合检索层

## 一句话定义

当 vault 规模增长、`index.md` 定位开始吃力时，用 QMD 在本地提供 BM25 + 向量 + rerank 的全文检索层，帮助 Agent 找回 raw/wiki 中的相关片段。

## 它在我们架构里的位置

QMD 不是资料库核心，不是第二大脑本身，也不是结论判断器。

它属于搜索扩展层：

```text
raw 原始资料
  -> QMD 检索层：找片段、找原文、找跨分类线索
  -> wiki 编译层：摘要、概念、结构化知识
  -> claim / pattern / anti-pattern 验证层
  -> graph / index / health 关系层
  -> context pack / API 调用层
```

## 解决的问题

1. `index.md` 变长后，Agent 每次读 index 的成本变高，定位精度下降。
2. 跨分类查询时，index 的分类结构不一定能命中真实语义。
3. wiki 是编译产物，会丢失 raw 里的具体原话、案例、数字、细节。
4. 纯 grep 找不到语义相近但字面不同的内容。
5. 纯向量搜索对版本号、工具名、精确词不稳。

## 核心机制

- BM25：解决关键词、版本号、专有名词精确匹配。
- Vector search：解决语义相似但字面不同。
- Query expansion：扩展用户问题的表达方式。
- RRF fusion：合并多路检索结果。
- LLM reranking：对候选结果做最终相关性排序。
- CLI / MCP：让 Agent 可以直接调用。

## 来源证据

- Karpathy LLM Wiki gist 明确说：小规模时 index 文件够用，wiki 长大后需要真正搜索，qmd 是好选项。
- `tobi/qmd` README 描述 QMD 是本地 markdown 搜索引擎，包含 BM25、向量语义搜索、LLM reranking。
- QMD README 描述它支持 CLI、MCP、collection、context、`search/vsearch/query/get`。

## 标签与量化

- domain: knowledge_retrieval
- problem: scalable_vault_search
- maturity: emerging
- complexity: medium
- problem_fit: 4
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 4
- evidence_strength: 4
- reversibility: 5

## 交叉验证

- 相似来源：Karpathy optional CLI tools、llm_wiki local API/search、用户去年 Zilliz + 原文回溯设计。
- 历史项目影子：用户之前已设计“向量检索只做雷达，命中后回原始 Session 审计”。
- 支持证据：QMD 提供 hybrid query 和 MCP，适合作为 Agent search layer。
- 反例：资料库还很小时，上 QMD 会过早增加复杂度。

## 触发条件

满足任意两个再考虑引入：

- `raw + wiki` 文件超过 100-200 个。
- `index.md` 超过几百行，Agent 开始找错页面。
- 经常需要找 raw 中某个原话、例子、数字。
- 跨分类查询明显增多。
- Agent 检索 token 成本明显上升。

## 不适用场景

- 当前资料库还在结构打磨阶段。
- source / claim / pattern 模板还没稳定。
- 只是为了“看起来先进”。
- 想用 QMD 直接替代人工验证和 claim 沉淀。

## 融合建议

短期不安装、不接入核心架构。

先记录为中期候选：

```text
QMD = raw/wiki 搜索雷达
不是 truth layer
不是 claim layer
不是 gbrain
```

未来接入时，必须遵守：

1. QMD 返回的是候选片段。
2. Agent 必须回到原文上下文。
3. 重要结论必须写入 claim / pattern / anti-pattern。
4. context pack 必须带 source、confidence、verification_status。

## 阿尔法设计方向

真正的阿尔法不是“装 QMD”，而是：

```text
Compiled Knowledge + Local Hybrid Search + Source Audit
```

也就是：

- wiki 负责长期理解。
- QMD 负责找回遗漏细节。
- claim/pattern 负责确认结论。
- health/review 负责防漂移。

## 验证指标

- QMD 命中结果是否比 index/grep 更准。
- 是否能找回 raw 中未进入 wiki 的细节。
- 是否降低 Agent 检索 token。
- 是否仍然保持来源和验证状态清晰。
- 是否没有让未验证片段直接污染高置信知识。
