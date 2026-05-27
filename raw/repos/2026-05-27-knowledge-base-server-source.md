---
type: source
status: source-captured
title: "willynikes2/knowledge-base-server source review"
source_url: "https://github.com/willynikes2/knowledge-base-server"
source_type: repo
captured_at: 2026-05-27
captured_by: Codex
raw_location: "temporary clone: %TEMP%/codex-kb-server-6fb862fffed241a7aac7ffd357810845"
processing_mode: immediate
review_priority: high
review_owner: Codex
formalization_status: candidate-generated
topics:
  - ai-memory
  - knowledge-base-server
  - MCP
  - Obsidian
  - SQLite
  - FTS5
  - memory-tier
  - retrieval-layer
projects:
  - verified-action-knowledge-system
source_family: ai-knowledge-runtime
verification_status: single-source
relations:
  - target: "[[2026-05-27-knowledge-base-server-architecture-review]]"
    type: derived_from
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-knowledge-base-server-source]]"
    rationale: "This source record anchors the architecture review and extracted memory-tier patterns."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - source
  - repo
  - ai-memory
  - mcp
  - retrieval
  - memory-tier
---

# Source Record: willynikes2/knowledge-base-server

## Why captured

User asked to inspect `willynikes2/knowledge-base-server` with the same source-level rigor as the PARA and Kepano reviews: understand its design logic, preserve source/code anchors, extract what can strengthen the whole architecture, and compare it against the current memory-tier / dev-context branch.

## Source information

- Publisher: GitHub
- Repo URL: https://github.com/willynikes2/knowledge-base-server
- Capture method: GitHub page + `git clone --depth 1`
- Checked commit: `6bdc476bd81c2ab75d227b8450d94c8973eb1a8d`
- Commit message: `fix: deduplicate 'web' tag in kb_capture_web`
- Local clone used for review: `%TEMP%/codex-kb-server-6fb862fffed241a7aac7ffd357810845`

## Repo character

This repo is a real AI knowledge runtime, not just an Obsidian template.

It provides:

```text
Node.js server
SQLite + FTS5 database
MCP stdio and HTTP transports
REST API
Obsidian vault sync
classification and summarization pipeline
capture tools
promotion tools
synthesis tools
safety review
local embeddings
web dashboard
CLI
```

## Source / code map

Important top-level files:

```text
README.md
EXTENDING.md
CODEMAP.md
openapi.json
llms.txt
package.json
bin/
docs/
src/
tests/
```

Important source modules:

```text
src/db.js:
  SQLite schema, documents table, FTS5 table, vault_files tracking table, embeddings table, search functions.

src/tools.js:
  MCP tool registry for search, context, read, write, ingest, classify, capture, promote, synthesize, safety check.

src/vault/parser.js:
  Maps vault folder prefixes into note types and extracts frontmatter fields.

src/vault/indexer.js:
  Scans Obsidian vault files, hashes content, skips unchanged files, indexes into SQLite, reconciles deleted files.

src/classify/classifier.js:
  Calls Claude CLI to classify notes into type, tags, project, summary, confidence, and key topics.

src/classify/summarizer.js:
  Generates short retrieval summaries and writes them back into frontmatter.

src/promotion/promoter.js:
  Promotes raw inbox/source notes into structured destinations using LLM prompts.

src/synthesis/weekly-review.js:
  Reads recent vault notes and generates weekly synthesis prompts/notes.

src/safety/review.js:
  Searches KB for past incidents and asks a model to review destructive actions.

src/capture/terminal.js:
  Captures sessions and fixes as durable notes.

src/capture/web.js:
  Captures web articles with metadata and deduplication.
```

## Important implemented ideas

The README describes the repo as a persistent memory system for multiple AI agents. It claims Obsidian is the human source of truth and the KB server is the optimized retrieval layer.

The core loop:

```text
capture
classify
synthesize
promote
retrieve
improve
```

The memory tiers:

```text
Hot:
  active project context, recent sessions, current decisions

Warm:
  accumulated lessons, research, validated workflows, summarized/tagged vault files

Cold:
  raw captures, archived sources, old logs, unprocessed inbox/clippings
```

The retrieval workflow:

```text
kb_context:
  returns summaries and metadata first

kb_search:
  keyword search through SQLite FTS5

kb_search_smart:
  hybrid keyword plus semantic search

kb_read:
  reads full content only after context/search identifies the useful documents
```

