# Source-Family Independence Trap Protocol

## Purpose

Test whether the cockpit prevents count, lineage, repeated mention, snapshots, and derived summaries from being mistaken as independent support.

## Sample

Use:

```text
SOURCE_FAMILY_INDEPENDENCE_TRAP_SAMPLE.csv
```

Current size:

```text
60 rows
```

## Trap Types

Look for:

- source count treated as support strength,
- repeated mention treated as independent evidence,
- repo snapshot lineage treated as support,
- review output treated as authority,
- derived QA / summary treated as reviewed truth,
- multiple reports from same family treated as independent sources.

## Operator Task

For each row, answer:

```text
Is this independent support?
Is this only route/context/provenance?
Would you use it as action basis?
What exact evidence would be needed?
```

## Pass Criteria

```text
independence_misread = 0
action_basis_from_count_or_lineage = 0
source_family_boundary_understood = yes
```

## Design Rule

Lineage can raise "look here" priority.

Lineage cannot raise:

```text
truth confidence
support strength
action readiness
```

