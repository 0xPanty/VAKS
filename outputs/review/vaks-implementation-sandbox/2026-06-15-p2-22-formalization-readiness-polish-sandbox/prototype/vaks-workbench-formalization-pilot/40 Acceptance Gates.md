---
record_kind: sandbox_acceptance_gates
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Acceptance Gates

- `first_run_under_5_minutes`: A new operator reaches the boundary FAQ and first run checklist in three links or fewer.
- `status_answered_in_2_clicks`: Status, blocker, receipt, and next safe step are visible from Pilot Home.
- `receipt_path_visible`: P2-21 verification, boundary, reviewer, and product reports are linked from the pilot pack.
- `authority_confusion_blocked`: No page says sandbox pass equals reviewed knowledge, evidence support, action basis, merge, sync, commit, or push.
- `write_scope_clean`: All generated files stay under this slice path.
- `reviewer_boundary_product_acceptance`: Reviewer, Boundary Auditor, and GPT-5.5 xhigh Product Acceptance reports exist before next slice.

## Required Gate Order

1. Validator passes positive fixtures and failure cases.
2. Reviewer returns `REVIEW_PASS`.
3. Boundary Auditor returns `BOUNDARY_PASS`.
4. GPT-5.5 reasoning=xhigh Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Non-Claim

Validator pass is not reviewer approval. Reviewer pass and Boundary pass are not
Product Acceptance. Product Acceptance on this slice is not mainline approval.
