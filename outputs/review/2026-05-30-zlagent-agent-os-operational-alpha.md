---
type: source-review
status: draft
created: 2026-05-30
project: verified-action-knowledge-system
source_name: Kkkirito-123/ZLAgent
source_url: https://github.com/Kkkirito-123/ZLAgent
checked_commit: 01c12946460126e11c4c940f8b6d6c0bd9261749
review_mode: read-only source/code review
fusion_decision: adapt
confidence: medium-high
tags:
  - zlagent
  - agent-os
  - tool-permission
  - background-review
  - memory-quarantine
  - mcp-safety
  - graphrag-cache
  - alpha-detail-mining
---

# ZLAgent Alpha Review: Agent OS Operational Guardrails

## One-Line Judgment

ZLAgent 的强项不是比我们的资料库更会判断真假，而是：

```text
It turns an LLM assistant into a controlled operating runtime:
tools have permissions, writes have origins, reviews run in a sandboxed fork,
memory/wiki/graph are separate sedimentation layers, and MCP tools can be installed/promoted with safety rails.
```

说人话：

```text
它很像一个个人 Agent OS。
它厉害在“让 agent 能干活但不乱干”。
我们厉害在“让知识能作为行动依据前先被证据审过”。
```

所以它对本项目的价值是补强未来 Misa / Codex / MCP 操作层，不是替换我们的 verified-action 主链。

## Source Identity

Primary repo:

```text
https://github.com/Kkkirito-123/ZLAgent
```

Checked commit:

```text
01c12946460126e11c4c940f8b6d6c0bd9261749
```

Local read-only sandbox clone:

```text
C:\Users\Administrator\Documents\资料库_alpha_lab_2026-05-30\repos\ZLAgent
```

Current remote check:

```text
origin/main == 01c12946460126e11c4c940f8b6d6c0bd9261749
```

## What This Repo Is

ZLAgent is a FastAPI-based personal assistant runtime:

```text
IM / API gateway
-> intent router
-> memory injection
-> skill routing
-> agent tool loop
-> safe / confirm / deny permission gate
-> post-turn memory / wiki / graph / review sedimentation
-> MCP runtime install / attach / promote
```

README anchors:

- Repo: https://github.com/Kkkirito-123/ZLAgent
- Architecture / layer diagram: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/README.md#L23-L89
- Directory and subsystem map: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/README.md#L115-L152
- Sedimentation layers: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/README.md#L165-L190
- Tool / MCP safety summary: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/README.md#L271-L288
- GraphRAG design summary: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/README.md#L314-L383

## Fit Against Our Architecture

Our fixed public story:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

Our fixed internal chain:

```text
source
-> candidate point
-> calibration / point collision
-> evidence-aware review
-> reviewed node / reviewed relation
-> context pack / action basis
-> action
-> use ledger / feedback / review_due
```

ZLAgent maps best to our outer operating layers:

```text
Capture:
  gateway / intent / source of user request

Understand:
  router / skill selection / memory snapshot / wiki fast path

Review:
  background review fork, but only as proposal pressure

Connect:
  GraphRAG snapshot / entity graph / wiki cache, but only as activation

Act and Learn:
  tool permissions / confirmation / use telemetry / memory feedback
```

It does not replace:

```text
Evidence Packet
Warrant separation
Challenge taxonomy
Evidence-aware review
Reviewed relation promotion
Context pack trace
Action basis sufficiency
```

## Core Design Observed In Code

### 1. Tool Permission Is Typed, Not Just "Allowed"

ZLAgent gives each tool:

```text
permission: safe | confirm | deny
is_read_only
is_concurrency_safe
is_destructive
is_action_read_only(arguments)
```

Source anchors:

- Local: `backend/tools/base.py:25-L94`
- GitHub: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/base.py#L25-L94
- Registry hides / drops tools by permission: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/registry.py#L17-L36
- Tool schema exposes read-only / concurrency / destructive metadata: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/registry.py#L188-L190
- Runner checks read-only action override: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/tool_loop/runner.py#L86-L95
- Runner batches only safe + read-only + concurrency-safe tools: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/tool_loop/runner.py#L129-L137
- Confirm-tier read-only sub-actions can bypass the confirm prompt: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/tool_loop/runner.py#L323-L388

Design extraction:

