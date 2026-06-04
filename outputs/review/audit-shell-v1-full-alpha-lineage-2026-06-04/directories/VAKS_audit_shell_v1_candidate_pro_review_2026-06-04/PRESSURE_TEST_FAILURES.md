# Pressure Test Failures And Corrections

## Corrected Failure Count

`	ext
false_lite = 0
over_heavy = 0
`

## What Looked Like A Failure First

The first pass flagged video JSON diagnostic artifacts as false-lite cases.

- acquisition ledgers,
- segments.json,
- source metadata,
- transcript metadata.

Those should stay light. They are not evidence and not action material. The shell should mark them as diagnostic metadata, not open full audit.

## Real Failure Status

No real false-lite remained after distinguishing diagnostic metadata from ASR text used as evidence.

The meaningful rule is:

`	ext
ASR/acquisition metadata = ordinary diagnostic
segments.md = for_review
transcript.txt = blocking before evidence/action use
`

This is a design requirement, not a reason to weaken the shell.
