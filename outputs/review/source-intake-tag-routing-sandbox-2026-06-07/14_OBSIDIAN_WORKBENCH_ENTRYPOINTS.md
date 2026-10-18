---
type: sandbox_design_note
status: candidate_only
created_at: 2026-06-07
scope: Obsidian workbench and topic entrypoint design
truth_boundary: sandbox design note only; entrypoints are navigation, not reviewed knowledge
---

# Obsidian Workbench Entrypoints

## Plain Rule

```text
Make the front door obvious.
```

The retrieval lanes are the safety mechanism.

The Obsidian workbench is the user experience:

```text
topic entry pages
read-first indexes
artifact registry links
current-rule lane
candidate-reference lane
raw-drilldown lane
active-project-overlay lane
audit-evidence lane
```

## Local Evidence

Borrowed from existing VAKS materials:

```text
hierarchical-index-context-routing:
  start from an index, choose a sub-index, open full notes only after summary/tag match.

Kagantic architecture review:
  index pages as agent entrypoints; summary/tag pre-read.

DataChain candidate distillation:
  compiled markdown workbench can be an agent/human shared read-first surface.

Obsidian practitioner distillations:
  forgotten context resurfaces when the vault has useful entrypoints and steering files.

current source-intake sandbox:
  topic retrieval pack is navigation-only.
```

## Candidate Entrypoints

Create only for repeated, high-value work:

```text
source-intake-routing
retrieval-workbench
candidate-distillation
project-overlay
context-pack
feedback-query-run
vault-health
```

Do not create a page for every tag.

## Topic Entrypoint Shape

```yaml
record_kind: obsidian_workbench_entrypoint_candidate
topic_id:
created_at:
updated_at:
status: candidate
truth_boundary: navigation_only
default_mode:
artifact_registry_ref:
default_include_lanes: []
default_exclude_lanes: []
freshness:
  last_reviewed:
  stale_after:
allowed_use:
  - navigation
  - query_start
  - context_pack_seed
forbidden_use:
  - truth
  - reviewed_relation
  - action_basis
  - ontology
```

Page sections:

```text
Start Here
Current Rule
Candidate Orientation
Raw Drilldown
Active Project Overlay
Audit Evidence
Known Exclusions
Common Queries
Last Refreshed
```

## Include / Exclude Defaults

Default include:

```text
mainline docs
current templates
latest handoff
topic artifact registry
reviewed support if relevant
active project overlay only when project mode is active
```

Default exclude:

```text
old sandbox
package copy
baseline copy
zip
repo snapshot
archived overlay
feedback diagnostics
unconfirmed suggestions
candidate material for action mode
```

## Human Experience

Before:

```text
Search a phrase and inspect 50 mixed results.
```

After:

```text
Open a topic entrypoint.
Read current rule first.
Open candidate references only when researching.
Open raw only for anchors.
Open audit only when asking why/how.
```

## Agent Experience

The agent should use entrypoints as maps:

```text
read entrypoint
read registry
choose mode
apply lane filters
build pack
drill down only when needed
```

The agent must not use entrypoints as:

```text
truth
reviewed relation graph
permission to act
project adoption
```

## Workbench Before Bases

MVP should be plain Markdown.

Optional later:

```text
Obsidian Bases views
SQLite/FTS derived cache
read-only viewer
MCP read resources
```

Do not start with:

```text
mandatory plugin stack
global ontology
automatic daily synthesis
write-enabled agent workbench
```

## Freshness Rule

Every entrypoint needs:

```text
last refreshed
known stale links
latest handoff
latest sandbox/check if relevant
```

If stale:

```text
show warning
do not use as current-rule authority
route to latest handoff/index first
```

## Recommendation

First real entrypoint candidate should be:

```text
source-intake-routing
```

Reason:

```text
It has current mainline docs, active sandbox evidence, candidate distillations,
raw sources, project overlays, and audit checks. It is the best pressure case
for the whole retrieval workbench.
```
