---
record_kind: source_annotation
annotation_id: ann-linxiv-001-namespaced-source-id
status: candidate
knowledge_status: candidate
processing_tier: light
annotation_scope: source_local_anchor
source_ref: "raw/repos/2026-06-23-linxiv-dev-linXiv-source.md"
source_snapshot_ref: "raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip"
selector_type: file_line_range
selector_value: "docs/adr/0002-namespaced-source-id.md:1-46"
anchor_status: anchored
annotation_role: candidate_seed
support_checked: false
evidence_support_status: not_checked
retrieval_policy: annotation_not_support
action_basis_allowed: false
truth_mutation_allowed: false
candidate_refs: "[outputs/review/2026-06-23-linxiv-dev-linXiv-strong-distillation.md]"
project_overlay_refs: "[outputs/review/project_overlays/2026-06-23-linxiv-dev-linXiv-vaks-local-research-library-overlay.md]"
---

# Source Annotation：provider-prefixed source identity

## Locator

```text
raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip
docs/adr/0002-namespaced-source-id.md:1-46
```

## Why Pin This

linXiv explicitly chooses provider-prefixed paper identities:

```text
arxiv:
openalex:
local:
```

This is useful for VAKS source adapter design because it separates source identity
and dedupe from later evidence/review status.

## Boundary

This annotation is a locator and candidate seed only. It does not prove a VAKS
schema decision, reviewed relation, or action basis.
