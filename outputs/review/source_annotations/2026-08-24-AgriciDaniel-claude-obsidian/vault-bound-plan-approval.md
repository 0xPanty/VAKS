---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: claude-obsidian-vault-bound-plan-approval
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "claude_obsidian/transaction.py:1287-1308"
selector_exact: "def plan_approval_sha256("
selector_prefix:
selector_suffix:
selector_position: "claude_obsidian/transaction.py:1287-1308"
source_hash: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
content_hash: "sha256:ca23820a70fdd5e2f6ce587faba32e981c7a3e795e87e0c79e93f7a0fcd28037"
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: candidate_seed
body_note: "Pin the approval-hash projection that binds operation identity, canonical vault identity, expanded bundle and exact prepared writes."
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
  - plan-approval
  - transaction-integrity
---

# Source Annotation：Vault-Bound Plan Approval

## Locator

    source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
    selector_value: claude_obsidian/transaction.py:1287-1308
    anchor_status: exact_verified

## Why This Span Matters

这个 span 展示 approval hash 如何绑定 canonical vault、expanded bundle 和 prepared writes。对 VAKS 的候选价值是把 authority receipt 进一步绑定到真正将被写入的路径、字节与模式。

## Boundary

这是 locator / review input，不是 action approval、evidence support、正式 pattern 或已采纳 executor 设计。

