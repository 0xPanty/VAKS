---
type: source
record_kind: source_card
status: source-captured
title: "VectifyAI/OpenKB"
source_url: "https://github.com/VectifyAI/OpenKB"
source_type: repo
author: "VectifyAI / PageIndex contributors"
publisher: GitHub
published_at:
captured_at: 2026-05-27
captured_by: Codex
topics:
  - llm-wiki
  - knowledge-base
  - pageindex
  - skill-factory
  - agent-context
projects:
  - verified-knowledge-system
evidence_level: primary
source_integrity:
  capture_confidence: 4
source_status: source-captured
verified_by: Codex source review
last_verified: 2026-05-27
next_review: 2026-06-03
related_claims:
related_concepts:
  - "[[2026-05-27-openkb-architecture-review]]"
  - "[[wiki-foundation-generator-surface-separation]]"
  - "[[long-document-tree-index-source-adapter]]"
  - "[[knowledge-to-agent-skill-factory]]"
  - "[[path-scoped-agent-output-writes]]"
  - "[[ghost-wikilink-whitelist-before-write]]"
  - "[[source-hash-registry-and-idempotent-ingest]]"
  - "[[url-source-ingest-normalization]]"
  - "[[removal-cleanup-with-registry-commit-point]]"
  - "[[artifact-trigger-and-body-alignment-eval]]"
  - "[[skill-artifact-iteration-workspace-rollback]]"
candidate_relation_suggestions:
  - target: "[[2026-05-27-openkb-architecture-review]]"
    type: derived_from
    strength: 5
    confidence: high
    evidence:
      - "[[2026-05-27-openkb-source]]"
    rationale: "The architecture review is based on README and source-code inspection of OpenKB."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[2026-05-27-openkb-as-module-reference]]"
    type: supports
    strength: 4
    confidence: high
    evidence:
      - "[[2026-05-27-openkb-source]]"
    rationale: "OpenKB provides useful module contracts but does not replace the verified truth schema."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - source/repo
  - openkb
  - llm-wiki
  - pageindex
  - skill-factory
knowledge_status: raw
processing_tier: light
source_id: "https://github.com/VectifyAI/OpenKB"
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
# 来源记录：VectifyAI/OpenKB

## 为什么收录

OpenKB 是一个和本资料库主线高度接近的开源实现：它把 raw documents 编译成 Markdown wiki，再让 query/chat/Skill Factory 从 wiki 产生输出。

它对我们有两个价值：

1. 验证 Karpathy LLM Wiki 路线正在被工程化。
2. 提供几个可直接借鉴的实现模块：长文档树索引、wiki foundation/generator 分层、agent 工具权限隔离、skill 输出工厂。

## 核心内容

OpenKB 的公开定位是：用 LLM 把原始文档编译成结构化、互链的 wiki-style knowledge base，并用 PageIndex 支持无向量数据库的长文档检索。

源码显示它的实际结构是：

```text
raw/
-> convert_document / url_ingest
-> short doc: markitdown / pymupdf
-> long PDF: PageIndex tree + per-page JSON
-> wiki/sources
-> wiki/summaries
-> wiki/concepts
-> wiki/index.md + log.md
-> query / chat / skill factory / lint
```

## 来源信息

- 作者：VectifyAI / PageIndex contributors
- 发布方：GitHub
- 发布时间：未在 README 中明确
- 原始链接：https://github.com/VectifyAI/OpenKB
- 采集方式：GitHub README + source snapshot + local source review
- 采集提交：`5e8119613758a73d597dfc6deeb91c02052b2d32`
- 本地快照：`raw/repos/_snapshots/openkb-main-2026-05-27.zip`
- 临时解压：`C:\Users\Administrator\AppData\Local\Temp\openkb_probe\OpenKB-main`

## 标签与量化

- source_type: repo
- evidence_level: primary
- source_status: source-captured
- source_quality: 4
- freshness: 5
- relevance: 5
- confidence: 4
- cross_source_count: 1

## 已验证内容

- `pyproject.toml` 显示 OpenKB 是 Python CLI 包，命令入口为 `openkb = "openkb.cli:cli"`，依赖 PageIndex、markitdown、trafilatura、LiteLLM、openai-agents、watchdog、rich 等。
- `README.md` 明确把系统分为 wiki foundation 和 generators 两层。
- `openkb/schema.py` 定义默认 `AGENTS.md`，包含 `sources/`、`summaries/`、`concepts/`、`explorations/`、`reports/`、`index.md`、`log.md`。
- `openkb/converter.py` 用 SHA-256 registry 去重，把源文件复制到 `raw/`，短文档转 Markdown，长 PDF 交给 PageIndex。
- `openkb/indexer.py` 对长 PDF 建 PageIndex，并写出 `wiki/sources/<doc>.json` 与 `wiki/summaries/<doc>.md`。
- `openkb/agent/compiler.py` 使用 summary -> concept plan -> create/update/related -> backlink -> index update 的编译链路。
- `openkb/lint.py` 提供 broken links、orphans、raw without wiki entry、index sync 等结构检查，并有 ghost wikilink stripping。
- `openkb/agent/query.py` 构建 query/chat agent，按 index -> summaries -> concepts -> source page slices 的顺序读取。
- `openkb/agent/tools.py` 对读写工具做路径约束，chat 写入限制在 `wiki/explorations/**` 和 `output/**`。
- `openkb/skill/*` 实现 skill factory、validator、evaluator、workspace、rollback、marketplace manifest。

## 未验证内容

- 未实际安装运行 OpenKB。
- 未验证 PageIndex 在大 PDF 上的实际质量和成本。
- 未验证 Skill Factory 生成结果在 Codex/Claude/Gemini/Cursor 中的真实触发效果。
- 未验证当前 README 对所有 CLI 行为是否完全同步。

## 冲突或疑点

- OpenKB 默认把 LLM 编译结果直接写入 `wiki/concepts/`，这适合普通 LLM Wiki，但不适合本资料库 formal truth layer。
- 它的核心 schema 是 `summary / concept / exploration`，缺少本资料库需要的 `claim / pattern / anti-pattern / decision / actionability`。
- 它有 semantic lint，但没有把 claim-level verification、negative evidence、decision rollback、relation strength 作为核心契约。
- `watch` 自动编译对本资料库 v0.1 来说应默认禁用，最多作为候选队列输入。

## 可复用点

- 长文档源适配器：PageIndex tree + per-page JSON + targeted page slice。
- wiki foundation / generator surface 分层：知识底座和输出生成器分离。
- Skill Factory：把 verified knowledge 编译成可分发 agent skill。
- path-scoped tools：agent 可读 wiki，但写入只能落到 explorations/output。
- ghost wikilink whitelist：LLM 写入前只允许已存在或本轮计划产生的链接。
- remove pipeline：删除文档时同步清理 summaries、sources、concept sources、index、PageIndex state，并设置 registry commit point。

## 下一步

- 不直接采用 OpenKB schema。
- 将它作为 `IMPLEMENTATION_BLUEPRINT.md` 的候选实现参考。
- 优先吸收：long document adapter、generator surface、skill factory、path-scoped write tools、ghost wikilink lint。
- 避免吸收：unreviewed concept auto-update、watch auto-compile into truth layer。
