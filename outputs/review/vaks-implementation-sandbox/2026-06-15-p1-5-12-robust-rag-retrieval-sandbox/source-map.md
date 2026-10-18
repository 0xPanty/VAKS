---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p1-5-12-robust-rag-retrieval-sandbox
status: implemented_pending_review
truth_boundary: sandbox_trace_only
---

# Source Map

## Project Rules Used

| Source | Rule used |
|---|---|
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 900-960 | Robust RAG decides what to read; VAKS evidence/action layers decide support and action. P1.5 package requires query construction, route selection, indexing strata, receipts, rerank traces, eval diagnostics, and failure cases proving retrieval output is not support. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 986-1117 | GraphRAG pieces map to VAKS as TextUnit anchors, candidate graph fragments, theme briefings, local/global/DRIFT routes, and read-only adapters; forbidden imports include graph runtime as core, graph DB as system of record, extracted relations as reviewed relations, community reports as support, ranks as trust, and query result as action basis. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 1119-1145 | GR acceptance cases: TextUnit anchor cannot mark support, local/global/DRIFT route receipts, graph rank cannot set confidence, extracted relation cannot create reviewed relation, community report cannot satisfy sufficiency, optional plugin stays read-only/suggest-only. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 1174-1268 | Kwipu/Graph RAG reference: vector + BM25 + temporal + synonym retrieval is useful only as bucket-filtered retrieval with receipts; graph index is derived cache, not source of record. |
| `SOURCE_INTAKE.md` lines 738-879 | Bucket filter first; RRF only within buckets; selected_by is trace metadata only; adapter returns context-pack candidates, not support by default; graph paths and extracted edges are recall metadata, not reviewed relations/support/action. |
| `SOURCE_INTAKE.md` lines 1395-1460 | Graph/rank score becoming support is a failure; action-facing support must anchor to raw/stable material; retrieval rank is not trust. |
| `REVIEW_QUEUE.md` lines 433-448 | Similarity, graph neighbor, association path, and PPR-style activation are pending signals, not support/confidence/truth. |
| `REVIEW_QUEUE.md` lines 649-657 | Community report is briefing/review cue, graph rank is retrieval priority, auto-extracted relation is candidate relation, TextUnit anchor is provenance. |
| `REVIEW_QUEUE.md` lines 810-826 | Similarity/vector score/graph traversal/association score cannot auto-support, increase confidence, promote, or create reviewed relations. |
| P1-10 runtime artifact sandbox | Runtime artifact detector is reused read-only. |
| P1-11 semantic anchor support sandbox | Semantic anchor checker is reused read-only. |

## Artifact Mapping

| Requirement | Artifact coverage |
|---|---|
| Query construction preserves verbatim input | `fixtures/valid-action-sensitive-hybrid-bucketed.json`, `failure-cases/action-query-missing-verbatim.json` |
| Route receipt records included/excluded buckets | all fixtures, `failure-cases/route-missing-buckets.json` |
| Bucket-first RRF | `fixtures/valid-reviewed-only-rrf.json`, `failure-cases/cross-bucket-rrf-fusion.json` |
| Selected excluded bucket blocked | `failure-cases/selected-excluded-bucket.json` |
| Vector/rerank cannot set confidence | `failure-cases/vector-rerank-sets-confidence.json` |
| Item-level semantic/vector/graph score fields cannot claim support | `failure-cases/item-semantic-score-claims-support.json` |
| Graph path/extracted relation cannot create reviewed relation | `failure-cases/graph-path-reviewed-relation.json` |
| Graph artifact authority-claim variants cannot create reviewed relation | `failure-cases/graph-artifact-claims-reviewed-relation.json` |
| Summary cannot become support/action | `failure-cases/tree-summary-action-support.json`, `failure-cases/community-report-sufficiency.json` |
| Eval pass cannot be reviewer approval | `failure-cases/eval-pass-reviewer-approval.json` |
| Citation still needs support/sufficiency in action mode | `failure-cases/citation-action-basis-without-support.json` |
| Active retrieval cannot auto-promote | `failure-cases/active-retrieval-auto-promotes-candidate.json` |
| Runtime artifact exclusion | `failure-cases/runtime-cache-selected.json`, `failure-cases/runtime-filter-disabled.json` |
| P1-11 semantic anchor boundary reuse | `failure-cases/semantic-score-support.json` |
| DRIFT lineage | `fixtures/valid-drift-explore-lineage.json`, `failure-cases/drift-missing-lineage.json` |
| Derived cache lifecycle boundary | `failure-cases/stale-derived-cache-used.json` |
| Optional plugin read-only/suggest-only | `failure-cases/plugin-write-mode.json` |

## Boundaries

- No real vector DB, GraphRAG runtime, MCP server, Obsidian graph, or file watcher
  is created.
- No production `tools/` validator is created.
- No mainline docs, protected wiki paths, templates, tools, or Obsidian vault are
  edited.
- No evidence support, reviewed knowledge, reviewer approval, action basis,
  promotion, commit, push, or sync is created.
