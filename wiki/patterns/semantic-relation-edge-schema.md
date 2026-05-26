---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - internal-architecture-review
related_concepts:
  - second-brain-knowledge-graph
  - source-verification-and-trust-model
  - four-signal-graph-relevance
related_projects:
  - verified-vault
adoption_status: adapt
tags:
  - knowledge-graph
  - relation-schema
  - edge-strength
  - context-pack
evidence_count: 3
confidence: high
negative_evidence:
  - algorithmic-graph-scoring-without-source-quality
replaces:
superseded_by:
extension_points:
  - SCHEMA.md
  - health check
  - context pack ranking
  - future graph resolver
---

# 设计模式：语义关系边与关联强度

## 一句话定义

把 `[[链接]]` 升级成带方向、类型、强度、证据和理由的关系边，让资料库不只是卡片集合，而是一张可验证的有向知识图谱。

## 解决的问题

普通双链只能表达“有关联”，不能表达：

- 是支持、反驳、替代、风险还是实现？
- 关系强不强？
- 证据来自哪里？
- 这条边是否可信？
- 查询时哪条边应该优先进入 context pack？

对 verified knowledge system 来说，边的可信度和节点本身一样重要。

## 核心字段

每个高信号节点可以包含：

```yaml
relations:
  - target: "[[node-name]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[source-or-claim]]"
    rationale: "One sentence explaining why this edge exists."
    created: 2026-05-26
    last_verified: 2026-05-26
```

## 关系类型 v0.1

- `supports`: 支持某个 claim / pattern / decision。
- `contradicts`: 反驳或冲突。
- `refines`: 细化、收窄、改进。
- `replaces`: 替代旧方案或旧结论。
- `implements`: 某个 decision / project 实现某个 pattern。
- `applies_to`: 某个 claim / pattern 适用于某个 project。
- `derived_from`: 从某个 source / summary 提炼而来。
- `risk_of`: 某个 anti-pattern 是某个 pattern / decision 的风险。
- `alternative_to`: 互为备选方案。
- `blocked_by`: 被某个条件、风险或缺口阻塞。

## 强度规则

`strength: 1-5`

- `1`: 只是弱相关或背景提及。
- `2`: 有关联，但不是当前判断的关键依据。
- `3`: 中等关联，会影响理解。
- `4`: 强关联，是采用/拒绝的重要依据。
- `5`: 核心关系，没有这条边会误解节点。

## 为什么这不是过度设计

这不是引入新系统，而是让已有 Markdown 节点多一个结构化字段。

主记录保存的是人工/AI 判断出的语义边：

```text
type + target + strength + evidence + rationale
```

后续程序可以派生计算：

```text
source overlap
common neighbor
type affinity
vector score
graph score
```

语义关系是主记录，算法评分是派生层。

## 与向量检索的关系

向量检索不再是大脑，只是候选筛选器：

```text
query
  -> metadata / relation graph filter
  -> BM25 / vector candidate search
  -> relation strength ranking
  -> context pack with evidence / contradictions / gaps
  -> AI synthesis
```

## 反例与避坑

- 失败条件：AI 为了图谱好看给每个节点乱加强边。
- 相似反模式：algorithmic graph scoring without source quality。
- 复杂度风险：一开始就做图数据库、centrality、community detection。
- 替代方案：先用 `relations: []` 存主记录，后面用脚本生成图谱报告。

## 来源证据

- `llm_wiki` 提供四信号关系评分，验证了关系不应只靠双链。
- `nano-NotebookLM` 的 GraphRAG 说明检索时需要沿关系邻域扩展。
- gbrain 的 compiled truth / epistemology 层说明 claim、fact、take、decision 需要带证据和立场关系。

## 标签与量化

- domain: knowledge_graph
- problem: relation_semantics
- maturity: emerging
- complexity: low
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 2
- integration_fit: 5
- evidence_strength: 4
- reversibility: 5

## 最小实现方式

1. 在核心模板中加入 `relations: []`。
2. 在 `SCHEMA.md v0.1` 定义关系类型、强度、置信度和证据字段。
3. 手工为高信号 claim/pattern/decision 添加 1-5 条关系边。
4. 后续用脚本检查关系字段是否有效。
5. 再后续才计算 graph score 或输出 Obsidian/Bases/可视化视图。

## 验证指标

- context pack 是否能优先返回真正相关的节点。
- AI 回答是否更少把弱关联当强证据。
- 冲突关系是否更容易被发现。
- pattern 采纳时是否更容易看到支持证据和反模式风险。

