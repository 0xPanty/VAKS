---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-46-sandbox-status-normalization-compatibility-audit-sandbox
---

# Verification

Default read-only verification command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-46-sandbox-status-normalization-compatibility-audit-sandbox\artifact\verify_status_normalization_audit.py
```

Expected result:

- Positive fixtures pass.
- Failure cases match the oracle.
- Unknown statuses count is `0`.
- All examined slices remain gate-pass by Product/Reviewer/Boundary/verification booleans.
- Prototype and readout preserve sandbox-only boundaries.

Builder-only regeneration command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-46-sandbox-status-normalization-compatibility-audit-sandbox\artifact\verify_status_normalization_audit.py --rebuild
```

Final gate command after reviews:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-46-sandbox-status-normalization-compatibility-audit-sandbox\artifact\verify_status_normalization_audit.py --final-gate
```
