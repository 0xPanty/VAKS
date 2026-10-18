---
record_kind: sandbox_verification
slice_id: 2026-06-15-p2-32-formal-vault-execution-request-packet-sandbox
status: local_verification_passed_pending_review
truth_boundary: sandbox_only
---

# Verification

## Commands

Maintainer-only regeneration, not read-only review:

```powershell
python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-32-formal-vault-execution-request-packet-sandbox/artifact/verify_request_packet.py --rebuild
```

Default read-only verification:

```powershell
python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-32-formal-vault-execution-request-packet-sandbox/artifact/verify_request_packet.py
```

Pre-acceptance final gate:

```powershell
python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p2-32-formal-vault-execution-request-packet-sandbox/artifact/verify_request_packet.py --final-gate
```

Before Reviewer / Boundary / Product closeout, final gate should fail only on
pending report statuses.

## What Is Verified

- Three positive fixtures.
- 189 failure cases.
- Twelve manual negative probes that are not generated from the failure oracle.
- Exact P2-31 source hashes and report statuses.
- P2-31 readiness gate hash, receipt hash, check count, source count, and
  non-permission flags.
- Synthetic packet identity, projection identity, and non-submission flags.
- No current approval, actual user wording, formal-vault path, command, or
  execution-now intent.
- Prototype Markdown, HTML, and receipt tamper are fail-closed.

## Observed Current Results

```text
rebuild: passed true
default verification: passed true
positive fixtures: 3
failure cases: 189
failure mismatches: []
manual negative probes: 12
manual probe mismatches: []
prototype issues: []
pre-acceptance final gate: expected required_report_issues only
```

## Non-Claims

Verification is diagnostic only. It is not Product Acceptance, formal vault
approval, execution permission, action basis, evidence support, reviewed
knowledge, sync approval, commit approval, push approval, or promotion approval.
