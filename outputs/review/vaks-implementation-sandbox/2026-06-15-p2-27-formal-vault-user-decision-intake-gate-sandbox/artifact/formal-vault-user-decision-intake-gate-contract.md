# Formal Vault User Decision Intake Gate Contract

## Input Contract

- P2-26 product-grade decision rehearsal and hashes.
- P2-25 approval packet confirmation phrases.
- No actual user approval, real user text storage, formal vault read, scan,
  write, sync, snapshot, hash, or mutation.

## Required Future Decision Fields

- `decision_id`
- `decision_verdict`
- `future_user_exact_text_reference`
- `user_turn_id`
- `timestamp_utc`
- `packet_hash`
- `source_bundle_hash`
- `scope_hash`
- `rehearsal_hash`
- `intake_gate_hash`
- `operator_or_agent_id`
- `scope_ids`
- `explicit_exclusions_ack`
- `rollback_ack`
- `hash_ack`
- `dirty_state_ack`
- `extra_files_requested`

## Required Approval Phrases

- `future_approve_exact_scope`: `APPROVE EXACT P2 25 PACKET SCOPE FOR FUTURE WRITE ONLY`
- `future_approve_source_bindings`: `APPROVE EXACT SOURCE HASH BINDINGS FOR FUTURE WRITE ONLY`
- `future_approve_rollback_hash_checks`: `APPROVE ROLLBACK AND HASH GATES FOR FUTURE WRITE ONLY`
- `future_approve_no_sync_commit_push_promotion`: `APPROVE NO SYNC COMMIT PUSH OR PROMOTION FOR FUTURE WRITE`

## Output Contract

- Future decision intake contract.
- Synthetic approve/deny/revise intake reference records.
- Non-approval receipt for this slice.
- Stop condition register.
- Static inspector with no approval, write, save, submit, network, or storage
  controls.

## Boundary Promise

This is a user-decision intake gate draft only. It defines what a later,
separately approved slice must validate. A separate future execution slice is
required. It is not actual approval, not a user decision record, not action
basis, and not permission to write the formal vault.

## Hashes

- source_input_bundle_hash: `9b19ca1276580ec63cc90b56d33ed3962aacefde25f86e0018616f722b6fb673`
- source_rehearsal_hash: `cfa4c69de3df0dde571a1a4912a17bcfbf75dac3a901f112a1b1b98d84bed72c`
- source_packet_hash: `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3`
- source_packet_source_bundle_hash: `4e7f8cdc4042a6858fcf42796843821391fe6c44e0e55e9e11206eda653f95ad`
- source_packet_scope_hash: `f5ec5589dc4e983bda3b274bae47766bc58424a98e40363a6437e94b93f5b4e2`
- intake_gate_hash: `f9f0f7a0ac4fc75bae06c492e82a38646d1ae88b1c99829b478f5ca10ce5cf96`
