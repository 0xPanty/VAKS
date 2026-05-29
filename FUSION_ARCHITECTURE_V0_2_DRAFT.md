# Fusion Architecture v0.2 Draft

Status: draft for external review
Project: Verified Action Knowledge System / verified second brain
Date: 2026-05-28
Scope: architecture synthesis only; not an implementation plan

Reading note: sections 0-13 preserve the first synthesis path. Sections 14-26
append the Pro review revision and are the current v0.2 interpretation for
naming, MVP relation types, risk placement, and core/runtime/parked boundaries.

Current controlling interpretation:

```text
Public architecture:
  Capture -> Understand -> Review -> Connect -> Act and Learn

Internal engineering loop:
  source -> candidate points -> calibration / point collision -> review -> reviewed node or relation -> context pack / action basis -> intent confirmation when significant -> action -> feedback / outcome

Second-brain model:
  explanation and design checklist, not implementation structure.

Risk / Inhibition:
  cross-cutting control, not the final step.

Proactive Synthesis, Expression, and Agent Safety:
  runtime, output, or parked future layers; not truth core.

Evidence-Aware Review:
  review asks whether a candidate still stands under support, challenge,
  scope limits, and risk. It does not automatically decide winners.

Evidence Sufficiency Gate:
  before a context pack / action basis is finalized as action-ready,
  ask whether the assembled evidence is enough for this specific use.
  Ordinary capture and ordinary queries stay light.

Association Neighborhood Activation:
  queries should activate evidence-aware neighborhoods, not isolated chunks.
  Graph traversal, PPR, similarity, and association score are recall signals,
  not support, confidence, truth, or reviewed relation creation.

Graph Retrieval Stratification:
  GraphRAG / LightRAG-style graph retrieval can organize recall into
  low-level source / text unit / claim / entity retrieval, high-level
  pattern / theme / community retrieval, and relation-neighborhood traversal.
  These strata prepare context; they do not decide trust.

Temporal Applicability Check:
  truth is source-backed.
  Applicability is time-, version-, and scope-bound.
  A standing claim may still be stale, superseded, or out of scope for action.
  Stale means review pressure; expired means applicability boundary.

RKA-inspired Action Guardrails:
  significant action gets intent confirmation / backbrief.
  user verbatim input is kept separate from model interpretation.
  maintenance manifest reports health gaps without automatic repair.
  no full source span means no high confidence.
  decision outcome calibration improves future recommendations, not truth.

Activation Tier:
  the vault has activation tiers, not truth tiers.
  Hot means read early, not believe more.

Strict checks are lazy gates:
  ordinary capture stays light
  ordinary query stays simple
  promotion gets strict
  action basis gets auditable
```

## 0. Plain-English Summary

This project is not trying to build a prettier Obsidian vault, another RAG app, or a large all-in-one agent runtime.

The goal is a **verified second brain**:

```text
Capture information easily.
Turn important material into reviewed knowledge.
Connect new points to old points.
Surface contradictions instead of hiding them.
Package trusted context for decisions and action.
Learn from feedback without rewriting truth.
```

The current fusion is:

```text
Karpathy-simple outside.
Dusk-style workbench nearby.
Reviewed-action core inside.
Optional retrieval, synthesis, publishing, and agent tooling around it.
```

The system should feel simple in daily use:

```text
add source
ask what the vault knows
review candidates
make a context pack
record feedback
```

The strict parts should appear only when knowledge is promoted, used for decisions, or exposed to agents.

## 1. The Main Line

The stable main line is:

```text
raw source
-> candidate points
-> calibration / point collision against local reviewed knowledge
-> review candidate points and calibration outputs
-> reviewed / evidence-backed node
-> reviewed relation where appropriate
-> context pack / action basis
-> human or agent action
-> feedback event
```

This is the spine that prevents the project from becoming a pile of attractive but unrelated ideas.

Calibration happens before promotion, not before understanding.

```text
Raw source does not collide with the whole vault.
Candidate points collide with local reviewed knowledge.
The result is review input, not truth.
```

Every borrowed idea must answer:

```text
Does it help this chain?
Does it reduce work or improve judgment?
Does it preserve source and evidence?
Does it keep dashboard / retrieval / metadata away from truth authority?
Can it fail without damaging the core record?
```

If the answer is no, it stays outside core or is rejected.

## 2. What This Is Not

This is not:

```text
a PARA folder system
a generic concept wiki
a fully automated Obsidian rewrite agent
a vector database with notes attached
a dashboard-first productivity vault
a Claude/ChatGPT prompt pack
a plugin-heavy second-brain runtime
a dev-agent automation suite
```

Those references contain useful parts. None of them owns the architecture.

## 3. Core Architecture v0.2

The architecture has three rings:

```text
Ring 1: Truth Core
Ring 2: Runtime / Workbench Layer
Ring 3: Parked Future Modules
```

The biggest v0.2 change is that the core should be thinner.

Earlier drafts sometimes treated memory tier, dev context, context pack, feedback, proactive synthesis, and agent safety as if they were all equally core. They are important, but they are not all truth core.

### Ring 1: Truth Core

The truth core is small.

It contains only what is needed to make knowledge traceable, reviewable, connected, and falsifiable.

```text
1. Source provenance
2. Candidate / review queue
3. Reviewed / evidence-backed nodes
4. Reviewed relations
5. Negative evidence / risk
6. Promotion rules
```

#### 1. Source Provenance

Purpose:

```text
Know where material came from.
Keep enough source identity to review it later.
Do not rewrite raw material into conclusions.
```

Minimum:

```text
source path or URL
title
author / publisher when known
captured date
published / updated date when known
version / commit / DOI when relevant
why it was captured
processing level
```

Source provenance uses a small PROV-inspired vocabulary, not the full PROV stack.

Plain mapping:

```text
source identity = entity
capture / extraction = activity
human / model / tool = agent
```

Default source records stay flat and light.

```yaml
source_id:
source_uri:
source_type:
version_or_commit:
captured_at:
captured_by:
processing_level: light | medium | heavy
```

Medium or heavy sources may add optional extraction/provenance details:

```yaml
extraction:
  extracted_at:
  extracted_by:
  model:
  tool:
  source_ranges: []

provenance:
  model: PROV-lite
  activities:
    - type: captured
      at:
      by:
    - type: extracted
      at:
      by:
      tool:
      model:
  agents:
    - id:
      type: human | model | tool
```

Do not duplicate the same values in root fields and nested provenance unless the source is important enough to need an explicit audit trail.

Review, promotion, and context-pack use are recorded in their own records:

```text
reviewed_by -> reviewed node / reviewed relation
promoted_by -> promotion event or reviewed node
used_sources -> context pack / use ledger
```

Provenance records traceability. It does not decide truth, support, confidence, or action readiness.
A source link is not evidence. Evidence must support the specific point or relation.

This is the foundation. Without source provenance, later synthesis becomes untrustworthy.

#### 2. Candidate / Review Queue

Purpose:

```text
Let AI extract useful points without letting AI create truth directly.
```

Candidate records can include:

```text
summary candidates
claim candidates
pattern candidates
anti-pattern candidates
decision candidates
implementation-note candidates
missing-point candidates
```

Rule:

```text
Candidate is not truth.
Candidate is material for review.
```

RKA-style review queue taxonomy is useful here as a small routing vocabulary,
not as a runtime to copy:

```yaml
review_queue_item:
  item_type: low_confidence_claim | contradiction | missing_evidence | synthesis_needed | decision_superseded
  suggested_action: approve | reject | merge | override | request_evidence | mark_review_due | create_missing_point
```

