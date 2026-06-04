# Progress Note For Pro Review

## What Changed Since The 24-Case Alpha Test

The earlier test evaluated four separate alpha mechanisms:

```text
compact evidence card
compact coverage card
support/refine cluster
categorical feedback stub
```

This pilot instead tests Pro's stronger recommendation:

```text
merge the four alphas into one audit shell v1
add queue/history compression
preserve hard thickening triggers
```

## Current Pilot Result

```text
cases: 112
passed: 112/112
ordinary record reduction: 63.1%
overall visible-line reduction: 29.3%
grouped repeated-event reduction: 56.5%
resolved folding reduction: 100.0%
serious false-lite: 0
ordinary false-positive: 0
serious full-audit recall: 100%
serious anchor / missing-anchor state retention: 100%
review_due precision: 100%
front face violations: 0
over-grouping serious mismatch: 0
```

## Why The Result Improved

The improvement did not come from making every serious record shorter.

Serious records often stay the same size or become slightly thicker.

The gain comes from:

```text
ordinary front faces capped at 5-6 visible lines
resolved items folded out of the main view
repeated ordinary feedback/support-refine events grouped
hard triggers forcing full audit before lite mode can hide risk
```

## Important Correction Made During Testing

The first run failed serious anchor retention for `missing_anchor` cases.

That was a metric bug:

```text
missing_anchor cases cannot retain a valid source anchor
they must visibly preserve the missing-anchor state and thicken
```

The metric was split into:

```text
valid anchor retention
missing anchor visibility
```

After this correction, missing-anchor cases pass only if they thicken and preserve the missing-anchor note.

## Limits

This is still not a product-grade proof.

It is a fixture/risk-map pilot:

```text
typed labels are provided
dataset families are simulated as SciFact-like / AVeriTeC-like / AmbiFC-like / FEVER-like
real records are not ingested yet
reviewer agreement is not tested
source independence is not solved
runtime sampling safety is not tested
```

## What Pro Should Check

Please check whether:

```text
the shell really implements Pro's advice rather than merely renaming four alphas
the pilot gates are fair
the missing_anchor metric correction is legitimate
the grouping harness is too favorable or still too weak
any ordinary case got hidden in a way that would hurt evidence discipline
the next step should be real dataset ingestion or a stronger adversarial fixture set
```

## Recommended Next Step

Do not write this to the main vault yet.

Next should be:

```text
replace simulated families with real sampled records
SciFact: small claims
AVeriTeC: coverage/sufficiency
AmbiFC: ambiguity/over-grouping
FEVER: volume/ordinary false positives
full source anchors: messy source jump-back
derived replay: repeated/resolved/regressed feedback
```

Then rerun the same gates.

