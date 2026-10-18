---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox
status: built_pending_review
truth_boundary: sandbox_only
---

# Source Map

This slice reads P2-25 as the product-grade sandbox source. It does not read or
write the formal Obsidian vault.

| Source | Path | Evidence |
| --- | --- | --- |
| `source_next_step` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/next-step.md` | exists: `True` | sha256: `24bd141bc18398791177b1bcfa9daf8f2e56905b7c553fe2540c2ee9aa8eab0c` |
| `source_product_acceptance` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/product-acceptance-report.md` | exists: `True` | sha256: `1978e94a80c2b33e87ae7b6eb62c8ba0c3382d327721f0f6635e76a55a54a388` |
| `source_verification` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/verification.md` | exists: `True` | sha256: `7899646b14e57ab0d678a0f22ce6d64713a5a1c5142b57f53f45369724918ff7` |
| `source_reviewer_report` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/reviewer-report.md` | exists: `True` | sha256: `a30ec19f26dd37c990155d50caea75f2cbc1d75c7510acc32051892710c5c5f3` |
| `source_boundary_audit` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/boundary-audit.md` | exists: `True` | sha256: `0c27d011fdc8d9394f460085d61b3bdc75cf40bd48a4259f42dbe2d70123c757` |
| `source_map` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/source-map.md` | exists: `True` | sha256: `64267c00b302b5eefd61168dbcc3913b6925189c25d2ad2fefdd0652f4423239` |
| `source_config` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/fixtures/valid-approval-packet-config.json` | exists: `True` | sha256: `51c4a7f639b0d1bde387b4177cb0ab3cfa03b0e35f0a13978b0aaec12969fda5` |
| `source_contract` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/artifact/formal-vault-write-approval-packet-contract.md` | exists: `True` | sha256: `4eea2b5f0b61f6507996858db0dfb063f94f09065a49ac8b8fbedbf9ab465a80` |
| `source_receipt` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/prototype/formal-vault-write-approval-packet/Receipts/formal-vault-write-approval-packet-receipt.json` | exists: `True` | sha256: `e0b13d48d0eede7c8fdc0c8f66ada12e5fba30825c9477867b44845f49814c4a` |
| `source_scope_dossier` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/prototype/formal-vault-write-approval-packet/01 Scope Dossier.md` | exists: `True` | sha256: `5cbefc28051979e41bf30ef02f1ebe2a23c69fb566d95b6ca184665950fa597c` |
| `source_questions` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/prototype/formal-vault-write-approval-packet/02 Future Approval Questions.md` | exists: `True` | sha256: `59ccfcaae3b2eb78473243db9c1a535d2b5c423fec93543f043cbb91ab248654` |
| `source_non_approval_receipt` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/prototype/formal-vault-write-approval-packet/03 Non Approval Receipt.md` | exists: `True` | sha256: `9dc44526a62f73f2b26505d674488c7ea2bf88b84aa7972f4f61aac09b76b8cc` |
| `source_decision_template` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/prototype/formal-vault-write-approval-packet/04 Decision Record Template.md` | exists: `True` | sha256: `db092955a24dbc26385c3fbecdece7e0d83694e486d30be47e1f4743f124c95c` |
| `source_hash_binding` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/prototype/formal-vault-write-approval-packet/05 Source And Hash Binding.md` | exists: `True` | sha256: `f3462b20ed57d60ceb1a9feb31f26329ac4414013dafa0ba195cef0be9ba2fdb` |
| `source_stop_conditions` | `../2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox/prototype/formal-vault-write-approval-packet/06 Stop Conditions.md` | exists: `True` | sha256: `c84e2bf82e5071781900dc9f61a03a67333c57d67f487b26aea404bc7c7bffef` |

## Hash Inputs

- source_input_bundle_hash: `88a53d0d92e2ca7e0c5933e350d5e9f3d8ff823b188f9e1db9fa076a6d05f626`
- source_packet_hash: `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3`
- source_packet_source_bundle_hash: `4e7f8cdc4042a6858fcf42796843821391fe6c44e0e55e9e11206eda653f95ad`
- source_packet_scope_hash: `f5ec5589dc4e983bda3b274bae47766bc58424a98e40363a6437e94b93f5b4e2`
- rehearsal_hash: `cfa4c69de3df0dde571a1a4912a17bcfbf75dac3a901f112a1b1b98d84bed72c`

## Boundary

P2-25 `PASS_PRODUCT_GRADE` is a sandbox input only. It is not actual approval,
reviewed knowledge, evidence support, action basis, mainline approval, formal
vault approval, sync approval, commit approval, push approval, or promotion
approval.
