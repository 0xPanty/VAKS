---
type: decision
status: active
created: 2026-05-27
updated: 2026-05-27
tags:
  - architecture-principles
  - verified-knowledge-system
  - action-basis
  - extensibility
sources:
  - "[[SCHEMA]]"
  - "[[purpose]]"
  - "[[2026-05-26-architecture-layering-v0-1]]"
  - "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
  - "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
  - "[[2026-05-27-llm-wiki-compiler-implementation-extraction]]"
  - "[[2026-05-27-codex-mediated-ingest-and-review-gate]]"
verification_status: active
evidence_level: synthetic
confidence: high
last_verified: 2026-05-27
next_review: 2026-06-03
relations:
  - target: "[[SCHEMA]]"
    type: constrains
    strength: 5
    confidence: high
    evidence:
      - "[[ARCHITECTURE_PRINCIPLES]]"
    rationale: "Architecture principles define how SCHEMA is used by runtime modules, agents, retrieval, and future extensions."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
    type: implements
    strength: 5
    confidence: high
    evidence:
      - "[[ARCHITECTURE_PRINCIPLES]]"
    rationale: "This file turns the quality bar into concrete adoption and extension rules."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[2026-05-27-implementation-includes-llm-wiki-stack]]"
    type: constrains
    strength: 5
    confidence: high
    evidence:
      - "[[ARCHITECTURE_PRINCIPLES]]"
    rationale: "LLM Wiki stack capabilities are included, but must remain subordinate to verified truth and action-basis contracts."
    created: 2026-05-27
    last_verified: 2026-05-27
---

# ARCHITECTURE_PRINCIPLES.md v0.1

## AI-readable preamble

This vault is a Verified Action Knowledge System.

Do not treat it as a generic Obsidian vault, a generic LLM Wiki, a RAG store, or an agent memory dump.

The system of record is Markdown with structured metadata. Search, vector stores, graph scores, APIs, MCP tools, viewers, and agents are runtime surfaces. They may help find or present knowledge, but they cannot create truth without review.

The main flow is:

```text
raw source
-> ingest / compiler
-> review candidate
-> verified knowledge graph
-> decision / action basis
-> context pack / API / viewer
-> human / agent action
-> feedback timeline
-> updated confidence / gaps / next review
```

The purpose is not only to know. The purpose is to know with evidence, decide with context, act with risk awareness, and learn from the result.

## 1. Main architecture

The main architecture is:

```text
Verified Action Knowledge System
```

This name matters because it decides what belongs in the core.

The system has three inseparable goals:

```text
1. verified knowledge
2. action basis
3. extensible runtime
```

If a feature improves only storage, only search, only UI, or only automation, it is not automatically core. It must serve one of the three goals above.

## 2. Reference designs and their positions

External designs are inputs, not masters.

| Reference | Role in this system | Boundary |
|---|---|---|
| Karpathy LLM Wiki | Basic operating pattern: `raw/`, `wiki/`, `index.md`, `log.md`, ingest, query, lint. | It does not define verified truth or action readiness by itself. |
| `atomicstrata/llm-wiki-compiler` | Engineering reference for ingest, compile, review queue, provenance, lint, context pack, MCP, viewer. | Its generic page schema does not replace source/summary/claim/pattern/anti-pattern/decision. |
| OpenKB | Module reference for long-document tree indexing, wiki/generator layering, Skill Factory, path-scoped agent writes, and ghost-link lint. | Its auto-compiled generic concept wiki does not replace the verified truth layer. |
| gbrain | Epistemic inspiration: fact, take, hypothesis, bet, decision, holder, timeline, gaps. | Do not fork its full runtime before this vault's contracts are stable. |
| obsidian-second-brain | Agentic vault operations: AI-readable preamble, propagation rules, context loading, health checks. | No background rewrite or automatic conflict裁决 in the truth layer. |
| Obsidian Bases / Base Hub | Workbench and review views over structured Markdown. | Views do not define truth. They display and filter records. |
| BM25 / vector / QMD / Zilliz / GraphRAG | Candidate retrieval and ranking. | Retrieval is not verification. |
| Misa / gbrain / external agents | Read-only or suggest-only consumers and candidate proposers. | They do not directly write formal truth without review. |

## 3. Non-negotiable principles

### 3.1 Markdown is the system of record

The durable truth layer lives in Markdown/YAML files.

Runtime indexes, vector stores, API responses, dashboards, graph views, and generated context packs are derived artifacts. If they disagree with the Markdown record, Markdown wins until a reviewed update changes it.

### 3.2 Raw is preserved

`raw/` keeps source material and provenance. Raw material is not rewritten to fit later conclusions.

