---
slice_id: 2026-06-19-p2-99-portable-opus-evidence-bundle-sandbox
status: local_verification_passed
---

# Verification

## Local Verifier

Command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-19-p2-99-portable-opus-evidence-bundle-sandbox\artifact\verify_portable_opus_evidence_bundle.py
```

Result:

```json
{
  "passed": true,
  "failures": [],
  "summary": {
    "fixture_count": 5,
    "failure_case_count": 8,
    "snapshot_count": 9,
    "hash_match_count": 9,
    "bundle_ready": true,
    "actual_opus_result_present": false,
    "opus_approval_claimed": false,
    "mainline_ready": false,
    "goal_complete_now": false,
    "final_gate": false
  }
}
```

## Interpretation

The portable bundle is locally reproducible: required evidence snapshots are present, source and copied snapshot hashes match, fixtures and failure cases are present, and the bundle does not claim an actual Opus result, user approval, mainline readiness, or goal completion.

## Final Gate

Command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-19-p2-99-portable-opus-evidence-bundle-sandbox\artifact\verify_portable_opus_evidence_bundle.py --final-gate
```

Result:

```json
{
  "passed": true,
  "failures": [],
  "summary": {
    "fixture_count": 5,
    "failure_case_count": 8,
    "snapshot_count": 9,
    "hash_match_count": 9,
    "bundle_ready": true,
    "actual_opus_result_present": false,
    "opus_approval_claimed": false,
    "mainline_ready": false,
    "goal_complete_now": false,
    "final_gate": true
  }
}
```
