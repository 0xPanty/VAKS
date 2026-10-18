# VAKS 800 Pressure-Overlay Pilot Report

Status: sandbox-only. No main-vault writeback, no SCHEMA change, no human timing fabricated.

Gold status: frozen machine oracle from explicit overlays. Human adjudication packet is generated separately; this is not independent human gold.

## Dataset Mix

| pool/family | cases | source rows | status |
| --- | ---: | ---: | --- |
| scifact | 160 | 220 | real_with_qrels |
| averitec | 160 | 220 | real_dataset_server |
| ambifc | 160 | 220 | real_dataset_server |
| fever | 160 | 220 | real_dataset_server |
| full_anchor_real_pack | 80 |  |  |
| adversarial_holdout | 80 |  |  |

## shell_core

safety_pass: `True`

| hard gate | count |
| --- | ---: |
| state_mismatch | 0 |
| serious_false_lite | 0 |
| review_due_fn | 0 |
| serious_review_due_fn | 0 |
| queue_fn | 0 |
| source_anchor_failures | 0 |
| anchor_problem_visibility_failures | 0 |
| record_pointer_failures | 0 |
| evidence_pointer_failures | 0 |
| authority_leakage | 0 |
| authority_boundary_failures | 0 |
| ordinary_false_positive | 0 |
| front_line_violations | 0 |
| severe_over_grouping | 0 |
| serious_folded_count | 0 |

| metric | all | ordinary | serious | recurrence | resolved |
| --- | ---: | ---: | ---: | ---: | ---: |
| rendered_line_reduction_pct | 41.6 | 56.2 | 25.0 | 52.8 | 56.2 |
| rendered_char_reduction_pct | 41.6 | 63.4 | 17.6 | 55.7 | 60.5 |
| front_char_reduction_pct | -7.6 | 3.8 | -20.1 | -13.7 | -11.3 |
| review_proxy_delta_pct | -42.8 | -66.7 | -16.5 | -59.0 | -64.6 |

| front density | value |
| --- | ---: |
| ordinary_front_chars_p95 | 302 |
| serious_front_chars_p95 | 358 |
| front_chars_p95 | 341 |
| max_front_line_chars_p95 | 127 |

| resolved view metric | value |
| --- | ---: |
| resolved_count | 32 |
| resolved_default_queue_visible | 0 |
| resolved_front_line_violations | 0 |

Threshold audit:

{
  "all_continue_gates_pass": true,
  "gates": {
    "serious_false_lite_zero": true,
    "serious_full_audit_recall_100": true,
    "serious_folded_zero": true,
    "valid_anchor_resolve_ge_99": true,
    "record_evidence_pointer_ge_99_5": true,
    "review_due_serious_fn_zero": true,
    "ordinary_false_positive_le_2_pct": true,
    "front_line_violations_zero": true,
    "ordinary_line_reduction_ge_55": true,
    "ordinary_char_reduction_ge_60": true,
    "recurrence_grouped_reduction_ge_50": true,
    "resolved_default_surface_folded": true,
    "front_chars_p95_budget": true
  }
}

## shell_core_plus_recurrence

safety_pass: `True`

| hard gate | count |
| --- | ---: |
| state_mismatch | 0 |
| serious_false_lite | 0 |
| review_due_fn | 0 |
| serious_review_due_fn | 0 |
| queue_fn | 0 |
| source_anchor_failures | 0 |
| anchor_problem_visibility_failures | 0 |
| record_pointer_failures | 0 |
| evidence_pointer_failures | 0 |
| authority_leakage | 0 |
| authority_boundary_failures | 0 |
| ordinary_false_positive | 0 |
| front_line_violations | 0 |
| severe_over_grouping | 0 |
| serious_folded_count | 0 |

| metric | all | ordinary | serious | recurrence | resolved |
| --- | ---: | ---: | ---: | ---: | ---: |
| rendered_line_reduction_pct | 41.1 | 55.3 | 25.0 | 49.1 | 56.2 |
| rendered_char_reduction_pct | 41.2 | 62.8 | 17.6 | 53.4 | 60.5 |
| front_char_reduction_pct | -7.9 | 3.1 | -20.1 | -16.1 | -11.3 |
| review_proxy_delta_pct | -42.5 | -66.1 | -16.5 | -56.7 | -64.6 |

| front density | value |
| --- | ---: |
| ordinary_front_chars_p95 | 298 |
| serious_front_chars_p95 | 358 |
| front_chars_p95 | 341 |
| max_front_line_chars_p95 | 127 |

| resolved view metric | value |
| --- | ---: |
| resolved_count | 32 |
| resolved_default_queue_visible | 0 |
| resolved_front_line_violations | 0 |

Threshold audit:

{
  "all_continue_gates_pass": true,
  "gates": {
    "serious_false_lite_zero": true,
    "serious_full_audit_recall_100": true,
    "serious_folded_zero": true,
    "valid_anchor_resolve_ge_99": true,
    "record_evidence_pointer_ge_99_5": true,
    "review_due_serious_fn_zero": true,
    "ordinary_false_positive_le_2_pct": true,
    "front_line_violations_zero": true,
    "ordinary_line_reduction_ge_55": true,
    "ordinary_char_reduction_ge_60": true,
    "recurrence_grouped_reduction_ge_50": true,
    "resolved_default_surface_folded": true,
    "front_chars_p95_budget": true
  }
}

## leaky_or_unversioned_control

safety_pass: `False`