Compiled wiki nodes may summarize, classify, and relate raw material, but they must not erase the source trail.

### 3.3 Review creates truth

LLM output is a candidate, not a formal node.

A claim, pattern, anti-pattern, decision, or implementation note becomes trustworthy only after it has:

```text
source reference
verification_status
evidence_level
confidence
relations where relevant
known gaps or negative evidence where relevant
```

### 3.4 Search only recalls candidates

BM25, vector search, GraphRAG, Zilliz, QMD, embeddings, rerankers, and graph scores can decide what to read next.

They cannot decide what is true.

### 3.5 Relations are first-class records

Important links are not just Obsidian backlinks. They must be explicit when they affect reasoning.

Each important relation should include:

```yaml
target:
type:
strength:
confidence:
evidence:
rationale:
```

These relation records support context pack ranking, health checks, contradiction scans, and future graph tools.

### 3.6 Actionability is the upgrade from knowledge to decision

The system is not done when it can answer questions. It is useful when it can support action.

Decision and implementation nodes must eventually answer:

```yaml
recommended_action:
decision_status:
expected_gain:
risk:
preconditions:
blocked_by:
rollback:
owner:
review_by:
success_metric:
feedback_source:
```

Not every summary needs this. Any node used as an action basis does.

### 3.7 Extension happens through contracts

The system must be able to absorb future ideas without rewriting the truth layer.

New modules should plug into one of these extension points:

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

If a module requires changing the core truth model before proving value, it starts outside core.

### 3.8 Failure must degrade to Markdown

Any runtime layer must have a fallback:

```text
API down       -> read Markdown
viewer broken  -> read Markdown
vector stale   -> read index and files
agent unsure   -> create review candidate
compiler wrong -> keep raw source and reject candidate
```

If a feature cannot fail gracefully, it is not allowed to hold core truth.

## 4. Layer responsibilities

| Layer | Responsibility | Not responsible for |
|---|---|---|
| Raw source layer | Preserve original sources and provenance. | Deciding truth or action. |
| Ingest / compiler layer | Convert raw material into candidates. | Directly writing verified truth. |
| Review candidate layer | Hold AI/Codex/Misa generated candidates for approve/reject/edit. | Being a permanent dumping ground. |
| Verified knowledge graph layer | Store source, summary, claim, pattern, anti-pattern, decision, qa, implementation-note. | UI, search ranking, or agent autonomy. |
| Relation / health layer | Track typed relations, evidence, graph health, contradictions, orphaned nodes. | Replacing human review. |
| Retrieval layer | Recall likely relevant records and source windows. | Verification or final裁决. |
| Context pack / API layer | Package relevant evidence, warnings, gaps, and actionability for humans or agents. | Inventing unrecorded truths. |
| Agent access layer | Control read-only, suggest-only, reviewed-write, owner-final boundaries. | Unlimited write access. |
| Decision / action basis layer | Convert verified knowledge into risk-aware action guidance. | Acting without owner or workflow context. |
| Feedback timeline layer | Record outcomes and update confidence, gaps, and next_review. | Rewriting history silently. |
| Viewer / Obsidian workbench layer | Display, filter, review, and operate on structured records. | Defining schema or truth. |

## 5. Adoption gates for new ideas

Before any new repo, plugin, workflow, retrieval system, UI, API, or agent feature enters the architecture, answer these questions:

```text
1. Which layer does it belong to?
2. What real pain does it solve?
3. Does it improve verified knowledge, action basis, or extensibility?
4. Can it output or consume existing Markdown contracts?
5. Can it fail without damaging the truth layer?
6. Does it bypass review gates?
7. Does it confuse candidate retrieval with verified truth?
8. What is the smallest useful version?
9. What evidence would prove it is worth keeping?
10. What would make us remove or replace it?
```

Outcomes:

```text
core        = needed for the main flow and contract-stable
module      = useful behind an interface, replaceable
candidate   = promising but not yet proven
watch       = interesting, not needed now
reject      = conflicts with truth, review, or action basis
```

## 6. Anti-四不像 rules

The system becomes incoherent when it adopts features only because a good reference project has them.

Warning signs:

```text
The feature has no layer.
The feature cannot name the pain it solves.
The feature only makes demos look stronger.
The feature requires unreviewed background rewrite.
The feature hides provenance.
The feature makes search score look like truth.
The feature adds a new UI before the underlying contract is stable.
The feature needs a long explanation to justify why it belongs.
```

If two references conflict, resolve by this order:

```text
1. source evidence
2. SCHEMA.md
3. active decision records
4. architecture principles
5. implementation blueprint
6. tool convenience
```

Tool convenience loses to verified truth.

## 7. Agent operating principles

