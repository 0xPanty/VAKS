---
type: source
record_kind: source_card
status: source-captured
title: "Kwipu"
source_id: "repo:benmaster82/Kwipu@908f0e4e300578a22c5fadd4538f75ff7ccfc0b6"
source_uri: "github:benmaster82/Kwipu@908f0e4e300578a22c5fadd4538f75ff7ccfc0b6"
source_url: "https://github.com/benmaster82/Kwipu"
source_type: repository
author: "benmaster82"
publisher: GitHub
published_at: unknown
updated_at: "2026-06-13T20:39:57Z"
captured_at: "2026-06-14"
captured_by: Codex
version_or_commit: "908f0e4e300578a22c5fadd4538f75ff7ccfc0b6"
source_integrity:
  source_hash: null
  snapshot_hash: "sha256:365B39C54CDEB0D09C0817F806B95672B0E93F08BFFF3C1391C8AC10D3A9FD6A"
  ingest_state: new
adapter_ingest:
  adapter_name: "manual-github-review"
  adapter_version: "2026-06-14"
  capture_method: "GitHub repo page, GitHub API metadata, local shallow clone, source reads, and commit zip snapshot"
  extraction_trace:
    - "GitHub repo page opened"
    - "GitHub API repo metadata checked"
    - "git clone --depth 1 https://github.com/benmaster82/Kwipu.git"
    - "git archive commit snapshot"
    - "manual source inspection"
  known_limits:
    - "Repository was not executed as a full runtime because this machine reports Python 3.10.6 while README requires Python 3.11+."
    - "Ollama models and LlamaIndex dependencies were not installed for runtime testing."
    - "No dedicated upstream test suite was found in the repository."
    - "GitHub issues and discussions were not exhaustively reviewed."
source_status: active
raw_location: "raw/repos/_snapshots/2026-06-14-benmaster82-Kwipu-908f0e4e3005-source.zip"
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: review_due
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
why_saved: "User asked to strongly distill Kwipu and place it into the VAKS architecture research plan."
topics:
  - local-graph-rag
  - obsidian
  - markdown
  - hybrid-retrieval
  - mcp
  - derived-cache
projects:
  - verified-action-knowledge-system
source_family:
  - graph-rag
  - retrieval-sidecar
  - obsidian-plugin-reference
  - mcp-query-tool
upstream_sources:
  - "https://github.com/benmaster82/Kwipu"
verification_status: source_identity_checked
candidate_relation_suggestions:
  - target: "outputs/review/2026-06-14-benmaster82-Kwipu-strong-distillation.md"
    relation_type: derived_from
    relation_state: candidate
    why_suggested: "Strong distillation extracts local Obsidian Graph RAG and read-only MCP lessons from this repository."
    suggested_at: "2026-06-14"
tags:
  - source
  - repository
  - candidate-only
  - kwipu
  - graph-rag
  - obsidian
  - mcp
---

# 来源记录：Kwipu

## 为什么收录

用户给出：

```text
[benmaster82/Kwipu](https://github.com/benmaster82/Kwipu) 强蒸馏这个然后记得放进总调研方案里
```

这个仓库贴近 VAKS 的两个现实方向：

```text
1. 本地 Obsidian / Markdown vault 如何做图检索和混合检索。
2. 如何通过一个很薄的 MCP read-only tool 给 agent / MISA 查资料。
```

它不适合作为 VAKS 的权威层，但适合当作：

```text
derived retrieval cache / local graph RAG sidecar / read-only MCP query reference
```

## 来源信息

- 作者：benmaster82
- 发布方：GitHub
- 原始链接：https://github.com/benmaster82/Kwipu
- 版本 / commit：`908f0e4e300578a22c5fadd4538f75ff7ccfc0b6`
- commit time：`2026-05-18T16:20:42+02:00`
- commit subject：`Add MCP badge`
- 默认分支：`main`
- GitHub API：未归档；license `MIT`；stars `216`；forks `30`；open issues `1`；updated `2026-06-13T20:39:57Z`
- 本地快照：`raw/repos/_snapshots/2026-06-14-benmaster82-Kwipu-908f0e4e3005-source.zip`
- 快照 SHA256：`365B39C54CDEB0D09C0817F806B95672B0E93F08BFFF3C1391C8AC10D3A9FD6A`

## Intake Boundary

