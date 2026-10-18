---
slice_id: 2026-06-19-p2-87-old-file-status-normalization-diff-preview-sandbox
status: source_map_defined
---

# Source Map

## Inputs

- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json`
- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-86-approval-to-prewrite-gate-chain-sandbox/artifact/approval_to_prewrite_gate_chain.json`

## Output Contract

p2-87 is a read-only diff preview package. It reads current old-slice target files and computes proposed status-only changes in memory. It does not write target files, collect approval, authorize execution, promote knowledge, or create action basis.

## Reuse Value

Future agents can use this slice as the human-review packet for the 75 status-only operations before any separately approved executor slice.