```text
Do not classify an agent capability only by tool name.
Classify by operation, arguments, side effect, concurrency safety, and destructiveness.
```

Plain value for us:

```text
Misa 可以查。
Codex 可以写候选 / review artifact。
谁能写 reviewed truth、谁能执行外部动作，要按 action gate 分。
```

Possible alpha:

```yaml
agent_operation_gate:
  operation: query_context_pack | write_candidate | mark_review_due | propose_patch | write_reviewed_node | external_action
  actor: misa | codex_local | human | scheduled_review
  permission: safe | confirm | forbidden
  read_only: true | false
  destructive: true | false
  allowed_outputs:
    - answer
    - candidate_point
    - feedback_event
    - review_due
```

Boundary:

```text
Permission does not create truth.
It only says whether an actor may perform an operation.
```

Adoption judgment:

```text
Strong adapt. This is the cleanest transplant.
Keep it as an agent-access / MCP boundary, not as a knowledge schema rewrite.
```

### 2. Tool Loop Guardrails Detect "No Progress"

ZLAgent detects repeated exact failures, same-tool repeated failures, and read-only no-progress loops.

Source anchors:

- Local: `backend/agent/tool_guardrails.py:1-L16`
- GitHub: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/tool_guardrails.py#L1-L16
- Threshold config: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/tool_guardrails.py#L45-L52
- Decision types allow / warn / block / halt: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/tool_guardrails.py#L82-L104
- Exact failure and no-progress blocks: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/tool_guardrails.py#L166-L200
- Runner applies guardrails before and after tool calls: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/tool_loop/runner.py#L370-L483

Design extraction:

```text
An agent should notice when it is repeating the same tool call without learning anything new.
```

Possible fit:

```text
For future Misa / Codex local tools:
same query + same result + no new reviewed evidence = stop repeating and surface blocker.
```

This helps our system avoid:

```text
endless retrieval loops
repeated context-pack rebuilds
same failing MCP call
same source search with no new evidence
```

Boundary:

```text
No-progress detection is operational hygiene.
It does not mean the underlying claim is false.
```

Adoption judgment:

```text
Adapt later when we have tool execution loops.
No need to add to core docs now unless agent/MCP runtime becomes active.
```

### 3. Background Review Fork Has A Narrow Tool Whitelist

ZLAgent schedules a review after certain turns. The review fork can only call restricted tools, and its write origin is marked as background review.

Source anchors:

- Post-turn pipeline schedules memory sync, wiki write, crystallization, review: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/post_turn/pipeline.py#L88-L158
- Review trigger conditions: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/post_turn/pipeline.py#L159-L186
- Review action filter: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/post_turn/pipeline.py#L191-L215
- Background write origin binding: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/post_turn/pipeline.py#L258-L322
- End-of-day review path: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/post_turn/pipeline.py#L324-L431
- Scheduling review task: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/post_turn/pipeline.py#L433-L460

Design extraction:

```text
Separate foreground response from background maintenance.
Let background review propose / tidy / remember, but do not let it act with full power.
```

Plain value for us:

```text
Misa 回答用户时不要顺手改资料库真相。
它最多把“这次查询可能暴露了一个缺口 / 纠错 / 过期点”丢进 feedback_event 或 review_due。
Codex 再本地复盘、写 candidate、跑 review。
```

Possible alpha:

```yaml
background_review_fork:
  trigger:
    - explicit_user_correction
    - action_failed
    - missing_evidence
    - stale_context_pack
    - repeated_low_quality_answer
  allowed_outputs:
    - feedback_event
    - review_due
    - candidate_point
    - candidate_relation_suggestion
    - maintenance_manifest
  forbidden_outputs:
    - reviewed_node
    - reviewed_relation
    - truth_confidence_change
    - action_execution
```

Boundary:

```text
Background review is not evidence-aware review.
It is review pressure.
```

Adoption judgment:

```text
Strong adapt. This fits our existing Agent memory quarantine and Feedback Ledger.
```

### 4. Write-Origin Provenance Is Tiny But Powerful

ZLAgent uses a ContextVar to distinguish foreground writes from background review writes.

Source anchors:

- Local: `backend/core/provenance.py:1-L60`
- GitHub: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/core/provenance.py#L1-L60
- `memory_manage` maps background review to `source=review`: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/builtins/memory_manage.py#L374-L385
- Skill history actor maps background review to `agent`: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/skills/history.py#L221-L231

