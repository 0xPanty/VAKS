---
slice_id: 2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox
status: source_map_ready
---

# Source Map

## Inputs

| Input | Use | Boundary |
|---|---|---|
| p2-72 decision packet | 75 dry-run status changes | Dry-run manifest only |
| p2-75 approval request | Exact approval phrase and current approval status | Request packet only; approval not collected |
| p2-77 readiness gate | Current write gate | Currently blocked; not execution |
| p2-79 fresh drift recheck | Fresh clean/no-drift evidence | Preflight evidence only; not approval |
| p2-67 strict status package | Frontmatter status parser | Parser utility only |
| 75 target old slice reports | Current hashes and statuses | Read-only transaction inputs |

## Outputs

| Output | Purpose |
|---|---|
| `artifact/old_file_status_normalization_transaction_package.json` | Machine-readable no-write transaction package |
| `artifact/old_file_status_normalization_transaction_package.md` | Operator-readable transaction summary |
| `artifact/old_file_status_normalization_transaction_package.html` | Lightweight rendering |
| `artifact/build_old_file_status_normalization_transaction_package.py` | Builder |
| `artifact/verify_old_file_status_normalization_transaction_package.py` | Local verifier and final gate |

## Boundary

This transaction package is sandbox evidence and future execution preparation. It is not user approval, not write authority, not reviewed knowledge, not evidence support, not action basis, and not goal completion.
