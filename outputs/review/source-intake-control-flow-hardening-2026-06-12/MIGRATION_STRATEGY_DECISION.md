---
type: source_intake_migration_strategy_decision
status: conservative_plus_safe_middle
created_at: 2026-06-13
scope: Source Intake warning cleanup and migration strategy
truth_boundary: migration strategy only; not Source Intake P0 approval
---

# Migration Strategy Decision

## Plain Verdict

Do not aggressively clear all warnings.

The chosen path is:

```text
conservative red-zone cleanup
+ safe middle-mode isolation / downgrading
+ explicit runtime-test backlog
- no invented semantics
- no automatic P0 pass
```

This means true red zones are cleared or blocked, but low-confidence historical
or placeholder debt stays visible until a human review or runtime test justifies
further cleanup.

## Strategy Comparison

| Mode | How it works | Expected effort | Risk | Judgment |
|---|---|---:|---|---|
| Conservative mode | Keep most warnings; only upgrade canonical overlay placeholders, raw top-level `relations`, and raw top-level `confidence`. | 1-2 days | Medium | Best first step. Clears true red zones without inventing semantics. |
| Middle mode | Conservative mode plus legacy lens exclusion/migration and downgrading other authority-like raw fields. | 3-5 days | Low to medium | Good P0.5-style hardening if the team wants a stronger static boundary. |
| Aggressive mode | Try to clear nearly all warnings, including filling the remaining `why_saved` placeholders one by one. | 1-2+ weeks | High | Not recommended. It can create fake certainty and invented source intent. |

## Current Package Position

Current package state is best described as:

```text
static strategy: conservative_plus_safe_middle
runtime strategy: not_run
canonical P0: not_passed
```

Already done:

- canonical confirmed-overlay placeholders are hard errors;
- raw source top-level `relations` is a hard error;
- raw source top-level `confidence` is a hard error;
- `pack_allowed` uses a single string enum, no boolean/string false dual encoding;
- persistent `overlay_state` excludes `suggested`;
- `graph_neighbor` is not a Source Intake core `record_kind`;
- `promotion_gate` no longer carries review results such as `review_passed`;
- legacy Project Lens files are excluded into `_legacy_project_lens`;
- soft raw source authority-like fields are moved to `legacy_raw_metadata`;
- `legacy_raw_metadata` is audit-only and must be ignored by retrieval/graph/pack/support compilers;
- `why_saved` placeholders are only defer-ok when the body contains a real capture/save reason.

Intentionally not done:

- the remaining 118 defer-ok `why_saved` migration warnings are not auto-filled;
- the 4 missing-reason raw source cards are not auto-rewritten;
- runtime answer-loop / graph / feedback / anchor tests are not claimed as passed.

## Why Not Aggressive

Aggressively clearing warning counts would make the dashboard cleaner, but it
would also push the system toward fabricated semantics:

- inventing why a source was saved;
- converting old project lens fragments into canonical overlays without real
  project-local scope;
- treating historical triage numbers as if they had current authority;
- confusing "lint passed" with "runtime behavior is safe."

For VAKS, visible debt is safer than fake cleanliness.

## Next Gate

The next meaningful gate is not "zero warnings." It is:

1. a small human migration replay on representative files;
2. a read-only answer-loop pilot with receipts;
3. graph/compiler quarantine test;
4. feedback scope aggregation test;
5. anchor freshness replay.

These are tracked in `MINIMUM_TEST_CASES.md` and `RUNTIME_RISK_MATRIX.md`.