| hard gate | count |
| --- | ---: |
| state_mismatch | 376 |
| serious_false_lite | 376 |
| review_due_fn | 376 |
| serious_review_due_fn | 376 |
| queue_fn | 300 |
| source_anchor_failures | 0 |
| anchor_problem_visibility_failures | 6 |
| record_pointer_failures | 0 |
| evidence_pointer_failures | 0 |
| authority_leakage | 48 |
| authority_boundary_failures | 48 |
| ordinary_false_positive | 0 |
| front_line_violations | 0 |
| severe_over_grouping | 12 |
| serious_folded_count | 12 |

| metric | all | ordinary | serious | recurrence | resolved |
| --- | ---: | ---: | ---: | ---: | ---: |
| rendered_line_reduction_pct | 55.4 | 54.8 | 56.1 | 50.0 | 50.0 |
| rendered_char_reduction_pct | 63.8 | 63.2 | 64.4 | 61.1 | 59.2 |
| front_char_reduction_pct | 5.0 | 4.0 | 6.1 | -9.4 | -12.2 |
| review_proxy_delta_pct | -66.8 | -66.3 | -67.3 | -64.1 | -62.8 |

| front density | value |
| --- | ---: |
| ordinary_front_chars_p95 | 277 |
| serious_front_chars_p95 | 309 |
| front_chars_p95 | 287 |
| max_front_line_chars_p95 | 109 |

| resolved view metric | value |
| --- | ---: |
| resolved_count | 32 |
| resolved_default_queue_visible | 0 |
| resolved_front_line_violations | 0 |

Threshold audit:

{
  "negative_control_failed": true,
  "expected": "must fail"
}

## authority_leaky_renderer

safety_pass: `False`

| hard gate | count |
| --- | ---: |
| state_mismatch | 0 |
| serious_false_lite | 0 |
| review_due_fn | 0 |
| serious_review_due_fn | 0 |
| queue_fn | 0 |
| source_anchor_failures | 0 |
| anchor_problem_visibility_failures | 0 |
| record_pointer_failures | 0 |
| evidence_pointer_failures | 0 |
| authority_leakage | 692 |
| authority_boundary_failures | 48 |
| ordinary_false_positive | 0 |
| front_line_violations | 0 |
| severe_over_grouping | 0 |
| serious_folded_count | 0 |

| metric | all | ordinary | serious | recurrence | resolved |
| --- | ---: | ---: | ---: | ---: | ---: |
| rendered_line_reduction_pct | 41.6 | 56.2 | 25.0 | 52.8 | 56.2 |
| rendered_char_reduction_pct | 39.7 | 61.1 | 16.2 | 53.4 | 57.9 |
| front_char_reduction_pct | -23.9 | -16.6 | -31.9 | -34.1 | -33.0 |
| review_proxy_delta_pct | -41.4 | -64.8 | -15.5 | -57.2 | -62.6 |

| front density | value |
| --- | ---: |
| ordinary_front_chars_p95 | 355 |
| serious_front_chars_p95 | 387 |
| front_chars_p95 | 370 |
| max_front_line_chars_p95 | 156 |

| resolved view metric | value |
| --- | ---: |
| resolved_count | 32 |
| resolved_default_queue_visible | 0 |
| resolved_front_line_violations | 0 |

Threshold audit:

{
  "negative_control_failed": true,
  "expected": "must fail"
}

## fake_precision_feedback_renderer

safety_pass: `False`

| hard gate | count |
| --- | ---: |
| state_mismatch | 0 |
| serious_false_lite | 0 |
| review_due_fn | 0 |
| serious_review_due_fn | 0 |
| queue_fn | 0 |
| source_anchor_failures | 0 |
| anchor_problem_visibility_failures | 0 |
| record_pointer_failures | 0 |
| evidence_pointer_failures | 0 |
| authority_leakage | 692 |
| authority_boundary_failures | 48 |
| ordinary_false_positive | 0 |
| front_line_violations | 0 |
| severe_over_grouping | 0 |
| serious_folded_count | 0 |

| metric | all | ordinary | serious | recurrence | resolved |
| --- | ---: | ---: | ---: | ---: | ---: |
| rendered_line_reduction_pct | 41.6 | 56.2 | 25.0 | 52.8 | 56.2 |
| rendered_char_reduction_pct | 39.1 | 60.5 | 15.7 | 52.8 | 57.3 |
| front_char_reduction_pct | -28.8 | -21.6 | -36.8 | -39.0 | -38.0 |
| review_proxy_delta_pct | -40.9 | -64.4 | -15.0 | -56.8 | -62.1 |

| front density | value |
| --- | ---: |
| ordinary_front_chars_p95 | 367 |
| serious_front_chars_p95 | 399 |
| front_chars_p95 | 382 |
| max_front_line_chars_p95 | 168 |

| resolved view metric | value |
| --- | ---: |
| resolved_count | 32 |
| resolved_default_queue_visible | 0 |
| resolved_front_line_violations | 0 |

Threshold audit:

{
  "negative_control_failed": true,
  "expected": "must fail"
}

## Human Timing Status

Human review timing is not fabricated. See `review_packet/` for randomized assignment and blank timing sheets.

## Interpretation

- `shell_core` is the only default-core candidate.
- `shell_core_plus_recurrence` is a conditional arm and must be judged on recurrence-heavy slices, not mixed averages.
- Negative controls must fail: `leaky_or_unversioned_control`, `authority_leaky_renderer`, and `fake_precision_feedback_renderer`. If any negative control is not caught, the harness is not valid.
- This run proves the automated scaffold and frozen-gold workflow. It still requires human adjudication/timing before operation-convention promotion.
