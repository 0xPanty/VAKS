---
record_kind: sandbox_metric_dictionary
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: metric_dictionary_not_truth_layer
action_basis_allowed: false
---

# Phase B Metric Dictionary

This file defines the current sandbox metrics. It is diagnostic only.

| Metric | Level | Definition | Denominator | Notes |
|---|---|---|---|---|
| hit_at_5 | query aggregate | A query is counted when the harness first_hit_rank over the top20 local run is <= 5. | Resolvable queries for that test_set/corpus/mode. | Top10 replay independently checks rows whose first_hit_rank is within 10; ranks >10 remain query-level paired outcomes. |
| hit_at_10 | query aggregate | A query is counted when the harness first_hit_rank over the top20 local run is <= 10. | Resolvable queries for that test_set/corpus/mode. | Top10 replay should contain the matching hit when this metric is true. |
| mrr | query aggregate | Mean reciprocal rank over the local top20 run; query contribution is 1 / first_hit_rank, or 0 if no expected-term hit appears in top20. | Resolvable queries for that test_set/corpus/mode. | This is a retrieval diagnostic, not truth confidence. |
| action_leakage_rate | risk-query aggregate | For action/evidence queries, true when top1 is not support bucket or any risky top10 result has no warning. | Queries whose intent is action or evidence. | This is the strongest current governance signal. |
| forbidden_top1_rate | risk-query aggregate | For action/evidence queries, true when rank 1 is not in support buckets. | Queries whose intent is action or evidence. | Support buckets are core_framework and reviewed. |
| cross_bucket_violation_rate | risk-query aggregate | For action/evidence queries, true when risky buckets appear before the first support bucket in top10, or no support appears. | Queries whose intent is action or evidence. | Measures authority-like ranking collapse. |
| warning_coverage_risk | risk-query aggregate | For risky top10 results, fraction that carry a warning_code; if no risky result appears, the query receives 1.0. | Risky top10 results within each risk query, then averaged by query. | Soft guardrail only; not a hard safety control. |
| clickback_coverage | query aggregate | Average top10 fraction with clickback-present behavior. | Top10 result rows per query, then averaged by query. | Baseline file lexical has 0 by design in the current harness. |
| hash_coverage | query aggregate | Average top10 fraction with source_hash/chunk_hash available. | Top10 result rows per query, then averaged by query. | Used for auditability, not evidence support. |
| receipt_coverage | query aggregate | Average top10 fraction produced through adapter receipt behavior. | Top10 result rows per query, then averaged by query. | Receipt does not create action basis. |
| stale_detection_rate | stale query aggregate | Detected stale top10 results divided by exposed stale top10 results for stale-pressure queries, including holdout_stale. | Exposed stale results in stale-pressure queries. | P0 fixes the earlier ambiguity where holdout_stale was not counted by the older summary helper. |
