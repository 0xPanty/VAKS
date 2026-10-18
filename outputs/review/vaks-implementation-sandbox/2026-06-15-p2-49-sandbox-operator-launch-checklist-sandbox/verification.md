---
record_kind: sandbox_report
slice_id: 2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox
report: verification
status: local_verification_passed_pending_review
---

# Verification

Default read-only verifier passed:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox\artifact\verify_operator_launch_checklist.py
```

Builder-only rebuild verifier passed:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox\artifact\verify_operator_launch_checklist.py --rebuild
```

Read-only upstream freeze check passed:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-49-sandbox-operator-launch-checklist-sandbox\artifact\verify_operator_launch_checklist.py --run-upstream-freeze
```

Observed result: 5 source slices, 8 ordered launch steps, 3 positive fixtures, 81 failure cases, 0 orphan failure cases, 0 oracle mismatches, prototype/readout/contract/oracle checks clean, and p2-48 upstream freeze final gate passed.

`--final-gate` now automatically runs the p2-48 upstream freeze final gate. Before Reviewer/Boundary/Product reports were written, it failed only on pending report statuses, which is the expected pre-review state.

Important diagnostic note: p2-47 remains Product PASS as a historical sandbox slice, but its dynamic verifier is now drift-sensitive after later verifier files were added. This p2-49 checklist therefore treats p2-47 as diagnostic reference, not as a current launch green gate.

Run `--final-gate` again only after Reviewer, Boundary, and Product reports are written.
