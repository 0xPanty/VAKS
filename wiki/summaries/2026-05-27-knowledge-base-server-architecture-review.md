---
type: summary
status: summary-draft
created: 2026-05-27
updated: 2026-05-27
sources:
  - "[[2026-05-27-knowledge-base-server-source]]"
topics:
  - ai-memory
  - MCP
  - SQLite
  - FTS5
  - Obsidian
  - memory-tier
  - retrieval-layer
verification_status: single-source
evidence_level: secondary
confidence: medium
last_verified: 2026-05-27
next_review: 2026-06-03
relations:
  - target: "[[MEMORY_TIER]]"
    type: supports
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-knowledge-base-server-source]]"
    rationale: "The repo explicitly implements hot/warm/cold memory and uses retrieval tiers to reduce context pollution."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[DEV_CONTEXT]]"
    type: refines
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-knowledge-base-server-source]]"
    rationale: "The kb_context workflow suggests a context briefing step before selecting full documents for a dev context pack."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[auto-promotion-without-review-gate]]"
    type: risk_of
    strength: 5
    confidence: medium
    evidence:
      - "[[2026-05-27-knowledge-base-server-source]]"
    rationale: "The repo has auto classification and promotion surfaces that could bypass verified-action review if copied directly."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - summary
  - ai-memory
  - knowledge-base-server
  - memory-tier
  - retrieval
---

# knowledge-base-server Architecture Review

## AI-readable preamble

This review treats `willynikes2/knowledge-base-server` as an AI memory runtime reference.

Its strongest value for this project is not the exact codebase. It is the runtime pattern:

```text
Obsidian as human source of truth
SQLite/FTS/embeddings as derived AI retrieval layer
MCP/REST as agent access layer
context briefing before full reads
operational capture as compounding memory
```

It should not replace the verified-action truth layer, review queue, evidence model, or decision authority.

## What it solves

The repo solves a very practical agent problem:

```text
agents forget between sessions
agents waste tokens rereading whole documents
multiple agents do not share operational history
old terminal/session/fix knowledge gets lost
raw captures pollute search results if treated the same as refined decisions
```

Its answer is a server that sits between a vault and AI agents.

## Core design

The system has four major layers:

```text
human knowledge layer:
  Obsidian vault

machine retrieval layer:
  SQLite documents, FTS5 index, vault_files metadata, embeddings

agent access layer:
  MCP tools, REST API, CLI

learning loop:
  capture -> classify -> synthesize -> promote -> retrieve -> improve
```

The repo's README and `EXTENDING.md` both emphasize a three-tier memory model:

```text
Hot:
  active context, recent sessions, current decisions

Warm:
  classified/summarized/tagged accumulated knowledge

Cold:
  raw captures, inbox, clippings, old logs
```

This directly supports our memory-tier branch.

## Source / code extraction

Key implementation surfaces:

```text
src/db.js:
  documents table
  documents_fts FTS5 virtual table
  vault_files metadata/index table
  embeddings table
  FTS search with stop words, AND-first search, OR fallback, BM25 ranking

src/vault/indexer.js:
  recursive markdown scanner
  sha256 content hash
  skip unchanged files
  update documents and vault_files
  delete stale index entries

src/vault/parser.js:
  folder prefix to note type mapping
  frontmatter extraction
  project/status/source/confidence parsing

src/tools.js:
  MCP tools for search, context, read, write, classify, capture, promote, synthesize, safety check

src/classify/classifier.js:
  Claude CLI classification into type, tags, project, summary, confidence, key_topics

src/classify/summarizer.js:
  summaries optimized for deciding whether an agent needs the full note

src/promotion/promoter.js:
  raw source/inbox note to structured note generation

src/safety/review.js:
  KB-aware destructive action review
```

Detailed source anchors are preserved in:

```text
[[2026-05-27-knowledge-base-server-source]]
```

Most important anchors for复盘:

```text
src/db.js:41:
  FTS5 search table.

src/db.js:65:
  vault_files metadata cache.

src/tools.js:351:
  kb_context briefing before full read.

src/tools.js:421:
  HTTP tool filtering.

src/mcp-http.js:29:
  HTTP MCP session TTL.

skill/SKILL.md:
  retrieval habit and capture-after-work instructions.

CODEMAP.md:
  structural repo briefing before raw code reads.
```

## What is worth extracting

### 1. Token-efficient context briefing

`kb_context` is the clearest alpha for our current branch.

The pattern:

```text
do not read everything first
return summary + metadata + source pointers first
then full-read only the documents that matter
```

This fits perfectly between:

```text
memory-tier activation
dev context pack construction
context pack budget guardrails
```

Plain language:

```text
Before putting books on the desk, read the table of contents.
```

### 2. Derived machine retrieval layer

The repo keeps Obsidian as human source of truth and SQLite as retrieval layer.

This validates our boundary:

```text
Markdown/YAML owns durable truth records.
SQLite/FTS/vector/search owns fast recall.
```

The derived layer can be rebuilt. It should not own verification status.

### 3. Operational capture loop

`kb_capture_session` and `kb_capture_fix` are strong operational memory primitives.

They show how a system can capture:

```text
what was attempted
what failed
what worked
root cause
fix
lesson
```

