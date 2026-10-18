---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: light
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ann-semantica-009-agent-mcp-direct-write
source_ref: "raw/repos/2026-08-02-semantica-agi-semantica-source.md"
working_copy_ref: "raw/repos/_snapshots/semantica-agi-semantica-0d44756.zip"
source_snapshot_ref: "raw/repos/_snapshots/semantica-agi-semantica-0d44756.zip"
external_annotation_id:
selector_type: TextQuoteSelector
selector_exact: "def handle_add_entity(args: dict) -> dict:"
selector_prefix: "from mcp.session import get_graph"
selector_suffix: "\"\"\"Add an entity to the graph.\"\"\""
selector_position: "mcp/tools/graph.py:15-69; related mcp/tools/decisions.py, semantica/mcp_server/__init__.py:56-72,538-550 and semantica/agent_memory.py:369-395"
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
body_note: "MCP 与 AgentMemory 可直接 mutation entity/relation/decision，缺少 VAKS 所需的权限分级、证据审核、二次确认和 operation receipt；默认持久化也不可靠。"
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

# Agent 与 MCP 直接写图

## Boundary

这是固定提交中的源码定位器，只表示“以后复核这里”。

它不证明该代码正确，不创建 evidence support、reviewed relation、truth confidence、project verdict 或 action basis。

## Intended Use

用于 Agent Memory Quarantine 与未来 MCP 权限设计；正式 vault 必须默认禁用 mutation。

