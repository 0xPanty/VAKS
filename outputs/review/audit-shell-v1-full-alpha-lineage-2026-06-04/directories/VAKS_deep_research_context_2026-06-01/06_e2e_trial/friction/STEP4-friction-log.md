---
record_type: friction-log
status: active
created: 2026-06-01
step: 4
scope: feedback-loop
---

# Step 4 Friction Log: Feedback Loop

## Flow Completed

```text
feedback-event
-> similar query
-> changed activation / scope-fit
-> query-run record
```

## Field Pain

| Question | Observation |
|---|---|
| Which field could not be filled without guessing? | `signal_strength` and `signal_confidence` are numerical but this manual trial had no calibration scale. Values felt made up. |
| Which gate felt too heavy? | Feedback-event frontmatter is long for a simple "answer was too broad" signal. |
| Where did it get stuck? | There is no mechanical activation engine, so "activation changed" had to be recorded as a manual comparison between Q1 and Q2. |
| Which rule looked good but was hard to execute? | "Feedback improves activation / scope fit" is conceptually right, but without runtime it is only a written intention unless query-run records make the before/after explicit. |

## Lazy-Gate Check

The feedback loop did not change truth confidence or source reliability.

But recording feedback manually is heavy enough that it will not happen for ordinary lightweight interactions unless the template is compressed.

## Pain Classification

- Too heavy: feedback-event metadata for a small scope-fit correction.
- Missing: calibration guide for numeric feedback deltas.
- Ambiguous: manual activation change vs actual activation engine behavior.
- Not stuck: The before/after query records made the change inspectable.

