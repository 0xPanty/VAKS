# Post-Opus User Approval Decision Packet

## Purpose

Use this packet only after a real `OPUS_PASS_SANDBOX_CLOSEOUT` result has been retained and validated in a sandbox-only result-intake slice.

## Current Dry-Run State

- actual_opus_result_present: false
- validated_opus_pass_present: false
- user_approval_present: false
- mainline_merge_allowed: false
- promotion_allowed: false
- reviewed_knowledge_write_allowed: false
- evidence_support_write_allowed: false
- action_basis_allowed: false
- commit_push_sync_allowed: false
- goal_complete_now: false

## Exact Future Approval Phrase

The future user message must exactly match:

```text
I explicitly approve post-Opus mainline consideration for VAKS sandbox closeout: prepare a separate merge proposal only; do not merge, promote, commit, push, sync, or write reviewed knowledge/action basis without my next explicit approval.
```

## Boundary

Opus PASS is not user approval. This packet is not merge, promotion, reviewed knowledge, evidence support, action basis, commit, push, sync, or goal completion.

## Allowed After Exact Future Approval

Prepare a separate merge proposal only. The proposal must still be separately reviewed and explicitly approved before any mainline edit, promotion, commit, push, sync, or truth/action write.
