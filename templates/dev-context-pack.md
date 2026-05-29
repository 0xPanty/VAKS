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

## Coverage Map

Use this only for key judgments in the answer or action basis. Do not turn the pack into a full audit report.
Every pack should be coverage-aware, but ordinary use can keep only the overview plus high-risk, challenged, or missing-evidence items.
Expand full `coverage_map` detail only for decisions, action basis, agent context packs, high-impact answers, explicit audit requests, or challenged answers.

```yaml
coverage_overview:
  supported:
  weakly_supported:
  challenged:
  missing_evidence:
  out_of_scope:
  risk_flags:

coverage_map:
  - point:
    point_type:
    coverage_status: supported | weakly_supported | challenged | missing_evidence | out_of_scope | not_verifiable
    support_refs:
    challenge_refs:
    risk_refs:
    critical_omissions:
    note:

action_readiness:
  state: ready | not_ready | risky | needs_review
  reason:
```

Coverage rule:

```text
Citations are not enough.
Coverage status does not change truth confidence.
Coverage can consume evidence_support, but background_context cannot count as supported.
Risk flags are only overview signals; concrete risks stay in risk_refs and action_readiness.
Critical omissions are known major omissions only, not a full omission scan.
```

## Evidence Sufficiency Gate

Use this only before action basis, decision, promotion, strong reviewed relation, risk_sensitive_answer, or when the user asks whether evidence is enough.
Run it after the draft evidence/context envelope is assembled, before marking the pack action-ready.

```yaml
evidence_sufficiency:
  state: sufficient | weak | insufficient | out_of_scope | risky
  checked_for: context_pack | action_basis | decision | promotion | reviewed_relation | risk_sensitive_answer
  missing:
    -
  required_next_step: proceed | ask_user | retrieve_more | create_missing_point | narrow_scope | mark_not_actionable | needs_review
  reviewer_note:
```

Gate rule:

```text
Ordinary capture and ordinary query do not trigger this gate.
If evidence is insufficient, do not output a ready action basis.
If evidence is weak, expose gaps and weak support.
If evidence is out of scope, show the scope mismatch.
If evidence is out of scope only for the broad request, narrow_scope may be the right next step.
If evidence is risky, set action_readiness to risky or needs_review.
retrieve_more is a recommendation unless the user explicitly authorizes retrieval.
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
