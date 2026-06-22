---
type: candidate_distillation
record_kind: candidate_distillation
status: candidate
title: "AxDSan/mnemosyne candidate distillation for VAKS"
source_ref: "raw/repos/2026-06-11-AxDSan-mnemosyne-source.md"
source_id: "github:AxDSan/mnemosyne@17a7dda350cc3d3fd599c53209bd4a15c8713bf0"
source_uri: "https://github.com/AxDSan/mnemosyne"
created_at: "2026-06-11"
created_by: Codex
processing_tier: heavy
knowledge_status: candidate
overlay_state: none
truth_status: not_reviewed
evidence_status: source_code_inspected_not_reproduced
action_basis_allowed: false
truth_mutation_allowed: false
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
borrow_value: strong
borrow_order:
  - "derived retrieval/cache layer"
  - "context-pack preparation and activation diagnostics"
  - "embedding lifecycle hygiene"
  - "sqlite local-first vector adapter"
  - "agent memory integration only after quarantine rules"
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "VAKS is implementing a derived retrieval/cache adapter with bucket-aware authority boundaries."
  support_when: "The task is about activation, recall diagnostics, context-pack candidate assembly, or local-first vector storage."
  risk_when: "A proposal treats vector ranking, agent memory, or benchmark claims as reviewed evidence or action basis."
  cold_references:
    - "Hermes/MCP integration details"
    - "OpenWebUI/OpenClaw integrations"
    - "End-user memory-bank UX"
routing_hint:
  - retrieval-cache
  - context-pack-preparation
  - association-neighborhood-activation
  - agent-memory-quarantine
  - maintenance-lint
tags:
  - candidate
  - vaks/retrieval-cache
  - vaks/context-pack
  - vaks/activation-not-truth
  - vector/sqlite-vec
  - vector/binary
  - retrieval/hybrid
  - retrieval/polyphonic
  - cache/query
  - risk/authority-pollution
provisional: true
---

# AxDSan/mnemosyne Candidate Distillation

## Short Answer

Mnemosyne's vector technology is advanced as a compact local agent-memory retrieval layer, not advanced as a general-purpose vector database.

The strongest part is not one single algorithm. The valuable part is the system composition: SQLite plus sqlite-vec, FTS5, importance weighting, fallback JSON embeddings, binary vectors, query caching, graph/fact/temporal recall voices, diagnostics, and embedding refresh hygiene. For VAKS, this is very useful as retrieval/cache and context-pack preparation inspiration.

The weak boundary is also clear: it should not become VAKS truth storage, review authority, or evidence support. Vector recall can activate context; it cannot prove a point.

## What Is Actually Advanced

### 1. Local-first hybrid retrieval stack

Mnemosyne keeps retrieval in SQLite rather than outsourcing everything to a network vector database. The documented stack combines sqlite-vec, FTS5, and importance weighting, and the code backs that with `vec_episodes`, FTS5 virtual tables, and a fallback `memory_embeddings` table.

Why this matters to VAKS:

- It fits a derived index/cache layer over Markdown truth.
- It can support fast local context-pack candidate assembly.
- It keeps retrieval infrastructure simpler and more inspectable than a separate vector DB service.

VAKS tag fit:

- `retrieval-cache`
- `sqlite-vec`
- `fts5`
- `hybrid-retrieval`
- `context-pack-preparation`

Boundary:

- The hybrid score must remain activation score, not support score or truth confidence.

### 2. Multiple vector representations with graceful fallback

The repo supports `float32`, `int8`, and `bit` vector modes, probes sqlite-vec capability, and keeps JSON embedding fallback paths. This is valuable engineering because the system degrades instead of silently breaking.

Why this matters to VAKS:

- VAKS can borrow the idea of derived-index capability probing.
- If a vector extension fails, retrieval should fall back to lexical/source traversal, not return misleading semantic hits.
- The embedding lifecycle code that refreshes or removes stale embeddings is directly relevant to VAKS index hygiene.

VAKS tag fit:

- `embedding-lifecycle`
- `derived-index-hygiene`
- `retrieval-diagnostics`
- `maintenance-lint`

Boundary:

- Derived index health is process evidence. It is not reviewed knowledge.

### 3. Binary vectors as a storage/speed tradeoff

The MIB layer compresses embeddings by sign-thresholding dimensions and packing bits, then uses Hamming distance. This is clever and practical, especially for local memory with limited resources.

But this is not state-of-the-art vector search in the HNSW/PQ/IVF sense. It is a compact exhaustive binary scan or batched Hamming shortcut. It likely trades semantic precision for storage and speed.

VAKS tag fit:

- `binary-vector`
- `local-first-memory`
- `retrieval-cache`

Borrow grade:

- Watch/adapt, not adopt by default.

Boundary:

- Do not label MIB as "better vector search" until VAKS has local recall tests against its own note types.

### 4. Polyphonic recall as activation, not evidence

The polyphonic recall path combines vector, graph, fact, and temporal voices with deterministic RRF and diversity reranking. This is more advanced than simple vector search and maps well to VAKS's existing Association Neighborhood Activation idea.

Why this matters to VAKS:

- Vector voice can find semantic neighbors.
- Graph/fact voice can surface related candidate or reviewed structures.
- Temporal voice can reduce stale activation.
- RRF fusion can prepare context candidates before a human/model answer.

VAKS tag fit:

- `association-neighborhood-activation`
- `polyphonic-recall`
- `context-pack-preparation`
- `temporal-applicability-check`

Boundary:

- RRF and voice scores cannot create support, confidence, or reviewed relations.

### 5. Query cache and diagnostics

The query cache has exact, embedding, composite, synonym, and full-search tiers. This can reduce repeated context-pack assembly cost. The diagnostic layer can expose vector counts and retrieval health.

Why this matters to VAKS:

- Retrieval cache is a good support surface for repeated research/project work.
- Cache entries should be scoped to project, bucket, source version, and review boundary.
- Cache invalidation must be strict when a source card, candidate point, reviewed claim, or decision changes.

VAKS tag fit:

- `query-cache`
- `context-pack-cache`
- `retrieval-diagnostics`
- `maintenance-lint`

Boundary:

- Cache hits are not evidence. Cache hits are only reuse of previous retrieval work.

## What Is Not Advanced Enough To Borrow Blindly

- No cross-encoder rerank in the inspected retrieval path.
- No learned fusion weights in the inspected retrieval path.
- Binary vector search is compact, but not a mature vector DB index strategy.
- Entity normalization and conflict detection are listed by the repo itself as gaps in comparison docs.
- Benchmark claims are self-reported and not reproduced in this intake.
- End-to-end BEAM comparison is not fully apples-to-apples because the docs note judge differences.

## VAKS-Focused Candidate Points

### Candidate Point 1: Derived retrieval should be bucket-aware before it is relevance-aware

Mnemosyne shows that local hybrid retrieval can be compact and fast, but VAKS cannot merge raw, candidate, overlay, and reviewed notes into one undifferentiated relevance pool.

VAKS adaptation:

- First filter by authority bucket.
- Then run hybrid retrieval inside allowed buckets.
- Then label every retrieved item by status.
- Then build context pack with warnings.

Candidate status: strong candidate principle.

### Candidate Point 2: Embedding lifecycle hygiene should be treated as a first-class maintenance gate

The repo's embedding refresh logic is valuable because it recognizes stale embeddings as dangerous. For VAKS, stale derived indexes can produce false activation.

VAKS adaptation:

- Every derived embedding should know source path, source hash, and candidate/review status.
- If source hash changes, derived vector rows become stale.
- If embedding provider is unavailable, semantic retrieval should degrade visibly.

Candidate status: strong candidate principle.

### Candidate Point 3: Polyphonic recall maps to Association Neighborhood Activation

The vector/graph/fact/temporal voice split is a useful implementation hint for VAKS activation.

VAKS adaptation:

- Vector voice: semantic neighbor candidates.
- Lexical/source voice: exact source anchors and names.
- Reviewed relation voice: only reviewed edges.
- Temporal voice: scope/version/applicability warnings.
- Risk voice: inhibition and action-basis warnings.

Candidate status: strong architecture inspiration.

### Candidate Point 4: Binary vectors are optional acceleration, not a truth or quality improvement

Binary vector compression is interesting for local scale and speed, but VAKS should not assume it improves recall quality.

VAKS adaptation:

- Test only as an optional retrieval-cache storage mode.
- Compare against FTS5, rg/BM25-style lexical retrieval, sqlite-vec float/int8, and hybrid scoring.
- Keep source/result traces for false positives and false negatives.

Candidate status: watch/adapt.

### Candidate Point 5: Agent memory must remain quarantined

Mnemosyne is built for agents. That is useful for future VAKS agent access, but dangerous if copied directly into knowledge authority.

VAKS adaptation:

- Agent-written memory can create candidate records or feedback events.
- Agent memory cannot directly create reviewed claims, reviewed relations, confidence changes, or action basis.
- MCP/Hermes integration belongs behind read/write policy gates.

Candidate status: strong boundary reinforcement.

## VAKS Tagging Decision

Primary tags:

- `vaks/retrieval-cache`
- `vaks/context-pack`
- `vaks/activation-not-truth`
- `vaks/agent-memory-quarantine`
- `vector/sqlite-vec`
- `vector/binary`
- `retrieval/hybrid`
- `retrieval/polyphonic`
- `cache/query`
- `risk/authority-pollution`

Do not primarily tag this as:

- `reviewed-knowledge`
- `truth-maintenance-core`
- `evidence-review-engine`
- `decision-authority`
- `source-of-truth`

## Borrow / Avoid Gradient

Borrow strongly:

- SQLite-local derived retrieval/cache architecture.
- Bucket-aware hybrid retrieval design.
- Embedding lifecycle refresh and stale-index invalidation.
- Retrieval diagnostics.
- Polyphonic recall as activation candidate assembly.

Borrow carefully:

- Binary vectors and int8/bit modes.
- Query cache thresholds and synonym expansion.
- Agent-facing memory APIs.

Avoid:

- Treating Mnemosyne memory as VAKS knowledge authority.
- Using benchmark claims as proof of quality.
- Using relevance score as evidence support.
- Letting automatic graph/fact extraction create reviewed relations.

## Open Review Questions

- Can a VAKS retrieval adapter preserve authority buckets before scoring?
- Does sqlite-vec plus FTS5 beat simple lexical search on this vault's Chinese/English mixed corpus?
- How much recall quality is lost in bit/MIB mode on actual VAKS candidate points?
- Can query cache invalidation be scoped by source hash, candidate hash, reviewed node hash, and project lens?
- Should polyphonic recall include a separate risk/inhibition voice?

## Provisional Judgment

For VAKS, Mnemosyne is a high-value candidate reference for the future retrieval/cache layer and context-pack preparation. It should be kept out of reviewed truth, evidence support, and action-basis logic.

