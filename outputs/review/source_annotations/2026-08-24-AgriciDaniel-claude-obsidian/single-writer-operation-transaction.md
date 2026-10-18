---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: claude-obsidian-single-writer-operation-transaction
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "skills/wiki/references/operation-transactions.md:5-40"
selector_exact: "Pass the inspect result's exact"
selector_prefix:
selector_suffix:
selector_position: "skills/wiki/references/operation-transactions.md:5-40"
source_hash: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
content_hash: "sha256:f1b7c8f9e83cea3e24b6159206a529623472fa024b20d78be47c5f9b2b53b8ad"
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: candidate_seed
body_note: "Pin the one-logical-operation contract: workers draft, one orchestrator inspects, the exact reviewed approval hash is applied once, and Git history stays separate."
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
  - single-writer
  - operation-transaction
---

# Source Annotation：Single-Writer Operation Transaction

## Locator

    selector_value: skills/wiki/references/operation-transactions.md:5-40
    anchor_status: exact_verified

## Why This Span Matters

该合同把 parallel drafting 与 canonical mutation 分开，并要求 inspect、exact approval、one apply、separate checkpoint。它可作为未来 VAKS 多文件 writer 的候选操作骨架。

## Boundary

这是上游合同的 locator；Skill 文本本身不证明所有调用者都遵守，也不构成 VAKS implementation approval。
