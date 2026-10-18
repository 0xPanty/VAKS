---
slice_id: 2026-06-19-p2-88-old-file-normalization-user-decision-packet-sandbox
status: drafted
---

# Source Map

## Inputs

- p2-75 approval request contract:
  `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request_contract.json`
- p2-86 approval-to-prewrite gate chain:
  `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-86-approval-to-prewrite-gate-chain-sandbox/artifact/approval_to_prewrite_gate_chain.json`
- p2-87 old-file status normalization diff preview:
  `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-87-old-file-status-normalization-diff-preview-sandbox/artifact/old_file_status_normalization_diff_preview.json`

## Output Contract

The p2-88 artifact is a decision packet only. It can help a user understand the exact approval phrase and the consequences of approving or not approving. It must not:

- collect approval by itself;
- authorize old-file writes;
- apply status normalization;
- become a merge, promotion, reviewed knowledge, evidence support, or action basis.

## Reuse Contract

Later slices may use p2-88 as the user-facing decision packet before requesting or interpreting the exact p2-75 approval phrase. They must still re-check fresh hashes and boundaries before any old-file write.
