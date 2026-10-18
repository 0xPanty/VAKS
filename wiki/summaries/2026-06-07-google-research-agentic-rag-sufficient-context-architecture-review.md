---
type: library_review
status: draft
library_name: "Google Research Agentic RAG / Sufficient Context"
source_url: https://research.google/blog/unlocking-dependable-responses-with-gemini-enterprise-agent-platforms-agentic-rag/
reviewed_at: 2026-06-07
domain: agentic RAG, context sufficiency, cross-corpus retrieval
related_projects:
  - verified-action-knowledge-system
current_branch:
  - evidence-sufficiency
  - context-pack
  - known-omissions
  - retrieval-routing
  - action-basis-boundary
extracted_patterns:
  - sufficient-context-gate-before-generation
  - missing-context-feedback-loop
  - cross-corpus-retrieval-routing
  - sufficiency-signal-not-truth-confidence
  - agentic-rag-as-context-pack-assembly
fusion_decision: adapt
borrow_value: strong
confidence: medium
evidence_count: 8
cross_validated_with:
  - Google Research blog
  - Google Cloud retrieval-tool documentation
  - Google Research Sufficient Context article / OpenReview paper
negative_evidence:
  - vendor-reported performance claims
  - implementation details are product-specific
  - LLM-as-judge and internal evaluations cannot become VAKS benchmark authority
  - product docs must be rechecked before implementation
extension_potential: high
relations: []
tags:
  - google-research
  - agentic-rag
  - sufficient-context-agent
  - context-pack
  - evidence-sufficiency
  - known-omissions
  - strong-borrow
  - P1
  - candidate-only
---

# 架构评审：Google Research Agentic RAG / Sufficient Context

## 它解决什么问题

它解决的问题是：

```text
RAG 不是搜到东西就够了。
真正的问题是：搜到的 context 是否足够回答当前问题？
如果不够，缺的是哪一块？
应该继续搜哪里？
```

这是 VAKS 的核心痛点之一，因为 VAKS 不能让一个检索包自动变成 action basis。

## 核心设计

这篇文章里的关键机制可以压缩成：

```text
query understanding
-> retrieval / cross-corpus routing
-> context inspection
-> Sufficient Context Agent
-> missing-context feedback
-> follow-up retrieval
-> answer with enough context, or expose insufficiency
```

架构价值不在产品 API，而在控制点：

```text
Before final generation, inspect context sufficiency.
When insufficient, produce targeted missing-context requests.
Keep sufficiency separate from truth.
```

## 对 VAKS 的当前支线价值

当前支线：

```text
Evidence Sufficiency Gate / Context Pack / known omissions / retrieval routing
```

它对当前支线：

```text
strongly refines
```

具体价值：

- 把 `known omissions` 从静态清单变成检索循环里的可执行反馈。
- 把 `Evidence Sufficiency Gate` 具体化为 context-pack readiness check。
- 把 `Context Pack` 从“相关材料集合”提升为“足够回答当前问题的材料包”。
- 把跨 source/corpus 检索做成显式路由，而不是一个混合检索池。
- 把 sufficiency 和 truth confidence 分开，避免检索分数越权。

## VAKS 映射

| Google Agentic RAG | VAKS Mapping | Boundary |
|---|---|---|
| Query decomposition | Candidate task understanding | Not truth |
| Corpus selection | Source family / layer routing | Not source reliability |
| Retrieval snippets | Context-pack candidates | Not evidence support |
| Sufficient Context Agent | Evidence Sufficiency / omission gate | Not truth confidence |
| Missing-context feedback | Review queue / retrieve-more reason | Not automatic action |
| Iterative retrieval | Context-pack assembly loop | Not promotion |
| Final answer | Risk-scoped answer/action draft | Needs separate action gate |

## 值得提炼的模式

1. `sufficient-context-gate-before-generation`
2. `missing-context-feedback-loop`
3. `cross-corpus-retrieval-routing`
4. `sufficiency-signal-not-truth-confidence`
5. `agentic-rag-as-context-pack-assembly`

## 不值得照搬的部分

- Gemini Enterprise product dependency.
- Google vendor metrics as general benchmark proof.
- Any API/runtime choice before VAKS implementation requirements are set.
- Sufficiency labels as evidence support.
- Agentic retrieval as automatic review or promotion.

## Adoption Judgment

```yaml
fusion_decision: adapt
borrow_value: strong
borrow_order: P1
runtime_executed: false
promotion_status: none
```

人话：

```text
强，P1。
这篇补的是 VAKS 最难的门：上下文够不够支撑回答或行动。
但它只能作为候选架构参考，不能替代 evidence review，也不能直接成为 action basis。
```
