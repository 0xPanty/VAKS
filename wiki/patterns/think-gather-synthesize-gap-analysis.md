---
type: pattern
status: draft
created: 2026-05-26
source_libraries:
  - garrytan/gbrain
related_concepts:
  - verified-vault-api-for-agent-brain
  - local-verified-vault-api
related_projects:
  - verified-knowledge-system
adoption_status: watch
tags:
  - context-pack
  - synthesis
  - citations
  - gaps
evidence_count: 1
confidence: high
negative_evidence:
replaces:
superseded_by:
extension_points:
  - context-pack
  - local-api
  - answer-engine
---

# 设计模式：Gather -> synthesize -> citations -> gaps

## 一句话定义

回答问题时不要只返回搜索结果，而是先聚合多路证据，再生成带引用和缺口说明的综合答案。

## 解决的问题

普通检索把片段塞进 prompt，容易漏掉反例、时间变化和不同来源的立场差异。verified knowledge system 需要回答“我们知道什么、不知道什么、证据在哪”。

## 适用场景

- future API / context pack。
- agent 需要调用资料库回答架构问题。
- claim / pattern / decision 需要跨多个来源综合。

## 不适用场景

- 单文件查找。
- 当前手工资料整理早期，不需要马上实现。

## 反例与避坑

- 失败条件：LLM 直接综合但不暴露 evidence/gaps。
- 相似反模式：把所有 top-k 片段塞进 prompt。
- 复杂度风险：过早接入 reranker、graph walk、token budget、cache。
- 替代方案：短期用人工读取 index + source + summary。

## 来源证据

- gbrain `src/core/think/gather.ts` 聚合 hybrid page search、takes keyword、takes vector、graph walk 四路证据。
- gbrain `src/core/think/index.ts` 将 pages、takes、graph evidence 渲染给 LLM，输出 answer、citations、gaps。
- gbrain `docs/architecture/RETRIEVAL.md` 描述 vector + BM25 + RRF + graph traversal + rerank + token budget。

## 标签与量化

- domain: retrieval-synthesis
- problem: grounded-answer
- maturity: emerging
- complexity: high
- problem_fit: 4
- reuse_value: 5
- implementation_cost: 5
- integration_fit: 4
- evidence_strength: 4
- reversibility: 3

## 交叉验证

- 相似来源：llm_wiki local API / context pack，nano-NotebookLM GraphRAG。
- 支持证据：用户中期目标是给 agent 调用 verified vault。
- 反例：当前节点太少时实现完整 answer engine 没收益。

## 最小实现方式

先定义未来 context pack 输出：

```text
answer:
citations:
supporting_claims:
contradicting_claims:
unknowns_or_gaps:
confidence:
next_verification:
```

等资料量上来再接混合检索。

## 项目融合建议

作为中期 API 形态记录，当前不写代码。

## 验证指标

- 每个 answer 都能追溯到 source/claim/pattern。
- gaps 明确列出没有证据、证据冲突或过期的位置。
- agent 不能把 single-source 结论伪装成 high-confidence decision。

