---
type: candidate_design_note
status: candidate_only
created_at: 2026-06-06
updated_at: 2026-06-06
scope: VAKS Source Intake Control Flow -> short lifecycle + four orthogonal dimensions
truth_boundary: candidate design only; not reviewed knowledge; not architecture decision; not action basis
source_inputs:
  - user_pasted_pro_response_2026_06_06
  - user_refined_state_machine_2026_06_06
  - SOURCE_INTAKE.md
  - outputs/review/2026-06-06-project-overlay-obsidian-usage-supplement.md
external_references:
  - https://www.w3.org/TR/annotation-model/
  - https://www.w3.org/ns/prov/
  - https://adr.github.io/madr/
  - https://www.nasa.gov/nasa-lessons-learned/
v0_2_13_trigger: no
promotion_required_for_mainline: true
---

# Source Intake Control Flow State Machine Candidate Design

## One-Line Judgment

The better shape is not a single long state machine. It is:

```text
short lifecycle
+ four orthogonal dimensions
+ derived retrieval / promotion permissions
```

人话：

```text
Light / Medium / Heavy 只表示处理强度。
raw / candidate / reviewed 才表示知识地位。
Project Overlay 只是项目侧边栏。
review_pressure 才表示是否需要复核或阻断。
```

This prevents a common failure:

```text
heavy == more processed
heavy != more true
```

## Why This Matters

If VAKS mixes processing strength, authority, project fit, and retrieval use in
one field, agents will eventually overread candidate material.

Bad collapse:

```text
medium candidate written in rule-like language
-> retrieved into context
-> treated like adopted architecture
```

The design goal is to make that mechanically harder:

```text
candidate_provisional + knowledge_status=candidate
-> action_basis_allowed=false
-> action-facing use triggers v0.2.13
```

## Four Orthogonal Dimensions

### 1. Processing Tier

```yaml
processing_tier: light | medium | heavy
```

Meaning:

| Value | Meaning | Authority effect |
|---|---|---|
| `light` | Saved so it can be found later. | none |
| `medium` | Candidate distillation / candidate points. | none |
| `heavy` | Explicit claim/evidence/warrant review is open. | none until passed |

Rule:

```text
processing_tier never creates truth confidence.
```

Naming rule:

```text
Do not use authority as a field name.
Use knowledge_status.
```

### 2. Knowledge Status

```yaml
knowledge_status: raw | candidate | reviewed
```

Meaning:

| Value | Meaning | Can support action basis directly? |
|---|---|---|
| `raw` | Source/provenance only. | no |
| `candidate` | Extracted or interpreted, not reviewed. | no |
| `reviewed` | Passed review into reviewed knowledge / decision / adopted pattern. | conditional on scope |

Rule:

```text
candidate can be useful, high-signal, and well written while still not being authority.
```

### 3. Overlay State

```yaml
overlay_state: none | suggested | confirmed | archived
```

Meaning:

| Value | Meaning | Authority effect |
|---|---|---|
| `none` | No project sidecar. | none |
| `suggested` | System suspects project relevance. | none; temporary reviewer/operator trace only |
| `confirmed` | User/current task confirmed project-scoped sidecar. | project navigation only |
| `archived` | Project overlay was retired or project ended. | none; excluded by default |

Rule:

```text
Project Overlay is not adoption, not ADR, not truth, not action basis.
```

Storage / confirmation rule:

```text
suggested overlay:
  only exists in query-run trace, agent trace, or temporary suggestion inbox.
  do not write it as a durable vault note.
  do not include it in default retrieval.

confirmed overlay:
  only exists after explicit user confirmation, or when the task itself is an
  explicit current-project intake and writeback is allowed.
  store under outputs/review/project_overlays/<project>/...
  retrieve only in current project mode.

archived overlay:
  does not participate in default retrieval.
  project end or overlay cleanup should move it out of active project retrieval.
```

Confirmation must be an event, not a semantic similarity guess:

