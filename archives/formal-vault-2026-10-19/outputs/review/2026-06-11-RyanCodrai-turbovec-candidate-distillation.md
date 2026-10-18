---
type: candidate_distillation
status: draft
title: "turbovec：本地压缩向量索引与 allowlist rerank"
created_at: "2026-06-11"
created_by: Codex
processing_level: heavy
processing_tier: heavy
knowledge_status: candidate
overlay_state: project_sidecar_created
review_pressure: local_benchmark_required
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_and_local_benchmark_required
action_basis_allowed: false
truth_mutation_allowed: false
derived_from:
  - raw/repos/2026-06-11-RyanCodrai-turbovec-source.md
  - raw/repos/_snapshots/2026-06-11-RyanCodrai-turbovec-fcc1eb8-source.zip
  - wiki/summaries/2026-06-11-RyanCodrai-turbovec-architecture-review.md
  - outputs/review/project_lens_overlays/2026-06-11-turbovec-vector-retrieval-cache.md
projects:
  - verified-action-knowledge-system
topics:
  - vector-search
  - retrieval-cache
  - local-rag
  - embedded-index
  - hybrid-retrieval
  - context-pack-preparation
  - derived-cache
  - evidence-boundary
borrow_value: strong
borrow_order: P1_for_retrieval_cache_P2_for_dependency
evidence_strength: medium_for_design_low_for_vaks_runtime
tags:
  - candidate-only
  - source-distillation
  - github
  - pypi
  - vector-search
  - retrieval-cache
  - design-only
---

# 候选蒸馏：turbovec

## 一句话

`turbovec` 对 VAKS 的向量检索 **有帮助，而且是强相关**，但它现在应该进
`retrieval/cache` 的候选实验，不应该直接进主干依赖或 truth layer。

说人话：它像一个很省空间的本地向量索引。对我们有用的不是“它比所有向量数据库都强”，而是它刚好贴 VAKS 的几个需要：本地、轻、可增量、可持久化、能用稳定 ID、还能先用 BM25/SQL/权限/时间窗口筛一批候选，再只在这些 ID 里做 dense rerank。

## 对 VAKS 的主要价值

### 1. 本地 derived vector cache，而不是新的 truth store

VAKS 已经有明确边界：

```text
Markdown/YAML = 权威文本与结构
retrieval/cache = 可重建的派生层
vector score = activation signal, not truth
```

`turbovec` 正好适合放在第二行。它可以作为本地压缩向量缓存，帮助查询和 context pack 找候选材料，但不能决定 claim 是否成立。

### 2. allowlist search 很适合 VAKS 的桶内 rerank

它支持 search-time allowlist / mask。这个点比“压缩率”还贴我们。

VAKS 可以这样用：

```text
query
  -> SQLite / metadata / BM25 / authority bucket 先筛 ID
  -> turbovec 只在 allowlist 内 dense rerank
  -> 返回 source/chunk anchors
  -> 仍由 review/evidence gate 判断能不能当 support 或 action basis
```

这避免了一个常见问题：向量索引全库乱捞，把未审、候选、raw、过期、权限外内容混在一起。

### 3. IdMapIndex 对 Markdown chunk ID 很友好

VAKS 后续如果切 chunk，可以用稳定外部 ID 映射：

```text
source_id / chunk_id / path_hash / source_hash
  -> external u64 id
  -> turbovec slot
```

这样删除、更新、重建 cache 时不需要把向量槽位当成长期语义 ID。

### 4. Online ingest 适合增量 intake，但要测更新行为

它主打无训练、无 rebuild、在线 add。这对 VAKS 的日常 source intake 很香：

```text
新增 source/candidate note
  -> 生成 embedding
  -> append/update vector cache
```

但这里不能直接相信 README。需要实际测：

```text
不同写入顺序是否影响召回
remove/upsert 后 ID 映射是否稳定
embedding 模型切换后 cache 是否能干净失效
```

### 5. 压缩带来的意义是“本地可跑”，不是“更可信”

2-4 bit 压缩可能让 10 万到千万级向量在本机内存里更舒服。对 VAKS 的意义是：

```text
privacy: 不必把 vault 内容送到托管向量库
cost: 不先引入重型向量数据库
portability: repo/vault 可以带着 cache 或重建 cache
latency: context pack 准备更快
```

但压缩不提高 truth confidence。它只改变 retrieval 的成本和速度。

