---
record_kind: obsidian_workbench_entrypoint_candidate
status: candidate
created_at: 2026-06-07
topic_id: source-intake-routing
truth_boundary: navigation_only
default_mode: current-rule
artifact_registry_ref: fixtures/artifact-registry-source-intake.md
default_include_lanes:
  - mainline_current
  - reviewed_support
default_exclude_lanes:
  - old_sandbox
  - package_copy
  - baseline_copy
  - archived_overlay
  - feedback_diagnostics
allowed_use:
  - navigation
  - query_start
  - context_pack_seed
forbidden_use:
  - truth
  - reviewed_relation
  - action_basis
  - ontology
---

# Fixture: Source Intake Workbench Entrypoint

## Start Here

Use this entrypoint when the question is about source intake, metadata routing,
retrieval lanes, candidate distillation, project overlays, or context packs.

## Current Rule

```text
SOURCE_INTAKE.md
templates/source-record.md
templates/candidate-distillation.md
templates/query-run.md
latest handoff
```

## Candidate Orientation

```text
DataChain registry-before-recompute
Anthropic identifier-first-payload-later
RAG eval query-run receipt
Obsidian workbench entrypoint patterns
```

## Raw Drilldown

Open raw source only when a source anchor, provenance check, or evidence support
check is needed.

## Audit Evidence

Use sandbox checks only for why/how the design changed.

## Known Exclusions

```text
old sandbox
package copy
baseline copy
zip
archived overlay
feedback diagnostics
unconfirmed suggestions
```
