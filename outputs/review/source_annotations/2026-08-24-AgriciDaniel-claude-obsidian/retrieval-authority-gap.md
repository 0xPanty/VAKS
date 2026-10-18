---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: claude-obsidian-retrieval-authority-gap
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "scripts/contextual-prefix.py:834-849"
selector_exact: "def collect_pages(target):"
selector_prefix:
selector_suffix:
selector_position: "scripts/contextual-prefix.py:834-849"
source_hash: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
content_hash: "sha256:3b1de6e83aa695c01a85c087da56b35b1d174ce4f58b7155119fd9995fbfac9d"
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: risk_flag
body_note: "Pin the broad page-collection rule that indexes all non-hidden Markdown under wiki; it does not filter hot, log, meta, candidate or reviewed authority before retrieval."
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
  - retrieval-eligibility
---

# Source Annotation：Retrieval Authority Gap

## Locator

    selector_value: scripts/contextual-prefix.py:834-849
    anchor_status: exact_verified

## Why This Span Matters

collect_pages 会遍历 wiki 下全部非隐藏 Markdown。结合 retrieve.py 只核验 cache/page hash、不读取 source/claim ledger，可确认检索完整性与知识 authority 是分离的。

## Boundary

Rank、cache validity 和 page hash 都不代表 reviewed、supported、fresh、applicable 或 action-ready。

