# Pro Report Summary And Next Steps

Status:

```text
summary of product-grade audit shell advice
sandbox-planning only
no main-vault writeback
no SCHEMA change
```

## Plain-Language Verdict

The Pro report is useful. Its main value is that it moves VAKS from "make each record shorter" to "build a unified audit shell and queue/history compression layer."

The correct direction is:

```text
default light
conditionally thick
raw anchors always jump-backable
unresolved items visible first
resolved / repeated / nonblocking history folded or grouped
```

The report should not be used as permission to add four new permanent templates or a new truth layer.

## What The Report Actually Adds

### 1. The four alphas should be merged into one audit shell

Do not keep these as four isolated record families:

```text
compact evidence card
compact coverage card
support/refine cluster
categorical feedback stub
```

Instead, treat them as four front-face views inside one shell grammar:

```text
small reviewed claim -> compact evidence face
ordinary answer / query-run -> compact coverage face
support/refine collision -> unresolved cluster face
ordinary feedback -> categorical feedback event inside grouped thread
```

### 2. Product-level noise reduction comes from queue/history compression

The first sandbox test mainly compressed single records:

```text
24 cases
24/24 pass
overall saved 27.4%
ordinary-case saved 42.4%
false-lite 0
ordinary false positives 0
```

To approach product-grade 60%-80% reduction, the next gain must come from:

```text
unresolved-first queue
resolved folding
repeated-event grouping
feedback threads
nonblocking linked stubs
regressed reopen
metadata stub / compact front face
```

This means the main screen should show what still needs action, not every historical trail.

### 3. Quality is protected by hard thickening triggers

The shell is safe only if these triggers always thicken:

```text
action-basis
promotion
explicit challenge
conflict
regression
known omission
missing anchor
risk-sensitive answer
explicit correction
high-severity wrong answer
decision / action outcome review
```

Serious false-lite must remain zero.

### 4. Feedback should be categorical, not fake-precise

Ordinary feedback should not rely on uncalibrated numbers such as:

```text
activation_delta
scope_fit_delta
outcome_score
```

Use:

```text
feedback type
short reason
next activate
next avoid
recurrence
regressed / resolved
no truth change
```

### 5. Lineage helps review, but cannot prove independence

Sparse provenance and lineage pointers are useful:

```text
source anchor
source access
wasDerivedFrom / primary-source-style pointer
jump-back pointer
```

But:

```text
lineage is not source independence
group count is not support strength
source count is not independence
cluster membership is not truth
```

## Proposed Audit Shell V1 Shape

This is a view / wording / queue convention, not a schema rewrite.

### Front Face

Keep the front face short. Target:

```text
4 to 6 visible lines
```

Recommended front fields:

```text
state
core summary
anchor / jump-back
open gap or scope limit
upgrade trigger or why-not-full-audit
```

Avoid making these mandatory on every record:

```text
authority_boundary repeated per record
all provenance details
all history
all grouped events
all source contributions
```

### Expandable Back

Use for:

```text
full anchor text/span
counterevidence
known omission
conflict note
source contributions
grouped exemplars
history pointers
```

### Full Audit

Use existing heavy review surfaces. Open only when strict triggers require it:

```text
full evidence packet
full coverage map
full feedback event / review_due
full collision review
```

## Object Defaults

| Object | Default Front View | Must Thicken When |
| --- | --- | --- |
| Small reviewed claim | compact evidence face | action-basis, promotion, explicit challenge, conflict, known omission, missing anchor, high-risk use |
| Ordinary answer / query-run | compact coverage face | action-basis, risk-sensitive answer, explicit trust challenge, important omission, multi-source conflict, regression |
| Support/refine collision | unresolved cluster face | conflict, independence needed for confidence, action-basis, explicit challenge, reviewer blocks |
| Ordinary feedback | grouped categorical feedback event | explicit correction, action outcome, decision outcome, regression, missed contradiction, high-severity wrong answer |

## Product-Grade Test Plan

The Pro report proposes a 640-sample paired baseline-vs-shell test. This is a good product blueprint, but too heavy as the immediate next step.

Recommended staged path:

```text
Stage 1: 80-120 sample pilot
Stage 2: 300 sample medium test
Stage 3: 640+ product gate test
```

### Stage 1 Pilot

Use a mixed set:

```text
SciFact: small claims / evidence card
AVeriTeC: coverage, sufficiency, web evidence
AmbiFC: ambiguity, over-grouping risk
FEVER: volume, ordinary false positives
Full source anchors: messy sources and jump-back proof
Derived replay harness: repeated feedback, resolved/regressed, support-refine recurrence
```

The pilot should test the shell, not only claim correctness.

## Pilot Gates

Use these softer gates for the first shell pilot:

```text
serious false-lite = 0
serious anchor retention = 100%
ordinary record reduction >= 50%
ordinary false-positive <= 5%
over-grouping serious mismatch = 0
review_due precision >= 0.80
front face target <= 6 visible lines
```

## Product Gates

Use these only after the shell design is stable:

```text
ordinary record reduction >= 60%, target 70%-80%
repeated feedback grouping reduction >= 70%, target >= 80%
resolved folding reduction >= 80%, target >= 90%
serious false-lite = 0
ordinary false-positive <= 2%, target <= 1%
serious anchor retention = 100%
overall anchor retention >= 99.5%, target 100%
review_due precision >= 0.90, target >= 0.95
review_due recall >= 0.95
over-grouping risk <= 1%, target 0
full audit trigger recall on serious set = 100%
ordinary-stratum full audit trigger rate <= 15%, target <= 10%
ordinary median human review time down >= 40%, target >= 50%
serious p95 review time not worse by more than 10%
```

## Anti-Patterns To Exclude

Keep these out of VAKS:

```text
compact shell as authority layer
grouping as evidence strength
group count as source independence
lineage as independence proof
resolved/outdated as actually resolved
silent sampling of abnormal runs
uncalibrated numeric deltas as precision
dashboard/retrieval/tests/LLM summaries as truth shortcut
```

## What To Verify Next

Do not open a broad literature lane. Verify only the mechanisms needed for shell v1:

```text
GRADE / ATRS:
  layered summary vs detail wording and upgrade boundary

GitHub / GitLab / Sentry:
  unresolved-first queue, resolved folding, regressed reopen

Kubernetes / OpenTelemetry:
  metadata/full trace precedence, limits, and avoiding silent loss

PROV-AQ / BuildKit:
  sparse provenance pointer and min/max disclosure depth

SciFact / AVeriTeC / AmbiFC / FEVER:
  product-risk mapping for test design
```

Each verification card should answer:

```text
what the external mechanism is
what VAKS borrows
what VAKS refuses
whether it adds weight
how the pilot test covers it
```

## Recommended Next Action

Do not edit the main vault yet.

Next window should do:

```text
1. Draft audit shell v1 sandbox spec.
2. Keep front face <= 6 visible lines.
3. Define the state machine:
   ordinary
   for_review
   blocking
   resolved_folded
   regressed
   parked_nonblocking
4. Define hard thickening triggers.
5. Build an 80-120 sample pilot harness.
6. Run baseline vs shell v1.
7. Report whether shell v1 reaches >= 50% ordinary reduction with 0 serious false-lite.
```

Mainline writeback should only be considered after pilot evidence shows the shell reduces noise without lowering evidence discipline.

