---
type: source
record_kind: source_card
status: source-captured
title: "run-llama/llama_index"
source_id: github-run-llama-llama-index-2026-06-07
source_uri: https://github.com/run-llama/llama_index
source_url: https://github.com/run-llama/llama_index
source_type: repository
author: run-llama
publisher: GitHub
published_at: 2022-11-02
updated_at: 2026-06-06
captured_at: 2026-06-07
captured_by: Codex
version_or_commit: 9aa5ee5cd2a1ecff6ffa2a8cd6af46b87af674b9
source_status: active
raw_location: raw/repos/2026-06-07-run-llama-llama-index-source.md
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
  - source-intake
  - context-pack
entities:
  - LlamaIndex
  - LlamaParse
  - IngestionPipeline
  - CitationQueryEngine
aliases:
  - run-llama/llama_index
  - LlamaIndex
projects:
  - VAKS
source_family: github_repo_workbench_scout
upstream_sources: []
verification_status: source_metadata_checked
tags:
  - github-scout
  - source-intake-routing
---

# 来源记录：run-llama/llama_index

## 为什么收录

为 `source-intake-routing` 工作台调研。LlamaIndex 的价值在于 source reader、parser、ingestion pipeline、router query engine、citation query engine 等组件边界，可帮助 VAKS 设计“检索工作台如何从 source route 到 context pack”。

这张卡只记录来源，不代表 VAKS 采用 LlamaIndex。

## 来源信息

- 作者/组织：run-llama
- 发布方：GitHub
- 原始链接：https://github.com/run-llama/llama_index
- 版本 / commit：`9aa5ee5cd2a1ecff6ffa2a8cd6af46b87af674b9`
- commit time：2026-05-29T21:52:59Z
- GitHub pushed_at：2026-06-04T16:59:44Z
- stars captured：49958
- forks captured：7520
- default branch：main
- license：MIT
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
| `README.md:11` | OSS framework plus Parse platform for OCR/parsing/extraction/indexing. | Good source hygiene / parser-stage reference. | Product framing only. |
| `README.md:45-47` | LlamaParse includes Parse, Extract, Index. | Suggests separating parsing/extraction/indexing stages. | Do not import product architecture wholesale. |
| `docs/api_reference/api_reference/ingestion/index.md:1-3` | IngestionPipeline and DocstoreStrategy API reference. | Candidate model for explicit ingestion pipeline component. | API surface only; no action basis. |
| `docs/api_reference/api_reference/readers/file.md:1-3` | File readers include CSV, Docx, Epub, Markdown, PDF, PPTX, XML, video/audio, etc. | Strong reference for source type routing. | Reader success is not truth support. |
| `docs/api_reference/api_reference/node_parsers/markdown.md:1-3` | MarkdownNodeParser. | Relevant to Markdown/Obsidian source handling. | Parser output remains raw/candidate. |
| `docs/api_reference/api_reference/query_engine/router.md:1-3` | RouterQueryEngine API reference. | Useful analogy for route-aware query pack builder. | VAKS authority buckets still decide inclusion. |
| `docs/api_reference/api_reference/query_engine/citation.md:1-3` | CitationQueryEngine API reference. | Useful for citation/clickback surface. | Citation is not evidence support. |

## 初步看点

- LlamaIndex 的最大借鉴不是 UI，而是组件边界：reader -> parser -> ingestion pipeline -> query/router -> citation surface。
- 这能帮 VAKS 把 source-intake-routing 拆成轻量 stages，而不是做一个黑箱 RAG。
- LlamaParse/OCR/extract/index 的阶段感适合放进 source hygiene，而不是 truth 层。

## 明显疑点

- 未 clone、未运行、未验证具体 API 行为。
- 组件很多，容易把 VAKS 拖向 SDK 依赖和复杂 pipeline。
- Citation query engine 相关思想需要继续和 Evidence Support Check 分开。

## 可抽取 Candidate Points

- source type readers / parsers 应进入 source-intake-routing 的 route map。
- context pack builder 可以借鉴 pipeline stages，但输出必须 refs-only / lane-labeled。
- Citation/clickback 是 UX，不是 support verdict。

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 准备实现 source route adapter 或 context pack builder v1。
- 需要比较 LlamaIndex pipeline 与 Haystack pipeline 的轻量化边界。

## 下一步

进入 `source-intake-routing` GitHub scout candidate distillation。
