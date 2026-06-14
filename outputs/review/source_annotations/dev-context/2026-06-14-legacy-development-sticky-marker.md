---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-2026-06-14-legacy-development-sticky-marker
source_ref: DEV_CONTEXT.md
working_copy_ref:
external_annotation_id:
selector_type: TextQuoteSelector
selector_exact: "Legacy marker: this development context/workbench area may still contain old"
selector_prefix: "## 0. Legacy Development Sticky Marker"
selector_suffix: "project-tag or sticky-note language."
selector_position:
selector_timestamp_start:
selector_timestamp_end:
selector_page:
selector_rect:
content_hash:
anchor_status: exact_verified
annotation_role: implementation_note
body_note: "Marks the old development sticky-note/project-tag habit as legacy. Future source-level insights should use Source Annotation Sidecar."
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs: []
project_overlay_refs: []
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: annotation_not_support
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - source-annotation
  - legacy-dev-workbench-marker
---

# Legacy Development Sticky Marker

## Boundary

This annotation marks the old development sticky-note / project-tag habit as
legacy working material.

It is not reviewed knowledge, not evidence support, not a Project Overlay
verdict, and not action basis.

## Intended Use

Future agents should stop adding loose "useful for VAKS" notes to the old
development area.

Use:

```text
source-level useful span -> Source Annotation Sidecar
project-level borrow / non-borrow -> Project Overlay
review or action support -> Evidence Packet
```
