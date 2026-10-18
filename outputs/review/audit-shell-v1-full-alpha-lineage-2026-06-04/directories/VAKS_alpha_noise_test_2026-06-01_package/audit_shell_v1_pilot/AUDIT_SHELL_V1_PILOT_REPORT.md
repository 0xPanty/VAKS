# Audit Shell V1 Pilot Report

Status: sandbox-only fixture/risk-map pilot. Not a product gate and not real dataset ingestion.

## Executive Result

- cases: 112
- passed: 112
- baseline_visible_lines: 1742
- shell_visible_lines: 1232
- overall_reduction_pct: 29.3
- ordinary_reduction_pct: 63.1
- false_lite: 0
- ordinary_false_positive: 0
- serious_cases: 58
- serious_full_audit_recall: 1.0
- serious_anchor_retention: 1.0
- review_due_precision: 1.0
- front_face_violations: 0
- missing_anchor_visibility: 1.0
- grouped_reduction_pct: 56.5
- resolved_folding_reduction_pct: 100.0
- over_group_mismatches: 0
- pilot_gate_pass: True

## Dataset/Risk Mix

| source_family | cases | purpose |
| --- | ---: | --- |
| scifact_like | 24 | small claims, evidence card, abstract/rationale anchor pressure |
| averitec_like | 20 | coverage, sufficiency, action-basis style pressure |
| ambifc_like | 16 | ambiguity, support/refine vs conflict, over-grouping risk |
| fever_like | 20 | volume, ordinary false positive, resolved folding pressure |
| full_anchor_like | 8 | messy source anchor and jump-back pressure |
| derived_replay | 24 | repeated feedback, recurrence, resolved/regressed workflow |

## Gate Table

| gate | result | pass? |
| --- | ---: | --- |
| serious false-lite = 0 | 0 | PASS |
| serious anchor retention = 100% | 1.0 | PASS |
| ordinary record reduction >= 50% | 63.1 | PASS |
| ordinary false-positive <= 5% | 0 | PASS |
| over-grouping serious mismatch = 0 | 0 | PASS |
| grouped repeated-event reduction >= 50% | 56.5 | PASS |
| review_due precision >= 0.80 | 1.0 | PASS |
| front face <= 6 visible lines | 0 | PASS |

## Case Detail

