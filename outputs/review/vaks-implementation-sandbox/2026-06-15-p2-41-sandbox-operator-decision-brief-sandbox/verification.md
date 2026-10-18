---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-41-sandbox-operator-decision-brief-sandbox
---

# Verification

Local verification command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-41-sandbox-operator-decision-brief-sandbox\artifact\verify_decision_brief.py --rebuild
```

Expected local result:

- Primary `artifact/decision-brief.json` validates.
- Positive fixtures pass.
- Failure cases match the oracle.
- Prototype exposes decision options and non-claims without command, form, link, or formal-vault affordances.

Final gate command after reviews:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-41-sandbox-operator-decision-brief-sandbox\artifact\verify_decision_brief.py --final-gate
```
