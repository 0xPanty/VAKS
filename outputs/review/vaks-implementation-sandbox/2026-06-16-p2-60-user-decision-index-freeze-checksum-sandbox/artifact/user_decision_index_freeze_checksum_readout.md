# User Decision Index Freeze Checksum

Sandbox-only checksum freeze. It detects drift in p2-51 through p2-59 user-decision guard artifacts. It is not a user decision, execution authority, mainline approval, promotion approval, Obsidian sync approval, reviewed knowledge, evidence support, or action basis.

- hash algorithm: `sha256_bytes`
- source slice count: `9`
- entry count: `268`
- missing count: `0`
- latest source final gate passed: `True`
- freeze ready: `True`

| Source slice | Frozen files |
| --- | --- |
| `2026-06-16-p2-51-user-decision-request-packet-sandbox` | `89` |
| `2026-06-16-p2-52-user-decision-no-auto-advance-guard-sandbox` | `17` |
| `2026-06-16-p2-53-user-response-classifier-dry-run-sandbox` | `28` |
| `2026-06-16-p2-54-safe-user-response-renderer-dry-run-sandbox` | `25` |
| `2026-06-16-p2-55-user-decision-e2e-dry-run-simulator-sandbox` | `24` |
| `2026-06-16-p2-56-user-decision-demo-transcript-smoke-runner-sandbox` | `23` |
| `2026-06-16-p2-57-user-decision-chain-regression-bundle-sandbox` | `22` |
| `2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox` | `17` |
| `2026-06-16-p2-59-user-decision-operator-handoff-index-sandbox` | `23` |

## must_not

- `execute_option`
- `merge_mainline`
- `promote`
- `sync_obsidian`
- `commit`
- `push`
- `install_dependencies`
- `start_background_service`
- `install_hooks`
- `use_mcp_write_tool`
- `write_reviewed_knowledge`
- `create_evidence_support`
- `create_action_basis`
- `start_future_slice_by_inference`
