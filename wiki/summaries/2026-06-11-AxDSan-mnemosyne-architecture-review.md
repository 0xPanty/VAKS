---
type: architecture_review
record_kind: architecture_review
status: candidate
title: "AxDSan/mnemosyne architecture review"
source_ref: "raw/repos/2026-06-11-AxDSan-mnemosyne-source.md"
source_id: "github:AxDSan/mnemosyne@17a7dda350cc3d3fd599c53209bd4a15c8713bf0"
source_uri: "https://github.com/AxDSan/mnemosyne"
created_at: "2026-06-11"
created_by: Codex
knowledge_status: candidate
processing_tier: heavy
truth_status: not_reviewed
action_basis_allowed: false
truth_mutation_allowed: false
retrieval_policy:
  policy_kind: candidate_review_summary
  pack_allowed: context_with_warning
  action_basis_allowed: false
  warning_code: architecture_review_not_adoption
project_fit:
  verified_action_knowledge_system: strong_retrieval_cache_fit
  truth_layer: reject
  review_layer: limited_process_inspiration
  activation_layer: strong_fit
  context_pack_layer: strong_fit
assessment:
  domain: ai-agent-memory-retrieval-cache
  maturity: emerging
  complexity: high
  problem_fit_retrieval_cache: 4
  problem_fit_truth_review: 2
  reuse_value: 4
  implementation_cost: 4
  integration_fit: 3
  evidence_strength: 3
  reversibility: 4
tags:
  - architecture-review
  - candidate
  - vaks/retrieval-cache
  - vaks/context-pack
  - vaks/activation-not-truth
  - vector/sqlite-vec
  - retrieval/polyphonic
  - risk/authority-pollution
---

# AxDSan/mnemosyne Architecture Review

## One-Line Judgment

Mnemosyne is worth preserving as a strong candidate reference for VAKS's derived retrieval/cache and context-pack preparation layer, but it should be rejected as a truth store, review authority, or evidence-support engine.

## Problem It Solves

Mnemosyne attempts to give agents a local memory system that can remember working context, consolidate episodic memories, retrieve semantically and lexically, expose facts/triples, and integrate with agent runtimes such as Hermes and MCP.

The important architecture move is local-first memory in SQLite:

- Working memory for hot context.
- Episodic memory for long-term consolidated memory.
- sqlite-vec for dense retrieval.
- FTS5 for keyword retrieval.
- Importance, recency, binary vectors, triples, facts, temporal logic, cache, and diagnostics around that base.

## Why It Matters To VAKS

VAKS already separates truth authority from retrieval/activation. Mnemosyne gives concrete implementation patterns for the activation side:

- Derived local indexes over durable records.
- Multiple retrieval voices rather than only vector search.
- Embedding refresh and stale-index cleanup.
- Diagnostics for vector/index state.
- Agent memory integration patterns that VAKS can quarantine.

The architecture is most relevant to:

- `retrieval/cache`
- `context-pack-preparation`
- `association-neighborhood-activation`
- `agent-access-read-only`
- `maintenance-lint`

It is least relevant to:

- reviewed truth creation
- evidence review
- decision authority
- claim confidence changes

## Source And Code Anchors

| Area | Anchor | What it shows |
|---|---|---|
| Hybrid architecture | `README.md:242-255`, `docs/architecture.md:48-51` | SQLite, sqlite-vec, FTS5, importance, binary vector compression. |
| Vector modes | `README.md:284`, `mnemosyne/core/beam.py:393` | Vector type can be `float32`, `int8`, or `bit`. |
| sqlite-vec setup | `mnemosyne/core/beam.py:432`, `mnemosyne/core/beam.py:626` | sqlite-vec extension load and `vec_episodes` virtual table. |
| FTS5 setup | `mnemosyne/core/beam.py:633-668` | FTS5 tables and triggers for episodic and working memory. |
| Fallback embeddings | `mnemosyne/core/beam.py:799-831` | JSON embedding table when sqlite-vec is unavailable. |
| Vector insert/search | `mnemosyne/core/beam.py:1710-1720`, `mnemosyne/core/beam.py:1756-1766` | sqlite-vec binary/int8/float32 insert and search paths. |
| Embedding providers | `mnemosyne/core/embeddings.py:1-4`, `mnemosyne/core/embeddings.py:126-142` | local fastembed and API embedding support. |
| Embedding cache | `mnemosyne/core/embeddings.py:188-207`, `mnemosyne/core/embeddings.py:235-253` | availability gates and cached query embedding. |
| Binary vectors | `mnemosyne/core/binary_vectors.py:92-115`, `mnemosyne/core/binary_vectors.py:184-210` | sign-threshold bit packing and exhaustive Hamming search. |
| Main recall | `mnemosyne/core/beam.py:4287-4304`, `mnemosyne/core/beam.py:4859-4972` | recall merges working/episodic, vector/FTS/importance, and binary-vector scoring. |
| Embedding lifecycle | `mnemosyne/core/beam.py:6398-6458` | content changes refresh or clear stale embedding stores. |
| Polyphonic recall | `mnemosyne/core/polyphonic_recall.py:135-160`, `mnemosyne/core/polyphonic_recall.py:694-737` | vector, graph, fact, temporal voices with RRF and diversity rerank. |
| Query cache | `mnemosyne/core/query_cache.py:4-12`, `mnemosyne/core/query_cache.py:167-251` | exact, semantic, composite, synonym, and full-search cache tiers. |
| Comparison honesty | `docs/comparison.md:63`, `docs/comparison.md:201` | Mnemosyne is simpler than Hindsight and its latency advantage is architectural. |

