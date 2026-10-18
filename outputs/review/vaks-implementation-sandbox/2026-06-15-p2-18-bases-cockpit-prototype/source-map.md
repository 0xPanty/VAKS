---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p2-18-bases-cockpit-prototype
status: implemented_pending_review
truth_boundary: sandbox_trace_only
---

# Source Map

## Project Rules Used

| Source | Rule used |
|---|---|
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2369-2377 | Planned Bases surfaces: review candidates, context packs, feedback events, operator cockpit; each has explicit purpose, columns, and boundary. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2378-2388 | Product entries map to backend artifacts and boundaries. |
| `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md` lines 2397-2411 | Product surfaces explain, navigate, show state, and guard actions; they cannot approve, mutate truth, or imply trust/action readiness. |
| `outputs/review/vaks-implementation-sandbox/2026-06-15-p2-17-use-surface-optimization-pass/product-acceptance-report.md` | P2-17 passed product acceptance and can hand off to P2-18; product surfaces remain non-authoritative. |
| `DEV_CONTEXT.md` lines 302-310 | Context packs and retrieval receipts are not action basis by themselves. |
| `FEEDBACK.md` lines 65-121 | Feedback affects usefulness, scope, activation, and review pressure, not truth. |
| `SOURCE_INTAKE.md` lines 740-847 | Retrieval/context selection metadata is trace information; action-facing use needs support and readiness checks. |

## Artifact Mapping

| Requirement | Artifact coverage |
|---|---|
| Review candidates cockpit | `fixtures/valid-review-candidates-base.json`, `failure-cases/review-candidates-approves.json` |
| Context packs cockpit | `fixtures/valid-context-packs-base.json`, `failure-cases/context-packs-infer-ready.json` |
| Feedback events cockpit | `fixtures/valid-feedback-events-base.json`, `failure-cases/feedback-mutates-truth.json` |
| Operator cockpit | `fixtures/valid-operator-cockpit-base.json`, `failure-cases/operator-replaces-validators.json` |
| Cross-cockpit navigation | `fixtures/valid-cross-cockpit-navigation.json`, `failure-cases/navigation-creates-authority.json` |
| Prototype validated | `prototype/bases-cockpit-prototype.json`; verifier includes `prototype/*.json` |
| Key columns present | `failure-cases/base-missing-key-column.json`, `failure-cases/operator-missing-status-flag.json` |
| No authority confusion | `failure-cases/reviewed-write-enabled.json`, `promotion-enabled.json`, `action-basis-enabled.json` |
| Dirty/hash/activity are operator state only | `failure-cases/dirty-state-judges-knowledge.json`, `hash-match-as-support.json`, `activity-as-confidence.json` |
| Real Bases/runtime/sync forbidden | `failure-cases/real-base-file-created.json`, `obsidian-sync-enabled.json`, `runtime-started.json`, `mcp-write-tool.json` |
| Protected path and sandbox write scope | `failure-cases/write-path-outside-slice.json`, `protected-path-base.json`, `obsidian-case-protected-path.json` |

## Boundaries

- This slice is a copied JSON cockpit prototype and validator only.
- No real `.base` files, Obsidian vault files, templates, tools, raw records,
  reviewed claims, reviewed patterns, decisions, sync, commit, push, server,
  MCP tool, automation, hook, or watcher is created.
- Cockpit rows, filters, badges, columns, warnings, counts, dirty state, hash
  state, and navigation links are not truth, evidence support, reviewer
  approval, action basis, promotion, or mainline readiness.