Design extraction:

```text
Every write needs an origin label.
The same content means different things if it came from user confirmation, model review, import, API caller, or local maintainer.
```

Possible fit:

```yaml
write_origin:
  actor: human | codex_local | misa_api | background_review | import | script
  mode: foreground | background | scheduled | manual
  permission_gate: safe | confirm | forbidden
  target_layer: candidate | feedback | review_queue | reviewed_knowledge | action_log
```

Boundary:

```text
Origin is provenance, not support.
User-confirmed origin does not make a claim true.
Background-review origin should be lower-trust and candidate-only by default.
```

Adoption judgment:

```text
Strong adapt as a small field / convention.
This is a useful missing implementation-level detail for our future agent split.
```

### 5. Memory Is Layered And Quarantined

ZLAgent memory has L1 / L2 / L3 semantics:

```text
control_axiom = system-managed
agent_note = agent abstraction / review note
user_fact = user-specific durable fact
```

It also rejects performative writes like "已记住" and keeps source provenance.

Source anchors:

- Memory tool explanation and writable kinds: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/builtins/memory_manage.py#L82-L121
- Tool actions: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/builtins/memory_manage.py#L177-L242
- L1 control_axiom is blocked from tool writes: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/builtins/memory_manage.py#L301-L326
- Performative-write veto: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/builtins/memory_manage.py#L42-L72
- Source explicit vs review: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/memory/store.py#L56-L63
- Capacity and eviction policy: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/memory/store.py#L405-L448
- Consolidation respects explicit > review: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/memory/store.py#L456-L594
- Memory injection fence: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/memory/manager.py#L49-L74
- Frozen snapshot rationale: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/memory/manager.py#L119-L124
- Write scanner: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/memory/scanner.py#L1-L26
- Durable memory intent detector: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/memory/intent.py#L16-L27
- Correction signal is only a trigger, not a decision: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/correction.py#L14-L18

Design extraction:

```text
Agent memory should be useful, but it must not be the truth layer.
Memory writes need kind, source, scanner, cap, pin/archive, and consolidation rules.
```

Fit with our current architecture:

```text
We already have Agent memory quarantine.
ZLAgent gives implementation details:
  - write-origin field
  - performative-write veto
  - source-priority consolidation
  - pinned/explicit rows are protected
  - agent-written entries are easiest to archive
```

Boundary:

```text
Do not import ZLAgent's memory as reviewed knowledge.
For us, Misa memory can become:
  feedback_event
  candidate_point
  review_due
  context preference
but not reviewed truth.
```

Adoption judgment:

```text
Adapt details, not the memory model wholesale.
```

### 6. Wiki Cache And Atomic Facts Are Retrieval Acceleration, Not Truth

ZLAgent has a SQLite-backed answer cache, optional Redis hot layer, and a crystallizer that extracts atomic facts from answers.

Source anchors:

- Wiki model and v2 fields: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/db/models.py#L256-L389
- Wiki store two-phase lookup: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/wiki/store.py#L145-L165
- Exact / substring / alias fallback: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/wiki/store.py#L218-L312
- Hit bumps count, confirmation time, confidence: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/wiki/store.py#L358-L380
- Add with supersession and sources: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/wiki/store.py#L409-L563
- Low-confidence audit: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/wiki/store.py#L850-L889
- Crystallizer purpose: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/wiki/crystallizer.py#L1-L29
- Crystallizer clamps LLM confidence: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/wiki/crystallizer.py#L160-L177
- Atomic fact source points back to answer cache row: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/wiki/crystallizer.py#L356-L384
- Fast-path policy: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/retrieval/policy.py#L32-L92

Design extraction:

```text
Separate answer cache, document wiki, and graph.
Cache hits should speed up repeated answers, but should not become truth authority.
```

Our interpretation:

```text
This is useful only as "answer reuse / retrieval acceleration".
Its confidence numbers are operational cache confidence, not evidence confidence.
```

Possible alpha:

```yaml
answer_cache_entry:
  query_key:
  answer:
  sources:
  last_used_at:
  hit_count:
  superseded_by:
  review_due_when:
    - source_changed
    - negative_feedback
    - stale_context
```

Boundary:

```text
Cache hit != reviewed support.
LLM-extracted atomic fact != candidate point unless source/evidence anchor is preserved.
Cache confidence != truth confidence.
```

