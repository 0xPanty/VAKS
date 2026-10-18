# Failure Case Oracle

| File | Expected failure |
| --- | --- |
| `01-forbidden-formal_vault_write.json` | `forbidden_operation:formal_vault_write` |
| `02-forbidden-obsidian_sync.json` | `forbidden_operation:obsidian_sync` |
| `03-forbidden-commit.json` | `forbidden_operation:commit` |
| `04-forbidden-push.json` | `forbidden_operation:push` |
| `05-forbidden-promotion.json` | `forbidden_operation:promotion` |
| `06-forbidden-dependency_install.json` | `forbidden_operation:dependency_install` |
| `07-forbidden-background_service.json` | `forbidden_operation:background_service` |
| `08-forbidden-mcp_write_tool.json` | `forbidden_operation:mcp_write_tool` |
| `09-forbidden-hooks.json` | `forbidden_operation:hooks` |
| `10-forbidden-real_base_files.json` | `forbidden_operation:real_base_files` |
| `11-forbidden-production_ui.json` | `forbidden_operation:production_ui` |
| `12-forbidden-local_storage_write.json` | `forbidden_operation:local_storage_write` |
| `13-forbidden-network_post.json` | `forbidden_operation:network_post` |
| `14-missing-native-home.json` | `missing_native_page:native_home` |
| `15-missing-readonly-inspector-boundary.json` | `missing_boundary_phrase:read-only inspector` |
| `16-authority-confusing-page.json` | `authority_confusing_text` |
| `17-journey-too-long.json` | `journey_too_deep:native_first_run` |
| `18-journey-missing-stop-condition.json` | `journey_missing_stop_condition:status_to_stop` |
| `19-inspector-view-missing.json` | `missing_inspector_view:receipt_lanes` |
| `20-outside-write-scope.json` | `invalid_write_scope` |
| `21-inspector-save-control.json` | `inspector_control_not_allowed:button:save` |
| `22-too-few-failure-cases.json` | `minimum_failure_cases_too_low` |
