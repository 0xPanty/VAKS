---
record_kind: sandbox_failure_case_oracle
slice_id: 2026-06-15-p1-5-16-misa-runtime-memory-vaks-bridge-sandbox
status: implemented_pending_review
truth_boundary: sandbox_oracle_only
---

# Failure Case Oracle

| Failure case | Primary expected code |
|---|---|
| `dependency-install-requested.json` | `MB_DEPENDENCY_INSTALL_FORBIDDEN` |
| `real-runtime-started.json` | `MB_REAL_RUNTIME_FORBIDDEN` |
| `hooks-enabled.json` | `MB_HOOKS_FORBIDDEN` |
| `background-service-enabled.json` | `MB_BACKGROUND_SERVICE_FORBIDDEN` |
| `mcp-write-tool-exposed.json` | `MB_MCP_WRITE_TOOL_FORBIDDEN` |
| `broad-mcp-save-tool.json` | `MB_BROAD_MCP_TOOL_FORBIDDEN` |
| `obsidian-sync-requested.json` | `MB_OBSIDIAN_SYNC_FORBIDDEN` |
| `write-path-outside-slice.json` | `MB_WRITE_PATH_OUTSIDE_SLICE` |
| `protected-write-path.json` | `MB_PROTECTED_PATH_TARGET` |
| `runtime-memory-not-quarantined.json` | `MB_RUNTIME_MEMORY_NOT_QUARANTINED` |
| `runtime-memory-direct-vaks-write.json` | `MB_RUNTIME_DIRECT_VAKS_WRITE_FORBIDDEN` |
| `runtime-memory-invalid-type.json` | `MB_MEMORY_TYPE_INVALID` |
| `runtime-type-not-allowed-by-manifest.json` | `MB_MEMORY_TYPE_NOT_ALLOWED_BY_MANIFEST` |
| `runtime-memory-missing-source-observation.json` | `MB_SOURCE_OBSERVATION_TRACE_MISSING` |
| `runtime-fixture-missing-source-observation.json` | `MB_SOURCE_OBSERVATION_TRACE_MISSING` |
| `runtime-memory-missing-fixture.json` | `MB_FIXTURE_PATH_MISSING` |
| `runtime-memory-entry-action-basis.json` | `MB_ACTION_BASIS_FORBIDDEN` |
| `runtime-memory-rank-as-truth.json` | `MB_AUTHORITY_CONFUSION` |
| `context-not-readonly.json` | `MB_CONTEXT_NOT_READ_ONLY` |
| `context-labels-missing.json` | `MB_CONTEXT_LABELS_MISSING` |
| `context-pack-refs-missing.json` | `MB_CONTEXT_PACK_REFS_MISSING` |
| `context-bucket-filter-missing.json` | `MB_BUCKET_FILTER_NOT_FIRST` |
| `context-cross-bucket-fusion.json` | `MB_CROSS_BUCKET_FUSION` |
| `context-candidate-as-support.json` | `MB_CONTEXT_HIT_AS_SUPPORT` |
| `context-support-anchor-missing.json` | `MB_SUPPORT_ANCHOR_MISSING` |
| `context-item-action-basis.json` | `MB_ACTION_BASIS_FORBIDDEN` |
| `context-selected-by-missing.json` | `MB_SELECTED_BY_MISSING` |
| `context-selected-by-as-authority.json` | `MB_AUTHORITY_CONFUSION` |
| `context-pack-missing-fixture.json` | `MB_FIXTURE_PATH_MISSING` |
| `context-pack-fixture-not-readonly.json` | `MB_CONTEXT_FIXTURE_NOT_READ_ONLY` |
| `context-pack-fixture-runtime-bucket.json` | `MB_CONTEXT_FIXTURE_BUCKET_MISMATCH` |
| `context-item-not-in-pack.json` | `MB_CONTEXT_ITEM_NOT_IN_PACK` |
| `writeback-reviewed-claim.json` | `MB_WRITEBACK_TYPE_FORBIDDEN` |
| `writeback-type-not-allowed-by-manifest.json` | `MB_WRITEBACK_TYPE_NOT_ALLOWED_BY_MANIFEST` |
| `writeback-feedback-truth-mutation.json` | `MB_FEEDBACK_TRUTH_MUTATION` |
| `writeback-fixture-truth-mutation.json` | `MB_FEEDBACK_TRUTH_MUTATION` |
| `writeback-candidate-promotes.json` | `MB_CANDIDATE_SIGNAL_PROMOTION` |
| `writeback-review-due-invalidates-truth.json` | `MB_REVIEW_DUE_INVALIDATES_TRUTH` |
| `writeback-memory-save-direct.json` | `MB_DIRECT_MEMORY_WRITEBACK_FORBIDDEN` |
| `writeback-record-direct-to-reviewed.json` | `MB_REVIEWED_WRITE_FORBIDDEN` |
| `writeback-receipt-missing.json` | `MB_FIXTURE_PATH_MISSING` |
| `receipt-writes-reviewed-layer.json` | `MB_RECEIPT_WRITES_REVIEWED` |
| `receipt-id-mismatch.json` | `MB_RECEIPT_ID_MISMATCH` |
| `receipt-type-not-allowed.json` | `MB_RECEIPT_TYPE_NOT_ALLOWED` |
| `action-receipt-writes-reviewed-layer.json` | `MB_RECEIPT_WRITES_REVIEWED` |
| `action-receipt-mismatch.json` | `MB_ACTION_RECEIPT_MISMATCH` |
| `action-ready-with-insufficient-support.json` | `MB_ACTION_READY_WITH_INSUFFICIENT_SUPPORT` |
| `action-runtime-memory-as-basis.json` | `MB_RUNTIME_MEMORY_AS_ACTION_BASIS` |
| `action-check-missing.json` | `MB_ACTION_READINESS_CHECK_REQUIRED` |
| `action-blockers-missing.json` | `MB_ACTION_BLOCKERS_MISSING` |
| `use-loop-trace-missing.json` | `MB_MISSING_USE_LOOP_TRACE` |
| `use-loop-trace-action-basis.json` | `MB_USE_LOOP_ACTION_BASIS` |
| `use-loop-trace-not-readonly.json` | `MB_USE_LOOP_NOT_READ_ONLY` |
| `use-loop-fixture-not-readonly.json` | `MB_USE_LOOP_NOT_READ_ONLY` |
| `use-loop-trace-tool-writes.json` | `MB_USE_LOOP_WRITES_FORBIDDEN` |
| `use-loop-trace-labels-missing.json` | `MB_USE_LOOP_LABELS_MISSING` |
| `boundary-reviewed-write-allowed.json` | `MB_REVIEWED_WRITE_FORBIDDEN` |
| `boundary-support-created.json` | `MB_SUPPORT_CREATION_FORBIDDEN` |
| `boundary-promotion-ready.json` | `MB_AUTHORITY_CONFUSION` |
| `direct-authority-claim.json` | `MB_AUTHORITY_CLAIM_FORBIDDEN` |
| `missing-runtime-memory-block.json` | `MB_MISSING_RUNTIME_MEMORY` |
| `missing-context-adapter-block.json` | `MB_MISSING_CONTEXT_ADAPTER` |
| `missing-writeback-block.json` | `MB_MISSING_WRITEBACK` |
| `missing-action-readiness-block.json` | `MB_MISSING_ACTION_READINESS` |
| `missing-boundary-block.json` | `MB_MISSING_BOUNDARY` |

Expected failures are sandbox validation results only. Passing this suite does
not approve production runtime, reviewed knowledge, evidence support, action
basis, promotion, sync, commit, push, or mainline merge.
