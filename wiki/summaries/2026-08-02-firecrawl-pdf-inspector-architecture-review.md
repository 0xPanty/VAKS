---
type: library_review
status: draft
title: "firecrawl/pdf-inspector architecture review for VAKS PDF intake"
library_name: "pdf-inspector"
repo_url: "https://github.com/firecrawl/pdf-inspector"
source_url: "raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md"
checked_commit: "a15ec2d68d51dbe6a39d1da688ec7a3f642d846c"
commit_time: "2026-07-31T22:58:46-06:00"
source_status: active
reviewed_at: "2026-08-02"
domain: "PDF classification, native text extraction, layout/table recovery, Markdown conversion, OCR routing"
related_projects: "[verified-action-knowledge-system]"
current_branch: "document_parse intake route, transformed extraction bundle, page-level OCR escalation, parser evaluation"
extracted_patterns: "[native-text-first routing, positioned extraction receipt, multi-hypothesis table recovery, page-level OCR reasons, paired parser regression gate]"
fusion_decision: adapt-design-only
confidence: medium-high
inspection_confidence: medium-high
evidence_count: 34
cross_validated_with: "[SOURCE_INTAKE.md, REFERENCE_REVIEW_PROTOCOL.md, wiki/anti-patterns/transformed-evidence-as-original-source.md, wiki/summaries/2026-06-11-PaddlePaddle-PaddleOCR-architecture-review.md, wiki/summaries/2026-06-14-adithya-s-k-omniparse-architecture-review.md, wiki/summaries/2026-06-23-linxiv-dev-linXiv-architecture-review.md]"
negative_evidence: "[default Sample(8) contradicts README default EarlyExit, sampled OCR page list is not complete-document proof, lossy Markdown defaults, per-page metadata/rendering divergence, no execution in this review, incomplete global resource budgets, binding/version/package drift]"
extension_potential: "High for a sandboxed PDF adapter; low for VAKS truth/review/action layers."
knowledge_status: candidate
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: architecture_review_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
tags: "[summary, library-review, pdf-inspector, pdf-intake, parser-router, ocr-routing, candidate-only]"
---

# 库分析：firecrawl/pdf-inspector

## 一句话判断

`pdf-inspector` 是现有 VAKS `document_parse` 路由的一个强实现候选，不是新的系统架构点：

```text
native PDF text first
-> per-page quality/routing signals
-> OCR only where needed
-> retained transformed artifacts
-> candidate/review boundary unchanged
```

当前判断：

```text
adapt-design-only
candidate-only
pilot later
mainline no
authority no
```

## 它解决什么问题

它解决的是 PDF intake 中三个紧密相连的问题：

1. 这份 PDF 是原生文本、扫描、图片型还是混合型？
2. 哪些页/区域可以低成本抽取，哪些应升级 OCR？
3. 如何把 PDF 操作符、字体、坐标、布局和表格转换成可检索 Markdown？

它不解决：

```text
OCR/VLM execution
source identity acquisition
evidence support review
truth confidence
reviewed relations
action authorization
long-document navigation tree
```

## 核心设计

```text
PDF bytes
-> validate magic / load lopdf Document
-> detect text/image/font/layout signals
-> extract positioned TextItems
-> decode fonts / ToUnicode / XObjects / links / form fields
-> detect columns and reading order
-> recover tables through multiple hypotheses
-> convert to Markdown
-> emit page-level OCR needs and reasons
```

高级 seam：

```text
external layout / TSR model
-> region or cell bboxes
-> pdf-inspector fills cells with native PDF text
-> quality issue / fallback reason
-> external OCR remains separate
```

## Source / Code Anchors