This block is optional queue routing.
Ordinary candidates can rely on `point_type`, `verifiability`, and `review_route` without becoming queue items.

Interpretation:

```text
low_confidence_claim:
  useful but not promotion-ready

contradiction:
  challenge must stay visible

missing_evidence:
  a specific point or relation lacks support

synthesis_needed:
  multiple candidates or clusters need one reviewed judgment

decision_superseded:
  a newer decision or evidence package may replace an older decision for a scope
```

Boundary:

```text
Queue actions resolve workflow.
They do not directly create truth, confidence, reviewed relations, or action readiness.
```

#### 2.1 Verifiability Routing

Design note:

```text
VERISCORE's useful lesson is not the metric itself.
It is the distinction between verifiable and unverifiable content.
Not every useful candidate is a factual claim.
```

The project borrows that idea as a review-queue routing rule:

```text
Before review, each candidate point is routed by:
1. what kind of point it is
2. whether it is verifiable
3. what review path it needs
```

This prevents interpretations, hypotheses, preferences, risks, decisions, implementation notes, and open questions from being forced into claim-style truth verification.

Candidate point means atomic review unit, not atomic claim.

Minimal routing fields:

```yaml
point_type: claim | interpretation | hypothesis | pattern | risk | preference | decision | open_question | implementation_note
verifiability:
  state: verifiable | partially_verifiable | not_verifiable | unknown
  reason:
review_route: evidence_check | rationale_check | instance_check | risk_check | action_basis_check | personalization_only | research_question | code_anchor_check
```

`review_route` defaults from `point_type` and can be overridden by a reviewer.

Default mapping:

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

Confidence boundary:

```text
Only verifiable claims can receive truth / evidence confidence.
Unverifiable does not mean useless.
It means no truth confidence.
```

Other point types may have:

```text
rationale_strength
instance_support
risk_evidence_level
action_readiness
usefulness
scope_fit
research_value
```

Routing is review input.
It does not promote truth.

#### 2.2 Optional Point Graph Fragment

GraphFC's useful lesson is not the full graph fact-checking pipeline.
It is that complex claims can lose precision when represented only as natural-language sub-claims.

Most candidate points stay as natural-language review units.
For high-impact, complex, multi-hop, cross-document, action-relevant, or ambiguous points, the reviewer may attach an optional `point_graph_fragment`.

The fragment decomposes the point into entities and relation triplets so reviewers can see exactly what is being calibrated or checked.

It helps:

```text
understand complex points
improve point collision beyond semantic similarity
expose entity, relation, qualifier, and scope ambiguity
support evidence-aware review
provide triplet-level detail for coverage maps when needed
```

Minimal shape:

```yaml
point_graph_fragment:
  purpose: collision_check | evidence_review | scope_clarification | action_basis | ambiguity_resolution
  entities:
    - id:
      label:
      type:
      aliases: []
      resolution:
        status: resolved | unresolved | ambiguous
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
      blocks_review: true | false
```

Use only when natural-language review is too coarse or ambiguous.
If a fragment needs more than 3-5 essential triplets, split the candidate point instead.

Important boundaries:

```text
point_graph_fragment is a review aid, not a reviewed relation.
triplet extraction is not truth.
triplet similarity is not support.
triplet conflict is not automatic rejection.
Only reviewed relations enter the formal knowledge graph.
Do not require graph fragments for ordinary candidate points.
Do not build a full GraphFC pipeline in MVP.
```

A graph fragment can make review more precise, but it can also make a wrong extraction look precise.
When a triplet cannot be source-anchored, treat it as a review question.

#### 3. Reviewed / Evidence-backed Nodes

The formal knowledge nodes are:

```text
source
summary
claim
pattern
anti-pattern
decision
qa
implementation-note
```

High-impact nodes need:

```text
source reference
verification_status
evidence_level
confidence
known gaps
negative evidence where relevant
relations where relevant
```

#### 4. Reviewed Relations

Relations are not decorative links. They are the knowledge graph's reasoning edges.

Earlier relation pool from the first synthesis:

```text
supports
contradicts
refines
replaces
implements
applies_to
derived_from
inspired_by
risk_of
alternative_to
blocked_by
```

Current v0.2 MVP relation types are intentionally smaller:

```text
supports
contradicts
refines
risk_of
derived_from
```

The larger pool is parked for future use; it is not the current core enum.

Strong relations must include:

```text
evidence
rationale
confidence
last_verified
```

Dashboard links, tag overlap, backlinks, vector similarity, and search rank can suggest relations. They cannot become reviewed relations by themselves.

#### 5. Negative Evidence / Risk

Risk is not a footnote.

The system needs first-class negative memory:

```text
anti-patterns
contradictions
source hygiene warnings
known failure routes
wrong-scope warnings
stale claims
```

This is the immune system of the vault.

#### 6. Promotion Rules

Promotion is the path from raw material to reusable knowledge.

```text
raw source
-> candidate point
-> collision / comparison
-> reviewed claim or pattern
-> decision / implementation-note when action is needed
```

Promotion is manual or review-mediated in v0.2.

No automated direct-to-truth path.

### Ring 2: Runtime / Workbench Layer

This layer makes the truth core usable.

It is allowed to be helpful, fast, visual, proactive, and agent-friendly.

It is not allowed to decide truth.

Runtime / workbench modules:

```text
1. Karpathy-simple operating surface
2. Activation tier
3. Dev context
4. Context pack / action basis
5. Feedback / query-run
6. Dusk-style workbench
7. Retrieval / cache / association neighborhood activation
8. API / MCP / agent access
9. Proactive synthesis
10. Expression / publishing
11. Agent tool safety
```

#### 1. Karpathy-Simple Operating Surface

This is the default user experience.

Borrowed from Karpathy-style LLM Wiki:

```text
raw/
wiki/
index
log
ingest
query
lint
```

Why it stays:

```text
It keeps daily use light.
It makes the system understandable.
It prevents every note from becoming paperwork.
```

What we do not borrow:

```text
generic wiki pages as truth
unreviewed AI compilation as final knowledge
```

#### 2. Activation Tier

Activation tier controls what gets read early, not what is more true.

MemGPT's useful lesson is the fast / slow memory management intuition under limited context.
The vault borrows this as activation discipline, not as an autonomous memory OS.

```text
hot:
  read early for this scope

warm:
  reusable, nearby, not always loaded

cold:
  archived or historical, still findable
```

Rules:

```text
The vault has activation tiers, not truth tiers.
Hot means read early, not believe more.
hot != true
warm != verified
cold != useless
```

The field name may remain `memory_tier` for schema compatibility.
The concept should be explained as Activation Tier.
Activation tier belongs in runtime, not truth core.

#### 3. Dev Context

Dev context is a temporary working table for a project.

Layers:

```text
Core:
  must read, must obey

Support:
  useful background

Risk:
  contradictions, anti-patterns, do-not-forget warnings

Cold References:
  source trail and history, opened only when needed
```

The important design is not "load more context."

The important design is:

```text
load the right context
keep risk separate
refresh when scope changes
do not make dev context permanent truth
```

#### 4. Context Pack / Action Basis

Context pack is a runtime export.

It packages:

```text
supporting claims
contradicting claims
patterns
anti-patterns
decisions
sources
gaps
confidence
risk
next action
```

It does not create truth.

It is a way to hand verified context to a human or agent.

