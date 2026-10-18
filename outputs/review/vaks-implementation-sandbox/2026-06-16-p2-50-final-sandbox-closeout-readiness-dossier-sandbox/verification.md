---
record_kind: sandbox_report
slice_id: 2026-06-16-p2-50-final-sandbox-closeout-readiness-dossier-sandbox
report: verification
status: local_verification_passed_pending_review
---

# Verification

Default verifier passed:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-50-final-sandbox-closeout-readiness-dossier-sandbox\artifact\verify_closeout_readiness_dossier.py
```

Builder-only rebuild verifier passed:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-50-final-sandbox-closeout-readiness-dossier-sandbox\artifact\verify_closeout_readiness_dossier.py --rebuild
```

Read-only upstream verifier passed and ran the p2-49 final gate:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-16-p2-50-final-sandbox-closeout-readiness-dossier-sandbox\artifact\verify_closeout_readiness_dossier.py --run-upstream
```

Observed result: 6 source slices, 5 request categories, 3 positive fixtures, 100 failure cases, 0 orphan failure cases, 0 oracle mismatches, prototype/readout/contract/oracle checks clean, and p2-49 final gate passed. p2-49 in turn ran p2-48 upstream freeze final gate.

Pre-report final gate also ran p2-49 final gate and failed only because Reviewer, Boundary, Product, and next-step reports were still pending. That is the expected pre-review state.

Diagnostic p2-47 check:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox\artifact\verify_portability_audit.py
```

Observed summary: `passed=false`; first failures were `scanner_scope_mismatch`, `verifier_inventory_mismatch`, `summary_mismatch`, and `risk_inventory_mismatch`; `blocking_verifier_count=0`. Therefore p2-47 is correctly treated as drift-sensitive diagnostic context, not as a current launch green gate.

Run `--final-gate` again only after Reviewer, Boundary, and Product reports are written.
