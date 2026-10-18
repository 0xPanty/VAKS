---
record_kind: retrieval_pilot_protocol
status: candidate
knowledge_status: candidate
project_id: VAKS
action_basis_allowed: false
truth_mutation_allowed: false
---

# Pilot Protocol

## Hypothesis

A Yuxi-like runtime layer should improve VAKS retrieval by returning better chunk anchors and broader related context, while boundary labels may be enough for a capable Agent in ordinary exploration mode.

## What Counts As Help

Positive value:

- better expected-source hit rate than T0
- better heading/chunk anchors than file-level search
- more useful retrieval for retrieval-layer, context-pack, feedback, and boundary questions
- visible boundary labels on candidate/raw/overlay material

Negative value:

- candidate/overlay material appears as if it were reviewed
- retrieval score is presented like evidence support
- action-facing queries return candidate/raw material without warning
- graph/link expansion creates relation authority

## Test Corpus

Primary corpus:

```text
README / SCHEMA / architecture docs
wiki/
raw/
outputs/qa/
outputs/review/project_lens_overlays/
outputs/review/vaks-retrieval-layer-design-2026-06-11/
outputs/review/2026-06-11-*.md
```

Full noisy corpus:

```text
all markdown files in this repository
```

The primary corpus approximates what an Agent should usually retrieve. The full corpus is a noise and scale pressure test.

## Metrics

- `hit_at_5`: whether an expected source/path keyword appears in top 5.
- `hit_at_10`: whether an expected source/path keyword appears in top 10.
- `top1_status`: inferred authority bucket of the top result.
- `candidate_or_raw_top1`: whether top result is not reviewed.
- `warning_emitted`: whether T2 produced a warning when the result is not action-authoritative.
- `anchor_kind`: file or chunk.

## Interpretation

This pilot can support a design direction. It cannot prove production readiness, Yuxi product quality, or action readiness.

