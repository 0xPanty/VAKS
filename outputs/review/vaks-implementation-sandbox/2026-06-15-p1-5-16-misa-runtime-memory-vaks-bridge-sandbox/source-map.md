---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p1-5-16-misa-runtime-memory-vaks-bridge-sandbox
status: implemented_pending_review
truth_boundary: sandbox_trace_only
---

# Source Map

## Project Rules Used

| Source | Rule used |
|---|---|
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 1622-1624 | agentmemory is useful for MISA runtime continuity and VAKS context access, not as VAKS truth layer. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 1652-1665 | Safe split: MISA runtime memory, read-only VAKS context adapter, writeback only as feedback_event/candidate_signal/review_due. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 1707-1717 | Forbidden imports: runtime memory as truth, memory_save/on_memory_write direct writeback, broad MCP tools, unlabeled context injection. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 1719-1748 | Minimal sandbox test and pass conditions for MISA memory/VAKS bridge. |
| `FEEDBACK.md` lines 65-121 | Feedback can affect usefulness/scope/activation/review_due, not truth confidence or verification status. |
| `FEEDBACK.md` lines 633-638 | Agent/MCP memory writes may create candidate or feedback-event records, not reviewed truth or promotion. |
| `SOURCE_INTAKE.md` lines 212-222 | Raw/candidate/overlay/feedback to reviewed/decision/action-basis requires explicit human review. |
| `SOURCE_INTAKE.md` lines 740-847 | Retrieval/context packs must bucket-filter first; selected_by is trace metadata; static checks are not enough for action basis. |
| `DEV_CONTEXT.md` lines 302-310 | Retrieval receipts/context packs are not action basis by themselves. |

## Artifact Mapping

| Requirement | Artifact coverage |
|---|---|
| Runtime memory quarantine | `fixtures/valid-runtime-memory-quarantine.json`, `failure-cases/runtime-memory-not-quarantined.json` |
| No install/runtime/hooks/background/MCP/sync | `failure-cases/dependency-install-requested.json`, `real-runtime-started.json`, `hooks-enabled.json`, `background-service-enabled.json`, `mcp-write-tool-exposed.json`, `broad-mcp-save-tool.json`, `obsidian-sync-requested.json` |
| Runtime memory provenance | `fixtures/runtime/session-observation.json`, `failure-cases/runtime-memory-missing-source-observation.json` |
| Runtime fixture content cross-check | `failure-cases/runtime-fixture-missing-source-observation.json`, `failure-cases/runtime-type-not-allowed-by-manifest.json` |
| No runtime memory authority | `failure-cases/runtime-memory-direct-vaks-write.json`, `runtime-memory-entry-action-basis.json`, `runtime-memory-rank-as-truth.json` |
| Read-only VAKS context adapter | `fixtures/valid-readonly-context-pack-fetch.json`, `failure-cases/context-not-readonly.json` |
| Bucket and label boundaries | `failure-cases/context-labels-missing.json`, `context-bucket-filter-missing.json`, `context-cross-bucket-fusion.json`, `context-selected-by-missing.json` |
| Context-pack fixture content and item identity cross-check | `failure-cases/context-pack-refs-missing.json`, `failure-cases/context-pack-fixture-not-readonly.json`, `failure-cases/context-pack-fixture-runtime-bucket.json`, `failure-cases/context-item-not-in-pack.json` |
| Candidate/runtime context cannot support/action | `failure-cases/context-candidate-as-support.json`, `context-item-action-basis.json`, `context-support-anchor-missing.json` |
| Receipt-bound writeback | `fixtures/receipts/bridge-operation-receipt.json`, `failure-cases/writeback-receipt-missing.json` |
| Receipt id/type binding | `failure-cases/receipt-id-mismatch.json`, `failure-cases/receipt-type-not-allowed.json`, `failure-cases/receipt-writes-reviewed-layer.json`, `failure-cases/action-receipt-mismatch.json`, `failure-cases/action-receipt-writes-reviewed-layer.json` |
| Only feedback/candidate/review_due writeback | `fixtures/valid-feedback-candidate-review-due-writeback.json`, `failure-cases/writeback-reviewed-claim.json` |
| Feedback/candidate/review_due are not truth/promotion | `failure-cases/writeback-feedback-truth-mutation.json`, `writeback-fixture-truth-mutation.json`, `writeback-candidate-promotes.json`, `writeback-review-due-invalidates-truth.json` |
| Action readiness remains VAKS-gated | `fixtures/valid-action-readiness-block.json`, `failure-cases/action-ready-with-insufficient-support.json`, `action-runtime-memory-as-basis.json`, `action-check-missing.json` |
| Read-only use-loop trace | `fixtures/use-loop/read-only-bridge-trace.json`, `failure-cases/use-loop-trace-missing.json`, `failure-cases/use-loop-trace-action-basis.json`, `failure-cases/use-loop-trace-not-readonly.json`, `failure-cases/use-loop-fixture-not-readonly.json`, `failure-cases/use-loop-trace-tool-writes.json`, `failure-cases/use-loop-trace-labels-missing.json` |
| Protected path and slice write scope | `failure-cases/write-path-outside-slice.json`, `protected-write-path.json` |
| Direct authority fields are forbidden | `failure-cases/direct-authority-claim.json`, `boundary-reviewed-write-allowed.json`, `boundary-support-created.json`, `boundary-promotion-ready.json` |

## Boundaries

- No real MISA, Hermes, agentmemory, MCP, hooks, background service, or sync is
  started.
- No dependency is installed.
- No VAKS reviewed layer, protected path, raw source, template, tool, or
  Obsidian vault path is written.
- No evidence support, reviewed knowledge, reviewed relation, action basis,
  schema governance, promotion, commit, push, or mainline readiness is created.
