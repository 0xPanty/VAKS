---
record_kind: sandbox_future_approval_questions
slice_id: 2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox
status: sandbox_pilot
sandbox_only: true
truth_boundary: sandbox_only
---

# Future Approval Questions

| Question ID | Future Confirmation Phrase | Required Packet Hash | Default | Status | Excludes |
| --- | --- | --- | --- | --- | --- |
| `future_approve_exact_scope` | `APPROVE EXACT P2 25 PACKET SCOPE FOR FUTURE WRITE ONLY` | `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3` | `deny` | `not_requested` | obsidian_sync, commit, push, promotion |
| `future_approve_source_bindings` | `APPROVE EXACT SOURCE HASH BINDINGS FOR FUTURE WRITE ONLY` | `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3` | `deny` | `not_requested` | obsidian_sync, commit, push, promotion |
| `future_approve_rollback_hash_checks` | `APPROVE ROLLBACK AND HASH GATES FOR FUTURE WRITE ONLY` | `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3` | `deny` | `not_requested` | obsidian_sync, commit, push, promotion |
| `future_approve_no_sync_commit_push_promotion` | `APPROVE NO SYNC COMMIT PUSH OR PROMOTION FOR FUTURE WRITE` | `51244c5051881dfac5ac5648d34908bbf0a74ce1794f8f2868ff6b3378866cb3` | `deny` | `not_requested` | obsidian_sync, commit, push, promotion |

## Boundary

These questions are not being asked now. They are future prompts only. They
collect no approval in this slice and cannot authorize sync, commit, push, or
promotion.

## Next

- [[03 Non Approval Receipt]]
- [[06 Stop Conditions]]
