# Package Manifest

## Entry

- `README_FOR_PRO.md`
- `PRO_REVIEW_PROMPT.md`
- `PACKAGE_MANIFEST.md`
- `NEXT_REVIEW_READING_ORDER.md`

## Reports

- `reports/PILOT_800_REPORT.md`
- `reports/AUTOMATED_COMPLETION_AUDIT.md`
- `reports/PATCH_800_AUTOMATED_FIX_REPORT.md`
- `reports/AUDIT_SHELL_V1_SANDBOX_CLOSEOUT.md`
- `reports/CHINESE_REVIEWER_CARD_PATCH_SPEC.md`
- `reports/AUDIT_SHELL_V1_REVIEWER_CARD_CANDIDATE_CONVENTION.md`
- `reports/EXTERNAL_ARCHITECTURE_REVIEW_SYNTHESIS.md`
- `reports/EXTERNAL_SOURCE_PRIORITY_AND_FINAL_JUDGMENT.md`
- `reports/RISK_TIERED_REVIEWER_UX_PATCH_SPEC.md`
- `reports/AUDIT_SHELL_V1_STATE_AND_SLOT_CONVENTION.md`
- `reports/OPERATOR_RENDERER_SLOT_PATCH_REPORT.md`
- `reports/CHINESE_REVIEWER_CARD_USABILITY_PREFLIGHT_PROTOCOL.md`
- `reports/NEGATIVE_CONTROL_AND_VALIDATION_TIMELINE.md`
- `reports/QUALITY_GATES_AND_THRESHOLDS.md`
- `reports/CHINESE_FORBIDDEN_WORDING_LINT.md`
- `reports/CODEX_OPERATOR_PREFLIGHT_DRY_RUN_REPORT.md`
- `reports/PRO_REVIEW_PASS_WITH_CONCERNS_AND_NEXT_ROUTE.md`
- `reports/OPERATOR_ADJUDICATION_ROUND1_REVIEW_RESULT.md`
- `reports/CLICKBACK_SEMANTIC_LANDING_EVAL.md`

## Data And Gold

- `data/dataset_fetch_log.json`
- `data/fetched_rows.json`
- `data/case_build_manifest.json`
- `data/clickback_snapshot_manifest.json`
- `data/clickback_semantic_landing_eval.json`
- `candidate_cases.json`
- `gold_oracle_frozen.json`
- `gold_oracle_frozen.sha256`
- `gold_freeze_manifest.json`

## Artifacts And Checks

- `artifacts_baseline_full.json`
- `artifacts_shell_core.json`
- `artifacts_shell_core_plus_recurrence.json`
- `artifacts_leaky_or_unversioned_control.json`
- `artifacts_authority_leaky_renderer.json`
- `artifacts_fake_precision_feedback_renderer.json`
- `checks_baseline_full.json`
- `checks_shell_core.json`
- `checks_shell_core_plus_recurrence.json`
- `checks_leaky_or_unversioned_control.json`
- `checks_authority_leaky_renderer.json`
- `checks_fake_precision_feedback_renderer.json`
- `pilot_800_results.json`
- `quality_gates_v1.json`
- `quality_gate_eval_800.json`
- `forbidden_wording_zh.json`
- `authority_fuzz_results.json`

## Scripts

- `fetch_data_800.py`
- `build_candidate_cases_800.py`
- `materialize_clickback_snapshots_800.py`
- `freeze_gold_oracle_800.py`
- `renderer_800.py`
- `checker_800.py`
- `aggregator_800.py`
- `run_authority_fuzz_800.py`
- `make_human_review_packet.py`
- `make_risk_tiered_reviewer_preflight_24.py`
- `make_adversarial_operator_cases_12.py`
- `make_operator_adjudication_packet.py`
- `lint_forbidden_wording_zh.py`
- `evaluate_quality_gates_800.py`
- `evaluate_clickback_semantic_landing.py`
- `materialize_clickback_snapshots_live_retry.py`
- `materialize_clickback_snapshots_powershell_retry.py`
- `refresh_after_clickback_retry.py`
- `run_codex_operator_preflight_dry_run.py`
- `run_codex_local_real_operator_self_test.py`
- `run_800_pilot.py`
- `authority_rules_800.json`

