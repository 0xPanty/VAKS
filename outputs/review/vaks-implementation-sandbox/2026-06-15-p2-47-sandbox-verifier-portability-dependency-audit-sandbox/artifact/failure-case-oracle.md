# Failure Case Oracle

Slice: `2026-06-15-p2-47-sandbox-verifier-portability-dependency-audit-sandbox`

Total cases: 43

- `001-top-level-record_kind.json` -> `record_kind_mismatch`
- `002-top-level-slice_id.json` -> `slice_id_mismatch`
- `003-top-level-version.json` -> `version_mismatch`
- `004-top-level-truth_boundary.json` -> `truth_boundary_mismatch`
- `005-top-level-purpose.json` -> `purpose_mismatch`
- `006-top-level-write_scope.json` -> `write_scope_mismatch`
- `007-bad-view.json` -> `view_not_allowed:wrong`
- `008-extra-runtime-certification-claim.json` -> `unknown_top_level_field:runtime_certification_claim`
- `009-source-snapshot-drift.json` -> `source_snapshot_mismatch`
- `010-policy-drift.json` -> `portability_policy_mismatch`
- `011-scanner-scope-drift.json` -> `scanner_scope_mismatch`
- `012-summary-blocking-count.json` -> `summary_mismatch, blocking_verifier_present`
- `013-summary-external-import-count.json` -> `summary_mismatch, external_import_verifier_present`
- `014-summary-forbidden-token-count.json` -> `summary_mismatch, forbidden_token_verifier_present`
- `015-summary-syntax-error-count.json` -> `summary_mismatch, syntax_error_verifier_present`
- `016-synthetic-probe-failure.json` -> `synthetic_probes_mismatch, synthetic_probe_not_pass:stdlib_and_local_ok`
- `017-inventory-external-import.json` -> `verifier_inventory_mismatch, verifier_external_import:outputs/review/vaks-implementation-sandbox/2026-06-15-p0-07-action-boundary-failure-matrix-sandbox/artifact/verify_failure_matrix_sandbox.py`
- `018-inventory-blocking-issue.json` -> `verifier_inventory_mismatch, verifier_blocking_issue:outputs/review/vaks-implementation-sandbox/2026-06-15-p0-07-action-boundary-failure-matrix-sandbox/artifact/verify_failure_matrix_sandbox.py`
- `019-inventory-forbidden-token.json` -> `verifier_inventory_mismatch, verifier_forbidden_token:outputs/review/vaks-implementation-sandbox/2026-06-15-p0-07-action-boundary-failure-matrix-sandbox/artifact/verify_failure_matrix_sandbox.py`
- `020-inventory-warning-token-drift.json` -> `verifier_inventory_mismatch`
- `021-inventory-syntax-not-ok.json` -> `verifier_inventory_mismatch, verifier_syntax_not_ok:outputs/review/vaks-implementation-sandbox/2026-06-15-p0-07-action-boundary-failure-matrix-sandbox/artifact/verify_failure_matrix_sandbox.py`
- `022-agent-guide-rule-missing.json` -> `agent_run_guide_mismatch, agent_run_rule_missing:blocking import/token/syntax issues`
- `023-readiness-runtime-certified.json` -> `readiness_flag_not_false:runtime_certified`
- `024-readiness-mainline-ready.json` -> `readiness_flag_not_false:mainline_ready`
- `025-operation-old-verifier-executed.json` -> `operation_performed_not_false:old_verifier_executed`
- `026-operation-dependency-install.json` -> `operation_performed_not_false:dependency_install`
- `027-missing-non-claim-not-runtime-certification.json` -> `required_non_claims_mismatch`
- `028-missing-non-claim-not-dependency-installation.json` -> `required_non_claims_mismatch`
- `029-missing-non-claim-not-old-verifier-execution.json` -> `required_non_claims_mismatch`
- `030-missing-non-claim-not-old-slice-edit.json` -> `required_non_claims_mismatch`
- `031-missing-non-claim-not-release-approval.json` -> `required_non_claims_mismatch`
- `032-missing-non-claim-not-promotion-approval.json` -> `required_non_claims_mismatch`
- `033-missing-non-claim-not-mainline-ready.json` -> `required_non_claims_mismatch`
- `034-missing-non-claim-not-enterprise-production-ready.json` -> `required_non_claims_mismatch`
- `035-missing-non-claim-not-formal-vault-approval.json` -> `required_non_claims_mismatch`
- `036-missing-non-claim-not-Obsidian-sync.json` -> `required_non_claims_mismatch`
- `037-missing-non-claim-not-commit.json` -> `required_non_claims_mismatch`
- `038-missing-non-claim-not-push.json` -> `required_non_claims_mismatch`
- `039-missing-non-claim-not-reviewed-knowledge.json` -> `required_non_claims_mismatch`
- `040-missing-non-claim-not-evidence-support.json` -> `required_non_claims_mismatch`
- `041-missing-non-claim-not-action-basis.json` -> `required_non_claims_mismatch`
- `042-missing-non-claim-not-auto-advance.json` -> `required_non_claims_mismatch`
- `043-extra-non-claim.json` -> `required_non_claims_mismatch`
