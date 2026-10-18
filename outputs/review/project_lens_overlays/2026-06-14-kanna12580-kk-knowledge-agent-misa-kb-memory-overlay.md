---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
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
project_id: misa
target_ref: outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md
target_selector: "MISA external knowledge-base bridge scaffold"
target_hint: "MISA runtime context / external KB MCP bridge"
project_borrow_scope: "For MISA, borrow kk-knowledge-agent as a thin MCP-to-backend external knowledge-base bridge reference: small search/list tools, backend-owned retrieval core, explicit timeout/backend URL/proxy isolation, and read-first tool surface."
project_non_borrow_scope: "For project MISA, do not currently borrow kk-knowledge-agent as MISA's memory brain, VAKS truth layer, reviewed knowledge model, evidence support engine, or direct reviewed-write tool, because the repo is a lightweight RAG/MCP MVP without authority buckets, source anchors, review gates, feedback ledger, or action-basis boundaries. Reopen if a later MISA adapter adds receipts, authority labels, candidate-only write quarantine, and local benchmark evidence."
project_reopen_trigger: "Reopen when MISA starts implementing external knowledge-base tools, when agent writeback is proposed, or when a MISA answer uses retrieved chunks as action-facing support."
confirmation_basis: "User explicitly asked whether this source helps MISA use the knowledge base or improve memory; overlay is limited to MISA and is not a VAKS core adoption."
last_checked_at: 2026-06-14
expires_at:
tags:
  - misa
  - mcp
  - external-knowledge-base
---

# Project Overlay: kk-knowledge-agent for MISA

## Boundary

This is a project-scoped sidecar for MISA.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide active MISA design, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-14-kanna12580-kk-knowledge-agent-candidate-distillation.md
target_selector: MISA external knowledge-base bridge scaffold
target_hint: MISA runtime context / external KB MCP bridge
```

## Project Borrow Scope

For MISA, borrow kk-knowledge-agent only as this:

```text
small MCP tool surface
-> backend-owned retrieval core
-> external/local knowledge-base lookup
-> returned context with explicit warning labels
```

Useful details:

- `search_knowledge_base` is a good first tool shape.
- `list_knowledge_bases` is useful for operator/debug discovery.
- `add_text_document` is useful only after write quarantine exists.
- Backend should own retrieval, not the MCP server.
- Local backend calls should use explicit URL, timeout, and proxy isolation.
- MCP server/config changes may require restart or fresh agent session.

## Project Non-Borrow Scope

For project MISA, do not currently borrow kk-knowledge-agent as:

```text
MISA's memory brain
VAKS truth layer
reviewed knowledge model
evidence support engine
action-basis answer engine
direct reviewed-write tool
```

Reason:

```text
The repo is a lightweight RAG/MCP MVP.
It does not include authority buckets, source anchors, evidence packets, review gates, feedback ledger, temporal applicability, or memory lifecycle.
```

Reopen if:

```text
MISA adapter adds retrieval receipts,
authority labels,
candidate-only write quarantine,
and local benchmark evidence.
```

## Recommended MISA Adapter Shape

```yaml
tool: search_context
input:
  query: string
  scope: project_or_kb_ref
  top_k: integer
output:
  results:
    - title:
      snippet:
      source_ref:
      anchor_ref:
      authority_bucket: raw | candidate | reviewed | unknown
      usage_role: activation_only | review_input | support
      warning_code:
      action_basis_allowed: false
      retrieval_score: diagnostic_only
```

First release should expose:

```text
search_context
list_context_sources
```

Delay:

```text
add_candidate_note
log_feedback_event
add_text_document
```

until write receipts and quarantine are ready.

## Confirmation

```yaml
confirmation_basis: user asked for MISA relevance and warned not to write VAKS tags if not related
last_checked_at: 2026-06-14
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
VAKS core tag
```