Agents are useful because they can read, summarize, propose, and check. They are dangerous when they silently rewrite truth.

Default access tiers:

| Tier | Allowed | Not allowed |
|---|---|---|
| read-only | Read raw, wiki, index, decisions, context packs. | Modify formal nodes. |
| suggest-only | Create candidates, lint reports, QA outputs. | Approve own candidates. |
| reviewed-write | Write formal nodes after explicit review process. | Override conflicts silently. |
| owner-final | Make final adoption, rejection, and action decisions. | Skip evidence requirements. |

Misa/gbrain/external agents should start as read-only or suggest-only.

Codex can prepare candidates and implementation files, but formal architecture changes should still be visible in Markdown and index files.

### 7.1 Codex-mediated intake

The default intake model is:

```text
automatic capture -> raw/inbox only
external agents   -> read-only or suggest-only
Codex             -> reviewed write
user              -> final authority
```

There are two intake modes:

```text
inbox      = capture now, process later
immediate  = user names the source and asks Codex to process it now
```

Both modes preserve the raw source first. The difference is timing, not trust.

Daily brief and weekly synthesis belong to the feedback/review layer. They may produce connections, classification suggestions, summary candidates, claim candidates, contradiction warnings, and action candidates. They may not directly create verified claims or decisions.

## 8. Obsidian operating principles

Obsidian is the IDE, not the database authority.

Good uses:

```text
navigation
review workbench
Bases views
metadata filtering
manual inspection
graph exploration
```

Bad uses:

```text
letting a Base view define schema
using backlinks as the only relation evidence
mixing product drafts into truth nodes
hiding unverified notes inside polished dashboards
```

## 9. Context pack principles

Context packs are the main bridge between the vault and agents.

A good context pack should include:

```text
question or task
primary verified nodes
source evidence
relation rationale
negative evidence
confidence and verification_status
gaps
warnings
recommended next action where relevant
budget and truncation notes
```

A context pack should not include:

```text
uncited certainty
retrieval-only claims as truth
hidden raw dumps beyond budget
agent instructions that bypass review
```

## 10. Health and lint principles

Automation should first make problems visible.

Useful checks:

```text
missing required fields
broken wiki links
missing sources
malformed relations
low confidence decisions
claims without evidence
patterns without failure conditions
decisions without rollback
context packs without warnings or gaps
candidate backlog
stale next_review dates
conflicted nodes still used as active action basis
```

In v0.1, lint reports problems. It does not rewrite the vault in the background.

## 11. Progressive context loading

Future agents should not read the entire vault blindly.

Default loading order:

```text
1. purpose.md
2. ARCHITECTURE_PRINCIPLES.md
3. SCHEMA.md
4. wiki/indexes/knowledge-graph-index.md
5. relevant decision records
6. relevant source / summary / claim / pattern / anti-pattern nodes
7. raw source windows only when needed
```

This keeps answers grounded while avoiding full-vault noise.

## 12. Never create in isolation

New important files should connect back to the graph.

When creating a node, also consider whether to update:

```text
wiki/indexes/knowledge-graph-index.md
related decision records
related pattern or anti-pattern
outputs/review/README.md if it changes review flow
handoff if it changes recovery path
```

If a new node has no source, no relation, and no reason to exist, it should probably be an `outputs/qa/` note or a review candidate, not a core node.

## 13. Two-output rule

When an answer changes the knowledge system, produce two outputs:

```text
1. answer to the user
2. durable writeback to the vault
```

The writeback can be a source record, claim, pattern, anti-pattern, decision, QA note, implementation note, lint report, or handoff update.

Chat-only conclusions are not enough for durable architecture decisions.

## 14. Phase order

The system should grow in this order:

```text
1. Markdown contracts
2. review queue
3. lint rules
4. implementation blueprint
5. compiler scripts
6. context pack contract
7. retrieval adapters
8. API / MCP
9. viewer / Obsidian workbench
10. feedback automation
```

This order is not about being small. It is about making sure runtime power has a stable truth layer underneath it.

## 15. Current v0.1 conclusion

The architecture is a fusion design with one main spine:

```text
Karpathy gives the operating loop.
llm-wiki-compiler gives implementation mechanics.
OpenKB gives long-document ingest and generator/skill surfaces.
gbrain gives epistemic discipline.
obsidian-second-brain gives agentic vault hygiene.
Obsidian Bases gives the workbench.
retrieval tools give candidate recall.
Misa-style relations give graph semantics.

Verified Action Knowledge System gives the裁决权.
```

The system is allowed to become large, but only by adding replaceable modules behind stable contracts.

The core must stay simple enough to inspect, strict enough to trust, and expressive enough to support action.
