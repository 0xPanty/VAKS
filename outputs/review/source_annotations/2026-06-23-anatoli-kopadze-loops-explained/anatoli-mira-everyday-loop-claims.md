---
record_kind: source_annotation
annotation_id: anatoli-mira-everyday-loop-claims
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
selector_type: line_range
selector_value: "pasted-text.txt:125-137; pasted-text.txt:188-200"
selector_exact: "Mira is described as Telegram-based everyday loops/Skills with trigger/action/background execution, but author also warns not to force loops where they do not belong"
selector_prefix:
selector_suffix:
source_hash: 939BDC7966CDACAF8B9EE33B7128287697C06B61DB502ACA7F891EA120509D6E
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: risk_signal
body_note: "This span is useful for productized-loop UX, but product capability claims are unverified and should not become evidence or action basis."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-06-23-anatoli-kopadze-loops-explained-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_lens_overlays/2026-06-23-anatoli-kopadze-loops-explained-vaks-loop-overlay.md
source_digest_required: false
source_digest_ref:
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: annotation_not_support
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - source-annotation
  - everyday-loops
  - product-claim-risk
---

# Source Annotation: Mira Everyday Loop Claims

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:125-137; pasted-text.txt:188-200
anchor_status: exact_verified
```

## Why This Span Matters

This span frames everyday loops as:

```text
plain-language instruction
trigger
connected-app action
background execution
delivery back to user
```

It is useful as UX inspiration. It is not verified evidence that the named product can do every listed action.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

