---
record_kind: sandbox_robust_rag_contract
slice_id: 2026-06-15-p1-5-12-robust-rag-retrieval-sandbox
status: implemented_pending_review
truth_boundary: sandbox_contract_only
---

# Robust RAG Retrieval Contract

## Purpose

This sandbox proves a narrow retrieval contract:

```text
robust RAG decides what to read;
VAKS evidence gates decide what can support;
VAKS action gates decide what can be acted on.
```

The runner validates synthetic JSON manifests. It does not build a vector store,
GraphRAG runtime, MCP server, Obsidian integration, or production validator.

## Input Format

Input is one JSON file:

```json
{
  "record_kind": "robust_rag_retrieval_manifest",
  "scenario_id": "example",
  "expected_valid": true,
  "expected_codes": [],
  "query": {},
  "route_selection": {},
  "retrieval_config": {},
  "fusion_groups": [],
  "retrieved_items": [],
  "generated_answer": {},
  "derived_cache_manifest": {},
  "optional_plugin": {}
}
```

## Query Contract

The query object records:

- `query_mode`: `orientation`, `source_inspection`, `review`, or `action`;
- `verbatim_input`;
- `question_summary`;
- `action_sensitive`;
- `verbatim_preserved`.

Action-sensitive tasks must preserve verbatim user input.

## Route Contract

The route records:

- `selected`: `local_entity`, `global_theme`, `drift_explore`,
  `basic_vector`, or `hybrid_bucketed`;
- `authority_buckets_included`;
- `authority_buckets_excluded`;
- `selected_context_types`;
- `forbidden_support_types`;
- optional `query_lineage` for DRIFT routes.

Required forbidden support types:

- `retrieval_score`
- `graph_rank`
- `community_report_summary`
- `llm_extracted_relation`

## Retrieval Config

Required:

```json
{
  "bucket_filter_first": true,
  "rrf_within_bucket_only": true,
  "exclude_runtime_artifacts": true
}
```

RRF, rerank, vector, BM25, temporal, synonym, and graph scores can combine
relevance only inside an allowed authority bucket.

## Item Contract

Each `retrieved_items` entry may expose:

- `authority_bucket`;
- `record_kind`;
- `pack_role`;
- `selected`;
- `excluded`;
- `selected_by`;
- scores/ranks;
- `semantic_anchor` checked by P1-11;
- runtime artifact fields checked by P1-10.

Selected items must expose `selected_by`. Runtime artifacts must be excluded.
Candidate, feedback, project overlay, community report, graph relation, and
generated output records cannot become support or action basis.

## Reused P1 Gates

- P1-10 runtime artifact exclusion is imported read-only.
- P1-11 semantic anchor support check is imported read-only.

## Blocking Codes

| Code | Meaning |
|---|---|
| `RR_INVALID_RECORD_KIND` | Wrong manifest record kind. |
| `RR_MISSING_SCENARIO_ID` | Missing scenario id. |
| `RR_MISSING_QUERY` | Missing query object. |
| `RR_UNKNOWN_QUERY_MODE` | Unknown query mode. |
| `RR_VERBATIM_INPUT_REQUIRED` | Action-sensitive query failed verbatim preservation. |
| `RR_MISSING_QUESTION_SUMMARY` | Query lacks summary. |
| `RR_MISSING_ROUTE_SELECTION` | Missing route selection. |
| `RR_UNKNOWN_ROUTE_MODE` | Unknown robust retrieval route. |
| `RR_ROUTE_BUCKETS_MISSING` | Included/excluded buckets not recorded. |
| `RR_UNKNOWN_AUTHORITY_BUCKET` | Unknown bucket in route or item. |
| `RR_FORBIDDEN_SUPPORT_TYPES_MISSING` | Receipt omits forbidden support type list. |
| `RR_DRIFT_LINEAGE_MISSING` | DRIFT route lacks query lineage/user intent. |
| `RR_MISSING_RETRIEVAL_CONFIG` | Missing retrieval config. |
| `RR_BUCKET_FILTER_NOT_FIRST` | Ranking/fusion happens before bucket filtering. |
| `RR_RRF_NOT_BUCKET_LOCAL` | Fusion is not constrained inside buckets. |
| `RR_RUNTIME_FILTER_DISABLED` | Runtime artifact exclusion disabled. |
| `RR_INVALID_FUSION_GROUPS` | Fusion groups malformed. |
| `RR_CROSS_BUCKET_FUSION` | RRF/rerank merges across authority buckets. |
| `RR_MISSING_RETRIEVED_ITEMS` | No retrieved items. |
| `RR_INVALID_RETRIEVED_ITEM` | Retrieved item is malformed. |
| `RR_DUPLICATE_ITEM_ID` | Retrieved item ids are duplicated. |
| `RR_MISSING_ITEM_ID` | Retrieved item lacks id. |
| `RR_SELECTED_EXCLUDED_BUCKET` | Selected item comes from excluded bucket. |
| `RR_SELECTED_BUCKET_NOT_INCLUDED` | Selected item bucket was not included by route. |
| `RR_RUNTIME_ARTIFACT_SELECTED` | Runtime artifact was selected. |
| `RR_RUNTIME_ARTIFACT_NOT_EXCLUDED` | Runtime artifact was not excluded. |
| `RR_SCORE_SET_CONFIDENCE` | Score/rank claims support, confidence, or trust. |
| `RR_GRAPH_PATH_REVIEWED_RELATION` | Graph path or extracted relation creates reviewed relation. |
| `RR_SUMMARY_AS_ACTION_SUPPORT` | Community/RAPTOR/tree summary becomes support/action basis. |
| `RR_COMMUNITY_REPORT_SUFFICIENCY` | Community report satisfies sufficiency without drilldown. |
| `RR_CANDIDATE_AS_SUPPORT` | Candidate/review_input/project overlay becomes support/action basis. |
| `RR_FEEDBACK_AS_SUPPORT` | Feedback becomes support. |
| `RR_RETRIEVAL_ITEM_ACTION_BASIS` | Retrieved item claims action basis. |
| `RR_SUPPORT_BUCKET_INVALID` | Support role is outside a support bucket. |
| `RR_SELECTED_BY_MISSING` | Selected item lacks selected_by trace. |
| `RR_SEMANTIC_ANCHOR_BOUNDARY_FAILED` | P1-11 semantic anchor check blocks the item. |
| `RR_EVAL_PASS_AS_REVIEWER_APPROVAL` | Eval pass becomes reviewer approval. |
| `RR_ACTIVE_RETRIEVAL_AUTO_PROMOTION` | Active retrieval auto-promotes candidate. |
| `RR_GENERATED_ANSWER_ACTION_BASIS` | Generated answer claims action basis. |
| `RR_CITATION_WITHOUT_SUPPORT_CHECK` | Citations are used for action without support/sufficiency checks. |
| `RR_PLUGIN_NOT_READ_ONLY` | Optional plugin exposes writes or auto-update. |
| `RR_STALE_DERIVED_CACHE_USED` | Stale/mismatched derived cache is used silently. |

## Non-Claims

Passing this sandbox is not evidence support, reviewer approval, reviewed
knowledge, action basis, production readiness, mainline merge permission, commit
permission, push permission, or Obsidian sync permission.
