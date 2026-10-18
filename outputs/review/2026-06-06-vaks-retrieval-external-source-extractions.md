---
type: external_source_extraction
status: in_progress
created_at: 2026-06-06
scope: VAKS retrieval/query contract external references
truth_boundary: candidate extraction only; not reviewed knowledge; not architecture decision; not action basis
---

# VAKS Retrieval External Source Extractions

## Purpose

Extract key design lessons from external sources cited by Pro for strengthening
the VAKS retrieval / query / context-pack contract.

Rules:

```text
source extraction = candidate input
not truth
not adopted architecture
not action basis
```

## Derived Records

```text
raw/articles/2026-06-06-anthropic-contextual-retrieval-source.md
outputs/review/2026-06-06-anthropic-contextual-retrieval-candidate-distillation.md
raw/articles/2026-06-06-anthropic-effective-context-engineering-agents-source.md
outputs/review/2026-06-06-anthropic-effective-context-engineering-agents-candidate-distillation.md
raw/articles/2026-06-06-microsoft-azure-ai-search-agentic-retrieval-source.md
outputs/review/2026-06-06-microsoft-azure-ai-search-agentic-retrieval-candidate-distillation.md
raw/articles/2026-06-06-google-cloud-gemini-enterprise-hybrid-search-source.md
outputs/review/2026-06-06-google-cloud-gemini-enterprise-hybrid-search-candidate-distillation.md
raw/papers/2026-06-06-lost-in-the-middle-source.md
raw/papers/2026-06-06-ares-rag-evaluation-source.md
raw/papers/2026-05-29-self-rag-source.md
raw/papers/2026-06-06-raptor-source.md
raw/papers/2026-06-06-adaptive-rag-source.md
raw/papers/2026-06-06-longcite-source.md
raw/papers/2026-06-06-rag-vs-graphrag-systematic-evaluation-source.md
outputs/review/2026-06-06-arxiv-retrieval-batch-candidate-distillation.md
raw/papers/2026-06-06-microsoft-graphrag-query-focused-summarization-source.md
outputs/review/2026-06-06-microsoft-graphrag-query-focused-summarization-candidate-distillation.md
raw/articles/2026-06-06-trulens-feedback-rag-triad-source.md
raw/articles/2026-06-06-haystack-tracing-source.md
raw/articles/2026-06-06-llamaindex-citation-query-engine-source.md
raw/articles/2026-06-06-elastic-rrf-source.md
outputs/review/2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md
```

## 1. Anthropic: Contextual Retrieval

Source:

```text
https://www.anthropic.com/engineering/contextual-retrieval
```

Published:

```text
2024-09-19
```

### What The Source Says

Anthropic's core claim is that traditional RAG often loses important document
context when it chunks material. A chunk can be locally true but ambiguous
without its document-level situation: for example, "the company's revenue grew"
does not say which company, period, filing, or baseline.

Their proposed method is:

```text
for each chunk:
  generate a short document-aware context
  prepend that context to the chunk
  index the contextualized chunk for embeddings
  index the contextualized chunk for BM25
```

They call these:

```text
Contextual Embeddings
Contextual BM25
```

The article also supports a retrieval stack:

```text
BM25 + embeddings
-> rank fusion / deduplication
-> oversampled initial retrieval
-> reranking
-> final top-K context
```

Anthropic reports the following in its experiments:

```text
Contextual Embeddings reduced top-20 retrieval failure rate by 35%.
Contextual Embeddings + Contextual BM25 reduced top-20 retrieval failure rate by 49%.
Contextual Embeddings + Contextual BM25 + reranking reduced top-20 retrieval failure rate by 67%.
```

Implementation considerations from the article:

```text
chunk boundaries matter
embedding model choice matters
domain-specific contextualizer prompts can improve retrieval
more retrieved chunks can help but can also distract
run evals for the actual use case
reranking improves quality but adds latency/cost
```

### VAKS-Relevant Extraction

This source strongly supports these VAKS retrieval design deltas:

