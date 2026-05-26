---
type: source
status: source-captured
title: garrytan/gbrain
source_url: https://github.com/garrytan/gbrain
source_type: repo
author: garrytan
publisher: GitHub
published_at:
captured_at: 2026-05-26
captured_by: Codex
topics:
  - second-brain
  - knowledge-engine
  - retrieval
  - epistemology
  - graph
projects:
  - verified-knowledge-system
evidence_level: primary
source_status: source-captured
source_quality: 4
freshness: 5
relevance: 5
confidence: 4
cross_source_count: 1
verified_by:
  - local-source-read
last_verified: 2026-05-26
next_review:
related_claims:
related_concepts:
  - verified-knowledge-system
  - compiled-truth
  - epistemology-layer
tags:
  - repo
  - gbrain
  - architecture-reference
---

# 来源记录：garrytan/gbrain

## 为什么收录

用户提供 `garrytan/gbrain` 和关于 8 层 RAG / knowledge engine 的截图，要求判断它作为 agent 第二大脑是否有可借鉴之处。

它和当前资料库目标高度相关：不仅讨论检索，还明确包含 facts/takes、compiled truth、entity linking、schema packs、dream cycle、system of record 等设计。

## 核心内容

gbrain 不是普通 RAG 示例，而是一个面向个人/团队 brain 的知识引擎。它把 Markdown brain repo 作为 system of record，把 DB、向量索引、搜索缓存和图谱边作为派生索引，并通过 `think` / `dream cycle` 把检索、证据、判断和维护串起来。

## 来源信息

- 仓库：`https://github.com/garrytan/gbrain`
- 当前读取 commit：`32f8be96c2409b8ccd35b7835692fd56b640f5c4`
- 本地临时目录：`C:\Users\Administrator\AppData\Local\Temp\gbrain_probe\gbrain`
- 本地源码快照：`raw/repos/_snapshots/gbrain-32f8be96c2409b8ccd35b7835692fd56b640f5c4.zip`
- 采集方式：Git clone 后读取 README、docs、核心 TypeScript 源码。

## 已读取重点

- `README.md`
- `docs/guides/brain-vs-memory.md`
- `docs/guides/compiled-truth.md`
- `docs/designs/KNOWLEDGE_RUNTIME.md`
- `docs/architecture/RETRIEVAL.md`
- `docs/architecture/schema-packs.md`
- `docs/takes-vs-facts.md`
- `docs/architecture/system-of-record.md`
- `skills/RESOLVER.md`
- `src/core/vector-index.ts`
- `src/core/contextual-retrieval-service.ts`
- `src/core/think/index.ts`
- `src/core/think/gather.ts`
- `src/core/search/hybrid.ts`
- `src/core/search/query-intent.ts`
- `src/core/search/expansion.ts`
- `src/core/search/rerank.ts`
- `src/core/search/graph-signals.ts`
- `src/core/chunkers/recursive.ts`
- `src/core/chunkers/code.ts`
- `src/core/facts/extract.ts`
- `src/core/cycle.ts`
- `src/core/cycle/phases/consolidate.ts`
- `src/core/cycle/synthesize.ts`
- `src/core/cycle/patterns.ts`
- `src/core/schema-pack/base/gbrain-base.yaml`

## 标签与量化

- source_type: repo
- evidence_level: primary
- source_status: source-captured
- source_quality: 4
- freshness: 5
- relevance: 5
- confidence: 4
- cross_source_count: 1

## 已验证内容

- README / docs / 源码都支持：gbrain 明确采用 Markdown 为 canonical source，DB/index/cache 为派生层。
- 检索不是单一向量：包含 BM25、vector、RRF、query intent、query expansion、reranker、graph signals、token budget、semantic query cache。
- facts / takes 是独立 epistemology 层：turn fact 是热记忆，take 是冷判断，并记录 kind、holder、weight、time/source 等字段。
- dream cycle 不只是总结：它包含 lint、backlinks、sync、extract、patterns、consolidate、embed、orphans、schema-suggest 等维护阶段。

## 未验证内容

- README / docs 中的 benchmark 和效果数字没有独立复现实验。
- 其生产规模、真实用户体验、长期维护成本未验证。
- 截图中的部分表述属于宣传性总结，需要以当前源码为准。

## 冲突或疑点

- gbrain 体量很大，直接 fork 或照搬会把当前资料库从 schema 设计带偏到完整 agent runtime。
- 它的 page type / link type 默认更偏个人/团队 brain，不等同于我们需要的 source / claim / pattern / anti-pattern / decision。
- 它有 DB、MCP、OAuth、minions、scheduler 等产品层，当前阶段过重。

## 可复用点

- Markdown system of record + derived indexes。
- compiled truth + append-only timeline。
- facts / takes / bet / hunch 的 epistemology 结构。
- schema pack / schema version 对缓存和检索的隔离。
- gather -> synthesize -> citations -> gaps 的 answer engine。
- dream cycle 作为周期性健康检查和知识沉淀机制。

## 下一步

短期不实现 gbrain runtime，只把高信号设计压缩进本资料库的 `SCHEMA.md`、晋级流程、验证门槛、关系类型和健康检查。

