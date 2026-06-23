---
type: implementation-note
status: active_contract_with_migration_debt
created: 2026-05-28
updated: 2026-06-14
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
  - "[[templates/source-annotation]]"
  - "[[templates/video-source]]"
  - "[[templates/candidate-distillation]]"
  - "[[templates/review-candidate]]"
  - "[[templates/heavy-review-open]]"
  - "[[templates/query-run]]"
  - "[[templates/context-pack-manifest]]"
  - "[[templates/feedback-event]]"
  - "[[templates/project-overlay]]"
verification_status: contract_lint_pass_current_structural_pass_semantic_debt
evidence_level: synthetic
confidence: medium
confidence_basis: source annotation contract lint passed with 0 warnings and 0 errors; current lint passed structurally with existing migration warnings
last_verified: 2026-06-14
next_review: 2026-06-21
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
| `overlay_state` | `none` / `confirmed` / `archived` | Whether a persistent project sidecar is mounted or retained as history. Suggested overlays live only in trace/inbox artifacts. |
| `review_pressure` | `none` / `review_due` / `blocked` | Whether feedback or anchor problems require review. |
| `retrieval_policy.policy_kind` | `source_identity_only` / `orientation_only` / `project_context_only` / `reviewed_support_only` | How retrieval is allowed to use the record. |
| `retrieval_policy.pack_allowed` | `none` / `activation_only` / `review_input_only` / `drilldown_required` / `reviewed_support` | Whether this record can enter a context pack, and for what purpose. |
| `retrieval_policy.action_basis_allowed` | `true` / `false` | Whether this record can directly support action. Candidate material defaults to false. |
| `retrieval_policy.warning_code` | short machine-readable string | Why the record is limited. |
| `promotion_gate` | `none` / `v0_2_13_required` | What gate must be run before promotion or action use. Review outcome belongs in `review_status`, not this field. |

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

Source Annotation Sidecar:
  record_kind: source_annotation
  knowledge_status: candidate
  processing_tier: light | medium
  annotation_scope: source_local_anchor
  retrieval_policy:
    policy_kind: orientation_only
    pack_allowed: review_input_only
    action_basis_allowed: false
    warning_code: annotation_not_support
  anchor_status: exact_verified | fuzzy_recovered | ambiguous | broken | source_changed
  anchor_checked_at: last locator check date
  anchor_stale: false by default
  next_action: inspect_source_span by default
  support_checked: false by default
  evidence_support_status: not_checked by default
  no project-level borrow verdict, no truth score, no action basis

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

### 1.2 Canonical Enum Registry

The canonical machine values live in `tools/source_intake_enum_registry.json`.
Any source-intake validator, retrieval compiler, adapter, or context-pack builder
must fail closed on unknown enum values.

Core values:

| Field | Allowed values |
|---|---|
| `processing_tier` | `light`, `medium`, `heavy` |
| `knowledge_status` | `raw`, `candidate`, `reviewed` |
| `overlay_state` | `none`, `confirmed`, `archived` |
| `review_pressure` | `none`, `review_due`, `blocked` |
| `retrieval_policy.policy_kind` | `source_identity_only`, `orientation_only`, `project_context_only`, `reviewed_support_only` |
| `retrieval_policy.pack_allowed` | `none`, `activation_only`, `review_input_only`, `drilldown_required`, `reviewed_support` |
| `retrieval_policy.action_basis_allowed` | `true`, `false` |
| `retrieval_policy.warning_code` | registry-controlled warning code |
| `promotion_gate` | `none`, `v0_2_13_required` |
| `pack_role` | `orientation`, `review_input`, `support`, `anchor` |
| `support_result` | `supported`, `weak`, `missing_anchor`, `self_support_loop`, `scope_limited`, `not_ready` |
| `anchor_status` | `exact_verified`, `fuzzy_recovered`, `ambiguous`, `broken`, `source_changed` |
| `evidence_support_status` | `not_checked`, `supported`, `partial`, `unsupported`, `unclear` |
| `source_identity.aliases.kind` | `legacy`, `locator`, `provider_object_id`, `snapshot` |

Legacy or descriptive values such as `overlay_state: candidate`,
`overlay_state: project_sidecar_created`, `promotion_gate:
evidence_aware_review_required`, and `promotion_gate:
evidence_aware_review_and_local_benchmark_required` are not allowed machine
values. Preserve that nuance in prose fields, not in gate enums.

