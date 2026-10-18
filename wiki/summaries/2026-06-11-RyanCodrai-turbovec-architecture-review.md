---
type: summary
status: draft
title: "turbovec architecture review for VAKS retrieval cache"
created: 2026-06-11
source:
  - raw/repos/2026-06-11-RyanCodrai-turbovec-source.md
source_repo: https://github.com/RyanCodrai/turbovec
source_commit: fcc1eb8e06c52764907b677128845995309219e0
related_patterns: []
related_decisions: []
confidence: medium
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
fusion_decision: adapt-after-sandbox
tags:
  - summary
  - architecture-review
  - candidate-only
  - retrieval-cache
  - vector-search
---

# turbovec 架构评审：VAKS 检索缓存候选

## 一句话判断

`turbovec` 是 VAKS 向量检索层的 **强候选**，适合先做 sandbox pilot。

它不该改变 VAKS 的知识边界：向量索引仍然只是可重建的检索缓存，不是 truth store、review authority、evidence support、reviewed relation 或 action basis。

## 它是什么

从仓库、PyPI、源码和文档看，它是一个 Rust core + Python bindings 的本地向量索引库：

```text
TurboQuant-style 2-4 bit vector compression
SIMD-oriented search
online add
persistent index files
stable external ID wrapper
allowlist / mask filtering at search time
LangChain / LlamaIndex / Haystack / Agno adapters
```

PyPI 最新包在 2026-06-11 检查为 `0.7.1`，并标记为 Alpha。

## 和 VAKS 当前架构的贴合点

### 1. 符合 derived cache 边界

VAKS 当前原则里，BM25/vector/GraphRAG/rerank 都是派生检索层。`turbovec` 正好可以放在这里：

```text
Markdown/YAML/raw source = authority
SQLite/BM25/metadata = filter and routing
turbovec = compressed dense rerank cache
review/evidence gate = support and action readiness
```

这个分层能避免向量库越权。

### 2. allowlist 比全库搜索更重要

VAKS 需要的不是“全库语义搜索越多越好”，而是：

```text
先排除不该进入当前回答/决策的内容
再在允许集合内排序
最后回到 source anchors
```

`turbovec` 的 allowlist search 对这个很有价值。它可以让 BM25、metadata、source_status、knowledge_status、project_scope、time window、permission bucket 先定边界，然后 dense search 只负责排序。

### 3. Stable ID wrapper 能接上 source/chunk identity

VAKS 不能把 vector slot 当长期 ID。`IdMapIndex` 这类稳定外部 ID wrapper 可以用来映射：

```text
source_id
source_hash
chunk_id
path
line/span
embedding_model_namespace
```

这对删除、更新、重建和审计都更友好。

## 不足与风险

```text
1. Alpha package status means dependency risk is real.
2. Self-published README benchmarks are not adoption evidence.
3. Local Windows performance was not tested in this intake.
4. VAKS Chinese/English mixed corpus may behave differently from OpenAI/GloVe benchmarks.
5. Compression may hurt subtle recall, especially at 2-bit.
6. Persistence format compatibility needs checking before cache is treated as durable.
7. Framework adapters are convenience only; they should not decide VAKS architecture.
```

## VAKS 融合位置

| Layer | Fit | Note |
|---|---:|---|
| Source Intake | Medium | Incremental add can index new chunks after source capture |
| Candidate Comprehension | Medium | Can find similar raw/candidate material |
| Review Queue | Indirect | Can surface possible collisions, not judge them |
| Association / Connect | Medium | Can find nearby anchors before reviewed relation traversal |
| Activation / Context Pack | High | Best fit: fast local context preparation |
| Dev Context | High | Helps development windows find local docs and prior reviews |
| Truth / Schema | No | No truth mutation, no confidence, no reviewed relation |
| Action Basis | No | Needs evidence envelope and review gate outside retrieval |

## Suggested Pilot Contract

```yaml
pilot_name: turbovec-vaks-retrieval-cache-pilot
scope: sandbox_only
input_corpus: 200-1000 representative VAKS markdown chunks
embedding_namespaces:
  - current_default_embedding_model
  - optional_chinese_friendly_model
baselines:
  - BM25 only
  - exact cosine on small corpus
  - BM25 allowlist -> turbovec rerank
metrics:
  - recall_at_5
  - recall_at_10
  - source_anchor_correctness
  - false_positive_review_pressure
  - memory_footprint
  - build_time
  - update_delete_time
  - Windows import/search stability
pass_gate:
  - returns correct source anchors for known queries
  - never mixes authority buckets without explicit allowlist
  - cache rebuild is deterministic enough for operational use
  - embedding model namespace invalidation is explicit
fail_action:
  - park as watch
  - keep BM25/simple local search as default
```

## Architecture Boundary

If adopted later, the rule should be:

```text
VAKS may use turbovec to find candidates.
VAKS must not use turbovec to decide truth.
```

Practical wording:

```text
Vector search is a flashlight.
Evidence review is the court.
```

## Current Recommendation

```yaml
recommendation: run_sandbox_pilot
borrow_value: strong
borrow_order: P1_for_retrieval_cache
mainline_adoption: no
schema_change: no
decision_record_needed_now: no
review_queue_needed_now: optional_after_pilot
```

