---
record_kind: sandbox_decision_record_template
slice_id: 2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
---

# Decision Record Template

| Field | Value |
| --- | --- |
| status | `template_only` |
| approved_now | `False` |
| blank_fields_only | `True` |
| must_not_prefill_approval | `True` |
| default_verdict | `NEEDS_REVISION` |
| future_verdict_values | `APPROVED_BY_USER`, `DENIED_BY_USER`, `NEEDS_REVISION` |
| required_packet_hash | `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3` |
| required_source_bundle_hash | `4e7f8cdc4042a6858fcf42796843821391fe6c44e0e55e9e11206eda653f95ad` |
| required_scope_hash | `f5ec5589dc4e983bda3b274bae47766bc58424a98e40363a6437e94b93f5b4e2` |

## Required Future Fields

- `user_exact_text`
- `timestamp_utc`
- `packet_hash`
- `source_bundle_hash`
- `scope_hash`
- `operator_or_agent_id`
- `explicit_denials`
- `rollback_ack`
- `hash_ack`

## Boundary

This is a blank template only. It must not be prefilled by an agent and does not
create approval in this slice.
