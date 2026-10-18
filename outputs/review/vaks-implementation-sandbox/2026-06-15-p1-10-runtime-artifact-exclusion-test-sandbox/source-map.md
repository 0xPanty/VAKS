---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox
status: implemented_pending_review
truth_boundary: sandbox_source_map_only
---

# Source Map

## Governing User Boundary

- Writes are restricted to this sandbox path.
- Protected paths and Obsidian vault remain untouched.
- No commit, push, Obsidian sync, long-running automation, background service,
  MCP write tool, hook, or dependency install.
- Current dirty tree is pre-existing baseline; final audit checks only this
  slice's write path.

## Local Project Sources Read

| Source | Used For |
|---|---|
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md:2273-2287` | P1 target and `runtime artifact exclusion test` artifact. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p1-09-read-only-query-loop-pilot-sandbox/product-acceptance-report.md` | Confirms P1-09 `PASS_PRODUCT_GRADE` and P1-10 entry. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p1-09-read-only-query-loop-pilot-sandbox/next-step.md` | Recommends reusing P1-09 scenario shape for runtime artifact exclusion tests. |
| `SOURCE_INTAKE.md` | Retrieval rank not trust; runtime/default adoption not approved by adapter; archived/derived items excluded by default; action-facing support requires stable source anchors. |
| `DEV_CONTEXT.md` | Runtime tools/caches help agents find work but do not replace verified-action promotion; retrieval receipts/context packs are not action basis. |
| `REFERENCE_REVIEW_PROTOCOL.md` | Retrieval/cache/API/MCP/viewer layers are derived layers, not truth sources. |
| `REVIEW_QUEUE.md` | No automatic support/confidence/promotion from similarity, graph traversal, evaluator output, or automation. |
| `FEEDBACK.md` | Rebuildable caches and feedback outputs cannot mutate truth. |

## Implemented Boundary

Runtime artifacts include:

- Python bytecode and cache folders;
- test/suite/verifier output;
- execution logs;
- temporary/generated receipts;
- scratch files and temporary downloads;
- lock files;
- runtime caches and derived indexes;
- benchmark output and transient state.

They may be retained as process/debug traces, but when they are visible to a
retrieval scan they must be excluded with:

```text
excluded_reason: runtime_artifact_excluded
```

They cannot be selected, evidence support, reviewed/raw/support authority,
action basis, reviewer approval, reviewed knowledge, promotion, or mainline
readiness.

## Durable Non-Runtime Boundary

Durable sandbox documentation such as contracts, source maps, verification docs,
fixtures, and failure cases is not automatically treated as runtime artifact.
Those files remain sandbox artifacts, not reviewed knowledge or action basis.

## Non-Authority Note

This source map explains the sandbox prototype. It is not reviewed knowledge,
evidence support, reviewer approval, action basis, or a mainline implementation
decision.
