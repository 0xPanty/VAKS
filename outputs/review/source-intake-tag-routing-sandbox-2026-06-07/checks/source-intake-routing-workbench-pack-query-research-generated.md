---
record_kind: context_pack_manifest_candidate
status: candidate
created_at: 2026-06-07T04:04:39+08:00
pack_id: CPACK-source-intake-routing-research-20260607040440
topic_id: source-intake-routing
mode: research
route_map_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/source-intake-route-map.json
query_intent_router_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/query-intent-router-v0.json
query_intent_selected_mode: research
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
user_query: "research source-intake-routing references from high-star repos"
pattern: "source-intake-routing|Dify|RAGFlow|AnythingLLM|LlamaIndex|Haystack|metadata|router|context pack|workbench|research|references|high-star|repos"
original_pattern: "source intake|metadata-routing|context pack|registry-before-recompute|query-run receipt|retrieval_policy"
root: "C:\Users\Administrator\Documents\资料库"
mode: research
original_mode: research
limit: 260
route_map_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/source-intake-route-map.json"
query_intent_router_ref: "outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/query-intent-router-v0.json"
```

## Intent Router

```yaml
selected_mode: research
confidence: high
fallback_used: false
matched_terms: ["research", "reference", "repo", "routing", "source-intake-routing", "references", "high-star", "repos"]
route_bias: ["mainline_current", "raw_drilldown", "candidate_orientation", "active_project_overlay", "support_review_output"]
warnings: ["research_pack_is_orientation_not_truth"]
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
| `source-front-door` | yes | mainline_current, raw_drilldown, candidate_orientation | langgenius/dify, Mintplex-Labs/anything-llm | A visible source route is navigation; it is not authority. |
| `ingestion-parser-route` | yes | raw_drilldown, candidate_orientation | infiniflow/ragflow, run-llama/llama_index | Chunk metadata and parser output stay raw/candidate until evidence review. |
| `metadata-router-trace` | yes | mainline_current, candidate_orientation, support_review_output | deepset-ai/haystack, langgenius/dify | Metadata route hit is not confidence, truth, or action readiness. |
| `citation-clickback-route` | yes | raw_drilldown, reviewed_support | Mintplex-Labs/anything-llm, run-llama/llama_index | A citation link is not evidence support unless the cited span supports the specific point. |
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
| `mainline_current` | 37 | 0 | 5 |
| `reviewed_support` | 70 | 70 | 8 |
| `raw_drilldown` | 99 | 99 | 13 |
| `candidate_orientation` | 34 | 34 | 9 |
| `active_project_overlay` | 20 | 20 | 9 |

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
    selector_or_offset: "line:13"
    snippet: "pack_allowed: activation_only"
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
    selector_or_offset: "line:13"
    snippet: "query_intent: answer | decision | implementation | research | content | memory"
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
    selector_or_offset: "line:12"
    snippet: "policy_kind: project_context_only"
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
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-014
    display_label: "all-in-one-vault-runtime-before-modular-contracts"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\all-in-one-vault-runtime-before-modular-contracts.md"
    selector_or_offset: "line:17"
    snippet: "- '[[scope-dashboard-live-context-surface]]'"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-015
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
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-016
    display_label: "auto-promotion-without-review-gate"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\auto-promotion-without-review-gate.md"
    selector_or_offset: "line:20"
    snippet: "- '[[token-efficient-context-briefing]]'"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-017
    display_label: "binary-vault-template-download-as-trusted-source"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\binary-vault-template-download-as-trusted-source.md"
    selector_or_offset: "line:6"
    snippet: "domain: source-hygiene"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-018
    display_label: "derived-relatedness-as-truth-signal"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\derived-relatedness-as-truth-signal.md"
    selector_or_offset: "line:12"
    snippet: "- '[[algorithmic-graph-scoring-without-source-quality]]'"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-019
    display_label: "direct-compile-to-truth-layer-without-review"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\direct-compile-to-truth-layer-without-review.md"
    selector_or_offset: "line:10"
    snippet: "sources:"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["pack_builder_not_evidence_check"]
  - item_id: PI-020
    display_label: "do-not-blindly-merge-vault-and-agent-brain"
    lane: reviewed_support
    path_role: reviewed_knowledge
    source_ref: "wiki\anti-patterns\do-not-blindly-merge-vault-and-agent-brain.md"
    selector_or_offset: "line:12"
    snippet: "- source verification model"
    snippet_status: navigation_snippet_not_evidence
    selection_priority: 4010
    selection_reason: "ordinary_match > exact_topic_match > entity_match"
    citable_status: drilldown_required
    action_basis_allowed: false
    action_anchor_candidate: false
    action_role: navigation_only
    matched_channels: [path_or_text_match]
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match > recent_scout_or_current_sandbox."
    warnings: ["raw_is_provenance_only", "pack_builder_not_evidence_check"]
  - item_id: PI-027
    display_label: "2026-05-29-graphiti-zep-temporal-validity-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\articles\2026-05-29-graphiti-zep-temporal-validity-source.md"
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
  - item_id: PI-028
    display_label: "2026-05-29-w3c-prov-source"
    lane: raw_drilldown
    path_role: source_card
    source_ref: "raw\articles\2026-05-29-w3c-prov-source.md"
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
  - item_id: PI-029
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
  - item_id: PI-030
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
  - item_id: PI-031
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
  - item_id: PI-032
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
  - item_id: PI-033
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
  - item_id: PI-034
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
  - item_id: PI-035
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
  - item_id: PI-036
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
    why_included: "Matched query pattern inside allowed lane for mode 'research'; ranked as ordinary_match > exact_topic_match > entity_match."
    warnings: ["candidate_not_action_basis", "pack_builder_not_evidence_check"]
  - item_id: PI-037
    display_label: "VAKS-get-it-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS-get-it-2026-06-07.md"
    selector_or_offset: "line:12"
    snippet: "policy_kind: project_context_only"
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
  - item_id: PI-038
    display_label: "VAKS-linkwarden-linkwarden-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS-linkwarden-linkwarden-2026-06-07.md"
    selector_or_offset: "line:12"
    snippet: "policy_kind: project_context_only"
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
  - item_id: PI-039
    display_label: "VAKS-obsidian-excalidraw-example-vault-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS-obsidian-excalidraw-example-vault-2026-06-07.md"
    selector_or_offset: "line:12"
    snippet: "policy_kind: project_context_only"
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
  - item_id: PI-040
    display_label: "VAKS-obsidian-excalidraw-plugin-ymjr-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS-obsidian-excalidraw-plugin-ymjr-2026-06-07.md"
    selector_or_offset: "line:12"
    snippet: "policy_kind: project_context_only"
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
  - item_id: PI-041
    display_label: "VAKS-obsidian-excalidraw-scripts-2026-06-07"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS-obsidian-excalidraw-scripts-2026-06-07.md"
    selector_or_offset: "line:12"
    snippet: "policy_kind: project_context_only"
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
  - item_id: PI-042
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
  - item_id: PI-043
    display_label: "VAKS-cyrilxbt-claude-obsidian-90-days-2026-06-06"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS\VAKS-cyrilxbt-claude-obsidian-90-days-2026-06-06.md"
    selector_or_offset: "line:11"
    snippet: "retrieval_policy: project_context_only"
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
  - item_id: PI-044
    display_label: "VAKS-cyrilxbt-obsidian-from-scratch-2026-06-06"
    lane: active_project_overlay
    path_role: project_overlay
    source_ref: "outputs\review\project_overlays\VAKS\VAKS-cyrilxbt-obsidian-from-scratch-2026-06-06.md"
    selector_or_offset: "line:11"
    snippet: "retrieval_policy: project_context_only"
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
```

## Excluded Or Not Default

These hits matched the query but are not selected for this mode/default pack.

| file | lane | path_role | caution |
|---|---|---|---|
| `00_handoff\2026-05-26-knowledge-compile-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `00_handoff\2026-05-27-verified-action-knowledge-system-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `00_handoff\2026-05-28-verified-action-knowledge-system-v0-2-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-10-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-11-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-12-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-13-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-8-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `00_handoff\2026-05-29-verified-action-knowledge-system-v0-2-pro-1-9-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `00_handoff\2026-05-30-verified-action-knowledge-system-v0-3-evidence-discipline-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `00_handoff\2026-05-31-route-lock-confirmation-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `00_handoff\2026-06-05-vaks-v0-2-13-action-support-visibility-handoff.md` | `mainline_current` | `handoff` | `[]` |
| `AGENTS.md` | `mainline_current` | `project_guide` | `[]` |
| `ARCHITECTURE_PRINCIPLES.md` | `mainline_current` | `mainline_doc` | `[]` |
| `DEV_CONTEXT.md` | `mainline_current` | `mainline_doc` | `[]` |
| `FEEDBACK.md` | `mainline_current` | `mainline_doc` | `[]` |
| `FUSION_ARCHITECTURE_V0_2_DRAFT.md` | `mainline_current` | `mainline_doc` | `[]` |
| `IMPLEMENTATION_BLUEPRINT.md` | `mainline_current` | `mainline_doc` | `[]` |
| `MEMORY_TIER.md` | `mainline_current` | `mainline_doc` | `[]` |
| `purpose.md` | `mainline_current` | `mainline_doc` | `[]` |
| `README.md` | `mainline_current` | `mainline_doc` | `[]` |
| `REFERENCE_REVIEW_PROTOCOL.md` | `mainline_current` | `mainline_doc` | `[]` |
| `REVIEW_QUEUE.md` | `mainline_current` | `mainline_doc` | `[]` |
| `SCHEMA.md` | `mainline_current` | `mainline_doc` | `[]` |

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
