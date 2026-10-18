---
record_kind: candidate_distillation
status: candidate
provisional: true
title: "pdf-inspector：VAKS 原生 PDF 预检、逐页 OCR 路由与位置化提取候选"
created_at: "2026-08-02"
created_by: Codex
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
source_ref: "raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md"
derived_from: "[raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md, raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip, raw/captures/2026-08-02-firecrawl-pdf-inspector-a15ec2d/capture-envelope.json, wiki/summaries/2026-08-02-firecrawl-pdf-inspector-architecture-review.md, outputs/review/project_overlays/VAKS/VAKS-firecrawl-pdf-inspector-2026-08-02.md]"
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint: "[pdf-intake, native-text-first, page-level-ocr-routing, positioned-text, table-recovery, parser-evaluation]"
possible_project_refs: "[verified-action-knowledge-system]"
source_annotation_refs: "[ann-pdf-inspector-001-sampled-routing-gap, ann-pdf-inspector-002-single-load-positioned-extraction, ann-pdf-inspector-003-text-quality-ocr-reasons, ann-pdf-inspector-004-multi-hypothesis-tables, ann-pdf-inspector-005-lossy-markdown, ann-pdf-inspector-006-region-tsr-hybrid, ann-pdf-inspector-007-per-page-contract-drift, ann-pdf-inspector-008-benchmark-diagnostic-gates, ann-pdf-inspector-009-runtime-package-boundaries]"
point_anchor_refs: "[src/detector.rs:80-88, src/detector.rs:184-477, src/lib.rs:3558-3874, src/markdown/mod.rs:1247-1402, src/markdown/convert.rs:520-625, docs/benchmarking.md:3-62]"
borrow_value: medium-high
borrow_order: "P1 explicit Full/per-page routing and receipts; P2 positioned extraction and one normalized adapter; P3 region/TSR hybrid and paired evaluation"
avoid: "sampled confidence as completeness; Markdown as original evidence; implicit cross-page table identity; in-process parsing of untrusted PDFs without host budgets; direct binding leakage"
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "the task is specifically about PDF source intake, document_parse routing, OCR escalation, positioned source anchors, or parser evaluation"
  support_when: "designing a PDF adapter sandbox, mixed native/OCR page pipeline, table extraction, or retained extraction bundle"
  risk_when: "someone proposes treating parser Markdown, bbox text, confidence, benchmark scores, or needs_ocr=false as reviewed evidence or completeness proof"
  cold_references: "raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md; raw/repos/_snapshots/firecrawl-pdf-inspector-a15ec2d.zip"
tags: "[candidate, provisional, pdf-inspector, pdf-intake, ocr-routing, positioned-text, transformed-evidence, candidate-only]"
---

# 候选蒸馏：firecrawl/pdf-inspector

## Boundary

这是 heavy intake 产生的候选理解，不是 reviewed knowledge、架构决定、依赖采用批准或 action basis。

仓库代码、测试和 benchmark 均未在本机执行。所有运行时与质量结论都必须在未来 sandbox 中重新验证。

## 说人话

`pdf-inspector` 最准确的定位不是“OCR 库”，而是：

```text
PDF 原生文本预检器
+ 位置化提取器
+ 布局 / 表格恢复器
+ 外部 OCR 的页级/区域级路由器
```

它最适合插在现有 PDF intake 的前半段：先尝试低成本原生提取，只把真正异常的页或区域交给 PaddleOCR 等重型路线。

一句话判断：

```text
adapt / candidate-only
值得进入 PDF adapter sandbox
不值得现在进入正式 mainline，更不能成为证据权威
```

## 直接评分

| 维度 | 分数 | 判断 |
|---|---:|---|
| 原生文本 PDF 预检 | 8/10 | 分类、位置项、乱码检测和页级 reason code 组合完整。 |
| 混合 PDF OCR 路由 | 7/10 | 思路很好，但默认抽样会留下漏页风险，需显式 `Full`/全页路径。 |
| 布局与表格恢复参考 | 8/10 | 多假设探测、质量拒绝和区域 TSR seam 很值得借。 |
| VAKS evidence/provenance 直接适配 | 4/10 | 有 page/x/y/MCID，但默认 Markdown 有损，且输出仍是 transformed evidence。 |
| 不受信 PDF 的生产安全 | 4/10 | 有局部 cap，但缺统一 bytes/pages/time/memory/output 预算与隔离证明。 |
| 直接拿来用 | 3/10 | 文档/代码、API/绑定和版本线存在漂移，需要单一适配层与本地包级测试。 |

## Candidate Point 1：抽样分类是路由信号，不是文档完整性

源码默认：

```rust
strategy: ScanStrategy::Sample(8)
```

而 README 仍写默认 `EarlyExit`。更重要的是，当抽样结果把文档判成 `TextBased` 时，`pages_needing_ocr` 初始为空；未抽样页的补查主要针对字体解码故障，并不会完整补查所有图像页。

源码锚点：

- `src/detector.rs:80-88`
- `src/detector.rs:184-334`
- `src/detector.rs:379-445`
- `README.md:215-231`

