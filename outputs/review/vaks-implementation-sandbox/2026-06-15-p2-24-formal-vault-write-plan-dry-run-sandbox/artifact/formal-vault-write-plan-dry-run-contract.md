# Formal Vault Write-Plan Dry-Run Contract

## Input Contract

- P2-23 sandbox reports and native entry artifact.
- No formal vault read, scan, write, sync, or mutation.

## Output Contract

- Proposed relative file list.
- Per-file source path and SHA256 binding for every proposed target.
- Approval prompt matrix.
- Rollback manifest.
- Hash check plan.
- Stop condition register.
- Static plan inspector with no write controls.

## Product Promise

A future agent can understand exactly what would need approval before any formal
vault write, without receiving permission to perform that write.

## Boundary Promise

This is dry-run only. The formal vault is not accessed. Proposed paths are
relative labels, not write targets. Approval prompts are future gates, not
current approval. Hash receipts are process checks, not evidence support.
