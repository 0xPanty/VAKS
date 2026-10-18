---
type: implementation-note
status: active
created: 2026-05-28
updated: 2026-06-06
project: verified-action-knowledge-system
scope:
  - source-intake
  - processing-tier
  - ux
  - provenance
related_files:
  - "[[SCHEMA]]"
  - "[[IMPLEMENTATION_BLUEPRINT]]"
  - "[[DEV_CONTEXT]]"
  - "[[MEMORY_TIER]]"
  - "[[REFERENCE_REVIEW_PROTOCOL]]"
  - "[[templates/source-record]]"
  - "[[templates/video-source]]"
  - "[[templates/candidate-distillation]]"
  - "[[templates/review-candidate]]"
  - "[[templates/query-run]]"
  - "[[templates/feedback-event]]"
  - "[[templates/project-overlay]]"
verification_status: active
evidence_level: synthetic
confidence: high
last_verified: 2026-06-06
next_review: 2026-06-13
tags:
  - source-intake
  - processing-tier
  - karpathy-simple
  - source-provenance
  - video-intake
---

# SOURCE_INTAKE.md v0.1

## AI-readable preamble

This file defines how incoming material should be handled without making everyday use heavy.

The rule is:

```text
Karpathy for normal intake.
Dusk-style dashboard for project use.
Verified-action strictness only for strong sources and action-bearing knowledge.
```

Do not run the full verified-action process on every note.

## 1. Core Judgment

Not all material deserves the same processing depth.

Use three levels:

```text
light:
  capture and keep findable.

medium:
  summarize and route.

heavy:
  preserve provenance, extract points, compare, review, and write durable patterns/decisions/risks.
```

The goal is to avoid both extremes:

```text
too light:
  AI summaries become untraceable and unreliable.

too heavy:
  every ordinary note becomes paperwork.
```

## 1.1 Machine-Readable Boundary Fields

Do not collapse processing effort, truth status, project mounting, and review
pressure into one field.

Use these orthogonal fields:

| Field | Values | Meaning |
|---|---|---|
| `processing_tier` | `light` / `medium` / `heavy` | How much work has been done. This is not authority. |
| `knowledge_status` | `raw` / `candidate` / `reviewed` | Whether the record can act as knowledge. |
| `overlay_state` | `none` / `suggested` / `confirmed` / `archived` | Whether a project sidecar is mounted or retained as history. |
| `review_pressure` | `none` / `review_due` / `blocked` | Whether feedback or anchor problems require review. |
| `retrieval_policy.policy_kind` | `source_identity_only` / `orientation_only` / `project_context_only` / `reviewed_support_only` | How retrieval is allowed to use the record. |
| `retrieval_policy.pack_allowed` | `false` / `activation_only` / `review_input_only` / `drilldown_required` / `reviewed_support` | Whether this record can enter a context pack, and for what purpose. |
| `retrieval_policy.action_basis_allowed` | `true` / `false` | Whether this record can directly support action. Candidate material defaults to false. |
| `retrieval_policy.warning_code` | short machine-readable string | Why the record is limited. |
| `promotion_gate` | `none` / `v0_2_13_required` / `review_passed` | What gate must pass before promotion or action use. |

Minimal object rules:

