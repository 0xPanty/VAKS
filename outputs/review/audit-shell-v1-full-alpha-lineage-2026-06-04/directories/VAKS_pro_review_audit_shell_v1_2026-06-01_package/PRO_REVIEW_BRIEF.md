# Pro Review Brief: Audit Shell V1 Pilot

## 2026-06-01 Latest Status Update

This brief was originally written for the 112-case audit shell v1 pilot. It is now historical context.

The latest artifact in this package is:

```text
audit_shell_v1_adversarial_96/
```

That folder implements Pro's requested next step after the `pass with concerns` review:

```text
96 explicit adversarial cases
independent gold labels in adversarial_cases.psv
separate shell output and comparison
anchor/jump-back resolver against local raw_sources
review_due precision and recall
near-miss over-grouping battery
authority-leakage traps
hidden burden counters
```

Latest run:

```text
cases: 96
passed: 96/96
hard_gate_pass: true
false_lite: 0
review_due_precision: 1.0
review_due_recall: 1.0
jumpback_failures: 0
severe_over_grouping: 0
authority_leakage_incidents: 0
visible_front_reduction_pct: 58.7
grouped_reduction_pct: 50.0
```

Review order:

```text
1. NEXT_WINDOW_RECOVERY_FULL_GRAIN.md
2. audit_shell_v1_adversarial_96/PROGRESS_NOTE_FOR_PRO_REVIEW.md
3. audit_shell_v1_adversarial_96/ADVERSARIAL_PATCH_REPORT.md
4. audit_shell_v1_adversarial_96/adversarial_cases.psv
5. this historical brief for the earlier 112-case pilot
```

Do not treat the 96-case result as product proof. It is a stronger fixture patch before the proposed 480 real-data paired pilot.

## What Pro Asked For

Pro's recommendation was not to keep four separate alpha templates.

The recommended direction was:

```text
merge the four alphas into one audit shell v1
default front face stays light
expanded back carries details
full audit opens only on hard triggers
queue/history compression provides most product-level reduction
unresolved-first queue
resolved folding
repeated-event grouping
regressed reopen
metadata/compact stub for ordinary items
no SCHEMA change as first move
no truth authority shift into shell/grouping/feedback/dashboard/tests
```

## What Codex Implemented In This Pilot

Implemented in sandbox:

```text
AUDIT_SHELL_V1_SPEC.md
run_shell_pilot.py
112 fixture/risk-map cases
baseline vs shell v1 comparison
hard thickening triggers
front face <= 6 visible lines
states: ordinary, for_review, blocking, resolved_folded, regressed, parked_nonblocking
resolved folding
manual grouping guard
derived replay cases for repeated feedback/support-refine
missing_anchor visibility metric
pilot gates
```

Not implemented:

```text
real SciFact ingestion
real AVeriTeC ingestion
real AmbiFC ingestion
real FEVER ingestion
real full-source-anchor expansion beyond fixture forms
human reviewer timing
dual-review adjudication
runtime trace policy
automatic fingerprinting
automatic reopen
SCHEMA/main-vault writeback
```

## Why This Is Not Claimed As Product Proof

This is a fixture/risk-map pilot.

It tests:

```text
whether Pro's shell logic is implementable
whether pilot gates can be formalized
whether queue/history compression improves over the first 24-case alpha test
whether hard triggers still thicken
```

It does not test:

```text
messy raw extraction
reviewer agreement
source independence
production runtime safety
```

## First Alpha Test Baseline

The earlier alpha test measured the four mechanisms separately.

Result:

```text
cases: 24
passed: 24/24
overall saved: 27.4%
ordinary-case saved: 42.4%
false-lite: 0
ordinary false positives: 0
```

Interpretation:

```text
direction verified, but not product-level
mostly single-record compression
grouping/resolved folding not meaningfully tested
```

## Audit Shell V1 Pilot Result

Current pilot result:

```text
cases: 112
passed: 112/112
overall visible-line reduction: 29.3%
ordinary record reduction: 63.1%
grouped repeated-event reduction: 56.5%
resolved folding reduction: 100.0%
serious false-lite: 0
ordinary false-positive: 0
serious full-audit recall: 100%
serious anchor / missing-anchor state retention: 100%
review_due precision: 100%
front face violations: 0
over-grouping serious mismatch: 0
pilot_gate_pass: true
```

Interpretation:

```text
improvement over alpha test came from shell + queue/history compression
ordinary reduction crossed the pilot gate of >=50%
it reached the lower product target band of >=60% on fixture ordinary cases
it has not reached product proof because data is still simulated/typed
```

## Metric Notes

### Missing Anchor Correction

The first run incorrectly counted `missing_anchor` cases as failing anchor retention because they cannot retain a valid anchor.

The metric was corrected to distinguish:

```text
valid_anchor_retention:
  if a valid anchor exists, it must be retained

missing_anchor_visibility:
  if no valid anchor exists, the missing-anchor state must be visible and must thicken
```

Pro should check whether this correction is legitimate.

### Grouping Guard

The pilot groups only when these match:

```text
cluster_key
escalation_class
unresolved_gap_family
feedback_type when applicable
anchor_state compatible
```

It refuses grouping when:

```text
trigger class differs materially
action-basis differs
anchor state differs
conflict vs support/refine differs
scope limit changes action meaning
```

Pro should check whether this is strict enough or too favorable.

## Main Risks Codex Sees

```text
fixture labels may make shell look safer than real messy inputs
grouping may still be too easy because replay cases are controlled
review_due precision is artificial because labels are preassigned
human review time is not measured
real dataset ingestion may reveal extraction and anchor problems
overall reduction remains only 29.3% because serious cases remain thick
```

## Codex Recommendation Before Pro Review

Do not write to main vault yet.

Recommended next step depends on Pro's review:

```text
If Pro accepts shell pilot:
  proceed to real sampled records from SciFact / AVeriTeC / AmbiFC / FEVER + full source anchors

If Pro thinks grouping is too favorable:
  add adversarial fixture cases before real ingestion

If Pro thinks the shell is too heavy:
  narrow front face or state machine before expanding tests

If Pro finds evidence-discipline leakage:
  stop and fix shell boundaries before any further testing
```
