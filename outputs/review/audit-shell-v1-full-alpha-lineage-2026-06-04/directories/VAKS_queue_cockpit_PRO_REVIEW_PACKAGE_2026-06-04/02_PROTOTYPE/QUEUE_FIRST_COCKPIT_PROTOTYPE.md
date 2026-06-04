# Queue-First Operator Cockpit Prototype

## One Sentence

Audit shell v1 should become a backstage queue cockpit, not a stack of cards.

## Three Layers

### 1. Queue Layer

The first screen answers:

```text
who needs attention now
why
what is the next action
```

Prototype lanes:

| Lane | Count | Meaning |
|---|---:|---|
| `01_blocking_now` | 11 | Cannot act until anchor/evidence/package problem is fixed. |
| `02_regressed_reopen` | 2 | Old/recovery surface may mislead current work; reopen. |
| `03_review_now` | 30 | Review before answer/action/rule use. |
| `04_deferred_review_unless_promoted` | 109 | Keep out of main unresolved queue unless cited, promoted, challenged, or used for action. |
| `04_ordinary_light` | 113 | Light path. |
| `05_folded_history` | 17 | Historical/resolved, folded by default. |

The main unresolved queue is only:

```text
01_blocking_now
02_regressed_reopen
03_review_now
```

That gives 43 first-screen rows instead of throwing all 152 thick-path rows at the operator.

### 2. Issue Shell Row / Pane

Each row needs a short shell:

```text
state
lane
risk reason
anchor-strength strip
first action
targeted boundary reminder
jump-back handles
```

This is the card renderer's place. It is not the architecture center.

### 3. Deep Packet / Full Audit

Open only when crossing a threshold:

```text
action basis
rule / schema / convention basis
explicit challenge
conflict
missing anchor
blocking
regression
high-risk current answer
```

Deep packet should contain:

```text
point
source / record / evidence handles
selector-grade anchor
negative evidence / omission note
time/version context
why evidence is sufficient or insufficient
```

## Anchor-Strength Strip

Human front face should not show the full landing taxonomy by default.

Use four visible levels:

| Strip | Meaning |
|---|---|
| `1_precise_evidence_anchor` | Exact evidence landing. |
| `2_precise_text_unreviewed` | Exact text landing, not yet reviewed as evidence. |
| `3_source_claim_context_only` | Source, claim, or context landing only. |
| `4_diagnostic_history_binary_or_weak` | Diagnostic, history, binary, package, template, or flat transcript landing. |

The full landing class remains in machine/drilldown data.

Current prototype distribution:

```text
2_precise_text_unreviewed: 4
3_source_claim_context_only: 213
4_diagnostic_history_binary_or_weak: 65
```

Important design signal: this pressure set has no `1_precise_evidence_anchor` rows. The click-back pilot must include or create exact evidence-anchor cases before claiming product-grade evidence jump-back.

## Deferred Review Lane

This is the main Pro-driven change.

`for_review` should not always mean "open full audit now".

Split:

```text
review_now
review_later_unless_promoted
```

Examples that can usually defer:

- derived QA / summary,
- draft pattern not currently being used,
- stale next_review not being used for current action,
- count/lineage risk not currently used as support,
- dashboard/test/lint diagnostic note,
- timestamped ASR segment not yet promoted.

Upgrade immediately if:

```text
used in answer
used for action
used for rule/convention
explicitly challenged
conflicts with another record
missing anchor affects current work
```

## Recurrence / Grouping

Still default off.

If tested later, treat it as:

```text
conditional queue compressor
not evidence aid
not truth aid
```

Break out automatically for:

```text
serious risk
conflict
challenge
missing anchor
regression
action basis
different landing strength
different risk reason
```

## What This Lands

This prototype lands Pro's key correction:

```text
keep capability
shrink first-screen burden
move from card-first to queue-first
```