```text
1. Hybrid retrieval should be default, not optional:
   BM25 / lexical exact-match and dense semantic retrieval cover different
   failure modes.

2. Contextualized chunks are more valuable than raw chunks:
   a pack item or index item should preserve local text plus document/path/
   heading/version context.

3. Reranking belongs after oversampling:
   first-stage retrieval should collect a wider candidate pool before expensive
   ranking narrows it.

4. Context pack items need contextualized_snippet:
   VAKS should distinguish raw snippet from contextualized snippet.

5. Retrieval eval should measure failure-to-retrieve:
   VAKS can later test whether relevant anchors appear in the candidate pool
   before arguing about answer quality.
```

### Minimal VAKS Design Delta

Add these fields to the candidate `pack_item` contract:

```yaml
snippet:
contextualized_snippet:
source_title_or_path:
heading_or_local_context:
selector_or_offset:
matched_channels:
channel_ranks:
rerank_score:
citable_status:
```

Add this retrieval rule:

```text
Context used for retrieval is not evidence support by itself.
It improves activation quality. Evidence support still requires selector-grade
source anchor, quote window, and warrant for the claim being used.
```

Add this pack compiler rule:

```text
Do not pass raw top-K chunks directly into action-facing use.
Build a context-aware pack with source/path/heading context, then separate
activation-only items from span-ready evidence candidates.
```

### What VAKS Should Not Borrow Yet

Do not turn this into:

```text
mandatory contextualization for every light source
automatic evidence support
automatic correctness judgment
full RAG eval framework
provider-specific embedding dependency
```

### Adoption Judgment

```text
adopt:
  contextualized_snippet as a pack/index design concept

adapt:
  Contextual BM25 + embeddings + rerank as the default retrieval shape, but keep
  implementation local and replaceable

watch:
  prompt-caching-specific cost strategy, since it depends on provider/runtime

reject for core:
  treating contextual retrieval accuracy as truth confidence
```

## 2. Anthropic: Effective Context Engineering For AI Agents

Source:

```text
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
```

Published:

```text
unknown from current extraction
```

### What The Source Says

Anthropic frames context engineering as a central design problem for effective
AI agents. The practical theme is that agent context should stay compact,
task-relevant, and controllable. A strong agent should not blindly preload all
available text into the prompt.

The source supports a context strategy built around:

```text
lightweight identifiers before large payloads
just-in-time loading
progressive disclosure
context compaction
external notes / state
tool outputs that return useful compact context
```

### VAKS-Relevant Extraction

This source supports these VAKS retrieval/context-pack design deltas:

```text
1. Identifier-first, payload-later:
   pack should first carry path, title, heading, selector, item ID, and
   drilldown path before loading large source payloads.

2. Just-in-time context loading:
   retrieval should support drilldown/open actions instead of dumping all
   payloads into the first pack.

3. Progressive disclosure:
   pack compiler should present summary/navigation first and expand evidence
   detail only for claims/tasks that require it.

4. Context compaction is runtime hygiene:
   compaction can help long sessions, but compacted context is not reviewed
   knowledge.

5. Tool outputs should be compact but provenance-rich:
   read tools should return source_ref, selector, local context, warnings, and
   drilldown path instead of noisy raw dumps.
```

### Minimal VAKS Design Delta

Add or reinforce these `pack_item` fields:

```yaml
source_ref:
source_title_or_path:
heading_or_local_context:
selector_or_offset:
snippet:
contextualized_snippet:
drilldown_path:
citable_status:
why_included:
exclusion_or_caution_note:
```

Add this pack compiler rule:

```text
summary before detail;
identifier before payload;
drilldown before dump.
```

Add this agent context boundary:

```text
Compacted agent context and runtime notes are activation / trace surfaces.
They are not reviewed knowledge, evidence support, or action basis.
```

### What VAKS Should Not Borrow Yet

Do not turn this into:

```text
agent notes as reviewed memory
summary-only action basis
unbounded context dump
full agent workbench implementation now
provider-specific context management dependency
```

### Adoption Judgment

