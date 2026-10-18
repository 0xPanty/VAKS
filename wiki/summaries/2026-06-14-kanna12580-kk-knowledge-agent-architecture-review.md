---
type: library_review
status: draft
library_name: "kk-knowledge-agent"
repo_url: "https://github.com/kanna12580/kk-knowledge-agent"
source_url: "raw/repos/2026-06-14-kanna12580-kk-knowledge-agent-source.md"
checked_commit: 713cf3ada1d44b7484157d64a75f61f071caa1bb
commit_time: 2026-06-09T18:54:46+08:00
source_status: active
reviewed_at: 2026-06-14
domain:
  - mcp
  - external-knowledge-base
  - rag-mvp
  - agent-context
related_projects:
  - misa
current_branch: "MISA knowledge-base access and runtime-memory support"
extracted_patterns:
  - backend-core-mcp-thin-adapter
  - local-vector-kb-agent-tool
  - mcp-local-proxy-isolation
fusion_decision: adapt
confidence: medium
evidence_count: 18
cross_validated_with:
  - "existing VAKS agent memory quarantine boundary"
  - "existing MISA runtime memory question"
negative_evidence:
  - "No reviewed-knowledge, evidence-support, authority-bucket, feedback-ledger, or action-basis boundary."
  - "Retrieval score is ordinary vector similarity, not support."
extension_potential: "Useful as MISA external knowledge-base adapter scaffold; weak as long-term memory architecture."
relations: []
tags:
  - architecture-review
  - mcp
  - external-knowledge-base
  - misa-memory
---

# 库分析：kk-knowledge-agent

## 它解决什么问题

它解决的是一个很具体的问题：

```text
Agent 想查一个本地知识库
-> MCP tool call
-> Python MCP Server
-> Backend HTTP API
-> SQLite metadata + Chroma chunks
-> 返回相关 chunk
-> Agent 自己组织回答
```

说人话：它不是“第二大脑”，也不是“可靠知识系统”。它是一个轻量外接知识库 Demo，把“Agent 能不能查本地资料”这条链路跑通。

这对 MISA 有用，因为 MISA 以后确实需要从资料库或项目知识库里取上下文。但它对 MISA 的帮助主要在工程接口，不在记忆理论。

## 核心设计

```text
Frontend demo
  -> Backend API
      -> SQLite: knowledge base / document / chunk metadata
      -> ChromaDB: chunk embeddings
      -> sentence-transformers: local multilingual embedding

MCP Server
  -> exposes search/list/add tools
  -> calls Backend API only
  -> does not duplicate retrieval logic
```

最值得借的是这个分工：

```text
Backend = only business core
MCP = thin adapter
Frontend = demo / human operation
```

