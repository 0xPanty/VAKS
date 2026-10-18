---
record_kind: candidate_distillation
type: review-candidate
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: confirmed
review_pressure: none
derived_from:
  - raw/articles/2026-06-07-blakecrosley-obsidian-mcp-hybrid-retrieval-source.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
project: verified-action-knowledge-system
scope: blakecrosley-obsidian-mcp-hybrid-retrieval-distillation
source_checked_at: 2026-06-07
borrow_value: strong
borrow_order:
  - "P1: hybrid retrieval with lexical + vector + fusion for vault context lookup"
  - "P1: index hygiene, .indexignore-style exclusion, and credential filtering before indexing"
  - "P1: read-first, path-scoped MCP results with token limits and source spans"
  - "P2: note/frontmatter/chunk design as retrieval quality control"
  - "P2: cached context blocks and compression for context-pack budget control"
  - "P3: concrete implementation choices as later runtime references"
avoid:
  - "Do not treat retrieval rank as trust, truth, or relation strength."
  - "Do not enable MCP write tools from this source."
  - "Do not index secrets, credentials, private account data, or ignored files."
  - "Do not treat version/performance claims as verified without code/runtime checks."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Implementing VAKS retrieval cache, MCP read surface, or context-pack retrieval."
  support_when: "Designing vault search, index hygiene, source snippets, token budgets, or read-only agent access."
  risk_when: "Any proposal lets retrieval results, embeddings, or MCP output become authority."
  cold_references:
    - raw/articles/2026-06-07-blakecrosley-obsidian-mcp-hybrid-retrieval-source.md
routing_hint:
  - retrieval-cache
  - mcp-read-boundary
  - source-hygiene
  - context-pack
possible_project_refs:
  - SOURCE_INTAKE.md
  - SCHEMA.md
  - IMPLEMENTATION_BLUEPRINT.md
  - DEV_CONTEXT.md
point_anchor_refs:
  - source_ref: raw/articles/2026-06-07-blakecrosley-obsidian-mcp-hybrid-retrieval-source.md
    selector_type: page-section
    selector_value: "retrieval / MCP / index hygiene sections observed 2026-06-07"
tags:
  - candidate
  - provisional
  - article-distillation
  - obsidian
  - retrieval-runtime
borrow_tags:
  - P1/hybrid_retrieval_bm25_vector_rrf
  - P1/indexignore_and_credential_filtering
  - P1/read_first_path_scoped_mcp
  - P2/note_shape_as_retrieval_quality_control
  - P2/context_compression_and_cached_blocks
  - P3/runtime_implementation_reference
do_not_borrow_tags:
  - avoid/retrieval_rank_as_trust
  - avoid/mcp_write_access_default
  - avoid/secrets_in_index
  - avoid/performance_claim_without_runtime_check
---

# Blake Crosley Obsidian MCP Hybrid Retrieval Candidate Distillation

## Boundary

This is candidate orientation from a public web article.

It is not reviewed knowledge, not a VAKS implementation decision, and not action basis.

## Plain-Language Takeaway

说人话：这篇最有用的不是“Obsidian 怎么记笔记”，而是“AI 查 Obsidian 时怎么查得准、查得安全”。

VAKS 可以借它做未来检索层参考：

```text
vault text -> filtered index -> lexical + vector retrieval -> fused result -> path/snippet/token-limited context
```

但结果只能当 context candidate，不能当 evidence support 或 truth。

## Candidate Points

### 1. Hybrid retrieval should be a derived runtime layer

BM25 / lexical search and vector search solve different recall problems. Fusion can improve candidate context selection, but it remains derived cache behavior.

### 2. Index hygiene is a safety boundary

Ignored paths, credentials, private files, generated junk, and plugin/runtime artifacts must be excluded before indexing or embedding.

### 3. MCP should start read-first and path-scoped

Useful MCP shape for VAKS is:

```text
query -> ranked paths/snippets/source anchors -> token-limited context
```

Not:

```text
query -> arbitrary vault write / shell / plugin execution
```

### 4. Note shape affects retrieval quality

Frontmatter, headings, chunks, and local anchors affect whether future search retrieves the right material.

## Open Questions

- Should VAKS first implement plain FTS/BM25 before vector search?
- What paths must be permanently excluded from indexing?
- What is the minimum path/snippet format for future context packs?