```text
adopt:
  identifier-first / payload-later as a pack compiler principle

adapt:
  just-in-time loading and progressive disclosure into VAKS pack items and
  API/MCP read resources

watch:
  compaction strategies for long query-runs and Codex sessions

reject for core:
  treating compacted context or agent notes as reviewed knowledge
```

## 3. Microsoft: Agentic Retrieval In Azure AI Search

Source:

```text
https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview?tabs=quickstarts
```

Last updated:

```text
2026-06-02
```

### What The Source Says

Microsoft describes agentic retrieval in Azure AI Search as a multi-query
pipeline for complex questions in chat, RAG, copilot, and agent workflows.

Key shape:

```text
query + conversation history
-> LLM query planning
-> focused subqueries
-> parallel execution
-> keyword / vector / hybrid search
-> semantic reranking per subquery
-> unified retrieval response
```

The response is modular. It can include:

```text
grounding data for answer generation
source/reference documents for inspection
activity plan / execution details
```

Microsoft also exposes cost and latency concerns:

```text
agentic retrieval adds latency
planner and reranking consume tokens
fan-out and source count affect cost
activity logs help inspect issued queries and parameters
```

Availability caveat:

```text
Some capabilities are generally available in the 2026-04-01 REST API.
Other capabilities remain preview in the 2026-05-01-preview API.
```

### VAKS-Relevant Extraction

This source supports these VAKS retrieval design deltas:

```text
1. Query plan should be visible:
   query planning is not just prompt intuition; it should produce a traceable
   retrieval artifact.

2. Complex questions can become subqueries:
   planner may split multi-ask / synthesis / multi-hop questions into focused
   subqueries.

3. Parallel retrieval is a real production pattern:
   subqueries can run simultaneously across retrieval mechanisms.

4. Retrieval response should be modular:
   separate grounding candidates, source references, and execution trace.

5. Activity plan belongs in receipt:
   retrieval should expose what happened, not only final hits.

6. Agentic retrieval needs budget controls:
   reasoning effort, fan-out, number of sources, rerank window, latency, and
   token use need visibility.
```

### Minimal VAKS Design Delta

Add these `query_run` / `retrieval_receipt` fields:

```yaml
planner_output:
subqueries: []
filters: []
retrievers_called: []
candidate_counts_by_channel:
fusion_method:
rerank_window:
selected_items: []
dropped_high_rank_items: []
latency_by_stage:
token_cost_by_stage:
warnings: []
fallbacks_triggered: []
```

Add these `context_pack_manifest` fields:

```yaml
planner_mode:
risk_mode:
retrieval_profile:
channels_used:
reranker_used:
selection_policy:
evidence_required:
warnings: []
fallbacks: []
```

Add this planner rule:

```text
Only run multi-query / agentic retrieval when query typing justifies it:
multi-ask, synthesis, multi-hop, corpus-global, comparison, or action-facing
context preparation.
```

### What VAKS Should Not Borrow Yet

Do not turn this into:

```text
Azure dependency
always-on agentic retrieval
copy of Azure knowledge base object
preview API dependency
retrieval response as reviewed truth
automatic answer correctness
```

### Adoption Judgment

```text
adopt:
  query plan / subqueries / activity plan as retrieval receipt concepts

adapt:
  modular response shape into VAKS pack manifest + source refs + execution trace

watch:
  Azure product API details because some features are preview / product-specific

reject for core:
  treating the retrieval response as evidence support or action basis by itself
```

## 4. Google Cloud: Gemini Enterprise Hybrid Search

Source:

```text
https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/vector-search/about-hybrid-search?hl=zh-cn
```

Updated:

```text
2026-06-05
```

Translation caveat:

```text
The page is a Chinese Google Cloud documentation page and notes that AI
translation may contain errors.
```

### What The Source Says

Google Cloud describes hybrid search as an IR architecture pattern that combines:

```text
semantic search / vector search
keyword search / token-based search
```

The important production-search point is that semantic search does not cover all
retrieval requirements. The page names examples where semantic search can be
weak:

```text
arbitrary product numbers or SKU
new product names
company-proprietary code names
out-of-domain data
```

