---
type: real_vault_retrieval_smoke
status: pass
created_at: 2026-06-07
scope: actual repository search noise and role filtering smoke test
truth_boundary: retrieval smoke test only; not reviewed knowledge
---

# Real Vault Retrieval Smoke Test

## Purpose

Show why VAKS needs identity/path-role filtering before topic/tag/entity search.

This test uses the actual current repository, not only sandbox fixtures.

## Query

```text
source intake | source-intake | retrieval_policy | candidate_not_action_basis
```

Command shape:

```powershell
rg -l -i 'source intake|source-intake|retrieval_policy|candidate_not_action_basis' --glob '*.md'
```

## Raw Result

```text
total_hits=173
```

## Role Breakdown

| Role | Count | Meaning |
|---|---:|---|
| `mainline_or_recovery` | 10 | current docs/templates/handoff/index surfaces likely needed for current-rule answers |
| `audit_or_package_noise` | 48 | old sandbox, checks, baseline, package-style evidence; useful only for audit/history |
| `candidate_orientation` | 18 | provisional distillations; useful for orientation, not action basis |
| `raw_source` | 25 | provenance/source material; useful for drilldown and anchors |
| `project_overlay` | 13 | project-scoped sidecars; active project only |
| `new_sandbox_package` | 25 | this sandbox package |
| `other` | 34 | adjacent review/support files needing case-by-case routing |

## Interpretation

If a user asks "what is the current Source Intake rule?", an unfiltered keyword
search returns many files that are not the current rule.

The clean route is:

```text
current-rule mode
-> mainline_or_recovery lane first
-> exclude audit/package/candidate/raw/overlay by default
-> open audit/raw/candidate lanes only when the question asks for history,
   evidence, inspiration, or source inspection
```

## Verdict

```text
real_vault_smoke: pass
noise_problem_confirmed: yes
identity_first_filtering_needed: yes
```
