---
record_kind: source_annotation
annotation_id: ann-linxiv-003-obsidian-export
status: candidate
knowledge_status: candidate
processing_tier: light
annotation_scope: source_local_anchor
source_ref: "raw/repos/2026-06-23-linxiv-dev-linXiv-source.md"
source_snapshot_ref: "raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip"
selector_type: file_line_range
selector_value: "formats/markdown.py:123-204; linxiv_cli.py:583-590; api/app.py:1320-1333"
anchor_status: anchored
annotation_role: scope_limit
support_checked: false
evidence_support_status: not_checked
retrieval_policy: annotation_not_support
action_basis_allowed: false
truth_mutation_allowed: false
candidate_refs: "[outputs/review/2026-06-23-linxiv-dev-linXiv-strong-distillation.md]"
project_overlay_refs: "[outputs/review/project_overlays/2026-06-23-linxiv-dev-linXiv-vaks-local-research-library-overlay.md]"
---

# Source Annotation：Obsidian export is not reviewed knowledge

## Locator

```text
raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip
formats/markdown.py:123-204
linxiv_cli.py:583-590
api/app.py:1320-1333
```

## Why Pin This

linXiv has an Obsidian-flavoured Markdown exporter and CLI/API paths for project
paper export.

This is useful as a product/export reference, but it is also a VAKS scope warning:
exported paper Markdown is not reviewed knowledge.

## Boundary

Use as a locator for future export/import comparison only. Do not treat export
output as support, reviewed knowledge, or action basis.