## Architecture Shape

```text
agent / app call
-> working memory
-> episodic memory
-> embedding provider
-> sqlite-vec / memory_embeddings / binary_vector
-> FTS5
-> graph / facts / temporal hints
-> hybrid or polyphonic recall
-> cached and diagnostic retrieval result
```

For VAKS, this maps to:

```text
vault markdown truth
-> derived source/candidate/reviewed indexes
-> bucket-aware retrieval
-> activation neighborhood
-> context-pack candidate set
-> evidence-aware review or action-basis gate when needed
```

## Strong Borrow Candidates

### Derived retrieval index with explicit degradation

Mnemosyne checks available embedding/vector infrastructure and provides fallback paths. VAKS should borrow this as a rule: if a derived semantic index is stale, missing, or unavailable, it must degrade visibly instead of pretending recall is complete.

VAKS adaptation:

- Each vector row should include source path, source hash, source status, point id, and authority bucket.
- If a source hash changes, vector rows become stale.
- If embedding generation fails, semantic recall is unavailable for that item, not silently trusted.

### Hybrid retrieval inside authority buckets

Vector plus FTS plus importance is useful, but VAKS must apply bucket filters first.

VAKS adaptation:

```text
scope/project filter
-> authority bucket filter
-> vector/FTS/recency/importance ranking
-> context-pack warning labels
```

This preserves the existing VAKS rule that activation is not truth.

### Polyphonic recall as activation neighborhood

Vector/graph/fact/temporal voices are a good match for Association Neighborhood Activation. VAKS can refine the voice split:

- Source/text voice for exact anchors.
- Candidate point voice for draft ideas.
- Reviewed relation voice for vetted context.
- Temporal applicability voice for stale/superseded checks.
- Risk/inhibition voice for action-basis warnings.

### Embedding lifecycle hygiene

The embedding refresh/cleanup code is one of the most directly useful lessons. VAKS needs the same discipline for any future cache or derived index.

Potential VAKS maintenance checks:

- `source_hash_missing`
- `derived_index_stale`
- `embedding_provider_unavailable`
- `authority_bucket_missing`
- `context_pack_cache_unscoped`

## Watch Or Adapt Carefully

### Binary vectors

The binary vector layer is attractive for local speed/storage, but its implementation is sign-threshold binarization plus Hamming distance. This can be useful, but it is not automatically higher-quality semantic search.

VAKS should only test it as an optional storage mode after a small local benchmark with mixed Chinese/English notes, candidate points, reviewed claims, and source cards.

### Query cache

The cache tiers are useful, but VAKS invalidation is harder than a normal agent memory cache. Cache keys must include:

- project or query scope
- source hash
- candidate/reviewed bucket
- reviewed relation version
- template/context-pack version
- risk/action-basis mode

### Benchmark claims

The benchmark docs are valuable because they include caveats and reliability gates. Still, VAKS should treat all benchmark numbers as source claims, not evidence, until reproduced or independently reviewed.

## Reject As Direct Adoption

Reject these as VAKS core moves:

- Using Mnemosyne as the Markdown truth store.
- Letting memory writes create reviewed claims.
- Letting vector similarity create confidence.
- Letting automatic triples create reviewed relations.
- Treating benchmark deltas as adoption evidence.
- Combining raw/candidate/reviewed/overlay content in one unlabelled relevance list.

## Candidate Point Calibration

| Candidate point | VAKS fit | Review question | Current judgment |
|---|---:|---|---|
| SQLite-local hybrid retrieval can power derived cache. | High | Can it preserve authority buckets and source hashes? | Strong candidate. |
| Polyphonic recall can implement activation neighborhoods. | High | Can risk/review/temporal voices be made explicit? | Strong candidate. |
| Binary vectors are useful for storage/speed. | Medium | What is recall loss on VAKS corpus? | Watch/adapt. |
| Embedding refresh is required maintenance hygiene. | High | How should stale vector rows be surfaced? | Strong candidate. |
| Agent memory integration is useful. | Medium | Can writes be quarantined into candidate/feedback only? | Later, gated. |

## Direct Answer On Vector Sophistication

Advanced:

- Local-first SQLite vector/FTS hybrid design.
- Multiple vector storage formats.
- Fallback embedding paths.
- Binary vector compression.
- Multi-voice recall and deterministic fusion.
- Embedding lifecycle cleanup.
- Diagnostics and benchmark hygiene.

Not advanced in the vector-database sense:

- No inspected cross-encoder reranking.
- No learned fusion.
- No mature external ANN/vector DB serving layer.
- Binary search path is compact exhaustive Hamming search, not a high-end ANN index.
- Entity normalization and automatic conflict detection remain gaps.

## VAKS Adoption Posture

Recommended posture:

```text
design-only candidate
-> keep as retrieval/cache inspiration
-> prototype only behind derived-index boundary
-> require bucket-aware scoring before any context-pack use
-> never promote vector/cache scores to truth or evidence support
```

Do not promote this review to a pattern or decision without a separate evidence-aware review and, ideally, a small VAKS-local retrieval experiment.

