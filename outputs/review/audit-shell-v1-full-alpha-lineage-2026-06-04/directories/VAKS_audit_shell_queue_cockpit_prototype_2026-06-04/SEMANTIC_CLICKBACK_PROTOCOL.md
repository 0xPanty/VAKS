# Semantic Click-Back Pilot Protocol

## Purpose

Test whether source / record / evidence / transcript / package handles actually land in the right semantic place.

This test checks operator jump-back, not truth.

## Sample

Use:

```text
SEMANTIC_CLICKBACK_PILOT_SAMPLE_60.csv
```

Coverage:

- source record landing,
- claim/context landing,
- transcript segment landing,
- flat transcript landing,
- diagnostic landing,
- review output landing,
- handoff landing,
- template landing,
- weak/binary landing.

## Metrics

Record:

```text
first_correct_click
wrong_semantic_landing
dead_end_click
need_extra_navigation_count
selector_grade
notes
```

Selector grade:

```text
exact_quote_or_code_anchor
position_or_range_anchor
timestamp_segment_anchor
source_record_only
claim_or_context_only
diagnostic_or_history_only
binary_without_exposed_anchor
dead_end
```

## Proposed Gates

For valid anchor cases:

```text
first_correct_click >= 90%
dead_end_click = 0
```

For weak landing cases:

```text
wrong_semantic_landing = 0
operator must not call source/claim/context landing evidence landing
```

## Important Limitation

The current pressure set has no confirmed `1_precise_evidence_anchor` rows. To claim product-grade evidence click-back, add exact evidence-anchor fixtures or current main-vault records with selector-grade anchors.

