---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox
---

# Verification

Default read-only verification command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox\artifact\verify_portability_audit.py
```

Expected result:

- Positive fixtures pass.
- Failure cases match the oracle.
- Synthetic probes pass.
- Static verifier inventory has zero blocking import/token/syntax issues.
- Prototype and readout preserve sandbox-only boundaries.

Builder-only regeneration command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox\artifact\verify_portability_audit.py --rebuild
```

Final gate command after reviews:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox\artifact\verify_portability_audit.py --final-gate
```