### 1.2.1 Source Capture Envelope v1.0-alpha.1

Structured source capture uses the Source Capture Envelope artifacts for raw
provenance and intake hygiene only:

```text
capture-envelope.json
snapshot-manifest.jsonl
snapshot-hygiene.intoto.json
```

Alpha.1 adds operational metadata to make the Raw decision reproducible:

- `max_input_blob_size` limits the raw input before archive parsing.
- `observation.content_type` records the scanner-selected parser/container
  interpretation, not a filename or user-provided MIME hint.
- `producer.implementation` and `checker.implementation` pin the exact
  scanner/validator/schema/policy implementation manifest.
- `raw_handling.policy.digest` binds the admitted/quarantined decision to the
  actual Raw intake policy file.
- Source Card `provider_object_id` aliases may help provider adapters detect
  rename, transfer, or locator rebound, but they are not trust or evidence
  support.

This remains a Capture / Provenance hardening slice. It must not create
candidate, reviewed, decision, relation, action-basis, or feedback authority.

### 1.3 No Automatic Authority Promotion

Any migration from raw, candidate, overlay, or feedback material into reviewed
knowledge, decision, reviewed relation, or action basis requires explicit human
review.

Hard rule:

```text
raw/candidate/overlay/feedback -> reviewed/decision/action-basis
requires explicit human-confirmed review.
```

Suggested overlays may be produced by semantic match, tags, or embeddings only
inside query-run trace, agent trace, or a suggestion inbox. They cannot become
persistent project overlays merely because retrieval found a match.

### 1.4 Minimal State Machine

Use state names that make authority visible:

| State | Meaning | Automation allowed | Human confirmation |
|---|---|---|---|
| `LightRaw` | source identity and findability only | create source card and basic metadata | confirm source identity / why saved |
| `SourceAnnotated` | source-local span was marked for later use | create annotation sidecar and optional footnote handle | confirm only when it persists beyond scratch |
| `MediumCandidate` | provisional summary and candidate points | draft summary and routing hints | confirm provisional persistence |
| `OverlaySuggested` | project match suggestion in trace/inbox only | create transient suggestion | required before persistence |
| `OverlayConfirmed` | project-scoped sidecar | draft scope language | required for persistence and closeout |
| `OverlayArchived` | historical sidecar excluded by default | batch closeout draft | closeout confirmation |
| `HeavyReviewOpen` | review object is prepared, not passed | assemble evidence packet | reviewer must pass gate |
| `Reviewed` | reviewed knowledge / decision / relation | stale reminders only | content mutation requires review |
| `FeedbackCached` | append-only use event | log explicit use/failure event | confirm high-impact scope pressure |

Important wording: `HeavyReviewOpen` is not authority. It means the work has
entered review, not that the claim has passed review.

### 1.5 Object-Level Minimum Fields

Keep frontmatter small. Only fields needed for mechanical filtering, agent
constraints, and review routing should be mandatory.

| Object | Required fields | Optional fields | Boundary |
|---|---|---|---|
| Source Card | `source_id`, `source_url` or `raw_location`, `captured_at`, `title`, `why_saved` | `source_identity`, `latest_observed_capture_ref`, `adapter_ingest`, `author`, `version_or_commit` | provenance only; no adopt/reject |
| Source Annotation Sidecar | `annotation_id`, `source_ref`, `selector_type`, one stable selector, `anchor_status`, `annotation_role`, `support_checked`, `evidence_support_status` | `working_copy_ref`, `source_snapshot_ref`, `source_hash`, `content_hash`, `anchor_checked_at`, `anchor_stale`, `anchor_match_count`, `blocked_reason`, `next_action`, `source_digest_required`, `source_digest_ref`, `candidate_refs`, `project_overlay_refs`, `external_annotation_id`, `evidence_packet_ref` when `support_checked: true` | source-local locator; not support, not project verdict |
| Medium Candidate | `source_ref`, `provisional: true`, `knowledge_status: candidate`, structured summary, candidate points | `open_questions`, `routing_hint`, `point_anchor_refs`, `possible_project_refs` | provisional orientation, not rule |
| Project Overlay Confirmed | `project_id`, `target_ref`, `overlay_state: confirmed`, `project_borrow_scope`, `project_non_borrow_scope`, `project_reopen_trigger` | `target_hint`, `last_checked_at`, `expires_at`, `confirmation_basis` | project sidecar, not truth |
| Heavy Review Open | `claim`, `source_anchor_refs` or `evidence_anchor_refs`, `warrant`, `scope`, `gaps`, `residual_risk`, `review_status` | `assumptions`, `known_counterevidence`, `reviewer`, `reviewed_at` | review input, not review pass |
| Feedback Event | `event_kind`, `target_ref`, `project_ref` or `observed_in_context`, `event_time`, `review_pressure_effect` | `query_run_ref`, `temporary_project_warning`, `note` | append-only use event |

