---
record_kind: sandbox_product_model
status: draft
created_at: 2026-06-14
scope: source-annotation-scale-product-sandbox
truth_boundary: sandbox_only_not_adopted_architecture
---

# Source Annotation Product Model v0

## Plain-Language Answer

The new annotation layer should feel like Xiaohongshu-style footnotes while
behaving like VAKS.

In daily use:

```text
See useful original text -> mark the exact place -> add a short note if needed.
```

The system then keeps four things separate:

```text
where it is -> source selector
why we marked it -> annotation role / body note
where it may go -> candidate / project overlay / evidence packet refs
what it is allowed to prove -> nothing by itself
```

So the answer to "what happens when annotations grow" is:

```text
Do not make one giant tag pile.
Make a source-span inbox with repair, routing, project lens, and AI export gates.
```

## Product Position

Source Annotation is a locator workbench.

It is not:

- evidence support
- reviewed truth
- project borrow verdict
- action basis
- retrieval rank

It is:

- a pointer to a useful source span
- a lightweight note about why the span may matter
- a router into candidate review, Project Overlay, or Evidence Packet work
- a repairable anchor record

## Four Loops

### 1. Capture

The user should only need to care about:

```text
source
span
short note
role
optional project overlay link
```

Everything else should be filled by template or tool.

Required human-facing fields should stay below eight:

```text
source_ref
selector
annotation_role
body_note
project_overlay_refs
candidate_refs
review_pressure
archive / repair action
```

### 2. Triage

The default workbench should answer:

```text
What did I mark?
Which marks need repair?
Which marks are worth turning into candidate knowledge?
Which marks are project-specific?
Which marks are safe to send to AI as review input?
```

### 3. Use

For AI use, an annotation must travel with:

```text
source_ref
selector
resolved source window
annotation_role
body_note
warning_code: annotation_not_support
pack_role: review_input
```

The model must see the original source window, not only the note.

### 4. Repair

Anchors decay. The product should expect that.

Bad anchors move into a visible repair queue:

```text
ambiguous
broken
source_changed
```

They should not be silently used in action-facing context packs.

## Record Anatomy

### Identity

```yaml
annotation_id:
source_ref:
working_copy_ref:
source_snapshot_ref:
source_hash:
external_annotation_id:
```

`source_ref` should point to raw source text or a stable source artifact by
default. It should not point to a summary, Q&A answer, or candidate note unless
the annotation is explicitly about that artifact.

### Selector Bundle

Use multiple locators when possible:

```yaml
selector_type: TextQuoteSelector | TextPositionSelector | FragmentSelector | line_range | timestamp | page_rect | bbox
selector_exact:
selector_prefix:
selector_suffix:
selector_position_start:
selector_position_end:
selector_line_start:
selector_line_end:
selector_timestamp_start:
selector_timestamp_end:
selector_page:
selector_rect:
content_hash:
```

The preferred text anchor is:

```text
exact quote + prefix + suffix + source hash
```

Position, line, timestamp, and page rectangle are secondary locators. They are
useful for repair and navigation, but they should not be treated as proof.

### Anchor Health

Keep anchor health separate from workflow lifecycle.

```yaml
anchor_status: exact_verified | fuzzy_recovered | ambiguous | broken | source_changed
anchor_checked_at:
anchor_check_method: exact_quote | position | context_fuzzy | selector_fuzzy | manual
anchor_match_count:
anchor_stale: false
```

Meaning:

```text
exact_verified: current source has one reliable match
fuzzy_recovered: recovered one likely match, needs caution
ambiguous: multiple candidates
broken: no reliable candidate
source_changed: old snapshot differs from current source
```

`anchor_stale` is a workbench flag. It means the anchor may still be valid, but
it has not been checked recently enough for comfortable AI export or important
review use.

### Workflow Lifecycle

```yaml
lifecycle_state: source_annotated | triaged | routed | repair_needed | repair_candidate | repaired | archived
repair_note:
```

`archived` is not an anchor status. It means the item is closed, duplicate,
stale, or no longer worth processing.

### Role

Role is a routing hint, not a verdict.

```yaml
annotation_role: question | possible_support | counterexample | scope_limit | risk_signal | candidate_seed | term_definition | implementation_note | bookmark
body_note:
```

UI labels must avoid making these sound stronger than they are:

```text
possible_support != support
counterexample != disproved
risk_signal != confirmed risk
candidate_seed != adopted knowledge
```

### Routing

```yaml
candidate_refs: []
project_overlay_refs: []
evidence_packet_ref:
support_checked: false
evidence_support_status: not_checked
```

Project names can be displayed in the workbench, but the durable link should be
`project_overlay_refs`. The annotation itself must not create
`project_borrow_scope` or `project_non_borrow_scope`.

If `support_checked: true`, `evidence_packet_ref` is required. The support
still comes from the Evidence Packet, not from the annotation.

Enterprise priority rule:

```text
anchor repair beats support audit
```

If an anchor is broken, ambiguous, source_changed, or stale, it must be repaired
or refreshed before any support check can be treated as current.

### Authority Boundary

Every annotation carries the same hard boundary:

```yaml
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: annotation_not_support
action_basis_allowed: false
truth_mutation_allowed: false
```

