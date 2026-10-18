---
record_kind: source_annotation
annotation_id: ann-linxiv-006-vault-path-containment
status: candidate
knowledge_status: candidate
processing_tier: light
annotation_scope: source_local_anchor
source_ref: "raw/repos/2026-06-23-linxiv-dev-linXiv-source.md"
source_snapshot_ref: "raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip"
selector_type: file_line_range
selector_value: "service/vault.py:1-20; service/vault.py:34-55; service/vault.py:129-148; service/vault.py:195-197"
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

# Source Annotation：editor vault path containment

## Locator

```text
raw/repos/_snapshots/2026-06-23-linxiv-dev-linXiv-8085eeb-source.zip
service/vault.py:1-20
service/vault.py:34-55
service/vault.py:129-148
service/vault.py:195-197
```

## Why Pin This

linXiv's editor vault service documents root-relative paths, rejects path escape,
and treats on-disk editor files as a bounded per-note vault.

This is useful if VAKS later builds an editor/workbench or runtime artifact
surface that performs file operations.

## Boundary

This is a file-operation safety locator. It is not evidence support, reviewed
knowledge, or permission to add VAKS runtime file operations.
