# Opus Result Intake Template

## Source Transfer Package

- transfer_slice_id: `2026-06-19-p2-100-opus-review-transfer-package-sandbox`
- transfer_zip_path: `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox/artifact/opus-review-transfer-package.zip`
- transfer_zip_sha256: `2fa20d453406757c0e53abc2c2ad9842264c35359d1e12b203ea5113273b2640`
- operator_kit_slice_id: `2026-06-19-p2-101-opus-external-review-operator-kit-sandbox`

## Raw Opus Response

Paste or link the raw Opus response in the later intake slice. Do not summarize it as approval before validation.

```text
<RAW_OPUS_RESPONSE_GOES_HERE>
```

## Required Parsed Fields

- raw_conclusion_token: one of `OPUS_PASS_SANDBOX_CLOSEOUT`, `OPUS_REVISE_SANDBOX_CLOSEOUT`, `OPUS_BLOCKED_NEEDS_USER`
- reviewed_evidence:
- boundary_verdict:
- raw_response_path:
- blocking_issues:
- recommended_next_action:

## Boundary Requirements

- mainline_approval: false
- reviewed_knowledge: false
- evidence_support: false
- action_basis: false
- commit_push_sync: false
