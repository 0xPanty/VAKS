---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p2-27-formal-vault-user-decision-intake-gate-sandbox
status: built_pending_review
truth_boundary: sandbox_only
---

# Source Map

This slice reads P2-26 as the product-grade sandbox source and P2-25 packet
config for exact future confirmation phrases. It does not read or write the
formal Obsidian vault.

| Source | Path | Evidence |
| --- | --- | --- |
| `source_next_step` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/next-step.md` | exists: `True` | sha256: `0e444ae45b96c2888635b0728fe20dc4bf7392e227295fe1f2318ab135ef78fa` |
| `source_product_acceptance` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/product-acceptance-report.md` | exists: `True` | sha256: `6611c43ddd4ed1b4677eb99799c0e12e9d456f4e66b3b5f7e70943d34b76b4e2` |
| `source_verification` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/verification.md` | exists: `True` | sha256: `732dc3f9477bdb9d8595b1af277bc2175f9e256a027030b0a5210da3de89cebc` |
| `source_reviewer_report` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/reviewer-report.md` | exists: `True` | sha256: `2ee9fb507a01cd1bdb47b60a34620701147f49a76335d994e6d89dd195f67284` |
| `source_boundary_audit` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/boundary-audit.md` | exists: `True` | sha256: `93b88d53c17795399642a1ed3de0ab7ca7eb5376be2aec9bee788f4c2e384796` |
| `source_map` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/source-map.md` | exists: `True` | sha256: `e6ef308f02ee5a02e8fffeac638d51d6855f267fcda687a432a11c22b9d89f2a` |
| `source_rehearsal_config` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/fixtures/valid-decision-rehearsal-config.json` | exists: `True` | sha256: `3884fb3ee142653e3aef8e799fc0bb6c8f45bc6c3fe8507dafff58eb30deb234` |
| `source_rehearsal_contract` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/artifact/formal-vault-write-decision-rehearsal-contract.md` | exists: `True` | sha256: `737f832f062e4997375753021c842a477f23f48b6b2d77445ab698311b685e9c` |
| `source_rehearsal_receipt` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/prototype/formal-vault-write-decision-rehearsal/Receipts/formal-vault-write-decision-rehearsal-receipt.json` | exists: `True` | sha256: `b7a211bebc1c2b17814550e57db879a7c6906cad285c8b759deb1870865a1867` |
| `source_scenario_matrix` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/prototype/formal-vault-write-decision-rehearsal/01 Scenario Matrix.md` | exists: `True` | sha256: `41142ce0f08963c4f3b4aec5c2a211d3d66343fc688a1cf2743129140e38dfc3` |
| `source_decision_rules` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/prototype/formal-vault-write-decision-rehearsal/05 Decision Rules.md` | exists: `True` | sha256: `b67bca01b9077e18e57019387f5ccf807a715ec3403b6f553a1d4f98bd67a8ff` |
| `source_non_approval_receipt` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/prototype/formal-vault-write-decision-rehearsal/06 Non Approval Receipt.md` | exists: `True` | sha256: `7993bed36db5bfd8e09c13754ee30dcfd24c7d136d8894979633a0f94bab2b3b` |
| `source_stop_conditions` | `../2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox/prototype/formal-vault-write-decision-rehearsal/07 Stop Conditions.md` | exists: `True` | sha256: `48fdf628c4e4a3ce8c3f786ea08bbe02a7f7000891a577a4087cc0e40423bd5a` |
| `source_packet_config` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/fixtures/valid-approval-packet-config.json` | exists: `True` | sha256: `51c4a7f639b0d1bde387b4177cb0ab3cfa03b0e35f0a13978b0aaec12969fda5` |

## Hash Inputs

- source_input_bundle_hash: `9b19ca1276580ec63cc90b56d33ed3962aacefde25f86e0018616f722b6fb673`
- source_rehearsal_hash: `cfa4c69de3df0dde571a1a4912a17bcfbf75dac3a901f112a1b1b98d84bed72c`
- source_packet_hash: `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3`
- source_packet_source_bundle_hash: `4e7f8cdc4042a6858fcf42796843821391fe6c44e0e55e9e11206eda653f95ad`
- source_packet_scope_hash: `f5ec5589dc4e983bda3b274bae47766bc58424a98e40363a6437e94b93f5b4e2`
- intake_gate_hash: `f9f0f7a0ac4fc75bae06c492e82a38646d1ae88b1c99829b478f5ca10ce5cf96`

## Boundary

P2-26 `PASS_PRODUCT_GRADE` is a sandbox input only. It is not actual approval,
reviewed knowledge, evidence support, action basis, mainline approval, formal
vault approval, sync approval, commit approval, push approval, or promotion
approval.
