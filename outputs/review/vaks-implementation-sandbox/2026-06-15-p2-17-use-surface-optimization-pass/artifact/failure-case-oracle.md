---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p2-17-use-surface-optimization-pass
status: implemented_pending_review
truth_boundary: sandbox_oracle_only
---

# Failure Case Oracle

| Failure case | Primary expected code |
|---|---|
| `entry-missing.json` | `US_REQUIRED_ENTRY_MISSING` |
| `entry-approves-reviewed.json` | `US_ENTRY_APPROVES_FORBIDDEN` |
| `entry-reviewed-write.json` | `US_ENTRY_REVIEWED_WRITE_FORBIDDEN` |
| `entry-promotes.json` | `US_ENTRY_PROMOTION_FORBIDDEN` |
| `entry-action-basis.json` | `US_ENTRY_ACTION_BASIS_FORBIDDEN` |
| `entry-receipt-missing.json` | `US_ENTRY_RECEIPT_MISSING` |
| `question-missing.json` | `US_QUESTION_MISSING` |
| `question-creates-authority.json` | `US_QUESTION_CREATES_AUTHORITY` |
| `status-can-approve.json` | `US_STATUS_CAN_APPROVE` |
| `status-flags-missing.json` | `US_STATUS_FLAGS_MISSING` |
| `search-receipt-missing.json` | `US_RECEIPT_BACKED_SEARCH_REQUIRED` |
| `selected-by-as-support.json` | `US_SELECTED_BY_AS_SUPPORT` |
| `raw-topk-trust.json` | `US_RAW_TOPK_TRUST` |
| `action-mode-gate-missing.json` | `US_ACTION_MODE_GATE_MISSING` |
| `context-pack-as-action-basis.json` | `US_CONTEXT_PACK_AS_ACTION_BASIS` |
| `badge-promotes.json` | `US_BADGE_PROMOTES` |
| `badge-display-not-only.json` | `US_BADGE_DISPLAY_ONLY_REQUIRED` |
| `dirty-state-as-truth.json` | `US_DIRTY_STATE_AS_KNOWLEDGE` |
| `dirty-guardrail-missing.json` | `US_DIRTY_GUARDRAIL_MISSING` |
| `hash-as-support.json` | `US_HASH_AS_SUPPORT` |
| `sync-without-operation-receipt.json` | `US_SYNC_WITHOUT_OPERATION_RECEIPT` |
| `sync-mutates-truth.json` | `US_SYNC_MUTATES_TRUTH` |
| `mainline-ready.json` | `US_MAINLINE_READY_FORBIDDEN` |
| `write-path-outside-slice.json` | `US_WRITE_PATH_OUTSIDE_SLICE` |
| `protected-path-write.json` | `US_PROTECTED_PATH_TARGET` |
| `obsidian-path-case-bypass.json` | `US_PROTECTED_PATH_TARGET` |
| `runtime-or-sync-forbidden.json` | `US_RUNTIME_OR_SYNC_FORBIDDEN` |
| `real-ui-started.json` | `US_RUNTIME_OR_SYNC_FORBIDDEN` |
| `background-service-started.json` | `US_RUNTIME_OR_SYNC_FORBIDDEN` |
| `hook-enabled.json` | `US_RUNTIME_OR_SYNC_FORBIDDEN` |
| `automation-started.json` | `US_RUNTIME_OR_SYNC_FORBIDDEN` |

Expected failures are sandbox validation results only. Passing this suite does
not approve production UI, reviewed knowledge, evidence support, action basis,
promotion, sync, commit, push, or mainline merge.
