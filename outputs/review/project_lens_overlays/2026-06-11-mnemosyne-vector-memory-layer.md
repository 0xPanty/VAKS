---
type: project_overlay
record_kind: project_lens_overlay
status: candidate
title: "Mnemosyne vector memory layer overlay for VAKS"
project_id: verified-action-knowledge-system
source_ref: "raw/repos/2026-06-11-AxDSan-mnemosyne-source.md"
review_ref: "wiki/summaries/2026-06-11-AxDSan-mnemosyne-architecture-review.md"
distillation_ref: "outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md"
created_at: "2026-06-11"
created_by: Codex
knowledge_status: candidate
processing_tier: heavy
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
action_basis_allowed: false
truth_mutation_allowed: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: evidence_aware_review_required
borrow_value: strong
target_layers:
  - retrieval-cache
  - context-pack-preparation
  - association-neighborhood-activation
  - agent-memory-quarantine
  - maintenance-lint
non_target_layers:
  - reviewed-truth
  - evidence-support
  - confidence-update
  - reviewed-relation-creation
tags:
  - project-overlay
  - candidate
  - vaks/retrieval-cache
  - vaks/context-pack
  - vaks/activation-not-truth
  - vaks/agent-memory-quarantine
  - vector/sqlite-vec
  - retrieval/polyphonic
  - risk/authority-pollution
---

# Mnemosyne Vector Memory Layer Overlay For VAKS

## Overlay Purpose

This overlay records how `AxDSan/mnemosyne` should be retrieved for the Verified Action Knowledge System project. It is a project-side candidate lens, not a reviewed pattern, decision, or truth node.

Use it when discussing future VAKS retrieval/cache, context-pack preparation, local vector indexes, or agent memory quarantine.

Do not use it when answering whether a claim is true, reviewed, supported, or action-ready.

## Project-Specific Answer

For VAKS, Mnemosyne's main value is not "a better vector DB." Its value is a practical local memory architecture that can inspire a derived retrieval/cache layer:

```text
Markdown truth stays primary
-> derived SQLite retrieval cache
-> bucket-aware vector/FTS/graph/fact/temporal activation
-> context-pack candidate assembly
-> evidence-aware gate before action basis
```

## Borrow Scope

Borrow strongly:

- SQLite-local derived retrieval/cache over durable vault files.
- Hybrid vector plus FTS retrieval.
- Capability probing and visible fallback when embeddings/vector extension are unavailable.
- Embedding refresh and stale-index cleanup.
- Retrieval diagnostics.
- Polyphonic recall as activation-neighborhood assembly.

Borrow carefully:

- Binary vectors as an optional storage/speed mode.
- Query cache tiers and synonym expansion.
- Agent-facing MCP/Hermes memory APIs.

Borrow only after separate tests:

- Any claim that bit/int8 vectors are good enough for VAKS recall quality.
- Any benchmark implication that Mnemosyne is stronger than alternatives for VAKS.
- Any performance claim on Chinese/English mixed vault content.

## Non-Borrow Scope

Do not borrow:

- Mnemosyne memory as VAKS source of truth.
- Agent memory writes as reviewed knowledge.
- Vector score as evidence support.
- RRF/voice score as confidence.
- Automatic triples as reviewed relations.
- Benchmark results as adoption evidence.

## VAKS Implementation Hint

If VAKS later prototypes a retrieval cache, the adapter should start with this order:

```text
query intent
-> project/scope filter
-> authority bucket filter
-> source hash / freshness filter
-> vector + FTS + exact anchor retrieval
-> reviewed relation neighborhood only where reviewed
-> risk/stale/supersession warnings
-> context-pack candidate envelope
```

The important rule is that the bucket filter comes before relevance ranking.

## Suggested Tags For Future Retrieval

Primary:

- `retrieval-cache`
- `context-pack-preparation`
- `association-neighborhood-activation`
- `embedding-lifecycle`
- `retrieval-diagnostics`
- `agent-memory-quarantine`

Secondary:

- `sqlite-vec`
- `fts5`
- `hybrid-retrieval`
- `binary-vector`
- `polyphonic-recall`
- `query-cache`

Risk tags:

- `authority-pollution`
- `benchmark-overclaim`
- `candidate-not-action-basis`
- `activation-not-truth`

## Reopen Triggers

Reopen this overlay when:

- VAKS begins a local retrieval/cache prototype.
- `CONTEXT_PACK.md` or a context-pack builder is implemented.
- agent/MCP access to the vault is considered.
- a vector index or cache is allowed to write derived artifacts.
- a benchmark or maintenance manifest needs retrieval diagnostics.

## One Sentence For Future Context Packs

Mnemosyne is a strong candidate reference for VAKS derived retrieval/cache and activation-neighborhood engineering, but it must stay behind candidate/reviewed bucket boundaries and cannot be treated as a truth or evidence authority.