Placeholder fields are not all equal:

- Canonical confirmed overlays must not use placeholder values for
  `target_ref`, `project_borrow_scope`, `project_non_borrow_scope`, or
  `project_reopen_trigger`. If any of those fields are placeholders, the object
  is not a valid confirmed overlay.
- Legacy lens files may keep placeholder-like fields only when they are excluded
  from canonical overlay scope and retained through a compatibility
  manifest/tombstone.
- Raw source cards may keep `why_saved: see_body_or_legacy_record` as migration
  debt only when the body contains a real `Why Captured`, `Capture Reason`,
  `为什么收录`, or equivalent save-reason section. Without that body reason, the
  record has a missing intent/reason field, not merely harmless migration debt.
- `author` is optional on source cards. If unknown, use `unknown` or omit it;
  do not invent a specific placeholder that downstream retrieval could mistake
  for an authority signal.
- `kp_ref` is a legacy Project Lens maintenance pointer, not a Source Intake P0
  core field. It can help navigate old lens entries, but it must not be treated
  as evidence support, action basis, or proof that a canonical overlay exists.

### 1.6 Forbidden Intake Fields And Proxy Support

The following fields or writing patterns are forbidden in source, candidate,
overlay, and feedback records:

| Forbidden field or wording | Reason |
|---|---|
| `truth_score`, `truth_confidence`, `confidence_delta` | makes intake metadata look like truth confidence |
| `adopted`, `rejected`, `must_use`, `universal_ban` | makes candidate/overlay look like a decision |
| `action_basis_allowed: true` in candidate/overlay/feedback | bypasses the action gate |
| overlay `decision_outcome`, `review_verdict`, `accepted` | makes overlay look like ADR or review result |
| source-card top-level `relations` | makes raw provenance look like reviewed graph or support edges |
| source-card top-level `confidence` | makes capture quality or source trust look like truth authority |
| source-card top-level `freshness`, `relevance`, `source_quality`, `cross_source_count` | stable raw metadata can be mistaken for applicability, query relevance, trust, or multi-source support |
| `source_count`, `tool_count`, `project_count` as support | coverage count is not evidential support |
| `retrieval_score`, `graph_rank`, `dashboard_hit` as support | activation/diagnostic signal is not evidence |
| `vendor says`, `diagram looks clean`, `benchmark passed` as warrant | diagnostics do not bridge evidence to claim |

Heavy Review must explicitly check that these proxy signals were not used as
action-facing support.

If raw-source `confidence` means capture, transcript, or extraction quality,
place it under `source_integrity` or `adapter_ingest` with a scoped name such as
`capture_confidence` or `extraction_confidence`. If it means source trust, it
belongs in triage/review, not raw provenance.

If old raw-source `relations` must be retained, move it to
`candidate_relation_suggestions`, `legacy_raw_metadata.relations`, or a separate
candidate sidecar. It must not remain as a top-level raw source field.

If old raw-source `freshness`, `relevance`, `source_quality`, or
`cross_source_count` must be retained for audit, move them to a clearly
downgraded namespace such as `legacy_raw_metadata`. They are diagnostics or
historical triage values, not evidence support or authority.

`legacy_raw_metadata` is an audit/tombstone subtree. Retrieval compilers, graph
compilers, context-pack builders, and support checkers must ignore the entire
subtree by default. If a value from that subtree is ever needed again, promote it
through a new candidate/overlay/review object with explicit provenance instead
of selecting it directly.

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

If a specific source span matters, put the locator in a Source Annotation
Sidecar instead of rewriting the source or creating a loose development sticky
note.

If project-specific borrowing is needed, put the project-level judgment in
Project Overlay instead.

### Source Annotation Sidecar Gate