| Anchor | 观察 | VAKS 含义 |
|---|---|---|
| `src/detector.rs:80-88` | 默认 `Sample(8)` | 默认分类不是全页完整性检查。 |
| `README.md:215-231` | 文档仍写默认 `EarlyExit` | 接入必须记录实际配置，不能依赖文档默认。 |
| `src/detector.rs:184-477` | 规则式分类、页级 OCR 列表与原因 | 适合 lazy routing；confidence 不是校准概率。 |
| `src/lib.rs:3558-3874` | 单次加载的 detect/extract/quality pipeline | 可借 single-parse + explicit receipt。 |
| `src/types.rs:96-132` | TextItem 带 page/x/y/size/font/MCID | 可用于 source selector，但仍是派生定位。 |
| `src/text_quality.rs:1-25,250-300` | 多类乱码/解码失败检测 | 适合 warning/review pressure，不是语义正确证明。 |
| `src/markdown/mod.rs:1247-1402` | structure/rect/line/guided/heuristic 多路径表格 | 借多假设与 fallback，不借自动语义确认。 |
| `src/lib.rs:4010-4108` | table candidate issue 与候选切换 | 拒绝 tidy-looking fragment 的思路有价值。 |
| `src/markdown/mod.rs:848-907` | 默认删页码、页眉页脚、图片、page marker | Markdown 是有损 activation artifact。 |
| `src/markdown/convert.rs:520-625` | 跨页表格启发式合并 | 必须保留原页映射与合并 warning。 |
| `src/lib.rs:2040-2087` | 外部 TSR + 原生文本填充 | 与 PaddleOCR 互补的最强 extension seam。 |
| `src/lib.rs:457-576,5508-5585` | per-page 元数据和渲染使用的 table evidence 不同 | 需要 adapter 归一化和本地 fixture。 |
| `docs/benchmarking.md:3-62` | paired harness 与 alternate evidence probe | 适合作为维护诊断，不是 readiness/truth。 |
| `src/lib.rs:3392-3450,5746-5772` | 整文件读入；入口只做 magic 检查 | 不受信 PDF 需外层资源预算和隔离。 |

## 当前支线价值

### 1. document_parse / PDF adapter

当前 VAKS 已有 parser router 和 source-adapter contract。`pdf-inspector` 可以成为其中一个实现：

```text
route_kind: document_parse
adapter_kind: native_pdf_text
source_of_truth: original PDF
output_status: transformed_candidate
```

它补的是“普通 PDF 解析 first”这一格，不应新建 formal lane。

### 2. PaddleOCR 前置路由

与 PaddleOCR 的关系：

```text
pdf-inspector = cheap native path + failure locator
PaddleOCR      = scanned/complex page or region escalation
```

它不能替代 OCR；它能减少不必要的 OCR，并把升级范围缩小到页/区域。

### 3. source annotation / evidence landing

位置项使下游能够保留：

```text
page
bbox
font/style
MCID when present
```

但这只提升“回到原页”的能力。真正 evidence use 仍须：

```text
original PDF hash
original page or region
transformation trace
evidence support check
```

### 4. parser maintenance diagnostics

paired harness 的价值是把“平均分更好”拆成：

```text
same corpus/evaluator
aggregate delta
missing outputs
worst document regression
reference comparison
```

这可进入未来 adapter maintenance manifest，但不能自动给出 mainline readiness。

## 全貌架构价值

| VAKS 层 | 价值 | 说明 |
|---|---:|---|
| Capture / Provenance | 中 | 可记录 commit、binary/config 与原 PDF hash，但库本身不管理来源身份。 |
| Candidate Comprehension | 高 | 提供 Markdown、位置项、布局/表格候选与 OCR reason。 |
| Calibration / Point Collision | 低 | 乱码/alternate disagreement 可制造 review pressure，但不判断观点。 |
| Review / Consolidation | 低 | 不检查 evidence support、scope、challenge 或 omission。 |
| Association / Reviewed Relations | 无 | 不创建或验证关系。 |
| Activation / Context Pack | 中高 | 有损 Markdown 和 page-level output 适合作为激活材料。 |
| Decision / Action | 无 | 不提供行动授权或 action basis。 |
| Feedback / Cooling | 低 | benchmark 可诊断 parser 回归，但不是 VAKS feedback ledger。 |
| Risk / Inhibition | 中 | 原因码和局部资源 cap 有用，但宿主仍需完整隔离。 |

## 值得提炼的模式

### A. Native-text-first lazy routing

```text
cheap local parse
-> explicit page/region warning
-> selective expensive OCR
```

