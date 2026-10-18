---
type: source
record_kind: source_record
status: source-captured
title: "AxDSan/mnemosyne"
source_id: "github:AxDSan/mnemosyne@17a7dda350cc3d3fd599c53209bd4a15c8713bf0"
source_uri: "https://github.com/AxDSan/mnemosyne"
source_url: "https://github.com/AxDSan/mnemosyne"
source_type: repository
author: "AxDSan / Abdias J"
publisher: GitHub
published_at: "2026-04-05T14:59:04Z"
updated_at: "2026-06-10T16:28:47Z"
pushed_at: "2026-06-10T16:23:39Z"
captured_at: "2026-06-11"
captured_by: Codex
version_or_commit: "17a7dda350cc3d3fd599c53209bd4a15c8713bf0"
checked_commit: "17a7dda350cc3d3fd599c53209bd4a15c8713bf0"
checked_commit_time: "2026-06-10T18:22:19+02:00"
checked_commit_subject: "fix(install): migrate old installer from hermes-mnemosyne -> mnemosyne plugin dir"
language: Python
license: MIT
github_stars_at_capture: 1042
github_forks_at_capture: 98
github_open_issues_at_capture: 0
github_topics:
  - agents
  - ai
  - hermes
  - hermes-agent
  - ml
  - nousresearch
source_integrity:
  source_hash_kind: git_commit
  source_hash: "17a7dda350cc3d3fd599c53209bd4a15c8713bf0"
  snapshot_path: "raw/repos/_snapshots/2026-06-11-AxDSan-mnemosyne-17a7dda-source.zip"
  snapshot_sha256: "64D75268048390B355AD372F14B674DEABA3A1CFB591EBF52FA0DA86B007D35A"
  ingest_state: new
adapter_ingest:
  adapter_name: "git+github-api"
  adapter_version: "GitHub REST metadata + git clone --depth 1 + git archive"
  capture_method: "public GitHub API metadata, shallow git clone, local source inspection, archived snapshot"
  extraction_trace:
    - "README.md"
    - "docs/architecture.md"
    - "docs/comparison.md"
    - "docs/beam-benchmark.md"
    - "docs/benchmark-results-analysis.md"
    - "mnemosyne/core/beam.py"
    - "mnemosyne/core/embeddings.py"
    - "mnemosyne/core/binary_vectors.py"
    - "mnemosyne/core/polyphonic_recall.py"
    - "mnemosyne/core/mmr.py"
    - "mnemosyne/core/query_cache.py"
  known_limits:
    - "No runtime tests or benchmarks were executed during this intake."
    - "Repository benchmark claims are self-reported and not reproduced here."
    - "GitHub metadata is a capture-time snapshot and can drift."
source_status: active
raw_location: "raw/repos/_snapshots/2026-06-11-AxDSan-mnemosyne-17a7dda-source.zip"
processing_mode: immediate
processing_level: heavy
processing_tier: heavy
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
formalization_status: raw-only
review_priority: high
review_owner: Codex
topics:
  - local-first-memory
  - sqlite-vec
  - fts5
  - hybrid-retrieval
  - binary-vector
  - embedding-lifecycle
  - polyphonic-recall
  - query-cache
  - agent-memory-quarantine
  - context-pack-preparation
projects:
  - verified-action-knowledge-system
source_family: repo-ai-memory-layer
verification_status: unverified
candidate_outputs:
  - "outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md"
  - "wiki/summaries/2026-06-11-AxDSan-mnemosyne-architecture-review.md"
  - "outputs/review/project_lens_overlays/2026-06-11-mnemosyne-vector-memory-layer.md"
tags:
  - source/repo
  - status/raw
  - vaks/retrieval-cache
  - vaks/context-pack
  - vaks/agent-memory-quarantine
  - vector/sqlite-vec
  - vector/binary
  - retrieval/hybrid
  - retrieval/fts5
  - retrieval/polyphonic
  - boundary/not-action-basis
---

# AxDSan/mnemosyne Source Record

## Capture Reason

The user explicitly requested strong VAKS distillation and asked whether the repository's vector technology is advanced. This source is therefore captured as a heavy candidate reference for VAKS retrieval/cache and context-pack preparation, not as reviewed knowledge or an action basis.

## Source Identity

- Repository: `AxDSan/mnemosyne`
- URL: <https://github.com/AxDSan/mnemosyne>
- Checked commit: `17a7dda350cc3d3fd599c53209bd4a15c8713bf0`
- Checked commit time: `2026-06-10T18:22:19+02:00`
- Default branch at capture: `main`
- Capture metadata: public GitHub API, `git ls-remote`, shallow local clone, source snapshot zip
- Snapshot: `raw/repos/_snapshots/2026-06-11-AxDSan-mnemosyne-17a7dda-source.zip`
- Snapshot SHA256: `64D75268048390B355AD372F14B674DEABA3A1CFB591EBF52FA0DA86B007D35A`

## Source Claim Surface

The project presents itself as a zero-dependency, sub-millisecond AI memory system for Hermes agents and others. Its public architecture centers on SQLite-backed memory, working memory, episodic memory, triples, sqlite-vec, FTS5, binary vector compression, and hybrid recall.

Important self-claims and documentation anchors:

- README architecture shows SQLite-backed working memory, episodic memory, triples, sqlite-vec, FTS5, and MIB binary vectors: `README.md:242`, `README.md:250`, `README.md:253`, `README.md:255`.
- Configurable vector type is exposed through `MNEMOSYNE_VEC_TYPE` with `float32`, `int8`, and `bit`: `README.md:284`.
- Hybrid weighting is documented as vector similarity, FTS5 rank, and importance: `docs/architecture.md:48-51`, `docs/comparison.md:79`.
- The comparison doc openly says Hindsight has a more sophisticated retrieval stack with cross-encoder rerank, while Mnemosyne is simpler by choice: `docs/comparison.md:63`.
- The comparison doc frames Mnemosyne's advantage as in-process SQLite latency, not necessarily retrieval-quality superiority: `docs/comparison.md:201`.
- Benchmark notes say FTS5 and vector search were active in the BEAM run: `docs/beam-benchmark.md:74`.
- Benchmark analysis emphasizes reliability gates such as pure-recall flags, fallback rates, and extraction success before trusting deltas: `docs/benchmark-results-analysis.md`.

## Code Anchors

Core vector and retrieval implementation anchors:

- Embedding provider layer:
  - Local `fastembed` plus OpenAI-compatible API fallback surface: `mnemosyne/core/embeddings.py:1-4`, `mnemosyne/core/embeddings.py:45-52`.
  - Lazy local model loading and cache directory: `mnemosyne/core/embeddings.py:126-142`.
  - Dense retrieval availability gates and LRU query embedding cache: `mnemosyne/core/embeddings.py:188-207`, `mnemosyne/core/embeddings.py:235-253`.
- Binary vector layer:
  - Binary vector store and SQLite schema: `mnemosyne/core/binary_vectors.py:56-88`.
  - MIB is implemented as sign-threshold binarization and bit packing: `mnemosyne/core/binary_vectors.py:92-115`.
  - Hamming distance and normalized score: `mnemosyne/core/binary_vectors.py:119-157`.
  - Default search is exhaustive over binary vectors: `mnemosyne/core/binary_vectors.py:184-210`.
  - Optional batched numpy Hamming search: `mnemosyne/core/binary_vectors.py:268-301`.
- BEAM/SQLite recall layer:
  - Vector type controlled by `MNEMOSYNE_VEC_TYPE`: `mnemosyne/core/beam.py:393`.
  - sqlite-vec extension loading: `mnemosyne/core/beam.py:432`.
  - sqlite-vec virtual table for episodic embeddings: `mnemosyne/core/beam.py:626`.
  - FTS5 virtual tables and triggers: `mnemosyne/core/beam.py:633-668`.
  - JSON embedding fallback table: `mnemosyne/core/beam.py:799-831`.
  - sqlite-vec insert paths for binary, int8, and float32: `mnemosyne/core/beam.py:1710-1720`.
  - sqlite-vec search paths for binary, int8, and float32: `mnemosyne/core/beam.py:1756-1766`.
  - Main recall entry point documents sqlite-vec plus FTS5 for episodic memory and FTS5 for working memory: `mnemosyne/core/beam.py:4287-4304`.
  - Episodic recall combines vector/FTS/importance and binary-vector bonuses: `mnemosyne/core/beam.py:4859-4972`.
  - Embedding refresh removes or regenerates stale vector stores when content changes: `mnemosyne/core/beam.py:6398-6458`.
- Polyphonic recall:
  - Four retrieval voices are combined: vector, graph, fact, temporal: `mnemosyne/core/polyphonic_recall.py:135-160`.
  - RRF fusion and diversity rerank are implemented deterministically: `mnemosyne/core/polyphonic_recall.py:694-737`.
  - Diagnostics surface vector voice and graph/consolidation stats: `mnemosyne/core/polyphonic_recall.py:807`.
- Cache/rerank helpers:
  - Query cache has exact, embedding, composite, synonym, and full-search tiers: `mnemosyne/core/query_cache.py:4-12`.
  - Cache TTL and size defaults: `mnemosyne/core/query_cache.py:43-49`.
  - Cache lookup combines exact, semantic cosine, Jaccard, and synonym matching: `mnemosyne/core/query_cache.py:167-251`.
  - MMR helper uses lexical Jaccard novelty, not neural reranking: `mnemosyne/core/mmr.py:26-55`.

## Initial VAKS-Fit Read

This source is strongly relevant to VAKS as retrieval/cache architecture inspiration. It is not strongly relevant as a truth model, review model, or evidence authority.

High-fit areas:

- Derived retrieval/cache layer for raw/candidate/reviewed buckets.
- Context-pack preparation and activation support.
- Embedding lifecycle hygiene for derived indexes.
- Local-first SQLite deployment option.
- Retrieval diagnostics and benchmark hygiene.

Low-fit or rejected areas:

- Treating agent memory as reviewed knowledge.
- Letting vector similarity create support, confidence, or reviewed relations.
- Mixing raw, candidate, overlay, and reviewed material in one undifferentiated relevance ranking.
- Borrowing benchmark claims as evidence before local reproduction.

## Candidate Tags For VAKS

- `retrieval-cache`
- `sqlite-vec`
- `fts5`
- `hybrid-retrieval`
- `binary-vector`
- `embedding-lifecycle`
- `polyphonic-recall`
- `association-neighborhood-activation`
- `context-pack-preparation`
- `retrieval-diagnostics`
- `agent-memory-quarantine`
- `local-first-memory`
- `candidate-not-action-basis`

## Processing Boundary

This record is raw provenance plus capture metadata. It can be used to locate and inspect the source. It must not be used as reviewed truth, action basis, or adoption approval.

