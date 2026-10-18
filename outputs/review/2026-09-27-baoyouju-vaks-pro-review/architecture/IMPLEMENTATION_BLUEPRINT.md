---
type: implementation-note
status: active
created: 2026-05-27
updated: 2026-06-14
project: verified-action-knowledge-system
related_decisions:
  - "[[2026-05-27-karpathy-simple-verified-strict-ux-principle]]"
  - "[[2026-05-27-karpathy-spine-modular-extensions]]"
  - "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
  - "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
  - "[[2026-05-27-codex-mediated-ingest-and-review-gate]]"
  - "[[2026-05-27-traceability-first-graduated-verification]]"
related_patterns:
  - "[[review-gated-compile-queue]]"
  - "[[claim-level-provenance-source-ranges]]"
  - "[[accumulated-source-cross-validation]]"
  - "[[context-pack-evidence-envelope]]"
  - "[[static-wiki-health-lint-before-auto-rewrite]]"
  - "[[progressive-vault-context-loader]]"
  - "[[scope-dashboard-live-context-surface]]"
related_anti_patterns:
  - "[[direct-compile-to-truth-layer-without-review]]"
  - "[[generic-concept-schema-as-truth-layer]]"
  - "[[auto-compiled-concept-wiki-as-verified-truth-layer]]"
sources:
  - "[[purpose]]"
  - "[[SCHEMA]]"
  - "[[ARCHITECTURE_PRINCIPLES]]"
  - "[[knowledge-graph-index]]"
  - "[[REVIEW_QUEUE]]"
  - "[[FEEDBACK]]"
  - "[[2026-05-27-karpathy-simple-verified-strict-ux-principle]]"
  - "[[2026-05-27-karpathy-spine-modular-extensions]]"
  - "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
  - "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
  - "[[2026-05-27-codex-mediated-ingest-and-review-gate]]"
  - "[[2026-05-27-traceability-first-graduated-verification]]"
  - "[[SOURCE_INTAKE]]"
  - "[[REFERENCE_REVIEW_PROTOCOL]]"
verification_status: active
evidence_level: synthetic
confidence: high
validated_by:
  - "manual synthesis from active architecture decisions"
rollback_path:
  - "If the implementation becomes too broad, return to Phase 0 and keep only raw/wiki/index/log plus manual review."
last_verified: 2026-06-14
next_review: 2026-06-21
relations:
  - target: "[[ARCHITECTURE_PRINCIPLES]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[IMPLEMENTATION_BLUEPRINT]]"
    rationale: "This blueprint turns the architecture principles into phased implementation boundaries."
    created: 2026-05-27
    last_verified: 2026-05-28
  - target: "[[SCHEMA]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[IMPLEMENTATION_BLUEPRINT]]"
    rationale: "The first implementation phases use SCHEMA as the Markdown truth contract."
    created: 2026-05-27
    last_verified: 2026-05-28
  - target: "[[2026-05-27-karpathy-simple-verified-strict-ux-principle]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[IMPLEMENTATION_BLUEPRINT]]"
    rationale: "The blueprint starts with a Karpathy-simple command surface and hides strict fields behind promotion."
    created: 2026-05-27
    last_verified: 2026-05-28
tags:
  - implementation-blueprint
  - verified-action-knowledge-system
  - karpathy-simple
  - review-gate
  - context-pack
---

# IMPLEMENTATION_BLUEPRINT.md v0.1

## AI-readable preamble

This is the first implementation blueprint for the Verified Action Knowledge System.

The default experience must stay Karpathy-simple: add source, process source, query knowledge, lint vault, make context pack.

Raw capture is traceability-first: keep enough provenance to find the source again. Strict verified-action rules apply only when a candidate is promoted into a formal claim, pattern, anti-pattern, decision, implementation note, or context pack.

The first runnable version must prove one narrow end-to-end loop before adding heavier runtime modules.

As the vault grows, verification should become more comparative: new candidates should be checked against earlier similar points before promotion, instead of forcing every source to be fully verified at capture time.

## 1. Prime Directive

Build this system in this order:

```text
one raw source
-> optional source annotation sidecar
-> one review candidate
-> traceability lint / review
-> one verified wiki node
-> one context pack
-> one feedback note
```

