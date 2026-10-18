---
record_kind: retrieval_receipt_failure_case
case_id: feedback-as-support
expected_future_validator_result: fail
reason: feedback_used_as_truth_or_support
---

# Feedback As Support

Invalid pattern:

```yaml
selected_items:
  - ref: outputs/feedback/events/2026-06-15.jsonl#feedback-1
    record_kind: feedback_event
    authority_bucket: feedback
    pack_role: support
support_checks:
  - target_ref: decision:example
    proposed_support_item_ref: outputs/feedback/events/2026-06-15.jsonl#feedback-1
    result: supported
```

Why this fails:

```text
Feedback can change activation, usefulness, scope fit, and review pressure. It
cannot directly change truth confidence, verification status, source
reliability, reviewed notes, reviewed relations, or action basis.
```
