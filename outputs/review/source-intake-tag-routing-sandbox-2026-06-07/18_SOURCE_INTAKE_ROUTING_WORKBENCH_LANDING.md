---
type: sandbox_design_note
status: candidate_only
created_at: 2026-06-07
scope: source-intake-routing workbench implementation landing
truth_boundary: sandbox implementation note only; not reviewed knowledge; not action basis
---

# Source Intake Routing Workbench Landing

## Plain Result

The GitHub scout is now wired into the sandbox workbench instead of staying as a
separate research note.

It landed as:

```text
route map
Obsidian workbench entrypoint
context pack builder route sections
pinned external scout refs
high-pressure generated packs
context pack lint checks
```

## Borrowing Map

| Borrowed from | Landed as | Explicit non-borrow |
|---|---|---|
| Dify | source route front door and metadata/workbench visibility | no Dify platform clone |
| RAGFlow | ingestion/parser/chunk route as source hygiene | no heavy ingestion platform |
| AnythingLLM | Obsidian/GitHub/website connector UX and citation display | no workspace agent/memory adoption |
| LlamaIndex | reader/parser/router/citation stage boundaries | no framework dependency |
| Haystack | metadata filtering, routing, tracing language | no pipeline runtime or document-store stack |

## Implementation Choices

```text
Use a small JSON route map as the structured workbench source.
Keep generated packs Markdown-first for Obsidian.
Pin current-rule refs and external scout refs so path sorting cannot hide them.
Keep action mode strict: candidate/overlay/support-review output can match but
does not become selected action support.
Expose route cards and excluded/not-default hits in the pack.
```

## What This Improves

Before:

```text
Search phrase -> mixed results -> manual inspection.
```

After:

```text
Question -> route map -> mode -> lane-filtered pack -> explicit exclusions.
```

## Smallness Guard

This is deliberately not:

```text
vector database
RAG platform
Obsidian plugin
MCP server
automatic answer generator
automatic promotion workflow
new truth layer
```

## Test Handles

```text
checks/source-intake-routing-workbench-pack-research-generated.md
checks/source-intake-routing-workbench-pack-source-inspection-generated.md
checks/source-intake-routing-workbench-pack-action-generated.md
checks/source-intake-routing-workbench-high-pressure-test.md
```

## Review Question For GPT Pro

```text
Does this workbench make source-intake-routing more usable without allowing
metadata, citation UI, candidate notes, overlays, audits, or platform examples
to act as authority?
```
