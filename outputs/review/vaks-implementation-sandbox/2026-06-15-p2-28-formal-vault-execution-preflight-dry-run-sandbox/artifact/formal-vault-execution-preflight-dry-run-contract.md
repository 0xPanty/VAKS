# Formal Vault Execution Preflight Dry-Run Contract

## Input Contract

- P2-27 product-grade user-decision intake gate and hashes.
- P2-25 approval packet target scope.
- No actual approval collection, real user text storage, formal vault read,
  scan, state inspection, write, snapshot, hash, sync, or mutation.

## Required Preflight Checks

- `source_product_passed`
- `intake_gate_hash_match`
- `packet_hash_match`
- `source_bundle_hash_match`
- `scope_hash_match`
- `target_scope_exact`
- `targets_relative_only`
- `no_extra_targets`
- `formal_vault_not_accessed`
- `formal_vault_state_not_inspected`
- `snapshot_plan_present_not_executed`
- `rollback_plan_present_not_executed`
- `hash_plan_present_not_executed`
- `no_sync_commit_push_promotion`
- `real_user_text_not_stored`
- `separate_execution_slice_required`

## Dry-Run Target Manifest

- `native_home` -> `VAKS-Workbench-Draft/00 Native Home.md`
- `status_board` -> `VAKS-Workbench-Draft/02 Status Board.md`
- `receipt_index` -> `VAKS-Workbench-Draft/03 Receipt Index.md`
- `boundary_stop` -> `VAKS-Workbench-Draft/04 Boundary Stop.md`
- `readonly_inspector` -> `VAKS-Workbench-Draft/readonly-inspector.html`

## Output Contract

- Execution preflight contract.
- Dry-run target manifest.
- Synthetic approved/denied/revision preflight samples.
- Non-execution receipt.
- Stop condition register.
- Static inspector with no execute, approval, write, save, submit, network, or
  storage controls.

## Boundary Promise

This is an execution preflight dry-run only. It proves checklist shape, not
execution readiness. It does not approve, execute, inspect, write, sync, commit,
push, or promote.

## Hashes

- source_input_bundle_hash: `c44fcb9394950a4ec34020974e45e19b04db2e6aee8e9ff65791c9e8042f0263`
- source_intake_gate_hash: `f9f0f7a0ac4fc75bae06c492e82a38646d1ae88b1c99829b478f5ca10ce5cf96`
- source_packet_hash: `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3`
- source_packet_source_bundle_hash: `4e7f8cdc4042a6858fcf42796843821391fe6c44e0e55e9e11206eda653f95ad`
- source_packet_scope_hash: `f5ec5589dc4e983bda3b274bae47766bc58424a98e40363a6437e94b93f5b4e2`
- target_manifest_hash: `9a8934b0e9a313289f6298c38033ee4bd8f24a712742542cc49c9ea91f18bf9a`
- preflight_hash: `7c4ea5f23a2b14bdbc583eb0b014b14eb79883805382ddc00ae4e336b169bce1`
