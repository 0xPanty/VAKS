# Strict Status Adoption Screen

Sandbox-only adoption screening for the strict status package.

- adoption screen ready: `True`
- recommended next slice: `2026-06-16-p2-69-user-decision-future-verifier-adoption-prototype-sandbox`

## Adoption Options

| option | decision | allowed without separate approval |
| --- | --- | --- |
| `future_new_sandbox_verifier_adoption` | `RECOMMENDED_NEXT` | `True` |
| `package_only_hold` | `ALLOW_AS_PARKED_OPTION` | `True` |
| `old_slice_backfill` | `PARK_REQUIRES_SEPARATE_USER_APPROVAL` | `False` |
| `shared_helper_or_tools_adoption` | `PARK_REQUIRES_SEPARATE_USER_APPROVAL` | `False` |
| `mainline_integration` | `PARK_REQUIRES_SEPARATE_USER_APPROVAL` | `False` |

## Hard No

- `do_not_modify_old_slices`
- `do_not_create_shared_helper`
- `do_not_edit_tools`
- `do_not_merge_mainline`
- `do_not_promote`
- `do_not_sync_obsidian`
- `do_not_commit`
- `do_not_push`
- `do_not_install_dependencies`
- `do_not_start_background_service`
- `do_not_use_mcp_write_tool`
- `do_not_create_reviewed_knowledge`
- `do_not_create_evidence_support`
- `do_not_create_action_basis`
- `do_not_collect_user_approval_by_inference`