The source-of-truth split:

```text
Obsidian vault:
  human-facing source of truth

SQLite database:
  AI retrieval/cache layer
```

## Code evidence

Concrete implementation evidence:

```text
src/db.js:
  creates documents, documents_fts, vault_files, and embeddings tables.
  vault_files stores note_type, project, status, source, confidence, summary, key_topics.
  searchDocuments uses FTS5, stop-word filtering, AND-first query, OR fallback, BM25 ranking.

src/vault/indexer.js:
  scanVault walks markdown files.
  hashContent skips unchanged files.
  upsertVaultFile stores parsed metadata into SQLite.
  missing vault paths are deleted from the retrieval cache.

src/vault/parser.js:
  maps inbox/sources/projects/research/ideas/workflows/decisions/runbooks/builds/archive folders into note types.

src/tools.js:
  kb_context explicitly says to return summaries/metadata before full reads.
  kb_write writes new notes to the Obsidian vault.
  kb_capture_session and kb_capture_fix record operational learning.
  kb_promote is exposed as an admin tool, but the MCP handler itself mostly instructs the agent to read and use kb_write.

src/promotion/promoter.js:
  promoteNote can generate promoted notes from inbox/source notes and write files into destination folders.

src/classify/classifier.js:
  classification prompt returns type, tags, project, summary, confidence, key_topics.

src/safety/review.js:
  safety review searches the KB for past incidents before giving a destructive-action verdict.
```

## Source anchor matrix

Use this table for later复盘. It maps concrete source files and line anchors from the checked clone to the design point we extracted.

Checked clone:

```text
%TEMP%/codex-kb-server-6fb862fffed241a7aac7ffd357810845
commit: 6bdc476bd81c2ab75d227b8450d94c8973eb1a8d
```

| Source anchor | What exists in source | Design extraction | Our boundary |
|---|---|---|---|
| `README.md` | Describes Obsidian as source of truth and KB server as optimized retrieval layer | Human source + machine retrieval split | Do not let SQLite own truth |
| `EXTENDING.md` | Defines Hot/Warm/Cold and `kb_context` first workflow | Memory tier and context briefing | Tier controls activation, not confidence |
| `src/db.js:28` | `documents` table | Machine content index | Derived cache only |
| `src/db.js:41` | `documents_fts` FTS5 virtual table | Full-text retrieval layer | Search rank is not trust |
| `src/db.js:65` | `vault_files` table with path/hash/type/project/status/source/confidence/summary/key_topics | Metadata index for vault files | `confidence` here is classifier metadata, not verified confidence |
| `src/db.js:99` | `embeddings` table | Semantic retrieval layer | Vector similarity only recalls candidates |
| `src/db.js:181` and `src/db.js:200` | FTS snippets and BM25 ranking | Search/result ranking | Rank cannot promote truth |
| `src/db.js:291` | `upsertVaultFile` stores summary and key topics | Rebuildable vault metadata cache | Markdown/YAML remains authoritative |
| `src/vault/indexer.js:41` | `hashContent` | Idempotent/incremental indexing | Useful for source hash registry |
| `src/vault/indexer.js:45` | `indexVault` concurrency guard | Safe index job boundary | Runtime implementation reference only |
| `src/vault/indexer.js:66` | Embeddings lazy-load only when requested | Optional semantic layer | Do not make vector mandatory in v0.1 |
| `src/vault/parser.js` | Folder prefix to note type mapping | Folder can suggest type | Folder does not decide truth |
| `src/tools.js:16` | `ADMIN_ONLY_TOOLS` includes classify/promote/synthesize/safety/capture_youtube | Tool access tiering | Remote access must be narrower |
| `src/tools.js:99` | `kb_write` writes notes to vault | Agent write surface | In our system, writes need raw/candidate/review boundary |
| `src/tools.js:226` | `kb_capture_session` | Operational session capture | Creates candidates/feedback, not truth |
| `src/tools.js:252` | `kb_capture_fix` | Bug fix memory capture | Candidate for warm/risk after review |
| `src/tools.js:296` | `kb_promote` | Promotion tool surface | Must be review-gated in our system |
| `src/tools.js:351` | `kb_context` says summaries/metadata before full reads | Token-efficient context briefing | Briefing is loading plan, not evidence |
| `src/tools.js:421` | `getHttpToolDefinitions` filters admin tools | HTTP-safe tool surface | Supports AGENT_ACCESS tiering |
| `src/mcp-http.js:8` | Fresh MCP server per HTTP session | Session isolation | Useful future MCP reference |
| `src/mcp-http.js:24` | session store | Remote session lifecycle | Keep as later-stage implementation detail |
| `src/mcp-http.js:29` | `SESSION_TTL = 1 hour` | Expiring remote agent sessions | Remote context should not be permanent hot memory |
| `src/safety/review.js` | Searches KB history before destructive action review | Risk lookup before action | Strengthens Risk checkpoint |
| `skill/SKILL.md` | Teaches context-before-read and capture-after-work | Skill plus tool operating contract | Tools need usage policy |
| `docs/SKILL-VS-MCP.md` | Separates MCP engine from skill instructions | Tools are engine; skill is habit | Future AGENT_ACCESS / agent instruction layer |
| `docs/workflow/AGENTS.md.template` | Agent contract: search first, capture findings, avoid destructive actions | Shared agent operating rules | Must adapt to verified-action boundaries |
| `CODEMAP.md` | Generated structural map of repo | Code map as briefing | For code repos, map first then selective reads |
| `openapi.json` | External REST/OpenAPI surface | External agent integration surface | Must expose narrower permissions than local admin |
| `llms.txt` | Agent-readable orientation and tool list | Lightweight agent onboarding | Useful later for external docs/API |

