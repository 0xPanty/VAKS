---
record_kind: source_annotation
annotation_id: hermes-one-change-stop-rules
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source/pasted-text.txt
selector_type: line_range
selector_value: "pasted-text.txt:43-50; pasted-text.txt:57-59"
selector_exact: "freeze baseline, fix one thing, prove on unseen data, stop on target/budget/no improvement; every round logged, verified, scored, tested"
selector_prefix:
selector_suffix:
source_hash: DA2DEAD629955F928CBA56C917533231C2B928DD2394C7EEE3775447CE89A933
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: candidate_seed
body_note: "This span anchors loop discipline: one change at a time, holdout proof, explicit stop conditions, and logged/scored rounds."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-06-23-0xjeff-hermes-sensei-loop-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_lens_overlays/2026-06-23-0xjeff-hermes-sensei-loop-vaks-research-loop-overlay.md
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
  - stop-condition
  - attribution
---

# Source Annotation: One Change And Stop Rules

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-06-23-0xjeff-hermes-sensei-loop-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:43-50; pasted-text.txt:57-59
anchor_status: exact_verified
```

## Why This Span Matters

This span gives the operational loop discipline:

```text
freeze baseline
fix one recorded failure
test working set
test holdout set
ship target / best champion
stop after no holdout improvement
log, verify, score, test every round
```

For VAKS/MISA, this is useful because attribution collapses when multiple prompt changes happen at once.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

