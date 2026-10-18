---
type: source
record_kind: source_card
status: source-captured
title: "deepset-ai/haystack"
source_id: github-deepset-ai-haystack-2026-06-07
source_uri: https://github.com/deepset-ai/haystack
source_url: https://github.com/deepset-ai/haystack
source_type: repository
author: deepset-ai
publisher: GitHub
published_at: 2019-11-14
updated_at: 2026-06-06
captured_at: 2026-06-07
captured_by: Codex
version_or_commit: 56b5dd335071a415a9998703eed1a53b4c2e8053
source_status: active
raw_location: raw/repos/2026-06-07-deepset-ai-haystack-source.md
processing_mode: source-intake-routing-github-scout
processing_level: medium
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: normal
review_owner: Codex
formalization_status: raw-only
topics:
  - metadata-routing
  - retrieval
entities:
  - Haystack
  - metadata filtering
  - pipelines
  - routers
  - tracing
aliases:
  - deepset-ai/haystack
projects:
  - VAKS
source_family: github_repo_workbench_scout
upstream_sources: []
verification_status: source_metadata_checked
tags:
  - github-scout
  - source-intake-routing
---

# 来源记录：deepset-ai/haystack

## 为什么收录

为 `source-intake-routing` 工作台调研。Haystack 对 VAKS 最有价值的是“metadata filtering、routers、pipeline tracing、document store 和 retriever 分离”这些运行层边界。

这张卡只记录来源，不代表 VAKS 采用 Haystack。

## 来源信息

- 作者/组织：deepset-ai
- 发布方：GitHub
- 原始链接：https://github.com/deepset-ai/haystack
- 版本 / commit：`56b5dd335071a415a9998703eed1a53b4c2e8053`
- commit time：2026-06-05T13:43:31Z
- GitHub pushed_at：2026-06-05T14:24:07Z
- stars captured：25467
- forks captured：2830
- default branch：main
- license：Apache-2.0
- source_status：active
- 采集方式：GitHub API metadata + raw file anchor inspection; no clone; no runtime execution.

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

## Source / Code Anchors

| Anchor | What exists | Why it matters for source-intake-routing | Boundary |
|---|---|---|---|
| `README.md:12-14` | Modular pipelines with explicit control over retrieval, routing, memory, generation. | Directly relevant to lane-aware retrieval. | Framework claim only. |
| `docs-website/docs/concepts/pipelines.mdx:13-19` | Pipelines can be non-linear and include decision components. | Good model for context pack builder as explicit pipeline. | Do not build heavy pipeline runtime yet. |
| `docs-website/docs/concepts/metadata-filtering.mdx:10-14` | Metadata attached at indexing; metadata router and query-time filters. | Strong support for metadata as retrieval filter. | Metadata is not authority/truth. |
| `docs-website/docs/development/tracing.mdx:14-18` | Traces document request flow and execution order. | Useful for query-run/context-pack trace. | Trace is diagnostic, not evidence support. |
| `docs-website/docs/concepts/document-store.mdx:10-14` | Document Store stores data for retrievers and is distinct from pipeline component. | Helps separate source store from pack builder. | Document store is derived/cache layer. |
| `docs-website/docs/pipeline-components/routers.mdx:10-15` | Routers route queries/documents based on conditions or document length. | Useful for route-based source intake and context pack inclusion. | Routers cannot override authority buckets. |

## 初步看点

- Haystack gives the cleanest language for VAKS metadata-routing: metadata filters and routers happen inside retrieval, not truth.
- Pipeline tracing maps well to query-run receipt and context-pack trace.
- Document Store distinction reinforces Markdown source-of-truth vs derived index/cache separation.

## 明显疑点

- 未 clone、未运行、未验证 current docs build.
- Haystack pipeline runtime is heavier than current sandbox.
- Need avoid turning pipeline/tracing docs into mandatory VAKS implementation stack.

## 可抽取 Candidate Points

- Metadata filtering belongs after authority/path-role hard filters and before ranking.
- Context pack builder should expose a trace of stages and selected lanes.
- Document store/index/cache remains derived; Markdown/source card wins on conflict.

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 准备把 `vaks-context-pack-builder-v0.ps1` 推进到 v1 query-run receipt.
- 需要比较 Haystack pipeline traces 与 VAKS refs-only trace policy.

## 下一步

进入 `source-intake-routing` GitHub scout candidate distillation。
