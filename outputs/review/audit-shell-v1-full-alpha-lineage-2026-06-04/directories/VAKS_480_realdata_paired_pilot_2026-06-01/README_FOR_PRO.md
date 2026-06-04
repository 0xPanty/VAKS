# VAKS 480 Real-Data Paired Pilot Package

Status: sandbox-only. This package does not modify the main VAKS vault, `SCHEMA.md`, or operation conventions.

## What Was Tested

Three main arms:

- `baseline_full`: every record rendered as full audit.
- `shell_core`: hard-trigger shell + required unresolved gate + anchor health strip + sparse provenance pointer.
- `shell_core_plus_recurrence`: shell_core + representative recurrence card + open-only versioned dedup.

One negative control:

- `shell_core_plus_unversioned_control`: recurrence grouping without fingerprint version.

Dataset mix:

- SciFact 120, from `BeIR/scifact` + qrels.
- AVeriTeC 120, from `pminervini/averitec`.
- AmbiFC 120, from `just1nseo/ambifc`.
- FEVER 120, from `copenlu/fever_gold_evidence`.

All four lanes fetched at least 140 real rows. The pilot uses real rows plus deterministic pressure overlays for VAKS shell risks; it does not adjudicate factual truth.

## Main Result

`shell_core` and `shell_core_plus_recurrence` both passed hard gates:

- state mismatch: 0
- false-lite: 0
- review_due false negative: 0
- queue false negative: 0
- source anchor failures: 0
- record/evidence pointer failures: 0
- authority leakage in rendered candidates: 0
- severe over-grouping: 0
- serious folded: 0

The unversioned recurrence control failed as expected:

- severe over-grouping: 4 in the 480 pilot
- severe over-grouping: 20 in recurrence-heavy stress

## Alpha Judgment

Strongest alpha:

- `shell_core`: the minimum useful design. It gives the main global benefit while preserving evidence discipline.

Conditional positive alpha:

- `shell_core_plus_recurrence`: useful in recurrence-heavy traffic, but only as an optional bundle with versioned open-only dedup and serious breakout.

Guardrail-only:

- authority boundary lint
- categorical feedback wording

Authority fuzz caught 9/16 paraphrases, leaving 7 misses. This is useful lint, not a semantic firewall.

## Key Reports

- `reports/PILOT_480_REPORT.md`
- `reports/PRESSURE_EXTENSION_REPORT.md`
- `reports/FRAMEWORK_SANDBOX_MAPPING.md`
- `pilot_480_results.json`
- `pressure_extension_results.json`

