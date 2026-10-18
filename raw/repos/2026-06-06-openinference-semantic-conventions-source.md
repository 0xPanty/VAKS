---
type: source
status: source-captured
record_kind: source_card
knowledge_status: raw
retrieval_policy: source_identity_only
promotion_gate: none
lifecycle_state: source_registered
review_pressure: none
action_basis_allowed: false
truth_mutation_allowed: false
title: "OpenInference Semantic Conventions"
source_id: github-arize-openinference-semantic-conventions-2026-06-06
source_uri: github:Arize-ai/openinference/spec/semantic_conventions.md
source_url: https://github.com/Arize-ai/openinference/blob/main/spec/semantic_conventions.md
raw_url: https://raw.githubusercontent.com/Arize-ai/openinference/main/spec/semantic_conventions.md
source_type: repository_spec_file
author: Arize AI / OpenInference contributors
publisher: GitHub
published_at:
updated_at:
captured_at: 2026-06-06
captured_by: Codex
version_or_commit: ece68f51f91c7ad26a33cb8417e87ea3d3c2a046
source_status: active
license:
raw_location: raw/repos/2026-06-06-openinference-semantic-conventions-source/semantic_conventions.md
snapshot_ref_or_source_date: main_commit_ece68f51f91c7ad26a33cb8417e87ea3d3c2a046_2026-06-06
why_saved: primary spec reference for AI operation trace vocabulary candidate intake
raw_sha256: 7DC950B0C3B37E2C3EED31FDA02209E8339C2FEE3D29E4F13E0A7B8AB6079A79
processing_mode: immediate
processing_tier: medium
review_priority: medium
review_owner: Codex
formalization_status: candidate-generated
evidence_level: primary-source-snapshot
verification_status: primary-source-current-main-snapshot
capture_confidence_note: high for captured document contents at checked commit; medium for future upstream state after capture
projects:
  - verified-action-knowledge-system
source_family:
  - observability
  - ai-tracing
  - agent-runtime-receipts
  - retrieval-instrumentation
  - tool-call-tracing
topics:
  - openinference
  - semantic-conventions
  - opentelemetry
  - llm-tracing
  - span-kind
  - retriever
  - reranker
  - tool-call
  - evaluator
  - guardrail
  - prompt-template
  - token-cost
truth_boundary: primary source snapshot and candidate comprehension only; not VAKS schema; not architecture decision; not action basis
candidate_relation_suggestions:
  - target: "[[Activation Tier]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "Retriever, reranker, document score, and embedding traces are useful activation receipts, not truth support."
  - target: "[[Evidence Support Check]]"
    relation_type: contrasts_with
    relation_state: candidate
    why_suggested: "OpenInference trace attributes can record what was retrieved or generated; they do not prove evidence support."
  - target: "[[Agent tool access tiering]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "Tool and agent spans can make tool calls visible, but access authority still needs a separate VAKS policy."
  - target: "[[Use Ledger]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "Token, cost, prompt, session, and span metadata are useful operational receipts for later review."
tags:
  - openinference
  - semantic-conventions
  - tracing
  - ai-observability
  - agent-receipts
  - retrieval-is-activation
  - candidate-only
---

# OpenInference Semantic Conventions Source Record

## 为什么收录

这不是一篇 X 经验文，而是 OpenInference 仓库里的主规格文件。

它对 VAKS 的价值在于：它给 AI 应用运行过程提供了一套可复用的 trace 字段名，比如 LLM、Retriever、Reranker、Tool、Agent、Guardrail、Evaluator、Prompt 等 span kind，以及 input/output、prompt template、token/cost、tool call、retrieval documents、session/user/metadata 等属性。

说人话：

```text
它不是告诉我们“什么是真的”；
它是告诉我们“AI 系统运行时可以把什么痕迹记清楚”。
```

所以这份来源可以作为 VAKS 后续操作回执、agent session capture、retrieval diagnostic、tool-call audit 的候选参考，但不能直接变成 reviewed knowledge、schema 变更或 action basis。

## 来源信息

