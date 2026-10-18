# Sandbox Operator Decision Brief Contract

Slice: `2026-06-15-p2-41-sandbox-operator-decision-brief-sandbox`

Source slice: `2026-06-15-p2-40-sandbox-product-grade-rollup-dashboard-sandbox`

Truth boundary: `sandbox_operator_decision_brief_not_authority`.

This sandbox turns the product-grade rollup into a human operator decision brief. It is not formal vault approval, reviewed knowledge, evidence support, action basis, execution permission, mainline readiness, promotion approval, commit approval, push approval, or Obsidian sync approval.

## Decision Options

- `continue_sandbox_hardening` -> `allowed_only_in_fresh_sandbox`
- `prepare_promotion_request_packet` -> `allowed_as_sandbox_draft_only`
- `formal_vault_work` -> `blocked_needs_separate_user_approval`
- `mainline_merge_commit_push` -> `blocked_needs_separate_user_approval`
- `use_as_action_basis` -> `blocked`

## Required Non-Claims

- not formal vault approval
- not formal vault state
- not formal vault access
- not Obsidian sync
- not user approval
- not user instruction
- not execution permission
- not command surface
- not reviewed knowledge
- not evidence support
- not action basis
- not mainline readiness
- not promotion approval
- not dirty-tree repair
- not auto advance

## Reuse Rule

Use this brief only as a sandbox operator surface. Any promotion, formal vault work, commit, push, sync, or movement into `templates/` or `tools/` needs separate explicit user approval.
