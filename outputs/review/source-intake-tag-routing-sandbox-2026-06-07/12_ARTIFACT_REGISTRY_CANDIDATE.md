---
type: sandbox_design_note
status: candidate_only
created_at: 2026-06-07
scope: artifact registry candidate for source intake and retrieval workbench
truth_boundary: sandbox design note only; registry is derived activation/provenance, not reviewed knowledge
---

# Artifact Registry Candidate

## Plain Rule

```text
Before searching raw text again, check what work already exists.
```

The registry is not a new truth layer.

It is a read-first map over existing files:

```text
source card
candidate distillation
project overlay
query-run receipt
context-pack manifest
index build receipt
sync/hash check
```

## Local Evidence

Borrowed from existing VAKS materials:

```text
DataChain candidate distillation:
  read index first, reuse over rebuild, registry-before-recompute.

OpenKB source-hash pattern:
  use content hash / source identity to avoid duplicate ingest and drift.

incremental vault index pattern:
  derived cache can speed lookup, but Markdown remains authoritative.

current source-intake sandbox:
  hard-filter by identity/status/project/path role before relevance ranking.
```

## Candidate Record Shape

```yaml
record_kind: artifact_registry_candidate
registry_id:
topic_or_scope:
created_at:
updated_at:
build_method: manual | script_generated
truth_boundary: derived_index_not_truth
source_of_truth: markdown_files
entries:
  - artifact_id:
    artifact_type: source_card | candidate_distillation | project_overlay | query_run | context_pack | index_build | sync_check
    source_ref:
    path:
    content_hash:
    produced_at:
    produced_by:
    input_refs: []
    output_refs: []
    selector_refs: []
    related_artifacts: []
    lane:
    freshness_status: new | ok | stale | superseded | review_due
    allowed_use:
      - navigation
      - reuse_check
      - drilldown
    forbidden_use:
      - truth
      - reviewed_relation
      - action_basis
    warnings: []
```

## Build Order

```text
1. Read Markdown source records and candidate/review outputs.
2. Extract stable path, record kind/type, status, source refs, and hashes if present.
3. Link known chains:
   source -> candidate distillation -> project overlay -> query-run/context-pack/checks.
4. Publish a derived registry artifact.
5. Write a build receipt with inputs, outputs, warnings, and counts.
```

## Use In Retrieval

Default read-first order:

```text
1. latest handoff / AGENTS / index
2. artifact registry for the topic or source family
3. exact lookup over source IDs, headings, candidate slugs, and paths
4. lane-filtered retrieval
5. raw drilldown only when needed
```

This changes the user experience from:

```text
search everything and infer identities manually
```

to:

```text
see what has already been captured, distilled, tested, packed, or archived.
```

## Hard Boundaries

The registry may:

```text
route
dedupe
show lineage
show freshness
show warnings
help reuse prior work
```

The registry may not:

```text
create reviewed knowledge
promote candidates
set truth confidence
declare action readiness
hide contrary evidence
replace source records
```

## Staleness Rule

If a registry entry is stale, superseded, or review_due:

```text
keep it visible as history
exclude it from action-facing default packs
require a fresher anchor or reviewed replacement before action use
```

## Minimum MVP

For this sandbox, do not build SQLite or a global database.

Use:

```text
Markdown registry fixture
optional JSON later
hash/check receipt
lane classifier output
```

Stop before:

```text
global artifact database
automatic promotion
automatic context-pack builder
remote MCP write interface
```

## Pressure Cases

```text
duplicate source:
  registry warns duplicate hash, but preserves distinct origin if context differs.

stale candidate:
  registry can route to it for history, but cannot use it as current rule.

old sandbox package:
  registry lists it as audit evidence, excluded from current-rule mode.

active overlay:
  registry lists only current project overlay in project mode.

action-facing question:
  registry can find prior candidate/context pack, but final support must return
  to raw or reviewed anchors.
```

## Recommendation

Build this before a context-pack builder.

Reason:

```text
A pack builder needs to know what existing artifacts should be reused before it
decides what to retrieve.
```