对 MISA 来说，这个分工比它具体用 SQLite/Chroma 更重要。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:3` | Project says it supports knowledge-base management, upload, chunk vectorization, semantic retrieval, streaming, and MCP exposure. | Confirms whole product shape. | README scope is not proof of production readiness. |
| `README.md:5-24` | Architecture diagram: Frontend -> Backend -> SQLite/Chroma/sentence-transformers; Agent -> MCP -> Backend. | Clean split between human UI and agent tool path. | No authority/truth boundary in this diagram. |
| `AGENTS.md:13-18` | Backend is only business core; SQLite and Chroma split; Chinese semantic retrieval uses multilingual MiniLM. | Good implementation discipline for small local system. | Storage split is not VAKS schema governance. |
| `AGENTS.md:154-177` | MCP Server phase: `search_knowledge_base`, optional `list_knowledge_bases`, `add_text_document`, 10s timeout, backend error handling. | Useful MISA tool contract seed. | `add_text_document` must be quarantined if MISA writes to important stores. |
| `docs/PROJECT_HANDOFF.md:85-99` | MCP Server is an agent adapter; same backend core serves UI and agent tools. | Strongest architecture lesson. | Still a simple RAG app, not memory governance. |
| `backend/app/db/models.py:13-76` | KnowledgeBase, Document, DocumentChunk tables. | Minimal local knowledge-store shape. | No provenance/source anchor/review fields. |
| `backend/app/db/schemas.py:124-147` | SearchRequest, SearchResult, SearchResponse. | Simple retrieval response contract. | Missing authority bucket, warning code, receipt, citation anchor. |
| `backend/app/services/chunk_service.py:4-37` | Paragraph-first splitting; long paragraph fixed window; overlap support. | Good enough ingestion primitive for MVP. | Not enough for legal/source-grade anchors. |
| `backend/app/services/embedding_service.py:11-45` | Lazy sentence-transformers wrapper. | Simple local embedding adapter. | Model output is activation only. |
| `backend/app/vector/chroma_client.py:12-82` | Persistent Chroma client, add/delete/query with metadata filters. | Derived vector index pattern. | Chroma is cache/index, not source of truth. |
| `backend/app/services/document_service.py:74-145` | Create document, split, save chunks, embed, write vectors, save vector IDs. | Complete mini ingest path. | Rollback protects ingest, not knowledge correctness. |
| `backend/app/services/retrieval_service.py:12-23` | Query embedding then Chroma query by `knowledge_base_id`. | Narrow retrieval core. | No hybrid search/rerank/citations. |
| `backend/app/services/retrieval_service.py:59-69` | Converts Chroma distance to score using `1/(1+distance)`. | Practical score normalization. | Score must not become support/confidence. |
| `backend/app/services/stream_service.py:9-36` | SSE wrapper returns `start`, `delta`, `result`, `error`, `done`. | Product demo streaming pattern. | Stream is retrieval display, not LLM reasoning or evidence review. |
| `mcp-server/server.py:11-16` | FastMCP registers `search_knowledge_base`, `list_knowledge_bases`, `add_text_document`. | Agent-facing surface is small and understandable. | Tool permissions are coarse. |
| `mcp-server/tools.py:28-84` | Tool input validation and structured errors. | Useful MISA adapter hygiene. | Does not implement write authority levels. |
| `mcp-server/tools.py:89-117` | HTTP backend call with timeout, `trust_env=False`, readable errors. | Very useful local MCP reliability pattern. | Local-call fix does not solve authorization. |
| `docs/DEVELOPMENT_LOG.md:250-300` | Documents Bad Gateway proxy issue, restart/hot-load issue, and live Codex MCP query success. | Practical deployment learning for MISA. | This is one local validation, not general benchmark. |
| `backend/scripts/validate_real_backend.py:1-114` | Temporary SQLite/Chroma smoke test with real embedding queries. | Good local smoke-test shape. | Uses small demo corpus only. |

## 当前支线价值

当前支线：

```text
MISA using a local/external knowledge base and improving runtime memory continuity.
```

它对当前支线：

```text
refines
```

具体价值：

- 给 MISA 一个最小外接知识库桥的工程形状：MCP tool -> backend API -> retrieval core。
- 给 MISA 一个很清楚的“不重复检索逻辑”原则：MCP 只做工具适配，核心查询在 backend。
- 给 MISA 一个本地工具可靠性清单：backend URL、timeout、`trust_env=False`、重启 MCP 子进程。
- 给 MISA 一个候选写入口警告：`add_text_document` 很方便，但未来只能写 candidate / feedback / scratch，不许直写 reviewed knowledge。

风险：

- 如果把它当“记忆系统”，会跑偏。它没有长期记忆、事件记忆、反馈学习、冷热上下文、过期/复活机制。
- 如果把它当“VAKS 检索层”，会降级。它没有 authority bucket、source anchor、evidence packet、review gate。
- 如果把 Chroma score 当可信度或证据支持，会污染 MISA 的判断。

## 全貌架构价值

必须过一遍，不因当前支线而跳过。

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Simple repo layout and README/AGENTS handoff are clear. | adapt as style only |
| Dusk workbench | Frontend demo gives a simple operation surface. | watch |
| source ingest | Text/txt upload + chunking is useful as a minimal ingest path. | adapt for toy/sandbox only |
| review queue | No review queue. | no |
| schema / reviewed knowledge | No schema authority, no reviewed layer. | no |
| memory / dev context | Useful as retrieval context provider, not memory engine. | adapt for MISA bridge |
| feedback | No feedback ledger or outcome calibration. | no |
| retrieval / cache | SQLite metadata + Chroma vector cache is a clear small-stack pattern. | adapt as derived cache only |
| API / MCP / agent access | Strongest value: thin MCP adapter over backend API. | adapt |
| viewer / workbench | Frontend demo can inspire a minimal operator panel. | watch |
| publishing | No publishing path. | no |
| risk / anti-pattern | Main risk is confusing retrieval with evidence or memory. | keep as warning |

## 值得提炼的模式

### Pattern 1: Backend-core, MCP-thin-adapter

```text
Backend owns knowledge CRUD, chunking, embedding, retrieval.
MCP server owns only agent-facing tool calls.
```

MISA 可以借这个接口边界。尤其是未来 MISA 读资料库时，不应该在每个 agent 工具里重复实现解析、检索、过滤、缓存。

### Pattern 2: Local external KB as activation provider

检索结果可以给 MISA 激活上下文：

```text
query -> candidate chunks -> MISA reads/uses as context
```

但必须加我们的边界：

```text
retrieval_result = activation/orientation
not evidence support
not truth confidence
not action basis
```

### Pattern 3: MCP local-call hardening

`mcp-server/tools.py` 里 `httpx.AsyncClient(..., trust_env=False)` 很值得记住。MISA 接本地服务时，系统代理、Codex 进程环境、localhost/127.0.0.1、MCP 子进程热加载都会制造假故障。

### Pattern 4: Tool set is intentionally small

```text
search_knowledge_base
list_knowledge_bases
add_text_document
```

MISA 早期也应该小工具面，而不是一上来开放完整写库、改库、删库。

## 标签与量化

- domain: MCP / external knowledge base / RAG MVP
- problem: Agent needs a simple way to query local knowledge.
- pattern: backend-core-mcp-thin-adapter
- maturity: experimental
- complexity: medium
- problem_fit: 4/5 for MISA external KB access
- reuse_value: 3/5
- implementation_cost: 3/5
- integration_fit: 4/5 for MISA bridge, 1/5 for VAKS core
- evidence_strength: 3/5
- reversibility: 5/5 if used as design-only scaffold

## 交叉验证

- 相似设计来源：knowledge-base-server, agentmemory, MCP read-only tools, local RAG MVPs.
- 用户历史项目里的相似问题/影子：MISA needs durable runtime context and a safe bridge into the knowledge base.
- 支持证据：Repo includes backend, frontend, MCP server, docs, tests, and live Codex MCP validation notes.
- 反例或失败边界：No reviewed knowledge boundary; no source anchors; no action-basis discipline.
- 最小验证方式：Build a MISA adapter prototype that only exposes read/list first, returns retrieval receipts, and cannot write reviewed knowledge.

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| MCP thin adapter over backend API is useful for MISA. | Agent access should be read-first and path-scoped; runtime memory is not reviewed truth. | candidate_relation | What minimal tool set should MISA get first: search/list only, or add candidate write? |
| Local vector KB can provide activation context. | Association Neighborhood Activation is retrieval/activation, not truth. | refines | How should MISA label retrieval chunks so they cannot become support? |
| `add_text_document` is convenient for agent writeback. | Agent memory quarantine forbids direct reviewed writes. | risk_of | Should MISA write only feedback events / candidate notes through receipts? |
| Chroma score can rank chunks. | Retrieval rank is not trust. | supports as warning | Should MISA response schema hide or downgrade score by default? |
| The repo can improve MISA memory. | Memory Tier / Dev Context distinguish activation from truth and project context. | scope_mismatch | Is this runtime knowledge access, not durable memory? |

边界：

- 相似不是支持。
- 冲突不是自动推翻。
- 重复出现不是自动真理。
- 校准输出是 review input，不是 reviewed relation。

## Support / Challenge Review

- What supports it:
  - The repo has real MCP tool code and explicit backend-only retrieval logic.
  - Docs and development log describe live Codex MCP installation and query validation.
  - Tests cover MCP success, empty query, 404, timeout, and empty-result paths.
- What challenges it:
  - It lacks VAKS-grade provenance, review, action, and feedback boundaries.
  - It is not a true memory system.
  - It only handles txt/text and simple Chroma retrieval.
- Challenge severity: major for VAKS core; minor for MISA bridge scaffold.
- Scope limits:
  - Use for MISA external KB adapter shape.
  - Do not use for truth layer, reviewed knowledge, or action support.
- Known risks:
  - Retrieval score mistaken for confidence.
  - Agent write tool writes unreviewed memory into durable stores.
  - Demo stack mistaken for scalable production memory.
- Review again when:
  - MISA starts building an external knowledge-base bridge.
  - Any writeback tool is proposed.
  - A MISA answer uses retrieved chunks as evidence.
- Action readiness: not_ready

## 对当前项目的适配点

For MISA:

```text
MISA -> MCP tool -> knowledge backend -> retrieved chunks/context
```

Add VAKS/MISA safety wrapper:

```text
authority_bucket
retrieval_receipt
source_ref / candidate_ref
warning_code
write_scope
action_basis_allowed: false
```

The repo's direct value is not "better memory". It is "MISA can ask a knowledge backend for relevant context through a clean tool boundary".

## 可拓展性

- 是否适合作为插件/适配层：yes, as design scaffold.
- 是否会绑定核心结构：low if kept behind adapter contract.
- 未来替换成本：low; backend can be VAKS context-pack API, LanceDB, Qdrant, mdvs search, or custom retrieval.
- 可迁移路径：
  1. Keep MISA tool API small.
  2. Replace `knowledge_base_id` with project/context scope.
  3. Return retrieval receipts and authority labels.
  4. Add write quarantine before `add_text_document`.
  5. Keep vector store derived and rebuildable.

## 复杂度和风险

- Simple enough to copy conceptually.
- Too weak to adopt as-is for VAKS-grade knowledge.
- The main danger is seductive simplicity: it makes Agent-KB lookup feel solved while hiding evidence and action boundaries.

## 不可行点 / 避坑

- Do not use this as MISA's memory brain.
- Do not use ChromaDB as the source of truth.
- Do not expose `add_text_document` to write into reviewed stores.
- Do not treat returned score as evidence/confidence.
- Do not route VAKS action answers through raw chunks without review bucket filtering.
- Do not use `.txt`-only ingest as the final source intake path.

## 融合判断

- 结论：adapt
- 理由：Good MISA external knowledge-base bridge scaffold; not a VAKS core architecture source.
- 验证方式：Build a read-only MISA bridge prototype with receipts and authority labels, then test with a small VAKS-derived candidate corpus.

## 直接判断

- Direct use: no
- Fork: no
- Design-only: yes
- Reject: no
- Current branch value: medium-high for MISA KB access; low for durable memory.
- Whole architecture value: low for VAKS core, medium for agent access/productization.
- Risk: retrieval-as-truth and agent writeback pollution.
- Next action: keep as MISA bridge reference; do not add as VAKS tag/core module.

## 后续行动

- If MISA bridge work starts, create a small adapter spec:
  - read-only `search_context`
  - optional `list_context_sources`
  - no reviewed write
  - candidate/feedback-only write with receipts
- Compare this with `agentmemory`:
  - `kk-knowledge-agent` = external KB lookup path
  - `agentmemory` = runtime continuity/memory path
  - MISA may need both, but they should remain separate.
