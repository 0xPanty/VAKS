---
type: sandbox_lint_matrix
status: pass_with_expected_failures
created_at: 2026-06-07
scope: metadata/tag/routing lint checks
truth_boundary: sandbox lint only
---

# Lint Matrix

## Test Results

| ID | Check | Expected | Actual | Evidence |
|---|---|---|---|---|
| T01 | All Pro requirements mapped | pass | pass | `requirements=24` |
| T02 | Source card has discovery facets | pass | pass | `content_form/language/version/entities` |
| T03 | Good source has no authority tags | pass | pass | forbidden tag regex clean |
| T04 | Bad source triggers authority-tag lint | fail | fail | `reviewed/action-basis/best-practice` |
| T05 | Candidate uses `kp_ref` and is not action basis | pass | pass | `KP-001` + `candidate_not_action_basis` |
| T06 | Project borrowing isolated in overlay | pass | pass | `project_borrow_scope` + `active_project_only` |
| T07 | Action query filters to reviewed lane first | pass | pass | reviewed lane empty blocks action basis |
| T08 | Tag-first mixed bucket is blocked | fail | fail | `tag_first_pipeline` + `mixed_authority_bucket` |
| T09 | Suggestions are nonpersistent sidecar | pass | pass | `persistent_main_note_allowed: false` |
| T10 | Topic pack is navigation only with excludes | pass | pass | `navigation_only` + default exclusions |
| MC01 | Candidate SOURCE_INTAKE addendum contains core routing rule | pass | pass | fields/facets/entities/tags rule |
| MC02 | Candidate source-record template contains discovery facets | pass | pass | `content_form`, `language`, `version_or_time_scope`, `entities` |
| MC03 | Candidate distillation template contains `kp_ref` and candidate guard | pass | pass | `KP-001` + `candidate_not_action_basis` |
| MC04 | Candidate query-run template contains hard filters and lanes | pass | pass | `hard_filters` + `retrieval_lanes` |
| MC05 | Suggestion sidecar stays nonpersistent | pass | pass | `persistent_main_note_allowed: false` |
| MC06 | Topic pack stays navigation-only | pass | pass | `truth_boundary: navigation_only` |

## Expected Failures

These failures are intentional fixtures:

```text
T04: source-card-forbidden-authority-tags.md
T08: query-run-tag-first-failure.md
```

They prove the sandbox can name and block the two main pollution modes:

```text
authority tag pollution
tag-first mixed authority retrieval
```

## Forbidden Authority Tags

```text
reviewed
approved
adopted
use-this
best-practice
truth
safe
action-basis
decision
verified
high-confidence
for-vaks
do-not-borrow-for-vaks
adopt-for-vaks
```

## Lint Verdict

```text
lint_matrix: pass_with_expected_failures
unexpected_failures: 0
mainline_candidate_snapshot_checks: 6/6
```