Source Annotation Sidecar replaces source-level development sticky notes. It is
not a normal tag and not a Project Overlay.

Plain-language rule:

```text
tag = broad filter for a whole note
source_annotation = pin on a specific source span
project_overlay = project-level borrow / non-borrow boundary
```

User-facing capture may be lightweight:

```text
select source text
-> insert optional inline footnote / ann_id handle
-> create source_annotation sidecar
-> show sidecar rows in Bases / workbench
```

Canonical storage rule:

```text
do not pollute immutable raw source text with inline footnotes.
inline footnote is an entrance or working-copy handle only.
canonical annotation data lives in a Markdown/YAML source_annotation record.
```

Storage path:

```text
outputs/review/source_annotations/<source-slug>/<annotation-id>.md
```

Minimum record:

```yaml
record_kind: source_annotation
knowledge_status: candidate
processing_tier: light
annotation_scope: source_local_anchor
source_ref:
working_copy_ref:
source_snapshot_ref:
selector_type: TextQuoteSelector | TextPositionSelector | line_range | timestamp | page_rect | bbox
selector_exact:
selector_prefix:
selector_suffix:
selector_position:
selector_timestamp_start:
selector_timestamp_end:
selector_page:
selector_rect:
source_hash:
content_hash:
anchor_status: exact_verified | fuzzy_recovered | ambiguous | broken | source_changed
anchor_checked_at:
anchor_stale: false
anchor_match_count:
annotation_role: question | possible_support | counterexample | scope_limit | risk_signal | candidate_seed | term_definition | implementation_note
body_note:
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs: []
project_overlay_refs: []
source_digest_required: false
source_digest_ref:
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: annotation_not_support
action_basis_allowed: false
truth_mutation_allowed: false
```

Boundary:

```text
source_annotation means "inspect this source span".
it does not mean "this span supports the point".
support exists only after Evidence Packet / evidence_support checks the span
against a specific candidate, reviewed relation, decision, or action basis.
```

If `support_checked: true`, the annotation must point to the Evidence Packet or
review object that performed the check:

```yaml
evidence_packet_ref:
```

Annotation roles are routing hints, not verdicts:

```text
question -> look again
possible_support -> possible evidence candidate, not support
counterexample -> possible challenge candidate, not rejection
scope_limit -> likely boundary condition
risk_signal -> possible risk to inspect
candidate_seed -> may become a candidate point
term_definition -> local definition anchor
implementation_note -> possible implementation detail
```

If an annotation becomes important:

```text
source_annotation
-> candidate point or review candidate
-> Evidence Packet copies/resolves the source span into evidence_items.source_anchor
-> evidence_support checks whether the span actually bears on the point
```

If an annotation is project-specific:

```text
source_annotation may link to a Project Overlay.
Project Overlay still owns project_borrow_scope / project_non_borrow_scope /
project_reopen_trigger.
The annotation does not replace those fields.
```

Scale rule:

```text
Do not let source annotations become a giant flat tag pile.

At scale, use the source-annotation workbench as:
working inbox -> needs anchor repair -> source drilldown -> AI review-input gate -> source health.

Dense sources should route to a source digest / consolidation queue instead of
asking humans to inspect every row-level pin.
```

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
ordinary tags/topics as broad filters only
source_annotation if a specific source span is worth pinning
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
  pack_allowed: none
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
  pack_allowed: none
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

#### Retrieval Receipt and Context-Pack Manifest

Any query-run or context pack that includes raw, candidate, overlay, feedback, or
reviewed records must make its authority boundary visible at item level.

Minimum query-run trace:

```yaml
query_id:
query_time:
question_summary:
verbatim_input:
active_project:
query_mode: orientation | source_inspection | review | action
requested_authority_bucket:
included_buckets: []
excluded_buckets: []
retrieval_filters:
  include_candidates: false
  include_overlays: active_project_only
selected_items:
  - ref:
    record_kind:
    knowledge_status:
    pack_role: orientation | review_input | support | anchor
    warning_code:
    action_basis_allowed: false
    selected_by:
      lexical:
      semantic:
      graph:
      metadata:
      legacy_raw_metadata: false
support_checks:
  - claim_ref:
    independent_anchor_ref:
    result: supported | weak | missing_anchor | self_support_loop | scope_limited | not_ready
warnings: []
gaps: []
human_confirmation_required: false
```

Minimum context-pack item:

