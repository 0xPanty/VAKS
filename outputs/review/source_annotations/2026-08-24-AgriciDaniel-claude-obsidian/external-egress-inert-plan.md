---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: claude-obsidian-external-egress-inert-plan
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "claude_obsidian/capture.py:1151-1217"
selector_exact: "def plan_external_action("
selector_prefix:
selector_suffix:
selector_position: "claude_obsidian/capture.py:1151-1217"
source_hash: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
content_hash: "sha256:39f9eb663c11528f371ecb7743192b48b8c17189c861f2b4d81f6dc2c18fdac8"
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: candidate_seed
body_note: "Pin the external-action planner that validates declared/explicit domains and emits an inert argv/egress plan rather than executing a network client or process."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-08-24-AgriciDaniel-claude-obsidian-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_overlays/2026-08-24-AgriciDaniel-claude-obsidian-vaks-transaction-and-evidence-overlay.md
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
  - egress
  - inert-plan
---

# Source Annotation：External Egress Inert Plan

## Locator

    selector_value: claude_obsidian/capture.py:1151-1217
    anchor_status: exact_verified

## Why This Span Matters

上游把外部 URL/OCR/YouTube 类能力拆成 consent-aware plan 与外部 runner。planner 不偷偷执行网络或进程，是 capability honesty 与 egress boundary 的候选参考。

## Boundary

安全 plan 不证明外部 runner 安全、可用或已获本次授权。

