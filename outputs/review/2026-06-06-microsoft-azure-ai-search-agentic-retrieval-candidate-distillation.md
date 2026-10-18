---
type: candidate_distillation
status: candidate_only
created_at: 2026-06-06
scope: Microsoft Azure AI Search Agentic Retrieval -> VAKS retrieval/query contract
truth_boundary: candidate points only; not reviewed knowledge; not architecture decision; not action basis
source_ref: raw/articles/2026-06-06-microsoft-azure-ai-search-agentic-retrieval-source.md
---

# Microsoft Azure AI Search Agentic Retrieval Candidate Distillation

## Chain

This file tests the VAKS flow:

```text
external official documentation
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
```

## General Knowledge Candidate Judgment

Overall judgment:

```text
yes, this source contains reusable general knowledge point candidates.
```

Reason:

```text
The product-specific implementation is Azure AI Search, but the architecture
ideas are broader: visible query planning, subquery decomposition, parallel
retrieval, modular retrieval responses, activity traces, and cost governance.
```

## Candidate Points

### CP-001: Query Plan As Retrieval Output

```yaml
candidate_id: cp-azure-query-plan-as-retrieval-output
point_text: "Query planning should be a visible retrieval artifact, not hidden prompt logic."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/articles/2026-06-06-microsoft-azure-ai-search-agentic-retrieval-source.md
source_anchor:
  url: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview?tabs=quickstarts
  section: "Why use agentic retrieval / Architecture and workflow"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Add `planner_output` / `planner_mode` to query-run trace and context pack
manifest. Make query type, subquery decisions, branch choices, and stop rules
explicit.
```

Non-borrow scope:

```text
Do not copy Azure's knowledge base object as a VAKS truth object.
```

Candidate tags:

```text
query-planning, agentic-retrieval, retrieval-receipt, context-pack
```

### CP-002: Parallel Subquery Retrieval

```yaml
candidate_id: cp-azure-parallel-subquery-retrieval
point_text: "Complex questions can be decomposed into focused subqueries that run in parallel across retrieval channels."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/articles/2026-06-06-microsoft-azure-ai-search-agentic-retrieval-source.md
source_anchor:
  url: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview?tabs=quickstarts
  section: "Here's what it does / How it works"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
For synthesis, multi_hop, comparison, or corpus_global queries, allow planner
to emit `subqueries[]` and run lexical/dense/metadata/structure branches in
parallel or staged form.
```

Non-borrow scope:

```text
Do not run multi-query agentic retrieval for every exact lookup or low-risk
ordinary query.
```

Candidate tags:

```text
subquery-decomposition, parallel-retrieval, query-planner, retrieval
```

### CP-003: Modular Retrieval Response

```yaml
candidate_id: cp-azure-modular-retrieval-response
point_text: "Retrieval output should separate grounding data, source/reference data, and execution details."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: rationale_check
source_ref: raw/articles/2026-06-06-microsoft-azure-ai-search-agentic-retrieval-source.md
source_anchor:
  url: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview?tabs=quickstarts
  section: "What it does / retrieval component"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Split retrieval outputs into:
grounding_candidates, source_references, execution_trace.
This maps naturally to context pack items, source anchors, and retrieval receipt.
```

Non-borrow scope:

```text
Do not treat grounding candidates as reviewed truth.
```

Candidate tags:

```text
retrieval-response, grounding-data, source-reference, activity-plan
```

### CP-004: Activity Plan As Retrieval Receipt

```yaml
candidate_id: cp-azure-activity-plan-as-retrieval-receipt
point_text: "Query execution steps should be inspectable as a retrieval receipt or activity plan."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: rationale_check
source_ref: raw/articles/2026-06-06-microsoft-azure-ai-search-agentic-retrieval-source.md
source_anchor:
  url: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview?tabs=quickstarts
  section: "retrieval component / tips for controlling costs"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Add a retrieval receipt / query-run trace that records planner decisions,
subqueries, retrievers called, parameters, selected items, dropped high-rank
items, warnings, fallbacks, latency, and token cost.
```

Non-borrow scope:

```text
Do not treat the receipt as authority or reviewed knowledge.
```

Candidate tags:

```text
query-run, retrieval-receipt, trace, diagnostics
```

### CP-005: Agentic Retrieval Cost Governance

