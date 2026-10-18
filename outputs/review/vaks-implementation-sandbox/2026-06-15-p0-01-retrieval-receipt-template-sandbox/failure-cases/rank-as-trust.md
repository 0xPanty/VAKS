---
record_kind: retrieval_receipt_failure_case
case_id: rank-as-trust
expected_future_validator_result: fail
reason: rank_or_score_used_as_trust
---

# Rank As Trust

Invalid pattern:

```yaml
selected_items:
  - ref: outputs/review/example-candidate.md
    authority_bucket: candidate
    pack_role: support
    diagnostic_scores:
      semantic_score: 0.94
      graph_rank: 3
      rrf_rank: 1
      scores_are_support: true
warnings: []
```

Why this fails:

```text
Rank, score, semantic similarity, graph rank, and RRF order are diagnostic
retrieval signals. They are not evidence support, trust, confidence, or action
readiness.
```