| case | family | object | state | triggers | baseline | shell | false-lite | ordinary-fp | pass |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |
| SF-001 | scifact_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| SF-002 | scifact_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| SF-003 | scifact_like | small_claim | blocking | promotion | 15 | 16 | False | False | PASS |
| SF-004 | scifact_like | small_claim | blocking | missing_anchor | 15 | 16 | False | False | PASS |
| SF-005 | scifact_like | small_claim | for_review | known_omission | 15 | 16 | False | False | PASS |
| SF-006 | scifact_like | small_claim | blocking | explicit_challenge | 15 | 16 | False | False | PASS |
| SF-007 | scifact_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| SF-008 | scifact_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| SF-009 | scifact_like | small_claim | blocking | promotion | 15 | 16 | False | False | PASS |
| SF-010 | scifact_like | small_claim | blocking | missing_anchor | 15 | 16 | False | False | PASS |
| SF-011 | scifact_like | small_claim | for_review | known_omission | 15 | 16 | False | False | PASS |
| SF-012 | scifact_like | small_claim | blocking | explicit_challenge | 15 | 16 | False | False | PASS |
| SF-013 | scifact_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| SF-014 | scifact_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| SF-015 | scifact_like | small_claim | blocking | promotion | 15 | 16 | False | False | PASS |
| SF-016 | scifact_like | small_claim | blocking | missing_anchor | 15 | 16 | False | False | PASS |
| SF-017 | scifact_like | small_claim | for_review | known_omission | 15 | 16 | False | False | PASS |
| SF-018 | scifact_like | small_claim | blocking | explicit_challenge | 15 | 16 | False | False | PASS |
| SF-019 | scifact_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| SF-020 | scifact_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| SF-021 | scifact_like | small_claim | blocking | promotion | 15 | 16 | False | False | PASS |
| SF-022 | scifact_like | small_claim | blocking | missing_anchor | 15 | 16 | False | False | PASS |
| SF-023 | scifact_like | small_claim | for_review | known_omission | 15 | 16 | False | False | PASS |
| SF-024 | scifact_like | small_claim | blocking | explicit_challenge | 15 | 16 | False | False | PASS |
| AV-025 | averitec_like | answer_query_run | ordinary | - | 16 | 6 | False | False | PASS |
| AV-026 | averitec_like | answer_query_run | ordinary | - | 16 | 6 | False | False | PASS |
| AV-027 | averitec_like | answer_query_run | blocking | action_basis | 16 | 17 | False | False | PASS |
| AV-028 | averitec_like | answer_query_run | blocking | risk_sensitive | 16 | 17 | False | False | PASS |
| AV-029 | averitec_like | answer_query_run | for_review | known_omission | 16 | 17 | False | False | PASS |
| AV-030 | averitec_like | answer_query_run | ordinary | - | 16 | 6 | False | False | PASS |
| AV-031 | averitec_like | answer_query_run | ordinary | - | 16 | 6 | False | False | PASS |
| AV-032 | averitec_like | answer_query_run | blocking | action_basis | 16 | 17 | False | False | PASS |
| AV-033 | averitec_like | answer_query_run | blocking | risk_sensitive | 16 | 17 | False | False | PASS |
| AV-034 | averitec_like | answer_query_run | for_review | known_omission | 16 | 17 | False | False | PASS |
| AV-035 | averitec_like | answer_query_run | ordinary | - | 16 | 6 | False | False | PASS |
| AV-036 | averitec_like | answer_query_run | ordinary | - | 16 | 6 | False | False | PASS |
| AV-037 | averitec_like | answer_query_run | blocking | action_basis | 16 | 17 | False | False | PASS |
| AV-038 | averitec_like | answer_query_run | blocking | risk_sensitive | 16 | 17 | False | False | PASS |
| AV-039 | averitec_like | answer_query_run | for_review | known_omission | 16 | 17 | False | False | PASS |
| AV-040 | averitec_like | answer_query_run | ordinary | - | 16 | 6 | False | False | PASS |
| AV-041 | averitec_like | answer_query_run | ordinary | - | 16 | 6 | False | False | PASS |
| AV-042 | averitec_like | answer_query_run | blocking | action_basis | 16 | 17 | False | False | PASS |
| AV-043 | averitec_like | answer_query_run | blocking | risk_sensitive | 16 | 17 | False | False | PASS |
| AV-044 | averitec_like | answer_query_run | for_review | known_omission | 16 | 17 | False | False | PASS |
| AM-045 | ambifc_like | support_refine_collision | for_review | known_omission | 17 | 18 | False | False | PASS |
| AM-046 | ambifc_like | support_refine_collision | ordinary | - | 17 | 6 | False | False | PASS |
| AM-047 | ambifc_like | support_refine_collision | blocking | conflict | 17 | 18 | False | False | PASS |
| AM-048 | ambifc_like | support_refine_collision | blocking | independence_needed_for_confidence | 17 | 18 | False | False | PASS |
| AM-049 | ambifc_like | support_refine_collision | for_review | known_omission | 17 | 18 | False | False | PASS |
| AM-050 | ambifc_like | support_refine_collision | ordinary | - | 17 | 6 | False | False | PASS |
| AM-051 | ambifc_like | support_refine_collision | blocking | conflict | 17 | 18 | False | False | PASS |
| AM-052 | ambifc_like | support_refine_collision | blocking | independence_needed_for_confidence | 17 | 18 | False | False | PASS |
| AM-053 | ambifc_like | support_refine_collision | for_review | known_omission | 17 | 18 | False | False | PASS |
| AM-054 | ambifc_like | support_refine_collision | ordinary | - | 17 | 6 | False | False | PASS |
| AM-055 | ambifc_like | support_refine_collision | blocking | conflict | 17 | 18 | False | False | PASS |
| AM-056 | ambifc_like | support_refine_collision | blocking | independence_needed_for_confidence | 17 | 18 | False | False | PASS |
| AM-057 | ambifc_like | support_refine_collision | for_review | known_omission | 17 | 18 | False | False | PASS |
| AM-058 | ambifc_like | support_refine_collision | ordinary | - | 17 | 6 | False | False | PASS |
| AM-059 | ambifc_like | support_refine_collision | blocking | conflict | 17 | 18 | False | False | PASS |
| AM-060 | ambifc_like | support_refine_collision | blocking | independence_needed_for_confidence | 17 | 18 | False | False | PASS |
| FV-061 | fever_like | answer_query_run | ordinary | - | 16 | 6 | False | False | PASS |
| FV-062 | fever_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| FV-063 | fever_like | answer_query_run | for_review | known_omission | 16 | 17 | False | False | PASS |
| FV-064 | fever_like | small_claim | blocking | explicit_challenge | 15 | 16 | False | False | PASS |
| FV-065 | fever_like | answer_query_run | resolved_folded | - | 16 | 1 | False | False | PASS |
| FV-066 | fever_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| FV-067 | fever_like | answer_query_run | ordinary | - | 16 | 6 | False | False | PASS |
| FV-068 | fever_like | small_claim | for_review | known_omission | 15 | 16 | False | False | PASS |
| FV-069 | fever_like | answer_query_run | blocking | explicit_challenge | 16 | 17 | False | False | PASS |
| FV-070 | fever_like | small_claim | resolved_folded | - | 15 | 1 | False | False | PASS |
| FV-071 | fever_like | answer_query_run | ordinary | - | 16 | 6 | False | False | PASS |
| FV-072 | fever_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| FV-073 | fever_like | answer_query_run | for_review | known_omission | 16 | 17 | False | False | PASS |
| FV-074 | fever_like | small_claim | blocking | explicit_challenge | 15 | 16 | False | False | PASS |
| FV-075 | fever_like | answer_query_run | resolved_folded | - | 16 | 1 | False | False | PASS |
| FV-076 | fever_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| FV-077 | fever_like | answer_query_run | ordinary | - | 16 | 6 | False | False | PASS |
| FV-078 | fever_like | small_claim | for_review | known_omission | 15 | 16 | False | False | PASS |
| FV-079 | fever_like | answer_query_run | blocking | explicit_challenge | 16 | 17 | False | False | PASS |
| FV-080 | fever_like | small_claim | resolved_folded | - | 15 | 1 | False | False | PASS |
| FA-081 | full_anchor_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| FA-082 | full_anchor_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| FA-083 | full_anchor_like | small_claim | for_review | known_omission | 15 | 16 | False | False | PASS |
| FA-084 | full_anchor_like | small_claim | blocking | missing_anchor | 15 | 16 | False | False | PASS |
| FA-085 | full_anchor_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| FA-086 | full_anchor_like | small_claim | ordinary | - | 15 | 6 | False | False | PASS |
| FA-087 | full_anchor_like | small_claim | for_review | known_omission | 15 | 16 | False | False | PASS |
| FA-088 | full_anchor_like | small_claim | blocking | missing_anchor | 15 | 16 | False | False | PASS |
| DR-089 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-090 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-091 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-092 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-093 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-094 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-095 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-096 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-097 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-098 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-099 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-100 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-101 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-102 | derived_replay | feedback | ordinary | - | 15 | 5 | False | False | PASS |
| DR-103 | derived_replay | feedback | resolved_folded | - | 15 | 1 | False | False | PASS |
| DR-104 | derived_replay | feedback | resolved_folded | - | 15 | 1 | False | False | PASS |
| DR-105 | derived_replay | feedback | resolved_folded | - | 15 | 1 | False | False | PASS |
| DR-106 | derived_replay | feedback | resolved_folded | - | 15 | 1 | False | False | PASS |
| DR-107 | derived_replay | feedback | regressed | regression | 15 | 15 | False | False | PASS |
| DR-108 | derived_replay | feedback | regressed | regression | 15 | 15 | False | False | PASS |
| DR-109 | derived_replay | feedback | blocking | explicit_correction | 15 | 15 | False | False | PASS |
| DR-110 | derived_replay | feedback | blocking | explicit_correction | 15 | 15 | False | False | PASS |
| DR-111 | derived_replay | feedback | for_review | action_outcome | 15 | 15 | False | False | PASS |
| DR-112 | derived_replay | feedback | for_review | action_outcome | 15 | 15 | False | False | PASS |

## Interpretation

This pilot shows that audit shell v1 can exceed the previous single-record alpha reduction by adding queue/history compression.
The useful improvement is not merely shorter cards; it is resolved folding plus grouped repeated workflow items while preserving hard thickening triggers.

## Limits

- Cases are fixture/risk-map cases with typed labels, not live SciFact/AVeriTeC/AmbiFC/FEVER ingestion.
- This does not prove extraction from messy real sources.
- This does not prove reviewer agreement.
- This does not prove source independence.
- This does not justify SCHEMA changes.

## Next Step

Replace fixture families with real sampled records from SciFact/AVeriTeC/AmbiFC/FEVER plus full source anchors, then rerun the same gates.
