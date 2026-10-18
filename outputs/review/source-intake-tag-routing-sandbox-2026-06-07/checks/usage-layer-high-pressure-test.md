---
type: sandbox_check
status: pass
created_at: 2026-06-07
scope: usage-layer high pressure test for artifact registry, context-pack builder, and Obsidian workbench entrypoints
truth_boundary: sandbox pressure test only; not reviewed knowledge; not action basis
---

# Usage-Layer High Pressure Test

## Test Pattern

```text
artifact registry|context pack builder|obsidian workbench|source-intake-routing|registry-before-recompute
```

## Purpose

Stress the new usage-layer additions against the same noise problem that started
this sandbox:

```text
many old references, candidate notes, raw sources, overlays, packages, and
sandbox files match the query.
```

The test asks whether the retrieval MVP keeps identities separated.

## Current-Rule Mode

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-retrieval-mvp.ps1 `
  -Pattern 'artifact registry|context pack builder|obsidian workbench|source-intake-routing|registry-before-recompute' `
  -Mode current-rule `
  -Limit 200
```

Result:

```text
total_hits=49
mainline_current=5 included=5
candidate_orientation=2 included=0
raw_drilldown=2 included=0
active_project_overlay=7 included=0
audit_evidence=19 included=0
reviewed_support=2 included=0
support_review_output=12 included=0
other_needs_triage=0
```

Interpretation:

```text
current-rule mode shows current rule surfaces only.
New sandbox usage-layer additions do not become current rule by default.
```

## Research Mode

Result:

```text
total_hits=49
candidate_orientation=2 included=2
raw_drilldown=2 included=2
active_project_overlay=7 included=7
reviewed_support=2 included=2
support_review_output=12 included=12
audit_evidence=19 included=0
mainline_current=5 included=0
other_needs_triage=0
```

Interpretation:

```text
research mode can see candidate/reference/overlay/support material, but audit
packages stay out unless audit mode is selected.
```

## Action Mode

Result:

```text
total_hits=49
mainline_current=5 included=5
raw_drilldown=2 included=2
reviewed_support=2 included=2
candidate_orientation=2 included=0
active_project_overlay=7 included=0
audit_evidence=19 included=0
support_review_output=12 included=0
other_needs_triage=0
```

Interpretation:

```text
action mode excludes candidate, overlay, audit, and support-review outputs from
default final support.
```

## Audit Mode

Result:

```text
total_hits=49
audit_evidence=19 included=19
mainline_current=5 included=5
candidate_orientation=2 included=0
raw_drilldown=2 included=0
active_project_overlay=7 included=0
reviewed_support=2 included=0
support_review_output=12 included=0
other_needs_triage=0
```

Interpretation:

```text
audit mode can see the new sandbox additions and package/check history as
process evidence.
```

## Patch During Test

Initial run exposed:

```text
other_needs_triage=1
file=wiki/projects/2026-05-27-llm-wiki-compiler-implementation-extraction.md
```

Patch:

```text
tools/vaks-retrieval-mvp.ps1 now classifies wiki/projects/* as project_note
and maps project_note to support_review_output.
```

After patch:

```text
other_needs_triage=0
```

## Cross-Check

KP lint still catches bad knowledge-point IDs:

```text
files_checked=2
pass=1
fail=1
expected_fail=fixtures/candidate-distillation-bad-kp.md
```

Usage-layer lint catches bad candidate-to-action leakage:

```text
files_checked=13
pass=12
fail=1
expected_fail=fixtures/usage-layer-bad-authority-leak.md
```

## Verdict

```text
status=pass
```

The usage-layer additions improve the workbench path without changing the
current rule, truth layer, or action basis boundary.
