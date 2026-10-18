---
record_kind: context_pack_manifest_candidate
status: candidate
created_at: 2026-06-07T04:06:47+08:00
pack_id: CPACK-source-intake-routing-action-20260607040647
topic_id: source-intake-routing
mode: action
route_map_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/source-intake-route-map.json
action_facing: true
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
user_query: ""
pattern: "source-intake-routing|Dify|RAGFlow|AnythingLLM|LlamaIndex|Haystack|metadata|router|citation|ingestion|source route|action basis"
original_pattern: "source-intake-routing|Dify|RAGFlow|AnythingLLM|LlamaIndex|Haystack|metadata|router|citation|ingestion|source route|action basis"
root: "C:\Users\Administrator\Documents\资料库"
mode: action
original_mode: action
limit: 260
route_map_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/source-intake-route-map.json"
query_intent_router_ref: ""
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
| `source-front-door` | yes | mainline_current, raw_drilldown, candidate_orientation | langgenius/dify, Mintplex-Labs/anything-llm | A visible source route is navigation; it is not authority. |
| `ingestion-parser-route` | yes | raw_drilldown, candidate_orientation | infiniflow/ragflow, run-llama/llama_index | Chunk metadata and parser output stay raw/candidate until evidence review. |
| `metadata-router-trace` | yes | mainline_current, candidate_orientation, support_review_output | deepset-ai/haystack, langgenius/dify | Metadata route hit is not confidence, truth, or action readiness. |
| `citation-clickback-route` | yes | raw_drilldown, reviewed_support | Mintplex-Labs/anything-llm, run-llama/llama_index | A citation link is not evidence support unless the cited span supports the specific point. |
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
| `mainline_current` | 37 | 37 | 13 |
| `reviewed_support` | 43 | 43 | 8 |
| `raw_drilldown` | 91 | 91 | 8 |
| `candidate_orientation` | 35 | 0 | 0 |
| `active_project_overlay` | 25 | 0 | 0 |
| `support_review_output` | 29 | 0 | 0 |

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
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
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
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-003
    display_label: "candidate-distillation"
    lane: mainline_current
    path_role: formal_template
    source_ref: "templates\candidate-distillation.md"
    selector_or_offset: "line:14"
    snippet: "action_basis_allowed: false"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-004
    display_label: "query-run"
    lane: mainline_current
    path_role: formal_template
    source_ref: "templates\query-run.md"
    selector_or_offset: "line:25"
    snippet: "activated_routes: []"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
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
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
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
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
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
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
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
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
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
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
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
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
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
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
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
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
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
    action_anchor_candidate: true
    action_role: anchor_queue_rule_or_template
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-014
    display_label: "algorithmic-graph-scoring-without-source-quality"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\algorithmic-graph-scoring-without-source-quality.md"
    selector_or_offset: "line:12"
    snippet: "- source-verification-and-trust-model"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_reviewed_or_review_ready
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-015
    display_label: "all-in-one-vault-runtime-before-modular-contracts"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\all-in-one-vault-runtime-before-modular-contracts.md"
    selector_or_offset: "line:15"
    snippet: "- verified-action-knowledge-system"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_reviewed_or_review_ready
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-016
    display_label: "auto-compiled-concept-wiki-as-verified-truth-layer"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\auto-compiled-concept-wiki-as-verified-truth-layer.md"
    selector_or_offset: "line:18"
    snippet: "- source/summary/claim/pattern/anti-pattern/decision flow"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_reviewed_or_review_ready
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-017
    display_label: "auto-promotion-without-review-gate"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\auto-promotion-without-review-gate.md"
    selector_or_offset: "line:16"
    snippet: "- verified-action-knowledge-system"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_reviewed_or_review_ready
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-018
    display_label: "markdown-only-vault-for-media-heavy-production"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\markdown-only-vault-for-media-heavy-production.md"
    selector_or_offset: "line:11"
    snippet: "- '[[2026-05-26-obsidian-ai-orange-book-source]]'"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_reviewed_or_review_ready
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-019
    display_label: "para-folder-taxonomy-as-truth-layer"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\para-folder-taxonomy-as-truth-layer.md"
    selector_or_offset: "line:15"
    snippet: "- verified-action-knowledge-system"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_reviewed_or_review_ready
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-020
    display_label: "transformed-evidence-as-original-source"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\transformed-evidence-as-original-source.md"
    selector_or_offset: "line:7"
    snippet: "failure_mode: 'Treating OCR, translation, bbox, layout, or table-derived text as original source support without a recoverable original anchor.'"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_reviewed_or_review_ready
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-021
    display_label: "verified-vault-api-should-stay-separate-from-agent-gbrain"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\claims\verified-vault-api-should-stay-separate-from-agent-gbrain.md"
    selector_or_offset: "line:13"
    snippet: "sources:"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_reviewed_or_review_ready
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-022
    display_label: "2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_raw_provenance
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-023
    display_label: "2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_raw_provenance
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-024
    display_label: "2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_raw_provenance
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-025
    display_label: "2026-06-07-crosstalk-solutions-project-nomad-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-crosstalk-solutions-project-nomad-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_raw_provenance
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-026
    display_label: "2026-06-07-deepset-ai-haystack-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-deepset-ai-haystack-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_raw_provenance
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-027
    display_label: "2026-06-07-infiniflow-ragflow-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-infiniflow-ragflow-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_raw_provenance
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-028
    display_label: "2026-06-07-langgenius-dify-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-langgenius-dify-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_raw_provenance
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-029
    display_label: "2026-06-07-linkwarden-linkwarden-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-linkwarden-linkwarden-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: true
    action_role: anchor_queue_raw_provenance
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'action'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
```

## Excluded Or Not Default

These hits matched the query but are not selected for this mode/default pack.

| file | lane | path_role | caution |
|---|---|---|---|
| `outputs\review\2026-06-04-video-intake-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-anthropic-contextual-retrieval-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-anthropic-effective-context-engineering-agents-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-arxiv-retrieval-batch-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-beltromatti-get-it-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-datawhalechina-agent-learning-hub-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-google-cloud-gemini-enterprise-hybrid-search-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-helloianneo-ian-xiaohei-illustrations-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-lum1104-understand-anything-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-microsoft-azure-ai-search-agentic-retrieval-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-microsoft-graphrag-query-focused-summarization-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-openinference-semantic-conventions-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-pasted-high-judgment-skill-library-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-rag-eval-tracing-citation-rrf-batch-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-robzilla1738-supergoal-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-x-cyrilxbt-claude-obsidian-90-days-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-x-cyrilxbt-obsidian-from-scratch-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-x-cyrilxbt-obsidian-hermes-life-system-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-x-damidefi-obsidian-claude-research-stack-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-x-damidefi-obsidian-signal-density-cleanup-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-x-dontbesilent-content-asset-engineering-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-x-hamza-obsidian-second-brain-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |
| `outputs\review\2026-06-06-x-khairallah-obsidian-claude-workflows-candidate-distillation.md` | `candidate_orientation` | `candidate_distillation` | `["candidate_not_action_basis"]` |

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
  total: 29
  mainline_current: 13
  reviewed_support: 8
  raw_drilldown: 8
  note: navigation_queue_only_not_support
action_readiness:
  state: not_ready
  reason: "Builder only prepares an anchor_queue; evidence support check has not run."
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