```text
semantic match may create suggestion.
explicit confirmation creates confirmed overlay.
```

Minimal overlay entry:

```yaml
overlay_entry:
  target_ref:
  target_selector:
  motivation: borrowing | adapting | avoiding | comparing | watching
  project_id:
  borrow_scope:
  project_non_borrow_scope:
  reopen_trigger:
  target_hint:
  updated_at:
```

This borrows the Web Annotation distinction:

```text
body / target / motivation stay separate.
```

`project_non_borrow_scope` rules:

```text
1. Use project-local language:
   "For project X, do not currently borrow ... because ..."
   not "This is wrong."

2. Include a reopen trigger:
   "Reopen if project goal changes from A to B" or
   "Reopen if a heavy review finds cross-project negative knowledge."

3. Default status is candidate boundary note:
   it becomes reusable negative knowledge only after heavy review.
```

### 4. Review Pressure

```yaml
review_pressure: none | review_due | blocked
```

Meaning:

| Value | Meaning | Runtime effect |
|---|---|---|
| `none` | No special review pressure. | normal boundary rules |
| `review_due` | Negative feedback, broken anchor risk, source change, or scope mismatch needs review. | warn / route to review |
| `blocked` | Anchor missing, snapshot lost, representation uncertain, or critical scope gap. | block action-facing path |

Rule:

```text
review_pressure can attach to any lifecycle state.
```

## Short Lifecycle

### Main States

```yaml
lifecycle_state:
  source_registered:
    default_use: "来源登记、找回、快照。"
    action_basis_allowed: false

  light_findable:
    default_use: "普通可找回材料。"
    action_basis_allowed: false

  candidate_provisional:
    default_use: "候选蒸馏、项目探索、比较。"
    action_basis_allowed: false

  heavy_review_open:
    default_use: "显式 claim / anchor / warrant / scope / risk 审查中。"
    action_basis_allowed: false_until_review_passes

  reviewed_promoted:
    default_use: "正式 reviewed knowledge / decision / adopted pattern。"
    action_basis_allowed: conditional_on_scope_and_warrant

  archived_cold:
    default_use: "历史保留，不参与默认激活。"
    action_basis_allowed: false
```

### Default Field Combinations

| Lifecycle state | processing_tier | knowledge_status | overlay_state | review_pressure |
|---|---|---|---|---|
| `source_registered` | `light` | `raw` | `none` | `none` |
| `light_findable` | `light` | `raw` | `none` | `none` |
| `candidate_provisional` | `medium` | `candidate` | `none/suggested/confirmed` | `none/review_due` |
| `heavy_review_open` | `heavy` | `candidate` | `none/confirmed` | `review_due/blocked/none` |
| `reviewed_promoted` | `heavy` | `reviewed` | `none/confirmed` | `none/review_due` |
| `archived_cold` | `light/medium/heavy` | `raw/candidate/reviewed` | `none/confirmed/archived` | `none` |

Important:

```text
reviewed_promoted is the only state that can feed action basis,
and even then only with scope / warrant / risk checks.
```

## Transitions

### Upgrade

```text
source_registered -> light_findable:
  source is saved and findable.

light_findable -> candidate_provisional:
  structured distillation is useful,
  current project relevance is strong,
  or clear candidate points appear.

candidate_provisional -> heavy_review_open:
  architecture change requested,
  decision/action basis use requested,
  risk-sensitive answer requested,
  strong relation proposed,
  reviewed knowledge promotion requested,
  or normative should/must/adopt/reject language would be used.

heavy_review_open -> reviewed_promoted:
  claim + evidence + warrant + scope + risk/gap passes review.
```

### Downgrade / Block

```text
heavy_review_open -> candidate_provisional:
  claim, anchor, warrant, scope, gap, or risk is incomplete.

any state + review_pressure=review_due:
  negative feedback, broken anchor, source changed, scope mismatch, or conflict.

any state + review_pressure=blocked:
  missing anchor, lost snapshot, uncertain representation, or action-facing path
  would depend on candidate-only material.

any state -> archived_cold:
  long-term no use, project ended, overlay cleared, or source stale.
```

