# Static Boundary Scan Regression Readout

Sandbox-only scanner regression. This is not a general security sandbox, execution authority, mainline approval, promotion approval, reviewed knowledge, evidence support, or action basis.

| Live source | Issues |
| --- | --- |
| `outputs/review/vaks-implementation-sandbox/2026-06-16-p2-57-user-decision-chain-regression-bundle-sandbox/artifact/run_user_decision_chain_regression_bundle.py` | `0` |
| `outputs/review/vaks-implementation-sandbox/2026-06-16-p2-57-user-decision-chain-regression-bundle-sandbox/artifact/build_user_decision_chain_regression_bundle.py` | `0` |

## Scanner Limits

- This is not a general security sandbox.
- This is not execution authority.
- This is not mainline approval.
- This is not promotion approval.
- This scanner checks explicit command surfaces and known dangerous strings; it is not complete program verification.
- Passing this scanner does not authorize commit, push, sync, dependency install, service start, hook install, MCP write, reviewed knowledge, evidence support, or action basis.

## must_not

- `execute_option`
- `merge_mainline`
- `promote`
- `sync_obsidian`
- `commit`
- `push`
- `write_reviewed_knowledge`
- `create_evidence_support`
- `create_action_basis`
- `start_future_slice_by_inference`
