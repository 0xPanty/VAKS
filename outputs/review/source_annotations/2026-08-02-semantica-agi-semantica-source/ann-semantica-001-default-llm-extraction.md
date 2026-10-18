---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-semantica-001-default-llm-extraction
source_ref: "raw/repos/2026-08-02-semantica-agi-semantica-source.md"
working_copy_ref: "raw/repos/_snapshots/semantica-agi-semantica-0d44756.zip"
source_snapshot_ref: "raw/repos/_snapshots/semantica-agi-semantica-0d44756.zip"
external_annotation_id:
selector_type: TextQuoteSelector
selector_exact: "# Default to LLM methods as per requirement"
selector_prefix: "if ner_method is None:"
selector_suffix: "ner_method = NERMethod.LLM"
selector_position: "semantica/kg/graph_builder.py:231-285 (exact line 240)"
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
annotation_role: risk_signal
body_note: "原始文本构图在调用方未指定策略时默认选择 LLM NER、关系与三元组抽取；这限制了 deterministic graph construction 的适用范围。"
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

# 默认 LLM 抽取边界

## Boundary

这是固定提交中的源码定位器，只表示“以后复核这里”。

它不证明该代码正确，不创建 evidence support、reviewed relation、truth confidence、project verdict 或 action basis。

## Intended Use

在评估 text-to-KG 或自动抽取写入时，提醒抽取结果只能进入 candidate comprehension，不能直接创建 reviewed relation。