```text
Source Card:
  record_kind: source_card
  knowledge_status: raw
  retrieval_policy:
    policy_kind: source_identity_only
    pack_allowed: drilldown_required
    action_basis_allowed: false
    warning_code: raw_is_provenance_only
  review_pressure: none, unless anchor/source is broken
  action_basis_allowed: false
  no adopt/reject verdict, no truth score

Candidate Distillation:
  record_kind: candidate_distillation
  knowledge_status: candidate
  processing_tier: medium
  retrieval_policy:
    policy_kind: orientation_only
    pack_allowed: activation_only
    action_basis_allowed: false
    warning_code: candidate_not_action_basis
  promotion_gate: v0_2_13_required
  no project-level borrow verdict

Project Overlay:
  record_kind: project_overlay
  knowledge_status: candidate
  overlay_scope: project_sidecar_only
  overlay_storage: confirmed_persistent_project_bucket
  retrieval_scope: active_project_only
  default_retrieval: false
  retrieval_policy:
    policy_kind: project_context_only
    default_scope: project_only
    pack_allowed: activation_only
    action_basis_allowed: false
    warning_code: overlay_not_authority
  project_borrow_scope / project_non_borrow_scope / project_reopen_trigger / target_hint
  no decision outcome, no review verdict, no universal ban

Heavy Review:
  claim + evidence_anchors + non_circular_warrant + scope + gaps + residual_risk
  review_status controls promotion

Feedback Event:
  event_kind + observed_in_context + review_pressure_effect
  project_ref or explicit observed context
  retrieval_policy:
    policy_kind: project_context_only
    pack_allowed: review_input_only
    action_basis_allowed: false
    warning_code: feedback_not_truth
  forbidden_truth_mutation_fields_absent: true
  reviewed_note_mutation_allowed: false
  source_reliability_mutation_allowed: false
```

## 2. Processing Levels

### Light Processing

Use for:

```text
ordinary articles
interesting but unproven ideas
temporary references
small notes
low-impact links
material saved for possible future lookup
```

Minimum record:

```text
source link or file path
title
author/publisher if obvious
captured_at
why saved
short note or summary
current status
```

Do not require:

```text
confidence
evidence_level
relations
negative_evidence
formal review
pattern extraction
```

### Medium Processing

Use for:

```text
material likely to be reused
project background
useful references for a current question
docs that may enter a dev context
sources with clear but not architecture-changing ideas
```

Add:

```text
structured summary
tags/topics
source status
possible related files
candidate points
open questions
whether it belongs in a scope dashboard or dev context
```

Medium processing can feed:

```text
index
scope dashboard
context briefing
DEV_CONTEXT support or cold references
```

It still does not create truth.

#### Medium Provisional Identity

Every medium candidate distillation must carry an explicit provisional identity.

Required markers:

```yaml
record_kind: candidate_distillation
provisional: true
knowledge_status: candidate
processing_tier: medium
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
```

This is a retrieval guard, not paperwork.

Use enum-like fields instead of free-text warnings. A future retrieval layer
must be able to filter these records mechanically.

When an agent later sees a medium candidate in search results or a context
briefing, it must treat the file as:

```text
useful for orientation
useful for candidate ideas
useful for project discussion
not a rule
not a reviewed pattern
not action basis
not evidence support by itself
```

Medium candidate files may include:

```text
candidate_points
open_questions
routing_hint
possible_project_refs
point_anchor_refs
```

Medium candidate files must not include project-level adoption conclusions:

```text
architecture decision
action basis
formal pattern
borrow_scope / non_borrow_scope as project conclusion
```

If project-specific borrowing is needed, put it in Project Overlay instead.

### Project Overlay Gate

Project Overlay is not a normal tag.

It is a project-scoped sidecar that records:

```text
project usable range / project_borrow_scope
project forbidden range / project_non_borrow_scope
reopen condition / project_reopen_trigger
possible target layer / target_hint
```

Storage rule:

```text
write confirmed overlays under outputs/review/project_overlays/<project_id>/ or
another explicit project overlay / lens folder.
do not rewrite raw source metadata to express project fit.
```

Default automation rule:

```text
source/project semantic match may create a suggested overlay only in query-run
trace, agent trace, or a temporary suggestion inbox.
suggested overlay does not enter the long-term vault and does not participate in
default retrieval.
confirmed Project Overlay requires user confirmation or an explicitly active
project-intake task.
```

For ordinary source intake, do this:

```text
source card
ordinary tags/topics
candidate distillation if useful
suggested_project_overlay: yes/no
```

Only after confirmation, do this:

```text
write Project Overlay Card
set project_id
write project_borrow_scope / project_non_borrow_scope / project_reopen_trigger / target_hint
```

Suggested overlay trace markers:

```yaml
record_kind: query_run_trace | overlay_suggestion
knowledge_status: candidate
overlay_state: suggested
overlay_scope: project_sidecar_only
retrieval_policy:
  policy_kind: project_context_only
  pack_allowed: false
  action_basis_allowed: false
  warning_code: overlay_unconfirmed
persistent_overlay_allowed: false
default_retrieval_allowed: false
action_basis_allowed: false
truth_mutation_allowed: false
```

Confirmed Project Overlay markers:

```yaml
record_kind: project_overlay
knowledge_status: candidate
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
```

Archived Project Overlay markers:

```yaml
record_kind: project_overlay
knowledge_status: candidate
overlay_state: archived
overlay_scope: project_sidecar_only
retrieval_scope: archived_excluded
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  pack_allowed: false
  action_basis_allowed: false
  warning_code: archived_overlay_excluded
action_basis_allowed: false
truth_mutation_allowed: false
```

`project_non_borrow_scope` is the first field to read when using an overlay. It
is the project-level warning lane. It is not yet formal negative knowledge, but
it should stop agents from borrowing a source in the known-bad direction.

Hard rules for `project_non_borrow_scope`:

```text
use project-local language, not universal truth language.
Do not write a universal ban.
include why this project should avoid the borrowing direction.
include a reopen trigger for when the boundary should be reconsidered.
```

Good shape:

```text
For project VAKS, do not currently borrow X as Y because Z.
Reopen if the project goal changes to A, or if a later heavy review supports B.
```

Bad shape:

```text
X is wrong.
Never use X.
```

Confirmed overlays are project-mode context. Non-project queries should not read
them by default. Archived overlays do not participate in default retrieval.

### Retrieval Bucket Policy

Do not retrieve raw, candidate, overlay, and reviewed records from one mixed pool
and let relevance ranking imply authority.

Use bucketed retrieval first, then merge relevance signals inside the allowed
bucket:

```text
action / review mode:
  default: reviewed records only
  optional: raw anchors for evidence checks
  candidate / overlay: review input only, not final support

orientation mode:
  reviewed + candidate + confirmed overlay
  output must mark candidate/provisional material explicitly

source inspection mode:
  raw + candidate
  goal is source lookup, comparison, and distillation

project exploration mode:
  reviewed + candidate + confirmed overlay for the active project only
  any should / must / adopt / reject language triggers v0.2.13
```

Hybrid retrieval, lexical search, vector search, and RRF may combine relevance
signals inside an allowed bucket. They must not merge authority levels.

```text
RRF can merge relevance signals inside reviewed.
RRF can merge relevance signals inside candidate.
RRF can merge relevance signals inside active-project overlay.
RRF cannot merge across authority buckets.
RRF must not merge raw / candidate / reviewed / overlay into one authority-like list.
```

### Heavy Processing

Use only for strong sources:

```text
papers
valuable repositories
official specs/docs
high-signal technical articles
important design discussions
materials that can validate or falsify our architecture
sources that affect project direction
risks, anti-patterns, failure reports
sources likely to become action basis
```

Add:

```text
full provenance
PROV-inspired trace when the source is medium/heavy
author / organization
published_at / updated_at
captured_at
version / commit / DOI / release
source_status: active | legacy | deprecated | unknown
timeline notes
files or sections reviewed
source/code anchors
candidate points
supports / contradicts / refines / risk_of / derived_from relations
what we adopt
what we reject
risk and anti-pattern extraction
fit with current branch
fit with whole architecture
```

Heavy processing can create:

```text
source record
architecture review
pattern
anti-pattern
decision
review queue item
maintenance manifest
decision outcome record
implementation-note
index update
handoff update
```

### Video Source Intake

Video is a source format, not a truth format.

Use `raw/videos/` and `templates/video-source.md` for useful Bilibili, YouTube, course, lecture, interview, podcast-with-video, demo, or walkthrough material.

The borrowed product/workflow ideas are narrow:

```text
batch links instead of one-by-one manual handling
platform-aware source identity
public subtitles first
local ASR when subtitles are missing
timestamped transcript / segment ledger
key-entity confidence
anti-omission extraction pass
user visual check for unclear names, URLs, commands, numbers, or UI text
delete downloaded media scratch after transcript by default
copy retained text artifacts into project-visible `raw/videos/<source-slug>/`
route useful ideas into candidate points before review
```

Default processing:

```text
light:
  save source card, metadata, why saved, one-sentence summary, and uncertainty.

medium:
  add transcript or subtitle, timestamp segments, transcript metadata / ledger locations,
  project-visible artifact paths, key-entity confidence,
  anti-omission extraction, candidate points, borrow / do-not-borrow notes,
  and related VAKS layer.

heavy:
  only when the video affects architecture, decision, action basis,
  strong reviewed relation, important adoption, or explicit review.
```

Allowed direct conclusion:

```text
This video says X.
```

Not allowed without later review:

```text
X is true.
We should adopt X.
X supports a reviewed claim.
X changes confidence.
```

When upgrading video material to heavy, verify important entities and claims against stronger anchors such as official docs, project repositories, source code, release notes, screenshots / key frames, or independent sources. Then route the extracted point through `REVIEW_QUEUE.md`.

Anti-omission pass:

```text
pain point:
  What real user problem is the source solving?

workflow:
  What is the full input -> process -> output path?

tools / plugins:
  Which Obsidian plugins, AI tools, platforms, commands, or services appear?

information structure:
  How are notes, files, tags, links, databases, cards, folders, or dashboards organized?

judgment mechanism:
  How does the source decide what is useful, reliable, worth keeping, or worth acting on?

user experience:
  What becomes easier or harder than our current workflow?

automation boundary:
  Which steps are automatic, which stay manual, and where can automation mislead?

risk:
  What can pollute knowledge, create false authority, lose context, or become a junk pile?

fit for us:
  What can replace self-built design, reduce scope, or fill a gap?

challenge to us:
  Does this show our framework is too heavy, too slow, missing UI/workflow, or solving the wrong problem?
```

If a video / post digest only says "what it is about" but does not cover pain point, workflow, tools / plugins, risks, and VAKS comparison, the digest is incomplete.

If a medium / heavy video card says transcript or segments are `inline` but the full transcript or timestamp segments are only stored in `.codex` scratch, the writeback is incomplete. Copy the retained text artifacts into `raw/videos/<source-slug>/` or the formal Obsidian vault, then point the source card to those paths.

## 3. What "Preserve Source" Means

Preserving source means giving important knowledge an identity card.
For strong sources, it can also record a small handling trail:

```text
source identity:
  what the source is

capture / extraction:
  who or what captured and extracted it

agent:
  simple human/model/tool strings
```

This does not make capture heavy. Light sources keep the minimal identity fields; medium/heavy sources may add extraction and optional provenance details.

Review, promotion, and context-pack usage are not stored as source main fields. They belong to reviewed nodes, promotion records, context packs, or the use ledger.

For a repository:

```yaml
source_id:
source_uri:
source_url:
owner:
repo:
checked_commit:
commit_time:
captured_at:
captured_by:
extracted_by:
extracted_at:
extraction_tool:
extraction_model:
source_status: active | legacy | deprecated | unknown
files_reviewed:
source_anchor_matrix:
why_captured:
extracted_points:
not_adopted:
timeline_notes:
```

For user directives, explicit corrections, preferences, decisions, or action instructions that affect durable knowledge or action:

```yaml
verbatim_input:
model_interpretation:
intent_confirmation:
  restated_intent:
  assumptions:
  scope_in:
  scope_out:
  success_criteria:
```

Do not require `verbatim_input` / `model_interpretation` for ordinary article, repository, paper, or source capture.

For evidence that may support promotion, strong reviewed relations, decisions, or action basis, preserve a source anchor rather than only a source link:

```yaml
source_anchor:
  url_or_path:
  exact_quote:
  prefix:
  suffix:
  captured_at:
```

For heavy, high-drift, or action-relevant sources, add optional stability fields:

```yaml
source_anchor:
  position:
  content_hash:
  archived_url:
  checked_latest_at:
  source_changed: unknown | yes | no
```

