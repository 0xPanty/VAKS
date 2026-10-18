---
record_kind: obsidian_workbench_entrypoint_candidate
status: candidate
created_at: 2026-06-07
topic_id: source-intake-routing
truth_boundary: navigation_only
route_map_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/source-intake-route-map.json
artifact_registry_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/fixtures/artifact-registry-source-intake.md
context_pack_builder_ref: outputs/review/source-intake-tag-routing-sandbox-2026-06-07/tools/vaks-context-pack-builder-v0.ps1
allowed_use:
  - navigation
  - query_start
  - context_pack_seed
default_include_lanes:
  - mainline_current
  - reviewed_support
default_exclude_lanes:
  - old_sandbox
  - package_copy
  - baseline_copy
  - archived_overlay
  - feedback_diagnostics
  - unconfirmed_suggestion
forbidden_use:
  - truth
  - reviewed_relation
  - action_basis
  - ontology
  - platform_adoption
---

# Source Intake Routing Workbench

## Start Here

Use this page as the front door for source intake, metadata routing, source-card
metadata, candidate distillation, project overlays, and context pack questions.

Current-rule refs:

```text
SOURCE_INTAKE.md
templates/source-record.md
templates/candidate-distillation.md
templates/query-run.md
00_handoff/2026-06-06-source-intake-control-flow-mainline-merge-handoff.md
```

## Source Route Front Door

| route | use when | borrow source | guard |
|---|---|---|---|
| `source-front-door` | the user needs a clear intake/workbench entrypoint | Dify, AnythingLLM | source route is navigation, not authority |
| `ingestion-parser-route` | parser, connector, chunk, or source hygiene matters | RAGFlow, LlamaIndex | parser/chunk output stays raw or candidate |
| `metadata-router-trace` | metadata/filter/router/trace behavior matters | Haystack, Dify | metadata helps retrieval after authority filters |
| `citation-clickback-route` | source links, citations, or clickback UX matters | AnythingLLM, LlamaIndex | citation UI is not evidence support |
| `action-safety-route` | the question may affect action or decision support | VAKS current rule | candidate/overlay/audit cannot become action basis |

## Modes

```text
current-rule:
  Start from mainline docs and current templates.

research:
  Include raw, candidate, overlay, and support review lanes as orientation.

source-inspection:
  Prioritize raw source cards and candidate distillations.

action:
  Prepare only mainline/reviewed/raw anchors; keep action_readiness:not_ready
  until evidence support check runs.

audit:
  Explain why the sandbox changed; do not treat checks as current rule.
```

## Common Question Entrypoints

These entries convert ordinary questions into a stable workbench mode. They are
navigation presets only.

| question | expected mode | why |
|---|---|---|
| Can this candidate be used as action basis? | `action` | prepare an anchor_queue, not support |
| Show me the source cards behind this scout. | `source-inspection` | inspect raw/candidate intake artifacts |
| What did the GitHub scout teach the workbench? | `research` | compare borrowed design value |
| Why are candidate and overlay excluded from action mode? | `audit` | inspect guardrails and checks |
| What does the VAKS project overlay borrow? | `project-exploration` | inspect project-specific borrowing only |

Router smoke:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-query-intent-router-v0.ps1 `
  -Query 'can this candidate be used as action basis' `
  -Json
```

## Generated Packs

```text
checks/source-intake-routing-workbench-pack-research-generated.md
checks/source-intake-routing-workbench-pack-source-inspection-generated.md
checks/source-intake-routing-workbench-pack-action-generated.md
checks/source-intake-routing-workbench-pack-query-action-generated.md
checks/source-intake-routing-workbench-pack-query-source-inspection-generated.md
checks/source-intake-routing-workbench-pack-query-research-generated.md
checks/source-intake-routing-workbench-pack-query-audit-generated.md
checks/source-intake-routing-workbench-pack-query-project-exploration-generated.md
```

## Commands

Research pack:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-context-pack-builder-v0.ps1 `
  -Root . `
  -Pattern 'source-intake-routing|Dify|RAGFlow|AnythingLLM|LlamaIndex|Haystack|metadata|router|citation|ingestion|source route' `
  -Mode research `
  -TopicId source-intake-routing `
  -Limit 260 `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\source-intake-routing-workbench-pack-research-generated.md
```

Action safety check:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-context-pack-builder-v0.ps1 `
  -Root . `
  -Pattern 'source-intake-routing|Dify|RAGFlow|AnythingLLM|LlamaIndex|Haystack|metadata|router|citation|ingestion|source route|action basis' `
  -Mode action `
  -TopicId source-intake-routing `
  -Limit 260 `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\source-intake-routing-workbench-pack-action-generated.md
```

Natural question to action pack:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-context-pack-builder-v0.ps1 `
  -Root . `
  -Query 'can this candidate be used as action basis' `
  -TopicId source-intake-routing `
  -Limit 260 `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\source-intake-routing-workbench-pack-query-action-generated.md
```

Natural question to source inspection:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-context-pack-builder-v0.ps1 `
  -Root . `
  -Query 'show me the source cards behind this scout' `
  -TopicId source-intake-routing `
  -Limit 260 `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\source-intake-routing-workbench-pack-query-source-inspection-generated.md
```

## Result Roles

```text
selector_or_offset:
  where to start reading; navigation only

snippet:
  small visible preview; navigation only, not evidence

selection_priority:
  pinned refs > exact topic match > entity match > recent scout > ordinary match

action_role:
  action mode uses anchor_queue, not support
```

## External Scout References

```text
raw/repos/2026-06-07-langgenius-dify-source.md
raw/repos/2026-06-07-infiniflow-ragflow-source.md
raw/repos/2026-06-07-mintplex-labs-anything-llm-source.md
raw/repos/2026-06-07-run-llama-llama-index-source.md
raw/repos/2026-06-07-deepset-ai-haystack-source.md
outputs/review/2026-06-07-source-intake-routing-github-scout-candidate-distillation.md
outputs/review/project_overlays/VAKS/VAKS-source-intake-routing-github-scout-2026-06-07.md
```

## Known Exclusions

```text
old sandbox
package copy
baseline copy
zip
archived overlay
feedback diagnostics
unconfirmed suggestions
candidate material in action mode
```

## Boundary

This page is a workbench map.

It does not decide truth, adoption, reviewed status, action readiness, or
architecture promotion.
