---
type: sandbox_tool_test
status: pass
created_at: 2026-06-07
scope: retrieval MVP lane classifier script test
truth_boundary: sandbox tool test only
---

# Retrieval MVP Script Test

## Tool

```text
tools/vaks-retrieval-mvp.ps1
```

## Query

```text
source intake | source-intake | retrieval_policy | candidate_not_action_basis
```

## Mode Matrix

The same query returned:

```text
total_hits=181
```

| Mode | mainline | raw | candidate | overlay | audit | feedback | support_review | other |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `current-rule` included | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `action` included | 11 | 26 | 0 | 0 | 0 | 0 | 0 | 0 |
| `audit` included | 11 | 0 | 0 | 0 | 75 | 0 | 0 | 0 |
| `research` included | 0 | 26 | 20 | 15 | 0 | 0 | 31 | 0 |
| `source-inspection` included | 0 | 26 | 20 | 0 | 0 | 0 | 0 | 0 |
| `project-exploration` included | 11 | 26 | 20 | 15 | 0 | 0 | 31 | 0 |

Full lane counts:

```text
mainline_current=11
raw_drilldown=26
candidate_orientation=20
active_project_overlay=15
audit_evidence=75
feedback_diagnostics=2
support_review_output=31
other_needs_triage=1
```

## False Positive Fix

Initial run put `AGENTS.md` in `other_needs_triage`.

Patch:

```text
AGENTS.md -> project_guide -> mainline_current
```

Initial forbidden-tag scan also flagged `ARCHITECTURE_PRINCIPLES.md` because
its frontmatter uses `action-basis` as a theme tag.

Patch:

```text
forbidden authority-tag lint only applies to intake surfaces:
  source
  candidate_distillation
  project_overlay
  feedback_event
  query-run
  source/candidate/overlay path roles
```

Direct forbidden-tag test after patch:

```text
forbidden_hits=1
hit=fixtures/source-card-forbidden-authority-tags.md
```

## Verdict

```text
retrieval_mvp_script_test: pass
current_rule_noise_reduced: yes
mode_separation_working: yes
forbidden_tag_false_positive_fixed: yes
```
