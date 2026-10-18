---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: heavy
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
target_ref: outputs/review/2026-06-11-RyanCodrai-turbovec-candidate-distillation.md
target_selector: 'candidate source: RyanCodrai/turbovec'
target_hint:
- type: workflow
  value: retrieval-cache
  status: conceptual
  anchor_version: 2026-06-11-source-review
- type: workflow
  value: context-pack-preparation
  status: conceptual
  anchor_version: 2026-06-11-source-review
- type: doc
  value: IMPLEMENTATION_BLUEPRINT.md
  status: healthy
  anchor_version: 2026-06-11-file-checked
project_borrow_scope: Use turbovec as a sandbox candidate for local derived vector
  cache and allowlist dense rerank after BM25/metadata/authority filtering.
project_non_borrow_scope: Do not use turbovec as truth store, reviewed relation engine,
  action basis, schema authority, or immediate mainline dependency.
project_reopen_trigger: Reopen after a local VAKS retrieval pilot measures recall,
  source-anchor correctness, Windows stability, update/delete behavior, and cache
  invalidation.
confirmation_basis: GitHub/PyPI/source snapshot captured 2026-06-11; no local benchmark
  yet.
last_checked_at: 2026-06-11
expires_at: 2026-08-11
review_pressure: none
legacy_overlay_compatibility: true
canonical_p0_included: false
canonical_current_lint_scope: false
legacy_storage: outputs/review/_legacy_project_lens
truth_boundary: legacy project lens compatibility artifact only; not canonical overlay;
  not reviewed knowledge; not action basis
---

# Project Overlay: turbovec Vector Retrieval Cache

## Boundary

This is a VAKS project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note,
decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or
action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-11-RyanCodrai-turbovec-candidate-distillation.md
target_selector: "candidate source: RyanCodrai/turbovec"
target_hint:
  - type: workflow
    value: retrieval-cache
    status: conceptual
    anchor_version: 2026-06-11-source-review
  - type: workflow
    value: context-pack-preparation
    status: conceptual
    anchor_version: 2026-06-11-source-review
  - type: doc
    value: IMPLEMENTATION_BLUEPRINT.md
    status: healthy
    anchor_version: 2026-06-11-file-checked
```

## Project Borrow Scope

For VAKS, borrow `turbovec` only as a candidate implementation for:

```text
local derived vector cache
compressed embedding index
stable external source/chunk ID mapping
allowlist dense rerank after BM25/metadata/authority bucket filtering
context-pack candidate retrieval
dev-context retrieval support
```

The best fit is:

```text
BM25 / metadata / SQLite filter first
-> turbovec dense rerank inside the allowed candidate set
-> return source/chunk anchors
-> evidence/review gate decides support or action readiness
```

## Project Non-Borrow Scope

Do not borrow it for:

```text
truth storage
reviewed relation creation
truth confidence
claim promotion
decision/action basis
schema authority
automatic merge into mainline dependencies
```

Do not use its README benchmarks as proof that VAKS retrieval is good enough.
Use them only as pilot design hints.

## Reopen Trigger

Reopen this overlay when one of these happens:

```text
1. A local VAKS retrieval pilot has benchmark results.
2. turbovec leaves Alpha or changes persistence/API behavior.
3. VAKS chooses an embedding model namespace and chunk ID scheme.
4. Context-pack preparation enters implementation.
```

## Confirmation

```yaml
confirmation_basis:
  repository_head: fcc1eb8e06c52764907b677128845995309219e0
  pypi_version: 0.7.1
  pypi_status_classifier: "Development Status :: 3 - Alpha"
  snapshot_sha256: ec1795bb0d4fe86ac64be41f4ae26ce4afcc34b7fe9e8f2d910b4d72643deb16
  local_benchmark: not_run
last_checked_at: 2026-06-11
expires_at: 2026-08-11
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```

