# Audit Shell V1 Sandbox Spec

This is a sandbox specification, not a main-vault schema proposal.

## Core Rule

```text
default light
conditionally thick
raw anchors always jump-backable
unresolved first
resolved and repeated history folded/grouped
```

## Authority Boundary

The shell is a view and queue convention.

It is not:

```text
truth authority
source-independence proof
evidence strength
LLM summary authority
dashboard/test pass
```

## Front Face

Target:

```text
4 to 6 visible lines
```

Allowed front lines:

```text
state
core_summary
anchor_jump_back
open_gap_or_scope_limit
upgrade_trigger_or_why_not_full_audit
count_or_exemplar_when_grouped
```

Do not repeat on every front face:

```text
full authority warning
full provenance
full history
full source contribution list
all grouped events
all coverage rows
```

## Expandable Back

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

## Full Audit

Open existing heavy surfaces only when needed:

```text
full evidence packet
full coverage_map
full feedback/review_due event
full collision review
```

## States

```text
ordinary
for_review
blocking
resolved_folded
regressed
parked_nonblocking
```

## Hard Thickening Triggers

```text
action_basis
promotion
explicit_challenge
conflict
known_omission
missing_anchor
risk_sensitive
explicit_correction
action_outcome
decision_outcome
high_severity_wrong_answer
independence_needed_for_confidence
reviewer_blocks
regression
```

## Object Defaults

| Object | Front Face | Thickens When |
| --- | --- | --- |
| small_claim | compact evidence face | promotion, action basis, challenge, conflict, omission, missing anchor, high-risk use |
| answer_query_run | compact coverage face | action basis, risk-sensitive, explicit trust challenge, important omission, multi-source conflict, regression |
| support_refine_collision | unresolved cluster face | conflict, independence needed, action basis, explicit challenge, reviewer blocks |
| feedback | grouped categorical feedback event | explicit correction, action outcome, decision outcome, regression, missed contradiction, high-severity wrong answer |

## Grouping Guard

Only group when all of these match:

```text
cluster_key
escalation_class
unresolved_gap_family
feedback_type when applicable
anchor_state compatible
```

Do not group if:

```text
trigger class differs materially
one item needs action-basis and another does not
one item has missing anchor and another has valid anchor
one item is conflict and another is support/refine
scope limit changes the action meaning
```

## Provenance Rule

Sparse provenance is allowed in the front face:

```text
source_anchor
source_access
jump_back_pointer
lineage pointer when useful
```

But:

```text
lineage is not independence proof
source count is not independence
group count is not support strength
```

## Pilot Gates

```text
serious false-lite = 0
serious anchor retention = 100%
ordinary record reduction >= 50%
ordinary false-positive <= 5%
over-grouping serious mismatch = 0
review_due precision >= 0.80
front face <= 6 visible lines
```

