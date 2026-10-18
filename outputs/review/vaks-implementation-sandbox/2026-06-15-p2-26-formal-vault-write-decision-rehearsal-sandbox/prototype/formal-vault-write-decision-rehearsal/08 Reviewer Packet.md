---
record_kind: sandbox_reviewer_packet
slice_id: 2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
---

# Reviewer Packet

## Inspect First

- `artifact/formal-vault-write-decision-rehearsal-contract.md`
- `fixtures/valid-decision-rehearsal-config.json`
- `fixtures/valid-denial-rehearsal-config.json`
- `fixtures/valid-revision-rehearsal-config.json`
- `artifact/failure-case-oracle.md`
- `prototype/formal-vault-write-decision-rehearsal/`
- `artifact/verify_decision_rehearsal.py`

## Review Questions

- Does synthetic approval stay non-actionable?
- Do deny and revise outcomes block write?
- Are packet, source bundle, scope, and rehearsal hashes verified?
- Does any scenario collect actual user approval?
- Does the inspector remain read-only and non-approval-collecting?
