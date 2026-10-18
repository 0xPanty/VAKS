---
type: source
status: source-captured
title: "Effective Context Engineering for AI Agents"
source_id: anthropic-effective-context-engineering-agents-2025
source_uri: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
source_url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
source_type: article
platform: web
author: "Anthropic"
publisher: Anthropic
published_at:
updated_at:
captured_at: 2026-06-06
captured_by: Codex
raw_location: raw/articles/2026-06-06-anthropic-effective-context-engineering-agents-source.md
processing_mode: public-web-read
processing_level: medium
review_priority: normal
review_owner: Codex
formalization_status: raw-only
source_status: active
confidence_cap_reason: "Public article summary/extraction only; no full local article copy preserved."
topics:
  - context-engineering
  - ai-agents
  - context-pack
  - just-in-time-loading
  - compaction
  - progressive-disclosure
  - agent-workbench
  - retrieval
  - activation
projects:
  - verified-action-knowledge-system
candidate_relation_suggestions:
  - candidate:identifier_first_payload_later
  - candidate:just_in_time_context_loading
  - candidate:progressive_disclosure_context_packs
  - candidate:agent_context_compaction
  - candidate:agent_notes_as_runtime_trace_not_truth
tags:
  - raw-article
  - anthropic
  - context-engineering
  - retrieval
  - agent
  - candidate-only
---

# Source Record: Anthropic Effective Context Engineering for AI Agents

## Why Saved

This Anthropic engineering article is relevant to VAKS because Pro's retrieval
research suggested an `identifier-first, payload-later` direction for Markdown
vault retrieval and context-pack design.

The article is not only about search quality. It is about managing limited agent
context so that an agent can decide what to load now, what to reference, what to
compact, and what to keep as external state.

## Source Boundary

```text
Article = external source provenance.
This card = raw/source record.
Extraction note = candidate comprehension.
Candidate points = review input only.
No reviewed VAKS knowledge is created by this record.
```

## What Was Observed

The article frames context engineering as a central part of building effective
AI agents. It emphasizes that context windows are limited and that effective
agents should not blindly stuff all available information into the prompt.

Relevant ideas observed:

```text
keep context lean and task-relevant
use lightweight references / identifiers before loading full payloads
load details just in time
use progressive disclosure
compact or summarize long context when needed
externalize durable notes/state outside the immediate context window
design tools so they return useful, compact, relevant context
```

## VAKS Candidate Signals

Potential candidate knowledge points:

```text
identifier_first_payload_later:
  Use paths, titles, headings, selectors, and item IDs as the context-pack
  skeleton; open payload only when needed.

just_in_time_context_loading:
  Pack should support drilldown rather than dumping all raw snippets upfront.

progressive_disclosure_context_packs:
  Context pack should expose summary/identifier first, then evidence detail
  only when the task requires it.

agent_context_compaction:
  Long-running agent work should compact context and preserve trace/state,
  without treating the compacted memory as reviewed truth.

agent_notes_as_runtime_trace_not_truth:
  Agent notes, summaries, and context memory help operation and retrieval but
  are not reviewed knowledge.
```

## Not Adopted Yet

Do not treat this article as:

```text
permission to replace evidence anchors with summaries
permission to let agent notes become reviewed knowledge
proof that any specific Anthropic runtime pattern must be adopted
action basis for implementing a full agent workbench
```

## Related Candidate Extraction

```text
outputs/review/2026-06-06-vaks-retrieval-external-source-extractions.md
outputs/review/2026-06-06-anthropic-effective-context-engineering-agents-candidate-distillation.md
outputs/review/2026-06-06-vaks-retrieval-candidate-knowledge-index.md
```