Token-based search can use sparse methods such as:

```text
TF-IDF
BM25
SPLADE
```

For combining vector and keyword results, the page describes Reciprocal Rank
Fusion:

```text
RRF combines rank positions rather than pretending raw scores are comparable.
This is useful when different retrieval methods use different score scales.
```

It also exposes a keyword/vector balance knob:

```text
alpha = 0 means keyword-only
alpha = 1 means vector-only
default alpha = 0.5
```

And it points to reranking as a quality step after hybrid search.

### VAKS-Relevant Extraction

This source supports these VAKS retrieval design deltas:

```text
1. Hybrid recall should be the default candidate baseline:
   lexical/token and semantic/vector channels cover different failure modes.

2. Exact identifiers need their own retrieval path:
   file paths, headings, source IDs, schema names, version strings, and project
   codenames are VAKS equivalents of SKU / proprietary code name.

3. RRF belongs in activation, not truth:
   rank fusion is useful because scores are incomparable, but fused rank remains
   retrieval metadata.

4. Keyword/vector balance should be explicit:
   alpha-style balance should become a VAKS `retrieval_profile` knob, not hidden
   prompt behavior and not truth confidence.

5. Rerank is a second-stage retrieval operation:
   rerank can improve candidate order after oversampled hybrid recall, but it
   still cannot replace selector-grade evidence support.
```

### Minimal VAKS Design Delta

Add or strengthen these retrieval/query concepts:

```yaml
planner_output:
  retrieval_profile: identifier-heavy | balanced | semantic-heavy | exploratory

retrievers_called:
  lexical_or_token:
  semantic_or_vector:
  metadata_filter:

fusion_method:
  rrf_or_equivalent_rank_position_fusion

pack_item:
  matched_channels: []
  channel_ranks:
  fused_rank:
  rerank_score:
  citable_status:
```

Hard boundary:

```text
Hybrid rank, alpha, RRF position, and rerank score are activation or diagnostic
signals only unless linked to explicit source anchors and a claim-level warrant.
```

### What VAKS Should Not Borrow Yet

Do not turn this into:

```text
Google Cloud dependency
semantic-only retrieval
one universal alpha value
RRF rank as confidence
rerank score as evidence support
product-specific API behavior as VAKS architecture rule
```

### Adoption Judgment

```text
adopt:
  hybrid retrieval as a strong candidate baseline for recall

adapt:
  alpha-style balance into VAKS retrieval profiles
  RRF into an activation-only fusion receipt

watch:
  exact tuning values until VAKS has real query-run data

reject for core:
  treating fused rank, alpha, or rerank score as truth confidence
```

## 5. arXiv Retrieval Paper Batch

Sources:

```text
Lost in the Middle: https://arxiv.org/abs/2307.03172
ARES: https://arxiv.org/abs/2311.09476
Self-RAG: https://arxiv.org/abs/2310.11511
RAPTOR: https://arxiv.org/abs/2401.18059
Adaptive-RAG: https://arxiv.org/abs/2403.14403
LongCite: https://arxiv.org/abs/2409.02897
RAG vs. GraphRAG: https://arxiv.org/abs/2502.11371
```

Source handling:

```text
ARES appeared twice in the user-provided list and is deduplicated.
Self-RAG already had a source card and is reused instead of duplicated.
This pass is abstract/metadata-level candidate extraction, not full PDF review.
```

### What The Sources Say

The batch strengthens five retrieval-contract themes:

```text
1. Long context is not automatically usable context:
   Lost in the Middle shows that relevant information can be underused when
   buried in the middle of long inputs.

2. RAG evaluation dimensions are separate:
   ARES evaluates context relevance, answer faithfulness, and answer relevance
   as distinct dimensions.

3. Retrieval should adapt to task need:
   Self-RAG criticizes indiscriminate fixed-passage retrieval; Adaptive-RAG
   routes by question complexity.

4. Structure-aware retrieval is selective:
   RAPTOR uses summary trees for multi-level abstraction; RAG vs. GraphRAG
   emphasizes task-dependent strengths, trade-offs, failure modes, and
   efficiency concerns.

5. Citations need fine granularity:
   LongCite targets sentence-level citations in long-context QA, which maps to
   VAKS's claim-to-evidence binding need.
```

