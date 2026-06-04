---
record_type: e2e-trial-readme
status: active
created: 2026-06-01
scope: sandbox-only
main_vault_write: false
schema_change: false
runtime: none
scripted: false
---

# VAKS End-to-End Trial 001

## Boundary

This scratch directory mirrors the main vault shape enough to run a manual trial:

```text
raw/
outputs/review/
outputs/qa/
outputs/feedback/
wiki/claims/
context-packs/
friction/
```

Main vault path:

```text
C:\Users\Administrator\Documents\资料库
```

Main vault remains read-only for this trial. All files here are sandbox artifacts.

No script, runtime, automation, schema change, or mainline writeback is part of this trial.

## Trial Topic

Real question:

```text
Can a citation-backed LLM answer be treated as action-basis-ready in VAKS?
```

Reason for choosing it:

```text
The topic hits the core VAKS boundary: provenance and citation are useful,
but source-span support and coverage still decide whether a point can support action.
```

## Source Set

Step 1 source:

```text
S1: ALCE / Enabling Large Language Models to Generate Text with Citations
```

Step 2 collision sources:

```text
S2: Attributed Question Answering
S3: GopherCite / Teaching language models to support answers with verified quotes
S4: FRONT / Fine-Grained Grounded Citations
```

## Required Exit Conditions

- Step 1: raw -> candidate -> review -> verified node -> context pack -> feedback record.
- Step 2: add 2-4 same-theme sources and create at least one point collision.
- Step 3: answer one real question using a context pack with coverage_map and evidence_sufficiency.
- Step 4: record one feedback event and ask a similar question to observe activation / scope-fit change.
- Every step has a friction log.
- Pain report groups findings by stuck / too heavy / missing / ambiguous.

