---
type: candidate_distillation
status: candidate_only
created_at: 2026-06-06
scope: TruLens + Haystack + LlamaIndex + Elastic -> VAKS retrieval/query/query-run contract
truth_boundary: candidate points only; not reviewed knowledge; not architecture decision; not action basis
source_refs:
  - raw/articles/2026-06-06-trulens-feedback-rag-triad-source.md
  - raw/articles/2026-06-06-haystack-tracing-source.md
  - raw/articles/2026-06-06-llamaindex-citation-query-engine-source.md
  - raw/articles/2026-06-06-elastic-rrf-source.md
---

# RAG Eval / Tracing / Citation / RRF Batch Candidate Distillation

## Chain

This file tests the VAKS flow:

```text
official docs batch
-> source records
-> source extraction
-> candidate points
-> retrieval candidate index
-> later design review
```

Boundary:

```text
This is candidate distillation.
It does not create reviewed claims, reviewed patterns, or action basis.
```

## 人话总判断

这四个源合在一起，补的是 VAKS 检索层的“运行可解释性”：

```text
TruLens:
  检索上下文相关、回答是否贴上下文、回答是否回答问题，要分开看。

Haystack:
  pipeline 过程要能 trace，但内容追踪默认应该关，避免把敏感内容丢进后台。

LlamaIndex:
  citation 不是最后随手贴括号，而应是检索后一个显式工作流阶段。

Elastic RRF:
  多路召回融合最好先按排名融合，不要硬混 BM25 / dense / sparse 的原始分数。
```

对 VAKS 的直接设计收益是：

```text
query-run receipt 要记录运行链路
pack item 要保留 selector / source number / citable status
RRF/rerank/eval score 都只能是 activation or diagnostic
action-facing claim 仍然要回 source anchor + warrant + gap/risk
```

## Source 1: TruLens Feedback / RAG Triad

### What The Source Says

TruLens 的 RAG Triad 把 RAG app 的评估拆成：

```text
context relevance
groundedness
answer relevance
```

它还在 API reference 中提供 groundedness 相关函数，用 `source` 和 `statement`
检查 statement 中的句子是否被 source material 支持，并返回 score + reasons。

### VAKS-Relevant Extraction

VAKS 应借：

```text
1. query-run receipt 里把 diagnostics 拆开：
   context_relevance_diagnostic
   groundedness_diagnostic
   answer_relevance_diagnostic

2. groundedness 应更接近 claim/sentence 级检查：
   不要只问“整个回答有没有引用”，要问“这句话是否由这段材料支撑”。

3. evaluator reasons 有价值：
   reasons 可以帮助 reviewer 找问题。
```

VAKS 不应借：

```text
groundedness score -> truth confidence
LLM judge -> promotion reviewer
triad satisfactory -> action-ready
retrieved context support -> world correctness
```

### Candidate Point

```yaml
candidate_id: cp-trulens-rag-triad-diagnostic-separation
point_text: "RAG/query evaluation should separate context relevance, groundedness, and answer relevance diagnostics."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: rationale_check
source_ref: raw/articles/2026-06-06-trulens-feedback-rag-triad-source.md
source_anchor:
  url: https://www.trulens.org/getting_started/core_concepts/rag_triad/
  section: "The RAG Triad"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

## Source 2: Haystack Tracing

### What The Source Says

Haystack 支持 tracing backends，包括 OpenTelemetry 和 Datadog。它也支持 content tracing，即记录 pipeline components 的输入输出值。

关键边界是：

```text
content tracing is disabled by default
because sensitive user information might be sent to tracing backend
```

### VAKS-Relevant Extraction

VAKS 应借：

```text
1. query-run receipt 是 trace shape：
   stage, inputs refs, outputs refs, warnings, latency, fallback, selected items.

2. 内容追踪默认关：
   query-run receipt 默认只保存 refs / selectors / hashes / warnings。
   要保存 snippet / prompt / answer body 时必须显式选择。

3. tracing 是 debug 面：
   解释 pipeline 怎么跑，不证明回答对。
```

VAKS 不应借：

```text
observability platform
always-on content logging
external trace backend as source of truth
```

### Candidate Point

```yaml
candidate_id: cp-haystack-pipeline-trace-as-query-run-receipt
point_text: "Query-run records should use a trace-like shape while keeping content logging opt-in and diagnostic-only."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/articles/2026-06-06-haystack-tracing-source.md
source_anchor:
  url: https://docs.haystack.deepset.ai/docs/tracing
  section: "Configuring a Tracing Backend / Content Tracing"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

