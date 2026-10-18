---
record_kind: context_pack_manifest_candidate
status: candidate
created_at: 2026-06-07T04:13:47+08:00
pack_id: CPACK-source-intake-routing-research-20260607041347
topic_id: source-intake-routing
mode: research
route_map_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/source-intake-route-map.json
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
user_query: ""
pattern: "source intake|metadata-routing|context pack|registry-before-recompute|query-run receipt|retrieval_policy"
original_pattern: "source intake|metadata-routing|context pack|registry-before-recompute|query-run receipt|retrieval_policy"
root: "H:\Obsidian\资料库"
mode: research
original_mode: research
limit: 320
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
| `source-front-door` | no | mainline_current, raw_drilldown, candidate_orientation | langgenius/dify, Mintplex-Labs/anything-llm | A visible source route is navigation; it is not authority. |
| `ingestion-parser-route` | no | raw_drilldown, candidate_orientation | infiniflow/ragflow, run-llama/llama_index | Chunk metadata and parser output stay raw/candidate until evidence review. |
| `metadata-router-trace` | yes | mainline_current, candidate_orientation, support_review_output | deepset-ai/haystack, langgenius/dify | Metadata route hit is not confidence, truth, or action readiness. |
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
| `mainline_current` | 12 | 0 | 5 |
| `raw_drilldown` | 58 | 58 | 13 |
| `candidate_orientation` | 33 | 33 | 9 |
| `active_project_overlay` | 24 | 24 | 9 |
| `support_review_output` | 36 | 36 | 8 |
| `audit_evidence` | 109 | 0 | 0 |
| `feedback_diagnostics` | 1 | 0 | 0 |

## Pack Items

