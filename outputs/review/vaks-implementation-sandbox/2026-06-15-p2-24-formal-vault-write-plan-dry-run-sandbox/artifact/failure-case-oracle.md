# Failure Case Oracle

| File | Expected failure |
| --- | --- |
| `01-forbidden-formal_vault_read.json` | `forbidden_operation:formal_vault_read` |
| `02-forbidden-formal_vault_scan.json` | `forbidden_operation:formal_vault_scan` |
| `03-forbidden-formal_vault_write.json` | `forbidden_operation:formal_vault_write` |
| `04-forbidden-obsidian_sync.json` | `forbidden_operation:obsidian_sync` |
| `05-forbidden-commit.json` | `forbidden_operation:commit` |
| `06-forbidden-push.json` | `forbidden_operation:push` |
| `07-forbidden-promotion.json` | `forbidden_operation:promotion` |
| `08-forbidden-dependency_install.json` | `forbidden_operation:dependency_install` |
| `09-forbidden-background_service.json` | `forbidden_operation:background_service` |
| `10-forbidden-mcp_write_tool.json` | `forbidden_operation:mcp_write_tool` |
| `11-forbidden-hooks.json` | `forbidden_operation:hooks` |
| `12-forbidden-real_base_files.json` | `forbidden_operation:real_base_files` |
| `13-forbidden-production_ui.json` | `forbidden_operation:production_ui` |
| `14-forbidden-local_storage_write.json` | `forbidden_operation:local_storage_write` |
| `15-forbidden-network_post.json` | `forbidden_operation:network_post` |
| `16-absolute-formal-target.json` | `proposed_file_absolute_or_forbidden:native_home` |
| `17-write-enabled-target.json` | `proposed_file_write_enabled:native_home` |
| `18-missing-user-approval.json` | `proposed_file_missing_user_approval:native_home` |
| `19-auto-approval-prompt.json` | `approval_prompt_not_deny:approve_formal_vault_write_scope` |
| `20-missing-rollback-snapshot.json` | `rollback_snapshot_missing` |
| `21-missing-hash-before.json` | `hash_before_missing` |
| `22-executable-command-template.json` | `hash_plan_executable_command` |
| `23-authority-confusing-stop.json` | `authority_confusing_text` |
| `24-approval-missing-file-binding.json` | `approval_prompt_missing_file_binding:approve_formal_vault_write_scope` |
| `25-approval-missing-plan-hash.json` | `approval_prompt_missing_plan_hash:approve_formal_vault_write_scope` |
| `26-rollback-file-entries-missing.json` | `rollback_file_entries_missing` |
| `27-rollback-dirty-abort-missing.json` | `rollback_dirty_state_abort_missing` |
| `28-hash-records-missing.json` | `hash_records_missing` |
| `29-hash-rollback-verify-missing.json` | `hash_rollback_verification_missing` |
| `30-too-few-failure-cases.json` | `minimum_failure_cases_too_low` |
| `31-missing-source-path-binding.json` | `proposed_file_source_path_missing:native_home` |
| `32-source-hash-mismatch.json` | `proposed_file_source_hash_mismatch:native_home` |