### VAKS-Relevant Extraction

This source batch supports these VAKS retrieval design deltas:

```text
1. Pack compiler needs an ordering policy:
   important evidence anchors and drilldown pointers should not be buried in a
   long undifferentiated pack.

2. Retrieval receipt should keep diagnostics separated:
   context relevance, answer faithfulness, answer relevance, and evidence
   binding status are different checks.

3. Planner should route by query complexity and risk:
   exact lookup, factual lookup, synthesis, multi-hop, corpus-global, and
   action-facing modes should not all use the same retrieval depth.

4. Structure-aware branches should be optional:
   summary tree / graph / neighborhood retrieval should run only when query type
   justifies it.

5. Action-facing answers need claim-level binding:
   document-level citation is not enough; VAKS should bind claims or sentences
   to source selectors, quote windows, support status, and gaps.
```

### Minimal VAKS Design Delta

Add or strengthen these fields:

```yaml
planner_output:
  query_type:
  risk_mode:
  complexity_level:
  retrieval_depth:
  selected_strategy:
  selected_strategy_reason:
  structure_branch_allowed:
  cost_budget:

context_pack_manifest:
  ordering_policy:
  evidence_priority_positions:
  summary_before_detail:
  selector_drilldown_required:

query_run_receipt:
  context_relevance_diagnostic:
  answer_faithfulness_diagnostic:
  answer_relevance_diagnostic:
  evidence_binding_status:
  latency_by_stage:
  cost_or_token_warning:
```

Hard boundary:

```text
Retrieval strategy, context position, evaluator score, citation marker, graph
rank, and summary-tree hit are activation or diagnostic signals only until
linked to explicit source anchors and a claim-level warrant.
```

### What VAKS Should Not Borrow Yet

Do not turn this into:

```text
mandatory trained query router
always-on agentic retrieval
always-on GraphRAG
RAPTOR as default retrieval skeleton
ARES as truth evaluator
LongCite as citation infrastructure
automatic self-reflection approval
universal retrieval confidence score
```

### Adoption Judgment

```text
adopt as candidate:
  query complexity router
  position-aware pack compiler
  sentence/claim-level evidence binding
  separated retrieval/eval diagnostics

adapt:
  RAPTOR/GraphRAG into selective structure-aware branches
  Self-RAG/Adaptive-RAG into planner stop/escalation rules

watch:
  whether VAKS's real query runs justify graph or summary-tree tooling

reject for core:
  turning any evaluator, retriever, graph, or citation generator into truth authority
```

## 6. Microsoft Research: GraphRAG Query-Focused Summarization

Source:

```text
https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/
```

Published:

```text
April 2024
```

Related existing VAKS source:

```text
raw/repos/2026-05-29-graphrag-source.md
```

### What The Source Says

The Microsoft Research page frames a key distinction:

```text
ordinary RAG:
  retrieve specific local information from a corpus

global corpus question:
  answer a query-focused summarization problem over the whole collection
```

The paper page describes GraphRAG as a local-to-global strategy:

```text
source documents
-> LLM-derived entity knowledge graph
-> community summaries for related entity groups
-> partial responses from community summaries
-> final global response from partial responses
```

The reported benefit is strongest for global sensemaking questions over large
text collections, especially answer comprehensiveness and diversity compared
with a conventional RAG baseline.

### VAKS-Relevant Extraction

This source supports these VAKS retrieval design deltas:

```text
1. Global questions need their own planner mode:
   "main themes across the corpus" is not the same as exact lookup or ordinary
   local retrieval.

2. Community summaries are high-level briefings:
   they can guide context preparation, but they remain derived context.

3. Local-to-global graph summarization is a selective branch:
   it belongs under corpus_global / relation_tracing / global_sensemaking, not
   in the default retrieval path.

4. Partial-response aggregation should be receipted:
   if used, the system should record which community/theme units and partial
   responses contributed to a global answer.
```