## Implementation-level cautions

The source has several useful implementation surfaces, but they should not be copied directly into the verified layer:

```text
src/classify/classifier.js:
  LLM classification returns type/tags/project/summary/confidence.
  In our system, this can only create candidate metadata.

src/classify/summarizer.js:
  writes summaries and key_topics back to frontmatter.
  In our system, summaries can support briefing but not replace source ranges.

src/promotion/promoter.js:
  writes promoted notes into destination folders.
  In our system, promotion must go through review queue before formal wiki.

src/synthesis/weekly-review.js:
  creates synthesis notes from recent notes.
  In our system, synthesis is review material, not verified conclusion.
```

## Candidate points

- Token-efficient context briefing before full document reads.
- SQLite/FTS/embedding database as a derived machine retrieval layer, not the human truth layer.
- Incremental vault indexing with content hashes and deleted-file reconciliation.
- Shared retrieval layer for multiple agents.
- Capture session/fix logs as operational learning, not just documentation.
- Synthesis as a periodic compaction loop.
- Safety review that checks past incidents before destructive actions.
- Hot/warm/cold as a retrieval-priority model.

## Direct value for MEMORY_TIER / DEV_CONTEXT

Can absorb:

```text
Brief first, read second:
  use low-token summaries/metadata to choose what to fully load.

Derived retrieval cache:
  SQLite/FTS/vector indexes can accelerate recall without owning truth.

Operational capture:
  session/fix logs can feed feedback, warm patterns, and risk records.

Shared agent memory:
  multiple agents should query the same retrieval layer and write through governed channels.

Tier-aware retrieval:
  hot/warm/cold should influence retrieval ordering and expansion depth.
```

Cannot absorb as core without modification:

```text
automatic classification as truth
automatic promotion into verified nodes
agent direct write into formal wiki
confidence from classifier as evidence confidence
retrieval rank as verification
weekly synthesis as reviewed truth
```

## Main architecture fit

Good fit as:

```text
derived retrieval layer
MCP/API reference
context briefing reference
capture and feedback intake reference
incremental indexer reference
shared multi-agent retrieval reference
```

Poor fit as:

```text
truth layer
review gate replacement
verified schema replacement
automatic promotion authority
decision authority
```

## Next step

- Created architecture review: `wiki/summaries/2026-05-27-knowledge-base-server-architecture-review.md`
- Created patterns:
  - `wiki/patterns/token-efficient-context-briefing.md`
  - `wiki/patterns/shared-agent-memory-retrieval-layer.md`
  - `wiki/patterns/operational-session-capture-loop.md`
  - `wiki/patterns/incremental-vault-index-retrieval-cache.md`
- Created anti-pattern:
  - `wiki/anti-patterns/auto-promotion-without-review-gate.md`
- Updated `MEMORY_TIER.md`, `DEV_CONTEXT.md`, `templates/dev-context-pack.md`, `wiki/indexes/memory-tier-reference-index.md`, `wiki/indexes/knowledge-graph-index.md`, and handoff.
