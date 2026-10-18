---
record_kind: context_pack_manifest_candidate
status: candidate
created_at: 2026-06-07T04:08:31+08:00
pack_id: CPACK-source-intake-routing-audit-20260607040832
topic_id: source-intake-routing
mode: audit
route_map_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/source-intake-route-map.json
query_intent_router_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/query-intent-router-v0.json
query_intent_selected_mode: audit
action_facing: false
truth_boundary: activation_pack_not_truth
allowed_use:
  - orientation
  - navigation
  - context_activation
  - drilldown_queue
forbidden_use:
  - truth
  - reviewed_relation
  - action_basis
---

# Context Pack Candidate: source-intake-routing

## Query

```yaml
user_query: "why are candidate and overlay excluded from action mode"
pattern: "source-intake-routing|high-pressure test|lint|audit|guardrail|action_readiness|evidence_support_check_not_run|candidate|overlay|excluded|action|mode"
original_pattern: "source intake|metadata-routing|context pack|registry-before-recompute|query-run receipt|retrieval_policy"
root: "C:\Users\Administrator\Documents\资料库"
mode: audit
original_mode: research
limit: 260
route_map_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/source-intake-route-map.json"
query_intent_router_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/query-intent-router-v0.json"
```

## Intent Router

```yaml
selected_mode: audit
confidence: high
fallback_used: false
matched_terms: ["why", "exclude", "candidate", "action", "mode", "audit_intent_override"]
route_bias: ["mainline_current", "audit_evidence", "support_review_output"]
warnings: ["audit_evidence_not_current_rule", "test_output_not_truth"]
truth_boundary: navigation_only_not_truth
action_basis_allowed: false
```

## Start Here

- `SOURCE_INTAKE.md`
- `templates/source-record.md`
- `templates/candidate-distillation.md`
- `templates/query-run.md`
- `00_handoff/2026-06-06-source-intake-control-flow-mainline-merge-handoff.md`

## Source Route Front Door

| route | matched | include lanes | borrowed from | guard |
|---|---:|---|---|---|
| `source-front-door` | no | mainline_current, raw_drilldown, candidate_orientation | langgenius/dify, Mintplex-Labs/anything-llm | A visible source route is navigation; it is not authority. |
| `ingestion-parser-route` | no | raw_drilldown, candidate_orientation | infiniflow/ragflow, run-llama/llama_index | Chunk metadata and parser output stay raw/candidate until evidence review. |
| `metadata-router-trace` | no | mainline_current, candidate_orientation, support_review_output | deepset-ai/haystack, langgenius/dify | Metadata route hit is not confidence, truth, or action readiness. |
| `citation-clickback-route` | no | raw_drilldown, reviewed_support | Mintplex-Labs/anything-llm, run-llama/llama_index | A citation link is not evidence support unless the cited span supports the specific point. |
| `action-safety-route` | yes | mainline_current, reviewed_support, raw_drilldown | VAKS source-intake control flow | Do not let route convenience override knowledge_status or retrieval_policy. |

## External Scout References

- `raw/repos/2026-06-07-langgenius-dify-source.md`
- `raw/repos/2026-06-07-infiniflow-ragflow-source.md`
- `raw/repos/2026-06-07-mintplex-labs-anything-llm-source.md`
- `raw/repos/2026-06-07-run-llama-llama-index-source.md`
- `raw/repos/2026-06-07-deepset-ai-haystack-source.md`
- `outputs/review/2026-06-07-source-intake-routing-github-scout-candidate-distillation.md`
- `outputs/review/project_overlays/VAKS/VAKS-source-intake-routing-github-scout-2026-06-07.md`

## Pack Summary

| lane | total_hits | included_by_mode | selected_for_pack |
|---|---:|---:|---:|
| `mainline_current` | 47 | 47 | 13 |
| `reviewed_support` | 105 | 0 | 0 |
| `raw_drilldown` | 108 | 0 | 0 |

## Pack Items