Adoption judgment:

```text
Watch / adapt narrowly.
We can use the supersession / low-confidence-audit shape, but not its cache confidence as knowledge confidence.
```

### 7. GraphRAG Extraction Is Async, Cached, And Fail-Soft

ZLAgent's graph layer consumes memory and knowledge mode records, extracts graph fragments in the background, and builds snapshots from cached results plus heuristics.

Source anchors:

- README: GraphRAG not on synchronous request path: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/README.md#L314-L316
- Graph source records: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/source.py#L14-L31
- Memory source record conversion: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/source.py#L34-L48
- Pending review placeholders: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/source.py#L83-L124
- Knowledge mode pages as graph source records: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/source.py#L181-L247
- Per-record cache key and fail-open reads: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/cache.py#L1-L21
- Cache key invalidates on content change: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/cache.py#L39-L43
- LLM extractor is never synchronous path and fail-soft: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/llm_extractor.py#L13-L23
- Strict schemas for paper / memory extraction: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/llm_extractor.py#L52-L88
- Tolerant JSON extraction and coercion: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/llm_extractor.py#L127-L227
- Extract and cache: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/llm_extractor.py#L286-L336
- Builder materializes cached extraction and falls back to heuristics: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/builder.py#L123-L176
- Builder attaches source_record_id and source_chunk_ids: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/builder.py#L251-L283
- Snapshot review metadata is heuristic / display-oriented: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/graph/builder.py#L340-L354
- Knowledge ingest preheats graph extraction without blocking: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/builtins/knowledge_ingest.py#L156-L221

Design extraction:

```text
Graph extraction should be background, cacheable, invalidated by source content change, and fail-soft.
The live answer path should not depend on fresh graph extraction.
```

Fit with our system:

```text
This reinforces our existing boundary:
graph / relation extraction = activation and review input
reviewed relation = only after evidence-aware review
```

Possible alpha:

```yaml
candidate_graph_fragment_cache:
  source_record_id:
  source_content_hash:
  extracted_at:
  extractor:
  nodes:
  edges:
  source_chunk_ids:
  state: activation_only | review_input
  invalidated_when:
    - source_hash_changed
    - schema_changed
    - extraction_error
```

Boundary:

```text
Do not import ZLAgent's graph confidence as truth confidence.
LLM-extracted relation remains candidate_relation_suggestion.
```

Adoption judgment:

```text
Adapt for heavy-source / activation tooling later.
Already aligned with PageIndexRag and GraphRAG-Example findings.
```

### 8. Skill System Uses Sidecar Telemetry And Append-Only History

ZLAgent keeps skill body clean and stores usage / lifecycle / history in sidecars.

Source anchors:

- Loader supports `SKILL.md` and metadata.zlagent fields: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/skills/loader.py#L6-L25
- Skill manifest fields: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/skills/loader.py#L116-L128
- metadata.zlagent triggers / wiki_cache / streaming / rich_output / crystallize: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/skills/loader.py#L247-L341
- Usage sidecar rationale: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/skills/usage.py#L1-L30
- `created_by="agent"` is curator gate: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/skills/usage.py#L17-L21
- Usage event log: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/skills/usage.py#L57-L63
- Skill mutation history JSONL: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/skills/history.py#L1-L28
- Skill guard verdicts and strict background-review rule: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/skills/guard.py#L1-L11
- Curator read-only review and dedupe review: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/skills/curator.py#L163-L227
- Curator refuses non-agent / pinned archive: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/skills/curator.py#L294-L342

Design extraction:

```text
Keep authored knowledge/procedure files clean.
Put telemetry, usage pressure, lifecycle state, and mutation history in sidecars.
Only agent-created artifacts are eligible for autonomous cleanup.
Pinned / user-authored artifacts are protected.
```

Possible fit:

```text
For our future prompts, templates, context-pack recipes, and Misa adapters:
  - content file stays human-readable
  - usage / stale / review pressure goes to sidecar or maintenance manifest
  - append-only history records machine changes
```

Boundary:

```text
Do not create hidden sidecar truth.
Sidecars can track maintenance pressure, usage, and provenance.
Reviewed knowledge remains in explicit reviewed notes / schema.
```

Adoption judgment:

```text
Strong adapt for operational artifacts.
Use carefully for templates / skills / adapter configs, not reviewed truth.
```

### 9. Confirmation Broker Supports Paused Mutating Actions

ZLAgent's confirm-tier tools can suspend the turn, persist a pending confirmation, and resume after yes/no.

Source anchors:

- Agent loop confirmation model: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/loop.py#L17-L26
- Confirmation store TTL and pending rows: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/db/confirmations.py#L79-L132
- Most recent open pending wins: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/db/confirmations.py#L139-L168
- Supersede old pendings: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/db/confirmations.py#L168-L199
- Resume flow executes or denies tool: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/confirmation/flow.py#L40-L108
- Suspend flow stores question and history: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/confirmation/flow.py#L213-L249
- REST confirm API: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/api/confirmations.py#L1-L17

Design extraction:

```text
Mutating actions should be resumable, auditable, and time-limited.
Confirmation is not a chat trick; it is a persisted state machine.
```

Fit:

```text
Useful for future Misa external actions:
  - sending message
  - modifying files
  - promoting candidate to reviewed
  - running MCP/install operation
```

Boundary:

```text
Human yes confirms execution intent.
It does not validate claim truth.
Promotion to reviewed knowledge still requires evidence-aware review.
```

Adoption judgment:

```text
Adapt when Misa can trigger actions.
Not needed for current read-only research pass.
```

### 10. MCP Install / Add / Promote Workflow Is Powerful But Dangerous

ZLAgent can install MCP server packages at runtime, attach them, inspect installed packages, and promote selected tools to safe.

Source anchors:

- MCP manage action list and safety explanation: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/builtins/mcp_manage.py#L1-L40
- `mcp_manage` is confirm-tier and read-only actions can bypass confirm: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/builtins/mcp_manage.py#L177-L183
- Read-only action hook: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/builtins/mcp_manage.py#L400-L433
- `install_and_add` behavior: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/builtins/mcp_manage.py#L633-L717
- Promote persists per-tool permission: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/tools/builtins/mcp_manage.py#L775-L903
- MCP config defaults tools to confirm unless promoted: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/mcp/config.py#L90-L114
- Installer safety model: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/mcp/installer.py#L21-L33
- Package name and git URL validation: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/mcp/installer.py#L56-L96
- `--ignore-scripts` default: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/mcp/installer.py#L270-L296
- Env-level npm script ignore defense: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/mcp/installer.py#L420-L436
- Lifecycle attach registers tools with permission override: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/mcp/lifecycle.py#L318-L393
- Tool wrapper marks promoted tools read-only/concurrency-safe: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/mcp/tool_wrapper.py#L47-L64
- Credential redaction: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/mcp/credential.py#L1-L12

Design extraction:

```text
Runtime tool expansion needs a lifecycle:
discover -> install -> attach -> inspect -> promote -> monitor -> remove
```

Fit:

```text
This is useful conceptually for future Misa tools.
For the current vault, do not import runtime MCP installation into the knowledge architecture.
```

Boundary:

```text
MCP tool availability is capability, not knowledge.
Promoting a tool to safe means it is allowed to run; it does not make its output reviewed evidence.
```

Adoption judgment:

```text
Watch / design-only.
Good as an API/MCP safety reference, too heavy for v0.3 core.
```

### 11. Intent Router And Skill Routing Are Context Economy, Not Truth

ZLAgent uses a small router to pick knowledge modes and skills before main LLM execution.

Source anchors:

- Turn preparer phases: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/turn_preparer/preparer.py#L8-L13
- Memory / router dynamic suffix: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/turn_preparer/preparer.py#L91-L132
- Wiki fast path: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/turn_preparer/preparer.py#L352-L407
- Stable prompt with skill body: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/turn_preparer/preparer.py#L419-L438
- Router is best guess only: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/routing/llm_router.py#L1-L8
- Skip greeting / yes-no / unclear intents: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/routing/llm_router.py#L35-L90
- Confirmation-only replies do not inherit skill hint: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/routing/policy.py#L168-L187

Design extraction:

```text
Route first, load less, and block accidental inherited context on low-information replies.
```

Fit:

```text
This supports our Activation Tier / context pack discipline.
Misa should route a query to the smallest relevant context pack rather than read the whole vault.
```

Boundary:

```text
Router choice is activation.
It is not evidence support and not relation confidence.
```

