---
record_type: dev-context-pack
context_id:
project:
task:
scope_key:
created:
updated:
created_by:
status: active
mode: development
base_memory_policy: "Use base memory tiers as input signals, but this pack is task-specific."
activation_policy: "Core requires likely-next-use for this task; cold references are opened only for evidence/history/conflict."
verification_status: draft
---

# Dev Context Pack

## AI-readable preamble

This is a temporary development-mode context pack.

Use Core first. Expand to Support when needed. Check Risk before decisions or writes. Open Cold References only for evidence, history, or contradiction checks.

## Task

```text

```

## Project Gate

This pack is valid only if the current task has a concrete goal, next action, or stop condition.

Goal:

```text

```

Next action:

```text

```

Stop condition:

```text

```

## Scope

In scope:

```text

```

Out of scope:

```text

```

## Context Briefing

Low-token summary used to decide what to open in full.

| File | Summary | Why suggested | Suggested layer |
|---|---|---|---|
|  |  |  |  |

Briefing rule:

```text
Use the briefing to choose reads. Do not treat the briefing as evidence.
```

## Core

Files that must be read and obeyed for this task.

| File | Why core | Required use |
|---|---|---|
|  |  |  |

Core rule:

```text
A file is Core only when the current task cannot safely proceed without it.
```

## Support

Relevant background to expand when design or implementation choices appear.

| File | Why support | When to open |
|---|---|---|
|  |  |  |

## Risk

Anti-patterns, negative evidence, contradictions, and do-not-build-first constraints.

| File | Risk | Checkpoint |
|---|---|---|
|  |  |  |

Risk rule:

```text
Check Risk before decisions, writes, or scope expansion.
```

## Cold References

Traceable sources and historical records. Do not load by default.

| File | Why retained | Open when |
|---|---|---|
|  |  |  |

Cold rule:

```text
Cold can be relevant without being loaded. Open it only for source evidence, history, or contradiction checks.
```

## Open Questions

-

## Stop Conditions

Stop or refresh this pack when:

-

## Writeback Targets

If the task produces durable knowledge, update:

-

## Exit Notes

At completion, record:

```text
What changed:
What should stay hot:
What cools to warm:
What returns to cold:
Follow-up:
```

## Closeout Scan

Before archiving this pack, decide:

```text
Reusable pattern / decision / implementation note:
One-off evidence returning to cold:
New risk or anti-pattern:
Missing source or review work:
Session/fix capture needed:
```
