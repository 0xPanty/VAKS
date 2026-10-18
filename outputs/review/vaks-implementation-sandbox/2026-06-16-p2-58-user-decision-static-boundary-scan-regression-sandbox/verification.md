---
record_kind: sandbox_verification
slice_id: 2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox
status: local_verification_passed
---

# Verification

Local command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox\artifact\verify_static_boundary_scan_regression.py
```

Final gate command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox\artifact\verify_static_boundary_scan_regression.py --final-gate
```

Expected:

- 3 positive fixtures pass.
- 22 failure cases are rejected with expected issue ids.
- 2 live p2-57 positive sources scan clean.
- p2-57 final gate passes in final gate mode.

## Local Result

Command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox\artifact\verify_static_boundary_scan_regression.py
```

Result:

```json
{
  "passed": true,
  "failures": [],
  "summary": {
    "slice_id": "2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox",
    "fixture_count": 3,
    "failure_case_count": 22,
    "live_positive_source_count": 2,
    "source_p2_57_final_gate_passed": null,
    "final_gate": false
  }
}
```

## Final Local Rerun

After Reviewer also noted `open(..., 'r+')`, Builder added `r+` to write-mode
detection and added `F22-read-write-mode-open`.

Final local result:

```json
{
  "passed": true,
  "failures": [],
  "summary": {
    "slice_id": "2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox",
    "fixture_count": 3,
    "failure_case_count": 22,
    "live_positive_source_count": 2,
    "source_p2_57_final_gate_passed": null,
    "final_gate": false
  }
}
```

Builder-only readout rebuild:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox\artifact\build_static_boundary_scan_regression_readout.py
```

Result: passed, and regenerated `static_boundary_scan_regression_readout.md`
plus `static_boundary_scan_regression_prototype.html` inside this sandbox path.

## Reviewer-Driven Hardening Rerun

After Reviewer identified non-blocking blind spots, Builder upgraded the scanner
inside this slice:

- simple assigned argv lists now resolve, for example `cmd = ['git', 'push']`
- annotated assigned argv lists now resolve
- `Path(...).open('w')` is detected
- `write_bytes()` is detected
- missing live source paths return a structured `source_missing` issue instead
  of raising

Rerun result:

```json
{
  "passed": true,
  "failures": [],
  "summary": {
    "slice_id": "2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox",
    "fixture_count": 3,
    "failure_case_count": 21,
    "live_positive_source_count": 2,
    "source_p2_57_final_gate_passed": null,
    "final_gate": false
  }
}
```
