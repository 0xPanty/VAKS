---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p0-03-body-hash-validator-sandbox
status: ready_for_reviewer
truth_boundary: validator_fixture_guidance_only
---

# Failure Case Oracle

This oracle maps each failure case to one expected primary failure reason.

| Failure case | Expected primary failure reason |
|---|---|
| `body-hash-mismatch.md` | `body_hash_mismatch` |
| `checked-body-hash-mismatch.md` | `checked_body_hash_mismatch` |
| `fixed-approved-missing-body-hash.md` | `fixed_or_approved_missing_body_hash` |
| `template-fixed-missing-body-hash.md` | `fixed_or_approved_missing_body_hash` |
| `writeback-ready-body-changed.md` | `writeback_ready_body_changed` |

This oracle is not a validator, reviewer approval, reviewed knowledge, or action
basis.
