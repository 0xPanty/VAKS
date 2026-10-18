---
type: sandbox_pressure_test
status: pass
created_at: 2026-06-07
scope: multi-dimensional retrieval pressure test
truth_boundary: sandbox test only; not reviewed knowledge; not action basis
---

# Retrieval Pressure Test

## Purpose

Stress the Pro recommendation against VAKS's current noise problem:

```text
old sandbox / package / baseline copy / candidate / raw / overlay / feedback
appearing together in one search result set.
```

The test asks whether the candidate design filters by content identity and use
before ranking by topics, entities, tags, lexical match, vector similarity, or
graph signals.

## Test Matrix

| ID | Query mode | Expected pool | Expected exclusions | Result |
|---|---|---|---|---|
| R01 | Current mainline rule | mainline docs, templates, latest handoff, index | sandbox, baseline, zip, snapshots, candidate, feedback | pass |
| R02 | External inspiration / open research | raw + candidate + optional confirmed project overlay | reviewed/action claims unless separately requested | pass |
| R03 | Action / implementation basis | reviewed/action lane + raw stable anchors | candidate, overlay, feedback, diagnostics as final support | pass |
| R04 | Source inspection | raw + candidate source context | reviewed/action claims as automatic conclusion | pass |
| R05 | Audit history | sandbox protocol, checks, pressure tests, baseline if needed | current-rule answer without mainline confirmation | pass |
| R06 | Active project exploration | reviewed + candidate + confirmed overlay for active project | suggested overlay, archived overlay, other-project overlay | pass |
| R07 | Non-project query | reviewed/mainline + raw when needed | confirmed overlays by default | pass |
| R08 | Suggested metadata review | suggestion sidecar / review diff / query-run trace | persistent source metadata until confirmed | pass |
| R09 | Topic pack navigation | high-value topic pack with include/exclude defaults | topic pack as truth layer | pass |
| R10 | Authority tag pollution | lint block | authority tag accepted as status | pass |
| R11 | Tag-first retrieval | fail and re-run with hard filters | mixed global authority bucket | pass |
| R12 | Diagnostic score pressure | diagnostics kept in trace | facet count / embedding score / graph rank as support | pass |

## Positive Fixture Evidence

```text
source-card-confirmed-metadata.md:
  raw source with topics/entities/content_form/language/version scope.
  Still not action basis.

candidate-distillation-kp-refs.md:
  KP-001 / KP-002 are explicit candidate points.
  `candidate_not_action_basis` remains active.

project-overlay-confirmed.md:
  project borrowing is isolated in active-project overlay.

query-run-action-review.md:
  action-facing query restricts action lane to reviewed support.
  Candidate/raw/overlay appear only as orientation/drilldown/context.

topic-retrieval-pack-source-intake.md:
  topic pack provides include/exclude defaults and lanes.
  Truth boundary is navigation only.
```

## Negative Fixture Evidence

```text
source-card-forbidden-authority-tags.md:
  intentionally contains reviewed/action-basis/best-practice tags.
  Expected result: lint fail.

query-run-tag-first-failure.md:
  intentionally searches by tag first and merges authority buckets.
  Expected result: fail, then re-run with hard filters first.
```

## Stress Verdict

```text
retrieval_pressure_test: pass
main failure modes blocked:
  - authority tags
  - mixed authority bucket ranking
  - candidate as action basis
  - project borrowing written into source
  - suggestion persisted as confirmed metadata
  - diagnostic signal used as support
```

## Remaining Non-Automated Work

```text
No actual retrieval engine exists yet.
This sandbox defines and tests the contract using fixtures and static checks.
Future implementation can turn these into a script or Obsidian/Bases saved views.
```
