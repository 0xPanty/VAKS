# Independent Oracle Hardening Patch Report

Status: sandbox-only. No main-vault writeback, no SCHEMA change, not 480 real-data proof.

## Verdict

Candidate variant `candidate_with_version` passes the independent-runner output oracle hard gates.

## Hard Gates

| gate | result |
| --- | ---: |
| state_mismatch | 0 |
| false_lite | 0 |
| review_due_fn | 0 |
| anchor_failures | 0 |
| anchor_problem_visibility_failures | 0 |
| authority_leakage | 0 |
| authority_boundary_failures | 0 |
| queue_failures | 0 |
| front_violations | 0 |
| severe_over_grouping | 0 |
| safety_pass | True |
| anchor_resolve_rate | 1.0 |
| grouping_recall | 1.0 |
| grouped_reduction_pct | 50.0 |

## Paired Metrics

| metric | value |
| --- | ---: |
| paired_total_rendered_line_reduction_pct | 16.5 |
| paired_ordinary_rendered_line_reduction_pct | 30.5 |
| paired_serious_rendered_line_delta_pct | 0.0 |
| paired_review_time_delta_pct | -22.7 |
| baseline_total_lines | 370 |
| candidate_total_lines | 309 |
| baseline_ordinary_lines | 200 |
| candidate_ordinary_lines | 139 |
| baseline_serious_lines | 170 |
| candidate_serious_lines | 170 |

## Interpretation

This patch addresses Pro's requested split: gold labels, renderer, checker, and aggregator are separate files/runners.
Authority leakage is checked through paraphrase regex families against rendered text.
Versioned fingerprint grouping is tested by hard cases where all non-version grouping fields are identical.
Headline reduction uses paired baseline-vs-candidate rendered lines rather than a synthetic total*12 baseline.
Anchor health is reported as anchor_problem_visibility for missing/stale/drift/moved pointers.

This still remains a fixture patch. If accepted, the next step is the 480 real-data paired pilot.
