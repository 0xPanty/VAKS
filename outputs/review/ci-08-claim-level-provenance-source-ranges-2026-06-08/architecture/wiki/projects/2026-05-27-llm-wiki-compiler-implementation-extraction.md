---
type: implementation-note
status: active
created: 2026-05-27
updated: 2026-05-27
title: llm-wiki-compiler 源码级实现提取
sources:
  - "[[2026-05-26-llm-wiki-compiler-source]]"
  - "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
  - "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
verification_status: primary-source
evidence_level: primary
confidence: high
last_verified: 2026-05-27
next_review: 2026-06-03
related_projects:
  - verified-knowledge-system
extracted_patterns:
  - incremental-source-state-compiler
  - self-contained-review-candidate-record
  - agent-context-pack-budget-guardrails
  - agent-tool-access-tiering
  - source-adapter-ingest-contract
  - project-state-next-action-contract
  - exportable-knowledge-artifact-surface
relations:
  - target: "[[2026-05-27-quality-bar-extensible-verified-action-knowledge-system]]"
    type: implements
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "This extraction turns llm-wiki-compiler source-code patterns into usable implementation contracts for the larger system."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - implementation/blueprint
  - llm-wiki-compiler
  - verified-knowledge-system
---

# llm-wiki-compiler 源码级实现提取

## 一句话结论

这个库已经不是只提供高层灵感了。它可以作为我们第一版实现的工程参照，但要把它的 `concept wiki compiler` 改造成我们的 `verified action knowledge compiler`。

## 已读源码范围

本轮重点阅读：

- `src/compiler/index.ts`
- `src/compiler/candidates.ts`
- `src/compiler/hasher.ts`
- `src/compiler/source-state.ts`
- `src/compiler/deps.ts`
- `src/compiler/page-renderer.ts`
- `src/compiler/prompts.ts`
- `src/compiler/prompt-budget.ts`
- `src/commands/review-approve.ts`
- `src/commands/review-show.ts`
- `src/commands/query.ts`
- `src/context/types.ts`
- `src/context/build.ts`
- `src/context/budget.ts`
- `src/context/ranking.ts`
- `src/context/retrieval.ts`
- `src/context/provenance.ts`
- `src/linter/rules.ts`
- `src/mcp/tools.ts`
- `src/mcp/resources.ts`
- `src/project/state.ts`
- `src/project/recommendations.ts`
- `src/ingest/*`
- `src/adapters/*`
- `src/utils/state.ts`
- `src/utils/lock.ts`
- `src/utils/markdown.ts`
- `src/utils/source-writer.ts`
- `src/utils/embeddings.ts`
- `src/utils/retrieval.ts`
- `src/viewer/server.ts`
- `src/viewer/path-safety.ts`
- `src/export/*`

## 可以直接用上的实现思想

### 1. Incremental Source State Compiler

可用程度：高，应该进入 v0.2 blueprint。

核心做法：

```text
source hash
-> new / changed / unchanged / deleted
-> only compile changed sources
-> preserve source state
-> handle shared concepts
-> freeze shared deleted-source concepts
```

我们要改造为：

```text
source hash
-> affected summaries / claims / patterns
-> only recompile affected candidates
-> never silently drop evidence from deleted raw source
```

### 2. Self-contained Review Candidate

可用程度：非常高，应该优先实现。

候选记录必须自包含：

```yaml
id:
title:
slug:
proposed_node_type:
sources:
body:
generated_at:
source_states:
schema_violations:
provenance_violations:
relation_violations:
actionability_violations:
```

批准时不再调用 LLM。review 的对象和最终入库的对象必须一致。

### 3. Schema + Provenance Lint Before Approval

可用程度：非常高。

`llm-wiki-compiler` 在 candidate 写入时就运行 schema lint 和 provenance lint。我们要扩展为：

```text
schema lint
provenance lint
relation lint
decision readiness lint
actionability lint
agent access lint
```

### 4. Context Pack v1 Envelope

可用程度：非常高。

它的 context pack 有稳定 envelope：

```text
version
prompt
budget
project
primary
neighbors
warnings
gaps
suggestedActions
```

我们要保留 envelope 思想，但增加：

```text
verification_status
evidence_level
confidence
negative_evidence
decision_status
actionability
agent_access_level
```

### 5. Budgeted Context And Source Windows

可用程度：高。

