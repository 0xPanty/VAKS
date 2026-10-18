---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-44-sandbox-evidence-ledger-sandbox
---

# Verification

Default read-only verification command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-44-sandbox-evidence-ledger-sandbox\artifact\verify_evidence_ledger.py
```

Expected local result:

- Primary `artifact/evidence-ledger.json` validates against current sandbox file evidence.
- Positive fixtures pass.
- Failure cases match the oracle.
- Prototype/readout show plan coverage, testing evidence, positive improvements, and non-production boundaries.

Builder-only regeneration command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-44-sandbox-evidence-ledger-sandbox\artifact\verify_evidence_ledger.py --rebuild
```

`--rebuild` deletes and regenerates slice-local generated directories. It is not a read-only reviewer command.

Final gate command after reviews:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-44-sandbox-evidence-ledger-sandbox\artifact\verify_evidence_ledger.py --final-gate
```
