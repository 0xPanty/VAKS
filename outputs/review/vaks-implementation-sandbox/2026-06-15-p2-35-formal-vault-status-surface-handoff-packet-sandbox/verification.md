---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-35-formal-vault-status-surface-handoff-packet-sandbox
---

# Verification

- Positive fixtures: `3`
- Fixture errors: `{"valid-next-agent-read-only-handoff-config.json": [], "valid-pause-or-park-handoff-config.json": [], "valid-product-workflow-prebrief-handoff-config.json": []}`
- Failure cases: `185`
- Failure mismatches: `[]`
- Manual negative probes: `12`
- Manual probe mismatches: `[]`
- Prototype issues: `[]`

Read-only verification command:

`python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-35-formal-vault-status-surface-handoff-packet-sandbox/artifact/verify_handoff_packet.py`

Builder-only rebuild command:

`python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-35-formal-vault-status-surface-handoff-packet-sandbox/artifact/verify_handoff_packet.py --rebuild`

Final-gate command after Reviewer, Boundary, Product Acceptance, and next-step closeout:

`python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-35-formal-vault-status-surface-handoff-packet-sandbox/artifact/verify_handoff_packet.py --final-gate`
