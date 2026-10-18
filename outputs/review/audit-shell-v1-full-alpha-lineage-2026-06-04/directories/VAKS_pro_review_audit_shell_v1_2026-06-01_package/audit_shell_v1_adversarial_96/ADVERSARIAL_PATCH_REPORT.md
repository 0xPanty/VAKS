# Audit Shell V1 Adversarial 96 Report

Status: sandbox-only adversarial fixture patch. This is still not the 480-sample real-data pilot.

## Executive Result

- cases: 96
- passed_cases: 96
- false_lite: 0
- ordinary_false_positive: 0
- review_due_precision: 1.0
- review_due_recall: 1.0
- valid_anchor_failures: 0
- missing_anchor_failures: 0
- authority_leakage_incidents: 0
- feedback_truth_change_incidents: 0
- front_face_violations: 0
- severe_over_grouping: 0
- grouped_reduction_pct: 50.0
- visible_front_reduction_pct: 58.7
- hard_gate_pass: True

## Case Mix

| category | cases |
| --- | ---: |
| anchor_jumpback | 16 |
| authority_leakage | 12 |
| false_lite | 16 |
| over_grouping | 24 |
| review_due | 16 |
| state_transition | 12 |

## Trigger-Family Recall

| trigger | recall |
| --- | ---: |
| action_basis | 1.0 |
| action_outcome | 1.0 |
| conflict | 1.0 |
| decision_outcome | 1.0 |
| explicit_challenge | 1.0 |
| explicit_correction | 1.0 |
| high_severity_wrong_answer | 1.0 |
| independence_needed_for_confidence | 1.0 |
| known_omission | 1.0 |
| missing_anchor | 1.0 |
| promotion | 1.0 |
| regression | 1.0 |
| reviewer_blocks | 1.0 |
| risk_sensitive | 1.0 |
| selector_drift | 1.0 |
| stale_pointer | 1.0 |

## Hidden Burden Counters

| metric | value |
| --- | ---: |
| manual_fields_total | 686 |
| manual_grouping_review_needed | 96 |
| manual_grouping_applied | 43 |
| front_back_expansions | 49 |
| authoring_time_units_total | 1211 |
| triage_time_units_total | 672 |

## Grouping Audit

- raw_groupable: 12
- grouped_items: 6
- grouped_reduction_pct: 50.0
- severe_over_grouping: 0

## Failed Cases

No failed cases.

## Interpretation

This patch is stronger than the 112-case pilot because gold labels are explicit in the case table, shell output is generated separately, and comparison logic is separate.
It still remains fixture-based, so passing it should lead to real-data paired pilot, not main-vault writeback.
