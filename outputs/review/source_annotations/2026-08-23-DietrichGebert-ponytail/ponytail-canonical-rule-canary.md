---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ponytail-canonical-rule-canary
source_ref: raw/repos/2026-08-23-DietrichGebert-ponytail-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "scripts/check-rule-copies.js:15-69"
selector_exact: "canary, not full equality"
selector_prefix:
selector_suffix:
selector_position: "scripts/check-rule-copies.js:15-69"
source_hash: 2ed6c52c9d7e5e56942508591085fd45dea277d3
content_hash: "sha256:b4e253ce4fb0c5a41a63fc8b0df796e621eb4e32a64e9aa13b5a4abd637b8988"
anchor_status: exact_verified
anchor_checked_at: 2026-08-23
anchor_stale: false
anchor_match_count: 1
annotation_role: implementation_note
body_note: "Pin the two-level drift strategy: exact equality for compact copies and a small invariant canary for longer non-identical variants."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-08-23-DietrichGebert-ponytail-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_overlays/2026-08-23-DietrichGebert-ponytail-vaks-minimalism-overlay.md
source_digest_required: false
source_digest_ref:
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
  - rule-drift
  - invariant-canary
---

# Source Annotation：Canonical Copy And Invariant Canary

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
selector_type: line_range
selector_value: scripts/check-rule-copies.js:15-69
anchor_status: exact_verified
```

## Why This Span Matters

这段代码区分了 exact-copy parity 与 long-form invariant canary。它可能帮助 VAKS 将重复关键边界做成只读 drift lint，但目前没有足够 recurrence 证据，不应据此新建脚本或自动修复。

## Boundary

这是 locator / implementation-note candidate，不是 reviewed maintenance policy 或写入权限。
