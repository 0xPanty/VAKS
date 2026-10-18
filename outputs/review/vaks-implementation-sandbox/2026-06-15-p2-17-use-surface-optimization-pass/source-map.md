---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p2-17-use-surface-optimization-pass
status: implemented_pending_review
truth_boundary: sandbox_trace_only
---

# Source Map

## Project Rules Used

| Source | Rule used |
|---|---|
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2300-2304 | P2 target is making the strict system usable without weakening it. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2322-2329 | Rough spots: manual reading, long docs, raw `rg` retrieval, dirty worktree caution, sync/hash procedure, unclear user entry paths. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2341-2356 | Optimization principle: make strictness visible, navigable, low-friction; one entry surface, status pages, receipt-backed search, badges, worktree/sync health, safe defaults. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2358-2367 | Acceptance questions: where to put it, state, use scope, blockers, source/hash/receipt proof. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2371-2388 | Bases and product entries are visibility/entry surfaces, not approval/truth authority. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2397-2411 | Product candidates and boundaries: explanation only, raw/candidate only, cannot approve, status only, navigation not authority, dirty state does not judge knowledge. |
| `DEV_CONTEXT.md` lines 302-310 | Context packs and retrieval receipts are not action basis by themselves. |
| `FEEDBACK.md` lines 65-121 | Feedback affects usefulness, scope, activation, and review pressure, not truth. |
| `SOURCE_INTAKE.md` lines 740-847 | Retrieval/context selection metadata is trace information; action-facing use needs support and readiness checks. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p1-5-16-misa-runtime-memory-vaks-bridge-sandbox/product-acceptance-report.md` | P1.5-16 passed product acceptance and can hand off to P2-17, but remains sandbox-only. |

## Artifact Mapping

| Requirement | Artifact coverage |
|---|---|
| One entry surface | `prototype/operator-use-surface-blueprint.json`, `fixtures/valid-entry-surface-map.json`; verifier validates both the copied prototype and positive fixtures |
| User can answer where to put content | `fixtures/valid-operator-use-surface.json` `user_questions.where_put_this` |
| User can answer current state | `fixtures/valid-status-navigation.json` status surfaces and layer badges |
| User can answer orientation/review/action scope | `fixtures/valid-operator-use-surface.json` `user_questions.orientation_review_or_action` |
| User can see blockers | `fixtures/valid-status-navigation.json` blocked/stale/missing-anchor/hash/action-not-ready states |
| Source/hash/receipt integrity visible | `fixtures/valid-receipt-backed-search.json`, `fixtures/valid-dirty-state-guardrail.json` |
| Receipt-backed search, not raw trust | `failure-cases/search-receipt-missing.json`, `selected-by-as-support.json`, `raw-topk-trust.json` |
| Entry buttons cannot approve or mutate truth | `failure-cases/entry-approves-reviewed.json`, `entry-reviewed-write.json`, `entry-promotes.json` |
| Badges cannot promote | `failure-cases/badge-promotes.json` |
| Dirty/hash/sync are operator state only | `failure-cases/dirty-state-as-truth.json`, `hash-as-support.json`, `sync-without-operation-receipt.json` |
| Action-adjacent surface remains gated | `failure-cases/action-mode-gate-missing.json`, `context-pack-as-action-basis.json` |
| Protected path and sandbox write scope | `failure-cases/write-path-outside-slice.json`, `protected-path-write.json`, `obsidian-path-case-bypass.json` |
| No real UI/runtime/hooks/background/automation | `failure-cases/runtime-or-sync-forbidden.json`, `real-ui-started.json`, `background-service-started.json`, `hook-enabled.json`, `automation-started.json` |

## Boundaries

- This slice is a product-surface contract and validator, not a deployed UI.
- The prototype is a copied JSON blueprint only.
- No real Bases file, Obsidian vault, template, tool, reviewed claim, reviewed
  pattern, decision, sync, commit, push, server, MCP tool, or automation is
  created.
- Status, badges, receipts, search results, dirty state, hash matches, and
  dashboard visibility are not truth, evidence support, reviewer approval,
  action basis, promotion, or mainline readiness.