这是现有路由思想的实现候选，不新建 pattern。

### B. Positioned transformed artifact

```text
derived text
+ page/bbox/style identity
+ original source hash
+ adapter receipt
```

位置不能把派生文本变成原文，但能降低复核成本。

### C. Multi-hypothesis extraction with abstention

```text
several structural hypotheses
-> compare shape/coverage/issues
-> reject suspicious fragment
-> fallback or abstain
```

### D. Paired regression envelope

```text
fixed corpus + fixed evaluator
-> baseline/candidate
-> aggregate and worst-case deltas
-> disagreement opens inspection
```

## 标签与量化

```yaml
borrow_value: medium-high
implementation_maturity_signal: medium-high
evidence_authority: none
runtime_confidence_for_vaks: low
benchmark_reproducibility_signal: medium-high
security_readiness_for_untrusted_pdf: unverified
schema_change_needed: false
new_pattern_needed: false
```

量化只用于候选排序，不代表 truth confidence 或采用批准。

## 交叉验证

### 公开 benchmark

项目给出的表格限定为：

```text
200 PDFs
OCR disabled
Apple M4 Pro
single process
sequential documents
one excluded warmup
median of five rotating/alternating runs
```

README 的数值和其官方 `firecrawl/opendataloader-bench` 结果分支可逐项对应，且公开了 predictions、evaluation 和 timing records。这提高了“项目确实按所述协议跑过该 benchmark”的可信度。

它仍然不能支持：

```text
all PDFs
Windows/Linux/WASM parity
concurrent throughput or tail latency
malicious/corrupt/huge PDFs
semantic completeness
citation faithfulness
production security
```

### 测试与 CI

静态源码包含大量 Rust test definitions，CI 运行 `cargo test`、developer script tests、fmt、clippy、native build 和 WASM checks。负面点：

- benchmark 不在普通 CI 中持续运行；
- Python pytest 与 NAPI behavior tests 没有在主 CI 执行；
- 未发现 fuzz、Miri/sanitizer、dependency audit gate；
- 本次 review 没有实际执行任何测试。

因此测试资产是维护信号，不是本次运行证明。

## Knowledge Calibration / Point Collision

### Collision 1：README default vs code default

```text
README: EarlyExit default
code:   Sample(8) default
```

处理：以 pinned source code 为当前行为依据；pilot 必须显式传策略，禁止依赖默认。

### Collision 2：per-page layout metadata vs Markdown render inputs

```text
metadata: items + rects + lines
render:   items + rects + empty lines/structure inputs
```

处理：在 adapter fixture 中分别验证元数据和最终 Markdown；二者不能互相替代。

### Collision 3：benchmark strength vs deployment scope

```text
strong published native-parser benchmark
does not imply
safe universal untrusted-PDF parser
```

处理：保留 benchmark 作为性能/结构诊断；生产安全由独立 gate 处理。

### Collision 4：版本身份

```text
Rust 0.1.7
Python 0.2.6
Node 1.11.2
WASM 0.1.3
```

处理：receipt 必须记录 distribution、version、commit、binary hash，不接受模糊的“pdf-inspector vX”。

## Support / Challenge Review

### 支持候选判断的源码事实

- 存在页级 OCR reasons 与位置项。
- detection/extraction 共享一个已加载文档。
- 多条 table/layout path 和显式质量 fallback 存在。
- paired benchmark harness 与 gate 脚本存在。
- MIT 主许可证存在。

### 挑战与缺口

- 默认抽样无法证明全页覆盖。
- Markdown 默认是有损输出。
- API/绑定的页号、坐标、能力和版本不统一。
- 全局资源预算与隔离不由库提供。
- CMap 的打包/第三方 notice 需要对最终 distribution 核验。
- 本地 Windows、中文、混合扫描、表格和长论文 corpus 尚未验证。

### 当前 standing

```text
implementation candidate: standing
formal architecture pattern: not needed
mainline dependency: not ready
evidence authority: rejected
production untrusted-PDF safety: unverified
```

## 关系边 / 关联强度

以下只是假设性关系，不创建 reviewed relation：

