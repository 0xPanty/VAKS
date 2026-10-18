# Failure Case Oracle

| File | Expected failure |
| --- | --- |
| `01-forbidden-formal_vault_read.json` | `forbidden_operation:formal_vault_read` |
| `02-forbidden-formal_vault_scan.json` | `forbidden_operation:formal_vault_scan` |
| `03-forbidden-formal_vault_write.json` | `forbidden_operation:formal_vault_write` |
| `04-forbidden-formal_vault_hash.json` | `forbidden_operation:formal_vault_hash` |
| `05-forbidden-formal_vault_snapshot.json` | `forbidden_operation:formal_vault_snapshot` |
| `06-forbidden-obsidian_sync.json` | `forbidden_operation:obsidian_sync` |
| `07-forbidden-commit.json` | `forbidden_operation:commit` |
| `08-forbidden-push.json` | `forbidden_operation:push` |
| `09-forbidden-promotion.json` | `forbidden_operation:promotion` |
| `10-forbidden-dependency_install.json` | `forbidden_operation:dependency_install` |
| `11-forbidden-background_service.json` | `forbidden_operation:background_service` |
| `12-forbidden-mcp_write_tool.json` | `forbidden_operation:mcp_write_tool` |
| `13-forbidden-hooks.json` | `forbidden_operation:hooks` |
| `14-forbidden-real_base_files.json` | `forbidden_operation:real_base_files` |
| `15-forbidden-production_ui.json` | `forbidden_operation:production_ui` |
| `16-forbidden-local_storage_write.json` | `forbidden_operation:local_storage_write` |
| `17-forbidden-network_post.json` | `forbidden_operation:network_post` |
| `18-forbidden-actual_approval_collection.json` | `forbidden_operation:actual_approval_collection` |
| `19-forbidden-actual_user_approval.json` | `forbidden_operation:actual_user_approval` |
| `20-forbidden-user_approval_inference.json` | `forbidden_operation:user_approval_inference` |
| `21-forbidden-action_basis_creation.json` | `forbidden_operation:action_basis_creation` |
| `22-forbidden-reviewed_knowledge_creation.json` | `forbidden_operation:reviewed_knowledge_creation` |
| `23-forbidden-external_notification.json` | `forbidden_operation:external_notification` |
| `24-source-input-path-missing.json` | `source_input_path_missing:source_config` |
| `25-source-input-hash-mismatch.json` | `source_input_hash_mismatch:source_config` |
| `26-source-input-bundle-hash-mismatch.json` | `source_input_bundle_hash_mismatch` |
| `27-source-packet-hash-mismatch.json` | `source_packet_hash_mismatch` |
| `28-source-packet-source-bundle-hash-mismatch.json` | `source_packet_source_bundle_hash_mismatch` |
| `29-source-packet-scope-hash-mismatch.json` | `source_packet_scope_hash_mismatch` |
| `30-rehearsal-hash-missing.json` | `rehearsal_hash_missing` |
| `31-rehearsal-hash-mismatch.json` | `rehearsal_hash_mismatch, non_approval_receipt_rehearsal_hash_mismatch` |
| `32-missing-approve-scenario.json` | `missing_decision_scenario:synthetic_approve_exact_packet, too_few_decision_scenarios` |
| `33-scenario-not-synthetic.json` | `scenario_not_synthetic:synthetic_approve_exact_packet` |
| `34-scenario-actual-user-input.json` | `scenario_uses_actual_user_input:synthetic_approve_exact_packet` |
| `35-scenario-user-text-present.json` | `scenario_has_actual_user_text:synthetic_approve_exact_packet` |
| `36-approve-missing-packet-hash.json` | `scenario_packet_hash_mismatch:synthetic_approve_exact_packet` |
| `37-approve-wrong-source-bundle-hash.json` | `scenario_source_bundle_hash_mismatch:synthetic_approve_exact_packet` |
| `38-approve-wrong-scope-hash.json` | `scenario_scope_hash_mismatch:synthetic_approve_exact_packet` |
| `39-approve-missing-question.json` | `approved_missing_required_question:synthetic_approve_exact_packet:future_approve_exact_scope` |
| `40-approve-allows-write-now.json` | `scenario_allows_formal_vault_write_now:synthetic_approve_exact_packet` |
| `41-approve-creates-action-basis.json` | `scenario_creates_action_basis:synthetic_approve_exact_packet` |
| `42-approve-actionable-result.json` | `approved_scenario_result_actionable:synthetic_approve_exact_packet, approved_scenario_result_bad:synthetic_approve_exact_packet` |
| `43-deny-allows-write.json` | `denied_scenario_allows_write:synthetic_deny_write` |
| `44-deny-wrong-result.json` | `denied_scenario_result_bad:synthetic_deny_write` |
| `45-revise-allows-write.json` | `revise_scenario_allows_write:synthetic_needs_revision` |
| `46-revise-wrong-result.json` | `revise_scenario_result_bad:synthetic_needs_revision` |
| `47-extra-files-requested.json` | `scenario_extra_files_requested:synthetic_approve_exact_packet` |
| `48-sync-allowed.json` | `scenario_allows_sync:synthetic_approve_exact_packet` |
| `49-commit-allowed.json` | `scenario_allows_commit:synthetic_approve_exact_packet` |
| `50-push-allowed.json` | `scenario_allows_push:synthetic_approve_exact_packet` |
| `51-promotion-allowed.json` | `scenario_allows_promotion:synthetic_approve_exact_packet` |
| `52-approved-missing-rollback-ack.json` | `approved_missing_rollback_ack:synthetic_approve_exact_packet` |
| `53-approved-missing-hash-ack.json` | `approved_missing_hash_ack:synthetic_approve_exact_packet` |
| `54-rule-allows-actual-user-input.json` | `rule_allows_actual_user_input` |
| `55-rule-approve-actionable.json` | `rule_allows_approved_outcome_actionable` |
| `56-rule-missing-packet-hash.json` | `rule_packet_hash_mismatch` |
| `57-receipt-claims-approval.json` | `non_approval_receipt_claims_approval` |
| `58-receipt-formal-vault-accessed.json` | `non_approval_receipt_formal_vault_accessed` |
| `59-authority-confusing-text.json` | `authority_confusing_text` |
| `60-too-few-failure-cases.json` | `minimum_failure_cases_too_low` |
| `61-inspector-approve-button.json` | `inspector_control_not_allowed:button:approve` |
