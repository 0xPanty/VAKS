# Failure Case Oracle

Each case must fail validation with the listed code. Failure cases focus on authority confusion, unsafe operations, missing product gates, and weak pilot usability.

| File | Expected failure |
| --- | --- |
| `01-forbidden-formal-vault-write.json` | `forbidden_operation:formal_vault_write` |
| `02-obsidian-sync-enabled.json` | `forbidden_operation:obsidian_sync` |
| `03-commit-enabled.json` | `forbidden_operation:commit` |
| `04-push-enabled.json` | `forbidden_operation:push` |
| `05-promotion-enabled.json` | `forbidden_operation:promotion` |
| `06-dependency-install-enabled.json` | `forbidden_operation:dependency_install` |
| `07-background-service-enabled.json` | `forbidden_operation:background_service` |
| `08-real-base-files-enabled.json` | `forbidden_operation:real_base_files` |
| `09-missing-sandbox-boundary.json` | `missing_boundary_phrase:sandbox only` |
| `10-missing-action-basis-boundary.json` | `missing_boundary_phrase:not action basis` |
| `11-authority-confusing-surface.json` | `authority_confusing_label` |
| `12-journey-too-deep.json` | `journey_too_deep:new_user_first_run` |
| `13-journey-missing-stop-condition.json` | `journey_missing_stop_condition:daily_triage` |
| `14-missing-receipt-surface.json` | `missing_surface:receipt_inspector` |
| `15-missing-decision-option.json` | `missing_decision_option:hybrid_pilot_path` |
| `16-decision-option-without-approval.json` | `decision_option_without_user_approval:obsidian_native_markdown_bases` |
| `17-missing-product-acceptance-gate.json` | `missing_acceptance_gate:reviewer_boundary_product_acceptance` |
| `18-outside-write-scope.json` | `invalid_write_scope` |
| `19-wrong-source-slice.json` | `wrong_source_slice` |
| `20-too-few-failure-cases.json` | `minimum_failure_cases_too_low` |