Do not start with the full App, full RAG stack, full MCP server, or autonomous background agents.

The first version should be explainable in one sentence:

```text
Add raw material, compile reviewed knowledge, ask with evidence, export context for action.
```

## 2. User-Facing Surface

The default command surface should stay small:

```text
add source
mark source span
process this
ask what the vault knows
lint / check vault
make context pack
review recent candidates
record action feedback
```

Strict fields, relation edges, negative evidence, actionability, provenance windows, and feedback timelines should appear when needed by promotion or action use. They should not make normal capture feel heavy.

### 2.1 Processing modes

Use three modes instead of one heavy path:

```text
normal question mode:
  Karpathy-simple. Search/read enough, answer, optionally save a light note.

project development mode:
  Dusk-style scope dashboard plus DEV_CONTEXT. Gather related materials, then lock Core / Support / Risk / Cold References.

strong source / decision mode:
  verified-action strictness. Preserve provenance, extract candidate points, compare, review, and write durable patterns/decisions/risks.
```

This means:

```text
ordinary material:
  light processing.

project material:
  medium processing plus source annotation workbench, scope dashboard, or DEV_CONTEXT when needed.

papers, valuable repos, official docs, key architecture material:
  heavy processing.
```

The full rules are in `SOURCE_INTAKE.md`.

### 2.2 Reference review rule

When reviewing external repositories, do not only inspect the active branch question.

Required rule:

```text
Current branch moves forward opportunistically.
Every reference must still be checked against the whole Verified Action Knowledge System.
```

This prevents a memory-tier session from missing useful signals for ingest, review queue, schema, lint, feedback, retrieval, API, viewer, agent access, publishing, or risk.

The detailed checklist is in `REFERENCE_REVIEW_PROTOCOL.md`.

## 3. System Spine

The operating spine is Karpathy-style LLM Wiki:

```text
raw/
wiki/
index.md or wiki/indexes/knowledge-graph-index.md
log.md or outputs/review logs
ingest
query
lint
```

The inner kernel is the verified-action layer:

```text
review gate
source provenance
verification_status
evidence_level
confidence
relations
negative evidence
decision readiness
context pack
feedback timeline
```

Reference libraries are modules, not competing skeletons.

## 4. Phase 0: Markdown-Only Verified Loop

Goal:

```text
Prove the knowledge flow without a runtime stack.
```

Required files:

```text
SCHEMA.md
ARCHITECTURE_PRINCIPLES.md
IMPLEMENTATION_BLUEPRINT.md
wiki/indexes/knowledge-graph-index.md
outputs/review/README.md
```

Minimum workflow:

1. Preserve a source in `raw/`.
2. Optionally pin important source spans as `source_annotation` sidecars.
3. Create a candidate in `outputs/review/`.
4. Manually review traceability first: source path or URL, source annotation refs or source ranges, extracted point, uncertainty.
5. Promote only reviewed content into `wiki/claims/`, `wiki/patterns/`, `wiki/anti-patterns/`, `wiki/decisions/`, or `wiki/projects/`.
6. Update `wiki/indexes/knowledge-graph-index.md`.
7. Create a context pack manually from verified nodes.
8. Record feedback after the context pack is used.

Exit criteria:

```text
At least one source has completed source -> optional annotation -> candidate -> verified node -> context pack -> feedback.
```

## 5. Phase 1: Review Queue Contract

Goal:

```text
Make candidates inspectable, rejectable, promotable, and traceable.
```

Created:

```text
REVIEW_QUEUE.md
templates/review-candidate.md
```

Candidate record must include:

```yaml
candidate_id:
candidate_type: summary | claim | pattern | anti-pattern | decision | implementation-note
source_refs:
source_annotation_refs:
source_ranges:
extracted_points:
uncertainty:
generated_by:
generated_at:
review_status: pending | approved | rejected | needs-edit
promotion_target:
review_notes: []
```

Promotion fields are added only when the target needs them:

```yaml
verification_status:
evidence_level:
confidence:
gaps: []
negative_evidence: []
relations: []
risk:
rollback:
success_metric:
```

Rules:

