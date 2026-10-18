---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: claude-obsidian-claim-support-validator-ceiling
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "claude_obsidian/ledgers.py:1030-1150"
selector_exact: 'reviewed_at = record.get("reviewed_at")'
selector_prefix:
selector_suffix:
selector_position: "claude_obsidian/ledgers.py:1030-1150"
source_hash: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
content_hash: "sha256:99965eb4b0e47b5b1eb1daf3e7bfdc80dd406d775a208d9dace43191945f89aa"
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: risk_flag
body_note: "Pin the actual accepted-claim validator ceiling: reviewed_at and fresh-source checks exist, while locator may be null and reviewer, warrant, support-bearing span, scope, omission and confidence coupling are absent."
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
  - risk-flag
  - evidence-support
---

# Source Annotation：Claim Support Validator Ceiling

## Locator

    selector_value: claude_obsidian/ledgers.py:1030-1150
    anchor_status: exact_verified

## Why This Span Matters

这段代码同时展示上游 validator 的含金量与上限：它会检查 review date、fresh support、独立来源和 contradiction，但 evidence locator 可空，也没有 VAKS 所需的 reviewer provenance、warrant、support-bearing、scope、omission 和 applicability。

## Boundary

这是 risk locator。它不能被反向解释为“上游 accepted 已等价 reviewed knowledge”。

