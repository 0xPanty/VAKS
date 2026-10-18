---
record_kind: sandbox_source_refresh_candidate_check
status: pass
project_id: VAKS
created_at: 2026-06-11
truth_boundary: source_refresh_candidate_not_support
action_basis_allowed: false
---

# Phase B Source Refresh Candidate Check

## Result

```text
source refresh status: pass
error count: 0
source refresh count: 90
refresh item count: 389
source_span_available_count: 389
pre_refresh_mismatch_count: 68
post_refresh_mismatch_count: 0
refreshed_item_count: 68
already_current_item_count: 321
blocked_no_source_anchor_count: 2
support_passed_count: 0
action_basis_allowed_count: 0
```

## Compared Floor

```text
previous version: Evidence Support Check candidate assembly
required: reduce hash mismatch without semantic support or action leakage
```

## Prior Gates

```text
evidence_support_check: pass / 0 errors
evidence_envelope: pass / 0 errors
context_pack: pass / 0 errors
runtime_feasibility: pass / 0 errors
minimal_doc_patch: pass / 0 errors
contract: pass / 0 errors
```

## Errors

- none