```yaml
candidate_id: cp-azure-agentic-retrieval-cost-governance
point_text: "Agentic retrieval should expose cost/latency controls such as reasoning effort, fan-out, number of sources, and rerank window."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: risk_check
source_ref: raw/articles/2026-06-06-microsoft-azure-ai-search-agentic-retrieval-source.md
source_anchor:
  url: https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview?tabs=quickstarts
  section: "Availability and pricing / Tips for controlling costs"
evidence_granularity: official_doc_section
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Add planner budget fields such as max_subqueries, max_sources, rerank_window,
token_budget, latency_budget, and retrieval_depth.
```

Non-borrow scope:

```text
Do not let cost controls hide evidence requirements for action-facing answers.
```

Candidate tags:

```text
retrieval-budget, cost-governance, latency, planner
```

## Proposed General Knowledge Point Candidates

| Candidate slug | Proposed type | Why general |
|---|---|---|
| `query-plan-as-retrieval-output` | pattern | Applies to any complex retrieval pipeline where planning should be inspectable. |
| `parallel-subquery-retrieval` | pattern | Applies to multi-ask, synthesis, and multi-hop retrieval beyond Azure. |
| `modular-retrieval-response` | concept | Separates grounding candidates, source references, and execution trace. |
| `activity-plan-as-retrieval-receipt` | concept | Makes retrieval execution auditable/debuggable. |
| `agentic-retrieval-cost-governance` | pattern | Controls cost/latency/fan-out for planner-driven retrieval. |

Current status:

```text
candidate_only
```

Do not create `wiki/patterns/` or `wiki/concepts/` entries until reviewed.

## Tags Are Navigation Only

Candidate tags:

```yaml
tags:
  - agentic-retrieval
  - azure-ai-search
  - query-planning
  - subquery-decomposition
  - parallel-retrieval
  - semantic-reranking
  - retrieval-receipt
  - activity-plan
  - cost-governance
  - evidence-boundary
```

Rule:

```text
Tags help retrieval and dashboards.
Tags do not prove generality, adoption, truth, or action readiness.
```

## VAKS Project Borrowing View

This is a usage-layer borrowing view, not Project Overlay mainline.

```yaml
kp_candidate_ref: query-plan-as-retrieval-output
borrow_scope: "Make planner_output a visible part of query-run and pack manifest."
non_borrow_scope: "Do not import Azure knowledge base object as VAKS truth model."
target_hint: "future retrieval/query contract; query-run trace"
stance: partial
```

```yaml
kp_candidate_ref: parallel-subquery-retrieval
borrow_scope: "Allow planner to emit subqueries for synthesis/multi-hop/corpus-global queries."
non_borrow_scope: "Do not run agentic multi-query retrieval for every simple lookup."
target_hint: "future query planner; recall funnel"
stance: partial
```

```yaml
kp_candidate_ref: modular-retrieval-response
borrow_scope: "Separate grounding candidates, source references, and execution trace."
non_borrow_scope: "Do not treat grounding candidates as reviewed truth."
target_hint: "future context pack manifest; retrieval receipt"
stance: partial
```

```yaml
kp_candidate_ref: activity-plan-as-retrieval-receipt
borrow_scope: "Record query execution steps, parameters, warnings, fallbacks, and selected/dropped items."
non_borrow_scope: "Do not let receipt become authority."
target_hint: "future retrieval receipt / query-run trace"
stance: partial
```

```yaml
kp_candidate_ref: agentic-retrieval-cost-governance
borrow_scope: "Expose retrieval fan-out, reasoning effort, rerank window, token and latency budgets."
non_borrow_scope: "Do not let budget limits hide evidence gaps for action-facing use."
target_hint: "future planner budget and retrieval profile"
stance: watch
```

## Review / Promotion Requirements

Before any candidate becomes reviewed pattern/concept:

```text
1. Compare with at least one or two other sources:
   LlamaIndex query decomposition, Self-RAG / Adaptive-RAG / CRAG,
   OpenInference tracing, Haystack / Phoenix traces.

2. Check VAKS need:
   query planner and receipt yes; implementation later.

3. Preserve boundary:
   query planning improves activation and coverage.
   it does not create evidence support or reviewed truth.

4. Decide destination:
   pattern for repeatable query/planner behavior.
   concept for response/receipt field design.
```

