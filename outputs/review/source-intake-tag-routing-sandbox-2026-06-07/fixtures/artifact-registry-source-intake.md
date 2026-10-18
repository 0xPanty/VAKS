---
record_kind: artifact_registry_candidate
status: candidate
created_at: 2026-06-07
topic_or_scope: source-intake-routing
truth_boundary: derived_index_not_truth
source_of_truth: markdown_files
build_method: manual_fixture
allowed_use:
  - navigation
  - reuse_check
  - drilldown
forbidden_use:
  - truth
  - reviewed_relation
  - action_basis
---

# Fixture: Source Intake Artifact Registry

## Entries

```yaml
entries:
  - artifact_id: source-intake-mainline
    artifact_type: mainline_doc
    path: SOURCE_INTAKE.md
    lane: mainline_current
    freshness_status: ok
    warnings: []

  - artifact_id: source-intake-control-flow-sandbox
    artifact_type: sandbox_check
    path: outputs/review/source-intake-control-flow-sandbox-2026-06-06/checks/mainline-merge-audit.md
    lane: audit_evidence
    freshness_status: ok
    warnings:
      - process_evidence_not_current_rule

  - artifact_id: source-intake-tag-routing-sandbox
    artifact_type: sandbox_design
    path: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/README.md
    lane: audit_evidence
    freshness_status: candidate
    warnings:
      - sandbox_not_mainline

  - artifact_id: source-intake-route-map
    artifact_type: workbench_route_map
    path: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/source-intake-route-map.json
    lane: audit_evidence
    freshness_status: candidate
    warnings:
      - route_map_navigation_not_truth

  - artifact_id: source-intake-workbench-entrypoint
    artifact_type: obsidian_workbench_entrypoint
    path: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/workbench/source-intake-routing.md
    lane: audit_evidence
    freshness_status: candidate
    warnings:
      - workbench_navigation_not_truth

  - artifact_id: source-intake-github-scout-distillation
    artifact_type: candidate_distillation
    path: outputs/review/2026-06-07-source-intake-routing-github-scout-candidate-distillation.md
    lane: candidate_orientation
    freshness_status: ok
    warnings:
      - candidate_not_action_basis

  - artifact_id: source-intake-github-scout-overlay
    artifact_type: project_overlay
    path: outputs/review/project_overlays/VAKS/VAKS-source-intake-routing-github-scout-2026-06-07.md
    lane: active_project_overlay
    freshness_status: ok
    warnings:
      - overlay_not_authority

  - artifact_id: github-scout-dify
    artifact_type: raw_source_card
    path: raw/repos/2026-06-07-langgenius-dify-source.md
    lane: raw_drilldown
    freshness_status: ok
    warnings:
      - raw_is_provenance_only

  - artifact_id: github-scout-ragflow
    artifact_type: raw_source_card
    path: raw/repos/2026-06-07-infiniflow-ragflow-source.md
    lane: raw_drilldown
    freshness_status: ok
    warnings:
      - raw_is_provenance_only

  - artifact_id: github-scout-anything-llm
    artifact_type: raw_source_card
    path: raw/repos/2026-06-07-mintplex-labs-anything-llm-source.md
    lane: raw_drilldown
    freshness_status: ok
    warnings:
      - raw_is_provenance_only

  - artifact_id: github-scout-llama-index
    artifact_type: raw_source_card
    path: raw/repos/2026-06-07-run-llama-llama-index-source.md
    lane: raw_drilldown
    freshness_status: ok
    warnings:
      - raw_is_provenance_only

  - artifact_id: github-scout-haystack
    artifact_type: raw_source_card
    path: raw/repos/2026-06-07-deepset-ai-haystack-source.md
    lane: raw_drilldown
    freshness_status: ok
    warnings:
      - raw_is_provenance_only

  - artifact_id: datachain-registry-before-recompute
    artifact_type: candidate_distillation
    path: outputs/review/2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md
    lane: candidate_orientation
    freshness_status: ok
    warnings:
      - candidate_not_action_basis

  - artifact_id: old-package-copy
    artifact_type: pro_package
    path: outputs/review/PRO_OPERATING_CONTRACTS_RESEARCH_PACKET_2026-06-06/
    lane: audit_evidence
    freshness_status: historical
    warnings:
      - package_copy_excluded_by_default
```

## Boundary

The registry tells a reader what exists.

It does not decide truth, adoption, action readiness, or review outcome.
