# VAKS Alpha Noise-Reduction Test Report

Status: sandbox-only, typed-case A/B test, not a truth benchmark.

## Executive Result

- cases: 24
- passed: 24/24
- baseline lines: 354
- alpha lines: 257
- saved lines: 97 (27.4%)
- false-lite cases: 0
- ordinary false positives: 0
- ordinary-case saved lines: 75 (42.4%)

## Candidate Summary

| candidate | cases | passed | all-case saved | ordinary-case saved | true failures caught | ordinary false positives | false-lite | recommendation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| categorical_feedback_stub | 6 | 6 | 22 (24.4%) | 15 (33.3%) | 2/2 | 0 | 0 | worth_next_round |
| compact_coverage_card | 6 | 6 | 21 (25.0%) | 18 (42.9%) | 3/3 | 0 | 0 | strong_next_round |
| compact_evidence_card | 6 | 6 | 19 (21.1%) | 21 (46.7%) | 3/3 | 0 | 0 | strong_next_round |
| support_refine_cluster | 6 | 6 | 35 (38.9%) | 21 (46.7%) | 1/1 | 0 | 0 | strong_next_round |

## Case Detail

| case | candidate | scenario | mode | baseline | alpha | saved | escalated as expected? | ordinary overburdened? | preserved? | pass |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| EC-01 | compact_evidence_card | ordinary | compact_card | 15 | 8 | 7 | yes | no | yes | PASS |
| EC-02 | compact_evidence_card | ordinary | compact_card | 15 | 8 | 7 | yes | no | yes | PASS |
| EC-03 | compact_evidence_card | ordinary | compact_card | 15 | 8 | 7 | yes | no | yes | PASS |
| EC-04 | compact_evidence_card | true_failure | full_audit | 15 | 15 | 0 | yes | no | yes | PASS |
| EC-05 | compact_evidence_card | boundary | full_audit | 15 | 15 | 0 | yes | no | yes | PASS |
| EC-06 | compact_evidence_card | boundary | full_audit | 15 | 17 | -2 | yes | no | yes | PASS |
| CC-01 | compact_coverage_card | ordinary | compact_coverage | 14 | 8 | 6 | yes | no | yes | PASS |
| CC-02 | compact_coverage_card | ordinary | compact_coverage | 14 | 8 | 6 | yes | no | yes | PASS |
| CC-03 | compact_coverage_card | ordinary | compact_coverage | 14 | 8 | 6 | yes | no | yes | PASS |
| CC-04 | compact_coverage_card | true_failure | full_coverage | 14 | 13 | 1 | yes | no | yes | PASS |
| CC-05 | compact_coverage_card | boundary | full_coverage | 14 | 13 | 1 | yes | no | yes | PASS |
| CC-06 | compact_coverage_card | boundary | full_coverage | 14 | 13 | 1 | yes | no | yes | PASS |
| SRC-01 | support_refine_cluster | ordinary | support_refine_cluster | 15 | 8 | 7 | yes | no | yes | PASS |
| SRC-02 | support_refine_cluster | ordinary | support_refine_cluster | 15 | 8 | 7 | yes | no | yes | PASS |
| SRC-03 | support_refine_cluster | ordinary | support_refine_cluster | 15 | 8 | 7 | yes | no | yes | PASS |
| SRC-04 | support_refine_cluster | true_failure | blocking_review_cluster | 15 | 17 | -2 | yes | no | yes | PASS |
| SRC-05 | support_refine_cluster | boundary | linked_stub | 15 | 6 | 9 | yes | no | yes | PASS |
| SRC-06 | support_refine_cluster | boundary | support_refine_cluster | 15 | 8 | 7 | yes | no | yes | PASS |
| FB-01 | categorical_feedback_stub | ordinary | feedback_stub | 15 | 10 | 5 | yes | no | yes | PASS |
| FB-02 | categorical_feedback_stub | ordinary | feedback_stub | 15 | 10 | 5 | yes | no | yes | PASS |
| FB-03 | categorical_feedback_stub | ordinary | feedback_stub | 15 | 10 | 5 | yes | no | yes | PASS |
| FB-04 | categorical_feedback_stub | true_failure | review_due_feedback | 15 | 14 | 1 | yes | no | yes | PASS |
| FB-05 | categorical_feedback_stub | boundary | review_due_feedback | 15 | 14 | 1 | yes | no | yes | PASS |
| FB-06 | categorical_feedback_stub | boundary | feedback_stub | 15 | 10 | 5 | yes | no | yes | PASS |

## Interpretation

The alphas reduced record surface in typed cases without missing strict-gate escalation.
The strongest immediate candidates are compact coverage cards, categorical feedback stubs, and compact evidence cards.
Support/refine clustering is useful, but should be tested against messier real source material because over-grouping is the main risk.

## Limits

- This test uses typed signals plus prose cases. It does not test extraction from messy raw papers.
- It measures record burden and gate behavior, not factual correctness.
- It does not prove source independence. Lineage can prompt review, not replace review.
- It does not justify SCHEMA changes.

## Next Suggested Test

Run the same four alphas on 10 to 20 real/distilled claim-evidence cases from SciFact/AVeriTeC plus 3 to 5 full source anchors from the existing E2E trial.