##### 4.1 Association Neighborhood Activation

HippoRAG's useful lesson is not the full retrieval stack.
It is the association retrieval idea:

```text
The vault does not retrieve isolated chunks.
It activates an evidence-aware association neighborhood.
```

For this vault, a query should light up the relevant neighborhood around the question:

```text
supporting reviewed points
challenging reviewed points
risk / anti-pattern
old decisions
scope / version / condition notes
source and evidence anchors
gaps, missing points, and review_due markers
```

This belongs to Activation and Context Pack preparation.
It is a runtime / workbench capability, not truth core.

It may use:

```text
reviewed relations
activation tier
dev context
risk refs
scope notes
source anchors
retrieval scores
graph traversal / PPR-style neighborhood expansion
```

Boundaries:

```text
association retrieval is recall and activation, not truth.
graph traversal is not support.
PPR / association score is not confidence.
similarity is not evidence.
activated neighbors are not reviewed relations.
Only reviewed evidence and rationale can support action.
Only reviewed relations enter the formal knowledge graph.
```

GraphRAG / LightRAG add a useful retrieval refinement:

```text
low-level retrieval:
  source / text unit / claim / entity

high-level retrieval:
  pattern / theme / community / community report

relation neighborhood:
  reviewed relation neighborhood around the query seed
```

This is graph retrieval stratification.
It helps a context pack avoid being just a few similar chunks.
It can bring concrete anchors and broad pattern context into the same draft envelope.

Boundary:

```text
TextUnit anchor is provenance, not support.
community report is briefing, not truth.
graph rank is retrieval priority, not trust.
auto-extracted relation is candidate material, not reviewed relation.
candidate relation traversal must be labeled candidate_relation_neighborhood,
not reviewed_relation_neighborhood.
```

Trigger lightly for ordinary queries.
Expand the neighborhood for decisions, action basis, risk_sensitive_answer, promotion review, strong reviewed relation review, explicit audit, challenged answer, or explicit contradiction/risk check.

##### 4.2 Claim / Point Coverage Map

PaperTrail's useful lesson is not the interface itself.
It is that citations are too coarse for serious verification.

Context pack is not a citation list.
It is a coverage map for the key points used in an answer or action basis.

Context packs must be coverage-aware, but they should not default to a full audit table.
Full `coverage_map` detail is required only for key judgments used in the answer or action basis.

For each key point, the context pack should show whether it is:

```text
supported by source anchors or reviewed nodes
weakly supported
challenged by contradictions, attacks, counterexamples, or risks
missing needed evidence
out of scope for the current project, version, time, or action
not verifiable because it is a preference, open question, hypothesis, or interpretation
marked with risk flags for the proposed action
```

Minimal shape:

```yaml
coverage_overview:
  supported:
  weakly_supported:
  challenged:
  missing_evidence:
  out_of_scope:
  risk_flags:

coverage_map:
  - point:
    point_type:
    coverage_status: supported | weakly_supported | challenged | missing_evidence | out_of_scope | not_verifiable
    support_refs: []
    challenge_refs: []
    risk_refs: []
    critical_omissions: []
    note:

action_readiness:
  state: ready | not_ready | risky | needs_review
  reason:
```

Important boundaries:

```text
Coverage map is an audit surface, not a truth layer.
Coverage status does not automatically change confidence.
Missing evidence does not mean false.
Challenged does not mean rejected.
Critical omissions are known major omissions only, not a full omission scan.
Non-verifiable points can still receive rationale, risk, or action-basis coverage.
Risk flags summarize risk presence; concrete risks stay in risk_refs and action_readiness.
Coverage map consumes evidence_support: direct_support can count as supported, inferential_support with reviewer_note can count as weak or reviewer-accepted support, background_context cannot count as supported, and counterexample becomes challenged or risk.
```

Progressive disclosure:

```text
Level 1: coverage overview by counts and high-risk items.
Level 2: key point coverage for important claims, risks, and decisions.
Level 3: evidence detail with source anchors, reviewed nodes, ranges, and review notes.
```

Default context packs should show the overview first.
Full evidence mapping should expand only for decisions, action basis, agent context packs, high-impact answers, explicit audit requests, challenged answers, or user-expanded points.

##### 4.3 Temporal Applicability Check

Graphiti / Zep's useful lesson is not automatic graph construction.
It is that facts and relations need validity windows.

For this vault:

```text
Truth is source-backed.
Applicability is time-, version-, and scope-bound.
```

This strengthens the Truth / Usefulness / Scope Fit split:

```text
truth:
  Is this point source-backed and reviewed?

usefulness:
  Did this point help answer this kind of question?

scope fit:
  Is this point valid for the current time, project, version, environment, and action?
```

Minimal shape:

```yaml
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
  check_state: in_scope | out_of_scope | stale | superseded | unknown | needs_review
  reviewer_note:
```

Boundaries:

```text
validity window is applicability metadata, not automatic truth.
valid_until / superseded_by does not erase old records.
out_of_scope does not mean false.
stale does not mean rejected.
automatic invalidation is not allowed in the truth core.
episodes / raw sources remain provenance; reviewed nodes and relations still need review.
```

Use this check for promotion, decisions, action basis, strong reviewed relation, risk_sensitive_answer, stale / contested points, or explicit "does this still apply?" questions.
Ordinary capture can leave validity windows blank.

##### 4.4 Decision Superseding

Decision superseding is a special case of temporal applicability and review pressure.

When new evidence or a newer decision replaces an older decision, the old decision
remains in the vault with an audit trail.

Minimal shape:

```yaml
decision_superseding:
  old_decision:
  replacement_decision:
  supersession_reason:
  applies_to:
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
```

Rules:

```text
old decision is not deleted
replacement decision links back to the old decision
affected downstream claims / patterns / relations / context packs are marked review_due
supersession changes current applicability, not historical auditability
```

This absorbs the RKA-style decision-superseding lesson without importing a runtime, MCP, or dashboard.

##### 4.5 Evidence Sufficiency Gate

Evidence Sufficiency Gate asks whether the current evidence is enough for the intended use.

It is different from Evidence Support Check:

```text
Evidence Support Check:
  Does this source span support this point or relation?

Evidence Sufficiency Gate:
  Is the available evidence enough for this context pack, action basis, decision, promotion, or strong relation?
```

This borrows the control idea from Self-RAG, CRAG, and A2RAG: do not escalate every query; escalate only when evidence is insufficient for the intended action.

The gate does not run in empty space. First assemble an activated evidence envelope or draft context pack, then run the gate, then finalize the context pack / action basis only if the evidence is sufficient for that use.
Temporal applicability is part of this envelope when the answer or action depends on current time, version, project, environment, or supersession state.

Minimum shape:

```yaml
evidence_sufficiency:
  state: sufficient | weak | insufficient | out_of_scope | risky
  checked_for: context_pack | action_basis | decision | promotion | reviewed_relation | risk_sensitive_answer
  missing: []
  required_next_step: proceed | ask_user | retrieve_more | create_missing_point | narrow_scope | mark_not_actionable | needs_review
  reviewer_note:
```

Trigger only for:

```text
promotion to reviewed memory
strong reviewed relation
context pack / action basis
decision
risk_sensitive_answer
explicit "is this enough / can we act" user question
```

Do not trigger for ordinary capture, ordinary query, or low-impact brainstorming.

Gate questions:

```text
Is there at least one reviewed support or direct primary source support?
Do key points have source anchors and evidence_support?
Are known contradictions, challenges, and risks included?
Does the evidence match the current project, version, time, and environment?
Does the reviewed point still apply, or is it stale, superseded, invalidated, or out of scope?
Is any critical evidence missing?
If evidence is not enough, should the system ask, retrieve more, create a missing-point candidate, narrow scope, mark not actionable, or require review?
```

Boundaries:

```text
Evidence Sufficiency Gate is not a truth layer.
It does not automatically change confidence.
It does not run automatic retrieval, web search, agentic retrievers, or correction loops.
retrieve_more is a recommendation unless the user explicitly authorizes retrieval.
weak evidence can support a cautious answer, but not a ready action basis.
insufficient evidence cannot produce action_readiness: ready.
out_of_scope requires a scope mismatch note.
out_of_scope may require narrow_scope rather than more retrieval.
risky requires action_readiness: risky or needs_review.
superseded or invalidated points cannot produce action_readiness: ready without an explicit replacement basis.
```

##### 4.6 Intent Confirmation / Backbrief Gate

Evidence sufficiency asks whether the basis is good enough.
Intent confirmation asks whether the system is about to do the right thing.

Use this gate only for significant action:

```text
architecture changes
implementation or deployment
multi-step mission
high-impact decision
irreversible or hard-to-rollback work
risk-sensitive action basis
```

Minimum shape:

```yaml
intent_confirmation:
  required: true | false
  restated_intent:
  assumptions: []
  scope_in: []
  scope_out: []
  success_criteria: []
  verification_plan:
  user_confirmed: true | false
  confirmation_ref:
```

For executor-style handoffs, use the same shape as a backbrief:

```yaml
backbrief:
  plan_summary:
  acceptance_criteria_interpretation:
  numbered_assumptions: []
  risks: []
  files_or_surfaces_expected:
  verification_method:
  approved_by:
```

Boundaries:

```text
Do not trigger for ordinary Q&A, simple capture, or low-impact edits.
This gate aligns intent; it does not decide truth.
If the user has already explicitly confirmed the intent in the current context, reference that confirmation instead of asking again.
```

#### 5. Feedback / Query-Run

Feedback improves future activation.

It does not directly rewrite truth.

The key split:

```text
truth confidence:
  Is the point true or well-supported?

usefulness:
  Did this point help answer this kind of question?

scope fit:
  Does this point apply to this project, version, time, or intent?
```

Feedback can adjust:

```text
usefulness
scope fit
activation ranking
route / keyword hints
missing-point candidates
review_due
```

Feedback cannot directly adjust:

```text
truth confidence
verification_status
source reliability
```

This is one of the project's main original design choices.

Reflexion and Reflective Memory Management support this boundary:

```text
feedback becomes verbal reflection / use memory
use memory guides later activation and decisions
use memory does not directly rewrite truth
```

Conservative rule:

```text
Positive feedback is weak.
Negative feedback creates review pressure.
Explicit correction creates review_due.
```

##### 5.1 Decision Outcome Calibration

Decision outcome calibration records whether a decision recommendation later worked.

It belongs to Use Ledger / Feedback, not to truth verification.

Minimum shape:

```yaml
decision_outcome:
  decision_ref:
  action_basis_ref:
  recommendation:
  confidence_at_decision:
  user_choice:
  outcome: succeeded | failed | mixed | unresolved
  outcome_note:
  recorded_by:
  recorded_at:
  affects:
    - future_recommendation
    - risk_calibration
    - scope_fit
    - option_framing
  never_affects_directly:
    - truth_confidence
    - verification_status
    - source_reliability
```

Later runtime can compute calibration metrics such as Brier, ECE, override rate, escape-hatch rate, or near-miss rate.

MVP rule:

```text
record outcomes first.
do not compute heavy metrics until enough decisions have outcomes.
outcomes improve future recommendation behavior, not truth.
```

#### 6. Dusk-Style Workbench

Dusk validates the need for a project desktop.

Useful ideas:

```text
scope dashboard
area / project page
task mailbox
closeout / cooling surface
```

Adopted boundary:

```text
dashboard is a candidate surface
dashboard is not truth
dashboard does not replace dev context
```

#### 7. Retrieval / Cache

Retrieval belongs outside the truth core.

Useful tools:

```text
BM25
vector search
RRF
GraphRAG
QMD
Zilliz
SQLite / FTS cache
```

Purpose:

```text
find candidate material
provide compact briefings
help choose what to read
```

Boundary:

```text
retrieval rank is not trust
cache is rebuildable
Markdown/YAML wins if cache disagrees
```

#### 8. API / MCP / Agent Access

Future agents should consume the vault through read-first interfaces.

Access levels:

```text
read-only
suggest-only
reviewed-write
owner-final
```

Early rule:

```text
No MCP write tools before review queue and write boundaries are stable.
```

#### 9. Proactive Synthesis

Borrowed from Vellum / Claude + Obsidian workflows.

Purpose:

```text
make the vault return to the user
surface non-obvious connections
surface repeated patterns
surface contradictions
surface unresolved questions
```

Minimal format:

```text
Connections
Patterns
Contradictions
Open Questions
```

Hard rule:

```text
Every item must trace back to a specific note or source.
No generic insight.
No automatic truth.
```

This belongs in runtime / review, not truth core.

#### 10. Expression / Publishing

This is parked, not core.

Purpose:

```text
turn reviewed or review-ready insights into external output:
posts
articles
reports
README sections
decision memos
research notes
```

Boundary:

```text
publishing draft is product output, not truth
reader reaction can become feedback
engagement metrics cannot directly change confidence
```

#### 11. Agent Tool Safety

Borrowed from ECC / AgentShield, but only as light rules.

Purpose:

```text
make sure Codex, Claude Code, MCP tools, hooks, skills, and future agents do not damage the vault
```

Minimal rules:

```text
use only tools needed for the task
read broadly, write narrowly
ask before destructive / external / credential / hook / MCP / bulk operations
session learning becomes candidate feedback, not automatic rule
do not promote candidate output to truth without review
```

This should be a one-page rule set later, not a security platform in v0.2.

### Ring 3: Parked Future Modules

These are valuable but should not distract the core.

```text
full hosted API
full MCP write surface
heavy vector/RAG stack
desktop app
automated scheduled synthesis
automatic publishing pipeline
agent security scanner / CI
multi-agent developer workflow
full gbrain / OpenKB / ECC runtime
```

They stay parked until the manual verified loop proves value.

## 4. Human Brain Mapping

This project can be explained as a brain model, as long as the metaphor stays disciplined.

```text
Capture:
  sensory input

Activation:
  activation tier and dev context

Comprehension:
  summaries and candidate points

Reviewed Memory:
  reviewed claims, patterns, anti-patterns, decisions

Association:
  reviewed relations and point collision

Proactive Synthesis:
  on-demand resurfacing first; scheduled synthesis later

Decision Support:
  context pack and action basis

Use Ledger / Feedback:
  usefulness, scope fit, activation ranking

Cooling / Reactivation:
  cold references and lazy reactivation

Risk / Inhibition:
  anti-patterns, contradiction, source hygiene, safety gates

Expression:
  publishing, reports, README, memos

Motor Safety:
  agent tool safety and execution discipline
```

The important warning:

```text
The brain can suggest.
Review decides.
Evidence wins.
```

## 5. Original Design Contributions

These are the main designs that emerged from this project rather than being copied whole from any single reference.

### 5.1 Verified Action Knowledge System

The project is not "store knowledge and search it."

It is:

```text
preserve source
extract candidate
review and connect
support action
record outcome
learn from feedback
```

### 5.2 Knowledge Calibration / Point Collision

Point Collision is the vault's knowledge calibration mechanism.

It borrows the useful part of truth-maintenance / reason-maintenance thinking: do not only store conclusions; keep track of why the vault currently believes something, what supports it, what challenges it, and what new evidence should trigger review.

The conceptual ancestor is Jon Doyle's 1979 paper "A Truth Maintenance System" (`raw/papers/2026-05-29-truth-maintenance-system-source.md`). The project does not copy the old AI system. It only absorbs the control idea:

```text
beliefs need reasons
new evidence should update review pressure
actions should be explainable from recorded reasons
```

When a new source produces candidate points, those points are compared with local reviewed claims, patterns, anti-patterns, decisions, and risks.

The calibration asks:

```text
Does this candidate support an existing judgment?
Does it challenge or contradict one?
Does it refine scope, version, time, or conditions?
Does it expose a risk in an existing pattern or decision?
Does it show that an older assumption may be stale?
Does it reveal missing evidence, synthesis need, decision superseding, or a review question?
```

The output is not truth.

It is review input:

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

This is the memory-formation mechanism: the vault slowly forms a local reviewed worldview by repeatedly checking new distilled points against existing reviewed knowledge.

Neither side wins automatically:

```text
External material can calibrate local knowledge.
Local reviewed knowledge can calibrate external material.
Review decides what changes.
```

Important boundary:

```text
Similarity can suggest calibration.
Similarity is not support.
Conflict is not automatic rejection.
Repetition is not automatic truth.
Only reviewed evidence and rationale can create reviewed relations.
```

### 5.2.1 Evidence-Aware Review / Support-Challenge Review

Review is not a mathematical logic engine and not an automatic debate system.

It is a human-readable standing check:

```text
Does this candidate still stand after support, challenge, scope limits, and risk are visible?
```

The useful idea is borrowed from abstract argumentation work such as Dung's 1995 paper on argument acceptability (`raw/papers/2026-05-29-dung-argumentation-framework-source.md`), but the project does not implement formal argumentation semantics. It only absorbs the review habit:

```text
do not review support alone
also review attacks, qualifications, risks, and unresolved questions
```

Lazy boundary:

```text
Ordinary candidate capture does not need the full review panel.
It only needs a short uncertainty / risk note when relevant.

Expand the full support / challenge / qualification / risk panel only for:
promotion
decision
context pack / action basis
strong reviewed relation
explicit contradiction
stale or contested claim
reviewer-requested standing check
```

Human-facing review families:

```text
support:
  evidence that supports the point

attack:
  evidence that challenges, contradicts, or weakens the point

qualification:
  scope, condition, version, time, or assumption limits

risk:
  failure mode, negative evidence, unsafe use, anti-pattern

provenance:
  source trail or derivation path
```

Rough mapping to schema relation types:

```text
supports     -> support
contradicts  -> attack
refines      -> qualification
risk_of      -> risk
derived_from -> provenance
```

This is a rough mapping, not perfect equivalence. `refines` can be an improvement or a qualification. `derived_from` is provenance, not support by itself.

Important rules:

```text
Provenance tells where a point came from.
Support tells whether evidence actually supports the point.
A citation is not automatically evidence.
A URL-only source reference is provenance, not support.

Multiple support edges do not automatically increase confidence.
They increase review evidence.
Confidence changes only through review.
```

#### 5.2.2 Evidence Support Check

Evidence Support Check is the bridge between provenance and review.

It asks a narrower question than citation faithfulness:

```text
Does this cited source span actually support this target point, node, or relation?
```

The project borrows the warning from ProVe and RAG attribution work, but it does not implement automated ProVe, NLI, RTE, support scoring, or causal citation faithfulness. It records human-reviewed evidence support for cited spans.

Minimum evidence item fields:

```yaml
evidence_support:
  span_supports_target: supported | partial | unsupported | unclear
  evidence_role: direct_support | inferential_support | background_context | counterexample
  reviewer_note:
```

Rules:

```text
Evidence support lives on evidence items, not on Source nodes.
To count as support, an evidence item needs a source range, quote, code anchor, table anchor, or equivalent source span.
background_context can remain as context, but it cannot count as supported or raise confidence.
inferential_support needs reviewer_note before it can count as promotion support.
counterexample belongs in challenge_refs or risk_refs.
span_supports_target = unsupported or unclear cannot be used as promotion support.
For strong reviewed relations, evidence must support the edge itself, not merely the two endpoint nodes.
Evidence support does not automatically change confidence.
```

Coverage mapping rule:

```text
supported + direct_support can count as supported.
partial + inferential_support + reviewer_note can count as weakly_supported, or reviewer-accepted promotion support.
background_context never counts as support.
counterexample belongs in challenge_refs or risk_refs, not support_refs.
unsupported / unclear cannot count as promotion support.
```

This is a review rule, not a new truth layer or standalone module.

Attack assessment:

```yaml
attack_assessment:
  severity: fatal | major | minor | out_of_scope | unresolved
  reason:
  affected_scope:
  requires_review_due: true | false
```

Meaning:

```text
fatal:
  directly breaks the current judgment

major:
  does not necessarily break it, but must appear in context packs or decisions

minor:
  a boundary case, exception, or weak counterexample

out_of_scope:
  looks like an attack, but applies to a different version, project, domain, time, or condition

unresolved:
  unclear which side is stronger; mark contested or review_due
```

Qualification should name the condition, not just say "it depends":

```yaml
qualification:
  applies_when:
  does_not_apply_when:
  version_scope:
  project_scope:
  domain_scope:
  time_scope:
  environment_scope:
  assumptions:
```

Node standing should describe the current knowledge state:

```yaml
status: candidate | standing | contested | stale | superseded | rejected
```

Meanings:

```text
candidate:
  not reviewed yet

standing:
  reviewed and currently holds

contested:
  reviewed but materially challenged

stale:
  may be outdated or shifted out of scope

superseded:
  replaced by a newer reviewed node

rejected:
  reviewed and not accepted
```

Action readiness stays separate from node standing:

```yaml
action_readiness:
  state: ready | not_ready | risky | needs_review
  reason:
```

A node can be standing but not useful for this action. A contested node can still inform a low-risk or reversible action if the risk is explicit.

Minimum review summary:

```yaml
review_summary:
  why_it_still_holds:
  strongest_challenge:
  scope_limits:
  known_risks:
  review_due_when:
```

In plain language:

```text
This currently holds because ...
The strongest challenge is ...
It applies when ...
The main risk is ...
Review this again when ...
```

Relations also need state:

```yaml
relation_state: candidate | reviewed | rejected | stale
```

Candidate relations come from calibration. Reviewed relations require evidence and rationale. Rejected relations are useful because they prevent repeated false links.

### 5.3 Activation Feedback

Feedback does not make a statement true or false.

Feedback tunes future activation.

This prevents a self-reinforcing belief machine.

Useful analogy:

```text
Reflexion:
  task feedback -> verbal reflection -> episodic memory -> later behavior

This vault:
  query/action feedback -> use ledger -> future activation / scope fit / review_due
```

### 5.4 Conversation-Derived Feedback

The next user turn can reveal weak feedback:

```text
same-line follow-up:
  route may be useful

narrower question:
  scope should narrow

correction:
  route was wrong

missing:
  create missing-point candidate

topic shift:
  do not persist positive signal
```

This is useful only because it is conservative.

