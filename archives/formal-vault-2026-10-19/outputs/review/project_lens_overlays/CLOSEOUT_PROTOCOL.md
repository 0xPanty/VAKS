---
type: project_lens_closeout_protocol
status: sandbox_policy
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-closeout-lifecycle
truth_boundary: sandbox operating convention only; not reviewed knowledge; not ADR; not action basis; not schema; not template
write_scope: outputs/review/project_lens_overlays only
---

# Project Lens Closeout Protocol

## 人话

Project Lens 是项目期脚手架。

项目进行中可以用它快速标记：

```text
watch
partial
avoid
park
```

项目结束时，脚手架必须拆。

它不能继续伪装成知识本体、项目决策、action basis、best practice、长期禁令，或默认检索信号。

## Core Rule

```text
Live Lens entries must drain at project closeout.
```

Closeout 之后，live Lens entry 只允许三类语义去向：

```text
landed snapshot
boundary snapshot
exit live layer
```

第三类在操作上拆成：

```text
archive by default
delete only as restricted exception with tombstone
```

Two extra operations are allowed, but they are actions, not durable states:

```text
carry-forward / reopen
supersede / withdraw
```

## Policy Sentences

```text
Project Lens is a project-time sidecar overlay, not truth, ADR, or action basis.
Live stance serves only the active project; it is not a durable closeout state.
After project closeout, a Lens entry must become a landed snapshot, become a boundary snapshot, or exit the live layer.
Exit from the live layer defaults to archive; delete is only for drafts, duplicates, or low-value noise and must leave a tombstone.
A landed snapshot records a real project adoption outcome with reusable value; it is not a formal best practice.
A boundary snapshot records a reusable failure boundary or non-fit condition; it is not a universal ban.
Any snapshot used for promotion, decision, action basis, or risk-sensitive answers must still pass evidence-aware review and the non-circular warrant rule.
Archived Lens entries do not enter default retrieval.
Tombstones never enter semantic retrieval.
```

## Closeout Outcomes

| Outcome or action | Trigger | Minimum metadata | Owner / review | Storage | Retrieval role |
|---|---|---|---|---|---|
| landed snapshot | Real project adoption with reusable future value | `project`, `kp_ref`, `from_lens_ref`, `adopted_scope`, `where_used`, `evidence_refs`, `outcome_note`, `scope_limits`, `created_by/at`, `truth_boundary` | project owner; add evidence-aware reviewer if used for future decisions | sandbox snapshots/landed first | candidate experience retrieval |
| boundary snapshot | Reusable non-fit, failure boundary, or avoid-this trigger | `project`, `kp_ref`, `from_lens_ref`, `trap_title`, `failure_context`, `trigger_conditions`, `why_non_fit`, `scope_boundary`, `safer_alternative`, `evidence_refs`, `created_by/at`, `truth_boundary` | project owner; reviewer recommended to prevent over-generalization | sandbox snapshots/boundary first | warning / boundary retrieval |
| archive | No durable outcome, but historical context may matter | `project`, `kp_ref`, `final_live_stance`, `archive_reason`, `closed_by/at` | project owner | closeout manifest; optional archive area | excluded from default retrieval |
| delete + tombstone | Draft, duplicate, low-quality AI noise, or mistaken entry with no downstream refs | `project`, `kp_ref`, `delete_reason`, `closed_by/at`, `downstream_refs: none_confirmed` | project owner; reviewer required if ever referenced | tombstone in closeout manifest | audit only, never semantic retrieval |
| carry-forward / reopen | A new active project still wants to inspect or try the point | `source_project`, `new_project`, `kp_ref`, `carry_forward_reason`, `new_lens_ref` | new project owner | new project overlay; old entry archived | new Lens only; old Lens stays closed |
| supersede / withdraw snapshot | Existing snapshot is narrowed, overturned, or replaced by later evidence/results | `supersedes`, `superseded_by`, `change_reason`, `review_refs`, `changed_by/at` | project owner + reviewer | successor snapshot and link update | latest chain preferred; old snapshot retained for audit |

## Retrieval Priority

Default retrieval should respect layer and lifecycle before similarity:

```text
reviewed core / decision / action basis
> landed_snapshot / boundary_snapshot
> active Project Lens for current project only
> archived Lens
> tombstone never
```

Meaning:

```text
reviewed core / decision / action basis = knowledge/action authority
snapshot = project outcome candidate / warning candidate
active Lens = current-project routing hint
archive = historical context only
tombstone = audit and de-dup only
```

Do not put Lens, snapshots, archive, and tombstones into one undifferentiated semantic pool.

## Backflow Rule

Snapshots may create candidates, not direct core changes.

```text
landed_snapshot
  -> candidate pattern
  -> implementation note
  -> best-practice candidate

boundary_snapshot
  -> negative-knowledge candidate
  -> warning note
  -> boundary rule candidate
```

Promotion from those candidates into reviewed knowledge, architecture, decision, or action basis still requires the existing review path and the v0.2.13 late-stage action-facing warrant rule.

## Risk Guardrails

```text
Do not use adopted / accepted / rejected as live Lens stance.
Do not snapshot every watch / partial / avoid.
Do not let archive appear in default retrieval.
Do not delete without tombstone.
Split long-lived partial entries before closeout when the borrowable and non-borrowable parts are mixed.
Boundary snapshots must include trigger conditions, scope boundary, and safer alternative.
Landed snapshots must keep truth_boundary visible and must not claim best-practice authority.
No naive regex migration or bulk rewrite in phase one.
AI may draft closeout suggestions, warnings, or manifests, but a human/project owner confirms closeout.
No project can be marked closed without a closeout owner.
Do not silently edit old snapshots when later evidence changes the judgment; supersede or withdraw instead.
```

## Current MVP

Current sandbox closeout MVP:

```text
outputs/review/project_lens_overlays/VAKS-closeout-manifest-2026-06-05.md
```

The MVP intentionally does not:

```text
move files
delete files
rewrite active Lens entries
create a database
create a schema
create a template family
automate migration
promote Project Lens into mainline architecture
```