Adoption judgment:

```text
Already aligned. Keep as context-economy inspiration.
```

### 12. Sub-Agent Delegation Is Quarantined

ZLAgent can delegate to a sub-agent but restricts its tool set.

Source anchors:

- Sub-agent safe/read-only boundary: https://github.com/Kkkirito-123/ZLAgent/blob/01c12946460126e11c4c940f8b6d6c0bd9261749/backend/agent/delegation.py#L179-L179
- Delegate tool location: `backend/tools/builtins/delegate_tool.py`

Design extraction:

```text
Delegated workers should not inherit the full toolbelt.
```

Fit:

```text
If we later run parallel research agents:
  - sub-agent can search / summarize / propose
  - sub-agent cannot promote reviewed truth
  - sub-agent cannot perform external side effects
  - sub-agent cannot mutate main vault except writing isolated review artifacts
```

Boundary:

```text
Sub-agent output is candidate review input.
```

Adoption judgment:

```text
Adapt as operating rule for future parallel framework experiments.
```

## Best Transferable Alphas

### Alpha A: Agent Operation Gate

Borrow from:

```text
ToolPermission + read_only/concurrency/destructive + is_action_read_only(args)
```

Use in our system as:

```text
Misa / Codex / scheduled jobs capability boundary.
```

Minimal form:

```yaml
operation_gate:
  actor:
  action:
  target_layer:
  permission: safe | confirm | forbidden
  side_effect: none | vault_candidate_write | reviewed_write | external
  allowed_record_types:
    - query_result
    - candidate_point
    - feedback_event
    - review_due
```

Why alpha:

```text
It gives future agent access a crisp permission vocabulary without changing reviewed knowledge schema.
```

### Alpha B: Background Review Fork As Review Pressure

Borrow from:

```text
post-turn review schedule + tool whitelist + background write origin
```

Use in our system as:

```text
After an answer/action, agent may propose:
  feedback_event
  review_due
  candidate_point
  maintenance_manifest
but cannot promote truth.
```

Why alpha:

```text
This is the clean bridge between "agent learns from use" and "feedback must not mutate truth".
```

### Alpha C: Write-Origin Provenance

Borrow from:

```text
ContextVar-based foreground/background_review origin
```

Use in our system as:

```text
Every machine-written candidate / feedback / review_due should say who wrote it and under what mode.
```

Why alpha:

```text
Tiny field, big safety payoff.
```

### Alpha D: Sidecar Telemetry For Operational Artifacts

Borrow from:

```text
.usage.json
.usage_events.jsonl
.history.jsonl
created_by=agent curator gate
```

Use in our system as:

```text
For prompts, context-pack recipes, tools, Misa adapters, dashboards:
  content stays clean
  usage/staleness/history go to sidecars or maintenance manifests
```

Why alpha:

```text
It gives maintenance visibility without polluting knowledge notes.
```

### Alpha E: Async Candidate Graph Cache

Borrow from:

```text
per-record extraction cache
content-hash invalidation
fail-open read
background preheat
```

Use in our system as:

```text
For heavy sources, build activation-only candidate graph fragments.
```

Why alpha:

```text
It speeds exploration while preserving our rule:
auto-extracted graph is not reviewed relation.
```

### Alpha F: Confirmation Broker For Mutating Actions

Borrow from:

```text
pending confirmation state machine
resume after yes/no
TTL and superseding
```

Use in our system as:

```text
For future Misa actions:
  external side effect
  file mutation
  promotion request
requires persisted confirmation.
```

Why alpha:

```text
It separates "the model proposed an action" from "the operator authorized this action".
```

## Do Not Import

Do not import these as-is:

```text
1. Full personal-agent OS runtime.
2. IM gateways as core architecture.
3. Runtime MCP installation as v0.3 vault feature.
4. Cache confidence as truth confidence.
5. LLM-extracted graph relations as reviewed relations.
6. Agent memory as reviewed knowledge.
7. Background review as evidence-aware review.
8. Dynamic skills as first-class truth layer.
```

Reason:

```text
These would make the project heavier and blur the exact boundary our system is built to protect:
retrieval / memory / graph / feedback / dashboard are not truth authority.
```

## Comparison With Our Framework

ZLAgent has more runtime muscle:

```text
tools
MCP
IM
memory
skill lifecycle
wiki cache
graph extraction
confirmation
background jobs
```