它的 context pack 不是无限塞上下文，而是有预算、trim 顺序、source window 上限和 path confinement。

我们应该直接吸收：

```text
neighbors 先裁剪
source windows 再裁剪
chunks 再裁剪
primary 最后裁剪
source snippets 默认关闭
include_sources 才开启
只允许读 raw/source 目录
```

### 6. Agent Tool Access Tiering

可用程度：高。

源码中已经区分：

```text
需要 LLM/provider 的工具
read-only 工具
会写入的工具
context pack 只读、provider optional
```

我们要进一步正式化成：

```text
Level 1 read-only
Level 2 suggest-only
Level 3 reviewed-write
Level 4 owner-final
```

### 7. Source Adapter Contract

可用程度：高。

可复用点：

- web/pdf/image/transcript/file 都走统一 ingest result。
- session adapters 把 Claude/Codex/Cursor 会话转成 source。
- source writer 处理 empty slug 和 filename collision。
- raw source frontmatter 记录 origin/truncated/sourceType。

我们要扩展到：

```text
web
pdf
repo
video transcript
image/OCR
chat/session
manual note
product output
field-test result
```

### 8. Prompt Budget For Shared Concepts

可用程度：中高。

它遇到多个 source 贡献同一 concept 时，会对 combined content 做预算，避免 prompt 爆上下文。

我们要升级为：

```text
shared claim / pattern compile budget
evidence-priority trimming
source-quality weighted trimming
```

不是平均裁剪所有 source，而是优先保留 primary/source-quality 高的证据。

### 9. Project State And Next Action

可用程度：中高。

`llmwiki next` 的思路值得吸收：系统能读当前状态，然后推荐下一步。

我们可以改造成：

```text
fresh
sources-only
review-pending
lint-attention
verified-ready
decision-ready
action-ready
feedback-needed
```

### 10. Exportable Knowledge Artifact Surface

可用程度：中。

它支持 `llms.txt`、`llms-full.txt`、JSON、JSON-LD、GraphML、Marp。

我们未来可以输出：

```text
llms.txt for model context
json/jsonl for agents
graphml for graph tools
context-pack bundles
decision-pack bundles
content/product packs
```

## 不能直接照搬的地方

### 1. Generic PageKind

它的 schema 是：

```text
concept / entity / comparison / overview
```

这适合作为普通 wiki page kind，不适合作为 truth layer。

我们的核心必须是：

```text
source / summary / claim / pattern / anti-pattern / decision / qa / implementation-note
```

### 2. Query Save Directly Into Wiki

`query --save` 会把回答保存成 wiki page。这个对普通 LLM Wiki 很爽，但对我们要进 review。

改造为：

```text
query answer -> qa output
query answer candidate -> review
reviewed answer -> formal node
```

### 3. Watch Auto Compile

`watch` 自动编译 source 很有用，但正式 truth layer 不能自动写入。

改造为：

```text
watch raw -> generate candidates -> notify review
```

### 4. Confidence 0..1 Too Thin

它的 `confidence/provenanceState/contradictedBy` 是好基础，但不够。

我们需要：

```text
verification_status
evidence_level
confidence
last_verified
next_review
negative_evidence
relation_strength
decision/actionability
```

## 我们的落地顺序建议

### v0.2

```text
outputs/review/candidates/
candidate schema
schema/provenance/relation lint checklist
project state / next action report
minimal context pack JSON
index/log
```

### v0.3

```text
incremental source state
source adapters
query -> qa/review candidate
claim-level source spans
decision readiness lint
Misa read-only context pack
```

### v0.4

```text
local API/MCP
viewer / Obsidian workbench
hybrid retrieval
export packs
feedback timeline
```

## 当前保存的模式

- [[incremental-source-state-compiler]]
- [[self-contained-review-candidate-record]]
- [[agent-context-pack-budget-guardrails]]
- [[agent-tool-access-tiering]]
- [[source-adapter-ingest-contract]]
- [[project-state-next-action-contract]]
- [[exportable-knowledge-artifact-surface]]

## 结论

`llm-wiki-compiler` 的源码可以用来建立我们的第一版工程骨架。我们不需要先 fork，但应该把这些实现 contract 写入蓝图：增量状态、候选自包含、lint before approval、context pack budget、source adapter、agent access、project next action、export surface。

这套骨架会让我们的系统从“可信模板”升级为“可执行、可扩展、可审查的知识操作系统”。
