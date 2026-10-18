---
type: source
record_kind: source_card
status: source-captured
title: "semantica-agi/semantica"
source_id: "vsrc:1:repo:github.com/semantica-agi/semantica"
source_uri: "git+https://github.com/semantica-agi/semantica@0d447560bc3c9a8dfa0bfb5e78d32dbe77416cd3"
source_url: "https://github.com/semantica-agi/semantica"
source_type: repository
source_identity:
  schema_version: 1
  source_id: "vsrc:1:repo:github.com/semantica-agi/semantica"
  kind: repo
  canonical_locator: "https://github.com/semantica-agi/semantica"
  identity_profile: "repo-provider-native/v1"
  aliases: []
latest_observed_capture_ref: "raw/captures/2026-08-02-semantica-agi-semantica-0d44756/capture-envelope.json"
author: "Semantica contributors / Hawksight AI"
publisher: GitHub
published_at: null
updated_at: "2026-08-01T20:52:55+05:30"
captured_at: "2026-08-02"
captured_by: Codex
version_or_commit: "0d447560bc3c9a8dfa0bfb5e78d32dbe77416cd3"
adapter_ingest:
  adapter_name: "manual-github-repository-review"
  adapter_version: "2026-08-02"
  capture_method: "git ls-remote, shallow clone, git archive, structured snapshot inspection, documentation and static source review"
  extraction_trace: "Pinned main to 0d44756; archived the exact tree; generated Source Capture Envelope v1, manifest, and hygiene statement; inspected README, architecture, package metadata, context/decision, KG builder, provenance, conflict, reasoning, ontology, temporal, MCP, CI, tests, and security files without executing repository code."
  known_limits:
    - "Repository code, tests, examples, benchmarks, services, MCP server, and packaged distribution were not executed."
    - "The large provider/backend surface was sampled around high-impact authority boundaries; this was not an exhaustive security or correctness audit."
    - "Project claims about regulation, auditability, performance, and production stability were not independently verified."
    - "Open issues, pull requests, release artifacts, PyPI wheels, and dependency advisories were not exhaustively audited."
source_status: active
raw_location: "raw/repos/_snapshots/semantica-agi-semantica-0d44756.zip"
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: review_due
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: high
review_owner: Codex
formalization_status: raw-only
why_saved: "User explicitly requested VAKS distillation of semantica-agi/semantica."
topics:
  - knowledge-graph
  - context-graph
  - decision-intelligence
  - provenance
  - reasoning
  - ontology
  - conflict-resolution
  - agent-memory
  - mcp
  - temporal-applicability
projects:
  - verified-action-knowledge-system
source_family:
  - knowledge-graph-platform
  - accountable-ai
  - agent-context
  - graph-retrieval
  - provenance-tooling
upstream_sources:
  - "https://github.com/semantica-agi/semantica"
verification_status: source_identity_checked
candidate_relation_suggestions: []
tags:
  - source
  - repository
  - semantica
  - knowledge-graph
  - candidate-only
---

# 来源记录：semantica-agi/semantica

## 为什么收录

用户明确要求蒸馏这个仓库。Semantica 把自己定位成 AI agent 下方的图原生上下文与问责基础设施，功能面覆盖：

```text
多源 ingest
-> parse / normalize / split
-> entity / relation / triplet extraction
-> dedup / conflict
-> knowledge graph
-> ontology / reasoning / provenance / decisions
-> graph / vector storage
-> REST / MCP / CLI / explorer
```

本记录只保存来源身份、固定快照与可复核入口。项目借用判断位于候选蒸馏、架构评审和 Project Overlay。

## 来源信息

- 仓库：https://github.com/semantica-agi/semantica
- 默认分支：`main`
- checked commit：`0d447560bc3c9a8dfa0bfb5e78d32dbe77416cd3`
- commit time：`2026-08-01T20:52:55+05:30`
- commit subject：`fix(provenance): log tracking failures and return None on storage error (closes #783) (#820)`
- package version：`0.6.0`
- Python：`>=3.8`
- license：MIT
- 本地快照：`raw/repos/_snapshots/semantica-agi-semantica-0d44756.zip`
- 快照 SHA256：`77A0397A7BCED20F79267AF0F69DA571DC68DCFA91C6249F1A76592B42CF86E4`
- 快照大小：`14,295,557` bytes

