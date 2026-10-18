---
record_kind: frontier_source_ledger
status: candidate
knowledge_status: candidate
project_id: VAKS
action_basis_allowed: false
truth_mutation_allowed: false
---

# Frontier Source Ledger

This ledger tracks retrieval/vector/search designs to absorb before producing a custom VAKS retrieval-layer design.

## Boundary

Entries here are research routing only.

```text
listed != endorsed
distilled != adopted
benchmark != proof
retrieval score != truth
```

## Ledger

| Source / Family | Status | What To Extract | VAKS Fit Question | Boundary Risk |
|---|---|---|---|---|
| `RyanCodrai/turbovec` | distilled + 0.8.0 refresh | Local compressed vector cache; allowlist rerank; stable IDs; cache-load hardening | Can it accelerate context-pack retrieval after bucket filtering? | Vector similarity or cache file treated as support |
| `AxDSan/mnemosyne` | distilled | Local-first SQLite retrieval layer; sqlite-vec + FTS5 hybrid recall; polyphonic vector/graph/fact/temporal recall; query cache; embedding lifecycle cleanup | Can VAKS use a rebuildable SQLite-derived retrieval cache while keeping bucket-first authority governance? | Agent memory or hybrid score treated as truth/evidence/action basis |
| `cBrain official mindmap` | distilled | Structure-first retrieval entry; tree navigation; node-title/note/library layered search; node workbench; knowledge-quantity activation signal | How should VAKS expose allowed drawers before retrieval and turn results into anchor workbench cards? | Tree position, kq, or UI connection treated as truth/support |
| `cBrain 1.3.2 offline package` | black-box distilled | Public package data shape: graph nodes/links, Markdown notes, domain object records, canvas JSON, export/migration model | Can VAKS use an anchor manifest + rebuildable relation cache + exportable context-pack modes without turning cache into truth? | Private implementation, local/offline data, or graph links treated as evidence/support |
| `cBrain quality transparency label` | P1 candidate point | Human-readable rigor/source/trust/consensus/scope/risk label for personal models and method notes | How should VAKS make authority boundaries visible on anchor cards and context packs? | Quality label treated as truth confidence, evidence support, or action readiness |
| `safishamsi/graphify` | distilled | Derived code/document knowledge graph; AST-first anchors; community activation; BFS/DFS query tools; MCP/agent query surface; graph-cache guardrails | Can VAKS add graph retrieval inside authority buckets without letting graph rank, community, or confidence become support? | Graph edge/community/query result treated as reviewed relation, truth, or action basis |
| `arXiv:2606.07972 OneFeed` | distilled | Search-recommendation fusion; shared behavior encoder; semantic-ID generation; intent-query generation; SID-query alignment; feedback loop | Can VAKS use controlled query variants from explicit query + active context to improve recall without feedback truth mutation? | Expected-performance tables treated as evidence; generated query bypasses authority buckets; feedback mutates truth |
| Embedded vector libraries | queue | Local indexes, quantization, update/delete model | Can VAKS avoid heavy vector DB while keeping recall high? | Cache mistaken for authority |
| FAISS / HNSW-style indexes | queue | Baseline ANN behavior and recall/speed tradeoffs | What should the benchmark baseline be? | Pure similarity overread |
| Qdrant / Milvus / Weaviate / LanceDB style systems | queue | Metadata filters, payload indexes, hybrid search, persistence | Which filter semantics should VAKS copy without adopting a server stack? | Payload filter treated as permission proof |
| `pgvector` / database-native vector search | queue | SQL-adjacent vector + metadata filtering | Is simple DB-backed vector enough for small VAKS deployments? | SQL table becomes shadow truth |
| BM25 / sparse retrieval / SPLADE family | queue | Keyword and sparse semantic recall | How to keep exact terms, names, versions, and Chinese text visible? | Keyword rank treated as evidence |
| Hybrid retrieval / RRF | queue | Combining lexical + vector ranks | How to fuse relevance only inside the same authority bucket? | RRF merging raw/candidate/reviewed into one list |
| Rerankers / cross-encoders | queue | Precision improvement after recall | Which rerank step is worth cost for action-facing packs? | Reranker score treated as truth confidence |
| Late-interaction retrieval | queue | Token-level matching with stronger recall | Does it help source-anchor precision enough to justify complexity? | Model score overcredited |
| GraphRAG / LightRAG / relation-neighborhood retrieval | partially absorbed | Low/high-level retrieval strata; relation neighborhood activation | How to recall context around reviewed relations without auto-creating relations? | Graph rank treated as trust |
| Chunking / document layout retrieval | queue | Stable chunk IDs, heading spans, section anchors | What chunk shape preserves source trace and context? | Snippet becomes decontextualized evidence |
| Retrieval evaluation / attribution / sufficiency | queue | Recall, anchor correctness, missing evidence, support checks | How to test retrieval quality without turning metrics into truth? | Benchmark or judge result becomes action readiness |
| Local-first / privacy-preserving retrieval | queue | Offline operation, rebuildable cache, vault portability | What can run on the user's machine without cloud dependency? | Local result assumed more trustworthy |

## Immediate Next Intake Candidates

```text
1. A mature vector DB with strong metadata filtering.
2. A hybrid retrieval design that combines sparse and dense retrieval.
3. A reranking / late-interaction design.
4. A chunking / anchor strategy source.
5. A retrieval-evaluation / attribution source.
```

## Absorbed Source Pointers

```text
turbovec:
  candidate distillation: outputs/review/2026-06-11-RyanCodrai-turbovec-candidate-distillation.md
  architecture review: wiki/summaries/2026-06-11-RyanCodrai-turbovec-architecture-review.md
  project overlay: outputs/review/project_lens_overlays/2026-06-11-turbovec-vector-retrieval-cache.md

mnemosyne:
  candidate distillation: outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md
  architecture review: wiki/summaries/2026-06-11-AxDSan-mnemosyne-architecture-review.md
  project overlay: outputs/review/project_lens_overlays/2026-06-11-mnemosyne-vector-memory-layer.md

cBrain official mindmap:
  source card: outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/source-card.md
  candidate distillation: outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/candidate-distillation.md
  offline package black-box notes: outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/offline-package-blackbox-notes.md

cBrain quality transparency label:
  P1 candidate point: outputs/review/vaks-retrieval-layer-design-2026-06-11/p1-cbrain-knowledge-quality-transparency-label.md

graphify:
  source card: raw/repos/2026-06-11-safishamsi-graphify-source.md
  candidate distillation: outputs/review/2026-06-11-safishamsi-graphify-candidate-distillation.md
  architecture review: wiki/summaries/2026-06-11-safishamsi-graphify-architecture-review.md
  project overlay: outputs/review/project_lens_overlays/2026-06-11-graphify-graph-retrieval-layer.md
  P1 retrieval-layer point: outputs/review/vaks-retrieval-layer-design-2026-06-11/p1-graphify-code-graph-retrieval-layer.md

OneFeed:
  source card: raw/papers/2026-06-11-guoxun-onefeed-source.md
  candidate distillation: outputs/review/2026-06-11-guoxun-onefeed-candidate-distillation.md
  architecture review: wiki/summaries/2026-06-11-guoxun-onefeed-architecture-review.md
  project overlay: outputs/review/project_lens_overlays/2026-06-11-onefeed-search-recommendation-fusion.md
  P2 retrieval-layer point: outputs/review/vaks-retrieval-layer-design-2026-06-11/p2-onefeed-feed-search-query-generation.md
```
