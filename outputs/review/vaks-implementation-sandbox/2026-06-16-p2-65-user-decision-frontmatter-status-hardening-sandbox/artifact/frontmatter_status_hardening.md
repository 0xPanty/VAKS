# Frontmatter Status Hardening

Sandbox-only strict status parser for user-decision closeout reports.

- hardening ready: `True`
- source slice: `2026-06-16-p2-64-user-decision-replay-portability-audit-sandbox`

## Source Statuses

| report | status | expected | match |
| --- | --- | --- | --- |
| verification | `local_verification_passed` | `local_verification_passed` | `True` |
| reviewer | `review_pass_no_blocker` | `review_pass_no_blocker` | `True` |
| boundary | `pass_boundary` | `pass_boundary` | `True` |
| product | `pass_product_grade` | `pass_product_grade` | `True` |
| next_step | `pass_product_grade_pending_next_slice` | `pass_product_grade_pending_next_slice` | `True` |

## Parser Contract

- `requires_opening_frontmatter_delimiter`: `True`
- `requires_closing_frontmatter_delimiter`: `True`
- `requires_exactly_one_status_in_frontmatter`: `True`
- `requires_non_empty_status`: `True`
- `ignores_body_status_mentions`: `True`
- `does_not_substring_match_pass_tokens`: `True`

## Hard No

- `do_not_execute_user_decision_option`
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