For durable source intake, add source identity fields when duplicate capture,
replacement, or later recompile is likely:

```yaml
source_identity:
  content_hash:
  hash_algorithm: sha256
  origin_uri:
  origin_label:
  raw_path:
  source_record_path:
  previous_content_hash:
  source_changed: unknown | yes | no
  ingest_decision: new_source | idempotent_skip | preserve_new_origin | replacement_candidate | orphan_review_due
  compiled_outputs: []
  referenced_by: []
  review_due_reason:
```

Rules:

```text
Markdown source record is primary.
The hash registry is derived and rebuildable.
Same origin + same hash may skip duplicate compile.
Same hash + different origin must preserve the new origin/provenance.
Same origin + changed hash creates a replacement/recompile candidate.
Missing raw source that is already referenced becomes orphan/review_due, not silent deletion.
Source hash is not evidence support, truth confidence, approval, or action readiness.
```

Track how far the evidence was actually inspected:

```yaml
evidence_granularity: metadata_only | abstract_or_summary | excerpt_or_passage | table_or_code_anchor | full_source_reviewed
```

Rule:

```text
Source provenance tells where material came from.
Source anchor tells where the specific evidence lives.
Neither proves support by itself.
```

For a paper:

```yaml
source_id:
source_uri:
title:
authors:
published_at:
venue:
doi_or_arxiv:
version:
captured_at:
captured_by:
extracted_by:
extracted_at:
extraction_tool:
extraction_model:
key_sections_reviewed:
main_claims:
limitations:
later_updates:
fit_to_our_architecture:
```

Plain rule:

```text
Do not let an AI summary become detached from who said it, when, where, and in what version.
Do not let an AI paraphrase replace the user's original words.
```

## 4. User Experience Modes

### Normal Question Mode

Use:

```text
Karpathy-simple
```

Flow:

```text
search/read enough
answer
optionally save light note if valuable
```

Do not create:

```text
dev context pack
full review
pattern/anti-pattern
feedback-event
```

unless the material proves important.

### Project Development Mode

Use:

```text
Dusk-style scope dashboard + DEV_CONTEXT
```

Flow:

```text
project goal
-> scope dashboard / related-material briefing
-> DEV_CONTEXT Core / Support / Risk / Cold References
-> development
-> closeout
```

The dashboard is a workbench.

It is not truth.

### Strong Source / Decision Mode

Use:

```text
verified-action strictness
```

Flow:

```text
source record
-> candidate points
-> collision / comparison
-> review
-> pattern / anti-pattern / decision
-> index / handoff
```

Use this mode when the source may affect future action.

## 5. When To Upgrade Processing

Upgrade light to medium when:

```text
the source is reused
the user asks about it again
it becomes relevant to a project
it appears in search/context briefing repeatedly
```

Upgrade medium to heavy when:

```text
it changes architecture
it validates or contradicts a design
it becomes a development constraint
it exposes a risk or failure mode
it should be cited as action basis
```

Downgrade or cool after use when:

```text
it was one-off evidence
it no longer fits the active project
its value is only historical
it has been superseded
```

## 5.1 Feedback Cache For Negative Use

When a candidate, overlay, or reviewed item fails in real project use, do not
silently edit truth-layer files.

Feedback Cache is append-only.

First write a feedback event:

```yaml
event_kind:
target_ref:
project_ref:
observed_in_context:
event_time:
review_pressure_effect:
retrieval_policy:
  policy_kind: project_context_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: feedback_not_truth
forbidden_truth_mutation_fields_absent: true
reviewed_note_mutation_allowed: false
source_reliability_mutation_allowed: false
```

This cache can warn the current project immediately, but it does not mutate
reviewed knowledge.

Allowed event kinds:

| event_kind | Immediate effect | Truth effect |
|---|---|---|
| `useful_orientation` | locally improve activation / routing | none |
| `misleading_orientation` | locally reduce activation and add `review_due` | none |
| `scope_mismatch` | add scope hint / project boundary pressure | none |
| `anchor_broken_or_source_changed` | set `blocked` or `review_due` until anchor/source is checked | none |

