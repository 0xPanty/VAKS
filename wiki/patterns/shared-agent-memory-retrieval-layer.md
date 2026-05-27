---
type: pattern
status: draft
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - willynikes2/knowledge-base-server
related_concepts:
  - "[[MEMORY_TIER]]"
  - "[[AGENT_ACCESS]]"
  - "[[FEEDBACK]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adapt
verification_status: single-source
evidence_level: secondary
evidence_count: 1
confidence: medium
negative_evidence:
  - "Shared retrieval is useful only when agent write permissions are constrained."
extension_points:
  - MCP
  - API
  - retrieval-layer
  - agent-access
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "Needs AGENT_ACCESS.md before implementation."
evidence_timeline:
  - date: 2026-05-27
    source: "[[2026-05-27-knowledge-base-server-source]]"
    observation: "The repo exposes the same knowledge base through MCP/REST for multiple agents."
    effect: supports
    confidence: medium
relations:
  - target: "[[AGENT_ACCESS]]"
    type: supports
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-05-27-knowledge-base-server-source]]"
    rationale: "A shared memory layer needs explicit tool permissions and write boundaries."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - agent-access
  - shared-memory
  - mcp
---

# Shared Agent Memory Retrieval Layer

## AI-readable preamble

Multiple agents can share one retrieval layer, but they must not share unrestricted write authority.

This pattern belongs to API/MCP/retrieval access. It does not replace the verified vault schema.

## One-line definition

Expose the same derived retrieval layer to many agents while keeping writeback governed.

## Problem solved

Without shared memory:

```text
each agent starts cold
fixes discovered by one agent do not help another
project preferences get repeated
session history disappears
```

With shared retrieval:

```text
agents can search the same operational memory
past fixes become reusable
context compounds across tools
```

## Source evidence

`willynikes2/knowledge-base-server` presents itself as one brain for Claude, Codex, Gemini, ChatGPT, and MCP clients.

Relevant implementation surfaces:

```text
src/mcp.js:
  local MCP stdio server

src/mcp-http.js:
  HTTP MCP transport for remote clients

src/routes/v1.js:
  REST routes for search, context, read, ingest, and capture

src/tools.js:
  shared tool registry
```

## Applicable scenarios

- Future MCP interface for this vault.
- Multiple agents reading the same verified knowledge graph.
- Shared feedback/query-run history.
- Retrieval across local Codex, Misa/Hermes, and other callers.

## Not applicable

- Giving all agents direct writes to formal wiki.
- Letting MCP results bypass review.
- Letting one agent's unreviewed synthesis become global truth.

## Minimum implementation

Separate tools by authority:

```text
read/search/context:
  broad access

capture raw / feedback event:
  allowed with source and scope metadata

candidate write:
  allowed into review queue only

verified node write:
  gated by review

decision/action update:
  gated by explicit owner approval or defined policy
```

## Fusion suggestion

Use this pattern later when creating `AGENT_ACCESS.md`.

The useful split:

```text
all agents can ask the library
few paths can write candidates
no agent directly rewrites verified truth without review
```

## Boundary

Shared memory should increase recall, not authority.
