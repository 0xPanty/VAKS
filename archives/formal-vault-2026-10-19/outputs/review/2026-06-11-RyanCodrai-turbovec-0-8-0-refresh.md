---
type: candidate_distillation_refresh
status: draft
title: "turbovec 0.8.0 refresh：安全审计释放与 VAKS 检索层影响"
created_at: "2026-06-11"
created_by: Codex
processing_level: medium
processing_tier: medium
knowledge_status: candidate
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
  - outputs/review/2026-06-11-RyanCodrai-turbovec-candidate-distillation.md
  - wiki/summaries/2026-06-11-RyanCodrai-turbovec-architecture-review.md
  - raw/repos/_snapshots/2026-06-11-RyanCodrai-turbovec-1e7200c-source.zip
projects:
  - verified-action-knowledge-system
topics:
  - vector-search
  - retrieval-cache
  - local-rag
  - embedded-index
  - hybrid-retrieval
  - source-integrity
  - untrusted-cache-load
borrow_value: strong
borrow_order: P1_for_retrieval_cache_P2_for_dependency
evidence_strength: medium_for_design_low_for_vaks_runtime
current_upstream:
  checked_at: 2026-06-11
  repository_head: 1e7200cfd8f26c92ce2855652db64bc7f85bc039
  py_tag: py-v0.8.0
  pypi_version: 0.8.0
  pypi_uploaded_at: 2026-06-10T18:11:10
  pypi_sdist_sha256: 4ff24956ef159cd8ccdb19c561b07eea3c191c344a23368cd0adad9cdd87382c
  snapshot_sha256: 33fce609b3edfedeb7281415c6c56c4734ed23e9b285143be4234dc5438dd5a8
tags:
  - candidate-only
  - source-distillation-refresh
  - vector-search
  - retrieval-cache
  - source-integrity
---

# turbovec 0.8.0 Refresh

## 一句话

`turbovec` 的核心检索逻辑没有因为 0.8.0 改方向；它仍然是一个 **本地压缩向量索引 + allowlist dense rerank** 候选。

0.8.0 对 VAKS 最重要的新信号是：它开始认真补 **不可信索引文件加载、Python API 错误边界、集成层数据一致性**。这让它作为未来本地 cache 的候选更成熟一点，但仍然是 Alpha，不能直接变主线依赖。

## 它的检索能力主要逻辑

说人话：

```text
先把 embedding 压小
再直接在压缩后的码上算相似度
同时支持只在一批允许 ID 里搜索
```

更具体一点：

```text
1. Normalize:
   把向量长度拆出来，主要保留方向。

2. Random rotation:
   用同一个随机正交矩阵旋转所有向量，让坐标分布更可预测。

3. TQ+ calibration:
   用第一次 add 的数据做每个坐标的轻量校准，后续复用。

4. Scalar quantization:
   每个坐标压到 2-4 bit。

5. Bit-pack:
   把小整数打包，显著减少内存。

6. Length-renormalized scoring:
   给每个向量存一个校正标量，降低量化后的内积偏差。

7. SIMD search:
   查询时不解压全向量，而是在压缩码上用查表和 SIMD 打分。

8. Allowlist / mask:
   搜索时只在允许的 slot / external id 集合里打分，适合 hybrid retrieval。
```

## 跟 VAKS 的区别

`turbovec` 解决的是：

```text
给定一批向量，怎么更省内存、更快地找相似向量。
```

VAKS 解决的是：

```text
给定一个任务，哪些资料有资格参与回答，
哪些只是 raw/candidate，
哪些可以进 context pack，
哪些能不能作为 action basis。
```

所以两者不是同一层：

| 问题 | turbovec | VAKS |
|---|---|---|
| 找相似向量 | 强 | 需要借工具 |
| 压缩向量内存 | 强 | 不自己做 |
| 本地/离线检索 | 强 | 需要这种能力 |
| raw/candidate/reviewed 分桶 | 不负责 | 核心边界 |
| evidence support | 不负责 | review gate 负责 |
| action basis | 不负责 | action gate 负责 |
| 反馈是否改 truth | 不负责 | 明确禁止 |

## 0.8.0 对原蒸馏判断的影响

### 增强点

```text
untrusted .tv / .tvim load path hardening
malformed index file returns clean error
NaN / Inf / huge query values map to ValueError
dim capped to prevent resource exhaustion
integration wrappers fix duplicate/orphan/delete issues
JSON side-car mismatch now raises clean error
README benchmark figures corrected
```

这些点对 VAKS 很重要，因为如果以后我们把 `.tv/.tvim` 当可重建 cache，加载 cache 也必须走不可信输入边界。cache 是本地的，也不能默认安全。

### 不改变的点

```text
仍然是 Alpha
仍然需要 Windows 本机 smoke test
仍然需要 VAKS 中文/英文混合 corpus recall test
仍然不能把 benchmark 当采用证据
仍然不能让 vector score 变成 support / truth / action basis
```

## 可借鉴点

### 1. Bucket-filtered dense rerank

最值得借。

```text
VAKS 先用 retrieval_policy / project_scope / knowledge_status / BM25 / metadata 产出 allowed ids
-> turbovec 只在 allowed ids 里搜索
-> 返回 source/chunk anchors
```

这正好保留 VAKS 的强边界，同时提升语义排序。

### 2. Stable ID mapping

`IdMapIndex` 思路适合 VAKS：

```text
source_id / chunk_id / path_hash / source_hash
-> external uint64 id
-> vector slot
```

这样删除、更新、重建 cache 时，不会把 vector slot 当业务身份。

### 3. Cache-load threat model

0.8.0 的安全审计提醒我们：

```text
不要把本地 cache 当可信真源。
不要加载来路不明的 .tv/.tvim。
cache 文件要能重建，不能成为唯一知识来源。
cache mismatch 应该报错而不是静默返回。
```

### 4. Benchmark shape

它的 benchmark 分类可以借来做 VAKS pilot：

```text
compression
recall
speed
filter selectivity
update/delete behavior
cross-platform smoke
```

## 最终判断

```yaml
fusion_decision: adapt-after-sandbox
borrow_value: strong
borrow_order: P1_for_retrieval_cache_P2_for_dependency
direct_use_now: no
mainline_dependency_now: no
best_next_step: VAKS retrieval pilot
```

说人话：

```text
turbovec 是一个很值得借的检索加速器。
它不是 VAKS 的检索治理系统。
我们可以借它的压缩索引、allowlist rerank、稳定 ID 和 cache 安全边界。
但 VAKS 的核心仍然是：先分桶、先看资格、再排序、最后再审查能不能用。
```

