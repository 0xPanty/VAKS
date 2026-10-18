---
type: implementation-note
status: active
created: 2026-05-27
updated: 2026-06-08
project: verified-action-knowledge-system
related_decisions:
  - "[[2026-05-27-traceability-first-graduated-verification]]"
related_patterns:
  - "[[review-gated-compile-queue]]"
  - "[[self-contained-review-candidate-record]]"
  - "[[accumulated-source-cross-validation]]"
  - "[[claim-level-provenance-source-ranges]]"
sources:
  - "[[IMPLEMENTATION_BLUEPRINT]]"
  - "[[2026-05-27-alpha-point-collision-research]]"
verification_status: active
evidence_level: synthetic
confidence: high
validated_by:
  - "subagent adversarial review"
  - "external source comparison"
rollback_path:
  - "If point collision creates noise, keep source/candidate records and disable collision promotion until manual review rules improve."
last_verified: 2026-05-31
next_review: 2026-06-03
relations:
  - target: "[[IMPLEMENTATION_BLUEPRINT]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[REVIEW_QUEUE]]"
    rationale: "This file defines the first concrete review queue contract required by the implementation blueprint."
    created: 2026-05-27
    last_verified: 2026-05-28
  - target: "[[accumulated-source-cross-validation]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[REVIEW_QUEUE]]"
    rationale: "The queue introduces candidate points, collision signals, and point clusters as the practical mechanism for accumulated cross-validation."
    created: 2026-05-27
    last_verified: 2026-05-28
tags:
  - review-queue
  - point-collision
  - alpha
  - traceability-first
---

# REVIEW_QUEUE.md v0.1

## AI-readable preamble

This is the first review queue contract for the vault.

The queue is not a dumping ground and not a reviewed knowledge layer. It is where raw sources become reviewable candidate points, and where similar points collide before anything is promoted.

The core alpha mechanism is:

```text
provenance-first
-> candidate point
-> self-contained review candidate record, when review or promotion is intended
-> knowledge calibration / point collision signal
-> reviewed cluster
-> promoted claim / pattern / anti-pattern / decision
```

Knowledge calibration is the practical queue-level version of the vault's truth-maintenance idea:

```text
do not only store a conclusion
record why it is believed
surface what new candidate points support, challenge, narrow, or make stale
send those effects to review before they can affect action
```

## 1. Why This Exists

We do not want every source to be fully verified when it enters the vault.

We also do not want AI output to become formal reviewed knowledge directly.

The review queue solves the middle:

```text
capture stays light
candidate points stay inspectable
promotion candidates become self-contained review records
similar points can cross-check each other
promotion stays reviewed
```

## 2. Queue Directory

Use this structure:

```text
outputs/review/
  candidates/
  collisions/
  clusters/
  archived/
```

v0.1 can create these directories lazily. The contract matters more than the folder existing before first use.

## 3. Core Records

### 3.1 Source Trace

Source trace is the minimum record needed before point extraction.

```yaml
source_id:
source_uri:
source_url_or_path:
raw_location:
source_type: article | paper | repo | docs | video | transcript | screenshot | chat | other
source_family:
upstream_sources: []
version_or_commit:
captured_at:
captured_by:
processing_mode: inbox | immediate
processing_status: raw-only | point-candidate-generated | reviewed | promoted | rejected
topics: []
```

Rules:

```text
source_family marks likely shared origin: same URL, same repo, same author, same org, same article chain, same transcript, same AI output.
upstream_sources records what this source appears to depend on or cite.
source_family and upstream_sources are hints, not final independence judgments.
Source trace records source identity and capture provenance only.
Extraction details belong to candidate points or medium/heavy source records.
Review, promotion, and context-pack use belong to reviewed nodes, promotion records, context packs, or the use ledger.
Provenance is traceability, not truth or confidence.
```

### 3.2 Candidate Point

Candidate point is the atomic review unit, not necessarily an atomic claim.

It should be one small comparable idea, question, risk, decision candidate, preference, or implementation note, not a whole article summary.