```yaml
relations:
  - target: PaddleOCR candidate
    relation_type: complements
    relation_state: candidate
    why: native-text pages first, OCR only for selected pages/regions
  - target: raw intake parser-router sandbox
    relation_type: implements_candidate
    relation_state: candidate
    why: can become one document_parse adapter behind the existing contract
  - target: transformed-evidence-as-original-source
    relation_type: constrained_by
    relation_state: candidate
    why: extracted Markdown, bbox text, and tables remain transformed artifacts
  - target: long-document tree index source adapter
    relation_type: feeds_candidate
    relation_state: candidate
    why: page output can feed later long-document navigation, but does not replace it
```

## 对当前项目的适配点

最小适配 contract：

```yaml
input:
  original_pdf_ref:
  original_sha256:
  intent: document_parse
host_limits:
  max_input_bytes:
  max_pages:
  max_wall_time_ms:
  max_memory_bytes:
adapter:
  distribution:
  distribution_version:
  checked_commit:
  binary_sha256:
  detector_strategy: full
output:
  page_markdown_ref:
  positioned_items_ref:
  pages_needing_ocr:
  ocr_reasons_by_page:
  warning_codes:
  transform_receipt_ref:
authority:
  knowledge_status: candidate
  action_basis_allowed: false
```

## 可拓展性

高价值后续：

- 与 PaddleOCR 做逐页混合路由。
- 用 position items 生成可回到原页的 source selectors。
- 对表格区域采用 external TSR + native text + OCR fallback。
- 将 paired regression envelope 接入 parser maintenance manifest。

不建议的扩展：

- 为该库新建独立架构 lane。
- 同时引入所有 bindings。
- 让 parser 自己决定 evidence support 或 promotion。
- 在 VAKS core 中固化某个 TSR provider 的补丁。

## 复杂度和风险

### 输入资源

局部 cap 存在，但公共入口会整文件读入内存，且没有统一的 bytes/pages/time/memory/output budget。对不受信来源必须隔离进程。

### API 语义

页号、坐标原点、输出字段和 binding feature set 不统一，存在 off-by-one 与语义漂移风险。

### 供应链

四个 distribution 独立发布。主代码 MIT；bundled Adobe CMap 有独立 BSD-style notice。最终包的 CMap 可用性与第三方 notice 需要做实际 tarball/wheel smoke。

### 转换损失

默认删减、跨页表格合并和图像占位会产生看似整洁但可能遗漏上下文的 Markdown。

## 不可行点 / 避坑

```text
Do not treat classification confidence as probability.
Do not infer full-page coverage from a sampled TextBased result.
Do not treat needs_ocr=false as no-omission proof.
Do not replace the original PDF with Markdown.
Do not use extracted table structure as reviewed semantics.
Do not parse untrusted PDFs in the main process without host limits.
Do not identify a deployment only by a vague package version.
Do not read benchmark victory as production approval.
```

## 融合判断

```text
Direct use now: no
Fork: no
Design borrowing: yes
Sandbox pilot: yes, when a real PDF adapter window opens
Formal schema/pattern change: no
Reviewed knowledge promotion: no
```

## 直接判断

| 问题 | 结论 |
|---|---|
| 是否比普通 `pdftotext`/简单 Markdown 转换更值得评测？ | 是。 |
| 是否可作为 PaddleOCR 前置 native path？ | 是，候选。 |
| 是否应现在接入正式资料库 intake？ | 否。 |
| 是否证明可以安全处理任意外部 PDF？ | 否。 |
| 是否能直接支持证据或 action basis？ | 否。 |
| 是否需要新 pattern / lane / schema？ | 否。 |

## 后续行动

未来只在以下触发时重开：

1. 明确启动真实 PDF adapter sandbox。
2. 准备中文/英文/混合扫描/表格/长论文/损坏 PDF fixture。
3. 用已发布 distribution 做 package-level smoke。
4. 配好隔离进程和完整资源预算。
5. 与现有 PaddleOCR/MarkItDown 路线做页级遗漏与锚点对比。
6. 通过 CMap packaging、notice 和依赖审计检查。

在此之前，只保留 source、candidate、annotations、architecture review 与 Project Overlay。