```yaml
items:
  - item_id: PI-001
    display_label: "SOURCE_INTAKE"
    lane: mainline_current
    path_role: mainline_doc
    source_ref: "SOURCE_INTAKE.md"
    selector_or_offset: "line:8"
    snippet: "- source-intake"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-003
    display_label: "candidate-distillation"
    lane: mainline_current
    path_role: formal_template
    source_ref: "templates\candidate-distillation.md"
    selector_or_offset: "line:11"
    snippet: "retrieval_policy:"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-004
    display_label: "query-run"
    lane: mainline_current
    path_role: formal_template
    source_ref: "templates\query-run.md"
    selector_or_offset: "line:2"
    snippet: "record_type: query-run"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
    warnings: ["pinned_by_route_map", "pack_builder_not_evidence_check"]
  - item_id: PI-005
    display_label: "2026-06-06-source-intake-control-flow-mainline-merge-handoff"
    lane: mainline_current
    path_role: handoff
    source_ref: "00_handoff\2026-06-06-source-intake-control-flow-mainline-merge-handoff.md"
    selector_or_offset: "line:6"
    snippet: "scope: Source Intake Control Flow round1 + round2 mainline merge"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14010
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match."
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["pinned_by_route_map", "raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-011
    display_label: "2026-06-07-source-intake-routing-github-scout-candidate-distillation"
    lane: candidate_orientation
    path_role: candidate_distillation
    source_ref: "outputs\review\2026-06-07-source-intake-routing-github-scout-candidate-distillation.md"
    selector_or_offset: "line:11"
    snippet: "- raw/repos/2026-06-07-langgenius-dify-source.md"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14510
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["pinned_by_route_map", "candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-012
    display_label: "VAKS-source-intake-routing-github-scout-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS\VAKS-source-intake-routing-github-scout-2026-06-07.md"
    selector_or_offset: "line:11"
    snippet: "retrieval_policy:"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 14510
    selection_reason: "ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > pinned_ref > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["pinned_by_route_map", "overlay_not_authority", "pack_builder_not_evidence_check"]
  - item_id: PI-013
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-014
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-015
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-016
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-017
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-018
    display_label: "2026-06-04-x-hermes-self-improving-agent-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\articles\2026-06-04-x-hermes-self-improving-agent-source.md"
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-019
    display_label: "2026-06-06-anthropic-effective-context-engineering-agents-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\articles\2026-06-06-anthropic-effective-context-engineering-agents-source.md"
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-020
    display_label: "2026-06-06-llamaindex-citation-query-engine-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\articles\2026-06-06-llamaindex-citation-query-engine-source.md"
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-021
    display_label: "2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-candidate-distillation"
    lane: candidate_orientation
    path_role: candidate_distillation
    source_ref: "outputs\review\2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-candidate-distillation.md"
    selector_or_offset: "line:11"
    snippet: "- raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-source.md"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-022
    display_label: "2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-candidate-distillation"
    lane: candidate_orientation
    path_role: candidate_distillation
    source_ref: "outputs\review\2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-candidate-distillation.md"
    selector_or_offset: "line:10"
    snippet: "derived_from: 'raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-source.md'"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-023
    display_label: "2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-candidate-distillation"
    lane: candidate_orientation
    path_role: candidate_distillation
    source_ref: "outputs\review\2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-candidate-distillation.md"
    selector_or_offset: "line:11"
    snippet: "- raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-source.md"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-024
    display_label: "2026-06-07-crosstalk-solutions-project-nomad-candidate-distillation"
    lane: candidate_orientation
    path_role: candidate_distillation
    source_ref: "outputs\review\2026-06-07-crosstalk-solutions-project-nomad-candidate-distillation.md"
    selector_or_offset: "line:11"
    snippet: "- raw/repos/2026-06-07-crosstalk-solutions-project-nomad-source.md"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-025
    display_label: "2026-06-07-infiniflow-ragflow-candidate-distillation"
    lane: candidate_orientation
    path_role: candidate_distillation
    source_ref: "outputs\review\2026-06-07-infiniflow-ragflow-candidate-distillation.md"
    selector_or_offset: "line:11"
    snippet: "- raw/repos/2026-06-07-infiniflow-ragflow-source.md"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-026
    display_label: "2026-06-07-linkwarden-linkwarden-candidate-distillation"
    lane: candidate_orientation
    path_role: candidate_distillation
    source_ref: "outputs\review\2026-06-07-linkwarden-linkwarden-candidate-distillation.md"
    selector_or_offset: "line:11"
    snippet: "- raw/repos/2026-06-07-linkwarden-linkwarden-source.md"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-027
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-028
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-029
    display_label: "MISA-VAKS-ragflow-context-engine-overlay-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\MISA-VAKS-ragflow-context-engine-overlay-2026-06-07.md"
    selector_or_offset: "line:6"
    snippet: "source_record: raw/repos/2026-06-07-infiniflow-ragflow-source.md"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["overlay_not_authority", "pack_builder_not_evidence_check"]
  - item_id: PI-030
    display_label: "VAKS-get-it-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS-get-it-2026-06-07.md"
    selector_or_offset: "line:11"
    snippet: "retrieval_policy:"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["overlay_not_authority", "pack_builder_not_evidence_check"]
  - item_id: PI-031
    display_label: "VAKS-linkwarden-linkwarden-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS-linkwarden-linkwarden-2026-06-07.md"
    selector_or_offset: "line:11"
    snippet: "retrieval_policy:"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["overlay_not_authority", "pack_builder_not_evidence_check"]
  - item_id: PI-032
    display_label: "VAKS-obsidian-excalidraw-example-vault-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS-obsidian-excalidraw-example-vault-2026-06-07.md"
    selector_or_offset: "line:11"
    snippet: "retrieval_policy:"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["overlay_not_authority", "pack_builder_not_evidence_check"]
  - item_id: PI-033
    display_label: "VAKS-obsidian-excalidraw-plugin-ymjr-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS-obsidian-excalidraw-plugin-ymjr-2026-06-07.md"
    selector_or_offset: "line:11"
    snippet: "retrieval_policy:"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["overlay_not_authority", "pack_builder_not_evidence_check"]
  - item_id: PI-034
    display_label: "VAKS-obsidian-excalidraw-scripts-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS-obsidian-excalidraw-scripts-2026-06-07.md"
    selector_or_offset: "line:11"
    snippet: "retrieval_policy:"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["overlay_not_authority", "pack_builder_not_evidence_check"]
  - item_id: PI-035
    display_label: "VAKS-project-nomad-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS-project-nomad-2026-06-07.md"
    selector_or_offset: "line:11"
    snippet: "retrieval_policy:"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["overlay_not_authority", "pack_builder_not_evidence_check"]
  - item_id: PI-036
    display_label: "MISA-agent-learning-hub-integration-overlay-2026-06-06"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\MISA-agent-learning-hub-integration-overlay-2026-06-06.md"
    selector_or_offset: "line:6"
    snippet: "source_record: raw/repos/2026-06-06-datawhalechina-agent-learning-hub-source.md"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["overlay_not_authority", "pack_builder_not_evidence_check"]
  - item_id: PI-037
    display_label: "2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-architecture-review"
    lane: support_review_output
    path_role: summary
    source_ref: "wiki\summaries\2026-06-07-bowen-0x00-obsidian-excalidraw-example-vault-architecture-review.md"
    selector_or_offset: "line:6"
    snippet: "source_url: https://github.com/Bowen-0x00/obsidian-excalidraw-example-vault"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["review_output_needs_anchor_before_action", "pack_builder_not_evidence_check"]
  - item_id: PI-038
    display_label: "2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-architecture-review"
    lane: support_review_output
    path_role: summary
    source_ref: "wiki\summaries\2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-architecture-review.md"
    selector_or_offset: "line:6"
    snippet: "source_url: 'raw/repos/2026-06-07-bowen-0x00-obsidian-excalidraw-plugin-ymjr-source.md'"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["review_output_needs_anchor_before_action", "pack_builder_not_evidence_check"]
  - item_id: PI-039
    display_label: "2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-architecture-review"
    lane: support_review_output
    path_role: summary
    source_ref: "wiki\summaries\2026-06-07-bowen-0x00-obsidian-excalidraw-scripts-architecture-review.md"
    selector_or_offset: "line:6"
    snippet: "source_url: https://github.com/Bowen-0x00/obsidian-excalidraw-scripts"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["review_output_needs_anchor_before_action", "pack_builder_not_evidence_check"]
  - item_id: PI-040
    display_label: "2026-06-07-crosstalk-solutions-project-nomad-architecture-review"
    lane: support_review_output
    path_role: summary
    source_ref: "wiki\summaries\2026-06-07-crosstalk-solutions-project-nomad-architecture-review.md"
    selector_or_offset: "line:6"
    snippet: "source_url: https://github.com/Crosstalk-Solutions/project-nomad"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["review_output_needs_anchor_before_action", "pack_builder_not_evidence_check"]
  - item_id: PI-041
    display_label: "2026-06-07-infiniflow-ragflow-architecture-review"
    lane: support_review_output
    path_role: summary
    source_ref: "wiki\summaries\2026-06-07-infiniflow-ragflow-architecture-review.md"
    selector_or_offset: "line:4"
    snippet: "library_name: 'RAGFlow'"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["review_output_needs_anchor_before_action", "pack_builder_not_evidence_check"]
  - item_id: PI-042
    display_label: "2026-06-07-linkwarden-linkwarden-architecture-review"
    lane: support_review_output
    path_role: summary
    source_ref: "wiki\summaries\2026-06-07-linkwarden-linkwarden-architecture-review.md"
    selector_or_offset: "line:6"
    snippet: "source_url: https://github.com/linkwarden/linkwarden"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4510
    selection_reason: "ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["review_output_needs_anchor_before_action", "pack_builder_not_evidence_check"]
  - item_id: PI-043
    display_label: "2026-06-05-cross-project-borrowing-4-item-pilot-test"
    lane: support_review_output
    path_role: review_output
    source_ref: "outputs\review\2026-06-05-cross-project-borrowing-4-item-pilot-test.md"
    selector_or_offset: "line:18"
    snippet: "但这轮测试**不回头修改本地已有 raw source card**。原因很简单：这些 source card 已经是来源备案和候选蒸馏记录，不能为了试点把旧资料改乱。"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["review_output_needs_anchor_before_action", "pack_builder_not_evidence_check"]
  - item_id: PI-044
    display_label: "2026-06-05-v0-2-13-dual-project-reuse-validation"
    lane: support_review_output
    path_role: review_output
    source_ref: "outputs\review\2026-06-05-v0-2-13-dual-project-reuse-validation.md"
    selector_or_offset: "line:6"
    snippet: "scope: candidate-pattern-cross-project-contextualization"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: activation_only
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["review_output_needs_anchor_before_action", "pack_builder_not_evidence_check"]
```

