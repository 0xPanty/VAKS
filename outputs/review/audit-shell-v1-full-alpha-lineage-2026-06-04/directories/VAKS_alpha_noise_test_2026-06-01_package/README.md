# VAKS Alpha Noise Test Package

This package contains the sandbox-only alpha tests for VAKS audit-noise reduction.

Current latest artifact:

```text
audit_shell_v1_adversarial_96/
```

For full recovery context, read:

```text
NEXT_WINDOW_RECOVERY_FULL_GRAIN.md
```

## Test Chronology

```text
1. alpha_noise_test/
   Four separate alpha mechanisms:
   compact evidence card, compact coverage card, support/refine cluster,
   categorical feedback stub.

2. audit_shell_v1_pilot/
   112-case unified shell pilot.
   Useful, but later judged too self-confirming for product proof.

3. pro_review_feedback/
   Pro's pass-with-concerns review and required next test.

4. audit_shell_v1_adversarial_96/
   96 explicit adversarial cases, independent gold labels, jump-back resolver,
   review_due precision/recall, over-grouping traps, authority-leakage traps,
   and hidden burden counters.
```

## Latest Result

```text
96/96 pass
hard_gate_pass: true
false_lite: 0
review_due_precision: 1.0
review_due_recall: 1.0
jumpback_failures: 0
severe_over_grouping: 0
authority_leakage_incidents: 0
visible_front_reduction_pct: 58.7
grouped_reduction_pct: 50.0
```

## Boundary

```text
main vault not modified by audit-shell tests
SCHEMA not modified
fixture tests are not product proof
tests are diagnostic, not truth authority
next step is Pro review, then possible 480 real-data paired pilot
```
