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
| `20-forbidden-actual_user_decision_collection.json` | `forbidden_operation:actual_user_decision_collection` |
| `21-forbidden-user_approval_inference.json` | `forbidden_operation:user_approval_inference` |
| `22-forbidden-action_basis_creation.json` | `forbidden_operation:action_basis_creation` |
| `23-forbidden-reviewed_knowledge_creation.json` | `forbidden_operation:reviewed_knowledge_creation` |
| `24-forbidden-external_notification.json` | `forbidden_operation:external_notification` |
| `25-forbidden-real_user_text_storage.json` | `forbidden_operation:real_user_text_storage` |
| `26-forbidden-real_user_text_capture.json` | `forbidden_operation:real_user_text_capture` |
| `27-forbidden-write_gate_opening.json` | `forbidden_operation:write_gate_opening` |
| `28-source-input-path-missing.json` | `source_input_path_missing:source_rehearsal_config` |
| `29-source-input-hash-mismatch.json` | `source_input_hash_mismatch:source_rehearsal_config` |
| `30-source-input-bundle-hash-mismatch.json` | `source_input_bundle_hash_mismatch` |
| `31-source-rehearsal-hash-mismatch.json` | `source_rehearsal_hash_mismatch` |
| `32-source-packet-hash-mismatch.json` | `source_packet_hash_mismatch` |
| `33-source-packet-source-bundle-hash-mismatch.json` | `source_packet_source_bundle_hash_mismatch` |
| `34-source-packet-scope-hash-mismatch.json` | `source_packet_scope_hash_mismatch` |
| `35-intake-gate-hash-missing.json` | `intake_gate_hash_missing, contract_intake_gate_hash_mismatch, sample_intake_gate_hash_mismatch:future_approve_reference_capture, sample_intake_gate_hash_mismatch:future_deny_reference_capture, sample_intake_gate_hash_mismatch:future_revision_reference_capture, sample_required_intake_gate_hash_mismatch:future_approve_reference_capture, sample_required_intake_gate_hash_mismatch:future_deny_reference_capture, sample_required_intake_gate_hash_mismatch:future_revision_reference_capture` |
| `36-intake-gate-hash-mismatch.json` | `intake_gate_hash_mismatch, non_approval_receipt_intake_gate_hash_mismatch, contract_intake_gate_hash_mismatch, sample_intake_gate_hash_mismatch:future_approve_reference_capture, sample_intake_gate_hash_mismatch:future_deny_reference_capture, sample_intake_gate_hash_mismatch:future_revision_reference_capture, sample_required_intake_gate_hash_mismatch:future_approve_reference_capture, sample_required_intake_gate_hash_mismatch:future_deny_reference_capture, sample_required_intake_gate_hash_mismatch:future_revision_reference_capture` |
| `37-missing-approve-sample.json` | `missing_intake_sample:future_approve_reference_capture, too_few_intake_samples` |
| `38-sample-not-synthetic.json` | `sample_not_synthetic:future_approve_reference_capture` |
| `39-sample-actual-user-input.json` | `sample_uses_actual_user_input:future_approve_reference_capture` |
| `40-sample-real-user-text-stored.json` | `sample_stores_real_user_text:future_approve_reference_capture` |
| `41-sample-captured-user-text-present.json` | `sample_captures_user_text:future_approve_reference_capture` |
| `42-sample-missing-future-text-reference.json` | `sample_missing_future_text_reference:future_approve_reference_capture` |
| `43-approve-missing-packet-hash.json` | `sample_packet_hash_mismatch:future_approve_reference_capture` |
| `44-approve-wrong-source-bundle-hash.json` | `sample_source_bundle_hash_mismatch:future_approve_reference_capture` |
| `45-approve-wrong-scope-hash.json` | `sample_scope_hash_mismatch:future_approve_reference_capture` |
| `46-approve-wrong-rehearsal-hash.json` | `sample_rehearsal_hash_mismatch:future_approve_reference_capture` |
| `47-approve-missing-confirmation-phrase.json` | `approved_missing_confirmation_phrase:future_approve_reference_capture:future_approve_exact_scope` |
| `48-approve-missing-exclusion-ack.json` | `approved_missing_exclusion_ack:future_approve_reference_capture:promotion` |
| `49-approve-missing-rollback-ack.json` | `approved_missing_rollback_ack:future_approve_reference_capture` |
| `50-approve-missing-hash-ack.json` | `approved_missing_hash_ack:future_approve_reference_capture` |
| `51-approve-missing-dirty-state-ack.json` | `approved_missing_dirty_state_ack:future_approve_reference_capture` |
| `52-approve-allows-write-now.json` | `sample_allows_formal_vault_write_now:future_approve_reference_capture` |
| `53-approve-creates-action-basis.json` | `sample_creates_action_basis:future_approve_reference_capture` |
| `54-approve-actionable-result.json` | `approved_sample_result_actionable:future_approve_reference_capture, approved_sample_result_bad:future_approve_reference_capture` |
| `55-deny-allows-write.json` | `denied_sample_allows_write:future_deny_reference_capture` |
| `56-deny-wrong-result.json` | `denied_sample_result_bad:future_deny_reference_capture` |
| `57-revise-allows-write.json` | `revise_sample_allows_write:future_revision_reference_capture` |
| `58-revise-wrong-result.json` | `revise_sample_result_bad:future_revision_reference_capture` |
| `59-contract-missing-required-field.json` | `contract_missing_required_future_field:intake_gate_hash` |
| `60-rule-allows-current-approval-collection.json` | `contract_allows_current_approval_collection` |
| `61-rule-allows-real-user-text-storage.json` | `contract_allows_real_user_text_storage` |
| `62-rule-allows-approval-inference.json` | `contract_missing_future_user_turn_required` |
| `63-rule-approved-actionable.json` | `contract_allows_approved_outcome_actionable` |
| `64-receipt-claims-approval.json` | `non_approval_receipt_claims_approval` |
| `65-receipt-real-user-text-stored.json` | `non_approval_receipt_real_user_text_stored` |
| `66-receipt-formal-vault-accessed.json` | `non_approval_receipt_formal_vault_accessed` |
| `67-authority-confusing-text.json` | `authority_confusing_text` |
| `68-too-few-failure-cases.json` | `minimum_failure_cases_too_low` |
| `69-inspector-approve-button.json` | `inspector_control_not_allowed:button:approve, inspector_buttons_not_allowlisted` |
| `70-missing-stop-condition-real-user-text.json` | `missing_stop_condition:real user text storage` |
