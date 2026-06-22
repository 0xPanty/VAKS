---
type: source
record_kind: source_card
status: source-captured
title: "kanna12580/kk-knowledge-agent"
source_id: github-kanna12580-kk-knowledge-agent
source_uri: https://github.com/kanna12580/kk-knowledge-agent
source_url: https://github.com/kanna12580/kk-knowledge-agent
source_type: repository
author: kanna12580
publisher: GitHub
published_at:
updated_at: 2026-06-09T18:54:46+08:00
captured_at: 2026-06-14
captured_by: Codex
version_or_commit: 713cf3ada1d44b7484157d64a75f61f071caa1bb
source_integrity:
  source_hash:
  snapshot_hash: 2258D9C9CE34281A07D9A86BC0D98BFB439E6527A2CD45ADAE22EB1595519095
  ingest_state: new
adapter_ingest:
  adapter_name: git-clone-and-archive
  adapter_version: git archive
  capture_method: "git clone --depth 1, then git archive HEAD"
  extraction_trace: "local inspection of README, AGENTS, backend, mcp-server, docs, tests"
  known_limits:
    - "No long-running backend/frontend/MCP runtime test was performed in this VAKS intake."
    - "Architecture review is based on code and project docs at commit 713cf3a."
source_status: active
raw_location: raw/repos/_snapshots/2026-06-14-kanna12580-kk-knowledge-agent-713cf3a-source.zip
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: normal
review_owner: Codex
formalization_status: raw-only
why_saved: "User asked whether kk-knowledge-agent can help future MISA knowledge-base use or memory improvement."
topics:
  - mcp
  - external-knowledge-base
  - rag-mvp
  - agent-context
projects:
  - misa
source_family:
  - repository
  - mcp-agent-knowledge
upstream_sources: []
verification_status: source_snapshot_captured
candidate_relation_suggestions: []
tags:
  - repo-intake
  - mcp
  - external-knowledge-base
  - misa-memory
---

# 来源记录：kanna12580/kk-knowledge-agent

## 为什么收录

用户要求蒸馏 `kanna12580/kk-knowledge-agent`，并明确询问它以后是否能帮助 MISA 使用知识库或提升记忆。

本记录只保存来源身份和可回溯快照。它不代表该仓库已经被采纳，也不代表任何检索结果可以作为事实支持或行动依据。

## 来源信息

- 作者：kanna12580
- 发布方：GitHub
- 原始链接：https://github.com/kanna12580/kk-knowledge-agent
- 版本 / commit：`713cf3ada1d44b7484157d64a75f61f071caa1bb`
- commit 时间：`2026-06-09T18:54:46+08:00`
- commit subject：`Add demo screenshots to README`
- source_status：active
- 采集方式：`git clone --depth 1` + `git archive HEAD`
- 本地快照：`raw/repos/_snapshots/2026-06-14-kanna12580-kk-knowledge-agent-713cf3a-source.zip`
- 快照 SHA256：`2258D9C9CE34281A07D9A86BC0D98BFB439E6527A2CD45ADAE22EB1595519095`

## Intake Boundary

