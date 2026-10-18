---
record_kind: sandbox_external_review_request
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: review_request_not_review_result
action_basis_allowed: false
---

# Pro Review Request: VAKS + Yuxi-like Phase B

## Plain Context

We tested whether Yuxi-like retrieval ideas should be adapted into VAKS.

Current local conclusion:

```text
Yuxi-like capabilities are useful as VAKS's retrieval / hand-eye layer.
VAKS must still own authority buckets, truth boundaries, review gates, and action-basis discipline.
Do not merge original Yuxi runtime or C-lite from this evidence alone.
```

## What To Audit

Please review the attached package and challenge the conclusion.

Focus on these questions:

```text
1. Do the metrics actually support VAKS+B over single VAKS baseline and Yuxi-native profile?
2. Is VAKS adding real value, or are most gains simply from Yuxi-like retrieval?
3. Are the sample sets too small, biased, or tuned to favor VAKS+B?
4. Is the current best fusion shape correct: VAKS authority bucket first, then Yuxi-like retrieval/rerank/clickback inside the boundary?
5. Did the tests check more than retrieval, especially action leakage, cross-bucket violation, click-back/hash/receipt coverage, and promotion gate behavior?
6. Are the governance claims valid, especially that vector/graph rank did not become evidence support, action basis, truth confidence, or reviewed relation?
7. Is it reasonable to commit the current documentation-only Phase B result?
8. Should we expand samples or add a stricter adversarial set before commit?
9. What exact evidence would be required before opening C-lite or runtime adoption?
```

## Local Claim To Verify

The package argues:

```text
Single Yuxi-like retrieval helps finding material, but leaks authority/action boundaries.
VAKS+B keeps most retrieval benefits while reducing action leakage to zero in the local tests.
This is a 1+1>2 result at the retrieval-governance layer, not proof of original Yuxi runtime adoption.
```

Key local metrics:

```text
main primary hit@5: 27/30 -> 30/30
main primary MRR:   0.7766 -> 1.0000
main full hit@5:    27/30 -> 30/30
main full MRR:      0.7272 -> 1.0000

holdout primary hit@5: 9/15 -> 12/15
holdout primary MRR:   0.4633 -> 0.7811
holdout full hit@5:    13/15 -> 13/15
holdout full MRR:      0.4944 -> 0.7591

Yuxi-native action leakage: 1.0000
VAKS+B action leakage:      0.0000

promotion gates blocked: 90 / 90
promotion/action/writeback/truth-change/reviewed-relation permissions: 0
```

## Important Boundary

This package should not be treated as:

```text
reviewed VAKS truth
runtime adoption approval
C-lite approval
original Yuxi full-stack validation
formal writeback approval
action basis
```

It is only an external review packet for checking the Phase B experiment logic.

