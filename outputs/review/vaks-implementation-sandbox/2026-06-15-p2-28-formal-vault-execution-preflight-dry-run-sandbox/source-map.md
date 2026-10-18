---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p2-28-formal-vault-execution-preflight-dry-run-sandbox
status: built_pending_review
truth_boundary: sandbox_only
---

# Source Map

This slice reads P2-27 as the product-grade sandbox source and P2-25 packet
config for exact target scope. It does not read or write the formal Obsidian
vault.

| Source | Path | Evidence |
| --- | --- | --- |
| `source_next_step` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/next-step.md` | exists: `True` | sha256: `73597a8c2723d961179850cc9b63dbc80948b7938f5a13b8636b99d49487fd0f` |
| `source_product_acceptance` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/product-acceptance-report.md` | exists: `True` | sha256: `6b9772ca013b0e5e69d518a2ed92079c787ca455e2a9bd89aec75d521658a19c` |
| `source_verification` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/verification.md` | exists: `True` | sha256: `85812f066a5c8c4bb48bd3ffe3bf6de3ff28d898873a5e8c32959304ab5bed62` |
| `source_reviewer_report` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/reviewer-report.md` | exists: `True` | sha256: `5458110950b91199e83eda0800b847c4f102f1b9938fcc8bef879efaefa68b16` |
| `source_boundary_audit` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/boundary-audit.md` | exists: `True` | sha256: `d07804f626182ecdc39d84f11ba7fc2bfb668539502cd3a97616ae916bd468ad` |
| `source_map` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/source-map.md` | exists: `True` | sha256: `55b0e0def2d0427c5b15619cc4fc1b010c066247c0b394b9a81fa6ddfd5aa5da` |
| `source_intake_config` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/fixtures/valid-user-decision-intake-gate-config.json` | exists: `True` | sha256: `36bce4633e423a74834a739c8e0de4c42d75c63bf7d9ecc2ca4226be8e9e12e8` |
| `source_intake_contract` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/artifact/formal-vault-user-decision-intake-gate-contract.md` | exists: `True` | sha256: `d4620b50589fb2351add4acc9f48c0ec7fdcd93727cdec4a0cad18b4a2e1fd41` |
| `source_intake_receipt` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/prototype/formal-vault-user-decision-intake-gate/Receipts/formal-vault-user-decision-intake-gate-receipt.json` | exists: `True` | sha256: `ffa16f9749394946ed5626454e48093c48812977658c1910a3414e31af86bd90` |
| `source_future_contract_page` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/prototype/formal-vault-user-decision-intake-gate/01 Future Decision Contract.md` | exists: `True` | sha256: `8e2f84f6936a3b645d0df917125bb095be93bf392025bb8dab98cc850685f749` |
| `source_capture_fields_page` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/prototype/formal-vault-user-decision-intake-gate/02 Required Capture Fields.md` | exists: `True` | sha256: `aa94529b9f4a0f6b267684b93eb6c05bfecbf6dfb9e3066ff8b1e26a25139baa` |
| `source_approval_checklist_page` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/prototype/formal-vault-user-decision-intake-gate/03 Future Approval Checklist.md` | exists: `True` | sha256: `0dcb27fa9ee18f2b90158b1f8f852c7aa4b360f9e3d5e62de70c7aecbf5f4458` |
| `source_stop_conditions_page` | `../2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox/prototype/formal-vault-user-decision-intake-gate/06 Stop Conditions.md` | exists: `True` | sha256: `7371ce66e039a062488f57ca47259b6d3dcd080f5e319936a45b151fef6ee5e2` |
| `source_packet_config` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/fixtures/valid-approval-packet-config.json` | exists: `True` | sha256: `51c4a7f639b0d1bde387b4177cb0ab3cfa03b0e35f0a13978b0aaec12969fda5` |

## Hash Inputs

- source_input_bundle_hash: `c44fcb9394950a4ec34020974e45e19b04db2e6aee8e9ff65791c9e8042f0263`
- source_intake_gate_hash: `f9f0f7a0ac4fc75bae06c492e82a38646d1ae88b1c99829b478f5ca10ce5cf96`
- source_packet_hash: `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3`
- source_packet_source_bundle_hash: `4e7f8cdc4042a6858fcf42796843821391fe6c44e0e55e9e11206eda653f95ad`
- source_packet_scope_hash: `f5ec5589dc4e983bda3b274bae47766bc58424a98e40363a6437e94b93f5b4e2`
- target_manifest_hash: `9a8934b0e9a313289f6298c38033ee4bd8f24a712742542cc49c9ea91f18bf9a`
- preflight_hash: `7c4ea5f23a2b14bdbc583eb0b014b14eb79883805382ddc00ae4e336b169bce1`

## Boundary

P2-27 `PASS_PRODUCT_GRADE` is a sandbox input only. It is not actual approval,
reviewed knowledge, evidence support, action basis, mainline approval, formal
vault approval, sync approval, commit approval, push approval, promotion
approval, or execution approval.
