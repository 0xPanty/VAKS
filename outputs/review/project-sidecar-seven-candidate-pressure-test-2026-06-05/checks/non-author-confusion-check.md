---
type: sandbox_check
status: completed
created_at: 2026-06-05
scope: non-author-confusion-simulation
truth_boundary: test report only; not reviewed knowledge; not action basis
---

# Non-Author Confusion Check

## Method

Simulated a strict non-author reader who sees short snippets from the sandbox
and must classify them as:

```text
overlay
candidate snapshot
archive/tombstone
decision / ADR
action basis
```

This is a wording pressure test, not a human study.

## Classification Samples

| Sample | Expected | Confusion risk | Score |
|---|---|---:|---:|
| `stance: partial` with `borrow_scope` | overlay | may sound like adoption if `partial` is read casually | 2/3 |
| `candidate experience snapshot` | candidate snapshot | may sound like best practice if `candidate` is omitted | 2/3 |
| `candidate boundary snapshot` | candidate snapshot | may sound like universal ban if trigger/scope omitted | 2/3 |
| `delete+tombstone` | archive/tombstone | clear if semantic retrieval exclusion is visible | 3/3 |
| `carry-forward / reopen` | operation | may sound like durable state if written in status field | 2/3 |
| `supersede / withdraw` | operation/snapshot chain | overlaps with existing decision superseding vocabulary | 2/3 |
| `default retrieval precedence` | retrieval inclusion order | clearer than priority, but still needs "not confidence" warning | 3/3 |
| action-facing escalation envelope | action-basis gate | clear because it explicitly says Lens alone insufficient | 3/3 |

## Aggregate

```text
total_score: 19 / 24
confusion_rate_estimate: 5 / 8 samples still need wording guardrails
```

## Findings

The wording is usable in sandbox, but too fragile for mainline object-model
promotion.

Most confusion disappears only when each artifact repeats a `truth_boundary`.
That is acceptable for `outputs/review`, but too much ceremony for the main
architecture spine.

## Recommended Guardrails

- Keep `candidate` in snapshot names.
- Do not write `landed`, `accepted`, `rejected`, or `approved` as live stance.
- Use `default retrieval precedence`, not `retrieval priority`.
- Treat carry-forward and supersede as actions, not status values.
- Keep action-facing warrant outside the sidecar overlay.