Scope rule:

```text
Every feedback event must bind to project_ref or observed_in_context.
Do not create global negative knowledge from a local feedback event.
```

Allowed immediate updates:

```text
retrieval heuristics for the same project/context/task family
review_pressure on a target or overlay
temporary project warning
```

Forbidden immediate updates:

```text
source card rewrite
candidate note rewrite
reviewed note rewrite
truth confidence delta
universal ban
automatic superseding decision
```

Escalate to heavy review only when:

```text
the same target receives repeated negative feedback in the same scoped context
an action-facing use was misled
an anchor is broken or source changed for a record needed in review/action
the feedback would change a project boundary, decision, or reviewed relation
```

After review, it may update:

```text
project_non_borrow_scope
avoid note
negative knowledge
decision supersede record
reviewed relation scope
```

## 5.2 Intake Control Failure Matrix

Use this matrix to pressure-test Source Intake and Promotion. These are expected
agent failure modes, not rare edge cases.

| Failure case | Bad result | Minimal guardrail |
|---|---|---|
| Medium candidate is written like a rule and quoted in default answers. | Candidate is treated as rule. | Use `knowledge_status` + `retrieval_policy` filtering; action mode excludes candidates. |
| Semantic match directly creates persistent Project Overlay. | Project pollution and zombie overlays. | Suggested overlay stays in trace/inbox only; confirmed overlay is the only persistent overlay. |
| `project_non_borrow_scope` is read as a universal ban. | One project experience pollutes every project. | Field name keeps project scope; require `project_reopen_trigger`; default candidate-only. |
| Candidate summary outranks raw anchor. | Polished summary replaces original evidence. | Bucket raw / candidate / reviewed separately; candidate is orientation, not evidence. |
| One successful use makes a source seem "more true". | Feedback mutates truth. | Feedback is append-only; it can affect activation and review pressure only. |
| Source page, repository, or video version changes. | Old anchor pretends to still point to current source. | Require `snapshot_ref_or_source_date` and selector-style anchors; broken anchors set `blocked` or `review_due`. |
| Heavy review is open but not passed, yet agent cites it. | Unresolved gaps become conclusions. | `heavy_review_open` is excluded from default answer pools until review passes. |
| Archived overlay remains in retrieval. | Historical sidecar keeps misleading current work. | Archived overlays are excluded from default retrieval; project closeout drains active overlays. |
| Confirmed overlay is read outside the active project. | One project's sidecar contaminates another project. | Require `retrieval_scope: active_project_only`; non-active-project retrieval excludes it. |
| Project overlay is written like an ADR or decision. | Candidate project guidance becomes adoption. | Forbid decision outcome, review verdict, action basis, and universal ban in overlay records. |

### Action-Facing Anchor Rule

For promotion, decision, strong reviewed relation, risk-sensitive answer, or
action basis, evidence anchors must return to raw source material or a stable
representation.

Allowed anchors:

```text
raw snapshot path
stable source URL plus captured date
commit SHA / branch / file path / line range
page / section / fragment selector
quote selector with enough surrounding context
timestamp / segment id for transcript or video
hash or stored artifact path when available
```

Forbidden as final support anchors:

```text
candidate distillation
project overlay
briefing summary
retrieval score
graph relation
LLM evaluator output
feedback event
```

These forbidden items may route review or orientation, but they cannot be the
final evidence anchor for action-facing support.

## 6. Non-negotiable Boundaries