For our architecture, these should feed:

```text
feedback-event
query-run
warm pattern candidates
risk / anti-pattern candidates
decision review inputs
```

### 4. Shared multi-agent memory

The repo assumes Claude, Codex, Gemini, and other agents can use the same retrieval layer.

This supports our larger architecture direction:

```text
one verified vault
many agent access paths
strict write boundaries
shared retrieval context
```

### 5. Incremental vault indexing

The hash-based vault indexer is practical and directly useful later.

It supports:

```text
source-hash registry
idempotent ingest
SQLite rebuildable cache
fast context discovery
```

### 6. Skill plus tool split

The repo ships both MCP tools and a `skill/SKILL.md`.

The useful distinction:

```text
MCP tools:
  engine that can search, read, write, capture, classify, and synthesize.

Skill / AGENTS contract:
  operating instructions that teach the agent when to search, when to read full docs, and when to capture findings.
```

Plain language:

```text
Tools give the agent hands.
The skill gives the agent working habits.
```

This is useful for our future `AGENT_ACCESS.md`.

The alpha is:

```text
Do not expose tools without a retrieval/writeback operating contract.
```

### 7. Access surface separation

The repo exposes the same knowledge through:

```text
local stdio MCP
remote HTTP MCP
REST API
OpenAPI spec for Custom GPT / external agents
llms.txt for agent-readable orientation
CLI setup and registration
```

This supports a future split in our system:

```text
human vault:
  Markdown / Obsidian

local agent access:
  read/search/context tools

remote agent access:
  filtered tools, auth, session TTL, no admin writes

external integration:
  OpenAPI/llms surface
```

Do not implement all of this now. Keep it as an API/MCP later-stage reference.

### 8. Session isolation and admin-tool filtering

`src/mcp-http.js` creates a fresh MCP server per HTTP session and expires idle sessions.

`src/tools.js` also distinguishes admin-only tools from HTTP-safe tools.

This validates a boundary we will need later:

```text
remote access should not equal local/admin access
```

For our architecture, this should map to:

```text
read/search/context:
  broadly available

raw capture:
  allowed with provenance

candidate write:
  review queue only

verified write / schema change / destructive action:
  local/admin/owner gated
```

### 9. Code map as briefing, not raw code dumping

The repo's `CODEMAP.md` and `skill/SKILL.md` imply a practical codebase rule:

```text
For code repos, start with a structural map before indexing or reading everything.
```

This fits our context briefing direction:

```text
code map first
targeted file reads second
session/fix capture after work
```

This is relevant to future source adapters, not the current memory-tier first draft.

## What not to absorb directly

The dangerous part is automatic elevation.

Do not adopt:

```text
auto-classification as verified type
classifier confidence as evidence confidence
auto-promotion into verified notes
agent direct writes into formal wiki
synthesis as reviewed conclusion
search rank as trust
```

Why:

```text
The repo is optimized for useful AI memory.
Our system is optimized for verified knowledge and action basis.
```

Useful memory can be wrong. Verified action needs review.

## Fit with main architecture

Strong fit:

```text
retrieval/cache layer
MCP/API access reference
context briefing reference
capture-session/fix intake reference
incremental index reference
multi-agent shared memory reference
safety-check reference
```

Weak fit:

```text
truth schema
review promotion authority
decision readiness
evidence/confidence contract
verified relations
```

## Fit with memory-tier branch

Very strong fit:

```text
hot/warm/cold retrieval priority
context briefing before full load
shared agent context
session/fix capture for cooling/reheating
cold raw captures preserved but not default-loaded
```

New alpha candidates:

```text
1. Context briefing before dev context pack.
2. SQLite/FTS as a rebuildable activation cache.
3. Session/fix capture as closeout writeback.
4. Hot/warm/cold should affect retrieval expansion depth, not truth.
```

## Collision with PARA and Kepano

PARA says:

```text
Ask where this will be needed next.
```

Kepano says:

```text
Do not move files just to make them visible. Use properties, links, and views.
```

knowledge-base-server says:

```text
Give agents a low-token briefing first, then read selected files through a shared retrieval layer.
```

Fusion:

```text
PARA chooses why something should activate.
Kepano shows how to surface it without moving it.
knowledge-base-server shows how agents can retrieve it efficiently at runtime.
verified-action schema decides whether it can be trusted or used for action.
```

## Second-pass status

This repo is mostly mined for design-level value.

Strongly extracted:

```text
context briefing before full read
derived SQL/FTS/vector retrieval cache
session/fix capture loop
shared multi-agent retrieval
auto-promotion risk boundary
```

Watch for later:

```text
MCP session isolation
admin-only tool filtering
OpenAPI / llms.txt external agent surface
CLI setup wizard
skill plus MCP operating contract
code map as codebase briefing
```

Not worth copying now:

```text
full server stack
OAuth / remote deployment
dashboard
complete auto-classify/promote loop
production service install scripts
```

## Direct judgment

This repo should not be forked as the main architecture.

It should be mined as a runtime reference for:

```text
context briefing
derived retrieval cache
MCP tool surface
session/fix capture
incremental indexing
shared agent memory
```

The promotion/classification pieces should be adapted only behind our review gate.
