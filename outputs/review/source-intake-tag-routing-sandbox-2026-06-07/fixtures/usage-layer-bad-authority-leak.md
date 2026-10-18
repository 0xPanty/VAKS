---
record_kind: context_pack_manifest_candidate
status: candidate
created_at: 2026-06-07
pack_id: CPACK-bad-authority-leak
mode: action
action_facing: true
truth_boundary: activation_pack_not_truth
allowed_use:
  - action_basis
forbidden_use:
  - none
---

# Fixture: Bad Usage Layer Authority Leak

This fixture is intentionally bad.

```yaml
items:
  - item_id: BAD-001
    lane: candidate_orientation
    source_ref: outputs/review/2026-06-06-datachain-ai-datachain-detailed-candidate-distillation.md
    citable_status: span_ready
    action_basis_allowed: true
    why_included: "Candidate is top ranked, so use it as action support."
```