## Derived Retrieval Policy

`retrieval_policy` should be derived from the four dimensions, not used as a
separate authority state.

```yaml
retrieval_policy:
  discoverable:
  default_scope:
  pack_allowed:
  action_basis_allowed:
  rank_behavior:
  warning_code:
```

Suggested derivation:

| Condition | pack_allowed | action_basis_allowed | rank_behavior | warning_code |
|---|---|---|---|---|
| `knowledge_status=raw` | `drilldown_required` | `false` | `normal` | `raw_is_provenance_only` |
| `knowledge_status=candidate` | `activation_only` | `false` | `downrank_for_action` | `candidate_not_action_basis` |
| `overlay_state=suggested` | `false` | `false` | `reviewer_only` | `overlay_unconfirmed` |
| `overlay_state=confirmed` | `activation_only` | `false` | `project_scope_only` | `overlay_not_authority` |
| `overlay_state=archived` | `false` | `false` | `exclude_by_default` | `overlay_archived` |
| `review_pressure=review_due` | `drilldown_required` | `false` | `warn` | `review_due` |
| `review_pressure=blocked` | `false` | `false` | `exclude_from_action` | `blocked_anchor_or_scope` |
| `lifecycle_state=reviewed_promoted` | `span_ready_if_anchored` | `requires_scope_warrant` | `normal` | `scope_check_required` |
| `lifecycle_state=archived_cold` | `manual_drilldown_only` | `false` | `exclude_by_default` | `archived_cold` |

Hard rule:

```text
retrieval relevance, overlay fit, processing tier, and trace lineage do not
create evidence support.
```

### Retrieval Bucket Policy

Do not use one mixed retrieval pool for all authority levels.

Preferred order:

```text
1. select mode
2. filter by authority bucket / policy
3. run lexical + vector + optional graph/search inside the allowed bucket
4. fuse relevance signals inside that bucket
5. compile pack with status labels
```

Mode rules:

| Mode | Default buckets | Candidate / overlay use | Action-facing rule |
|---|---|---|---|
| `action_review` | reviewed only; raw anchors for evidence check | review input only | v0.2.13 required |
| `orientation` | reviewed + candidate + confirmed overlay | allowed, must mark provisional/candidate | no action basis |
| `source_inspection` | raw + candidate | allowed for backsource/distillation | no action basis |
| `project_exploration` | reviewed + candidate + confirmed overlay for current project | allowed for exploration | should/must/adopt/reject triggers v0.2.13 |

RRF / hybrid rule:

```text
RRF may fuse lexical, semantic, sparse, metadata, or graph relevance signals
inside the same authority bucket.

RRF must not merge raw/candidate/reviewed/overlay into one authority-blind list.
```

## Promotion Gate

```yaml
promotion_gate:
  v0_2_13_trigger: no | conditional | yes
  trigger_reason:
    - architecture_adoption
    - decision
    - action_basis
    - reviewed_knowledge
    - risk_sensitive_answer
    - strong_relation
    - normative_language
    - conflict_resolution
    - negative_knowledge_promotion
  required_packet:
    - claim
    - evidence_anchor
    - warrant
    - scope
    - risk_gap
    - open_review
  gate_status: not_triggered | blocked | ready_for_review | passed | failed | parked
```

Default:

```yaml
lifecycle_state: candidate_provisional
processing_tier: medium
knowledge_status: candidate
promotion_gate:
  v0_2_13_trigger: no
  gate_status: not_triggered
```

If action-facing use is attempted:

```yaml
promotion_gate:
  v0_2_13_trigger: yes
  gate_status: blocked
  block_reason: "candidate material cannot support action basis without heavy review"
```

## Provenance / Lineage

Use a minimal PROV-inspired chain:

```yaml
lineage:
  entity_id:
  entity_type: source_card | candidate_distillation | overlay | review_packet | reviewed_note
  was_derived_from:
  was_revision_of:
  generated_by_activity:
  activity_time:
  responsible_agent:
```

Boundary:

```text
lineage explains origin.
lineage does not create authority.
```

Anchor / selector rule:

```text
Anchors should point back to the raw snapshot or stable source location.
Prefer selector-like fields over loose quotes:
  fragment
  text_quote
  text_position
  timestamp
  commit_sha
  branch_or_tag
  page
  line_range
  snapshot_ref
```

Minimal VAKS chain:

```text
source card
-> candidate distillation
-> optional project overlay
-> heavy review packet
-> reviewed claim / adopted pattern / decision / action basis
```

## Negative Knowledge

`project_non_borrow_scope` is useful, but before review it is still project-scoped
candidate negative knowledge.

```yaml
negative_signal:
  status: none | candidate | review_due | reviewed
  source_ref:
  project_scope:
  avoid_text:
  why_avoid:
  expires_or_review_due:
```

Flow:

```text
bad use / friction / failure
-> feedback_event
-> negative_signal candidate
-> review_due if repeated or high impact
-> reviewed_negative_knowledge only after review
```

Do not do:

```text
one bad experience -> global anti-pattern
project-specific non_borrow -> universal reviewed negative knowledge
feedback thumbs-down -> truth update
```

## Feedback Cache

Feedback Cache should be append-only.

It records use experience and review pressure. It must not edit source cards,
candidate distillations, reviewed notes, decisions, or truth confidence in
place.

Minimal event kinds:

| event_kind | Purpose | Truth effect |
|---|---|---|
| `useful_orientation` | Locally improves activation / routing for similar context. | none |
| `misleading_orientation` | Locally downranks and may create review_due. | none |
| `scope_mismatch` | Adds scope hint / project boundary reminder. | none |
| `anchor_broken_or_source_changed` | Sets blocked or review_due. | none |

Required feedback event scope:

```yaml
feedback_event:
  record_kind:
  target_ref:
  event_kind:
  observed_in_context:
  event_time:
  review_pressure_effect:
  project_ref:
```

Recommended optional refs:

```yaml
query_run_ref:
source_intake_state_at_time:
task_mode:
operator_note:
```

Feedback flow:

```text
feedback first writes an event.
event may tune retrieval heuristics within the same project/context.
repeated negative feedback or action-facing misleading use creates heavy review trigger.
only heavy review can produce a reviewed boundary note, superseding decision,
or reviewed relation scope update.
```

Scope rule:

```text
feedback must be narrow by default.
Bind it to project_ref or observed_in_context.
Without review, do not globalize a local failure into a universal ban.
```

PROV-style boundary:

```text
feedback event is a new event / derivation.
It is not direct mutation of the old entity's truth value.
```

Forbidden:

```text
truth_confidence_delta
source_reliability_delta
auto_mutate_reviewed_note
global_negative_knowledge_without_review
```

## Failure Matrix

| Failure case | Bad result | Minimal guardrail |
|---|---|---|
| Medium candidate written in normative style and cited by default QA. | Candidate becomes rule. | `knowledge_status + retrieval_policy` hard filter; action mode excludes candidate. |
| Semantic match directly writes persistent Project Overlay. | Project pollution and stale overlay. | Suggested overlay only in trace; confirmed overlay requires explicit event. |
| `project_non_borrow_scope` read as universal ban. | One project experience pollutes all projects. | Project-scoped wording + `reopen_trigger`; candidate-only by default. |
| Candidate summary outranks raw anchor. | Pretty summary replaces original evidence. | Raw/reviewed/candidate bucket filtering; candidate is orientation, not evidence. |
| One successful feedback makes source "more true". | Feedback pollutes truth. | Append-only feedback; only activation/review pressure changes. |
| Source page/repo/video version changes. | Old anchor pretends to still resolve. | `snapshot_ref_or_source_date` + selector; broken anchor becomes blocked. |
| Heavy review note has unresolved gaps but is cited. | Unresolved review becomes conclusion. | `heavy_review_open` excluded from default answer pool. |
| Archived overlay still appears in retrieval. | Historical sidecar misleads current work. | `overlay_state=archived` excluded by default; project closeout drains active overlay. |

