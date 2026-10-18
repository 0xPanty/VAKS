---
slice_id: 2026-06-19-p2-81-old-file-status-normalization-transaction-simulator-sandbox
status: source_map_ready
---

# Source Map

## Inputs

| Input | Use | Boundary |
|---|---|---|
| p2-80 transaction package | Source operations, hashes, before/proposed/rollback statuses | No-write future transaction package only |
| p2-75 approval request | Current approval state | Request packet only; approval not collected |
| p2-77 readiness gate | Current executor write gate | Currently blocked |
| p2-67 strict status package | Frontmatter status parser | Parser utility only |
| 75 target old slice report files | Original text for in-memory simulation | Read-only |

## Outputs

| Output | Purpose |
|---|---|
| `artifact/old_file_status_normalization_transaction_simulation.json` | Machine-readable simulation result |
| `artifact/old_file_status_normalization_transaction_simulation.md` | Operator-readable simulation summary |
| `artifact/old_file_status_normalization_transaction_simulation.html` | Lightweight rendering |
| `artifact/build_old_file_status_normalization_transaction_simulation.py` | Builder |
| `artifact/verify_old_file_status_normalization_transaction_simulation.py` | Local verifier and final gate |

## Boundary

This simulator is sandbox evidence only. It does not write old slice files, collect approval, authorize execution, create reviewed knowledge, create evidence support, create action basis, or complete the overall goal.
