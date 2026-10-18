---
type: other_role_classifier
status: candidate_only
created_at: 2026-06-07
scope: classify files that are not cleanly mainline/raw/candidate/overlay/audit
truth_boundary: candidate classifier only
---

# Other Role Classifier

## Why This Exists

The first real-vault smoke test found `other=34` for one noisy Source Intake
query.

That means identity-first filtering helps, but path roles need a finer
fallback taxonomy.

## Fallback Roles

| role | signals | default lane |
|---|---|---|
| `project_guide` | `AGENTS.md` | mainline/recovery |
| `review_output` | `outputs/review/*.md` not otherwise classified | candidate/support, not default current-rule |
| `pro_package` | path contains `PRO_`, `pro-review`, or package folder | audit/review input |
| `handoff` | `00_handoff/*.md` | mainline/recovery if latest/relevant |
| `source_card` | `raw/articles`, `raw/videos`, `raw/repos`, `raw/papers` | raw drilldown |
| `summary` | `wiki/summaries` | support/reviewed depending frontmatter |
| `formal_template` | `templates/*.md` | mainline operation |
| `index` | `wiki/indexes/*.md` | navigation/recovery |
| `feedback_event` | `outputs/feedback` or `record_kind: feedback_event` | feedback diagnostics |
| `legacy_or_unknown` | no strong signal | triage required |

## Rule

```text
Unknown is allowed.
Unknown cannot become action basis.
Unknown should be shown after known lanes.
```

## Classifier Implementation

The sandbox script maps unknown-ish files into:

```text
support_review_output
feedback_diagnostics
other_needs_triage
```

Future iterations can split `support_review_output` into more precise roles
after more real queries are tested.
