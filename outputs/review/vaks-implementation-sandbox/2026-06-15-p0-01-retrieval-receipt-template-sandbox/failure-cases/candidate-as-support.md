---
record_kind: retrieval_receipt_failure_case
case_id: candidate-as-support
expected_future_validator_result: fail
reason: candidate_material_marked_as_support
---

# Candidate As Support

Invalid pattern:

```yaml
selected_items:
  - ref: outputs/review/example-candidate-distillation.md
    record_kind: candidate_distillation
    knowledge_status: candidate
    authority_bucket: candidate
    pack_role: support
    action_basis_allowed: true
support_checks:
  - target_ref: review-candidate:target
    proposed_support_item_ref: outputs/review/example-candidate-distillation.md
    independent_anchor_ref:
    result: supported
```

Why this fails:

```text
Candidate material is review input or orientation. It cannot be final support or
action basis without independent evidence support and review.
```