```yaml
record_type: candidate-point
point_id:
point_text:
normalized_point:
point_type: claim | interpretation | hypothesis | pattern | risk | preference | decision | open_question | implementation_note
verifiability:
  state: verifiable | partially_verifiable | not_verifiable | unknown
  reason:
review_route: evidence_check | rationale_check | instance_check | risk_check | action_basis_check | personalization_only | research_question | code_anchor_check
why_checkworthy:
evidence_granularity: metadata_only | abstract_or_summary | excerpt_or_passage | table_or_code_anchor | full_source_reviewed
topics: []
entities: []
scope:
  domain:
  project:
  version:
  time_range:
  conditions:
temporal_applicability:
  valid_from:
  valid_until:
  supersedes:
  superseded_by:
  invalidated_by:
  applies_to:
    project:
    version:
    environment:
    timeframe:
    conditions:
  check_state:
  reviewer_note:
source_refs:
  - source_id:
    source_url_or_path:
    source_range:
    quote_or_excerpt:
    source_anchor:
      url_or_path:
      exact_quote:
      prefix:
      suffix:
      captured_at:
      position:
      content_hash:
      archived_url:
      checked_latest_at:
      source_changed: unknown | yes | no
    evidence_support:
      span_supports_target: supported | partial | unsupported | unclear
      evidence_role: direct_support | inferential_support | background_context | counterexample
      reviewer_note:
evidence_packet:
  point:
  evidence_items: []
  grounds:
  warrant:
  qualifier:
  strongest_rebuttal:
  challenge_kind: rebuttal | undercut | scope_limit | source_hygiene | stale_assumption | action_failure
  scope_limit:
  risk_flags: []
  omission_check:
    missing_risks:
    missing_scope_limits:
    possible_omissions:
    omission_questions:
    needs_full_source_read:
  review_question:
  minimal_revision_needed: keep | refine_scope | mark_contested | mark_stale | supersede | reject
extracted_by:
extracted_at:
uncertainty:
possible_related_points: []
review_status: pending | accepted | rejected | needs-edit
promotion_target:

# Optional, high-impact-only review aid.
point_graph_fragment:
  purpose:
  entities:
    - id:
      label:
      type:
      aliases: []
      resolution:
        status:
        note:
  relation_triplets:
    - subject:
      predicate:
      object:
      qualifier:
      scope:
      source_anchor:
      note:
  open_questions:
    - question:
      blocks_review:
```

Default route:

```text
claim -> evidence_check
interpretation -> rationale_check
hypothesis -> research_question
pattern -> instance_check
risk -> risk_check
preference -> personalization_only
decision -> action_basis_check
open_question -> research_question
implementation_note -> code_anchor_check
```

Rules:

```text
If a point cannot be traced to a source range or excerpt, it is not ready for collision.
If a point has broad wording, narrow the scope before promotion.
If a point is an AI inference, mark it as hypothesis unless source text directly supports it.
If a point may be promoted, used for action, used for a strong reviewed relation, or explicitly challenged, prefer an Evidence Packet over a loose source summary.
Point Collision is triggered by candidate / review / promotion / action need, not by raw capture itself.
URL-only source_refs are provenance, not support.
For dynamic data evidence, source identity includes query, filter, subset, as-of, and result-set scope when used for promotion, strong relation review, or action basis.
Evidence support is optional during early candidate capture, but required when a source_ref is used for promotion, strong relation review, or action basis.
Evidence Packet is review input, not a new truth layer.
`warrant` explains why the evidence supports or weakens the point; it is not the same as provenance.
`challenge_kind` names the challenge shape; it does not automatically reject the point.
`minimal_revision_needed` recommends the smallest review action; it does not edit reviewed knowledge.
`omission_check` is required only for heavy source digests, important repositories, long papers, high-impact decisions, or reviewer request.
background_context cannot count as support.
prior chat memory, agent memory, or model background cannot count as current source support unless tied to a current source span.
inferential_support needs reviewer_note before it can count as promotion support.
Not every candidate point can receive truth confidence.
Only verifiable claims can receive truth / evidence confidence.
Unverifiable does not mean useless; it means the point needs a non-truth review route.
Review route defaults from point_type and can be overridden by a reviewer.
point_graph_fragment is optional; use it only for complex, high-impact, cross-document, multi-hop, action-relevant, or ambiguous points.
Extracted triplets are not truth, not support, and not reviewed relations.
If a graph fragment needs more than 3-5 essential triplets, split the candidate point instead.
```