## Excluded Or Not Default

These hits matched the query but are not selected for this mode/default pack.

| file | lane | path_role | caution |
|---|---|---|---|
| `00_handoff\2026-06-05-vaks-v0-2-13-action-support-visibility-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `ARCHITECTURE_PRINCIPLES.md` | `mainline_current` | `mainline_doc` | `[]` |
| `FUSION_ARCHITECTURE_V0_2_DRAFT.md` | `mainline_current` | `mainline_doc` | `[]` |
| `templates\feedback-event.md` | `mainline_current` | `formal_template` | `[]` |
| `templates\project-overlay.md` | `mainline_current` | `formal_template` | `[]` |
| `templates\review-candidate.md` | `mainline_current` | `formal_template` | `[]` |
| `templates\video-source.md` | `mainline_current` | `formal_template` | `[]` |
| `wiki\indexes\knowledge-graph-index.md` | `mainline_current` | `index` | `[]` |
| `outputs\review\2026-06-05-v0-2-13-pro-review-response-revise-candidate.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\cross-project-borrowing-pro-review-package-2026-06-05\candidate_pattern_bank\retrieval-is-activation-not-truth.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\cross-project-borrowing-pro-review-package-2026-06-05\candidate_pattern_bank\search-to-analysis-before-answer.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\cross-project-borrowing-pro-review-package-2026-06-05\candidate_pattern_bank\source-structure-first-rag.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\cross-project-borrowing-pro-review-package-2026-06-05\candidate_pattern_bank\visual-workbench-for-retrieval-diagnostics.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\cross-project-borrowing-pro-review-package-2026-06-05\pilot\2026-06-05-cross-project-borrowing-4-item-pilot-test.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\cross-project-borrowing-pro-review-package-2026-06-05\project_borrowing_ledgers\VAKS.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\cross-project-borrowing-pro-review-package-2026-06-05\source_cards\2026-06-04-external-intake-source-routing-ledger.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\project-lens-closeout-pro-review-package-2026-06-05\01_CURRENT_MAINLINE\ARCHITECTURE_PRINCIPLES.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\project-lens-closeout-pro-review-package-2026-06-05\01_CURRENT_MAINLINE\FUSION_ARCHITECTURE_V0_2_DRAFT.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\project-lens-closeout-pro-review-package-2026-06-05\03_PROJECT_LENS_SANDBOX\2026-06-05-v0-2-13-project-lens-pro-response-landing.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\project-lens-closeout-pro-review-package-2026-06-05\03_PROJECT_LENS_SANDBOX\VAKS.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\project-lens-closeout-pro-review-package-2026-06-05\04_TEST_EVIDENCE\FULL_MAINLINE_COPY_INSERTION_TEST_REPORT.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\project-lens-closeout-pro-review-package-2026-06-05\05_RECOVERY_AND_USAGE\2026-06-05-vaks-v0-2-13-action-support-visibility-handoff.md` | `audit_evidence` | `pro_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\project-lens-full-mainline-copy-test-2026-06-05\baseline\ARCHITECTURE_PRINCIPLES.md` | `audit_evidence` | `audit_package` | `["audit_evidence_not_current_rule"]` |
| `outputs\review\project-lens-full-mainline-copy-test-2026-06-05\baseline\FUSION_ARCHITECTURE_V0_2_DRAFT.md` | `audit_evidence` | `audit_package` | `["audit_evidence_not_current_rule"]` |

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
