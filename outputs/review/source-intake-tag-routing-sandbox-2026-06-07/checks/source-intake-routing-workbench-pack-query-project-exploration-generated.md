---
record_kind: context_pack_manifest_candidate
status: candidate
created_at: 2026-06-07T04:05:47+08:00
pack_id: CPACK-source-intake-routing-project-exploration-20260607040548
topic_id: source-intake-routing
mode: project-exploration
route_map_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/source-intake-route-map.json
query_intent_router_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/query-intent-router-v0.json
query_intent_selected_mode: project-exploration
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
user_query: "what does the VAKS project overlay borrow for source-intake-routing"
pattern: "source-intake-routing|project overlay|VAKS|borrowing|active project|project scope|project|overlay|borrow"
original_pattern: "source intake|metadata-routing|context pack|registry-before-recompute|query-run receipt|retrieval_policy"
root: "C:\Users\Administrator\Documents\资料库"
mode: project-exploration
original_mode: research
limit: 260
route_map_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/source-intake-route-map.json"
query_intent_router_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/query-intent-router-v0.json"
```

## Intent Router

```yaml
selected_mode: project-exploration
confidence: high
fallback_used: false
matched_terms: ["overlay", "project overlay", "VAKS", "source-intake-routing", "borrow", "project"]
route_bias: ["active_project_overlay", "candidate_orientation", "support_review_output"]
warnings: ["project_overlay_not_universal_rule", "project_borrowing_not_truth_mutation"]
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
| `action-safety-route` | no | mainline_current, reviewed_support, raw_drilldown | VAKS source-intake control flow | Do not let route convenience override knowledge_status or retrieval_policy. |

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
| `mainline_current` | 46 | 46 | 13 |
| `reviewed_support` | 97 | 0 | 0 |
| `raw_drilldown` | 114 | 114 | 13 |
| `candidate_orientation` | 3 | 3 | 4 |

## Pack Items

