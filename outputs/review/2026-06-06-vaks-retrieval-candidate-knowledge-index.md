---
type: candidate_knowledge_index
status: in_progress
created_at: 2026-06-06
scope: VAKS retrieval/query contract candidate knowledge points
truth_boundary: candidate index only; not reviewed knowledge; not architecture decision; not action basis
---

# VAKS Retrieval Candidate Knowledge Index

## Purpose

Keep reusable retrieval/query/context-pack candidate points from external source
distillations findable without promoting them into reviewed knowledge.

Rules:

```text
candidate index = navigation / review queue aid
not truth
not adoption
not action basis
not Project Overlay mainline
```

## Candidate Points

| Candidate slug | Proposed type | Source distillation | Borrow scope | Status |
|---|---|---|---|---|
| `contextualized-retrieval-chunks` | pattern | `2026-06-06-anthropic-contextual-retrieval-candidate-distillation.md` | Preserve document/path/heading context around chunks/index items. | candidate_only |
| `hybrid-recall-plus-rerank` | pattern | `2026-06-06-anthropic-contextual-retrieval-candidate-distillation.md` | Candidate baseline for BM25/lexical + dense + rank fusion + rerank. | candidate_only |
| `pack-item-contextualized-snippet` | concept | `2026-06-06-anthropic-contextual-retrieval-candidate-distillation.md` | Distinguish raw snippet from contextualized snippet in pack item. | candidate_only |
| `retrieval-eval-failure-to-retrieve` | concept | `2026-06-06-anthropic-contextual-retrieval-candidate-distillation.md` | Future diagnostic: relevant anchor present in candidate pool before answer eval. | candidate_only |
| `identifier-first-payload-later` | pattern | `2026-06-06-anthropic-effective-context-engineering-agents-candidate-distillation.md` | Use path/title/heading/selector/item ID as pack skeleton before full payload. | candidate_only |
| `just-in-time-context-loading` | pattern | `2026-06-06-anthropic-effective-context-engineering-agents-candidate-distillation.md` | Support drilldown/open actions rather than dumping all payloads upfront. | candidate_only |
| `progressive-disclosure-context-pack` | concept | `2026-06-06-anthropic-effective-context-engineering-agents-candidate-distillation.md` | Pack compiler: summary before detail, identifier before payload, drilldown before dump. | candidate_only |
| `context-compaction-is-runtime-hygiene` | anti-pattern boundary | `2026-06-06-anthropic-effective-context-engineering-agents-candidate-distillation.md` | Treat compaction as runtime trace/activation aid, not reviewed memory. | candidate_only |
| `tool-output-compact-context` | pattern | `2026-06-06-anthropic-effective-context-engineering-agents-candidate-distillation.md` | API/MCP/read tools return compact, provenance-rich context. | candidate_only |
| `query-plan-as-retrieval-output` | pattern | `2026-06-06-microsoft-azure-ai-search-agentic-retrieval-candidate-distillation.md` | Make query planning a visible retrieval artifact. | candidate_only |
| `parallel-subquery-retrieval` | pattern | `2026-06-06-microsoft-azure-ai-search-agentic-retrieval-candidate-distillation.md` | Decompose complex queries into focused subqueries that can run in parallel. | candidate_only |
| `modular-retrieval-response` | concept | `2026-06-06-microsoft-azure-ai-search-agentic-retrieval-candidate-distillation.md` | Separate grounding candidates, source references, and execution trace. | candidate_only |
| `activity-plan-as-retrieval-receipt` | concept | `2026-06-06-microsoft-azure-ai-search-agentic-retrieval-candidate-distillation.md` | Expose query execution steps as receipt/trace. | candidate_only |
| `agentic-retrieval-cost-governance` | pattern | `2026-06-06-microsoft-azure-ai-search-agentic-retrieval-candidate-distillation.md` | Surface reasoning effort, fan-out, rerank window, token and latency budgets. | candidate_only |
| `hybrid-search-as-default-recall-baseline` | pattern | `2026-06-06-google-cloud-gemini-enterprise-hybrid-search-candidate-distillation.md` | Treat lexical/token + semantic/vector recall as the likely default retrieval baseline. | candidate_only |
| `exact-match-branch-for-codenames-and-identifiers` | pattern | `2026-06-06-google-cloud-gemini-enterprise-hybrid-search-candidate-distillation.md` | Preserve lexical/token retrieval for file paths, headings, version strings, schema names, source IDs, and project terms. | candidate_only |
| `rrf-fuses-incomparable-retrieval-ranks` | concept | `2026-06-06-google-cloud-gemini-enterprise-hybrid-search-candidate-distillation.md` | Use rank-position fusion when raw channel scores are not comparable. | candidate_only |
| `alpha-as-retrieval-profile-knob` | concept | `2026-06-06-google-cloud-gemini-enterprise-hybrid-search-candidate-distillation.md` | Treat keyword/vector balance as retrieval profile configuration, not evidence or confidence. | candidate_only |
| `hybrid-rerank-as-two-stage-retrieval` | pattern | `2026-06-06-google-cloud-gemini-enterprise-hybrid-search-candidate-distillation.md` | Let oversampled hybrid recall feed rerank before pack compile while keeping rerank activation-only. | candidate_only |
| `position-aware-context-pack-ordering` | pattern | `2026-06-06-arxiv-retrieval-batch-candidate-distillation.md` | Keep important evidence anchors and drilldown pointers from being buried in the middle of long packs. | candidate_only |
| `rag-eval-dimensions-are-separate` | concept | `2026-06-06-arxiv-retrieval-batch-candidate-distillation.md` | Separate context relevance, answer faithfulness, answer relevance, and evidence binding diagnostics. | candidate_only |
| `on-demand-retrieval-and-critique` | pattern | `2026-06-06-arxiv-retrieval-batch-candidate-distillation.md` | Trigger retrieval/critique by task need instead of fixed-passages-every-time. | candidate_only |
| `summary-tree-as-selective-structure-branch` | pattern | `2026-06-06-arxiv-retrieval-batch-candidate-distillation.md` | Use summary-tree retrieval only for long-document, corpus-global, synthesis, or multi-step needs. | candidate_only |
| `query-complexity-router` | pattern | `2026-06-06-arxiv-retrieval-batch-candidate-distillation.md` | Route exact/factual/synthesis/multi-hop/corpus-global queries to different retrieval depths. | candidate_only |
| `sentence-level-citation-binding` | pattern | `2026-06-06-arxiv-retrieval-batch-candidate-distillation.md` | Bind action-facing claims or sentences to source selectors, quote windows, support status, and gaps. | candidate_only |
| `selective-graphrag-branch` | pattern | `2026-06-06-arxiv-retrieval-batch-candidate-distillation.md` | Keep graph/heading/entity neighborhood retrieval as an optional branch, not the primary truth skeleton. | candidate_only |
| `retrieval-strategy-as-costed-choice` | concept | `2026-06-06-arxiv-retrieval-batch-candidate-distillation.md` | Record retrieval depth, branch choices, latency, and cost/fallback warnings. | candidate_only |
| `global-question-as-qfs-mode` | concept | `2026-06-06-microsoft-graphrag-query-focused-summarization-candidate-distillation.md` | Route whole-corpus theme/pattern questions as query-focused summarization, not ordinary local top-k retrieval. | candidate_only |
| `community-summary-as-global-briefing` | concept | `2026-06-06-microsoft-graphrag-query-focused-summarization-candidate-distillation.md` | Treat GraphRAG/community reports as derived high-level briefings with drilldown required. | candidate_only |
| `local-to-global-graph-summarization-branch` | pattern | `2026-06-06-microsoft-graphrag-query-focused-summarization-candidate-distillation.md` | Use entity/heading/link neighborhoods plus high-level summaries only for corpus-global or relation-tracing needs. | candidate_only |
| `compiled-kb-as-read-first-surface` | pattern | `2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md` | Compile source/candidate/review/query-run metadata into an agent-readable index/workbench before raw search. | candidate_only |
| `registry-before-recompute` | pattern | `2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md` | Check existing source cards, candidate distillations, context packs, and query-run receipts before re-extracting. | candidate_only |
| `versioned-operational-artifacts` | concept | `2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md` | Treat source extraction, candidate distillation, query-run, context-pack, feedback, and index build outputs as named/versioned receipts. | candidate_only |
| `staged-atomic-toolchain-writes` | pattern | `2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md` | Use staging, validation, receipts, and explicit publish for lightweight scripts to avoid partial or silent overwrite. | candidate_only |
| `one-stage-one-script-toolchain` | pattern | `2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md` | Keep ingest, candidate generation, index rebuild, context-pack generation, and feedback recording as separate semantic steps. | candidate_only |
| `expensive-compute-save-full-filter-later` | pattern | `2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md` | Preserve reusable ASR/OCR/embedding/extraction substrate before task-specific filtering. | candidate_only |
| `dataset-db-is-not-vaks-truth-source` | anti-pattern boundary | `2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md` | Keep DB/cache/compiled KB/indexes as derived activation or provenance surfaces, not reviewed truth. | candidate_only |
| `rag-triad-diagnostic-separation` | concept | `2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md` | Separate context relevance, groundedness, and answer relevance as diagnostics. | candidate_only |
| `pipeline-trace-as-query-run-receipt` | pattern | `2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md` | Record planner/retriever/rerank/pack/answer/evidence-binding stages as a trace-like receipt. | candidate_only |
| `content-tracing-default-off` | anti-pattern boundary | `2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md` | Keep query-run receipts refs-only by default; full content/snippet logging must be explicit. | candidate_only |
| `citation-stage-as-explicit-workflow` | pattern | `2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md` | Treat citable pack item creation as a named post-retrieval stage before answer synthesis. | candidate_only |
| `numbered-source-node-with-selector-backref` | concept | `2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md` | Use short source numbers in packs only when backed by stable source refs/selectors. | candidate_only |
| `rrf-rank-position-fusion` | concept | `2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md` | Fuse heterogeneous retrieval channels by rank position and keep the result activation-only. | candidate_only |
| `rank-window-as-oversampling-control` | concept | `2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md` | Treat first-stage retrieval window size as an explicit profile/cost knob before rerank or pack compile. | candidate_only |

