# Opus External Review Operator Runbook

## Purpose

Use this runbook to submit the p2-100 transfer package to external Opus review and preserve the result for a later sandbox-only intake slice.

## Pre-Submission Checks

- Confirm transfer ZIP path: `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox/artifact/opus-review-transfer-package.zip`
- Confirm transfer ZIP SHA256: `2fa20d453406757c0e53abc2c2ad9842264c35359d1e12b203ea5113273b2640`
- Confirm SHA256 file contains the same hash: `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox/artifact/opus-review-transfer-package-sha256.txt`
- Confirm the transfer manifest says `transfer_ready=true`.
- Confirm the transfer manifest says `actual_opus_result_present=false`, `opus_approval_claimed=false`, `mainline_ready=false`, and `goal_complete_now=false`.

## Submission

Send the ZIP file and SHA256 to the external Opus review surface. Use `opus-external-review-submission-message.md` as the message body.

## Required Opus Result Tokens

The raw Opus response must include exactly one of:

- `OPUS_PASS_SANDBOX_CLOSEOUT`
- `OPUS_REVISE_SANDBOX_CLOSEOUT`
- `OPUS_BLOCKED_NEEDS_USER`

## Post-Response Intake

After Opus responds, do not edit old slices or main architecture. Create a later sandbox-only intake slice and preserve the raw response using `opus-result-intake-template.md` as the capture shape.

## Boundary

This operator kit is not an Opus result, not Opus approval, not mainline readiness, not reviewed knowledge, not evidence support, not action basis, and not goal completion.