Evidence support is not a Source-node property. It is a source-span-to-target check:

```text
source provenance:
  where this material came from

evidence support:
  whether this source span supports this candidate point, reviewed node, or reviewed relation
```

### 3.2.1 Self-Contained Review Candidate Record

A self-contained review candidate record is required only when a candidate is
prepared for promotion, formal writeback, action-basis use, or a reviewer asks
for a fixed review object.

It is not required for ordinary light capture.

```yaml
record_type: review-candidate
candidate_id:
source_candidate_points: []
promotion_target: claim | pattern | anti-pattern | decision | reviewed_relation | none
proposed_title:
proposed_path:
review_object_state: draft | fixed_for_review | revised_after_review | archived
candidate_body_location:
body_hash:
body_hash_algorithm: sha256_utf8_lf_trim_body_without_heading
evidence_packet_ref:
source_anchor_refs: []
scope_limits: []
risk_flags: []
known_counterevidence: []
missing_evidence: []
approval_integrity:
  approved_by:
  approval_source:
  approved_at:
  llm_assisted: true | false
  checked_specific_evidence: true | false
  checked_body_hash:
archive_reason:
```

Rules:

```text
The record is a review object, not reviewed knowledge.
candidate_body_location points to the exact Markdown section or file proposed for writeback.
Do not embed long Markdown bodies in frontmatter/YAML metadata.
Canonical body hash rule: hash the content pointed to by `candidate_body_location`, excluding the heading, normalizing CRLF to LF, trimming leading/trailing whitespace, encoded as UTF-8 SHA256.
If the candidate body changes after review, body_hash changes and the candidate returns to review.
Approval may approve the fixed candidate body; it must not silently regenerate a different body.
source_anchor_refs must point to independent source anchors, not only to source summaries or the candidate itself.
Evidence Packet remains the support check; the self-contained record only fixes the object being reviewed.
```

Candidate lint before approval:

```yaml
candidate_lint:
  schema_violations: []
  provenance_violations: []
  lint_status: unchecked | pass | warnings | blocked
```

Candidate lint records visible problems before approval. It is review input, not
a rejection verdict, truth change, reviewed relation, or automatic promotion
decision.

### 3.2.2 Review-Gated Compile / Writeback Queue

Any LLM / compile / agent output that proposes a formal `wiki/` node must enter
the review queue before writeback.

This applies to:

```text
source -> generated summary / claim / pattern / anti-pattern / decision
query answer -> proposed reviewed node
brief / proactive synthesis -> proposed reviewed node
agent suggestion -> proposed reviewed node
```

The required path is:

```text
generated body
-> review-candidate record
-> fixed body hash when prepared for review
-> lint / evidence review
-> approval of that exact body
-> formal wiki writeback or archive
```

Rules:

```text
Compile/writeback review is an entrance gate, not a truth layer.
It does not replace Evidence Packet, Evidence Sufficiency Gate, or approval integrity.
It does not create confidence, reviewed relations, action readiness, or automatic promotion.
Approval must write the fixed candidate body; it must not silently regenerate a new body.
Rejected candidates are archived or left auditable; rejection must not delete the source trail.
Raw source capture and ordinary outputs/qa records do not require this gate until they are proposed for formal wiki writeback.
Watch, query-save, MCP write, Obsidian sync, or bulk scripts must not bypass this gate for formal reviewed knowledge.
```

### 3.3 Calibration / Collision Signal

Calibration / collision signal records how a new candidate point may affect local reviewed knowledge or another candidate point.

```yaml
record_type: calibration-signal
signal_id:
from_point:
to_point:
relation: supports | contradicts | refines | risk_of | derived_from | duplicates | near_miss | unrelated
challenge_kind: rebuttal | undercut | scope_limit | source_hygiene | stale_assumption | action_failure
output_kind: candidate_relation | contradiction_candidate | scope_mismatch | stale_assumption_candidate | missing_evidence | synthesis_needed | decision_superseded | review_question | review_due
minimal_revision_needed: keep | refine_scope | mark_contested | mark_stale | supersede | reject
similarity_basis:
  - keyword
  - entity
  - source_overlap
  - semantic_similarity
  - graph_neighbor
  - association_path
  - manual
source_independence: independent | same-origin | derived | unknown
independence_rationale:
relation_rationale:
review_status: pending | accepted | rejected | needs-edit
reviewed_by:
reviewed_at:
```

