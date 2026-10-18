---
type: sandbox_check
status: pass
created_at: 2026-06-07
scope: GitHub scout for source-intake-routing workbench
truth_boundary: sandbox scout evidence only; not reviewed knowledge; not action basis
action_basis_allowed: false
truth_mutation_allowed: false
---

# GitHub Source-Intake-Routing Scout

## Question

Which high-star, recently active GitHub repos provide useful reference material
for the first `source-intake-routing` workbench entrypoint?

## Selection Rule

```text
At least 5 repos.
Prefer high-star and recently pushed.
Must have direct relevance to source intake, knowledge workbench, metadata
routing, ingestion, context pack, connector, parser, citation/clickback, or
retrieval trace.
```

## Selected Sources

| Repo | Stars captured | Pushed at | Source card |
|---|---:|---|---|
| `langgenius/dify` | 144154 | 2026-06-06T16:00:22Z | `raw/repos/2026-06-07-langgenius-dify-source.md` |
| `infiniflow/ragflow` | 82040 | 2026-06-05T13:59:26Z | `raw/repos/2026-06-07-infiniflow-ragflow-source.md` |
| `Mintplex-Labs/anything-llm` | 61149 | 2026-06-06T00:16:52Z | `raw/repos/2026-06-07-mintplex-labs-anything-llm-source.md` |
| `run-llama/llama_index` | 49958 | 2026-06-04T16:59:44Z | `raw/repos/2026-06-07-run-llama-llama-index-source.md` |
| `deepset-ai/haystack` | 25467 | 2026-06-05T14:24:07Z | `raw/repos/2026-06-07-deepset-ai-haystack-source.md` |

## Why These Five

```text
Dify:
  product workbench for dataset/document/RAG pipeline/retrieval/observability.

RAGFlow:
  ingestion templates, document/chunk APIs, connectors, parser routes.

AnythingLLM:
  source route UI and Obsidian/GitHub/website/citation workbench references.

LlamaIndex:
  reader/parser/ingestion/router/citation component boundary.

Haystack:
  metadata filtering, routers, document store, pipeline tracing.
```

## Distillation Artifacts

```text
outputs/review/2026-06-07-source-intake-routing-github-scout-candidate-distillation.md
outputs/review/project_overlays/VAKS/VAKS-source-intake-routing-github-scout-2026-06-07.md
```

## Verdict

```text
status=pass
minimum_sources_required=5
sources_checked=5
candidate_only=true
action_basis_allowed=false
```

## Boundary Check

New files checked:

```text
files_checked=8
action_basis_allowed_false=8/8
truth_mutation_allowed_false=8/8
action_basis_allowed_true=0/8
```

Action-mode retrieval smoke for:

```text
source-intake-routing|github-scout|Dify|RAGFlow|AnythingLLM|LlamaIndex|Haystack
```

Result:

```text
active_project_overlay: 2 total / 0 included_by_default
audit_evidence: 54 total / 0 included_by_default
candidate_orientation: 13 total / 0 included_by_default
feedback_diagnostics: 1 total / 0 included_by_default
mainline_current: 3 total / 3 included_by_default
raw_drilldown: 11 total / 11 included_by_default
reviewed_support: 2 total / 2 included_by_default
support_review_output: 27 total / 0 included_by_default
```

Interpretation:

```text
The 5 new repo cards can appear as raw drilldown, but remain provenance-only.
The new candidate distillation and project overlay do not enter action mode by
default.
```

The scout supports the next sandbox step:

```text
draft a real source-intake-routing Obsidian entrypoint with source-route front
door, lane-labeled context packs, and explicit exclusions.
```