## Human Review Packet

- `review_packet/README_HUMAN_REVIEW.md`
- `review_packet/packet_summary.json`
- `review_packet/main_core_assignments.csv`
- `review_packet/main_core_timing_sheet_blank.csv`
- `review_packet/main_core_dual_review_adjudication_blank.csv`
- `review_packet/side_recurrence_assignments.csv`
- `review_packet/side_recurrence_timing_sheet_blank.csv`
- `review_packet/side_recurrence_dual_review_adjudication_blank.csv`
- compatibility copies:
  - `review_packet/review_assignments.csv`
  - `review_packet/timing_sheet_blank.csv`
  - `review_packet/dual_review_adjudication_blank.csv`

## Risk-Tiered Reviewer UX Preflight

- `review_packet_risk_tiered_24/README_RISK_TIERED_24.md`
- `review_packet_risk_tiered_24/RISK_TIERED_REVIEWER_CARDS_ZH.md`
- `review_packet_risk_tiered_24/RISK_TIERED_REVIEWER_SHEET_BLANK.csv`
- `review_packet_risk_tiered_24/hidden_gold_after_done.csv`
- `review_packet_risk_tiered_24/sample_coverage.json`
- `review_packet_risk_tiered_24/render_integrity_lint.json`
- `review_packet_risk_tiered_24/forbidden_wording_lint_zh.json`
- `review_packet_risk_tiered_24/CODEX_OPERATOR_PREFLIGHT_DRY_RUN.csv`
- `review_packet_risk_tiered_24/CODEX_OPERATOR_PREFLIGHT_DRY_RUN_SUMMARY.json`

## Codex Local Real Operator Self-Test

- `reports/CODEX_LOCAL_REAL_OPERATOR_SELF_TEST_REPORT.md`
- `review_packet_local_real_self_test/LOCAL_REAL_OPERATOR_SELF_TEST.csv`
- `review_packet_local_real_self_test/LOCAL_REAL_OPERATOR_SELF_TEST_SUMMARY.json`

## Adversarial Operator Add-On

- `review_packet_adversarial_12/README_ADVERSARIAL_12.md`
- `review_packet_adversarial_12/ADVERSARIAL_OPERATOR_CARDS_ZH.md`
- `review_packet_adversarial_12/ADVERSARIAL_REVIEW_SHEET_BLANK.csv`
- `review_packet_adversarial_12/hidden_gold_after_done.csv`
- `review_packet_adversarial_12/adversarial_coverage.json`
- `review_packet_adversarial_12/render_integrity_lint.json`
- `review_packet_adversarial_12/CODEX_ADVERSARIAL_OPERATOR_DRY_RUN.csv`
- `review_packet_adversarial_12/CODEX_ADVERSARIAL_OPERATOR_DRY_RUN_SUMMARY.json`
- `review_packet_adversarial_12/mock_sources/`
- `review_packet_adversarial_12/mock_records/`
- `review_packet_adversarial_12/mock_evidence/`

## Narrow Operator Adjudication Packet

- `review_packet_operator_adjudication_narrow/README_OPERATOR_ADJUDICATION_NARROW.md`
- `review_packet_operator_adjudication_narrow/CORE_24_DOUBLE_REVIEW_SHEET_BLANK.csv`
- `review_packet_operator_adjudication_narrow/ADVERSARIAL_12_DOUBLE_REVIEW_SHEET_BLANK.csv`
- `review_packet_operator_adjudication_narrow/ADJUDICATION_RESOLUTION_SHEET_BLANK.csv`
- `review_packet_operator_adjudication_narrow/GATE_SUMMARY_BLANK.json`
- `review_packet_operator_adjudication_narrow/packet_manifest.json`

## Local Stores

- `raw_sources/`
- `full_anchor_sources/`
- `real_source_snapshots/`
- `records/`
- `evidence/`
