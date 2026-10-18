---
record_kind: source_annotation
annotation_id: ann-linxiv-002-data-dir-source-of-truth
status: candidate
knowledge_status: candidate
processing_tier: light
annotation_scope: source_local_anchor
source_ref: "raw/repos/2026-06-23-linxiv-dev-linXiv-source.md"
source_snapshot_ref: "raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip"
selector_type: file_line_range
selector_value: "docs/adr/0014-data-dir-single-source-of-truth.md:1-68"
anchor_status: anchored
annotation_role: implementation_note
support_checked: false
evidence_support_status: not_checked
retrieval_policy: annotation_not_support
action_basis_allowed: false
truth_mutation_allowed: false
candidate_refs: "[outputs/review/2026-06-23-linxiv-dev-linXiv-strong-distillation.md]"
project_overlay_refs: "[outputs/review/project_overlays/2026-06-23-linxiv-dev-linXiv-vaks-local-research-library-overlay.md]"
---

# Source Annotation：runtime data root is explicit

## Locator

```text
raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip
docs/adr/0014-data-dir-single-source-of-truth.md:1-68
```

## Why Pin This

linXiv separates runtime data from the source checkout and makes the runtime data
directory explicit across CLI, MCP, API, and desktop app paths.

This is a useful candidate for VAKS future derived caches, indexes, or product
cockpit state.

## Boundary

Runtime data root discipline is useful engineering hygiene. It does not turn a
runtime cache or SQLite database into VAKS reviewed knowledge or source of truth.
