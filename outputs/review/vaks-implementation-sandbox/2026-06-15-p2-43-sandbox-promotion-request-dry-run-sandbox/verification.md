---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-43-sandbox-promotion-request-dry-run-sandbox
---

# Verification

Default read-only verification command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-43-sandbox-promotion-request-dry-run-sandbox\artifact\verify_promotion_request.py
```

Expected local result:

- Primary `artifact/promotion-request-dry-run.json` validates.
- Positive fixtures pass.
- Failure cases match the oracle.
- Prototype/readout expose request items, preconditions, and non-claims without command, form, link, or formal-vault affordances.

Builder-only regeneration command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-43-sandbox-promotion-request-dry-run-sandbox\artifact\verify_promotion_request.py --rebuild
```

`--rebuild` deletes and regenerates slice-local generated directories. It is not a read-only reviewer command.

Final gate command after reviews:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-43-sandbox-promotion-request-dry-run-sandbox\artifact\verify_promotion_request.py --final-gate
```
