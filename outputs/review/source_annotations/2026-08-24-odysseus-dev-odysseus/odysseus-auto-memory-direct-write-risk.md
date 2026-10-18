---
record_kind: source_annotation
status: captured
annotation_id: odysseus-auto-memory-direct-write-risk
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
source_ref: raw/repos/2026-08-24-odysseus-dev-odysseus-source.md
source_snapshot_ref: "https://github.com/odysseus-dev/odysseus/blob/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c/services/memory/memory_extractor.py"
selector_type: line_range
selector_value: "services/memory/memory_extractor.py:448-471"
selector_exact: "entry = memory_manager.add_entry(fact_text, source=\"auto\", category=category, owner=_owner)"
source_hash: b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c
content_hash: 8421701a20e21c86965ef59a0f974bf67e728594aaceda47b1fab93318ef2780
content_hash_scope: full_source_file
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: risk_signal
body_note: "This code path adds auto-extracted facts directly to durable memory, auto-pins identity facts, and saves the store; it is a risk locator for VAKS agent-memory quarantine, not a complete call-chain verdict."
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
candidate_refs:
  - outputs/review/2026-08-24-odysseus-dev-odysseus-candidate-distillation.md
project_overlay_refs: []
source_digest_required: false
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
  - agent-memory
  - direct-write-risk
  - review-input
---

# Source Annotation: Auto Memory Direct-Write Risk

## Locator

```yaml
source_snapshot_ref: https://github.com/odysseus-dev/odysseus/blob/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c/services/memory/memory_extractor.py
selector_type: line_range
selector_value: services/memory/memory_extractor.py:448-471
anchor_status: exact_verified
```

## Why This Span Matters

这段定位到一条实际代码路径：自动抽取事实以 `source="auto"` 加入 memory，identity 类别被 pin，然后保存 JSON 并更新向量索引。

这是 VAKS 应保留的反向锚点：agent/model 提取只能创建 candidate 或 feedback-event，不能直接改写 reviewed truth。本次未审计该函数的全部上游触发、设置和 UI，所以 annotation 只说“检查这条路径”，不作全局无审核的结论。

## Related Tension

`docs/agent-migration.md:14-26;166-181` 提倡 archive 与 reviewable memory candidates 分层。文档契约与本运行时路径之间的张力值得后续强蒸馏，但不应在 medium 阶段被自动解读为已证实的系统级冲突。

## Boundary

This annotation is a locator and review input only. It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.
