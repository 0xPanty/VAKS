---
record_kind: source_annotation
annotation_id: ann-linxiv-005-case-collision
status: candidate
knowledge_status: candidate
processing_tier: light
annotation_scope: source_local_anchor
source_ref: "raw/repos/2026-06-23-linxiv-dev-linXiv-source.md"
source_snapshot_ref: "raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip"
selector_type: zip_entry_list
selector_value: "storage/config/sql/tables/PROJECT_TO_TAG.SQL; storage/config/sql/tables/PROJECT_TO_TAG.sql; storage/config/sql/tables/TAG.SQL; storage/config/sql/tables/TAG.sql"
anchor_status: anchored
annotation_role: risk_signal
support_checked: false
evidence_support_status: not_checked
retrieval_policy: annotation_not_support
action_basis_allowed: false
truth_mutation_allowed: false
candidate_refs: "[outputs/review/2026-06-23-linxiv-dev-linXiv-strong-distillation.md]"
project_overlay_refs: "[outputs/review/project_overlays/2026-06-23-linxiv-dev-linXiv-vaks-local-research-library-overlay.md]"
---

# Source Annotation：case-colliding SQL paths

## Locator

```text
raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip
linXiv-8085eeb61d03cadeb74eff2352afc148a3fa202c/storage/config/sql/tables/PROJECT_TO_TAG.SQL
linXiv-8085eeb61d03cadeb74eff2352afc148a3fa202c/storage/config/sql/tables/PROJECT_TO_TAG.sql
linXiv-8085eeb61d03cadeb74eff2352afc148a3fa202c/storage/config/sql/tables/TAG.SQL
linXiv-8085eeb61d03cadeb74eff2352afc148a3fa202c/storage/config/sql/tables/TAG.sql
```

## Why Pin This

The local Windows clone reported path collisions, while the zip snapshot retains
both uppercase and lowercase SQL variants.

This is directly useful for VAKS repo intake hygiene: a case-insensitive checkout
may not faithfully represent all source files.

## Boundary

This is source hygiene pressure. It is not a reviewed judgment about linXiv
runtime correctness.
