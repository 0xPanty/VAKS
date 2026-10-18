---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-40-sandbox-product-grade-rollup-dashboard-sandbox
---

# Verification

Local verification command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-40-sandbox-product-grade-rollup-dashboard-sandbox\artifact\verify_rollup_dashboard.py --rebuild
```

Expected local result:

- Positive fixtures pass.
- Failure cases match the oracle.
- Source slice PASS and verification-file counts match current file evidence.
- Prototype has no form, download, contenteditable, anchor, or formal-vault path affordance.

Final gate command after reviews:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-40-sandbox-product-grade-rollup-dashboard-sandbox\artifact\verify_rollup_dashboard.py --final-gate
```