### Minimal VAKS Design Delta

Add or strengthen these fields:

```yaml
planner_output:
  query_type: corpus_global | relation_tracing | synthesis | ...
  global_sensemaking: true | false
  structure_branch_allowed: true | false
  selected_structure_branch: none | graph_neighborhood | summary_tree | community_summary

context_pack_manifest:
  high_level_briefings: []
  local_anchor_items: []
  derived_summary_items: []
  drilldown_required: true

query_run_receipt:
  community_or_theme_units_considered:
  partial_response_refs:
  aggregation_method:
  local_anchor_coverage:
  warnings:
```

Hard boundary:

```text
Community summaries, graph neighborhoods, partial responses, and final global
summaries are context-preparation artifacts until they are tied back to source
anchors and claim-level warrants.
```

### What VAKS Should Not Borrow Yet

Do not turn this into:

```text
GraphRAG as primary store
GraphRAG as reviewed relation creator
community report as truth
global summary as action basis
graph centrality or community membership as evidence support
always-on GraphRAG pipeline
```

### Adoption Judgment

```text
adopt as candidate:
  global question / QFS mode in the query planner
  community summaries as high-level briefings with drilldown required

adapt:
  local-to-global graph summarization into a selective structure-aware branch

watch:
  whether real VAKS queries frequently need corpus-global sensemaking

reject for core:
  full GraphRAG runtime or graph/community summary as truth authority
```

## 7. TruLens / Haystack / LlamaIndex / Elastic: Eval, Tracing, Citation, RRF

Sources:

```text
https://www.trulens.org/reference/trulens/feedback/
https://www.trulens.org/getting_started/core_concepts/rag_triad/
https://docs.haystack.deepset.ai/docs/tracing
https://developers.llamaindex.ai/python/examples/workflow/citation_query_engine/
https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion
```

### What The Sources Say

This source cluster reinforces four operational retrieval-layer ideas:

```text
TruLens:
  split RAG diagnostics into context relevance, groundedness, and answer relevance.

Haystack:
  trace pipeline execution, but keep content tracing disabled by default because
  inputs/outputs may contain sensitive user data.

LlamaIndex:
  treat citation creation as a post-retrieval workflow stage that splits
  retrieved nodes into smaller numbered source chunks.

Elastic:
  use RRF to combine ranked results from multiple child retrievers; record
  rank_window_size / rank_constant as retrieval-profile choices.
```

### VAKS-Relevant Extraction

This cluster supports these VAKS retrieval design deltas:

```text
1. Query-run receipt should be trace-shaped:
   planner, retrieval, fusion, rerank, pack, answer, evidence-binding, warnings.

2. Diagnostics must stay separated:
   context relevance is not groundedness; groundedness is not answer relevance;
   none of these is truth confidence.

3. Content logging should be refs-only by default:
   full snippets / prompts / answers in receipts require explicit mode.

4. Citation needs a workflow stage:
   source numbers are useful for drafting, but must point back to stable
   source refs/selectors.

5. RRF belongs in activation:
   rank fusion solves heterogeneous retrieval ordering; it does not measure
   evidence support.
```

### Minimal VAKS Design Delta

Add or strengthen:

```yaml
query_run_receipt:
  trace_events:
  content_trace_policy:
  diagnostics:
    context_relevance:
    groundedness:
    answer_relevance:
    evidence_binding_status:

pack_item:
  display_source_number:
  selector_or_offset:
  citable_status:
  rrf_rank:
  rank_window_source:
```

Hard boundary:

```text
trace != truth
metric != truth confidence
RRF rank != evidence support
citation marker != claim support
groundedness in retrieved context != world correctness
```

### Adoption Judgment

```text
adopt as candidate:
  query-run trace shape
  diagnostic separation
  citation stage as explicit workflow
  RRF rank-position fusion

adapt:
  content tracing into refs-only default
  numbered sources into pack item display IDs backed by selectors

reject for core:
  observability platform, mandatory framework dependency, evaluator-as-reviewer,
  score/rank/citation as truth
```
