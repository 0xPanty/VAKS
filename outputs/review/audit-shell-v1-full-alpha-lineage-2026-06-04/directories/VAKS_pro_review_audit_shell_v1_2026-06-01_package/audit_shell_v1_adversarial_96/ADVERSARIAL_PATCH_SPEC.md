# Audit Shell V1 Adversarial Patch Spec

This is a sandbox test spec, not a main-vault rule.

## Pro Critique Addressed

The previous 112-case pilot was useful but too self-confirming:

```text
case labels and shell decisions were too coupled
front-face cap was structurally hard to fail
anchor retention was boolean, not jump-back success
review_due precision had no recall
grouping was too friendly
missing triggers and states were not covered
```

## This Patch Adds

```text
96 explicitly listed adversarial cases
independent gold label columns
shell output structure separate from gold labels
actual front/back/full pointer fields
jump-back resolver against local raw source anchors
review_due precision and recall
trigger-family recall
near-miss over-grouping battery
authority leakage checks
hidden burden counters
```

## Case Mix

```text
24 over-grouping near-miss
16 false-lite traps
16 anchor / jump-back traps
16 review_due traps
12 state transition traps
12 authority leakage traps
```

## Hard Gates

```text
serious false-lite = 0
trigger-family recall = 100%
valid-anchor jump-back success = 100%
missing-anchor visibility = 100%
severe over-grouping = 0
authority leakage incidents = 0
feedback changing truth = 0
review_due recall >= 0.95
review_due precision >= 0.90
front-face violation = 0
```

## Limits

This is still fixture-based.

It does not replace the later 480-sample real-data paired pilot.