Rules:

```text
Raw source does not collide directly; candidate points do.
Light capture stays source-only by default; it enters collision only after a candidate point is generated and there is a review, promotion, action, contradiction, or explicit user-processing need.
Similarity only creates a pending signal.
Similarity is not support.
Graph neighbor / association path / PPR-style activation only creates a pending signal.
Association score is not support or confidence.
Challenge kind and minimal revision are review routing metadata, not automatic truth changes.
Only reviewed signals can increase promotion readiness.
Same-origin or derived sources do not count as independent support.
Background citations do not count as support.
Contradictions must stay visible; do not auto-resolve them.
Calibration output is review input, not truth.
```

### 3.3.1 Review Queue Item Taxonomy

Review queue items explain why human attention is needed.

They are not new truth nodes. They are routing labels for candidate points,
clusters, collision signals, decisions, or downstream dependencies.

```yaml
record_type: review-queue-item
queue_item_id:
item_type: low_confidence_claim | contradiction | missing_evidence | synthesis_needed | decision_superseded
target_refs: []
triggered_by:
  - candidate_point
  - calibration_signal
  - point_cluster
  - reviewed_node
  - decision
  - feedback_event
  - action_outcome
reason:
suggested_action: approve | reject | merge | override | request_evidence | mark_review_due | create_missing_point
status: open | in-review | resolved | rejected | parked
reviewed_by:
reviewed_at:
resolution_note:
```

Rules:

```text
low_confidence_claim means the point may be useful but cannot be promoted yet.
contradiction means a challenge must remain visible until reviewed.
missing_evidence means the system needs support for a specific point or relation, not just another URL.
synthesis_needed means several candidates or clusters need a single reviewed judgment, pattern, anti-pattern, or decision.
decision_superseded means a newer decision or evidence package may replace an older decision for some scope.
approve / reject / merge / override are queue resolutions, not automatic truth changes.
override requires rationale and audit trail.
```

Maintenance manifests may add lint-style review items. These can use the same queue, but they remain repair prompts:

```text
missing_intent_confirmation
confidence_cap_violation
validity_window_mismatch
missing_outcome_calibration
orphan_review_candidate
```

### 3.3.2 Approval Integrity

Approval integrity is process evidence, not evidence support.

LLM-assisted labels, model-prefilled review notes, high agreement, majority vote, or a human "looks good" confirmation can create review input or review pressure, but they do not by themselves create evidence review, truth confidence, reviewed relations, or automatic promotion.

For any approval that can affect promotion, formal writeback, benchmark label reuse, or action basis, keep the narrow process facts visible: approved_by, approval_source, approved_at, body_hash, llm_assisted, and whether the human checked the specific evidence rather than only the summary.

### 3.4 Point Cluster

Point cluster groups recurring candidate points.

```yaml
record_type: point-cluster
cluster_id:
canonical_point:
member_points: []
reviewed_supports: []
reviewed_contradictions: []
reviewed_refinements: []
source_families: []
independent_source_count:
primary_source_count:
status: emerging | in-review | promoted | conflicted | stale | rejected
promotion_readiness: none | watch | review | promote-candidate
promotion_target:
gaps: []
warnings: []
last_seen:
next_review:
```

Rules:

```text
A cluster is not truth.
A cluster is a dashboard for promotion review.
Clusters with contradictions can still be valuable, but they promote as conflict-aware claims or anti-patterns.
```

## 4. Minimum Workflow

### Step 1: Capture Source

Write source into `raw/` or source-specific raw folder.

Minimum requirement:

```text
source_url_or_path
raw_location
captured_at
captured_by
processing_status
```

### Step 2: Extract Candidate Points

Codex extracts 2-8 candidate points from the source.

Each point must be small enough to compare.

Good:

```text
Claude-Obsidian uses hot.md as a recent context cache for cross-session recall.
```

Too broad:

```text
Claude-Obsidian is useful.
```

### Step 3: Find Possible Collisions

For each new point, search existing points and promoted nodes.

v0.1 search order:

```text
1. exact entity / keyword search
2. topic and tag search
3. source family / source overlap search
4. optional embedding search later
```

### Step 4: Create Pending Collision Signals

Do not decide truth yet.

Create pending signals:

```text
supports
contradicts
refines
risk_of
derived_from
duplicates
near_miss
unrelated
```

Also record what kind of review input the signal creates:

```text
candidate_relation
contradiction_candidate
scope_mismatch
stale_assumption_candidate
missing_evidence
synthesis_needed
decision_superseded
review_question
review_due
```

### Step 5: Review Collision Signals

Review asks:

```text
Are these points actually saying the same thing?
Are their scopes compatible?
Are the sources independent?
Does one source copy the other?
Is the newer source more authoritative?
Is there a direct contradiction?
Does this signal only show similarity, or does it have evidence and rationale?
Does this association path only explain retrieval, or does it reveal a reviewable relation?
Is this community / theme / graph-neighborhood signal only a retrieval cue, or does it point to a concrete candidate point that can be reviewed?
Is the underlying TextUnit / source anchor available, or are we only looking at a generated briefing?
Does this signal require a local reviewed claim, pattern, or decision to be rechecked?
What supports the point?
What challenges it?
Is the challenge fatal, major, minor, out of scope, or unresolved?
What qualifications limit where it applies?
Is it still valid for the current time, version, project, environment, and action?
Has it been superseded or invalidated by a newer point, decision, source, or observed result?
What risks must be carried forward?
```

### Step 6: Update Cluster

Accepted signals update the point cluster.

Rejected signals stay auditable.

Graph retrieval signals follow the same rule:

```text
community report -> briefing / review cue
graph rank -> retrieval priority
auto-extracted relation -> candidate_relation
TextUnit anchor -> provenance
reviewed evidence + rationale -> possible support
```

### Step 7: Promote

Promotion is allowed only when a cluster is reviewed.

For any claim, pattern, anti-pattern, decision, reviewed relation, or action-basis
promotion, the target must first be represented as a self-contained review
candidate record:

```text
candidate point / cluster
-> fixed candidate body + body_hash
-> Evidence Packet + Evidence Sufficiency Gate
-> reviewer approval of that exact body
-> writeback / archive receipt
```

This gate protects review/writeback alignment. It does not create truth,
confidence, reviewed relations, automatic promotion, or action readiness by
itself.

Promotion examples:

```text
claim:
  two independent sources support a narrow factual point

pattern:
  several sources show the same reusable design

anti-pattern:
  repeated evidence shows a failure mode

decision:
  reviewed pattern + project fit + risk + rollback
```

### Step 7.1: Decision Superseding

When new evidence or a new reviewed decision replaces an older decision,
do not delete the old decision.

Record the replacement link and mark downstream affected knowledge for review:

```yaml
decision_superseding:
  old_decision:
  replacement_decision:
  supersession_reason:
  scope:
    project:
    version:
    environment:
    timeframe:
    conditions:
  affected_claims: []
  affected_patterns: []
  affected_relations: []
  affected_context_packs: []
  mark_review_due: true
  audit_note:
```

Rules:

```text
Old decision remains historical and auditable.
Replacement decision must link back to what it supersedes.
Affected claims, patterns, relations, or context packs are marked review_due when their action basis depended on the old decision.
Superseding changes applicability, not past truth.
If the replacement scope is narrower than the old decision, do not retire the old decision globally.
```

Before promotion, run a lightweight Evidence Sufficiency Gate:

```yaml
evidence_sufficiency:
  state: sufficient | weak | insufficient | out_of_scope | risky
  checked_for: promotion | reviewed_relation | decision | action_basis | risk_sensitive_answer
  missing: []
  required_next_step: proceed | ask_user | retrieve_more | create_missing_point | narrow_scope | mark_not_actionable | needs_review
  reviewer_note:
```

Rules:

```text
Do not run this gate for ordinary capture or ordinary query.
Run it for promotion, strong reviewed relation, decision, context pack / action basis, risk_sensitive_answer, or explicit "is this enough?" questions.
sufficient can proceed.
weak must expose gaps and weak support.
insufficient cannot produce promotion or ready action basis.
out_of_scope needs a scope mismatch note.
out_of_scope may require narrow_scope instead of more retrieval.
risky needs action_readiness: risky or needs_review.
retrieve_more is a recommendation unless the user explicitly authorizes retrieval.
```

Known omission check is review input, not action readiness.

For context-pack, action-basis, risk-sensitive, or explicit "is this enough" reviews, check whether known support, known counterevidence, known gaps, and known conflicts are visible. The result may be enough_for_action_basis_review, not_enough, or conflicting.

This check must not create a global evidence pool, coverage score, automatic retrieve_more action, truth confidence, or ready action basis. Missing evidence or visible conflict creates review pressure, scope narrowing, or a next-step recommendation only.

## 5. Promotion Rules

### Claim Promotion

Minimum:

```text
at least one source-backed candidate point
source range or excerpt
evidence_support marked direct_support, or inferential_support with reviewer_note
evidence_sufficiency not insufficient / out_of_scope for promotion
no unresolved high-severity contradiction
reviewed collision signals if cross-source support is claimed
```

Strong candidate:

```text
2+ independent source families support it
or 1 primary source directly supports it
```

### Pattern Promotion

Minimum:

```text
one or more reviewed claims
one reusable design statement
applicable context
failure condition
negative evidence or explicit "not found yet"
```

### Decision Promotion

Minimum:

```text
reviewed source-backed basis
risk
preconditions
rollback
success metric
feedback path
evidence_sufficiency checked for action_basis or decision
```

## 6. What Must Not Be Automated

v0.1 forbids:

```text
auto cross-checked from similarity
auto support from similarity
auto confidence increase from repetition
counting same-origin copies as independent support
counting AI summaries as independent sources
auto contradiction resolution
auto promotion to claim / pattern / decision
auto creation of reviewed relations from calibration signals
vector score as evidence
graph traversal / PPR / association score as evidence
association neighborhood activation as promotion support
silent overwrite of older claims
```

## 6.1 Evidence-Aware Review Fields

When a candidate point, cluster, claim, pattern, anti-pattern, or decision is reviewed, prefer this compact review panel:

Lazy boundary:

```text
Ordinary candidate capture does not need the full panel.
It only needs a short uncertainty / risk note when relevant.

Expand the full support / challenge / qualification / risk panel only for:
claim / pattern / anti-pattern / decision promotion
context pack / action basis
strong reviewed relation
explicit contradiction
stale or contested claim
reviewer-requested standing check
```

```yaml
review_state: candidate | reviewed | rejected
knowledge_state: standing | contested | stale | superseded | retired
attack_assessment:
  severity: fatal | major | minor | out_of_scope | unresolved
  reason:
  affected_scope:
  requires_review_due: true | false
qualification:
  applies_when:
  does_not_apply_when:
  version_scope:
  project_scope:
  domain_scope:
  time_scope:
  environment_scope:
  assumptions:
review_summary:
  why_it_still_holds:
  strongest_challenge:
  challenge_kind: rebuttal | undercut | scope_limit | source_hygiene | stale_assumption | action_failure
  scope_limits:
  known_risks:
  review_due_when:
    - new_primary_source
    - contradiction
    - correction_or_retraction
    - source_version_change
    - dependency_release_change
    - action_failure
    - missed_feedback
    - stale_assumption
  minimal_revision_needed: keep | refine_scope | mark_contested | mark_stale | supersede | reject
action_readiness:
  state: ready | not_ready | risky | needs_review
  reason:
```

Rules:

```text
reviewed means it was examined.
standing means it currently holds.
contested means it has a material challenge.
stale means time, version, or scope may have moved.
stale is review pressure, not automatic expiry.
valid_until / out_of_scope is an applicability boundary, not historical falsity.
action_readiness is separate from truth status.
not_enough_evidence is a valid review result, not a failure to produce an answer.
action_failure can trigger review_due through the Use Ledger; it does not directly reject the reviewed point.
```

Relations also need state:

```yaml
relation_state: candidate | reviewed | rejected | stale
```

Rules:

```text
candidate relation:
  suggested by calibration

reviewed relation:
  accepted with evidence and rationale

rejected relation:
  looked related, but review says it is not a valid relation

stale relation:
  used to hold, but time, version, or scope changed
```

## 7. Lint Rules

First lint checks:

```text
candidate point without source_refs
candidate point without source_range or excerpt
promotion support from URL-only source_ref
promotion support from evidence_role: background_context
promotion or ready action basis support from prior chat memory, agent memory, or model background without current source span support
promotion support from inferential_support without reviewer_note
promotion support from span_supports_target: unsupported or unclear
dynamic data evidence used for promotion or ready action basis without query/filter/subset/as-of/result-set identity
promotion or ready action basis with evidence_sufficiency: insufficient
ready action basis with evidence_sufficiency: out_of_scope or risky
collision signal still pending but used for promotion
support signal with source_independence: same-origin counted as independent
contradiction signal ignored during promotion
point cluster promoted with no reviewed signals
point cluster promoted while status: conflicted
decision promoted without rollback or feedback path
significant action basis without intent_confirmation or success_criteria
high confidence claim with only abstract/snippet/URL/summary source access
valid_until expired but downstream action basis not marked review_due or out_of_scope
stale/review_due used as if it were proof of invalidity
decision outcome recorded without recommendation, confidence_at_decision, user_choice, or outcome_note
```

## 8. First Field Test

Use 10 real sources.

Expected output:

```text
10 source traces
20-50 candidate points
10-30 collision signals
3-8 point clusters
1 promoted claim or pattern candidate
1 visible contradiction or near_miss
```

Success condition:

```text
The queue makes it easier to see recurring ideas and conflicts than reading the source list manually.
```

Failure condition:

```text
The queue produces noisy clusters that cannot support promotion decisions.
```

If it fails, adjust point granularity and source independence rules before adding embeddings or scoring.

## 9. Formal Operator Convention: Audit Shell v1 / Queue-First Operator Cockpit

Status:

```text
ready_for_formal_operator_only_operation_convention
formal operator-only operation convention
not schema guidance
not truth-layer guidance
not user-facing UI
not automatic evidence / truth authority
recurrence / grouping default-off
```

Current handoff:

```text
00_handoff/2026-06-04-audit-shell-v1-formal-graduation-handoff.md
```

Formal verdict:

```text
outputs/review/2026-06-04-audit-shell-v1-formal-graduation-verdict.md
outputs/review/2026-06-04-audit-shell-v1-formal-adoption-recommendation.md
```

Historical candidate record:

```text
outputs/review/2026-06-04-audit-shell-v1-candidate-operation-convention.md
```

Full alpha lineage now lives inside the main vault:

```text
outputs/review/audit-shell-v1-full-alpha-lineage-2026-06-04/
```

This directory keeps the June 1 through June 4 audit shell alpha materials intact:

```text
full ingest simulation
pressure test
800 independent oracle pilot lineage
queue-first cockpit prototype
Pro review package
final closeout package
intermediate zip snapshots
```

Formal operator rule:

```text
Use queue-first cockpit as the formal operator-only convention for backstage
source / record / evidence triage. Do not treat it as reviewed truth,
schema guidance, truth-layer guidance, user-facing UI, or automatic
evidence / truth authority.
```

Hard boundary:

```text
deferred_review_unless_promoted items must generate a promotion receipt and
move to review_now / blocking / regressed before they can be used as
action-basis, rule/convention basis, conflict handling, explicit challenge
handling, or high-risk answer support.

anchor-strength strip is only a front-face summary. Only selector-grade
jump-back can claim evidence landing. source / claim / context / diagnostic /
history / binary landing cannot be described as evidence support.
```

Graduation evidence:

```text
initial formal pilot: 200 / 200 row_pass=true
high-intensity supplement: 3701 total result rows, 0 failures, 0 hard failures
exact eligible evidence anchors verified: 1453
weak legacy evidence anchors quarantined: 67
source-family adversarial cases verified: 480
first-screen unresolved remains 43 vs direct full audit 152
```

Grouping / merging remains parked:

```text
outputs/review/2026-06-04-audit-shell-v1-grouping-default-off-future-note.md
```
