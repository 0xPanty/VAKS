---
type: source
record_kind: source_card
status: source-captured
created: 2026-05-26
updated: 2026-05-26
title: atomicstrata/llm-wiki-compiler
source_url: "https://github.com/atomicstrata/llm-wiki-compiler"
source_type: repo
author: Ethan Joffe / atomicstrata
publisher: GitHub
captured_at: 2026-05-26
captured_by: Codex
topics:
  - llm-wiki
  - knowledge-compiler
  - review-queue
  - provenance
  - context-pack
projects:
  - verified-knowledge-system
sources:
  - "https://github.com/atomicstrata/llm-wiki-compiler"
  - "raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip"
verification_status: primary-source
evidence_level: primary
source_integrity:
  capture_confidence: high
last_verified: 2026-05-26
next_review: 2026-06-02
snapshot_path: "raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip"
related_claims: []
related_concepts:
  - "[[2026-04-04-karpathy-llm-wiki-pattern]]"
  - "[[2026-05-26-llm-wiki-compiler-architecture-review]]"
candidate_relation_suggestions:
  - target: "[[review-gated-compile-queue]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "The repo implements compile --review, candidate persistence, approve/reject, and candidate lint metadata."
    created: 2026-05-26
    last_verified: 2026-05-26
  - target: "[[claim-level-provenance-source-ranges]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "The repo parses and lints claim citations with source line ranges."
    created: 2026-05-26
    last_verified: 2026-05-26
  - target: "[[context-pack-evidence-envelope]]"
    type: supports
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-26-llm-wiki-compiler-source]]"
    rationale: "The repo defines a stable v1 context pack for agent-ready evidence."
    created: 2026-05-26
    last_verified: 2026-05-26
tags:
  - source/repo
  - knowledge-system
  - llm-wiki
knowledge_status: raw
processing_tier: light
source_id: "https://github.com/atomicstrata/llm-wiki-compiler"
why_saved: see_body_or_legacy_record
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
legacy_raw_metadata:
  source_quality: 4
  freshness: 5
  relevance: 5
  cross_source_count: 1
---
# 来源记录：atomicstrata/llm-wiki-compiler

## 为什么收录

这是 Karpathy LLM Wiki 模式的工程化实现之一。它不是单纯的 Obsidian 模板，而是把 `sources/ -> compile -> wiki/ -> query/context/lint` 做成 CLI、review queue、MCP 工具、只读 viewer 和 context pack。

对本资料库最关键的价值：它已经把“LLM 生成候选”和“正式 wiki 写入”拆开，并且把 provenance、schema lint、context pack 边界做成了可检查的工程结构。

## 核心内容

- `llmwiki compile --review` 把生成页写入 `.llmwiki/candidates/`，不是直接写入 `wiki/`。
- `review approve/reject/show/list` 支持人工复核；approve 时复制候选正文，不再调用 LLM。
- 候选记录包含完整 page body、sources、generatedAt、sourceStates、schemaViolations、provenanceViolations。
- approve/reject 使用 `.llmwiki/lock`；approve 会在锁内重读候选，避免 TOCTOU。
- 多候选来自同一 source 时，source state 延迟到最后一个 sibling candidate 通过后才持久化。
- claim-level provenance 支持 `file.md:42-58` / `file.md#L42-L58` 形式，并有 malformed / out-of-bounds lint。
- provenance metadata 包含 `confidence`、`provenanceState`、`contradictedBy`。
- context pack v1 是稳定 JSON envelope，包含 prompt、budget、project、primary、neighbors、warnings、gaps、suggestedActions。
- `includeSources` 是显式开关，并限制只能读 `sources/` 下的 source window。
- viewer 是只读本地浏览器 UI，默认绑定 `127.0.0.1`，强调 path confinement 和本地安全。
- semantic chunks、BM25 rerank、graph neighbors 只用于候选上下文召回，不构成 truth layer。

## 来源信息

- 作者：Ethan Joffe / atomicstrata
- 发布方：GitHub
- 发布时间：repo 当前 README / package / CHANGELOG 快照以 2026-05-26 采集为准
- 原始链接：https://github.com/atomicstrata/llm-wiki-compiler
- 本地快照：`raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip`
- 采集方式：GitHub README + CHANGELOG + main branch zip + 源码抽样阅读

## 已验证内容

- `package.json` 显示包名 `llm-wiki-compiler`、版本 `0.7.0`、Node `>=24`。
- README 描述 quickstart、compile、review、schema、query、context、lint、watch、serve、viewer 等 CLI 面。
- 源码存在 `src/compiler/candidates.ts`、`src/commands/review-approve.ts`、`src/commands/review-show.ts`，实现候选保存、展示、批准和归档。
- 源码存在 `src/context/types.ts`、`src/context/build.ts`，定义并构建 context pack v1。
- 源码存在 `src/linter/rules.ts`，包含 broken wikilink、orphan、missing summary、duplicate、empty、low confidence、contradicted page、uncited prose、schema cross-link、broken/malformed citation 等规则。
- 源码存在 `src/mcp/tools.ts`，区分 provider-needed 工具和 read-only 工具，并暴露 `get_context_pack`。

## 未验证内容

- 本轮没有安装依赖、运行测试或实际执行 CLI。
- 没有验证 npm 最新发布包是否与 GitHub main 分支完全一致。
- 没有验证 MCP server 在外部 agent 中的真实交互体验。

## 冲突或疑点

- `package.json` 版本为 `0.7.0`，README roadmap 中出现 “Shipped in 0.8.0” 的 context pack 描述；需要以后复查发布状态。
- `package.json` repository/homepage/bugs 字段使用 `atomicmemory/llm-wiki-compiler`，用户提供和 GitHub 页面为 `atomicstrata/llm-wiki-compiler`；需要视为 repo ownership / metadata 迁移痕迹。
- 默认 page kinds 是 `concept/entity/comparison/overview`，不适合作为本资料库 verified truth layer 的核心类型。

## 可复用点

1. Review-gated compile queue：先出候选，再复核入库。
2. Candidate JSON：候选必须自包含、可审计、可归档。
3. Candidate lint：schema/provenance 错误要在批准前暴露。
4. Claim-level source ranges：重要 claim 要能指向具体 source line。
5. Context pack envelope：agent 读取的是证据包，不是直接“真相答案”。
6. Source window opt-in：原文片段默认不暴露，按需、限目录读取。
7. Static lint first：程序先检查结构和证据，不自动重写 vault。
8. Lock/deferred state：未来多 agent 或并发写入时需要防止候选状态污染。

## 下一步

- 把 review queue、claim provenance、context pack、static lint 提炼为本资料库 pattern。
- 不直接采用其 page kinds、viewer、完整 MCP server、watch auto-compile。
- 后续 v0.2 可以先做 Markdown-only 候选队列和 lint，再考虑 API。