RMM-style prospective / retrospective reflection maps here as:

```text
forward-looking:
  summarize routes, scope hints, missing points, and future retrieval cues

backward-looking:
  inspect cited evidence, missed contradictions, and failed retrieval paths
```

Both produce feedback events or review candidates, not truth updates.

### 5.5 Truth / Usefulness / Scope Fit Split

This is essential.

```text
truth:
  evidence and verification

usefulness:
  did it help answer?

scope fit:
  does it apply here?
```

Many systems confuse these three.

This system must not.

### 5.6 Risk as First-Class Context

Risk is not a footnote in Support.

Risk is a decision checkpoint.

This is why dev context has a separate Risk layer.

### 5.7 Traceability-First, Graduated Verification

Capture should not feel like paperwork.

Heavy verification should happen when material is promoted or used for action.

This avoids two bad extremes:

```text
too light:
  summaries become untraceable

too heavy:
  every note becomes bureaucracy
```

## 6. Reference Source Map

### Karpathy LLM Wiki

Adopt:

```text
simple raw/wiki operating loop
LLM as maintainer
Obsidian as IDE
index/log/query/lint mindset
```

Do not adopt:

```text
unreviewed wiki compilation as truth
```

### llm-wiki-compiler

Adopt:

```text
ingest and compile mechanics
review queue
claim-level provenance
context pack envelope
static lint
future API/MCP/viewer reference
```

Do not adopt:

```text
generic page schema as truth
watch auto-recompile as formal promotion
full viewer/MCP stack before core proof
```

### gbrain

Adopt:

```text
Markdown system of record
facts / takes / hypotheses / bets / decisions
holder / timeline / gaps
compiled truth plus append-only timeline
think-answer-citation-gaps discipline
```

Do not adopt:

```text
full runtime
minions
scheduler
OAuth
HNSW/reranker stack
```

### OpenKB

Adopt:

```text
long-document tree index
wiki foundation / generator surface separation
skill output adapter
path-scoped agent writes
ghost wikilink whitelist
source hash / idempotent ingest ideas
```

Do not adopt:

```text
auto-compiled generic concept wiki as reviewed truth
direct rewrite into formal nodes
```

### obsidian-second-brain

Adopt:

```text
AI-readable preamble
never create in isolation
two-output rule
progressive context loader
health checks
write-time discipline
```

Do not adopt:

```text
background agent rewrite
scheduled conflict resolution
full vault runtime before schema stability
```

### PARA

Adopt:

```text
actionability routing
archive-first lazy reactivation
project goal gate
project closeout scan
```

Do not adopt:

```text
PARA folders as truth architecture
physical file movement as primary memory tier
```

### Kepano

Adopt:

```text
property-driven context workbench
link overlap as related-context hint
random revisit for cold memory maintenance
view-first activation
```

Do not adopt:

```text
link overlap / tags / ratings / recency as evidence
```

### Dusk

Adopt:

```text
scope dashboard
task mailbox
monthly closeout / cooling surface
project desktop feel
```

Do not adopt:

```text
all-in-one plugin-heavy vault runtime
dashboard as truth authority
```

### knowledge-base-server

Adopt:

```text
token-efficient context briefing
shared agent retrieval layer with governed writes
operational session capture
incremental vault index cache
```

Do not adopt:

```text
auto-classify/promote/writeback without review
full hosted server stack now
```

### HippoRAG

Adopt:

```text
association retrieval for context activation
query-triggered neighborhood expansion
LLM + graph retrieval as recall inspiration
support / challenge / risk / decision / scope appearing together
```

Do not adopt:

```text
full HippoRAG stack as a core module
LLM-generated graph as the formal knowledge graph
Personalized PageRank as evidence or confidence
graph traversal as truth or reviewed relation creation
```

### GraphRAG / LightRAG

Adopt:

```text
TextUnit-style source anchors for traceability
low-level retrieval for source / text unit / claim / entity
high-level retrieval for pattern / theme / community
relation-neighborhood retrieval for context activation
community / theme reports as briefings
incremental graph index updates as cache-maintenance inspiration
```

Do not adopt:

```text
full GraphRAG or LightRAG runtime as core architecture
community summary as truth
graph rank as trust
auto-extracted relation as reviewed relation
LLM-derived claim status as verification_status
incremental index update as automatic truth update
```

### Graphiti / Zep

Adopt:

```text
temporal validity windows for facts and relations
valid_from / valid_until style applicability metadata
superseded_by / invalidated_by as review and action warnings
episode / raw-source traceability as provenance discipline
```

Do not adopt:

```text
automatic graph construction as reviewed knowledge
automatic invalidation as truth update
graph database runtime as the Markdown source of truth
agent memory platform as core architecture
```

### Reflexion / Reflective Memory Management

Adopt:

```text
feedback as verbal reflection / use memory
episodic feedback records guiding later activation
forward-looking reflection for future retrieval cues
backward-looking reflection for cited-evidence and missed-contradiction review
```

Do not adopt:

```text
feedback-driven truth confidence changes
hidden reinforcement learning over reviewed knowledge
weight updates or model learning as vault truth
positive feedback as proof
```

### MemGPT

Adopt:

```text
virtual context management intuition
fast / slow memory as activation priority
explicit movement between active context and archive
context-window discipline for agent work
```

Do not adopt:

```text
agent OS as core architecture
autonomous memory manager before manual loop works
hot / warm / cold as truth tiers
hidden paging that bypasses context-pack evidence boundaries
```

### RKA / Research Knowledge Assistant

Current source status:

```text
Repository identified: https://github.com/infinitywings/rka
Checked commit: 7bc2d76efba61b92db5b056220f7009763003a0d
Source record: raw/repos/2026-05-29-rka-source.md
```

Adopt:

```text
review queue item taxonomy:
  low_confidence_claim
  contradiction
  missing_evidence
  synthesis_needed
  decision_superseded

audit-preserving decision superseding:
  old decision remains
  replacement decision links back
  affected downstream knowledge becomes review_due

intent confirmation / backbrief for significant action:
  restated intent
  assumptions
  scope
  success criteria

verbatim input preservation:
  user original words separate from model interpretation

maintenance manifest:
  provenance gaps, orphaned records, stale dependencies, and missing links as lint items

staleness / validity split:
  valid_until is applicability
  stale / review_due is review pressure

empty valid_until:
  no reviewed expiry boundary has been recorded yet; not globally valid forever

confidence cap without full text:
  abstract / snippet / URL-only material cannot receive high evidence confidence

decision outcome calibration:
  recommendation, confidence, user choice, and outcome improve future recommendations
```

Do not adopt:

```text
full runtime
MCP surface
dashboard
workflow actions as truth changes
SQLite as the source of truth
calibration metrics as truth confidence
automatic background repair
```

### Kagantic

Adopt:

```text
hierarchical Markdown index routing
summary/tag pre-read before full note read
source hygiene caution
```

Do not adopt:

```text
trusting binary vault download artifacts
```

### Vellum / Claude + Obsidian Articles

Adopt:

```text
daily / weekly proactive synthesis
connections / patterns / contradictions / open questions
traceable synthesis rule
accumulated context as compounding asset
```

Do not adopt:

```text
automatic movement of raw material
generic insight without note trace
daily brief as truth
auto-publishing
```

### ECC / AgentShield

Adopt:

```text
agent capability selection
tool safety mindset
security check before agent write surfaces
think-before-code discipline
session learning as candidate, not rule
```

Do not adopt:

```text
full Claude Code plugin stack as core
automatic continuous learning into rules
agent security platform before actual agent surface exists
```

## 7. Repeatedly Validated Directions

Multiple references independently support these directions:

```text
Markdown / files should remain the durable record.
AI output should enter as candidate first.
Source trace matters more than pretty organization.
Views and dashboards are useful but not authoritative.
Retrieval should recall candidates, not decide truth.
Queries should activate evidence-aware association neighborhoods, not isolated chunks.
Applicability should be checked against time, version, project, environment, and supersession state.
Activation tiers should guide what to read first without changing trust.
Context should be briefed before full-read when the vault grows.
Agent access needs explicit write boundaries.
Old material should cool, not disappear.
Contradictions are valuable outputs, not failures.
Daily/weekly synthesis is useful only when traceable.
```

These can become strong patterns.

## 8. Main Conflicts And Decisions

### Conflict 1: Simple Capture vs Verified Truth

Resolution:

```text
Capture stays light.
Promotion gets strict.
```

### Conflict 2: Dashboard Convenience vs Truth Authority

Resolution:

```text
Dashboard displays and filters.
Markdown/YAML decides.
```

### Conflict 3: Retrieval Power vs Evidence Discipline

Resolution:

```text
Retrieval ranks candidates.
Association traversal recalls context.
Reviewed evidence ranks trust.
Temporal applicability gates action use.
```

### Conflict 4: Proactive Synthesis vs Hallucinated Insight

Resolution:

```text
Every synthesis item must cite specific notes.
No citation, no insight.
```

### Conflict 4b: Standing Truth vs Current Applicability

Resolution:

```text
Truth is source-backed.
Applicability is time-, version-, and scope-bound.
```

### Conflict 4c: Activation Priority vs Truth Confidence

Resolution:

```text
The vault has activation tiers, not truth tiers.
Hot means read early, not believe more.
```

### Conflict 5: Agent Learning vs Memory Pollution

Resolution:

```text
Session learning becomes feedback candidate.
Repeated and reviewed learning can become pattern or rule.
```

### Conflict 6: Rich Architecture vs User Burden

Resolution:

```text
The default interface stays small.
Strict fields appear only at promotion or action use.
```

## 9. What Should Be Core, Plugin, Parked, Or Rejected

### Core

```text
source provenance
candidate / review queue
verified nodes
reviewed relations
negative evidence / risk
promotion rules
```

### Runtime / Plugin

```text
memory tier
dev context
context pack
feedback event
Dusk dashboard
Obsidian Bases
retrieval / cache
API / MCP read surface
proactive synthesis
publishing / expression
agent tool safety
```

### Parked

```text
full desktop app
full API server
MCP write tools
heavy vector database
scheduled automation
automatic daily synthesis
automatic publishing
agent security scanner / CI
multi-agent coding runtime
```

### Rejected For Core

```text
dashboard state as truth
retrieval rank as trust
PARA folders as truth layer
generic concept wiki as reviewed truth
LLM direct-to-truth compilation
automatic conflict resolution
automatic promotion
plugin-heavy all-in-one vault runtime
```

## 10. Anti-Frankenstein Rules

These rules prevent the system from becoming a collage.

```text
1. One core, many modules.
   The core is verified-action truth.

2. Every module must know its layer.
   Workbench is workbench. Retrieval is retrieval. Publishing is product output.

3. No module may create truth directly.

4. If a feature requires changing the truth model before proving value, it starts outside core.

5. If a feature increases daily burden, it must prove a large judgment-quality gain.

6. If a feature can fail, Markdown/YAML must still be readable and authoritative.

7. If a feature cannot explain its source trail, it cannot become action basis.
```

## 11. Minimal Validation Path

Do not validate with a full app.

Do not validate with embeddings first.

Do not validate with automation first.

Validate with a tiny manual trial.

### 3-Source Micro-Trial

Use:

```text
1 paper / deep article
1 repository
1 official document or strong source
```

For each source:

```text
extract 3-5 candidate points
record source anchors
mark uncertainty
```

Across sources:

```text
create 2-3 supports / contradicts / refines / risk_of relations
promote 1 claim or pattern candidate
record 1 negative evidence or contradiction
```

Then ask one real question twice:

```text
Answer A:
  without the verified mini-core

Answer B:
  using the verified mini-core / context pack
```

Compare:

```text
Did B reduce irrelevant context?
Did B preserve contradictions?
Did B cite sources better?
Did B avoid overclaiming?
Did B produce a clearer action basis?
```

If yes, expand to the 10-source point collision trial.

If no, adjust:

```text
candidate point size
relation criteria
source independence
risk handling
context pack format
```

Do not add automation until the manual loop improves answers.

## 12. Review Questions For External Models

Please review this draft against these questions:

```text
1. Is the main line coherent, or is this still a pile of borrowed ideas?
2. Is the truth core thin enough?
3. Which runtime modules still look too core-like?
4. What should be deleted or delayed?
5. Does the human-brain metaphor clarify the architecture or add noise?
6. Does the design beat a plain Karpathy wiki, a plain RAG app, or a plain Claude+Obsidian workflow?
7. Where would implementation become painful?
8. What is the smallest trial that could falsify or validate the architecture?
9. What is the easiest way this becomes over-engineered?
10. What should the README say in one minute to an open-source user?
```

## 13. Current Judgment

Current architecture direction:

```text
positive
```

Need to shrink:

```text
yes
```

What to shrink:

```text
truth core
```

What to preserve:

```text
verified-action boundary
light capture
review before truth
risk as first-class
activation not truth
feedback not truth
```

Can the project move from architecture design to minimal loop trial?

```text
yes
```

But the next step should be a manual micro-trial, not implementation of automation.

Final plain-English call:

```text
The skeleton is good.
The danger is adding every good organ at once.
Keep the core small, prove the loop, then attach modules only when they earn their place.
```

---

# v0.2 Revision After Pro Review

Status: revision notes appended after external Pro review
Purpose: preserve the original draft above while recording the tighter architecture direction
Do not treat this as a new implementation plan yet

## 14. What Changed After Review

The Pro review did not reject the architecture.

It sharpened the main warning:

```text
The brain model is useful as an explanation and design-checking language.
It should not become the engineering module structure.
```

The original draft correctly identified the main parts, but it still made too many things look equally central.

The revision is:

```text
Make the core thinner.
Make the public story simpler.
Move risk, provenance, traceability, and safety into cross-cutting controls.
Move synthesis, publishing, dashboards, retrieval, and agent safety out of the core.
```

## 15. Revised Public Story: Five Layers

For README and open-source users, the system should not start with 10-12 brain layers.

Use five plain layers:

```text
1. Capture
   Save sources without forcing instant judgment.

2. Understand
   Turn sources into candidate claims, patterns, risks, and questions.

3. Review
   Promote only source-backed, reviewed knowledge into durable memory.

4. Connect
   Compare new points with old points:
   supports, contradicts, refines, risk_of.

5. Act and Learn
   Build context packs for decisions,
   record feedback,
   improve future activation without rewriting truth.
```

Short boundary:

```text
The system can suggest.
Only reviewed evidence can support action.
Feedback improves activation, not truth.
```

This is the open-source-facing story.

The deeper brain model stays as an internal explanation, not the first thing a new user sees.

## 16. Revised Main Loop

The main loop should be expressed as a loop, not a long list of brain organs.

```text
Capture
-> Understand
-> Review
-> Connect
-> Activate
-> Act
-> Feedback
-> Re-review / Cooling
```

