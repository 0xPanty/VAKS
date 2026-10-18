---
record_kind: source_annotation
status: captured
annotation_id: odysseus-exact-action-binding-payload
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
source_ref: raw/repos/2026-08-24-odysseus-dev-odysseus-source.md
source_snapshot_ref: "https://github.com/odysseus-dev/odysseus/blob/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c/src/tool_approvals.py"
selector_type: line_range
selector_value: "src/tool_approvals.py:104-165;237-313"
selector_exact: "return _canonical_digest(expected) == self.pending.digest"
source_hash: b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c
content_hash: cf5acb367086ee5138644254a7226c91db4c81b63a15f55def2fcaf18608a990
content_hash_scope: full_source_file
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: implementation_note
body_note: "The server binds owner, session, origin run, exact tool input, workspace, document version/digest, untrusted-context state, selected tools, effects, and result integrity into a canonical digest, then matches and claims the exact action once."
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
  - exact-action-approval
  - operation-receipt
  - review-input
---

# Source Annotation: Exact Action Binding Payload

## Locator

```yaml
source_snapshot_ref: https://github.com/odysseus-dev/odysseus/blob/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c/src/tool_approvals.py
selector_type: line_range
selector_value: src/tool_approvals.py:104-165;237-313
anchor_status: exact_verified
```

## Why This Span Matters

这段展示的候选机制不只是“弹出授权按钮”，而是把精确动作的服务端载荷归一化、摘要绑定，使用时重算并只 claim 一次。

它可以作为 VAKS operation receipt / action bridge 的后续比较输入，但本 annotation 不确认该实现无漏洞，也不授予当前动作权。

## Boundary

This annotation is a locator and review input only. It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.