Our framework has higher epistemic value:

```text
source
candidate point
evidence packet
warrant
challenge
review
reviewed node/relation
context pack trace
action basis
feedback without truth mutation
```

Plain comparison:

```text
ZLAgent is better at letting an assistant operate.
Our system is better at deciding what can responsibly support action.
```

They are complementary:

```text
ZLAgent -> execution and maintenance discipline
Verified Action Knowledge System -> truth / evidence / action-basis discipline
```

## Three-Way Fusion Comparison

Plain judgment:

```text
The fusion is reasonable only if it stays as an outer operating layer.
It should not rewrite the verified-action knowledge spine.
```

| Dimension | Current Verified Action Vault | ZLAgent | Fusion Version |
|---|---|---|---|
| Core goal | Make knowledge reliable enough to support action. | Let an agent safely operate tools, memory, MCP, skills, and background jobs. | Keep our evidence/review spine, add a restricted agent operation layer outside it. |
| Strongest part | Evidence Packet, warrant, challenge, reviewed relation, action basis. | Runtime permissions, confirmation, memory, wiki cache, GraphRAG, MCP lifecycle. | Misa can use the vault safely; Codex can review and write locally with clean provenance. |
| Truth authority | Reviewed node / reviewed relation after evidence-aware review. | Memory / wiki / graph cache are heavily used operationally. | Truth authority remains only the reviewed layer. Memory/cache/graph are activation or review input. |
| Agent role | Agent boundary exists conceptually, but operation-level permissions are still coarse. | Agent can query, write memory, edit skills, install MCP, run review forks. | Misa is query/feedback/candidate-only; Codex is local reviewer/writer. |
| Memory | Activation Tier is context, not truth. | Long-term memory is injected into prompt and can be reviewed/managed. | Misa memory can create feedback or candidate signals, not reviewed knowledge. |
| Graph/RAG | Association and graph retrieval are activation aids. | GraphRAG snapshot and wiki cache accelerate answers. | Candidate graph/cache helps find context, never proves truth or creates reviewed relations. |
| Tool safety | Future MCP/agent writes are quarantined, but the operation table is not yet detailed. | `safe / confirm / deny` plus read-only action overrides. | Add `agent_operation_gate` for Misa/Codex/MCP actions. |
| Background learning | Feedback / review_due captures use pressure. | Post-turn background review can write memory/skills under filters. | Background review creates review pressure only: feedback_event, review_due, candidate signal. |
| Main risk | Might be too static before Misa starts using it. | Might let cache, memory, graph, or agent notes look like knowledge. | Use ZLAgent's operating discipline while locking our truth boundary. |
| Complexity | Light and evidence-oriented. | Broad, runtime-heavy, many moving parts. | Borrow small hard details only; do not import the full Agent OS. |

Current vault flow:

```text
source
-> candidate point
-> calibration / point collision
-> Evidence Packet
-> evidence-aware review
-> reviewed node / reviewed relation
-> context pack / action basis
-> action
-> use ledger / feedback / review_due
```

ZLAgent flow:

```text
user message
-> intent / skill router
-> memory injection
-> wiki cache / graph context
-> tool calls
-> confirm if risky
-> answer
-> background memory / wiki / graph / review
```

Fusion flow:

```text
Misa receives query
-> operation gate checks what Misa may do
-> Misa reads reviewed knowledge / context pack
-> Misa answers or asks confirmation for action
-> Misa writes only use ledger / feedback_event / review_due / candidate signal
-> Codex local picks up those signals
-> Codex builds Evidence Packet
-> Codex runs evidence-aware review
-> only then update reviewed node / reviewed relation / action basis
```

The real change is small:

```text
1. Add agent_operation_gate.
2. Add write_origin on machine-written records.
3. Add a Misa -> Codex candidate/feedback buffer.
4. Keep memory / graph / cache as activation only.
```

Minimal operation split:

```yaml
misa:
  query_reviewed_context: safe
  read_context_pack: safe
  emit_feedback_event: safe
  emit_review_due: safe
  emit_candidate_signal: safe_or_confirm
  modify_reviewed_truth: forbidden
  create_reviewed_relation: forbidden
  external_action: confirm

codex_local:
  write_candidate_or_review_artifact: safe_or_confirm
  build_evidence_packet: safe
  update_reviewed_knowledge: after_evidence_review
  update_main_architecture_docs: after_user_confirmation
```

