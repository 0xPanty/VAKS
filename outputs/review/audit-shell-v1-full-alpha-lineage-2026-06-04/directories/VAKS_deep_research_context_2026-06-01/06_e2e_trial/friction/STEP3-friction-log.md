---
record_type: friction-log
status: active
created: 2026-06-01
step: 3
scope: context-pack-real-question
---

# Step 3 Friction Log: Real Question

## Flow Completed

```text
reviewed claims + source records
-> context pack
-> real question
-> coverage_map
-> evidence_sufficiency
-> query-run record
```

## Field Pain

| Question | Observation |
|---|---|
| Which field could not be filled without guessing? | `checked_for: action_basis` was semantically awkward because the question was about action-basis policy, not a concrete action. |
| Which gate felt too heavy? | `coverage_map` is useful but slow; seven rows for one simple answer felt like a lot. |
| Where did it get stuck? | The key answer depended partly on VAKS local rules and partly on external papers. Coverage status had no clean "local rule plus external support" label. |
| Which rule looked good but was hard to execute? | `required_next_step` options are too coarse. `needs_review` does not explain whether we need full paper review, more diverse sources, or an operational trial. |

## Lazy-Gate Check

This was a decision-like question, so `coverage_map` and `evidence_sufficiency` were appropriate.

But if every design answer needs full coverage rows, ordinary architecture discussion would become heavy.

## Pain Classification

- Too heavy: full coverage_map for one answer.
- Missing: coverage status for "local architecture rule supported by outside sources."
- Ambiguous: action_basis policy vs concrete action_basis.
- Not stuck: The pack could answer cautiously.

