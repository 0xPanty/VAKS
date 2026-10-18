---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-33-formal-vault-execution-request-screening-sandbox
---

# Verification

## Local Build Result

- Positive fixtures: `3`
- Fixture validation errors: `{"valid-denied-request-screening-config.json": [], "valid-missing-confirmation-request-screening-config.json": [], "valid-reviewable-request-screening-config.json": []}`
- Failure cases: `212`
- Failure mismatches: `[]`
- Manual negative probes: `12`
- Manual probe mismatches: `[]`
- Prototype issues: `[]`

## Commands Used

- `python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-33-formal-vault-execution-request-screening-sandbox/artifact/verify_request_screening.py --rebuild`

## Boundary Result

The local verification checks configuration, source hashes, generated failure
cases, manual negative probes, prototype Markdown, prototype HTML, and prototype
receipt. It does not inspect or change the formal vault.
