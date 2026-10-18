---
slice_id: 2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox
status: source_map_ready
---

# Source Map

## Inputs

| Source | Used for | Limit |
|---|---|---|
| p2-72 decision packet JSON | Dry-run manifest with 75 status-only changes | Dry-run only; not approval |
| p2-73 sidecar ledger JSON | Sidecar closeout counts and old-file strict gap | Sidecar only |
| p2-74 operator status surface JSON | Human-readable state and blocked old-file normalization | Status surface only |
| p2-67 strict status package | Final-gate status parser | Parser only |

## Outputs

| Output | Purpose |
|---|---|
| `artifact/old_file_status_normalization_approval_request_contract.json` | Contract and invariants |
| `artifact/build_old_file_status_normalization_approval_request.py` | Rebuilds request packet |
| `artifact/old_file_status_normalization_approval_request.json` | Machine-readable request |
| `artifact/old_file_status_normalization_approval_request.md` | Human-readable approval request |
| `artifact/old_file_status_normalization_approval_request.html` | Portable approval request |
| `artifact/verify_old_file_status_normalization_approval_request.py` | Local verifier and final gate |

## Boundary

This packet asks for a future user decision. It is not approval by itself.
