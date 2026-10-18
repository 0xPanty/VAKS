# Formal Vault Write Decision Rehearsal Contract

## Input Contract

- P2-25 product-grade approval packet and hashes.
- No actual user approval, formal vault read, scan, write, sync, snapshot, hash,
  or mutation.

## Output Contract

- Synthetic approve/deny/revise scenarios.
- Decision rule matrix.
- Non-approval rehearsal receipt.
- Stop condition register.
- Static decision inspector with no approval or write controls.

## Product Promise

A future agent can understand how a real future decision should be classified,
without treating this rehearsal as the decision itself.

## Boundary Promise

This is decision rehearsal only. Synthetic approval is not actionable. Deny and
revise block write. Nothing in this slice approves formal vault write, sync,
commit, push, promotion, reviewed knowledge, evidence support, or action basis.

## Hashes

- source_input_bundle_hash: `88a53d0d92e2ca7e0c5933e350d5e9f3d8ff823b188f9e1db9fa076a6d05f626`
- source_packet_hash: `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3`
- source_packet_source_bundle_hash: `4e7f8cdc4042a6858fcf42796843821391fe6c44e0e55e9e11206eda653f95ad`
- source_packet_scope_hash: `f5ec5589dc4e983bda3b274bae47766bc58424a98e40363a6437e94b93f5b4e2`
- rehearsal_hash: `cfa4c69de3df0dde571a1a4912a17bcfbf75dac3a901f112a1b1b98d84bed72c`
