---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-semantica-008-bitemporal-normalization
source_ref: "raw/repos/2026-08-02-semantica-agi-semantica-source.md"
working_copy_ref: "raw/repos/_snapshots/semantica-agi-semantica-0d44756.zip"
source_snapshot_ref: "raw/repos/_snapshots/semantica-agi-semantica-0d44756.zip"
external_annotation_id:
selector_type: TextQuoteSelector
selector_exact: "class BiTemporalFact:"
selector_prefix: "@dataclass"
selector_suffix: "\"\"\"Wrapper for facts with bitemporal metadata."
selector_position: "semantica/kg/temporal_model.py:27-66 (exact line 28)"
selector_timestamp_start:
selector_timestamp_end:
selector_page:
selector_rect:
source_hash: "sha256:77A0397A7BCED20F79267AF0F69DA571DC68DCFA91C6249F1A76592B42CF86E4"
content_hash:
anchor_status: exact_verified
anchor_checked_at: "2026-08-02"
anchor_stale: false
anchor_match_count: 1
annotation_role: candidate_seed
body_note: "BiTemporalFact 区分 valid time、recorded time 与 superseded；这是 Temporal Applicability Check 的有用字段形状。"
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - "outputs/review/2026-08-02-semantica-agi-semantica-candidate-distillation.md"
project_overlay_refs:
  - "outputs/review/project_overlays/VAKS/VAKS-semantica-agi-semantica-2026-08-02.md"
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
  - semantica
  - review-input
---

# 双时态最小字段

## Boundary

这是固定提交中的源码定位器，只表示“以后复核这里”。

它不证明该代码正确，不创建 evidence support、reviewed relation、truth confidence、project verdict 或 action basis。

## Intended Use

未来设计 temporal record 时作为候选字段参考；实现前仍需不可变历史、替代链和查询语义。

