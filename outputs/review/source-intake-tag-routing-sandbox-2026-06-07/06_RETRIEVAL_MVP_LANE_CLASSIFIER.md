---
type: sandbox_mvp_design
status: candidate_only
created_at: 2026-06-07
scope: retrieval lane classifier MVP
truth_boundary: sandbox MVP only; not production retrieval
---

# Retrieval MVP Lane Classifier

## Plain Goal

Turn "full-vault keyword search" into "search results grouped by identity".

The MVP does not answer the question by itself. It only says:

```text
this hit is current rule
this hit is candidate orientation
this hit is raw source
this hit is active project overlay
this hit is audit evidence
this hit is feedback/diagnostic
this hit needs triage
```

## Tool

```text
tools/vaks-retrieval-mvp.ps1
```

Example:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-retrieval-mvp.ps1 `
  -Pattern 'source intake|source-intake|retrieval_policy|candidate_not_action_basis' `
  -Mode current-rule `
  -Limit 200
```

## Modes

```text
current-rule:
  include current mainline/recovery surfaces first.

research:
  include raw, candidate, reviewed, and project overlay as orientation lanes.

action:
  include reviewed/mainline and raw drilldown only as possible final support.
  candidate/overlay/feedback remain non-final.

source-inspection:
  include raw and candidate source context.

audit:
  include sandbox/check/package evidence.

project-exploration:
  include active project overlays plus candidate/raw context.
```

## Classification Inputs

```text
path role
frontmatter record_kind/type
knowledge_status
retrieval_policy warning_code
overlay_state
tags lint
query mode
```

## Non-Goals

```text
no vector index
no automatic answer generation
no evidence sufficiency
no reviewed relation creation
no source mutation
```

## MVP Success

```text
The same noisy query should expose how many hits belong to each lane.
Current-rule mode should make mainline/recovery easy to see instead of burying
it among sandbox, raw, candidate, overlay, and package files.
```