```yaml
items:
  - item_id: PI-001
    display_label: "SOURCE_INTAKE"
    lane: mainline_current
    path_role: mainline_doc
    source_ref: "SOURCE_INTAKE.md"
    selector_or_offset: "line:3"
    snippet: "status: active"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
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
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-003
    display_label: "candidate-distillation"
    lane: mainline_current
    path_role: formal_template
    source_ref: "templates\candidate-distillation.md"
    selector_or_offset: "line:8"
    snippet: "overlay_state: none"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-004
    display_label: "query-run"
    lane: mainline_current
    path_role: formal_template
    source_ref: "templates\query-run.md"
    selector_or_offset: "line:14"
    snippet: "query_scope:"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-005
    display_label: "2026-06-06-source-intake-control-flow-mainline-merge-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-06-06-source-intake-control-flow-mainline-merge-handoff.md"
    selector_or_offset: "line:3"
    snippet: "status: active_recovery_entry"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-006
    display_label: "2026-06-07-langgenius-dify-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-langgenius-dify-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14510
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["pinned_by_route_map", "raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-007
    display_label: "2026-06-07-infiniflow-ragflow-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-infiniflow-ragflow-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14510
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["pinned_by_route_map", "raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-008
    display_label: "2026-06-07-mintplex-labs-anything-llm-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-mintplex-labs-anything-llm-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14510
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["pinned_by_route_map", "raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-009
    display_label: "2026-06-07-run-llama-llama-index-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-run-llama-llama-index-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14510
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["pinned_by_route_map", "raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-010
    display_label: "2026-06-07-deepset-ai-haystack-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\repos\2026-06-07-deepset-ai-haystack-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14510
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["pinned_by_route_map", "raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-011
    display_label: "2026-06-07-source-intake-routing-github-scout-candidate-distillation"
    lane: candidate_orientation
    path_role: candidate_distillation
    source_ref: "outputs\review\2026-06-07-source-intake-routing-github-scout-candidate-distillation.md"
    selector_or_offset: "line:8"
    snippet: "overlay_state: none"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14510
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["pinned_by_route_map", "candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-012
    display_label: "VAKS-source-intake-routing-github-scout-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS\VAKS-source-intake-routing-github-scout-2026-06-07.md"
    selector_or_offset: "line:2"
    snippet: "record_kind: project_overlay"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14510
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["pinned_by_route_map", "overlay_not_authority", "pack_builder_not_evidence_check"]
  - item_id: PI-013
    display_label: "2026-05-26-knowledge-compile-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-26-knowledge-compile-handoff.md"
    selector_or_offset: "line:117"
    snippet: "Source/Library -> Concept/Pattern -> Project/Decision/Problem -> Output"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-014
    display_label: "2026-05-27-verified-action-knowledge-system-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-27-verified-action-knowledge-system-handoff.md"
    selector_or_offset: "line:24"
    snippet: "raw source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-015
    display_label: "2026-05-29-verified-action-knowledge-system-v0-2-pro-1-10-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-10-handoff.md"
    selector_or_offset: "line:3"
    snippet: "status: active"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-016
    display_label: "2026-05-29-verified-action-knowledge-system-v0-2-pro-1-11-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-11-handoff.md"
    selector_or_offset: "line:3"
    snippet: "status: active"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-017
    display_label: "2026-05-29-verified-action-knowledge-system-v0-2-pro-1-12-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-12-handoff.md"
    selector_or_offset: "line:3"
    snippet: "status: active"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-018
    display_label: "2026-05-29-verified-action-knowledge-system-v0-2-pro-1-13-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-13-handoff.md"
    selector_or_offset: "line:3"
    snippet: "status: active"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-019
    display_label: "2026-05-29-verified-action-knowledge-system-v0-2-pro-1-8-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-8-handoff.md"
    selector_or_offset: "line:3"
    snippet: "status: active"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-020
    display_label: "2026-05-29-verified-action-knowledge-system-v0-2-pro-1-9-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-9-handoff.md"
    selector_or_offset: "line:3"
    snippet: "status: active"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-021
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
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-022
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
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-023
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
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-024
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
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-025
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
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-026
    display_label: "2026-06-07-bilibili-self-learning-library-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\videos\2026-06-07-bilibili-self-learning-library-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-027
    display_label: "segments"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\videos\2026-06-07-bilibili-self-learning-library-source\segments.md"
    selector_or_offset: "line:419"
    snippet: "[1026.30-1028.30] 就Project Harness Workflow"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-028
    display_label: "2026-01-thinking-os-with-ai-vault-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\articles\2026-01-thinking-os-with-ai-vault-source.md"
    selector_or_offset: "line:2"
    snippet: "type: source"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-029
    display_label: "2026-06-04-video-intake-candidate-distillation"
    lane: candidate_orientation
    path_role: candidate_distillation
    source_ref: "outputs\review\2026-06-04-video-intake-candidate-distillation.md"
    selector_or_offset: "line:6"
    snippet: "proposed_title: 'Video Intake Candidate Distillation: Light Capture, Workbench, and Feedback Surface'"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-030
    display_label: "2026-06-06-anthropic-contextual-retrieval-candidate-distillation"
    lane: candidate_orientation
    path_role: candidate_distillation
    source_ref: "outputs\review\2026-06-06-anthropic-contextual-retrieval-candidate-distillation.md"
    selector_or_offset: "line:5"
    snippet: "scope: Anthropic Contextual Retrieval -> VAKS retrieval/query contract"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-031
    display_label: "2026-06-06-anthropic-effective-context-engineering-agents-candidate-distillation"
    lane: candidate_orientation
    path_role: candidate_distillation
    source_ref: "outputs\review\2026-06-06-anthropic-effective-context-engineering-agents-candidate-distillation.md"
    selector_or_offset: "line:5"
    snippet: "scope: Anthropic Effective Context Engineering -> VAKS retrieval/query and context-pack contract"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'project-exploration'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["candidate_not_action_basis", "pack_builder_not_evidence_check"]
```

## Excluded Or Not Default

These hits matched the query but are not selected for this mode/default pack.

| file | lane | path_role | caution |
|---|---|---|---|
| `wiki\anti-patterns\algorithmic-graph-scoring-without-source-quality.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\all-in-one-vault-runtime-before-modular-contracts.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\auto-compiled-concept-wiki-as-verified-truth-layer.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\anti-patterns\automated-brief-as-truth-without-review.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
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
| `wiki\claims\each-vault-needs-purpose-specific-philosophy.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\claims\llm-wiki-is-implemented-reference-architecture.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\claims\orange-book-is-guide-not-turnkey-vault-template.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\claims\purpose-specific-vaults-change-the-system-goal.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\claims\semantic-relation-strength-should-be-core-schema-field.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\claims\skills-turn-knowledge-vaults-into-action-systems.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |
| `wiki\claims\vault-index-guides-context-loading.md` | `reviewed_support` | `reviewed_knowledge` | `[]` |

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
