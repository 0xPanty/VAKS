---
type: candidate_distillation
status: candidate_only
created_at: 2026-06-06
scope: arXiv retrieval / context / evaluation papers -> VAKS retrieval/query contract
truth_boundary: candidate points only; not reviewed knowledge; not architecture decision; not action basis
source_refs:
  - raw/papers/2026-06-06-lost-in-the-middle-source.md
  - raw/papers/2026-06-06-ares-rag-evaluation-source.md
  - raw/papers/2026-05-29-self-rag-source.md
  - raw/papers/2026-06-06-raptor-source.md
  - raw/papers/2026-06-06-adaptive-rag-source.md
  - raw/papers/2026-06-06-longcite-source.md
  - raw/papers/2026-06-06-rag-vs-graphrag-systematic-evaluation-source.md
---

# arXiv Retrieval Batch Candidate Distillation

## Chain

This file tests the VAKS flow:

```text
external papers
-> source records
-> source extraction
-> candidate points
-> possible general knowledge point candidates
-> tags / indexes / project borrowing view
```

Boundary:

```text
This is candidate distillation.
It does not create reviewed claims, reviewed patterns, or action basis.
ARES was provided twice by the user and is deduplicated here.
Self-RAG already had a source card, so this batch reuses that existing card.
```

## General Knowledge Candidate Judgment

Overall judgment:

```text
yes, this batch contains reusable general knowledge point candidates.
```

Reason:

```text
The individual methods differ, but their reusable design lessons converge on
the same VAKS retrieval-contract needs: context order matters, evaluation
dimensions must stay separated, retrieval depth should adapt to query
complexity, summary/graph branches should be selective, and action-facing use
needs fine-grained claim-to-evidence binding.
```

## Candidate Points

### CP-001: Position-Aware Context Pack Ordering

```yaml
candidate_id: cp-arxiv-position-aware-context-pack-ordering
point_text: "Context pack order should be intentional because long-context models may underuse relevant information buried in the middle."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/papers/2026-06-06-lost-in-the-middle-source.md
source_anchor:
  url: https://arxiv.org/abs/2307.03172
  section: "Abstract"
evidence_granularity: arxiv_abstract
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Pack compiler should put high-priority evidence anchors, query plan, and
selector-grade drilldown pointers in predictable visible positions rather than
burying them inside a long undifferentiated context dump.
```

Non-borrow scope:

```text
Do not treat position as evidence support.
Do not assume long context removes the need for retrieval, pack selection, or
claim-level evidence binding.
```

### CP-002: RAG Eval Dimensions Are Separate

```yaml
candidate_id: cp-arxiv-rag-eval-dimensions-are-separate
point_text: "Context relevance, answer faithfulness, and answer relevance are separate diagnostic dimensions and should not collapse into one truth score."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: rationale_check
source_ref: raw/papers/2026-06-06-ares-rag-evaluation-source.md
source_anchor:
  url: https://arxiv.org/abs/2311.09476
  section: "Abstract"
evidence_granularity: arxiv_abstract
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use separate diagnostic labels in query-run receipts:
context_relevance, answer_faithfulness, answer_relevance, and evidence_binding.
```

Non-borrow scope:

```text
Do not treat evaluator scores as reviewed truth confidence.
Do not let automated evaluation promote knowledge.
```

### CP-003: On-Demand Retrieval And Critique

```yaml
candidate_id: cp-arxiv-on-demand-retrieval-and-critique
point_text: "Retrieval and critique should be triggered by task need rather than applied indiscriminately with a fixed number of passages."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: already_partially_absorbed_check
source_ref: raw/papers/2026-05-29-self-rag-source.md
source_anchor:
  url: https://arxiv.org/abs/2310.11511
  section: "Abstract"
evidence_granularity: arxiv_abstract
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use this to strengthen query planner / risk typing: ordinary queries can stay
light, while promotion, decision, action-facing, multi-hop, or unsupported
claim cases can escalate.
```

Non-borrow scope:

```text
Do not implement Self-RAG training, reflection tokens, or self-approval.
Do not let model self-critique decide truth.
```

### CP-004: Summary Tree As Selective Structure Branch

```yaml
candidate_id: cp-arxiv-summary-tree-as-selective-structure-branch
point_text: "Summary-tree retrieval can help long-document or corpus-level synthesis, but should remain a selective structure-aware branch."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/papers/2026-06-06-raptor-source.md
source_anchor:
  url: https://arxiv.org/abs/2401.18059
  section: "Abstract"
evidence_granularity: arxiv_abstract
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Planner may enter a summary-tree branch for corpus_global, long_document,
synthesis, or multi_step reasoning queries.
```

Non-borrow scope:

```text
Do not turn generated summaries into reviewed knowledge.
Do not use summary tree hits as evidence support without source selectors.
```

### CP-005: Query Complexity Router