- Repository: `Arize-ai/openinference`
- Spec file: `spec/semantic_conventions.md`
- GitHub URL: https://github.com/Arize-ai/openinference/blob/main/spec/semantic_conventions.md
- Raw URL: https://raw.githubusercontent.com/Arize-ai/openinference/main/spec/semantic_conventions.md
- Captured main branch commit: `ece68f51f91c7ad26a33cb8417e87ea3d3c2a046`
- Captured at: `2026-06-06`
- Raw file hash: `7DC950B0C3B37E2C3EED31FDA02209E8339C2FEE3D29E4F13E0A7B8AB6079A79`
- Raw copy: `raw/repos/2026-06-06-openinference-semantic-conventions-source/semantic_conventions.md`
- Inspected mode: spec file read and captured; no package execution; no SDK instrumentation launched.

## 文件锚点

| Anchor | What exists | VAKS extraction | Boundary |
|---|---|---|---|
| `semantic_conventions.md:1-3` | Defines semantic conventions as keys and values for concepts, protocols, and operations; used to populate span attributes and span events. | Strong fit for operational receipts. | It defines trace vocabulary, not truth rules. |
| `semantic_conventions.md:6-20` | `openinference.span.kind` is required and includes `LLM`, `EMBEDDING`, `CHAIN`, `RETRIEVER`, `RERANKER`, `TOOL`, `AGENT`, `GUARDRAIL`, `EVALUATOR`, `PROMPT`. | Candidate taxonomy for AI operation traces. | Span kind is a runtime classification, not a reviewed knowledge type. |
| `semantic_conventions.md:29-32` | Document attributes include content, id, metadata, and relevance score. | Useful for retrieval receipts and context-pack provenance. | `document.score` is retrieval signal, not evidence support. |
| `semantic_conventions.md:43-57` | Input value/mime type, LLM messages, invocation parameters, provider/system/model, output messages, prompt template and version. | Useful for run reproduction and prompt-version receipts. | Captured prompts may contain sensitive content and require scope/redaction. |
| `semantic_conventions.md:58-76` | Token counts and cost attributes for prompt, completion, reasoning, audio, cache read/write, and USD cost. | Useful for budget/cost receipts. | Cost and token metrics say nothing about correctness. |
| `semantic_conventions.md:77-85` | LLM advertised tools and message tool-call structures. | Useful for tool-call audit. | Tool-call visibility is not tool permission or safety approval. |
| `semantic_conventions.md:86-92` | Multimodal/reasoning content, provider signatures, encrypted content, and redacted-thinking data fields. | Useful as trace preservation vocabulary. | Reasoning/signature data is sensitive operational data, not reviewed evidence. |
| `semantic_conventions.md:93-114` | Span metadata, output value, reranker/retrieval documents, session id, tags, tool fields, user id. | Useful for session capture and retrieval diagnostics. | User/session/metadata fields need privacy and path-scope boundaries. |
| `semantic_conventions.md:168-188` | Token count detail explains cache read/write, reasoning/audio tokens, cost analysis, and billing reconciliation. | Useful for Use Ledger / run receipts. | Billing reconciliation is operational accounting, not truth calibration. |
| `semantic_conventions.md:193-203` | System/model/provider identification rules and embedding-specific model naming. | Useful for trace clarity. | Model name is source context, not quality evidence. |
| `semantic_conventions.md:231-338` | Indexed attribute prefixes flatten lists of messages, multimodal content, tool calls, and available tools. | Useful if VAKS ever exports trace records to OTel-style attributes. | Flattened attributes are interoperability mechanics, not architecture adoption. |

## 人话总结

OpenInference 这份规格可以帮助 VAKS 把下面这些东西记成可复盘的操作回执：

```text
一次 agent / LLM / retriever / reranker / tool / evaluator / guardrail / prompt rendering
到底发生了什么，输入输出是什么，用了什么模型、prompt、工具、token、成本，
拿到了哪些文档，给了什么分数，属于哪个 session / user / tag。
```

但它不能回答：

```text
这个检索结果是否真的支持结论？
这个 evaluator 分数是否足够可靠？
这个 tool call 是否应该被允许？
这个输出能不能作为行动依据？
```

这些仍然属于 VAKS 自己的 review、warrant、scope、risk、action-basis 边界。

## 当前处理结果

- Source card written: `raw/repos/2026-06-06-openinference-semantic-conventions-source.md`
- Raw spec snapshot retained: `raw/repos/2026-06-06-openinference-semantic-conventions-source/semantic_conventions.md`
- Candidate distillation: `outputs/review/2026-06-06-openinference-semantic-conventions-candidate-distillation.md`
- Project overlay: `outputs/review/project_overlays/VAKS-openinference-semantic-conventions-2026-06-06.md`

