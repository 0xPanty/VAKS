---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-34-formal-vault-operator-status-surface-sandbox
---

# Verification

## Local Build Result

- Positive fixtures: `3`
- Fixture validation errors: `{"valid-boundary-stop-focus-status-surface-config.json": [], "valid-chain-overview-status-surface-config.json": [], "valid-latest-screening-focus-status-surface-config.json": []}`
- Failure cases: `267`
- Failure mismatches: `[]`
- Manual negative probes: `12`
- Manual probe mismatches: `[]`
- Prototype issues: `[]`

## Commands Used

- `python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-34-formal-vault-operator-status-surface-sandbox/artifact/verify_status_surface.py --rebuild`

## Boundary Result

The local verification checks source hashes, upstream statuses, generated
failure cases, manual negative probes, prototype Markdown, prototype HTML, and
prototype receipt. It does not inspect or change the formal vault.