```yaml
items:
  - item_id: PI-001
    display_label: "SOURCE_INTAKE"
    lane: mainline_current
    path_role: mainline_doc
    source_ref: "SOURCE_INTAKE.md"
    selector_or_offset: "line:6"
    snippet: "project: verified-action-knowledge-system"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-002
    display_label: "source-record"
    lane: mainline_current
    path_role: formal_template
    source_ref: "templates\source-record.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-003
    display_label: "candidate-distillation"
    lane: mainline_current
    path_role: formal_template
    source_ref: "templates\candidate-distillation.md"
    selector_or_offset: "line:2"
    snippet: "record_kind: candidate_distillation"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-004
    display_label: "query-run"
    lane: mainline_current
    path_role: formal_template
    source_ref: "templates\query-run.md"
    selector_or_offset: "line:12"
    snippet: "model_interpretation:"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-005
    display_label: "2026-06-06-source-intake-control-flow-mainline-merge-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-06-06-source-intake-control-flow-mainline-merge-handoff.md"
    selector_or_offset: "line:5"
    snippet: "project: verified-action-knowledge-system"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-006
    display_label: "2026-05-26-knowledge-compile-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-26-knowledge-compile-handoff.md"
    selector_or_offset: "line:3"
    snippet: "> 2026-05-28 更新：本文件已不是最新恢复入口。后续窗口优先读 `00_handoff/2026-05-28-verified-action-knowledge-system-v0-2-handoff.md`。当前主架构已收缩为 v0.2：Karpathy 简单主线 + Dusk 项目桌面 + reviewed-action core；对外五层 `Capture / Understand / Review / Conne..."
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-007
    display_label: "2026-05-27-verified-action-knowledge-system-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-27-verified-action-knowledge-system-handoff.md"
    selector_or_offset: "line:1"
    snippet: "# 2026-05-27 handoff：Verified Action Knowledge System 主架构确认"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-008
    display_label: "2026-05-28-verified-action-knowledge-system-v0-2-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-28-verified-action-knowledge-system-v0-2-handoff.md"
    selector_or_offset: "line:1"
    snippet: "# 2026-05-28 handoff：Verified Action Knowledge System v0.2"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-009
    display_label: "2026-05-29-verified-action-knowledge-system-v0-2-pro-1-10-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-10-handoff.md"
    selector_or_offset: "line:5"
    snippet: "project: verified-action-knowledge-system"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-010
    display_label: "2026-05-29-verified-action-knowledge-system-v0-2-pro-1-11-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-11-handoff.md"
    selector_or_offset: "line:5"
    snippet: "project: verified-action-knowledge-system"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-011
    display_label: "2026-05-29-verified-action-knowledge-system-v0-2-pro-1-12-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-12-handoff.md"
    selector_or_offset: "line:5"
    snippet: "project: verified-action-knowledge-system"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-012
    display_label: "2026-05-29-verified-action-knowledge-system-v0-2-pro-1-13-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-13-handoff.md"
    selector_or_offset: "line:5"
    snippet: "project: verified-action-knowledge-system"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-013
    display_label: "2026-05-29-verified-action-knowledge-system-v0-2-pro-1-8-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-8-handoff.md"
    selector_or_offset: "line:5"
    snippet: "project: verified-action-knowledge-system"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'audit'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
```

## Excluded Or Not Default

These hits matched the query but are not selected for this mode/default pack.

| file | lane | path_role | caution |
|---|---|---|---|
| `wiki\anti-patterns\algorithmic-graph-scoring-without-source-quality.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\all-in-one-vault-runtime-before-modular-contracts.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\auto-compiled-concept-wiki-as-verified-truth-layer.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\automated-brief-as-truth-without-review.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\automatic-agentic-vault-rewrite-before-schema-stability.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\auto-promotion-without-review-gate.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\binary-vault-template-download-as-trusted-source.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\copying-full-second-brain-runtime-before-schema-stabilizes.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\derived-relatedness-as-truth-signal.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\direct-compile-to-truth-layer-without-review.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\do-not-blindly-merge-vault-and-agent-brain.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\full-app-overengineering-before-clean-markdown-vault.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\generic-concept-schema-as-truth-layer.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\markdown-only-vault-for-media-heavy-production.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\overgrown-always-on-instructions.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\para-folder-taxonomy-as-truth-layer.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\transformed-evidence-as-original-source.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\yolo-permissions-for-production-vault.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\claims\semantic-relation-strength-should-be-core-schema-field.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\claims\skills-turn-knowledge-vaults-into-action-systems.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\claims\verified-vault-api-should-stay-separate-from-agent-gbrain.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\concepts\evidence-backed-design-validation.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\concepts\negative-evidence-and-avoidance.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\concepts\positive-design-fusion.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |

## Coverage Overview

```yaml
coverage_overview:
  supported: 0
  weakly_supported: 0
  challenged: 0
  missing_evidence:
    - evidence_support_check_not_run
  out_of_scope: 0
  risk_flags:
    - pack_is_activation_not_truth
final_support:
  state: none
  reason: evidence_support_check_not_run
anchor_queue:
  total: 0
  mainline_current: 0
  reviewed_support: 0
  raw_drilldown: 0
  note: navigation_queue_only_not_support
action_readiness:
  state: not_ready
  reason: "Orientation/workbench pack only; not action-facing support."
evidence_sufficiency:
  state: insufficient
  checked_for: context_pack_builder_v0_smoke
  required_next_step: open raw/reviewed anchors and run evidence support check before action-facing use
context_pack_trace:
  retrieval_script: tools/vaks-retrieval-mvp.ps1
  route_map_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/source-intake-route-map.json"
  fusion_method: lane_grouping_only_no_cross_lane_rrf
  content_trace_policy: refs_only
```
