# Fusion Architecture v0.2 Draft

Status: draft for external review
Project: Verified Action Knowledge System / verified second brain
Date: 2026-05-28
Scope: architecture synthesis only; not an implementation plan

Reading note: sections 0-13 preserve the first synthesis path. Sections 14-26
append the Pro review revision and are the current v0.2 interpretation for
naming, MVP relation types, risk placement, and core/runtime/parked boundaries.

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
Verified-action truth core inside.
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
-> review candidate
-> point collision / relation check
-> reviewed verified node
-> context pack / action basis
-> human or agent action
-> feedback event
```

This is the spine that prevents the project from becoming a pile of attractive but unrelated ideas.

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
3. Reviewed verified nodes
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

#### 3. Reviewed Verified Nodes

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

Core relation types:

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
2. Memory tier
3. Dev context
4. Context pack / action basis
5. Feedback / query-run
6. Dusk-style workbench
7. Retrieval / cache
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

#### 2. Memory Tier

Memory tier controls activation, not truth.

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
hot != true
warm != verified
cold != useless
```

Memory tier belongs in runtime, not truth core.

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
```

Feedback cannot directly adjust:

```text
truth confidence
verification_status
source reliability
decision outcome
```

This is one of the project's main original design choices.

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

### 5.2 Point Collision

When a new point enters, it should collide with old points:

```text
support
contradict
refine
replace
expose risk
```

This is the memory-formation mechanism.

It helps the system avoid isolated notes.

### 5.3 Activation Feedback

Feedback does not make a statement true or false.

Feedback tunes future activation.

This prevents a self-reinforcing belief machine.

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
Reviewed evidence ranks trust.
```

### Conflict 4: Proactive Synthesis vs Hallucinated Insight

Resolution:

```text
Every synthesis item must cite specific notes.
No citation, no insight.
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
-> Activation Tier where possible

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

Feedback cannot adjust directly:

```text
truth confidence
verification_status
source reliability
decision outcome
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