## 候选知识点

### Candidate Point 1: embedded compressed vector cache

VAKS 可以优先试一个 embedded vector cache，而不是先上 heavy vector database。

```yaml
status: candidate
borrow_value: strong
fit_layer: Retrieval / cache
not_fit_layer: Reviewed knowledge / truth / decision
needed_evidence:
  - local Windows import/search smoke test
  - VAKS corpus recall comparison
  - rebuild/update/delete behavior test
```

### Candidate Point 2: bucket-filtered dense rerank

最值得借的是 allowlist 模式。

```text
BM25 / metadata / authority bucket decides where search is allowed.
Vector search ranks only inside that allowed set.
```

这和 VAKS 的边界一致：先守边界，再排序。

### Candidate Point 3: stable ID wrapper

`IdMapIndex` 的设计可以对应到 VAKS 的 source/chunk ID，不让 vector slot 泄漏成业务 ID。

### Candidate Point 4: benchmark scripts are useful as test shape, not proof

它的 benchmark 脚本有参考价值：compression、recall、speed 分开测。但这些结果在 VAKS 里只能当“测试模板”，不能当采用证据。

## 对 VAKS 的具体映射

| VAKS 区域 | 可借鉴点 | 不要越界 |
|---|---|---|
| Capture | 新 source 写入后增量 embedding/index | source 入库不等于可用作支持 |
| Understand | dense retrieval 帮助找相似 candidate material | 相似不等于理解正确 |
| Review | 找同题材、反例、旧结论辅助 review | vector hit 不是 evidence support |
| Connect | relation-neighborhood 前先找 source/chunk seeds | 自动相似关系不是 reviewed relation |
| Activation | hot/warm/cold context pack 准备可用向量召回 | activation tier 不是 truth tier |
| Dev Context | 为开发窗口快速找相关 docs/code notes | dev context 不是 action basis |
| Feedback | 可记录 query-run 召回好坏用于后续调参 | 用户说“好用”不改变 claim confidence |

## Borrow Gradient

```yaml
borrow_value: strong
borrow_order: P1_for_retrieval_cache_P2_for_dependency
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "task is specifically about VAKS retrieval cache, local vector search, context-pack preparation, or source/chunk ranking"
  support_when: "designing BM25+vector hybrid search, allowlist dense rerank, local/offline RAG, or embedding cache invalidation"
  risk_when: "someone proposes vector score as truth, evidence support, reviewed relation, adoption proof, or action basis"
  cold_references:
    - raw/repos/2026-06-11-RyanCodrai-turbovec-source.md
    - raw/repos/_snapshots/2026-06-11-RyanCodrai-turbovec-fcc1eb8-source.zip
    - wiki/summaries/2026-06-11-RyanCodrai-turbovec-architecture-review.md
```

## 不要借鉴

- 不要把 `turbovec` 变成 VAKS 的知识权威。
- 不要把 README benchmark 当作独立证据。
- 不要把 GitHub stars 当成 adoption proof。
- 不要因为它支持 LangChain/LlamaIndex 就倒逼 VAKS 选框架。
- 不要跳过 BM25/metadata/authority bucket，直接全库向量搜索。
- 不要把 vector similarity 自动写成 reviewed relation。
- 不要现在就加入主干依赖；先做 sandbox pilot。

## 最小实验建议

先做一个很小的 VAKS retrieval pilot：

```text
input:
  200-1000 representative markdown chunks
  mixed Chinese/English queries
  known source/claim target pairs

compare:
  BM25 only
  exact cosine small baseline
  BM25 -> turbovec allowlist rerank
  optional BM25 + vector RRF

measure:
  recall@5 / recall@10
  source anchor correctness
  memory footprint
  build/update/delete time
  Windows import/search stability
  cache invalidation on embedding model change
```

Gate:

```text
If pilot passes, use as derived retrieval cache.
If pilot fails, keep BM25/simple local search and park turbovec as watch.
In either case, do not treat retrieval score as support or truth.
```

## 融合判断

```yaml
fusion_decision: adapt-after-sandbox
direct_use: no
fork: no
design_only_now: yes
schema_change: no
current_branch_value: high_for_retrieval_cache_design
whole_architecture_value: medium_high
implementation_evidence: medium_from_source_low_from_local_vaks
action_readiness: not_ready
mainline_dependency_readiness: not_ready
```

