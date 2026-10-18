---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox
---

# Verification

Default read-only verification command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox\artifact\verify_freeze_bundle.py
```

Expected result:

- Positive fixtures pass.
- Failure cases match the oracle.
- Recomputed p2-44..p2-47 hashes match the freeze manifest.
- Missing file count is `0`.
- Report status mismatch count is `0`.
- Prototype and readout preserve sandbox-only boundaries.

Builder-only regeneration command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox\artifact\verify_freeze_bundle.py --rebuild
```

Final gate command after reviews:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox\artifact\verify_freeze_bundle.py --final-gate
```
