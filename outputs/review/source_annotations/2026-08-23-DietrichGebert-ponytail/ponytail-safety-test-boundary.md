---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ponytail-safety-test-boundary
source_ref: raw/repos/2026-08-23-DietrichGebert-ponytail-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "skills/ponytail/SKILL.md:90-112"
selector_exact: "Never simplify away"
selector_prefix:
selector_suffix:
selector_position: "skills/ponytail/SKILL.md:90-112"
source_hash: 2ed6c52c9d7e5e56942508591085fd45dea277d3
content_hash: "sha256:46a57e26a2632e7fa40eae6a3cf3011ccdc4d8db19d8f8617907d6b5deef055e"
anchor_status: exact_verified
anchor_checked_at: 2026-08-23
anchor_stale: false
anchor_match_count: 1
annotation_role: scope_limit
body_note: "Borrow the non-negotiable safety carve-outs, but treat the one-check/no-fixtures guidance as a local coding preference rather than a universal VAKS assurance limit."
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
  - scope-limit
  - assurance
---

# Source Annotation：Safety Carve-Out And Test Scope Limit

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
selector_type: line_range
selector_value: skills/ponytail/SKILL.md:90-112
anchor_status: exact_verified
```

## Why This Span Matters

值得借的是“理解、trust boundary、数据损失、安全、可访问性和明确需求不能被简化掉”。需要限制的是 one-check/no-fixtures：VAKS 的 schema、migration、Guard、negative fixture 与 replay 必须按风险决定验证深度。

## Boundary

这是 scope-limit locator，不是测试政策、review pass 或 runtime readiness。

