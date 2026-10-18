---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: claude-obsidian-research-dossier-canonical-merge-split
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "skills/autoresearch/SKILL.md:79-117"
selector_exact: "## File the research dossier"
selector_prefix:
selector_suffix:
selector_position: "skills/autoresearch/SKILL.md:79-117"
source_hash: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
content_hash: "sha256:f070cd6f63c2eab4e614e98510d9e59e4b71c2246e68d6a89a3c77a6535633e5"
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: candidate_seed
body_note: "Pin the workflow split in which a research dossier is filed first and canonical-page updates require a second separately reviewed transaction."
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
  - research-dossier
  - promotion-boundary
---

# Source Annotation：Research Dossier / Canonical Merge Split

## Locator

    selector_value: skills/autoresearch/SKILL.md:79-117
    anchor_status: exact_verified

## Why This Span Matters

这个 span 把研究 dossier 的持久化与 canonical page merge 拆成两个审核事务。它直接支持 VAKS 的 research candidate-only 与 promotion separation。

## Boundary

这是 workflow-contract locator；它不表示 dossier 结论已 review，也不表示 canonical merge 已获授权。

