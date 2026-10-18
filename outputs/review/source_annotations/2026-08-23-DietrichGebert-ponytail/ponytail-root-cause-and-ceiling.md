---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ponytail-root-cause-and-ceiling
source_ref: raw/repos/2026-08-23-DietrichGebert-ponytail-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "skills/ponytail/SKILL.md:50-64"
selector_exact: "Bug fix = root cause, not symptom"
selector_prefix:
selector_suffix:
selector_position: "skills/ponytail/SKILL.md:50-64"
source_hash: 2ed6c52c9d7e5e56942508591085fd45dea277d3
content_hash: "sha256:46a57e26a2632e7fa40eae6a3cf3011ccdc4d8db19d8f8617907d6b5deef055e"
anchor_status: exact_verified
anchor_checked_at: 2026-08-23
anchor_stale: false
anchor_match_count: 1
annotation_role: implementation_note
body_note: "Pin the shared-root repair rule and the requirement that deliberate simplifications name a ceiling and upgrade path."
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
  - root-cause
  - reopen-trigger
---

# Source Annotation：Shared Root And Explicit Ceiling

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
selector_type: line_range
selector_value: skills/ponytail/SKILL.md:50-64
anchor_status: exact_verified
```

## Why This Span Matters

这里同时钉住两个可迁移点：修共同调用根部，而不是只补最近症状；故意接受的简化必须写明 ceiling 和 upgrade path。VAKS 可复用现有 consumer scan、`project_reopen_trigger` 与 `review_due_when`，不需要新债务系统。

## Boundary

这是 locator / review input，不是 support、正式 implementation rule 或 action basis。

