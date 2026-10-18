---
slice_id: 2026-06-19-p2-76-old-file-status-normalization-executor-preflight-sandbox
status: source_map_ready
---

# Source Map

## Inputs

| Source | Used for | Limit |
|---|---|---|
| p2-72 decision packet JSON | 75 dry-run status changes | Dry-run source only |
| p2-75 approval request JSON | exact approval phrase and current no-approval state | Request packet only, not approval |
| p2-67 strict status package | frontmatter status parsing | Parser only |
| original old slice report files | read-only current status verification | Read-only; no writes |

## Outputs

| Output | Purpose |
|---|---|
| `artifact/old_file_status_normalization_executor_preflight_contract.json` | Contract and invariants |
| `artifact/build_old_file_status_normalization_executor_preflight.py` | Builds preflight dry-run |
| `artifact/old_file_status_normalization_executor_preflight.json` | Machine-readable preflight |
| `artifact/old_file_status_normalization_executor_preflight.md` | Human-readable preflight |
| `artifact/old_file_status_normalization_executor_preflight.html` | Portable preflight view |
| `artifact/verify_old_file_status_normalization_executor_preflight.py` | Local verifier and final gate |

## Boundary

This preflight is an executor rehearsal only. It is not approval, not execution, not rollback execution, and not old-file normalization.
