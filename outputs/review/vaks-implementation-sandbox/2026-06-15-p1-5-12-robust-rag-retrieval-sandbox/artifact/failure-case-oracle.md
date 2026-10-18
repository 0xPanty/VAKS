---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p1-5-12-robust-rag-retrieval-sandbox
status: implemented_pending_review
truth_boundary: sandbox_oracle_only
---

# Failure Case Oracle

Each failure case contains `expected_valid: false` and expected issue codes.
The suite requires the listed codes. Extra codes are allowed when one malformed
record violates more than one boundary.

| Failure case | Primary expected code |
|---|---|
| `action-query-missing-verbatim.json` | `RR_VERBATIM_INPUT_REQUIRED` |
| `route-missing-buckets.json` | `RR_ROUTE_BUCKETS_MISSING` |
| `cross-bucket-rrf-fusion.json` | `RR_CROSS_BUCKET_FUSION` |
| `selected-excluded-bucket.json` | `RR_SELECTED_EXCLUDED_BUCKET` |
| `vector-rerank-sets-confidence.json` | `RR_SCORE_SET_CONFIDENCE` |
| `graph-path-reviewed-relation.json` | `RR_GRAPH_PATH_REVIEWED_RELATION` |
| `tree-summary-action-support.json` | `RR_SUMMARY_AS_ACTION_SUPPORT` |
| `eval-pass-reviewer-approval.json` | `RR_EVAL_PASS_AS_REVIEWER_APPROVAL` |
| `citation-action-basis-without-support.json` | `RR_CITATION_WITHOUT_SUPPORT_CHECK` |
| `active-retrieval-auto-promotes-candidate.json` | `RR_ACTIVE_RETRIEVAL_AUTO_PROMOTION` |
| `runtime-cache-selected.json` | `RR_RUNTIME_ARTIFACT_SELECTED` |
| `semantic-score-support.json` | `RR_SEMANTIC_ANCHOR_BOUNDARY_FAILED` |
| `community-report-sufficiency.json` | `RR_COMMUNITY_REPORT_SUFFICIENCY` |
| `drift-missing-lineage.json` | `RR_DRIFT_LINEAGE_MISSING` |
| `stale-derived-cache-used.json` | `RR_STALE_DERIVED_CACHE_USED` |
| `plugin-write-mode.json` | `RR_PLUGIN_NOT_READ_ONLY` |
| `candidate-as-support.json` | `RR_CANDIDATE_AS_SUPPORT` |
| `generated-answer-action-basis.json` | `RR_GENERATED_ANSWER_ACTION_BASIS` |
| `selected-by-missing.json` | `RR_SELECTED_BY_MISSING` |
| `runtime-filter-disabled.json` | `RR_RUNTIME_FILTER_DISABLED` |
| `item-semantic-score-claims-support.json` | `RR_SCORE_SET_CONFIDENCE` |
| `graph-artifact-claims-reviewed-relation.json` | `RR_GRAPH_PATH_REVIEWED_RELATION` |

Expected failures are sandbox validation results only. A passing manifest is a
well-shaped retrieval trace, not support, reviewed truth, or action basis.
