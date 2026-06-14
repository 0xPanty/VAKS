---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id:
source_ref:
working_copy_ref:
external_annotation_id:
selector_type:
selector_exact:
selector_prefix:
selector_suffix:
selector_position:
selector_timestamp_start:
selector_timestamp_end:
selector_page:
selector_rect:
content_hash:
anchor_status: exact_verified
annotation_role: candidate_seed
body_note:
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
  - review-input
---

# Source Annotation

## Boundary

This record is a source-local locator.

It says "inspect this span." It does not say the span supports a claim,
reviewed relation, decision, or action basis.

Inline footnotes, highlights, PDF notes, Zotero annotations, Readwise highlights,
or browser annotations may create this record. They are capture surfaces, not the
canonical data layer.

## Source Span

```yaml
source_ref:
working_copy_ref:
selector_type:
selector_exact:
selector_prefix:
selector_suffix:
selector_position:
selector_timestamp_start:
selector_timestamp_end:
selector_page:
selector_rect:
content_hash:
anchor_status:
```

## Annotation Body

```yaml
annotation_role:
body_note:
```

Allowed role intent:

```text
question
possible_support
counterexample
scope_limit
risk_signal
candidate_seed
term_definition
implementation_note
```

## Review Routing

```yaml
candidate_refs:
project_overlay_refs:
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
```

If `support_checked` becomes true, `evidence_packet_ref` must identify the
Evidence Packet or review object that performed the support check.

## Forbidden

```text
truth confidence
reviewed relation
project_borrow_scope
project_non_borrow_scope
decision outcome
action basis
```
