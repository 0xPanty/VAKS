# README For Pro Review

This package asks Pro to review the latest VAKS audit shell v1 output-level oracle hardening patch and alpha bakeoff.

## Current Status

```text
sandbox-only
no main-vault writeback
no SCHEMA change
not 480 real-data proof
```

## What Changed Since The 96-Case Patch

Pro's critique was that the prior adversarial patch split files physically, but still had semantic self-proof risk.

This sandbox changes the test target:

```text
old: compare shell fields against same-family gold fields
new: compare final rendered front/back/full artifacts against output-level oracle checks
```

The new oracle checks:

```text
state upgrade correctness
false-lite
review_due false negatives
authority leakage in rendered text
authority boundary visibility
actual anchor pointer resolution
missing/stale/drifted anchor visibility
front-face line count from rendered output
grouping recall and severe over-grouping
```

## Main Result

The strongest result is not one isolated alpha. It is a guarded stack:

```text
trigger-held deep packet retention
+ sparse provenance mention pointer
+ folded recurrence card
+ versioned fingerprint grouping
+ categorical feedback revision strip
```

The stack passes the output-level hard gates:

```text
state mismatch: 0
false-lite: 0
review_due false negative: 0
jump-back failures: 0
authority leakage: 0
authority boundary failures: 0
severe over-grouping: 0
visible front reduction: 56.3%
grouping recall: 1.0
grouped reduction: 50.0%
```

The old control-like variant fails the new black-box checks:

```text
state mismatch: 21
false-lite: 15
review_due false negative: 15
authority leakage: 13
authority boundary failures: 13
```

## Suggested Reading Order

```text
1. PRO_REVIEW_PROMPT.md
2. ALPHA_BAKEOFF_REPORT.md
3. FRAMEWORK_SANDBOX_PRESSURE_REPORT.md
4. oracle_results.json
5. rendered_artifacts.json
6. run_output_oracle_alpha_bakeoff.py
7. anchors.json
8. raw_sources/
```

## What This Does Not Prove

```text
It does not prove product readiness.
It does not replace the 480 real-data paired pilot.
It does not authorize main-vault operation convention writeback.
It does not change truth core, SCHEMA, REVIEW_QUEUE, SOURCE_INTAKE, or FEEDBACK.
```

## Non-Negotiable Boundaries

```text
grouping is triage, not support strength
lineage/provenance is traceability, not independence proof
dashboard/test/shell/feedback output is diagnostic metadata, not truth authority
anchor pointer only counts if it resolves
feedback wording must not create truth/confidence deltas
sandbox pass cannot trigger truth writeback
```
