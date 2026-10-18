---
record_kind: sandbox_reviewer_report
slice_id: 2026-06-15-p1-5-13-local-obsidian-graph-retrieval-readonly-mcp-sandbox
status: review_pass_no_blocker
truth_boundary: reviewer_report_only
---

# Reviewer Report

## Reviewer Scope

Read-only review for:

- bugs;
- missing tests;
- overdesign;
- maintainability;
- fixture and failure-case coverage;
- whether local verification really exercises the contract.

## Initial Conclusion

```text
REVIEW_BLOCKERS_FOUND
```

## Initial Blockers

Reviewer found three blockers:

1. `vault_path` pointing to `H:/Obsidian/...` could pass if the manifest also
   declared `sandbox_fixture_only: true`.
2. `has_file_citations + citations_claim_support +
   support_sufficiency_checked: true` could pass, even though generated answers
   with file citations are not evidence support.
3. `FORBIDDEN_AUTHORITY_CLAIMS` did not include plain `support`, so a structural
   triple could claim support while staying candidate-shaped.

## Builder Repair

Builder repaired all three blockers inside this sandbox path:

- formal `H:/Obsidian/...` vault paths now always block in this sandbox;
- file citations that claim support now block even if support/sufficiency is
  marked checked;
- `support`, `direct_support`, `inferential_support`, `reviewed_support`,
  `ready_action_basis`, and `action_ready` were added to forbidden authority
  claims;
- three failure cases were added:
  - `real-vault-path-disguised-fixture.json`;
  - `file-citation-claims-support-even-after-check.json`;
  - `triple-claims-support.json`.

Post-repair observed verification:

```text
positive_fixtures: 4
failure_cases: 20
passed: true
failures: []
```

## Current Conclusion

```text
REVIEW_PASS_NO_BLOCKER
```

## Recheck Evidence

Two independent read-only Reviewer rechecks completed after repair.

Observed verification:

```text
positive_fixtures: 4
failure_cases: 20
passed: true
failures: []
target __pycache__: 0
```

The rechecks confirmed that:

- `real-vault-path-disguised-fixture.json` is blocked by
  `OG_REAL_VAULT_ACCESS_REQUESTED`;
- `file-citation-claims-support-even-after-check.json` is blocked by
  `OG_CITED_ANSWER_ACTION_BASIS`;
- `triple-claims-support.json` is blocked by
  `OG_TRIPLE_CLAIMS_REVIEWED_RELATION`;
- additional triple claims such as `direct_support`, `reviewed_support`,
  `ready_action_basis`, and `action_ready` are also blocked by the authority
  claim rule.

## Residual Risk

This remains a synthetic sandbox oracle. It does not validate a real Obsidian
vault, a real MCP runtime, evidence support, action-basis construction, or
mainline readiness.

## Product Acceptance Revision

The first GPT-5.5 xhigh Product Acceptance pass later returned:

```text
REVISE_BEFORE_NEXT
```

It found that authority-claim blocking had not yet been applied to:

- `derived_cache_manifest.claims`;
- `retrieval_receipt.receipt_claims`;
- receipt-level `vector_score_claims_support` and `score_sets_confidence`;
- `generated_answer.claims`.

Builder repaired these issues inside this sandbox path and added four failure
cases:

- `cache-claims-authority.json`;
- `receipt-claims-authority.json`;
- `receipt-vector-score-claims-support.json`;
- `answer-claims-authority.json`.

Post-repair local verification:

```text
positive_fixtures: 4
failure_cases: 24
passed: true
failures: []
```

## Second Recheck Evidence

Reviewer completed the second read-only recheck after the Product Acceptance
revision repair.

Observed verification:

```text
positive_fixtures: 4
failure_cases: 24
passed: true
failures: []
target __pycache__: 0
```

The recheck confirmed:

- cache claims are blocked by `OG_CACHE_CLAIMS_AUTHORITY`;
- receipt claims are blocked by `OG_RECEIPT_CLAIMS_AUTHORITY`;
- receipt vector/rank/score authority is blocked by
  `OG_RANK_AS_SUPPORT_OR_CONFIDENCE`;
- generated answer claims are blocked by `OG_ANSWER_CLAIMS_AUTHORITY`.

No new blocker, missing key test, overdesign issue, or maintainability blocker
was found.