## Workbench Views

### Annotation Inbox

Default place to look.

Shows:

```text
annotation_id
source_ref
role
short note
anchor_status
review_pressure
route refs
path
```

Hides long selectors and audit fields.

Enterprise refinement:

```text
Annotation inbox is a working inbox, not the whole annotation pool.
```

It should show new or untriaged items only. Stable locators move to the locator
pool and source drilldown. Otherwise a 5,000-annotation vault becomes one giant
table again.

### Locator Pool

The large set of stable, already-triaged locators.

This pool is queryable by AI export and source drilldown, but it is not the
daily human inbox.

### Source Drilldown

Opened from a source card.

Sorted by:

```text
line / position / timestamp / page
```

This is where dense source-local annotations remain readable.

### Project Lens

Opened from a Project Overlay.

Filters by:

```text
project_overlay_refs contains current overlay
```

This view is project-specific, but it does not make source annotation a project
verdict.

### Routing Queue

Items that may become:

```text
candidate distillation
project overlay item
evidence packet
repair item
archive
```

### Needs Anchor Repair

Only:

```text
ambiguous
broken
source_changed
```

These should be excluded from AI export ready.

### Support Checked Audit

Shows items where:

```text
support_checked: true
```

Missing `evidence_packet_ref` is a hard error.

### Stale Anchors

Shows old anchors before they silently become trusted background.

Stale anchors should be refreshed before AI export or high-value review use.

### Scale Debt / Consolidation Queue

Shows sources and selectors that are becoming too dense:

```text
too many active annotations on one source
many annotations with the same selector
source digest required
```

This queue prevents the workbench from becoming a new pile of tiny notes.

Enterprise refinement:

```text
scale debt is source-level first
```

Operators should first see the dense source, not thousands of row-level
annotations. A dense source should carry:

```yaml
digest_ref:
last_digest_at:
next_digest_due:
debt_queue: source_digest_backlog
debt_owner_or_queue:
next_action: create_or_refresh_source_digest
digest_backlog_age_days:
```

This keeps the locator pool from becoming a legal junk drawer.

### Source Health Dashboard

Enterprise operation should include source-level rows:

```text
source
active annotations
AI-ready locators
repair count
stale count
scale debt count
digest route
```

This prevents a Base limit of 100 rows from hiding backlog.

### AI Export Ready / Blocked

Product name:

```text
AI review-input ready
```

Avoid calling it "AI export ready" in user-facing UI because "ready" can sound
like evidence readiness.

Ready:

```text
exact_verified or fuzzy_recovered
not stale
not archived
warning_code present
action_basis_allowed false
source window can be resolved
```

Blocked:

```text
bad anchor
missing selector
missing warning
support_checked without evidence packet
forbidden truth / project / action fields
```

Blocked rows should show:

```yaml
blocked_reason:
next_action:
```

No one should have to infer the next step from a status enum.

### Cold Archive

Closed duplicates, obsolete marks, or low-value marks.

Archived annotations should not be in the default retrieval path.

## Scale Controls

### Pin Budget

Suggested default:

```text
5-15 active annotations per source
```

If one source exceeds the budget, the workbench should ask for one of:

```text
source digest
candidate distillation
project overlay grouping
archive duplicates
```

### Duplicate Pressure

Same source + same selector + same role should become lint debt unless there is
a clear reason.

### Stale Badge

Any annotation whose anchor has not been checked recently should show a stale
badge before high-stakes use.

### View Limits

Tables can default to 100 rows, but the workbench must show backlog counts so a
limit does not hide debt.

## AI Context Export

Machine format should be JSON. Markdown can mirror it for human reading.

Minimum buckets:

```text
query
authority_gate
selected_items
resolved_source_spans
coverage_overview
action_readiness
warnings
```

Selected source annotations must look like:

```json
{
  "record_kind": "source_annotation",
  "pack_role": "review_input",
  "warning_code": "annotation_not_support",
  "action_basis_allowed": false
}
```

Resolved source spans must say:

```json
{
  "may_count_as_support": false,
  "support_check_required": true
}
```

## Hard Tests

The sandbox must fail if:

- any annotation allows action basis
- any annotation mutates truth
- any annotation contains project borrow verdict fields
- `support_checked: true` lacks `evidence_packet_ref`
- a context pack uses `source_annotation` as `support`
- broken / ambiguous / source_changed anchors enter AI export ready
- dense source annotations exceed budget without a digest route
- duplicate IDs exist
- stale anchors enter AI export ready
- selector requirements are missing for their selector type
- archived annotations enter default retrieval
- working inbox becomes a giant pool instead of a small actionable queue

## Kill Criteria

Stop expanding this layer if:

- annotations routinely become evidence by accident
- Project Overlay gets auto-filled without review
- repair backlog becomes invisible
- raw source reading becomes polluted with footnote bodies
- most annotations never become candidate, overlay, evidence packet, archive, or delete

## Adoption Criteria

This design becomes ready for main framework only if the sandbox proves:

```text
capture stays light
views stay understandable
bad anchors are visible
AI export keeps original source context
annotation cannot become support/action basis by schema or pack bug
project filtering works without project-truth pollution
```
