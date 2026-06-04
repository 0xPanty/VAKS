# README For Pro Review

This package contains the small hardening patch requested after the previous output-level oracle bakeoff review.

## Status

```text
sandbox-only
no main-vault writeback
no SCHEMA change
not 480 real-data proof
```

## What This Patch Changes

The prior bakeoff still kept cases, renderer, checker, and aggregator in one script. This patch splits them:

```text
cases_input.json      input observations for renderer
gold_oracle.json      independent expected states/gates/groups
renderer.py           renders front/back/full artifacts
checker.py            black-box checks rendered artifacts against gold
aggregator.py         computes paired metrics
run_independent_patch.py
```

## New Hardening Points

```text
authority paraphrase families, not exact phrases only
true versioning hard counterexample
paired metrics against baseline_full rendered artifacts
anchor_problem_visibility for missing / stale / drift / moved
required unresolved gate check
```

## Main Result

Candidate variant:

```text
candidate_with_version
```

Hard gates:

```text
state_mismatch: 0
false_lite: 0
review_due_fn: 0
anchor_failures: 0
anchor_problem_visibility_failures: 0
authority_leakage: 0
authority_boundary_failures: 0
queue_failures: 0
front_violations: 0
severe_over_grouping: 0
anchor_resolve_rate: 1.0
grouping_recall: 1.0
grouped_reduction_pct: 50.0
```

Paired metrics:

```text
paired_total_rendered_line_reduction_pct: 16.5
paired_ordinary_rendered_line_reduction_pct: 30.5
paired_serious_rendered_line_delta_pct: 0.0
paired_review_time_delta_pct: -22.7
baseline_total_lines: 370
candidate_total_lines: 309
```

Control checks:

```text
control_leaky fails:
  state_mismatch: 17
  false_lite: 17
  review_due_fn: 17
  authority_leakage: 12
  severe_over_grouping: 2

candidate_no_version fails:
  severe_over_grouping: 1
```

## Review Question

Does this small hardening patch sufficiently address the remaining fixture-level concerns so VAKS can proceed to the 480 real-data paired pilot?

If not, what is the one remaining blocker?