```yaml
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: review_due
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

This source record is provenance and findability only. It does not adopt Kwipu, does not approve runtime use, and does not make extracted graph triples reviewed relations.

## Inspected Repository Areas

| Anchor | What exists | VAKS extraction | Boundary |
|---|---|---|---|
| `README.md:22-45` | MCP server, incremental updates, storage integrity, property graph index, wikilink/frontmatter parsing, hybrid retrieval, local Ollama. | Confirms strong fit as local retrieval sidecar reference. | README claims are not runtime evidence. |
| `README.md:104-134` | Pipeline diagram: notes -> pre-processing -> LLM extraction -> property graph -> hybrid retrieval -> LLM response. | Useful minimal local Graph RAG architecture. | Does not include VAKS authority buckets. |
| `README.md:223-230` and `CONTRIBUTING.md:27-47` | Upstream asks for retriever attribution logging, eval set, provenance inspector, and still mentions old incremental-update gap. | Direct evidence that Kwipu lacks several VAKS-grade receipts/provenance controls. | Roadmap text may be stale. |
| `requirements.txt:1-7` | LlamaIndex, Ollama, watchdog, MCP, Rich, PyYAML. | Small dependency map for sandbox planning. | Dependencies not installed locally. |
| `geode_graph.py:88-113` | Config, Ollama LLM/embedding initialization, chunk size. | Model/runtime config sidecar. | Default model `gpt-oss:20b-cloud` needs locality review. |
| `geode_graph.py:114-145` | Anti-hallucination prompt requiring context-only answers and file citations. | Useful answer prompt discipline. | Prompt rules are not evidence support or action readiness. |
| `geode_graph.py:165-267` | Custom multilingual BM25 chunk retriever. | Keyword recall layer. | BM25 score is activation only. |
| `geode_graph.py:271-337` | Temporal/metadata retriever with dates, tags, proper names. | Good reference for temporal query route. | Temporal hit is not applicability review. |
| `geode_graph.py:340-372` | Read/write lock around index updates and queries. | Useful runtime safety for local cache. | Runtime lock is not authority control. |
| `geode_graph.py:373-565` | YAML frontmatter parser, Obsidian wikilink triple extraction, multilingual relation inference, structural triple dedupe. | Strong candidate_relation_suggestion reference. | Extracted triples cannot become reviewed relations. |
| `geode_graph.py:566-746` | Load/build index, embedding-model manifest, incremental insert/update with delete+reinsert fallback. | Derived cache lifecycle and model mismatch check. | Cache freshness is not truth freshness. |
| `geode_graph.py:747-848` | Structural triples injected into PropertyGraphIndex; LLM path extraction; graph persistence. | Graph-index construction reference. | LLM extraction remains candidate-only. |
| `geode_graph.py:860-935` | Normal mode adds LLM synonym retriever; fast mode uses vector + BM25 + temporal; query engine composed from sub-retrievers. | Retrieval-strata implementation reference. | Needs retrieval receipt and authority bucket filter. |
| `geode_graph.py:947-1110` | Watchdog file watcher, content MD5 cache, debounce, incremental update, delete triggers full rebuild. | Useful derived-cache invalidation pattern. | MD5 is okay for change detection but not VAKS provenance hash. |
| `geode_graph.py:1113-1228` | Startup validation for Ollama/model availability and CLI model override. | Good runtime UX reference. | Runtime readiness is not answer support. |
| `lang_config.py:1-424` | Multilingual stopwords, temporal keywords, relation patterns, tokenization, language detection. | Borrowable as query/tokenization idea. | Current language set lacks Chinese/Japanese/Korean. |
| `kwipu_mcp_server.py:36-87` | FastMCP server with one `query_graph(question)` tool and lazy RAG instance. | Strong thin read-only MCP entry reference. | No write tools; keep it that way for VAKS/MISA until receipts exist. |
| `knowledge_base/examples/*.md` | Example Obsidian-like notes with frontmatter, wikilinks, dates, participants, tasks. | Shows intended source shape. | Toy examples, not benchmark. |

## 初步看点

Kwipu 是一个很小的本地图检索系统：

```text
Markdown / Obsidian notes
-> frontmatter + wikilink structural triples
-> LLM triplet extraction
-> LlamaIndex PropertyGraphIndex
-> vector + BM25 + temporal + optional synonym retrieval
-> cited LLM answer
-> optional MCP query tool
```

对 VAKS 最有价值的是：

```text
本地可拆 retrieval sidecar + read-only MCP query tool
```

不是：

```text
review engine
truth engine
action-basis engine
reviewed relation graph
```

## 明显疑点

- 没有 VAKS 的 authority bucket filter。
- 没有 retrieval receipt：无法追踪哪个 retriever 选中了哪些内容、哪些 bucket 被排除。
- 没有 support check：答案引用文件名不等于证据支持。
- 没有 action readiness：回答能生成不代表可以行动。
- 自动抽取的 triples 容易被误当成 reviewed relations。
- 默认模型名包含 `gpt-oss:20b-cloud`，和 fully local 叙述之间需要运行配置复核。
- 使用 MD5 做内容变化检测可接受，但 VAKS provenance/hash 应使用 SHA256。
- 没有测试套件；本地只做了 `py_compile`，未跑完整 runtime。
- 文档存在轻微漂移：README 前面说修改文件已增量更新，贡献文档还把它列成待办。

## 可抽取 Candidate Points

1. Kwipu can be a strong reference for a VAKS local Obsidian Graph RAG retrieval sidecar.
2. Obsidian wikilinks and frontmatter can produce candidate graph fragments, but must not create reviewed relations.
3. Hybrid retrieval should combine vector/BM25/temporal/synonym routes only behind authority buckets and retrieval receipts.
4. File watcher + content hash + embedding-model manifest is useful for derived-cache lifecycle.
5. Thin MCP should expose read-only query first; write tools require operation receipts, permission tiers, and review gates.
6. Prompt-level anti-hallucination is useful answer discipline but not enough for evidence support or action readiness.

## 当前处理等级

```text
heavy source review, candidate only
```

升级条件：

- User asks to build a local VAKS retrieval sidecar or MISA read-only VAKS query tool.
- P0/P1 retrieval/operation receipt validators exist.
- A sandbox can prove graph/vector/BM25/temporal hits are receipt-labeled and cannot become support without anchors.
- Chinese-heavy vault performance and relation extraction quality are tested.

## 下一步

Read:

- `outputs/review/2026-06-14-benmaster82-Kwipu-strong-distillation.md`
- `wiki/summaries/2026-06-14-benmaster82-Kwipu-architecture-review.md`
- `outputs/review/project_lens_overlays/2026-06-14-benmaster82-Kwipu-vaks-local-graph-rag-overlay.md`

