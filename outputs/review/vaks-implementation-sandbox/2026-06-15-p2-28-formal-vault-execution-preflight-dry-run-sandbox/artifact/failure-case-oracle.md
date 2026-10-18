# Failure Case Oracle

| File | Expected failure |
| --- | --- |
| `01-forbidden-formal_vault_read.json` | `forbidden_operation:formal_vault_read` |
| `02-forbidden-formal_vault_scan.json` | `forbidden_operation:formal_vault_scan` |
| `03-forbidden-formal_vault_write.json` | `forbidden_operation:formal_vault_write` |
| `04-forbidden-formal_vault_hash.json` | `forbidden_operation:formal_vault_hash` |
| `05-forbidden-formal_vault_snapshot.json` | `forbidden_operation:formal_vault_snapshot` |
| `06-forbidden-formal_vault_state_check.json` | `forbidden_operation:formal_vault_state_check` |
| `07-forbidden-obsidian_sync.json` | `forbidden_operation:obsidian_sync` |
| `08-forbidden-commit.json` | `forbidden_operation:commit` |
| `09-forbidden-push.json` | `forbidden_operation:push` |
| `10-forbidden-promotion.json` | `forbidden_operation:promotion` |
| `11-forbidden-dependency_install.json` | `forbidden_operation:dependency_install` |
| `12-forbidden-background_service.json` | `forbidden_operation:background_service` |
| `13-forbidden-mcp_write_tool.json` | `forbidden_operation:mcp_write_tool` |
| `14-forbidden-hooks.json` | `forbidden_operation:hooks` |
| `15-forbidden-real_base_files.json` | `forbidden_operation:real_base_files` |
| `16-forbidden-production_ui.json` | `forbidden_operation:production_ui` |
| `17-forbidden-local_storage_write.json` | `forbidden_operation:local_storage_write` |
| `18-forbidden-network_post.json` | `forbidden_operation:network_post` |
| `19-forbidden-actual_approval_collection.json` | `forbidden_operation:actual_approval_collection` |
| `20-forbidden-actual_user_approval.json` | `forbidden_operation:actual_user_approval` |
| `21-forbidden-actual_user_decision_collection.json` | `forbidden_operation:actual_user_decision_collection` |
| `22-forbidden-user_approval_inference.json` | `forbidden_operation:user_approval_inference` |
| `23-forbidden-real_user_text_storage.json` | `forbidden_operation:real_user_text_storage` |
| `24-forbidden-real_user_text_capture.json` | `forbidden_operation:real_user_text_capture` |
| `25-forbidden-write_gate_opening.json` | `forbidden_operation:write_gate_opening` |
| `26-forbidden-execution_performed.json` | `forbidden_operation:execution_performed` |
| `27-forbidden-snapshot_taken.json` | `forbidden_operation:snapshot_taken` |
| `28-forbidden-rollback_executed.json` | `forbidden_operation:rollback_executed` |
| `29-forbidden-hash_before_collected.json` | `forbidden_operation:hash_before_collected` |
| `30-forbidden-hash_after_collected.json` | `forbidden_operation:hash_after_collected` |
| `31-forbidden-action_basis_creation.json` | `forbidden_operation:action_basis_creation` |
| `32-forbidden-reviewed_knowledge_creation.json` | `forbidden_operation:reviewed_knowledge_creation` |
| `33-forbidden-external_notification.json` | `forbidden_operation:external_notification` |
| `34-source-input-path-missing.json` | `source_input_path_missing:source_intake_config` |
| `35-source-input-hash-mismatch.json` | `source_input_hash_mismatch:source_intake_config` |
| `36-source-input-bundle-hash-mismatch.json` | `source_input_bundle_hash_mismatch` |
| `37-source-intake-gate-hash-mismatch.json` | `source_intake_gate_hash_mismatch` |
| `38-source-packet-hash-mismatch.json` | `source_packet_hash_mismatch` |
| `39-source-bundle-hash-mismatch.json` | `source_packet_source_bundle_hash_mismatch` |
| `40-source-scope-hash-mismatch.json` | `source_packet_scope_hash_mismatch` |
| `41-preflight-hash-missing.json` | `preflight_hash_missing, contract_preflight_hash_mismatch, sample_preflight_hash_mismatch:synthetic_approved_reference_preflight, sample_preflight_hash_mismatch:synthetic_denied_reference_preflight, sample_preflight_hash_mismatch:synthetic_dirty_state_preflight_block, sample_preflight_hash_mismatch:synthetic_revision_reference_preflight, sample_required_preflight_hash_mismatch:synthetic_approved_reference_preflight, sample_required_preflight_hash_mismatch:synthetic_denied_reference_preflight, sample_required_preflight_hash_mismatch:synthetic_dirty_state_preflight_block, sample_required_preflight_hash_mismatch:synthetic_revision_reference_preflight` |
| `42-preflight-hash-mismatch.json` | `preflight_hash_mismatch, non_execution_receipt_preflight_hash_mismatch, contract_preflight_hash_mismatch, sample_preflight_hash_mismatch:synthetic_approved_reference_preflight, sample_preflight_hash_mismatch:synthetic_denied_reference_preflight, sample_preflight_hash_mismatch:synthetic_dirty_state_preflight_block, sample_preflight_hash_mismatch:synthetic_revision_reference_preflight, sample_required_preflight_hash_mismatch:synthetic_approved_reference_preflight, sample_required_preflight_hash_mismatch:synthetic_denied_reference_preflight, sample_required_preflight_hash_mismatch:synthetic_dirty_state_preflight_block, sample_required_preflight_hash_mismatch:synthetic_revision_reference_preflight` |
| `43-target-absolute-path.json` | `target_path_not_relative:native_home, target_relative_target_mismatch:native_home` |
| `44-target-parent-traversal.json` | `target_path_not_relative:native_home, target_relative_target_mismatch:native_home` |
| `45-extra-target-requested.json` | `target_manifest_scope_mismatch, target_not_in_packet_scope:extra_target, too_many_targets` |
| `46-target-source-hash-missing.json` | `target_source_hash_missing:native_home, target_source_hash_mismatch:native_home` |
| `47-target-state-checked.json` | `target_formal_vault_state_checked:native_home` |
| `48-target-snapshot-taken.json` | `target_snapshot_taken:native_home` |
| `49-target-hash-before-collected.json` | `target_hash_before_collected:native_home` |
| `50-target-write-enabled.json` | `target_write_enabled_now:native_home` |
| `51-target-relative-drift.json` | `target_relative_target_mismatch:native_home` |
| `52-target-source-path-drift.json` | `target_source_path_mismatch:native_home` |
| `53-target-source-sha-drift.json` | `target_source_hash_mismatch:native_home` |
| `54-sample-not-synthetic.json` | `sample_not_synthetic:synthetic_approved_reference_preflight` |
| `55-sample-actual-user-input.json` | `sample_uses_actual_user_input:synthetic_approved_reference_preflight` |
| `56-sample-real-user-text-stored.json` | `sample_stores_real_user_text:synthetic_approved_reference_preflight` |
| `57-sample-captured-user-text.json` | `sample_captures_user_text:synthetic_approved_reference_preflight` |
| `58-sample-missing-decision-reference.json` | `sample_missing_decision_reference:synthetic_approved_reference_preflight` |
| `59-sample-intake-hash-mismatch.json` | `sample_intake_gate_hash_mismatch:synthetic_approved_reference_preflight` |
| `60-sample-packet-hash-mismatch.json` | `sample_packet_hash_mismatch:synthetic_approved_reference_preflight` |
| `61-sample-scope-hash-mismatch.json` | `sample_scope_hash_mismatch:synthetic_approved_reference_preflight` |
| `62-sample-check-false.json` | `sample_preflight_check_failed:synthetic_approved_reference_preflight:formal_vault_not_accessed` |
| `63-sample-execution-performed.json` | `sample_execution_performed:synthetic_approved_reference_preflight` |
| `64-sample-formal-vault-accessed.json` | `sample_accesses_formal_vault:synthetic_approved_reference_preflight` |
| `65-sample-state-inspected.json` | `sample_inspects_formal_vault_state:synthetic_approved_reference_preflight` |
| `66-sample-snapshot-taken.json` | `sample_snapshot_taken:synthetic_approved_reference_preflight` |
| `67-sample-hash-before-collected.json` | `sample_hash_before_collected:synthetic_approved_reference_preflight` |
| `68-sample-allows-write.json` | `sample_allows_formal_vault_write_now:synthetic_approved_reference_preflight` |
| `69-sample-creates-action-basis.json` | `sample_creates_action_basis:synthetic_approved_reference_preflight` |
| `70-approved-actionable-result.json` | `approved_sample_result_actionable:synthetic_approved_reference_preflight, approved_sample_result_bad:synthetic_approved_reference_preflight` |
| `71-deny-allows-execution.json` | `denied_sample_executes:synthetic_denied_reference_preflight` |
| `72-deny-wrong-result.json` | `denied_sample_result_bad:synthetic_denied_reference_preflight` |
| `73-revise-allows-execution.json` | `revise_sample_executes:synthetic_revision_reference_preflight` |
| `74-revise-wrong-result.json` | `revise_sample_result_bad:synthetic_revision_reference_preflight` |
| `75-dirty-state-does-not-block.json` | `dirty_sample_result_bad:synthetic_dirty_state_preflight_block` |
| `76-contract-allows-execution.json` | `contract_allows_execution` |
| `77-contract-allows-vault-access.json` | `contract_allows_formal_vault_access` |
| `78-contract-missing-separate-execution.json` | `contract_missing_separate_execution_slice` |
| `79-contract-missing-check.json` | `contract_missing_required_preflight_check:formal_vault_not_accessed` |
| `80-receipt-claims-execution.json` | `non_execution_receipt_claims_execution` |
| `81-receipt-formal-vault-accessed.json` | `non_execution_receipt_formal_vault_accessed` |
| `82-receipt-hash-collected.json` | `non_execution_receipt_hash_before_collected` |
| `83-authority-confusing-text.json` | `authority_confusing_text` |
| `84-too-few-failure-cases.json` | `minimum_failure_cases_too_low` |
| `85-inspector-execute-button.json` | `inspector_buttons_not_allowlisted, inspector_control_not_allowed:button:execute` |
| `86-missing-stop-condition-execution.json` | `missing_stop_condition:execution requested` |
