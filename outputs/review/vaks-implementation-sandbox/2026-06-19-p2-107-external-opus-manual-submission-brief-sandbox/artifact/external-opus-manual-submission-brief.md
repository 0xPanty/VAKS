# External Opus Manual Submission Brief

Use this as the operator-facing one-page brief for external Opus submission.

## Attach

- ZIP: `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox/artifact/opus-review-transfer-package.zip`
- ZIP SHA256: `2fa20d453406757c0e53abc2c2ad9842264c35359d1e12b203ea5113273b2640`
- Dispatch message: `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-106-external-opus-dispatch-packet-sandbox/artifact/external-opus-dispatch-message.md`

## Required Opus Result Token

- `OPUS_PASS_SANDBOX_CLOSEOUT`
- `OPUS_REVISE_SANDBOX_CLOSEOUT`
- `OPUS_BLOCKED_NEEDS_USER`

## Required Response Fields

- `raw_conclusion_token`
- `reviewed_evidence`
- `boundary_verdict`
- `blocking_issues`
- `recommended_next_action`

## After Opus Responds

Preserve the raw Opus response in a new sandbox-only intake slice. Validate it with p2-102 before any user approval or merge discussion.

## Boundary

This manual brief is not external submission, not an Opus response, not Opus approval, not user approval, not mainline readiness, not mainline merge, not promotion, not reviewed knowledge, not evidence support, not action basis, not commit, not push, not sync, and not goal completion.

