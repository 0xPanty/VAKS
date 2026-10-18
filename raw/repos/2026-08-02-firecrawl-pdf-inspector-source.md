---
type: source
record_kind: source_card
status: source-captured
title: "firecrawl/pdf-inspector"
source_id: "vsrc:1:repo:github.com/firecrawl/pdf-inspector"
source_uri: "git+https://github.com/firecrawl/pdf-inspector@a15ec2d68d51dbe6a39d1da688ec7a3f642d846c"
source_url: "https://github.com/firecrawl/pdf-inspector"
source_type: repository
source_identity:
  schema_version: 1
  source_id: "vsrc:1:repo:github.com/firecrawl/pdf-inspector"
  kind: repo
  canonical_locator: "https://github.com/firecrawl/pdf-inspector"
  identity_profile: "github-owner-repository"
  aliases: []
latest_observed_capture_ref: "raw/captures/2026-08-02-firecrawl-pdf-inspector-a15ec2d/capture-envelope.json"
author: "Firecrawl Team"
publisher: GitHub
published_at: null
updated_at: "2026-07-31T22:58:46-06:00"
captured_at: "2026-08-02"
captured_by: Codex
version_or_commit: "a15ec2d68d51dbe6a39d1da688ec7a3f642d846c"
adapter_ingest:
  adapter_name: "manual-github-repository-review"
  adapter_version: "2026-08-02"
  capture_method: "git ls-remote, shallow clone, git archive, structured snapshot inspection, source and documentation reads"
  extraction_trace: "Pinned main to a15ec2d; archived exact tree; generated Source Capture Envelope v1, manifest, and hygiene statement; inspected Rust core, bindings, docs, CI, tests, and benchmark scripts without executing repository code."
  known_limits:
    - "Repository code, tests, benchmark, and packaged bindings were not executed."
    - "Published benchmark results were inspected as project-produced diagnostics, not independently reproduced."
    - "Open issues, pull requests, release artifacts, and dependency advisories were not exhaustively audited."
    - "Static source review cannot prove parser safety or extraction completeness on adversarial PDFs."
source_status: active
raw_location: "raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip"
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
review_priority: normal
review_owner: Codex
formalization_status: raw-only
why_saved: "User explicitly requested VAKS distillation of firecrawl/pdf-inspector."
topics: "[pdf-classification, native-text-extraction, markdown-conversion, layout-analysis, table-recovery, ocr-routing, rust, source-intake]"
projects: "[verified-action-knowledge-system]"
source_family: "[pdf-parser, document-intake-adapter, transformed-evidence, local-extraction]"
upstream_sources: "[https://github.com/firecrawl/pdf-inspector]"
verification_status: source_identity_checked
candidate_relation_suggestions: []
tags: "[source, repository, pdf-inspector, firecrawl, pdf, candidate-only]"
---

# 来源记录：firecrawl/pdf-inspector

## 为什么收录

用户明确要求蒸馏这个仓库。它是一个 Rust PDF 预检与原生文本提取库，核心表面包括：

```text
PDF 类型分类
-> 带位置的文本提取
-> 布局 / 表格恢复
-> Markdown 转换
-> 页级 OCR 路由信号
-> Rust / Python / Node / WASM 绑定
```

本记录只保存来源身份、快照和可复核入口。项目借用结论位于单独的候选蒸馏、架构评审与 Project Overlay 中。

## 来源信息

- 作者/组织：Firecrawl Team
- 发布方：GitHub
- 原始链接：https://github.com/firecrawl/pdf-inspector
- 默认分支：`main`
- checked commit：`a15ec2d68d51dbe6a39d1da688ec7a3f642d846c`
- commit time：`2026-07-31T22:58:46-06:00`
- commit subject：`docs(readme): refresh local parser benchmark results (#192)`
- Rust crate version：`0.1.7`
- Python package version：`0.2.6`
- npm package version：`1.11.2`
- license：MIT
- 本地快照：`raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip`
- 快照 SHA256：`A15AE3C5CB4A290F6FA594A690AC3D3FA6E7B0473E7F7A1A962172B04A01A815`
- 快照大小：`10,839,586` bytes

## Capture Envelope

```yaml
capture_id: urn:uuid:b8737c02-2e7b-4dc9-9385-feb1a871d843
source_id: vsrc:1:repo:github.com/firecrawl/pdf-inspector
resolved_revision: a15ec2d68d51dbe6a39d1da688ec7a3f642d846c
snapshot_id: vsnap:1:tree:sha256:d0413ccef08d6bf3baa63a75994b7d71e7a9a942569a3f126fc5157639867e79
snapshot_manifest_digest: sha256:d0413ccef08d6bf3baa63a75994b7d71e7a9a942569a3f126fc5157639867e79
archive_digest: sha256:a15ae3c5cb4a290f6fa594a690ac3d3fa6e7b0473e7f7a1a962172b04a01a815
raw_disposition: admitted
hygiene_findings: 0
fidelity: not_checked
```

`hygiene_findings: 0` 只表示当前静态快照检查器没有发现其规则能检测到的问题，不代表代码安全、运行正确、依赖可信或输出完整。

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
library, validate its benchmark, verify runtime safety, or turn parser output
into evidence support.

## 时间线 / 上下文

- 观察时点：2026-08-02。
- 固定版本：`main` 在采集时指向 `a15ec2d`。
- 上游在该提交刚刷新了本地解析器基准说明。
- 仓库包含持续集成、四类发布流程和大量静态测试定义；本次没有执行任何一项。

## 初步看点

- 分类与提取共享一次 PDF 解析。
- 保留页号、坐标、字体、样式与 MCID 等位置化信息。
- 对乱码、CID/ToUnicode 问题、空提取和复杂布局给出 OCR 路由信号。
- 表格恢复组合 structure tree、矩形、线段、文本启发式与区域 TSR 接口。
- benchmark harness 同时检查整体回归、缺失预测和单文档最坏回归。

## 明显疑点

- README 声称默认 `EarlyExit`，源码默认却是 `Sample(8)`。
- 分类 `confidence` 来自规则常数/公式，不是经过校准的概率。
- 默认 Markdown 会删页码、页眉页脚并忽略图片，是有损派生物。
- 某些 per-page API 的布局元数据路径与 Markdown 渲染路径不完全一致。
- Rust、Python、npm 版本号独立变化，接入时需要锁定具体生态包和 commit。
- 公共 API 具有若干局部复杂度上限，但没有统一的调用级文件大小、页数、时间和内存预算。

## 可抽取 Candidate Points

候选提取已写入：

`outputs/review/2026-08-02-firecrawl-pdf-inspector-candidate-distillation.md`

## Source Annotation Sidecars

```yaml
source_annotation_refs:
  - ann-pdf-inspector-001-sampled-routing-gap
  - ann-pdf-inspector-002-single-load-positioned-extraction
  - ann-pdf-inspector-003-text-quality-ocr-reasons
  - ann-pdf-inspector-004-multi-hypothesis-tables
  - ann-pdf-inspector-005-lossy-markdown
  - ann-pdf-inspector-006-region-tsr-hybrid
  - ann-pdf-inspector-007-per-page-contract-drift
  - ann-pdf-inspector-008-benchmark-diagnostic-gates
  - ann-pdf-inspector-009-runtime-package-boundaries
```

这些注释只是源码定位器与 review input，不是证据支持或项目结论。

## 下一步

若未来启动 PDF adapter sandbox，再用本地真实语料做一次受控微评测；在此之前不安装、不接入正式 intake，也不创建 reviewed pattern/decision。
