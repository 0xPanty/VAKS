# Strict Status Package Manifest

Sandbox-local package for strict frontmatter status parsing.

- package ready: `True`
- source slice: `2026-06-16-p2-66-user-decision-chain-hardening-readiness-sandbox`

## Package API

### `parse_strict_frontmatter_status`

- input: `markdown text`
- output: `dict(valid, status, errors, body_status_mentions)`
- authority: parser result only; not reviewer or Product Acceptance

### `status_matches`

- input: `markdown text and expected status`
- output: `bool`
- authority: status comparison only; not action approval

## Self Tests

- `valid_status_matches`: `True`
- `body_override_does_not_match`: `True`
- `body_override_preserves_frontmatter`: `True`
- `duplicate_rejected`: `True`
- `missing_opening_rejected`: `True`

## Hard No

- `do_not_modify_old_slices`
- `do_not_create_shared_helper`
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