VAKS 可借：

```text
cheap classification as lazy gate
+ page-level reason codes
+ explicit escalation
```

VAKS 不可借：

```text
confidence = calibrated probability
TextBased = every page extractable
empty pages_needing_ocr = complete coverage
```

重要 intake 应显式用 `Full` 或直接采用真正全页的 per-page 路径，并记录调用配置。

## Candidate Point 2：一次解析 + 位置项 + 质量回执是最实用的核心

核心 pipeline 在一个已加载的 `Document` 上完成检测、提取和 Markdown，避免重复解析：

- `src/lib.rs:3558-3640`

`TextItem` 保存：

```text
text
page
x / y / width / height
font / font_size
bold / italic / underline / strikeout
item_type
mcid
```

锚点：`src/types.rs:96-132`。

这对 VAKS 的真正价值不是“更漂亮的 Markdown”，而是能形成可审计的 retained extraction bundle：

```yaml
original_pdf_ref:
original_sha256:
adapter_commit:
distribution:
distribution_version:
binary_sha256:
config:
page_markdown:
positioned_items:
pages_needing_ocr:
ocr_reasons_by_page:
warnings:
```

这些字段仍然是提取回执与 review input，不是 evidence support。

## Candidate Point 3：它只做 OCR 路由，不做 OCR

扫描型或图片型 PDF 会返回 `markdown: None`，代码依赖中没有 OCR/VLM 模型：

- `src/lib.rs:3589-3602`
- `Cargo.toml:28-57`

reason code 能区分扫描、无文本、矢量轮廓文字、疑似乱码等情况。正确融合应是：

```text
native extraction
-> page/region quality receipt
-> selected pages/regions to PaddleOCR or another OCR adapter
-> preserve both original and transformed artifacts
-> candidate only
```

渲染、OCR、拼接、冲突处理、原页锚定都仍是调用方责任。

## Candidate Point 4：多假设表格恢复值得借，但不能自动变成语义结构

完整 Markdown 路径大致按以下顺序寻找表格：

```text
tagged structure tree
-> rectangles
-> ruled lines
-> rect-guided reconstruction
-> text heuristic
```

锚点：`src/markdown/mod.rs:1247-1402`。

区域 API 又同时比较 rect、line、heuristic、column、key-value 候选，并在结构欠计数时切换候选或要求 OCR：

- `src/lib.rs:4010-4108`

这可以蒸馏成一个候选实现原则：

```text
multiple extraction hypotheses
-> explicit issue flags
-> reject tidy-looking fragments
-> fallback with reason
```

但几何上像表格不等于语义表格已确认；任何表格输出仍需保留原页、bbox、行列身份与转换轨迹。

## Candidate Point 5：Markdown 是有损 activation artifact

默认 Markdown 配置会：

```text
remove standalone page numbers
omit page markers
strip repeated headers/footers
omit images
```

锚点：`src/markdown/mod.rs:848-907`。

即使开启图片，也只生成 `![Image: name](image)` 占位。跨页表格合并还只依赖连续页、单表、列数相同和 table-only 等启发式：

- `src/markdown/convert.rs:520-625`
- `src/markdown/mod.rs:1584-1599`
- `src/markdown/mod.rs:1644-1655`

所以它适合：

```text
retrieval
activation
token-efficient context
candidate comprehension
```

不适合：

```text
replace original PDF
serve as the only retained text
stand alone as evidence support
prove no page/table content was omitted
```

这与现有 `transformed-evidence-as-original-source` anti-pattern 完全一致，不需要创建新正式 pattern。

## Candidate Point 6：region + TSR + native text 是最强扩展 seam

仓库可以接受外部 table-structure model 的 structure tokens 和 cell bbox，再用 PDF 原生文本填充单元格：

- `src/lib.rs:2040-2087`
- `src/lib.rs:2995-3094`

这与 PaddleOCR 是互补关系：

```text
layout / TSR model: where and what structure
pdf-inspector: native text inside cells
OCR: only where native text is absent or unreliable
```

值得借的是混合边界与 `fallback_reason`，不是 SLANet 特定修复。旋转页、检测错误和 heuristic empty 都仍有保留原始 TSR Markdown 的降级路径，不能当作质量已通过。

## Candidate Point 7：公共 API 需要 VAKS 自己的归一化 adapter

两个高风险契约漂移：

1. per-page API 用完整 items/rects/lines 算布局元数据，却在单页 Markdown 渲染时把 `pdf_lines`、structure roles、tagged tables 传空：`src/lib.rs:457-576` 与 `src/lib.rs:5508-5585`。
2. 页号和坐标契约混合 0-indexed / 1-indexed、top-left / bottom-left；Rust、Python、Node、WASM 暴露能力也不同。

结果可能出现：

```text
metadata says table
but markdown path did not use the same line/tagged-table evidence
```

如果 pilot，只允许一个 VAKS adapter 向上暴露统一 schema：

