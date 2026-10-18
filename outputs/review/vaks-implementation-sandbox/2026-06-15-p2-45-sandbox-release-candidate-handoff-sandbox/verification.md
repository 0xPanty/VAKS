---
status: local_verification_passed_pending_review
slice_id: 2026-06-15-p2-45-sandbox-release-candidate-handoff-sandbox
---

# Verification

Default read-only verification command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-45-sandbox-release-candidate-handoff-sandbox\artifact\verify_release_candidate_handoff.py
```

Expected local result:

- Primary `artifact/release-candidate-handoff.json` validates against p2-44 evidence.
- Positive fixtures pass.
- Failure cases match the oracle.
- Prototype/readout show plain answers, stop conditions, and non-production boundaries.

Builder-only regeneration command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-45-sandbox-release-candidate-handoff-sandbox\artifact\verify_release_candidate_handoff.py --rebuild
```

`--rebuild` deletes and regenerates slice-local generated directories. It is not a read-only reviewer command.

Final gate command after reviews:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-45-sandbox-release-candidate-handoff-sandbox\artifact\verify_release_candidate_handoff.py --final-gate
```
