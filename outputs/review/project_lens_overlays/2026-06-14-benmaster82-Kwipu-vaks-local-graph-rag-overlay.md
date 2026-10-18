---
record_kind: project_overlay
type: project_lens_overlay
status: candidate
knowledge_status: candidate
processing_tier: heavy
overlay_state: confirmed
review_pressure: none
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
project_id: VAKS
project_name: "Verified Action Knowledge System / 资料库"
target_ref: "outputs/review/2026-06-14-benmaster82-Kwipu-strong-distillation.md"
target_selector: candidate_distillation
target_hint:
  - type: workflow
    value: "retrieval/local-obisidian-graph-rag-sidecar"
    status: conceptual
    anchor_version: candidate-workflow-only
  - type: source_card
    value: "raw/repos/2026-06-14-benmaster82-Kwipu-source.md"
    status: healthy
    anchor_version: "2026-06-14"
  - type: repo_snapshot
    value: "raw/repos/_snapshots/2026-06-14-benmaster82-Kwipu-908f0e4e3005-source.zip"
    status: healthy
    anchor_version: "sha256:365B39C54CDEB0D09C0817F806B95672B0E93F08BFFF3C1391C8AC10D3A9FD6A"
project_borrow_scope:
  - "Use Kwipu as a design reference for a local Obsidian/Markdown Graph RAG retrieval sidecar."
  - "Borrow wikilink/frontmatter structural triple extraction only as candidate graph fragments."
  - "Borrow vector + BM25 + temporal + optional synonym retrieval routes, but require VAKS retrieval receipts and authority buckets."
  - "Borrow derived-cache lifecycle ideas: model manifest, content-change detection, debounce, incremental update, visible rebuild."
  - "Borrow the thin FastMCP read-only `query_graph` shape for future MISA/VAKS context access."
project_non_borrow_scope:
  - "For VAKS, do not currently borrow Kwipu as the source of record because VAKS reviewed knowledge remains Markdown/YAML and review-gated."
  - "For VAKS, do not treat Kwipu extracted triples as reviewed relations because edge support requires later evidence-aware review."
  - "For VAKS, do not treat vector/BM25/temporal/synonym rank as support, confidence, or action readiness because retrieval only chooses what to inspect."
  - "For VAKS/MISA, do not expose reviewed-write MCP tools because operation receipts, permission tiers, and review gates are not in place."
  - "For VAKS, do not treat prompt citation as evidence support because support must point to independent source anchors under scope."
project_reopen_trigger:
  - "User asks to implement P1.5 retrieval receipt / local graph retrieval sandbox."
  - "MISA needs a read-only way to query the VAKS vault."
  - "A real Obsidian/VAKS fixture set is ready for graph/vector/BM25/temporal comparison."
  - "Retrieval receipt and support-boundary validators exist."
confirmation_basis:
  - "User explicitly requested strong distillation and inclusion in the total VAKS research plan."
  - "Official repo page, GitHub API metadata, local source files, and commit snapshot were inspected."
last_checked_at: "2026-06-14"
expires_at: null
borrow_value: strong
borrow_order:
  - "P1: local Graph RAG retrieval sidecar with receipts"
  - "P1: read-only MCP query bridge for MISA/VAKS context"
  - "P2: derived-cache lifecycle and model mismatch manifest"
  - "P3: multilingual temporal/BM25/synonym route ideas"
avoid:
  - "No graph triples as reviewed relations."
  - "No retrieval score as support."
  - "No MCP reviewed-write tools."
  - "No graph cache as source of record."
  - "No prompt citation as action basis."
tags:
  - project-lens
  - VAKS
  - kwipu
  - graph-rag
  - retrieval
  - mcp
  - candidate-only
legacy_overlay_compatibility: true
canonical_p0_included: false
canonical_current_lint_scope: false
legacy_storage: outputs/review/project_lens_overlays
truth_boundary: "project lens compatibility artifact only; not canonical reviewed knowledge; not action basis"
---

# Project Lens: Kwipu as VAKS Local Graph RAG Sidecar

## Boundary

This is a project-scoped sidecar. It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide future VAKS retrieval/MCP design, but it cannot act as reviewed knowledge or action basis.

## Project Borrow Scope

For VAKS, borrow Kwipu narrowly:

```text
Use it as a reference for local, read-only retrieval over Markdown/Obsidian notes.
```

Concrete borrow:

- Obsidian wikilink and YAML frontmatter structural triple extraction.
- Property-graph/vector/BM25/temporal hybrid retrieval shape.
- Fast mode vs full mode query cost split.
- Derived storage manifest for embedding-model compatibility.
- File watcher debounce and incremental update.
- Thin MCP read-only query entry.

VAKS-specific wrapper:

```text
Kwipu-like retrieval
  -> authority bucket filter
  -> retrieval receipt
  -> context pack draft
  -> support/sufficiency/action gates
```

Preferred sandbox artifact bundle:

```text
outputs/review/retrieval-sidecar-sandbox/
  structural_triples.candidate.yml
  derived_cache_manifest.example.yml
  retrieval_receipt.hybrid_graph.example.yml
  mcp_readonly_query_contract.md
  graph_rank_not_support.failure.md
  auto_triple_not_reviewed_relation.failure.md
  prompt_citation_not_action_basis.failure.md
```

## Project Non-Borrow Scope

Do not borrow:

- `storage_graph/` as VAKS source of record.
- Auto-extracted triples as reviewed relations.
- Retrieval rank as trust/confidence/support.
- Cited generated answer as action basis.
- MCP write tools for reviewed knowledge.
- Prompt-only anti-hallucination as evidence gate.
- MD5 content cache as VAKS provenance hash.

## Reopen Trigger

Reopen this overlay when:

```text
VAKS starts P1.5 local graph retrieval sandbox.
MISA needs a read-only VAKS knowledge query bridge.
Retrieval receipt validators can block rank/citation/triple over-trust.
Chinese/CJK vault fixtures are ready for quality testing.
```

## Minimal Pilot Gate

```yaml
pilot_scope: sandbox_only
inputs:
  - small_vaks_markdown_fixture
  - raw_source_card
  - candidate_distillation
  - reviewed_claim
  - project_overlay
  - stale_decision
checks:
  - authority_bucket_filter_applied_before_retrieval
  - selected_by_records_vector_bm25_temporal_graph
  - structural_triples_relation_state_candidate
  - retrieval_score_cannot_set_support
  - generated_citation_cannot_set_action_basis
  - mcp_tools_read_only
  - derived_cache_manifest_records_model_and_source_state
pass_result:
  - local_retrieval_sidecar_candidate
fail_result:
  - keep_as_design_reference_only
```

## Confirmation

```yaml
confirmation_basis:
  user_request: "强蒸馏这个然后记得放进总调研方案里"
  inspected_source:
    - raw/repos/2026-06-14-benmaster82-Kwipu-source.md
    - raw/repos/_snapshots/2026-06-14-benmaster82-Kwipu-908f0e4e3005-source.zip
  conclusion: "strong retrieval/MCP sidecar reference, not VAKS authority layer"
last_checked_at: 2026-06-14
```

