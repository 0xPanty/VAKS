---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-37-formal-vault-operator-workflow-usability-screening-sandbox
---

# Verification

- Positive fixtures: `3`
- Failure cases: `133`
- Manual negative probes: `12`
- Prototype issues: `[]`

Read-only verification command:

`python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-37-formal-vault-operator-workflow-usability-screening-sandbox/artifact/verify_usability_screening.py`

Builder-only rebuild command:

`python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-37-formal-vault-operator-workflow-usability-screening-sandbox/artifact/verify_usability_screening.py --rebuild`

Final-gate command after Reviewer, Boundary, Product Acceptance, and next-step closeout:

`python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-37-formal-vault-operator-workflow-usability-screening-sandbox/artifact/verify_usability_screening.py --final-gate`
