---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: verified-action-knowledge-system
target_ref: outputs/review/2026-06-07-blakecrosley-obsidian-mcp-hybrid-retrieval-candidate-distillation.md
source_card: raw/articles/2026-06-07-blakecrosley-obsidian-mcp-hybrid-retrieval-source.md
target_selector: obsidian_mcp_hybrid_retrieval
target_hint: "Use only as active-project borrowing context for retrieval cache, MCP read tools, and index hygiene."
borrow_tags:
  - P1/hybrid_retrieval_bm25_vector_rrf
  - P1/indexignore_and_credential_filtering
  - P1/read_first_path_scoped_mcp
  - P2/note_shape_as_retrieval_quality_control
  - P2/context_compression_and_cached_blocks
do_not_borrow_tags:
  - avoid/retrieval_rank_as_trust
  - avoid/mcp_write_access_default
  - avoid/secrets_in_index
project_reopen_trigger:
  - "When implementing VAKS retrieval cache or context pack retrieval."
  - "When designing MCP/API read surfaces."
  - "When defining index ignore and credential filtering policy."
confirmation_basis: "Public page observed on 2026-06-07 with HTTP 200 and HTML hash."
last_checked_at: 2026-06-07
expires_at:
---

# VAKS Overlay: Blake Crosley Obsidian MCP Hybrid Retrieval

## Boundary

This is project context only. It cannot authorize MCP writes, indexing secrets, or using retrieval rank as truth.

## Project Borrow Scope

For VAKS, borrow:

- hybrid lexical + semantic retrieval as derived context selection;
- explicit index exclusions and credential filtering;
- read-first, path-scoped MCP result shape;
- note/chunk/frontmatter design as retrieval hygiene;
- token-limited cached context blocks.

## Project Non-Borrow Scope

Do not borrow:

- retrieval score as trust;
- MCP write access;
- secrets/private files in indexes;
- unchecked performance or version claims.
