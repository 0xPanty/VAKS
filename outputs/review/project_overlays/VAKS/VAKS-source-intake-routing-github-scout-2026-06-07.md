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
project_id: VAKS
target_ref: outputs/review/2026-06-07-source-intake-routing-github-scout-candidate-distillation.md
target_selector: "Candidate Points"
target_hint: "path=outputs/review/2026-06-07-source-intake-routing-github-scout-candidate-distillation.md; heading=Practical Design Takeaway"
project_borrow_scope: "Use as candidate guidance for the source-intake-routing Obsidian workbench front door, source route sections, metadata/router filters, trace/clickback display, and context-pack item fields."
project_non_borrow_scope: "Do not adopt Dify, RAGFlow, AnythingLLM, LlamaIndex, or Haystack as VAKS core; do not turn parser/connector/chunk/citation objects into reviewed knowledge; do not use star counts as authority."
project_reopen_trigger: "Reopen when building source-intake-routing Obsidian entrypoint, source_route field proposal, or context pack builder v1."
confirmation_basis: "User requested GitHub scout for source-intake-routing; 5 repos checked via GitHub API and raw anchors on 2026-06-07."
last_checked_at: 2026-06-07
expires_at: 2026-07-07
---

# Project Overlay: VAKS Source-Intake-Routing GitHub Scout

## Boundary

This is a VAKS project-scoped sidecar.

It does not rewrite the source cards, candidate distillation, reviewed notes,
decisions, or patterns.

It can guide the active `source-intake-routing` sandbox, but it cannot act as
reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-07-source-intake-routing-github-scout-candidate-distillation.md
target_selector: Candidate Points
target_hint: path + heading locator for the next sandbox workbench step
```

## Project Borrow Scope

For VAKS, borrow these only as candidate workbench ideas:

```text
1. Source route front door:
   repo, article, paper, video, Obsidian, website, GitHub, document upload.

2. Route-specific recipe:
   each source route can have a small path, not one mandatory heavy pipeline.

3. Metadata/router as retrieval helper:
   use after authority/status/path filters, never as truth.

4. Context pack trace/clickback:
   show source type, lane, selector, warning, and action_basis_allowed.

5. Parser/connector humility:
   parser/OCR/connector/chunk metadata are source hygiene, not evidence support.
```

## Project Non-Borrow Scope

Do not currently borrow:

```text
full Dify/RAGFlow/AnythingLLM platform stack
mandatory vector database or document store
mandatory connector runtime
agent workflow engine
automatic source-to-truth pipeline
star-count-based priority
citation UI as evidence support
chunk metadata as reviewed support
```

This is not a universal ban. It is the current VAKS sandbox boundary.

## Reopen Trigger

Reopen when:

```text
source-intake-routing Obsidian entrypoint is being drafted
source_route field is proposed for source cards
context pack builder v1 needs item fields
we compare actual workbench UX across Dify/RAGFlow/AnythingLLM
```

## Confirmation

```yaml
confirmation_basis:
  - user explicitly requested GitHub scout and Obsidian/VAKS distillation
  - 5 repos checked with GitHub API metadata
  - raw source cards created with commit anchors
last_checked_at: 2026-06-07
expires_at: 2026-07-07
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
