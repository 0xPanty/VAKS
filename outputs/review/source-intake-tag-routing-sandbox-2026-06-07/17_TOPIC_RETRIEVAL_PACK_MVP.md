---
type: sandbox_design_note
status: candidate_only
created_at: 2026-06-07
scope: topic retrieval pack MVP for source-intake-routing workbench
truth_boundary: sandbox design note only; topic packs are navigation/context activation, not truth
---

# Topic Retrieval Pack MVP

## Plain Rule

```text
One topic page should answer:
Where do I start, what can I trust, what is only orientation, and what noise is excluded?
```

## MVP Shape

Use a generated context-pack candidate as the first working version of a topic
retrieval pack.

Minimum sections:

```text
Query
Pack Summary
Pack Items
Excluded Or Not Default
Coverage Overview
```

This is enough to make the workbench usable without building a database, MCP
server, vector index, or Obsidian Bases stack.

## Source-Intake Routing Pack Defaults

```yaml
topic_id: source-intake-routing
start_here:
  mode: current-rule
  lanes:
    - mainline_current
research_body:
  mode: research
  lanes:
    - reviewed_support
    - raw_drilldown
    - candidate_orientation
    - active_project_overlay
    - support_review_output
excluded_by_default:
  - audit_evidence
  - feedback_diagnostics
  - pro_package
  - old_sandbox
  - baseline_copy
  - package_copy
  - archived_overlay
```

## Generated Pack Command

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-context-pack-builder-v0.ps1 `
  -Root . `
  -Pattern 'source intake|metadata-routing|context pack|registry-before-recompute|query-run receipt|retrieval_policy' `
  -Mode research `
  -TopicId source-intake-routing `
  -Limit 120 `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\topic-retrieval-pack-source-intake-generated.md
```

## Safety Properties

The generated pack must keep these labels visible:

```text
mainline_current:
  start here, not automatically a complete answer.

reviewed_support:
  stable support candidate, still needs selector/scope check for action.

raw_drilldown:
  provenance and source anchor; not reviewed by itself.

candidate_orientation:
  useful idea extraction; never action basis.

active_project_overlay:
  project-scoped hint; not generic source metadata.

audit_evidence:
  why/how evidence; excluded unless audit mode.

feedback_diagnostics:
  usefulness/review pressure; not truth mutation.
```

## Real-Vault Smoke Question

```text
Can a question about source intake metadata and context packs produce a clean
workbench pack from the actual vault, while old package/baseline/sandbox noise
stays out of the default pack?
```

Pass condition:

```text
1. current-rule Start Here appears.
2. raw/candidate/review outputs are separated by lane.
3. candidate items have action_basis_allowed=false.
4. excluded/noise section lists audit/package/sandbox material instead of mixing it into support.
5. action_readiness stays not_ready until evidence support check runs.
```