```yaml
candidate_id: cp-arxiv-query-complexity-router
point_text: "Query complexity should guide retrieval strategy, from no retrieval to single-step retrieval to more complex iterative strategies."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/papers/2026-06-06-adaptive-rag-source.md
source_anchor:
  url: https://arxiv.org/abs/2403.14403
  section: "Abstract"
evidence_granularity: arxiv_abstract
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Add an explicit planner mode such as:
exact_lookup, factual_lookup, synthesis, multi_hop, corpus_global, or
action_facing.
```

Non-borrow scope:

```text
Do not require a trained complexity classifier now.
Do not let planner confidence become evidence confidence.
```

### CP-006: Sentence-Level Citation Binding

```yaml
candidate_id: cp-arxiv-sentence-level-citation-binding
point_text: "Long-context answers need fine-grained citation or claim-to-evidence binding rather than document-level citation only."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/papers/2026-06-06-longcite-source.md
source_anchor:
  url: https://arxiv.org/abs/2409.02897
  section: "Abstract"
evidence_granularity: arxiv_abstract
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
For action-facing answer/use, extract claims and bind each claim to source_id,
selector/offset, quote window, support status, and gap/counterevidence notes.
```

Non-borrow scope:

```text
Do not implement LongCite training.
Do not treat a citation marker as sufficient support by itself.
```

### CP-007: Selective GraphRAG Branch

```yaml
candidate_id: cp-arxiv-selective-graphrag-branch
point_text: "GraphRAG and text RAG have task-dependent strengths and trade-offs; graph retrieval should be a selective branch, not the default truth skeleton."
candidate_general_knowledge: true
proposed_node_type: pattern
review_route: rationale_check
source_ref: raw/papers/2026-06-06-rag-vs-graphrag-systematic-evaluation-source.md
source_anchor:
  url: https://arxiv.org/abs/2502.11371
  section: "Abstract"
evidence_granularity: arxiv_abstract
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Use graph / heading / entity / relation neighborhood only when planner marks
multi_hop, relation_tracing, corpus_global, or synthesis needs.
```

Non-borrow scope:

```text
Do not make GraphRAG the primary store.
Do not treat graph rank, centrality, or community summary as support strength.
```

### CP-008: Retrieval Strategy As Costed Choice

```yaml
candidate_id: cp-arxiv-retrieval-strategy-as-costed-choice
point_text: "Retrieval strategy should be selected with visible cost, latency, and failure-mode trade-offs."
candidate_general_knowledge: true
proposed_node_type: concept
review_route: rationale_check
source_ref:
  - raw/papers/2026-06-06-adaptive-rag-source.md
  - raw/papers/2026-06-06-rag-vs-graphrag-systematic-evaluation-source.md
source_anchor:
  url:
    - https://arxiv.org/abs/2403.14403
    - https://arxiv.org/abs/2502.11371
  section: "Abstract"
evidence_granularity: arxiv_abstract
promotion_readiness: not_ready
```

VAKS borrow scope:

```text
Record retrieval_depth, branch choices, fallbacks, latency, and token/cost
warnings in query-run receipts.
```

Non-borrow scope:

```text
Do not hide planner fan-out in prompt behavior.
Do not treat expensive retrieval as automatically more correct.
```

## Minimal VAKS Design Delta

If promoted later, this batch would strengthen the retrieval/query contract in
these places:

```yaml
planner_output:
  query_type:
  risk_mode:
  complexity_level:
  retrieval_depth:
  selected_strategy:
  selected_strategy_reason:
  structure_branch_allowed:
  cost_budget:

context_pack_manifest:
  ordering_policy:
  evidence_priority_positions:
  summary_before_detail:
  selector_drilldown_required:

pack_item:
  item_priority:
  position_reason:
  citable_status:
  source_selector:
  quote_window:

query_run_receipt:
  context_relevance_diagnostic:
  answer_faithfulness_diagnostic:
  answer_relevance_diagnostic:
  evidence_binding_status:
  latency_by_stage:
  cost_or_token_warning:
```

Hard boundary:

```text
Retrieval strategy, context position, evaluator score, citation marker, graph
rank, and summary-tree hit are activation or diagnostic signals only until
linked to explicit source anchors and a claim-level warrant.
```

## What VAKS Should Not Borrow Yet

Do not turn this batch into:

```text
mandatory trained query router
always-on agentic retrieval
always-on GraphRAG
RAPTOR as default retrieval skeleton
ARES as truth evaluator
LongCite as citation infrastructure
automatic self-reflection approval
universal retrieval confidence score
```

## Adoption Judgment

```text
adopt as candidate:
  query complexity router
  position-aware pack compiler
  sentence/claim-level evidence binding
  separated retrieval/eval diagnostics

adapt:
  RAPTOR/GraphRAG into selective structure-aware branches
  Self-RAG/Adaptive-RAG into planner stop/escalation rules

watch:
  whether VAKS's real query runs justify graph or summary-tree tooling

reject for core:
  turning any evaluator, retriever, graph, or citation generator into truth authority
```
