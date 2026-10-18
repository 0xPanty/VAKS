---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-36-formal-vault-read-only-product-workflow-prototype-sandbox
---

# Verification

- Positive fixtures: `3`
- Failure cases: `136`
- Manual negative probes: `12`
- Prototype issues: `[]`

Read-only verification command:

`python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-36-formal-vault-read-only-product-workflow-prototype-sandbox/artifact/verify_workflow_prototype.py`

Builder-only rebuild command:

`python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-36-formal-vault-read-only-product-workflow-prototype-sandbox/artifact/verify_workflow_prototype.py --rebuild`

Final-gate command after Reviewer, Boundary, Product Acceptance, and next-step closeout:

`python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-36-formal-vault-read-only-product-workflow-prototype-sandbox/artifact/verify_workflow_prototype.py --final-gate`
