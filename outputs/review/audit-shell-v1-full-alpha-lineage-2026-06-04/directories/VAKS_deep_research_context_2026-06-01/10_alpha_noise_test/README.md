# VAKS Alpha Noise-Reduction Sandbox

Status:

```text
sandbox only
main vault read-only
no SCHEMA change
no mainline conclusion
```

## Goal

Test whether the external-research alpha mechanisms reduce VAKS record noise without weakening lazy gates.

Alphas under test:

```text
compact_evidence_card
compact_coverage_card
support_refine_cluster
categorical_feedback_stub
```

Cross-cutting invariant:

```text
default light
condition thick
raw anchors jump-backable
```

## What This Test Can Prove

This test can show whether typed design cases preserve required anchors, avoid fake precision, reduce record length, and still escalate strict-gate cases.

## What This Test Cannot Prove

This is not a truth benchmark and not a source-reading benchmark.

It does not prove:

```text
the system can infer all case labels from messy raw text
source independence can be automatically determined
real-world runtime sampling is safe
the design should land in the main vault
```

## Run

```powershell
python run_tests.py
```

Expected outputs:

```text
results.json
ALPHA_NOISE_TEST_REPORT.md
MAIN_RULE_OVERLAP_AUDIT.md
```