## Seven Minimal Guardrails

```text
1. Light / Medium / Heavy = processing_tier only.
2. authority / retrieval_warning = knowledge_status / retrieval_policy / promotion_gate.
3. suggested overlay and confirmed overlay stay separate; suggested is trace-only.
4. borrow / do-not-borrow leaves medium candidate; candidate keeps routing_hint only.
5. action-facing evidence anchors must return to raw snapshot or stable representation.
6. Feedback Cache is append-only, narrow-scope, activation/review-pressure only.
7. Retrieval filters by authority bucket before hybrid / RRF; never one mixed pool.
```

## Field Checklist Candidate

### Source Card

Required:

```yaml
record_kind:
source_type:
source_url:
raw_location:
captured_at:
snapshot_ref_or_source_date:
topics:
why_saved:
knowledge_status: raw
processing_tier: light | medium | heavy
```

Optional:

```yaml
representation_hint:
license_or_access:
canonical_url:
```

Forbidden:

```text
adopt/reject verdict
confidence
truth score
```

### Candidate Distillation

Required:

```yaml
record_kind:
derived_from:
knowledge_status: candidate
processing_tier: medium
retrieval_policy: orientation_only
promotion_gate: v0_2_13_required
```

Optional:

```yaml
candidate_points:
open_questions:
routing_hint:
possible_project_refs:
point_anchor_refs:
```

Forbidden:

```text
architecture decision
action basis
formal pattern
borrow_scope as project conclusion
project_non_borrow_scope as project conclusion
```

Boundary:

```text
Medium candidate may say where it might route.
Medium candidate must not decide what a project should borrow or avoid.
That belongs in Project Overlay.
```

### Project Overlay Note

Required:

```yaml
record_kind:
project_id:
target_ref:
overlay_state:
overlay_scope: project_sidecar_only
borrow_scope:
project_non_borrow_scope:
reopen_trigger:
target_hint:
promotion_gate: v0_2_13_required
last_checked_at:
```

Optional:

```yaml
confirmation_basis:
expires_at:
short_reason:
```

Forbidden:

```text
decision outcome
confidence
residual risk
review verdict
universal ban
```

### Heavy Review Note

Required:

```yaml
claim:
evidence_anchors:
non_circular_warrant:
scope:
gaps:
residual_risk:
review_status:
```

Optional:

```yaml
counterevidence:
reviewer:
```

Forbidden:

```text
auto-pass
truth score
```

### Feedback Event

Required:

```yaml
record_kind:
target_ref:
event_kind:
observed_in_context:
event_time:
review_pressure_effect:
project_ref:
```

Optional:

```yaml
query_run_ref:
project_ref:
note:
```

Forbidden:

```text
truth_confidence_delta
auto-mutate reviewed note
```

## Minimal Header Candidate

For medium candidate distillations:

```yaml
source_intake:
  lifecycle_state: candidate_provisional
  processing_tier: medium
  knowledge_status: candidate
  overlay_state: none
  review_pressure: none
  retrieval_policy:
    discoverable: true
    pack_allowed: activation_only
    action_basis_allowed: false
    rank_behavior: downrank_for_action
    warning_code: candidate_not_action_basis
  routing_hint:
  possible_project_refs:
  promotion_gate:
    v0_2_13_trigger: no
    gate_status: not_triggered
  lineage:
    was_derived_from:
    generated_by_activity:
    responsible_agent:
```

For confirmed Project Overlay:

```yaml
source_intake:
  lifecycle_state: candidate_provisional
  processing_tier: medium
  knowledge_status: candidate
  overlay_state: confirmed
  review_pressure: none
  retrieval_policy:
    discoverable: true
    default_scope: project_only
    pack_allowed: activation_only
    action_basis_allowed: false
    rank_behavior: project_scope_only
    warning_code: overlay_not_authority
  project_mount:
    project_id:
    target_ref:
    target_selector:
    motivation:
    borrow_scope:
    project_non_borrow_scope:
    reopen_trigger:
    target_hint:
  promotion_gate:
    v0_2_13_trigger: conditional
    trigger_reason:
      - architecture_adoption
      - decision
      - action_basis
    gate_status: not_triggered
```

For heavy review:

```yaml
source_intake:
  lifecycle_state: heavy_review_open
  processing_tier: heavy
  knowledge_status: candidate
  overlay_state: none | confirmed
  review_pressure: review_due | blocked | none
  promotion_gate:
    v0_2_13_trigger: yes
    gate_status: ready_for_review | blocked
```

## Candidate Lint Rules

Future script / skill checks:

```text
1. processing_tier=heavy must not imply knowledge_status=reviewed.
2. knowledge_status=candidate must imply action_basis_allowed=false.
3. overlay_state=suggested must not be written as a durable vault note.
4. overlay_state=suggested must not enter ordinary context packs.
5. overlay_state=confirmed must be created by explicit confirmation or explicit project-intake write permission.
6. overlay_state=confirmed must be project_scope_only unless user expands scope.
7. overlay_state=archived must be excluded from default retrieval.
8. review_pressure=blocked must exclude action-facing use.
9. candidate_provisional with should/must/adopt/reject wording must trigger heavy_review_open.
10. Candidate distillation must not contain project-level borrow_scope or project_non_borrow_scope conclusions.
11. project_non_borrow_scope must include project-local wording and a reopen_trigger.
12. project_non_borrow_scope cannot become reviewed negative knowledge without review.
13. Anchor refs should use selector-like fields, not only pasted quotes.
14. Do not use authority / retrieval_warning / promotion_required as execution fields; use knowledge_status / retrieval_policy / promotion_gate.
15. RRF/hybrid fusion must stay inside an allowed authority bucket.
16. retrieval rank / dashboard hit / overlay stance cannot become truth confidence.
```

## What To Change Now vs Later

### Now Design

```text
short lifecycle
four orthogonal dimensions
derived retrieval policy
retrieval bucket policy
promotion gate trigger rules
overlay sidecar shape
candidate lint rules
field checklist and naming repairs
```

### Next Stage

```text
tool/script support:
  source-router
  candidate-frontmatter linter
  overlay-suggestion generator
  retrieval-policy filter
  review_due emitter
```

### Parked

```text
mainline schema change
automatic promotion
full W3C Annotation / PROV implementation
full ADR/MADR conversion for overlays
global negative knowledge system
observability platform
```

## Current Compatibility Note

Current `SOURCE_INTAKE.md` already contains:

```text
light / medium / heavy
Medium Provisional Identity
Project Overlay Gate
```

This candidate design sharpens it:

```text
Light / Medium / Heavy
-> processing_tier only

candidate / reviewed
-> knowledge_status

Project Overlay
-> overlay_state + project_mount sidecar

free-text warning
-> derived retrieval_policy + promotion_gate

authority / retrieval_warning / promotion_required
-> knowledge_status / retrieval_policy / promotion_gate

non_borrow_scope
-> project_non_borrow_scope inside Project Overlay only
```

## Provisional Verdict

```text
recommendation: adopt as candidate design direction
mainline now: no
write target if accepted later: SOURCE_INTAKE.md + Codex skill + future toolchain lint
risk if not adopted: candidate and overlay material will keep looking like authority in retrieval
main risk if over-adopted: intake becomes too bureaucratic for ordinary sources
```

## Sources Used

- W3C Web Annotation Data Model: https://www.w3.org/TR/annotation-model/
- W3C PROV namespace: https://www.w3.org/ns/prov/
- MADR: https://adr.github.io/madr/
- NASA Lessons Learned: https://www.nasa.gov/nasa-lessons-learned/