```text
Capture must stay easy.
Strong sources must remain traceable.
Important evidence should carry a source anchor, not just a URL.
Evidence granularity must stay visible: metadata-only or summary-only material cannot silently become high-confidence support.
Heavy source digests should include an omission check for missing risks, missing scope limits, likely dropped facts, and whether full source read is needed.
Dashboard state is not truth.
Retrieval rank is not trust.
Repeated appearance is a signal, not proof.
Heavy review is for promotion and action, not ordinary saving.
Evidence support and evidence sufficiency checks are lazy gates: use them for promotion, decision, strong relation, action basis, or explicitly challenged points, not for ordinary capture.
Association neighborhood activation is also lazy: use it for query/context-pack preparation, promotion review, action basis, or explicit contradiction/risk checks, not for ordinary source capture.
Graph traversal, PPR, similarity, and association score can suggest what to inspect next; they cannot create support, confidence, reviewed relations, or action readiness.
Graph retrieval strata can organize context-pack preparation: low-level source/text-unit/claim/entity recall, high-level pattern/theme/community recall, and relation-neighborhood recall. TextUnit anchors are provenance, community reports are briefings, and graph rank is not trust.
Temporal applicability is checked when a point is promoted, used in a decision/action basis, or appears stale/superseded/out-of-scope; ordinary capture can leave validity windows blank rather than inventing dates.
Confidence caps are checked when a candidate is promoted or used for action: abstract/snippet/URL-only material cannot become high-confidence support without a direct source span or full-text anchor.
Intent confirmation is checked only before significant action, high-impact decision, implementation, deployment, or hard-to-rollback work.
Medium candidates are provisional by default: they require machine-filterable status and retrieval-policy markers and cannot be used as action basis without promotion.
Project overlays can be suggested automatically, but confirmed project mounting requires user confirmation or an explicitly active project-intake task.
Confirmed overlays are active-project-only by default; archived overlays are excluded from default retrieval.
Negative feedback creates review pressure first; it does not directly mutate reviewed truth.
Processing tier is not authority: `light`, `medium`, and `heavy` describe effort, while `knowledge_status` describes boundary status.
Lineage is traceability, not authority.
Feedback is scoped and append-only: it can affect activation and review pressure, but not truth confidence or reviewed notes without review.
Action-facing support must anchor to raw source material or a stable representation, not to distillation, overlay, retrieval score, evaluator output, or feedback.
Retrieval must filter by authority bucket first and fuse relevance only inside the allowed bucket.
```

### Answer Preparation / Independent Support Boundary

When a query, review, or answer draft uses a claim as support, do not let the
claim note prove itself.

Use this lightweight chain for important answer preparation:

```text
route by authority bucket
-> assemble a context / evidence envelope
-> check whether key answer claims have independent evidence/source anchors
-> draft only within supported or explicitly qualified scope
```

This is a lazy gate for answer-bearing, review-bearing, or action-adjacent use.
It is not required for ordinary source capture or casual lookup.

Rules:

```text
supported != truth
answer-ready != action-ready
claim_refs = trace handles, not proof
test / lint / blind review = diagnostic process evidence, not reviewer approval
claim note cannot self-support
independent evidence/source anchor is required before a claim can count as support
missing independent anchor means not_ready, weak, missing_anchor, or scope_limited
scope overclaim must be blocked or narrowed
```

Allowed independent anchors include:

```text
raw source material
source snapshot
source summary or architecture review with inspected anchors
code/file/line selector
quote / excerpt / section selector
transcript timestamp or segment
stable captured artifact with hash or version
```

Not enough by themselves:

```text
claim note repeating its own conclusion
URL-only provenance
candidate distillation
project overlay
briefing summary
retrieval score
graph rank
LLM evaluator output
test pass
blind review pass
```

Useful result states:

```text
supported: independent anchor supports the target within scope
weak: support exists but is secondary, partial, or low-granularity
missing_anchor: provenance exists but no source/evidence anchor was inspected
self_support_loop: the claim note is supporting itself
scope_limited: evidence supports a narrower conclusion than the draft says
not_ready: answer or review should not proceed as supported
```

Answer drafts, skeletons, smoke checks, or similar helpers may improve human
drafting discipline, but they do not create truth, reviewed knowledge, action
basis, or approval.

## 7. First Implementation

Do not write automation first.

First prove this manually with real material:

```text
1 light source
1 medium project reference
1 heavy repo/paper review
1 scope dashboard or dev context pack
1 closeout update
```

Only after the manual loop works should scripts or CLI commands be written.