```yaml
ref:
record_kind:
knowledge_status:
pack_role:
warning_code:
project_scope:
action_basis_allowed:
independent_anchor_ref:
selected_by:
excluded_reason:
```

Hard rules:

```text
candidate and overlay items may enter packs only as orientation or review_input.
support requires reviewed material or a raw/stable independent anchor.
if support lacks independent_anchor_ref, mark missing_anchor or not_ready.
selected_by is trace metadata only; it is not authority or evidence.
`legacy_raw_metadata` must remain false. It is retained for audit only and must
not be used as a retrieval, graph, pack, or support signal.

Static schema/lint checks are necessary but not sufficient. They can catch
mis-serialized fields, invalid receipt shapes, and obvious support misuse; they
do not prove answer-loop faithfulness, groundedness, or tool behavior. Runtime
validation still requires read-only query -> retrieval -> answer/use-loop traces.
```

#### Phase B Read-Only Retrieval Adapter

VAKS may record a documentation-only Phase B direction for a derived retrieval
adapter. This does not approve runtime, default, or production adoption.

Allowed adapter use:

```text
parser / chunk / metadata / vector-like recall / graph-neighborhood recall
click-back anchors
source and chunk hashes
retrieval receipts
warning codes
retrieval reasons
```

Required boundary:

```text
apply VAKS authority buckets before ranking or RRF fusion
merge relevance signals only inside the allowed bucket
return context-pack candidates, not support by default
```

`graph_path`, retrieval reasons, graph-neighborhood hits, and extracted graph
edges are recall metadata only. They are not reviewed relations, evidence
support, truth confidence, or action basis.

The adapter must not promote raw, candidate, diagnostic, feedback, or overlay
material into reviewed support, reviewed relation, truth confidence, or action
basis.

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

Legacy source hash / incremental ingest hygiene:

```yaml
source_integrity:
  source_hash:
  snapshot_hash:
  ingest_state: new | changed | unchanged | deleted | unknown
```

Source hashes help detect duplicate, changed, unchanged, or deleted source
material. They are source hygiene only. They do not decide truth, evidence
support, review verdict, verification status, or action readiness.

`source_integrity` is legacy compatibility. New structured captures should not
add new meanings to this catch-all field. Use Source Capture Envelope v1:

```text
Source Card
-> capture-envelope.json
-> snapshot-manifest.jsonl
-> snapshot-hygiene.intoto.json
```

The v1 contract separates:

```text
Source    stable upstream identity
Revision  upstream version claim
Snapshot  intrinsic observed content identity
Capture   one observation/capture event
```

Minimal Source Card pointer:

```yaml
source_identity:
  schema_version: 1
  source_id: "vsrc:1:repo:github.com/owner/name"
  kind: repo
  canonical_locator: "git+https://github.com/owner/name"
  identity_profile: "repo-provider-native/v1"
  aliases: []
latest_observed_capture_ref: "raw/captures/<capture-id>/capture-envelope.json"
```

When `source_identity` appears, it switches the Source Card into v1 strict mode:
the mapping is limited to `schema_version`, `source_id`, `kind`,
`canonical_locator`, `identity_profile`, and `aliases`. Capture history,
manifest details, hygiene findings, adapter events, and review facts belong in
Capture Envelope / manifest / hygiene artifacts, not inside `source_identity`.

The capture envelope records the actual observation, captured blob, snapshot ID,
report references, observation/change/fidelity state, and raw handling
disposition. Snapshot manifests are deterministic logical content descriptions.
Hygiene attestations bind versioned checker facts to a digest. These are raw
capture facts only; they do not create trust, evidence support, reviewed
knowledge, reviewed relations, verification status, or action readiness.
Repo captures use repo hygiene predicates/profiles. Generic blobs, PDFs, videos,
web bundles, or isolated files must not automatically inherit repo portability
or repo completeness conclusions.

Authoritative v1 details live in:

- `docs/source-id-v1.md`
- `docs/snapshot-manifest-v1.md`
- `schemas/source-capture-v1.schema.json`
- `schemas/snapshot-hygiene-v1.schema.json`

Read-only inspector entry point:

```powershell
python tools/inspect_source_snapshot.py <source-blob-or-archive> --out <explicit-output-dir>
```

The inspector must not modify Source Cards, candidates, reviewed knowledge, or
action artifacts.