```yaml
processing_tier: medium
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

Source records provide provenance and findability. They must not carry adopt/reject verdicts, truth scores, project borrowing conclusions, or action basis.

## Inspected Repository Areas

| Area | Anchor | Why inspected |
|---|---|---|
| Project framing | `README.md:1`, `README.md:3`, `README.md:5`, `README.md:110` | Confirms lightweight knowledge-agent scope and MVP capabilities. |
| Development guide | `AGENTS.md:3`, `AGENTS.md:9`, `AGENTS.md:13`, `AGENTS.md:154` | Confirms backend-core and MCP-as-adapter design intent. |
| Handoff / architecture | `docs/PROJECT_HANDOFF.md:15`, `docs/PROJECT_HANDOFF.md:85`, `docs/PROJECT_HANDOFF.md:98`, `docs/PROJECT_HANDOFF.md:523` | Confirms intended agent external knowledge-base path. |
| Data model | `backend/app/db/models.py:13`, `backend/app/db/models.py:32`, `backend/app/db/models.py:60` | Confirms SQLite model split: knowledge base, document, document chunk. |
| Schema / API payloads | `backend/app/db/schemas.py:124`, `backend/app/db/schemas.py:138`, `backend/app/db/schemas.py:147` | Confirms search request/result/response contract. |
| Chunking | `backend/app/services/chunk_service.py:4` | Confirms paragraph-first chunking with overlap. |
| Embedding | `backend/app/services/embedding_service.py:11`, `backend/app/services/embedding_service.py:27` | Confirms local sentence-transformers embedding wrapper. |
| Vector store | `backend/app/vector/chroma_client.py:12`, `backend/app/vector/chroma_client.py:36`, `backend/app/vector/chroma_client.py:62` | Confirms Chroma add/query/delete wrapper. |
| Retrieval | `backend/app/services/retrieval_service.py:12`, `backend/app/services/retrieval_service.py:26`, `backend/app/services/retrieval_service.py:59` | Confirms query embedding, Chroma query, score conversion. |
| Streaming | `backend/app/services/stream_service.py:9`, `backend/app/services/stream_service.py:36` | Confirms SSE event stream wrapper. |
| MCP bridge | `mcp-server/server.py:11`, `mcp-server/server.py:14`, `mcp-server/server.py:15`, `mcp-server/server.py:16`, `mcp-server/tools.py:28`, `mcp-server/tools.py:89`, `mcp-server/tools.py:94` | Confirms FastMCP tools and local-proxy guard. |
| Tests / verification | `mcp-server/tests/test_mcp_tools.py:54`, `mcp-server/tests/test_mcp_tools.py:82`, `mcp-server/tests/test_mcp_tools.py:100`, `backend/scripts/validate_real_backend.py:1` | Confirms tool tests and real backend smoke script exist. |

## 初步看点

- 它是一个可讲清楚的最小外接知识库：Backend API 是核心，MCP Server 是薄适配层。
- 它可以帮助 MISA 未来通过 MCP 查询外部知识库，但它不是完整记忆系统。
- 它没有 reviewed knowledge、evidence support、action basis、feedback ledger 等边界，不能直接作为 VAKS 或 MISA 的可信知识层。
- 它有一个现实工程坑的修复：MCP 调本地 Backend 时使用 `trust_env=False`，避免代理环境污染本地服务调用。

## 明显疑点

- 只支持 `.txt` 和直接文本，缺少 PDF/DOCX/网页/source anchor 等正式资料库输入。
- 检索结果只有 chunk/score，缺少 authority bucket、retrieval receipt、evidence packet、citation highlight。
- MCP 的 `add_text_document` 如果直接连到 MISA/VAKS，必须被限制为 candidate/feedback 写入，不能写 reviewed truth。
- 这不是长期记忆系统；没有 episode、reflection、temporal validity、feedback-driven review pressure。

## 可抽取 Candidate Points

1. Backend-core / MCP-thin-adapter is a useful MISA bridge pattern.
2. Local knowledge retrieval can be useful as MISA activation context, not truth support.
3. MCP local-call reliability requires explicit timeout, backend URL, proxy isolation, and restart/hot-reload notes.
4. SQLite + Chroma + sentence-transformers is enough for a demo bridge, but not a VAKS-grade knowledge substrate.
5. Direct add-document tools need write quarantine before being exposed to MISA.

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- MISA starts implementing a real external knowledge-base adapter.
- A future design tries to let MISA write back into VAKS / reviewed knowledge.
- A context-pack or action-basis feature attempts to cite kk retrieval results as support.

## 下一步

- Use the candidate distillation for orientation.
- Use the MISA project overlay only when designing MISA external knowledge-base access.
- Do not use this source as action basis without a later implementation review and local benchmark.