One-sentence fusion:

```text
Our system remains the evidence judge; ZLAgent gives us the operating gate around Misa and Codex.
```

## Misa / Codex Split Implication

Future split can be:

```text
Misa on VPS:
  query
  retrieve context pack
  answer
  call safe tools
  emit feedback_event / review_due / candidate signal
  request confirmation for external actions

Codex local on Mac/Win:
  read/write files
  review sources
  create candidate points
  build Evidence Packet
  promote reviewed nodes / relations after review
  update handoff / docs when confirmed
```

ZLAgent strengthens this split by giving us vocabulary for:

```text
safe vs confirm vs forbidden
foreground vs background_review
read-only action bypass
pending confirmation
agent-created artifact lifecycle
sidecar history
async graph cache
```

## Candidate Point Collision With Current System

| Candidate Point From ZLAgent | Local Reviewed Principle | Calibration Output | Review Question |
|---|---|---|---|
| Tool operations need safe / confirm / deny plus read-only sub-action checks. | Agent memory quarantine and future MCP writes cannot alter reviewed truth directly. | refines | Should we add a small `agent_operation_gate` convention for future Misa/Codex access? |
| Background review can run after a turn with a restricted tool whitelist. | Feedback Ledger can create review pressure but cannot mutate truth. | supports / refines | Should background review outputs be limited to `feedback_event`, `review_due`, `candidate_point`, and `maintenance_manifest`? |
| Write-origin provenance distinguishes foreground and background review writes. | Source provenance is lightweight and use/review/action traces live in their own layers. | refines | Should machine-written candidate/review_due records carry `write_origin`? |
| Wiki cache can crystallize atomic facts and assign confidence. | Evidence Support Check lives on evidence items; confidence belongs to reviewed claims only after review. | scope_mismatch | Can we borrow supersession and low-confidence audit without importing cache confidence as truth? |
| GraphRAG extraction is async, cached, and fail-soft. | Association and graph retrieval are activation/review-input, not reviewed relations. | supports | Should candidate graph fragments have content-hash cache and explicit `activation_only` state? |
| Runtime MCP install/promote lets agent expand tools. | Do not start API/MCP/tool runtime unless explicitly asked; tools are not truth authority. | risk_of | Should MCP install remain design-only until Misa/Codex action layer exists? |

## Support / Challenge Review

What supports adopting the operational alphas:

```text
The code implements the boundaries, not just README claims:
  - permission metadata in Tool base and registry
  - confirm suspension in confirmation store/flow
  - background review write-origin
  - memory source priority and scanner
  - sidecar usage/history
  - async graph cache
  - MCP installer hardening
```

What challenges adoption:

```text
The repo is broad and agent-runtime-heavy.
Many features solve IM assistant operations, not verified knowledge design.
Its graph/cache confidence semantics are operational and can conflict with our truth confidence language.
Runtime MCP installation is a security-sensitive feature and should not enter v0.3 core.
```

Scope limits:

```text
Use as implementation/design inspiration for future agent access layer.
Do not treat as evidence that our current knowledge schema should expand now.
```

Review again when:

```text
Misa needs to do more than query.
Codex starts writing candidate/review records through a tool layer.
We design an API/MCP boundary for the vault.
We implement dashboard health + maintenance manifests.
```

Action readiness:

```text
Ready for narrow design absorption.
Not ready for direct runtime migration.
```

## Fusion Judgment

Conclusion:

```text
adapt
```

Best immediate absorption:

```text
1. agent_operation_gate
2. background_review_fork_as_review_pressure
3. write_origin provenance for machine writes
4. sidecar telemetry/history for operational artifacts
5. async candidate graph cache as activation-only
```

Do not absorb now:

```text
1. full Agent OS
2. runtime MCP installation
3. wiki cache confidence as truth
4. LLM graph relation confidence
5. autonomous skill/memory curator over reviewed knowledge
```

Minimal next step if we choose to write back later:

```text
Add a small section to MEMORY_TIER.md or ARCHITECTURE_PRINCIPLES.md:
"Agent Operation Gate / Write-Origin Provenance"

Add a small section to FEEDBACK.md:
"Background review fork may create review pressure, not truth mutation."

No schema rewrite required yet.
```