```text
Candidate is never truth.
Rejected candidates stay auditable.
Approved candidates must name their promotion target.
Promotion requires the fields appropriate to the target type. Raw and candidate records require traceability; claim/pattern/decision/context-pack outputs require stricter verification or action fields.
```

## 6. Phase 2: Lint and Health Checks

Goal:

```text
Make schema and graph problems visible before automation grows.
```

Create next:

```text
LINT_RULES.md
scripts/lint-vault.*
```

First lint checks:

```text
missing required frontmatter
missing source path / URL / source refs
candidate point repeats earlier source without linking it
candidate point contradicts earlier source without marking uncertainty
claim without evidence
pattern without failure conditions
anti-pattern without replacement
decision without rollback
strong relation without evidence or rationale
broken wiki links
stale next_review
candidate promoted without review trail
context pack containing unverified certainty
```

Rule:

```text
Phase 2 reports problems. It does not rewrite formal nodes automatically.
```

## 7. Phase 3: Context Pack Contract

Goal:

```text
Give humans and agents evidence-aware context for answers, decisions, and implementation.
```

Create next:

```text
CONTEXT_PACK.md
templates/context-pack.md
```

Minimum context pack shape:

```yaml
task:
answer_scope:
primary_nodes:
supporting_claims:
contradicting_claims:
patterns:
anti_patterns:
decisions:
sources:
relation_rationale:
gaps:
warnings:
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
    coverage_status:
    support_refs:
    challenge_refs:
    risk_refs:
    note:
action_readiness:
  state:
  reason:
evidence_sufficiency:
  state:
  checked_for: context_pack | action_basis | decision | promotion | reviewed_relation | risk_sensitive_answer
  missing:
  required_next_step: proceed | ask_user | retrieve_more | create_missing_point | narrow_scope | mark_not_actionable | needs_review
  reviewer_note:
confidence:
last_verified:
budget:
truncation_notes:
recommended_next_action:
```

Coverage map is required only for important answer/action points in the first manual trial.
It is not a full PaperTrail implementation and must not become a truth layer.
Context packs must be coverage-aware, but ordinary query output should not become a full coverage audit.
Full `coverage_map` detail is required only for key judgments used in the answer or action basis, especially decisions, agent context packs, high-impact answers, explicit audit requests, or challenged answers.
`risk_flags` only summarizes risk presence; concrete risks stay in `risk_refs` and `action_readiness`.
`evidence_sufficiency` is checked after a draft evidence envelope is assembled and before promotion, decision, strong reviewed relation, context pack / action basis, or risk_sensitive_answer is finalized as action-ready.

Sorting priority:

```text
1. verification_status
2. evidence_level
3. confidence
4. relation strength
5. negative evidence present
6. freshness / last_verified
7. search similarity
```

Search similarity is useful only after trust fields are considered.

## 8. Phase 4: Minimal Compiler Scripts

Goal:

```text
Turn repeated manual steps into scripts without bypassing review.
```

First scripts:

```text
ingest-source
make-candidate
promote-candidate
lint-vault
make-context-pack
update-index
record-feedback
```

Implementation rules:

```text
Scripts write candidates first.
Scripts may promote only when review_status is approved.
Scripts preserve raw sources.
Scripts append logs instead of silently replacing history.
Scripts fail back to Markdown files.
```

## 9. Phase 5: Query Layer

Goal:

```text
Recall relevant verified records without confusing retrieval with truth.
```

Start with simple local search:

```text
frontmatter filters
filename / wiki link search
Markdown text search
relation traversal
```

Then add optional engines:

```text
BM25
vector search
hybrid RRF
graph neighborhood expansion
external stores such as Zilliz
```

Boundary:

```text
Retrieval finds candidates.
Verified nodes decide trust.
Decision records decide action.
```

Phase B query-layer documentation may describe a read-only derived adapter:

```text
build chunk manifest and retrieval receipt artifacts
filter by VAKS authority bucket before ranking
run bucket-local retrieval and rerank
return context-pack candidates with click-back and warnings
require pressure, contract, readiness, and external-review gates before any runtime/default/production adoption beyond this documentation note
```

Do not attach Skills, MCP writes, subagents, formal writeback, or production
claims to Phase B.

