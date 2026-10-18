---
type: sandbox_check
status: pass
created_at: 2026-06-07
scope: retrieval mode regression after context pack builder prototype
truth_boundary: sandbox regression evidence only; not reviewed knowledge; not action basis
---

# Retrieval Mode Regression After Builder

## Purpose

Confirm that adding the topic/context pack builder did not widen default
retrieval lanes.

## Determinism Patch

`tools/vaks-retrieval-mvp.ps1` now sorts matched Markdown paths before applying
`-Limit`.

Reason:

```text
The workbench should not show different first-window lane counts just because
rg returns files in a different order.
```

## Command Shape

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-retrieval-mvp.ps1 `
  -Root . `
  -Pattern 'source intake|metadata-routing|context pack|registry-before-recompute|query-run receipt|retrieval_policy' `
  -Mode <mode> `
  -Limit 240 `
  -Json
```

## Results

Format:

```text
lane:total_hits/included_by_default
```

Current-rule:

```text
active_project_overlay:18/0
audit_evidence:73/0
candidate_orientation:28/0
feedback_diagnostics:1/0
mainline_current:20/20
support_review_output:100/0
```

Action:

```text
active_project_overlay:18/0
audit_evidence:73/0
candidate_orientation:28/0
feedback_diagnostics:1/0
mainline_current:20/20
support_review_output:100/0
```

Audit:

```text
active_project_overlay:18/0
audit_evidence:73/73
candidate_orientation:28/0
feedback_diagnostics:1/0
mainline_current:20/20
support_review_output:100/0
```

## Interpretation

```text
current-rule:
  current rule only.

action:
  no candidate, overlay, audit, feedback, or support-review output enters by
  default in this sorted pressure window.

audit:
  audit evidence is visible only in audit mode, alongside current rule.
```

The local sorted first window is dominated by `outputs/review` material. That is
useful as a noise test: old sandbox/package/support artifacts do not become
action-facing context just because they match the topic.