## Source 3: LlamaIndex Citation Query Engine

### What The Source Says

LlamaIndex 这个例子把 citation 做成工作流：

```text
retrieve nodes
-> create citation nodes
-> split retrieved content into smaller numbered sources
-> synthesize answer with citation prompt
```

它的 prompt 明确要求：

```text
answer based solely on sources
cite only when explicitly referencing a source
if sources are not helpful, say that
```

### VAKS-Relevant Extraction

VAKS 应借：

```text
1. citation stage 显式化：
   create citation / citable pack items is a named step after retrieval.

2. source numbering 有用：
   pack item 可以给模型短 source number，但背后必须保留 path / selector / offset。

3. sources not helpful 是合法输出：
   如果 pack 不支持答案，不应该硬答。
```

VAKS 不应借：

```text
citation marker -> support
source number -> selector
retrieved chunk -> evidence packet
```

### Candidate Point

```yaml
candidate_id: cp-llamaindex-citation-stage-as-explicit-workflow
point_text: "Citation generation should be a distinct post-retrieval workflow stage that creates citable pack items before answer synthesis."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: evidence_check
source_ref: raw/articles/2026-06-06-llamaindex-citation-query-engine-source.md
source_anchor:
  url: https://developers.llamaindex.ai/python/examples/workflow/citation_query_engine/
  section: "The Workflow Events / Citation Prompt Templates / create_citation_nodes"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

## Source 4: Elastic Reciprocal Rank Fusion

### What The Source Says

Elastic 的 RRF 文档给出的是工程形状：

```text
multiple child retrievers
-> each returns top documents
-> RRF combines by rank position
-> rank_constant and rank_window_size control influence/window
```

文档示例包括：

```text
kNN + standard search
BM25 / term query + sparse vector retrieval
```

### VAKS-Relevant Extraction

VAKS 应借：

```text
1. RRF 是 hybrid recall 的默认融合候选：
   不同 retriever 的原始 score 不可比，按 rank 融合更稳。

2. rank_window_size 对应 oversampling：
   第一阶段要给后续 rerank/pack 足够候选窗口。

3. RRF score/rank 只能进 activation/diagnostic：
   不得写入 evidence support 或 truth confidence。
```

VAKS 不应借：

```text
Elasticsearch dependency
RRF as universal best answer
RRF rank as support strength
```

### Candidate Point

```yaml
candidate_id: cp-elastic-rrf-rank-position-fusion
point_text: "RRF can fuse heterogeneous retrieval channels by rank position and should be recorded as activation metadata rather than evidence support."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: rationale_check
source_ref: raw/articles/2026-06-06-elastic-rrf-source.md
source_anchor:
  url: https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion
  section: "Reciprocal rank fusion API"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

## Combined Minimal Design Delta For VAKS

### Query-Run Receipt

```yaml
query_run_id:
timestamp:
query_type:
risk_type:
planner_output:
retrieval_profile:
retrievers_called:
candidate_counts_by_channel:
fusion_method:
rank_window_size:
rerank_window:
trace_events:
  - stage:
    input_refs:
    output_refs:
    latency_ms:
    warnings:
content_trace_policy: refs_only | snippets_allowed | full_content_allowed
selected_pack_id:
diagnostics:
  context_relevance:
  groundedness:
  answer_relevance:
  evidence_binding_status:
feedback_ref:
```

### Pack Item

```yaml
item_id:
display_source_number:
source_ref:
selector_or_offset:
snippet:
contextualized_snippet:
citable_status: activation_only | drilldown_required | span_ready
matched_channels:
channel_ranks:
rrf_rank:
rerank_score:
why_included:
exclusion_or_caution_note:
```

### Hard Boundary

```text
trace != truth
metric != truth confidence
RRF rank != evidence support
citation marker != claim support
groundedness in retrieved context != world correctness
```

## Adoption Judgment

```text
adopt as candidate:
  diagnostic separation for query-run receipts
  trace-like query-run records
  citation stage as explicit workflow
  RRF rank-position fusion as hybrid retrieval candidate

adapt:
  TruLens metrics into labels/review aids, not evaluator authority
  Haystack content tracing into refs-only default
  LlamaIndex citation nodes into VAKS pack items with selector backrefs
  Elastic rank_window_size into retrieval-profile/oversampling field

park:
  observability backend
  universal evaluator scoring
  mandatory LlamaIndex/Haystack/Elasticsearch dependency

reject for core:
  any route where metric, trace, citation, or rank becomes reviewed truth
```
