---
type: candidate_distillation
status: candidate_only
created_at: 2026-06-06
scope: Microsoft Research GraphRAG query-focused summarization -> VAKS retrieval/query contract
truth_boundary: candidate points only; not reviewed knowledge; not architecture decision; not action basis
source_ref: raw/papers/2026-06-06-microsoft-graphrag-query-focused-summarization-source.md
related_source_ref: raw/repos/2026-05-29-graphrag-source.md
---

# Microsoft GraphRAG Query-Focused Summarization Candidate Distillation

## Chain

This file tests the VAKS flow:

```text
external official publication page
-> source record
-> source extraction
-> candidate points
-> possible general knowledge point candidates
-> tags / indexes / project borrowing view
```

Boundary:

```text
This is candidate distillation.
It does not create reviewed claims, reviewed patterns, or action basis.
It supplements the existing GraphRAG repository/documentation source card.
```

## General Knowledge Candidate Judgment

Overall judgment:

```text
yes, this source contains reusable general knowledge point candidates.
```

Reason:

```text
The product/method is GraphRAG, but the design lesson is broader: some queries
are global corpus sensemaking tasks, not ordinary explicit retrieval tasks.
Those queries need a different retrieval branch and a different receipt shape.
```

## Candidate Points

### CP-001: Global Question As QFS Mode

```yaml
candidate_id: cp-ms-graphrag-global-question-as-qfs-mode
point_text: "Global corpus questions should be routed as query-focused summarization mode, not treated as ordinary local top-k retrieval."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: rationale_check
source_ref: raw/papers/2026-06-06-microsoft-graphrag-query-focused-summarization-source.md
source_anchor:
  url: https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/
  section: "Publication summary"
evidence_granularity: official_publication_page_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Add or strengthen a planner mode for `corpus_global` / `global_sensemaking`
queries such as "what are the main themes", "how has this evolved", or "what
patterns recur across the vault".
```

Non-borrow scope:

```text
Do not send every synthesis query into GraphRAG.
Do not treat global summary as evidence support for a specific claim.
```

Candidate tags:

```text
query-focused-summarization, corpus-global, query-planning, graphrag
```

### CP-002: Community Summary As Global Briefing

```yaml
candidate_id: cp-ms-graphrag-community-summary-as-global-briefing
point_text: "Community summaries can brief global questions, but they are derived context and not reviewed knowledge."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: rationale_check
source_ref: raw/papers/2026-06-06-microsoft-graphrag-query-focused-summarization-source.md
source_anchor:
  url: https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/
  section: "Publication summary"
evidence_granularity: official_publication_page_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Represent community/theme summaries as high-level briefing pack items with
`source_layer: derived_index` and `citable_status: drilldown_required` unless
they carry source selectors back to reviewed anchors.
```

Non-borrow scope:

```text
Do not promote community summaries, graph communities, or global reports into
truth. Do not use them as claim-level support without drilldown.
```

Candidate tags:

```text
community-summary, global-briefing, derived-index, evidence-boundary
```

### CP-003: Local-To-Global Graph Summarization Branch

```yaml
candidate_id: cp-ms-graphrag-local-to-global-graph-summarization-branch
point_text: "A selective graph branch can build from local entity/text anchors toward global community summaries and aggregate partial responses for corpus-level questions."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/papers/2026-06-06-microsoft-graphrag-query-focused-summarization-source.md
source_anchor:
  url: https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/
  section: "Publication summary"
evidence_granularity: official_publication_page_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
For `corpus_global` queries, allow a branch that gathers entity/heading/link
neighborhoods, high-level theme summaries, and partial response receipts before
pack compilation.
```

Non-borrow scope:

```text
Do not adopt the full Microsoft GraphRAG runtime now.
Do not let graph extraction create reviewed relations or action basis.
```

Candidate tags:

```text
local-to-global, graph-branch, corpus-global, partial-response-aggregation
```

## Minimal VAKS Design Delta

If promoted later, this source would strengthen these retrieval/query fields:

```yaml
planner_output:
  query_type: corpus_global | relation_tracing | synthesis | ...
  global_sensemaking: true | false
  structure_branch_allowed: true | false
  selected_structure_branch: none | graph_neighborhood | summary_tree | community_summary

context_pack_manifest:
  high_level_briefings: []
  local_anchor_items: []
  derived_summary_items: []
  drilldown_required: true

query_run_receipt:
  community_or_theme_units_considered:
  partial_response_refs:
  aggregation_method:
  local_anchor_coverage:
  warnings:
```

Hard boundary:

```text
Community summaries, graph neighborhoods, partial responses, and final global
summaries are context-preparation artifacts until they are tied back to source
anchors and claim-level warrants.
```

## What VAKS Should Not Borrow Yet

Do not turn this into:

```text
GraphRAG as primary store
GraphRAG as reviewed relation creator
community report as truth
global summary as action basis
graph centrality or community membership as evidence support
always-on GraphRAG pipeline
```

## Adoption Judgment

```text
adopt as candidate:
  global question / QFS mode in the query planner
  community summaries as high-level briefings with drilldown required

adapt:
  local-to-global graph summarization into a selective structure-aware branch

watch:
  whether real VAKS queries frequently need corpus-global sensemaking

reject for core:
  full GraphRAG runtime or graph/community summary as truth authority
```