## 10. Phase 6: API, MCP, Viewer, and Obsidian Workbench

Goal:

```text
Expose the system without moving truth out of Markdown.
```

Allowed surfaces:

```text
read-only API
context-pack API
MCP read tools
Obsidian Bases views
source annotation workbench
review dashboard
read-only viewer
export adapters
```

Write access boundary:

```text
raw capture: allowed for automation
review candidate: allowed for Codex or suggest-only agents
formal wiki node: reviewed write only
SCHEMA / ARCHITECTURE / decisions: user/Codex explicit review only
```

If API, MCP, viewer, or index cache disagrees with Markdown, Markdown wins.

## 11. Phase 7: Feedback and Learning Loop

Goal:

```text
Make action results update usefulness, scope fit, gaps, and next_review, while creating review work for confidence changes.
```

Feedback note should include:

```yaml
action_taken:
based_on:
expected_result:
actual_result:
worked:
failed:
new_evidence:
confidence_review:
nodes_to_review:
next_review:
```

Feedback may:

```text
support a decision
flag a claim for weakening review
create an anti-pattern
trigger a replacement decision
update next_review
```

Feedback must not silently rewrite old conclusions.

## 12. Extension Points

Modules can be added only behind stable contracts:

```text
source adapters
node schema packs
compile strategies
lint rule packs
retrieval engines
review workflows
context pack modes
agent access tiers
output adapters
feedback adapters
```

Adoption gate:

```text
What layer does it belong to?
What real pain does it solve?
Does it improve verified knowledge, action basis, or extensibility?
Can it consume or output existing Markdown contracts?
Can it fail without damaging the reviewed knowledge layer?
Does it bypass review?
What evidence would prove it should stay?
What would make us remove it?
```

## 13. Agent Access

Default access tiers:

```text
Level 1: read-only
Level 2: suggest-only
Level 3: reviewed write
Level 4: limited auto-write for low-risk outputs
Level 5: full write, forbidden in v0.1
```

Current defaults:

```text
Misa / gbrain / Hermes: read-only or suggest-only
Codex: reviewed write
User: final authority
Automation: raw capture and review outputs only
```

Create next:

```text
AGENT_ACCESS.md
```

## 14. Feedback Calibration

Goal:

```text
Make answers improve from use without letting feedback rewrite truth.
```

Contract:

```text
FEEDBACK.md
templates/feedback-event.md
templates/query-run.md
wiki/patterns/conversation-derived-feedback-routing.md
```

Feedback separates:

```text
truth confidence
usefulness
scope fit
```

Rules:

```text
feedback can adjust usefulness, scope fit, and activation ranking
feedback cannot directly adjust truth confidence or verification_status
feedback can create review work for stale, contradicted, missing, or wrong-scope points
conversation-derived feedback is weak by default and should adjust routes before points
```

This supports query-time activation without creating a self-reinforcing belief system.

First storage rule:

```text
Markdown remains the readable knowledge layer.
JSONL append-only records query-run and feedback-event truth.
SQLite, if added, is only a rebuildable cache.
```

Conversation-derived feedback:

```text
same-line follow-up:
  session-local boost only by default

narrower follow-up:
  create or strengthen route / keyword / channel

correction or wrong scope:
  lower route / scope fit, not truth

missing:
  create missing-point or missing-route candidate
```

## 15. What Not To Build First

Do not start with:

```text
full desktop App
heavy vector database
autonomous scheduled rewrite
automatic conflict resolution
automatic direct-to-truth compilation
polished graph UI before relations are reviewed
MCP write tools before review queue exists
```

These may become useful later, but only after Phase 0 through Phase 3 are stable.

## 16. Immediate Next Files

Recommended order:

```text
1. MEMORY_TIER.md
2. DEV_CONTEXT.md
3. templates/dev-context-pack.md
4. CONTEXT_PACK.md
5. LINT_RULES.md
6. AGENT_ACCESS.md
7. templates/context-pack.md
```

## 17. Current Stop Point

This blueprint defines the implementation route but does not yet implement scripts, API, MCP, viewer, or retrieval.

Next concrete action:

```text
Use the first real project/reference set to create a dev context pack, then run one query-run / feedback-event trial and the 10-source point-collision trial.
```