```yaml
page_index_base: 1
coordinate_origin: top_left | bottom_left
coordinate_unit: pdf_point
detector_strategy:
result_semantics:
warning_codes:
adapter_distribution:
adapter_version:
adapter_commit:
```

不要让上层直接依赖四套绑定。

## Candidate Point 8：paired benchmark 的方法比排行榜更值得借

仓库的 paired harness 强制 baseline 和 candidate 使用同一 corpus/evaluator，并检查：

```text
overall delta
missing predictions
worst per-document regression
optional reference lead
```

锚点：

- `docs/benchmarking.md:3-29`
- `scripts/bench_opendataloader.py:64-167`

MuPDF evidence probe 也明确把 backend disagreement 当作“需要检查”的信号，而不是自动把 alternate 当正确：

- `docs/benchmarking.md:42-62`
- `scripts/probe_backend_evidence.py:171-212`

这是 VAKS 可以借的维护诊断形状：

```text
same fixture envelope
-> candidate vs baseline
-> aggregate + worst-case deltas
-> disagreement creates review pressure
-> no automatic truth/readiness promotion
```

README 的公开结果只覆盖 200 份 PDF、OCR 关闭、Apple M4 Pro、单进程顺序运行。NID/TEDS/MHS 和速度不是语义完整性、引用忠实度、安全或跨平台证明。

## Candidate Point 9：生产接入必须加外层资源与供应链边界

源码已有局部防护：

- content operations 上限 1,000,000：`src/extractor/content_stream.rs:233-254`
- structure tree 深度 64：`src/structure_tree.rs:478-491`
- Form XObject 深度 5：`src/extractor/xobjects.rs:16,271-289`
- rect cluster cap 2000：`src/tables/detect_rects.rs:81-119`

但入口只验证前 1024 字节是否有 `%PDF-`，随后把整个文件读入内存：

- `src/lib.rs:3392-3450`
- `src/lib.rs:5746-5772`

因此未来生产 pilot 必须由宿主额外提供：

```text
max input bytes
max pages
max decoded/output bytes
CPU / wall-clock timeout
memory limit
isolated worker process
killable job
dependency audit
malicious/corrupt corpus
```

另外，Rust/Python/Node/WASM 分别有独立版本线；记录版本时必须写 `distribution + version + commit + binary hash`。bundled Adobe CMap 还有独立许可文本，最终分发包需做第三方 notice 核验。

## 与现有 VAKS 去重

| 现有来源/设计 | 已覆盖 | 本库新增 | 结论 |
|---|---|---|---|
| PaddleOCR | 普通提取后按需升级 OCR/结构化/VL | 提供更具体的轻量 native-text backend 与页级 reason | 互补，不替代 |
| OmniParse | parser router、retained bundle、quarantine | 更窄、更轻的 PDF backend | 不再造 router |
| OpenKB / long-doc adapter | 长文档树索引和 page windows | 提供 page Markdown / positioned items 输入 | 前后级组合 |
| linXiv | 论文获取、source identity、source adapter | 下载后的 PDF 内容预检/解析 | 不替代身份采集 |
| transformed evidence guard | OCR/layout/bbox/table 输出不是原始支持 | 坐标提高可恢复性 | 边界不变 |
| raw intake parser-router sandbox | lazy route、retained bundle、candidate | 可作为真实 PDF pilot implementation | 不是新 contract |

因此：

```text
不新增正式 pattern
不改 SCHEMA.md
不新增 parser lane
只建 Project Overlay + candidate records
```

## 最小融合草图

```text
Original PDF + SHA256
-> isolated VAKS PDF adapter
-> pdf-inspector with explicit Full/per-page configuration
-> retain positioned items + page markdown + warnings + binary/config receipt
-> native-text pages continue
-> suspicious pages/regions -> PaddleOCR
-> optional long-document tree index
-> source card / candidate only
-> original page/bbox required before evidence use
```

## 明确不借

```text
sampled confidence as completeness/truth
needs_ocr=false as no-omission guarantee
default Markdown as original or only retained text
automatic cross-page table merge as confirmed table identity
README benchmark as universal production proof
in-process parsing of untrusted PDFs without budgets
all four bindings at once
SLANet-specific repairs as VAKS core
parser output directly into reviewed knowledge or action basis
```

## Open Questions / Reopen Gate

只有同时满足以下条件才值得重开“正式接入”讨论：

1. 建立中文、英文、混合扫描、表格、长论文、加密/损坏 PDF 的代表集与失败集。
2. 对已发布 wheel/CLI 做包级 smoke，而不只在源码 checkout 测试。
3. 验证 `Full`/per-page 路由的漏路由与错路由阈值。
4. 与当前 MarkItDown/PaddleOCR 路线比较遗漏、阅读顺序、表格、锚点和资源曲线。
5. 宿主完成 bytes/pages/time/memory/output cap 与隔离进程。
6. 核验 CMap 打包、第三方 notice、依赖审计和实际 Windows 目标。

## Forbidden

```text
reviewed truth
truth confidence
reviewed relation
automatic promotion
action basis
dependency adoption approval
benchmark-driven mainline readiness
```