## Capture Envelope

```yaml
capture_id: urn:uuid:f215f345-bd8b-473b-b943-3a11f96c3dee
source_id: vsrc:1:repo:github.com/semantica-agi/semantica
resolved_revision: 0d447560bc3c9a8dfa0bfb5e78d32dbe77416cd3
snapshot_id: vsnap:1:tree:sha256:b8b3a0e1ce0a80e7aa8e9b0f29c7f25267f0bde6216d6f5f5041d07e6dc366f3
snapshot_manifest_digest: sha256:b8b3a0e1ce0a80e7aa8e9b0f29c7f25267f0bde6216d6f5f5041d07e6dc366f3
archive_digest: sha256:77a0397a7bced20f79267af0f69da571dc68dcfa91c6249f1a76592b42cf86e4
raw_disposition: admitted
hygiene_findings: 0
fidelity: not_checked
```

`hygiene_findings: 0` 只表示静态快照检查器未发现其规则能检测到的问题，不代表代码安全、功能正确、依赖可信或宣传成立。

## Intake Boundary

```yaml
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: review_due
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

This source record is provenance and findability only. It does not adopt the
library, validate its compliance claims, approve graph writes, or turn
extracted facts, rules, decisions, provenance links, or graph relations into
reviewed knowledge.

## 初步看点

- 有完整的 source-to-graph 工具箱，而不只是一个向量检索包装。
- Decision 记录形状、双时间字段、推理 premise/rule/conclusion 回执、SHACL 路径和冲突对象都值得做候选参考。
- 图、三元组、向量和多种 provider/backend 被统一到一套 Python 包与 CLI/MCP 表面。
- 代码中存在真实实现、薄适配、启发式和占位实现混在同一宣传层级的情况。

## 明显疑点

- README 宣称 KG 构建可完全确定性运行，但原始文本建图默认使用 LLM 做 NER、关系和三元组抽取。
- GraphBuilder 先构图并写 GraphStore，后检测冲突；其内置 resolve 路径只统计，没有回写。
- Decision reasoning/confidence/causal edge 主要由调用方声明；另一路因果追踪把共享实体和时间先后当影响线索。
- Decision provenance 接线缺必填 `source` 且调用不存在的 `track_activity`，失败只记录日志。
- Rete 的 alpha matcher 与 beta join 当前无条件返回 True。
- OntologyValidator 的一致性和可满足性检查是 placeholder，只有独立 pySHACL 路径是真校验。
- 默认 MCP 直接暴露 add entity、add relationship、record decision，没有 VAKS 式 authority bucket、approval 或 operation receipt。
- 包标为 Production/Stable，但主 CI 只构建前端和 wheel，不运行仓库的 pytest 套件。
- 默认依赖包含 torch、transformers、spaCy、OpenCV、FAISS、绘图库等，作为 VAKS 核心依赖过重。

## Source Annotation Sidecars

```yaml
source_annotation_refs:
  - ann-semantica-001-default-llm-extraction
  - ann-semantica-002-conflict-after-persistence
  - ann-semantica-003-declared-and-heuristic-causality
  - ann-semantica-004-decision-provenance-wiring-gap
  - ann-semantica-005-provenance-integrity-boundary
  - ann-semantica-006-rete-unconditional-matches
  - ann-semantica-007-ontology-validator-placeholder
  - ann-semantica-008-bitemporal-normalization
  - ann-semantica-009-agent-mcp-direct-write
  - ann-semantica-010-ci-build-only
```

这些注释是源码定位器与 review input，不是 evidence support、缺陷裁决或采用决定。

## 下一步

本源卡只负责来源身份、快照与复核入口。候选理解见 `outputs/review/2026-08-02-semantica-agi-semantica-candidate-distillation.md`；项目范围判断见对应 Project Overlay；架构采用判断见 library review。这里不承载采用、拒绝或 promotion 结论。
