# VAKS Audit Shell V1 Pilot Sandbox

Status:

```text
sandbox only
main vault read-only
no SCHEMA change
not a product gate
```

## Purpose

This sandbox advances the Pro recommendation from four separate alpha templates into one `audit shell v1` test harness.

It tests whether queue/history compression adds meaningful noise reduction beyond the first alpha test while preserving hard escalation gates.

## Tested Mechanisms

```text
front face <= 6 visible lines
compact/full expandable shell
unresolved-first queue
resolved folding
nonblocking linked stubs
manual cluster key + exemplar
manual recurrence / regressed state
metadata stub for ordinary run/event surfaces
```

## What This Proves

This pilot can test:

```text
record surface reduction
main-view queue reduction
strict trigger preservation
anchor/jump-back retention
over-grouping guard behavior in typed cases
```

## What This Does Not Prove

This pilot uses fixture/risk-map cases, not live dataset ingestion.

It does not prove:

```text
automatic extraction from messy papers
source independence
real-world reviewer agreement
production runtime sampling safety
```

## Run

```powershell
python run_shell_pilot.py
```

Expected outputs:

```text
pilot_cases.json
pilot_results.json
AUDIT_SHELL_V1_SPEC.md
AUDIT_SHELL_V1_PILOT_REPORT.md
```

