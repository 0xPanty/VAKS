# README For Pro Review

This package asks Pro to review the latest VAKS `audit shell v1` sandbox work.

Latest status: Codex has already run the 96-case adversarial patch that Pro requested after the earlier 112-case pilot. The current review target is therefore the adversarial patch first, with the 112-case pilot treated as historical context.

## Current Review Questions

Please check:

```text
1. Did the 96-case adversarial patch actually respond to Pro's concerns about self-confirming metrics?
2. Are oracle/gold labels separated from shell implementation strongly enough?
3. Do false-lite, review_due precision/recall, over-grouping, anchor/jump-back, state transitions, and authority leakage get tested for real within fixture scope?
4. Are any metrics still overclaimed or too favorable?
5. Does the result justify moving to a 480 real-data paired pilot, or is one more adversarial patch needed?
6. Are there new alpha mechanisms beyond the current shell/group/fold/reopen direction that could reduce noise without weakening evidence discipline?
7. What must remain out of the main vault and out of SCHEMA for now?
```

## Current Status

```text
main vault untouched by audit-shell work
SCHEMA untouched
sandbox/package only
96-case adversarial fixture patch completed
not product-grade proof
480 real-data paired pilot not yet run
```

## Latest Results To Review First

```text
96 adversarial cases
96/96 pass
hard_gate_pass: true
false_lite: 0
review_due_precision: 1.0
review_due_recall: 1.0
jumpback_failures: 0
severe_over_grouping: 0
authority_leakage_incidents: 0
feedback_truth_change_incidents: 0
visible_front_reduction_pct: 58.7
grouped_reduction_pct: 50.0
```

Important caveat:

```text
This is stronger than the 112-case pilot, but it is still fixture-based.
It does not replace the later 480-sample real-data paired pilot.
```

## Reading Order

Read in this order:

```text
1. NEXT_WINDOW_RECOVERY_FULL_GRAIN.md
2. audit_shell_v1_adversarial_96/PROGRESS_NOTE_FOR_PRO_REVIEW.md
3. audit_shell_v1_adversarial_96/ADVERSARIAL_PATCH_REPORT.md
4. audit_shell_v1_adversarial_96/ADVERSARIAL_PATCH_SPEC.md
5. audit_shell_v1_adversarial_96/adversarial_cases.psv
6. audit_shell_v1_adversarial_96/run_adversarial_patch.py
7. pro_review_feedback/PRO_REVIEW_FEEDBACK_AND_NEXT_ACTION.md
8. audit_shell_v1_pilot/AUDIT_SHELL_V1_PILOT_REPORT.md
9. audit_shell_v1_pilot/AUDIT_SHELL_V1_SPEC.md
10. alpha_noise_test/ALPHA_NOISE_TEST_REPORT.md
11. pro_summary/PRO_REPORT_SUMMARY_AND_NEXT_STEPS.md
12. external_research_intake/VAKS_AUDIT_NOISE_REDUCTION_REPORT_INTAKE.md
```

## Non-Negotiables

```text
Do not treat shell/grouping/dashboard/feedback/tests as truth authority.
Do not treat source count, lineage, or group count as independence.
Do not recommend SCHEMA changes as the next move.
Do not claim product readiness from fixture tests.
Do not hide open gaps, missing anchors, known omissions, or trigger reasons to improve reduction metrics.
```
