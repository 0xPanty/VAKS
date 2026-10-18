---
slice_id: 2026-06-19-p2-82-old-file-status-normalization-sandbox-copy-executor-rehearsal-sandbox
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
| 75 target old slice report files | Copied into sandbox fixtures | Read-only source; not modified |

## Outputs

| Output | Purpose |
|---|---|
| `fixtures/target-copies/*.md` | Sandbox copies used for apply/rollback rehearsal |
| `artifact/sandbox_copy_executor_rehearsal.json` | Machine-readable rehearsal result |
| `artifact/sandbox_copy_executor_rehearsal.md` | Operator-readable rehearsal summary |
| `artifact/sandbox_copy_executor_rehearsal.html` | Lightweight rendering |
| `artifact/build_sandbox_copy_executor_rehearsal.py` | Builder |
| `artifact/verify_sandbox_copy_executor_rehearsal.py` | Local verifier and final gate |

## Boundary

This rehearsal writes only sandbox fixture copies. It does not write old slice files, collect approval, authorize execution, create reviewed knowledge, create evidence support, create action basis, or complete the overall goal.
