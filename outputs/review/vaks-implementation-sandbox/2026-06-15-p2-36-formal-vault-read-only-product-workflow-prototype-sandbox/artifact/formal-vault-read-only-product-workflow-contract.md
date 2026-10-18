# Formal Vault Read-Only Product Workflow Contract

Slice: `2026-06-15-p2-36-formal-vault-read-only-product-workflow-prototype-sandbox`

Version: `p2-36-formal-vault-read-only-product-workflow-prototype-v1`

Truth boundary: sandbox read-only product workflow prototype only. This is not formal vault approval, user instruction, execution permission, reviewed knowledge, evidence support, action basis, mainline readiness, promotion approval, merge approval, or dirty-tree repair.

## Purpose

Show a product-grade read-only operator workflow that connects:

1. P2-33 formal-vault request screening.
2. P2-34 formal-vault operator status surface.
3. P2-35 safe status-surface handoff packet.

The workflow exists to make the safe path visible. It must never collect approval, store user wording, emit commands, access the formal vault, or imply that sandbox output can be merged.

## Source Inputs

- `p2_33_product_acceptance`: `outputs/review/vaks-implementation-sandbox/2026-06-15-p2-33-formal-vault-execution-request-screening-sandbox/product-acceptance-report.md` (`request_screening_pass`)
- `p2_33_verification`: `outputs/review/vaks-implementation-sandbox/2026-06-15-p2-33-formal-vault-execution-request-screening-sandbox/verification.md` (`request_screening_verification`)
- `p2_33_contract`: `outputs/review/vaks-implementation-sandbox/2026-06-15-p2-33-formal-vault-execution-request-screening-sandbox/artifact/formal-vault-execution-request-screening-contract.md` (`request_screening_contract`)
- `p2_34_product_acceptance`: `outputs/review/vaks-implementation-sandbox/2026-06-15-p2-34-formal-vault-operator-status-surface-sandbox/product-acceptance-report.md` (`status_surface_pass`)
- `p2_34_verification`: `outputs/review/vaks-implementation-sandbox/2026-06-15-p2-34-formal-vault-operator-status-surface-sandbox/verification.md` (`status_surface_verification`)
- `p2_34_contract`: `outputs/review/vaks-implementation-sandbox/2026-06-15-p2-34-formal-vault-operator-status-surface-sandbox/artifact/formal-vault-operator-status-surface-contract.md` (`status_surface_contract`)
- `p2_35_product_acceptance`: `outputs/review/vaks-implementation-sandbox/2026-06-15-p2-35-formal-vault-status-surface-handoff-packet-sandbox/product-acceptance-report.md` (`handoff_packet_pass`)
- `p2_35_verification`: `outputs/review/vaks-implementation-sandbox/2026-06-15-p2-35-formal-vault-status-surface-handoff-packet-sandbox/verification.md` (`handoff_packet_verification`)
- `p2_35_contract`: `outputs/review/vaks-implementation-sandbox/2026-06-15-p2-35-formal-vault-status-surface-handoff-packet-sandbox/artifact/formal-vault-status-surface-handoff-packet-contract.md` (`handoff_packet_contract`)
- `p2_35_next_step`: `outputs/review/vaks-implementation-sandbox/2026-06-15-p2-35-formal-vault-status-surface-handoff-packet-sandbox/next-step.md` (`handoff_next_step`)

## Workflow Modes

- `screen_status_handoff_walkthrough`
- `stop_before_formal_vault_workflow`
- `fresh_sandbox_prebrief_workflow`

## Required Checks

- `source_slices_passed`
- `request_screening_visible`
- `status_surface_visible`
- `handoff_packet_visible`
- `no_approval_capture`
- `no_command_surface`
- `no_formal_vault_path`
- `no_action_basis_claim`
- `fresh_sandbox_next_step_only`
- `stop_before_execution`

## Forbidden Operations

- `formal_vault_read` must be `false`
- `formal_vault_scan` must be `false`
- `formal_vault_write` must be `false`
- `formal_vault_hash` must be `false`
- `formal_vault_snapshot` must be `false`
- `formal_vault_state_check` must be `false`
- `obsidian_sync` must be `false`
- `commit` must be `false`
- `push` must be `false`
- `promotion` must be `false`
- `dependency_install` must be `false`
- `background_service` must be `false`
- `mcp_write_tool` must be `false`
- `hooks` must be `false`
- `approval_collection` must be `false`
- `user_instruction_collection` must be `false`
- `user_wording_storage` must be `false`
- `command_emitted` must be `false`
- `absolute_vault_path_resolved` must be `false`
- `execution_permission_granted` must be `false`
- `execution_performed` must be `false`
- `action_basis_creation` must be `false`
- `reviewed_knowledge_creation` must be `false`
- `evidence_support_creation` must be `false`
- `mainline_merge` must be `false`
- `dirty_tree_repair` must be `false`
- `workflow_auto_advance` must be `false`

## Product Surface Rules

- The prototype must be readable without a server.
- The prototype may use inert filter buttons for local visual scanning only.
- The prototype must contain no form, download link, anchor link, contenteditable region, command text box, approval widget, or vault path.
- Any next implementation must start in a fresh sandbox path.