Expanded:

```text
Capture:
  preserve source and context

Understand:
  create summaries and candidate points

Review:
  promote only reviewed claims, patterns, risks, and decisions

Connect:
  create reviewed relations and point collisions

Activate:
  choose what matters for this question or project

Act:
  create context pack / action basis

Feedback:
  record usefulness, scope fit, misses, contradictions, and outcomes

Re-review / Cooling:
  update review_due, cool one-off context, reactivate useful material when needed
```

This loop is the engineering story.

## 17. Cross-Cutting Controls

These should not be modeled as late-stage modules.

They run across the whole loop.

```text
Provenance:
  every important point should trace back to source.

Traceability:
  every output used for action should explain where it came from.

Risk / Inhibition:
  contradictions, negative evidence, source hygiene, and anti-patterns must surface early.

Safety Gate:
  agent or automation writes must respect scope, permissions, and review boundaries.
```

Risk especially should not be the last step.

Risk appears at every stage:

```text
Capture:
  source hygiene

Understand:
  uncertainty and possible hallucination

Review:
  contradiction and negative evidence

Connect:
  false relation risk

Activate:
  wrong-scope warning

Act:
  rollback and failure mode

Feedback:
  missed contradiction triggers review_due
```

## 18. Renaming Decisions

The Pro review found several names that could mislead open-source readers.

Adopt these names in the current document pass:

```text
Attention
-> Activation

Memory Tier
-> Activation Tier

Verified Memory
-> Reviewed Memory or Evidence-backed Memory

Forgetting
-> Cooling

Feedback Learning
-> Use Ledger when referring to records
```

Why:

```text
hot/warm/cold are activation priority, not truth levels.
Use Activation Tier as the public name.
reviewed memory is more honest than verified memory.
cooling means lower activation, not deletion.
feedback records use, not truth.
```

## 19. Revised Internal Brain Model

The internal brain model can stay, but it should be grouped by role.

Do not present these as 12 equal modules.

```text
Input:
  Capture

Activation:
  activation tier
  dev context
  context activation

Comprehension:
  source digest
  summary
  candidate point
  missing point

Reviewed Memory:
  claim
  pattern
  anti-pattern
  decision

Association:
  point collision
  reviewed relations

Action:
  context pack
  decision support
  implementation note

Learning:
  query-run
  feedback-event
  action outcome
  review_due
  cooling / reactivation

Cross-Cutting Inhibition:
  risk
  negative evidence
  contradiction
  source hygiene
  safety gate

Optional Output:
  proactive synthesis
  expression / publishing
```

This preserves the brain metaphor without letting it drive the module tree.

## 20. Candidate-Only Boundaries

Two areas need especially strict wording.

### Comprehension

Comprehension outputs are candidates.

```text
summary:
  source-level digest, not reviewed memory

candidate point:
  extracted idea, not claim

candidate pattern:
  possible reusable pattern, not adopted pattern

missing point:
  review work, not truth update
```

### Proactive Synthesis

Proactive synthesis is a candidate generator.

It should not be first implemented as scheduled daily automation.

Start on-demand:

```text
synthesize recent material since 7 days
```

Output:

```text
Connections
Patterns
Contradictions
Open Questions
```

Rules:

```text
must cite specific note or source
no generic insight
candidate only
no automatic update to reviewed memory
```

## 21. MVP Relation Types

The schema can keep more relation types for future compatibility.

But the first validation should use only five:

```text
supports
contradicts
refines
risk_of
derived_from
```

Why:

```text
small enough to review by hand
enough to test point collision
enough to preserve positive, negative, refinement, risk, and provenance links
```

Defer:

```text
replaces
implements
applies_to
inspired_by
alternative_to
blocked_by
```

These can return after the first micro-trial proves relation quality.

## 22. Use Ledger, Not Feedback Truth

Feedback should be treated as a use ledger.

It records how knowledge was used, not whether it became true.

Reflexion and RMM support the non-parametric learning shape:

```text
learn from use by storing reflection / feedback records
do not update truth confidence directly
use negative feedback to create review pressure
```

Minimal use ledger records:

```text
query-run
context-pack snapshot
feedback-event
action outcome
review_due marker
cooling / reactivation event
```

MVP should stay light:

```text
append-only file or simple Markdown record
no scoring engine
no feedback database first
no automatic confidence update
```

Feedback can adjust:

```text
usefulness
scope fit
activation ranking
missing-point candidate
review_due
```

Feedback event families:

```text
explicit_correction
missing_evidence
scope_mismatch
answer_helpful
contradiction_missed
action_outcome
```

Feedback cannot adjust directly:

```text
truth confidence
verification_status
source reliability
decision outcome
```

Polarity rule:

```text
Positive feedback is weak.
Negative feedback creates review pressure.
Explicit correction creates review_due.
```

## 23. Expression And Agent Safety Stay Outside The Main Brain Diagram

Expression / Publishing:

```text
valuable later
optional output surface
not part of the core knowledge loop
not first implementation
```

Agent Tool Safety:

```text
valuable when agents can write or execute
parked until there is a real agent write surface
one-page rules first, not a security platform
```

This prevents the project from looking like:

```text
knowledge system
+ publishing factory
+ agent runtime
+ security platform
```

The v0.2 story should stay:

```text
verified knowledge loop first
extensions later
```

## 24. Revised Core / Runtime / Parked Classification

### Truth Core

```text
source provenance
candidate / review queue
reviewed memory
reviewed relations
negative evidence / anti-pattern / contradiction
promotion rules
```

### Use Ledger

```text
query-run
context-pack snapshot
feedback-event
action outcome
review_due
cooling / reactivation event
```

Use Ledger does not decide truth.

It records what happened when knowledge was used.

### Runtime / Workbench

```text
activation tier
dev context
dashboard
retrieval / cache
context activation
association neighborhood activation
on-demand proactive synthesis
read-only API / MCP
```

### Parked

```text
scheduled daily synthesis
expression / publishing pipeline
agent tool safety file
MCP write surface
agent security scanner
desktop app
heavy RAG
automatic publishing
```

## 25. Revised Minimal Validation

The original 3-source micro-trial still stands, but the success criteria should use the new framing.

Use:

```text
1 paper or deep article
1 repository
1 official document or strong source
```

For each:

```text
capture source provenance
create source-level digest
extract 3-5 candidate points
mark uncertainty
```

Across sources:

```text
create only these relation types:
  supports
  contradicts
  refines
  risk_of
  derived_from

promote:
  1 reviewed claim or pattern
  1 negative evidence / contradiction
```

Then compare two answers to the same real question:

```text
Answer A:
  no reviewed mini-core

Answer B:
  with reviewed mini-core and context pack
```

Success means B is measurably better in at least three ways:

```text
fewer irrelevant sources
clearer source trace
visible contradiction or risk
less overclaiming
clearer action basis
better scope fit
```

Failure means:

```text
candidate points too large or vague
relations too noisy
source independence too weak
risk layer not visible
context pack too verbose
```

If the micro-trial fails, do not add automation.

Fix the loop first.

## 26. Revised Final Judgment

After Pro review, the judgment is:

```text
The architecture is directionally strong.
The main risk is over-explaining it into too many layers.
The core should shrink.
The brain model should explain, not define, the engineering structure.
The next work should be document tightening, then one manual micro-trial.
```

One-line version:

```text
Keep the verified knowledge loop as the system.
Use the brain model as the explanation.
Let every other idea earn its place as a module.
```
