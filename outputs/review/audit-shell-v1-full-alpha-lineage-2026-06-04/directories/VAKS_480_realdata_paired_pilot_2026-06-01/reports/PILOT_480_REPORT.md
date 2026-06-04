# VAKS 480 Real-Data Paired Pilot Report

Status: sandbox-only pilot. No main-vault writeback, no SCHEMA change, no operation-convention promotion.

## Verdict

`shell_core`: safety_pass=True.
`shell_core_plus_recurrence`: safety_pass=True.
`shell_core_plus_unversioned_control`: safety_pass=False (negative control).

Interpretation: core shell is the minimum design under test; recurrence bundle is only evaluated as an optional add-on for recurrence-heavy slices.

## Dataset Mix

| family | cases | source status | fetched rows |
| --- | ---: | --- | ---: |
| scifact | 120 | real_with_qrels | 140 |
| averitec | 120 | real_dataset_server | 140 |
| ambifc | 120 | real_dataset_server | 140 |
| fever | 120 | real_dataset_server | 140 |

## shell_core

| hard gate | count |
| --- | ---: |
| state_mismatch | 0 |
| false_lite | 0 |
| review_due_fn | 0 |
| queue_fn | 0 |
| source_anchor_failures | 0 |
| anchor_problem_visibility_failures | 0 |
| record_pointer_failures | 0 |
| evidence_pointer_failures | 0 |
| authority_leakage | 0 |
| authority_boundary_failures | 0 |
| severe_over_grouping | 0 |
| serious_folded_count | 0 |
| safety_pass | True |
| front_budget_warnings | 0 |
| grouping_recall | 0.0 |
| severe_over_grouping | 0 |

| paired metric | all cases | ordinary slice | serious slice | recurrence slice |
| --- | ---: | ---: | ---: | ---: |
| rendered_line_reduction_pct | 32.4 | 48.8 | 3.9 | 31.3 |
| rendered_char_reduction_pct | 44.8 | 62.0 | 15.9 | 43.0 |
| front_char_reduction_pct | -3.4 | 3.1 | -14.6 | -29.0 |
| review_proxy_delta_pct | -43.0 | -62.3 | -10.1 | -43.1 |

| front realism metric | value |
| --- | ---: |
| front_chars_p50 | 256 |
| front_chars_p95 | 361 |
| max_front_line_chars_p95 | 153 |

## shell_core_plus_recurrence

| hard gate | count |
| --- | ---: |
| state_mismatch | 0 |
| false_lite | 0 |
| review_due_fn | 0 |
| queue_fn | 0 |
| source_anchor_failures | 0 |
| anchor_problem_visibility_failures | 0 |
| record_pointer_failures | 0 |
| evidence_pointer_failures | 0 |
| authority_leakage | 0 |
| authority_boundary_failures | 0 |
| severe_over_grouping | 0 |
| serious_folded_count | 0 |
| safety_pass | True |
| front_budget_warnings | 0 |
| grouping_recall | 1.0 |
| severe_over_grouping | 0 |

| paired metric | all cases | ordinary slice | serious slice | recurrence slice |
| --- | ---: | ---: | ---: | ---: |
| rendered_line_reduction_pct | 32.5 | 49.1 | 3.9 | 32.9 |
| rendered_char_reduction_pct | 44.9 | 62.1 | 15.9 | 43.7 |
| front_char_reduction_pct | -3.0 | 3.8 | -14.6 | -25.5 |
| review_proxy_delta_pct | -43.1 | -62.5 | -10.1 | -43.8 |

| front realism metric | value |
| --- | ---: |
| front_chars_p50 | 254 |
| front_chars_p95 | 370 |
| max_front_line_chars_p95 | 149 |

## shell_core_plus_unversioned_control

| hard gate | count |
| --- | ---: |
| state_mismatch | 0 |
| false_lite | 0 |
| review_due_fn | 0 |
| queue_fn | 0 |
| source_anchor_failures | 0 |
| anchor_problem_visibility_failures | 0 |
| record_pointer_failures | 0 |
| evidence_pointer_failures | 0 |
| authority_leakage | 0 |
| authority_boundary_failures | 0 |
| severe_over_grouping | 4 |
| serious_folded_count | 0 |
| safety_pass | False |
| front_budget_warnings | 0 |
| grouping_recall | 1.0 |
| severe_over_grouping | 4 |

| paired metric | all cases | ordinary slice | serious slice | recurrence slice |
| --- | ---: | ---: | ---: | ---: |
| rendered_line_reduction_pct | 32.7 | 49.3 | 3.9 | 34.1 |
| rendered_char_reduction_pct | 45.1 | 62.4 | 15.9 | 45.0 |
| front_char_reduction_pct | -2.2 | 5.0 | -14.6 | -18.7 |
| review_proxy_delta_pct | -43.2 | -62.6 | -10.1 | -44.8 |

| front realism metric | value |
| --- | ---: |
| front_chars_p50 | 251 |
| front_chars_p95 | 362 |
| max_front_line_chars_p95 | 149 |

## Alpha Readout

- Strongest core alpha: hard-trigger shell + required unresolved gate + anchor health strip + sparse provenance pointer. It is the minimum set that preserves serious escalation while reducing ordinary surface.
- Positive optional alpha: representative recurrence card + open-only versioned dedup. It should stay scoped to recurrence-heavy, ordinary, valid-anchor items; serious, regressed, challenge, action-basis, and anchor-problem members break out.
- Guardrail-only items: authority boundary lint and categorical feedback wording. They are useful constraints, not value engines and not truth authority.

## Limits

- This is a real-row paired shell pilot with deterministic pressure overlays; it does not adjudicate factual truth of dataset claims.
- Review-time numbers are proxy units, not observed human timings.
- Anchor resolution is local path/marker plus record/evidence file resolution, not a full UI selector click-through.
- Grouping still depends on supplied recurrence fields; messy extraction remains a future runtime risk.