Inspector defaults are conservative: `change.state` defaults to `unknown`;
repo/web/video sources require an explicit stable `source_id` unless content
fallback is explicitly allowed; local absolute `resolved_locator` is not emitted
unless supplied by the caller.

`raw_handling.disposition: admitted` only means raw-layer admission. It is not a
verified-source label. `max_severity: none` only means the current checker found
no known issue under the recorded parameters.

Source adapter ingest contract:

```yaml
adapter_ingest:
  adapter_name:
  adapter_version:
  capture_method:
  extraction_trace:
  known_limits: []
```

Adapter records preserve how a source was captured or converted. They are ingest
hygiene only. Adapter output may create raw/source records or candidate material,
but it must not directly create reviewed wiki nodes, truth confidence,
verification status, reviewed relations, or action readiness.

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

Track how far the evidence was actually inspected:

```yaml
evidence_granularity: metadata_only | abstract_or_summary | excerpt_or_passage | table_or_code_anchor | full_source_reviewed
```

Rule:

```text
Source provenance tells where material came from.
Source anchor tells where the specific evidence lives.
Source annotation tells which source span deserves inspection.
Neither proves support by itself.
```

Source Annotation Sidecar may supply the locator for a later
`evidence_items.source_anchor`, but it is not itself evidence support. When a
candidate is promoted, used for a strong relation, decision, risk-sensitive
answer, or action basis, the reviewer must still check the anchored span against
the specific target point.

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

| Failure case | Trigger | Expected guardrail | Detection | Recovery |
|---|---|---|---|---|
| Medium candidate becomes action basis. | Candidate summary enters action/review mode. | Bucket filter first; candidate `action_basis_allowed: false`. | Query-run trace shows candidate as `support`. | Reclassify as `review_input`; add receipt warning. |
| Suggested overlay persists without confirmation. | Semantic match writes durable overlay. | `suggested` exists only in trace/inbox. | Lint finds persisted `overlay_state: suggested`. | Delete persisted note; keep trace-only suggestion. |
| Confirmed overlay leaks into inactive project retrieval. | Retrieval skips active project filter. | `retrieval_scope: active_project_only`. | Non-project receipt includes overlay. | Fix filter; rebuild derived index/cache. |
| `project_non_borrow_scope` becomes universal ban. | Wording says "Never use X" or "X is wrong". | Project-local sentence plus reopen trigger. | Lint checks universal-ban wording in overlay. | Rewrite as project-local non-borrow scope. |
| Candidate summary outranks raw anchor. | Top-k candidate is marked `support`. | Support needs independent raw/stable anchor. | Receipt `support` lacks `independent_anchor_ref`. | Mark `missing_anchor`; add raw/stable anchor or reject. |
| Broken anchor is cited in action mode. | Source page changed or repo moved. | `review_pressure: blocked`. | Anchor checker / stale scan / use failure. | Pause action use; recapture source or reopen review. |
| Negative feedback does not create review pressure. | Repeated scoped failures only downrank locally. | Repeated negative -> `review_due`. | Feedback aggregation report. | Add feedback event; reopen Heavy Review if needed. |
| Archived overlay remains in default retrieval. | Closeout moved file but not filter state. | `overlay_state: archived` + default exclude. | Project closeout audit / retrieval receipt. | Fix state; rebuild index/cache. |
| Heavy Review Open is treated as Review Passed. | `review_status: pending` is cited as support. | Review-status hard gate. | Action receipt includes pending review object. | Block writeback; return to review. |
| Enum drift bypasses filter. | New example uses unregistered enum. | Enum registry + vault lint. | Lint reports unknown enum. | Normalize enum; move nuance into prose. |
| Feedback directly mutates reviewed truth. | Agent edits reviewed note from feedback. | `truth_mutation_allowed: false`. | Git/vault diff or feedback lint. | Revert truth edit; write feedback event. |
| Graph/rank score becomes support. | Graph edge or vector rank is cited. | Diagnostics-only labels. | Support check has no independent anchor. | Downgrade to orientation; add anchor or reject. |

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
Source-local insights should use Source Annotation Sidecar, not loose development sticky notes.
Inline footnotes are capture affordances or working-copy handles; they are not the canonical annotation data layer.
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
Source annotations can be created as low-friction pins, but they cannot create Project Overlay scope, reviewed relations, confidence, or action readiness.
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