## Tags / Navigation

Current navigation tags:

```text
retrieval
contextual-retrieval
hybrid-search
token-search
sparse-retrieval
bm25
splade
embeddings
semantic-search
exact-match
identifiers
rrf
rerank
two-stage-retrieval
retrieval-profile
long-context
lost-in-the-middle
context-ordering
context-engineering
context-pack
pack-compiler
rag-evaluation
answer-faithfulness
answer-relevance
context-relevance
evaluator-boundary
groundedness
rag-triad
just-in-time-loading
progressive-disclosure
compaction
mcp-read-layer
agentic-retrieval
query-planning
subquery-decomposition
parallel-retrieval
retrieval-receipt
activity-plan
cost-governance
query-run-trace
trace-event
content-tracing
refs-only
privacy-boundary
inline-citation
numbered-source
selector-backref
rank-window
compiled-knowledge-base
read-first-agent
artifact-registry
versioned-artifacts
toolchain-contract
staged-write
atomic-publish
reuse-before-recompute
one-stage-one-script
checkpoint
delta-processing
delta-unsafe
compiled-index
obsidian-workbench
query-complexity
structure-aware-retrieval
summary-tree
raptor
graphrag
query-focused-summarization
corpus-global
global-sensemaking
community-summary
global-briefing
local-to-global
partial-response-aggregation
citation-binding
sentence-level-citation
activation
evidence-boundary
```

Tag rule:

```text
Tags help find candidates.
Tags do not prove candidate quality, generality, adoption, or truth.
```

## Review Needs

Before promotion to reviewed pattern / concept:

```text
compare across multiple sources
check VAKS need and scope
preserve retrieval-as-activation boundary
preserve selector / evidence / warrant boundary
decide whether destination is pattern, concept, anti-pattern, or decision
```
