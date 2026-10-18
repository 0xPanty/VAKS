---
record_kind: candidate_distillation
status: draft
provisional: true
title: "OmniParse：VAKS raw 资料整理入口候选"
created_at: "2026-06-14"
created_by: Codex
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
source_ref: "raw/repos/2026-06-14-adithya-s-k-omniparse-source.md"
derived_from:
  - "raw/repos/2026-06-14-adithya-s-k-omniparse-source.md"
  - "raw/repos/_snapshots/2026-06-14-adithya-s-k-omniparse-9d1ae83-source.zip"
  - "wiki/summaries/2026-06-14-adithya-s-k-omniparse-architecture-review.md"
  - "outputs/review/project_lens_overlays/2026-06-14-adithya-s-k-omniparse-vaks-raw-intake-overlay.md"
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - source-intake
  - raw-material-organization
  - multimodal-parser
  - extraction-bundle
  - parser-adapter
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - "raw/repos/2026-06-14-adithya-s-k-omniparse-source.md#Inspected Repository Areas"
  - "raw/repos/_snapshots/2026-06-14-adithya-s-k-omniparse-9d1ae83-source.zip:README.md"
  - "raw/repos/_snapshots/2026-06-14-adithya-s-k-omniparse-9d1ae83-source.zip:server.py"
  - "raw/repos/_snapshots/2026-06-14-adithya-s-k-omniparse-9d1ae83-source.zip:omniparse/models/__init__.py"
  - "raw/repos/_snapshots/2026-06-14-adithya-s-k-omniparse-9d1ae83-source.zip:omniparse/documents/router.py"
  - "raw/repos/_snapshots/2026-06-14-adithya-s-k-omniparse-9d1ae83-source.zip:python-sdk/omniparse_client/omniparse.py"
borrow_value: strong
borrow_order:
  - "P1: multimodal raw intake router before VAKS source cards"
  - "P2: extraction bundle contract wrapping text/images/metadata/chunks with VAKS anchors"
  - "P3: sandboxed parser service reference, only after license/runtime checks"
avoid:
  - "Do not let OmniParse output become reviewed knowledge, action basis, or truth confidence."
  - "Do not embed GPL/Marker-derived code into VAKS product code without license review."
  - "Do not make it always-on for ordinary capture."
  - "Do not use web crawling on private/account pages or cookie-backed content by default."
  - "Do not replace PaddleOCR/RAG-Anything lessons with OmniParse; use it as a router/comparison reference."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "the task is specifically to design or implement raw-material parsing / source-intake adapters"
  support_when: "designing extraction bundles, parser routing, or multimodal raw staging"
  risk_when: "someone proposes parser Markdown as evidence support, reviewed truth, or direct action basis"
  cold_references:
    - "raw/repos/2026-06-14-adithya-s-k-omniparse-source.md"
    - "raw/repos/_snapshots/2026-06-14-adithya-s-k-omniparse-9d1ae83-source.zip"
tags:
  - candidate
  - provisional
  - strong-distillation
  - omniparse
  - source-intake
  - raw-materials
  - parser-adapter
  - candidate-only
---

# 候选蒸馏：OmniParse

## 说人话

可以帮我们整理 raw 资料，而且方向挺对。

但它不能当 VAKS 的“大脑”，更不能当“审核器”。它最合适的位置是：

```text
乱七八糟的 raw 文件 / URL
  -> 先用 OmniParse 这类入口解析器拆出来
  -> 保存成 VAKS 可追踪 extraction bundle
  -> 再进入 source card / candidate / review
```

一句话：

```text
OmniParse 适合做 raw 入口整理工，不适合做资料库权威层。
```

## 直接评分

| 维度 | 分数 | 判断 |
|---|---:|---|
| 帮 VAKS 整理 raw 资料 | 8/10 | 强相关，尤其是 PDF / 图片 / 音视频 / 网页混合入口。 |
| 进入 VAKS 核心架构 | 4/10 | 不该进核心；应该作为可替换插件/适配器。 |
| 直接拿来生产用 | 4/10 | Linux-only、重依赖、许可证、SDK/endpoint 粗糙度都要先过 sandbox。 |
| 设计借鉴价值 | 8/10 | 入口路由、模态分层、懒加载模型、统一输出形态很值得借。 |

所以结论不是“装上就完事”，而是：

```text
design-only / adapter-reference now
sandbox pilot later
mainline dependency no
```

## Candidate Point 1: OmniParse is a raw intake router

VAKS 现在的强项是：

```text
source provenance
candidate distillation
review queue
evidence gate
activation / context pack
feedback
```

但 raw 入口越来越杂：

```text
doc/docx/pdf/ppt/pptx
png/jpg/tiff/bmp/heic
mp3/wav/aac
mp4/mkv/avi/mov
dynamic web pages
```

OmniParse 的价值是把这些入口先统一到一个 parser API：

```text
input raw material
-> parse_document / parse_image / process_image / parse_audio / parse_video / parse_website
-> responseDocument(text, images, metadata, chunks)
```

VAKS 借这个思路，但不能照搬结果：

```text
responseDocument
-> VAKS extraction bundle
-> source card
-> candidate distillation
-> optional review queue
```

## Candidate Point 2: raw 整理应该先建 extraction bundle

OmniParse 给的是简单输出对象：

```text
text
images
metadata
chunks
```

对普通 RAG 这够用。对 VAKS 不够。

VAKS 需要包一层自己的 raw extraction bundle：

```yaml
original:
  path:
  sha256:
  source_type:
parser:
  adapter_name:
  adapter_version:
  runtime:
  model_flags:
  known_limits:
outputs:
  markdown_path:
  json_path:
  images_dir:
  chunks_path:
anchors:
  page_refs: []
  timestamp_refs: []
  region_refs: []
  url_refs: []
quality:
  extraction_confidence:
  language_risk:
  layout_risk:
  missing_parts:
boundary:
  knowledge_status: raw
  action_basis_allowed: false
  truth_mutation_allowed: false
```

这层才是跟 VAKS 架构合拍的东西。

## Candidate Point 3: use lazy parser escalation

OmniParse 的 server 启动有模块开关：

```text
--documents
--media
--web
```

这个思路适合 VAKS：

| raw 类型 | VAKS 默认动作 | OmniParse-like 动作 |
|---|---|---|
| 已经是 Markdown / txt | 直接 source card，不解析 | skip |
| born-digital PDF / Word / PPT | 轻解析成 Markdown + metadata | document parser |
| 扫描 PDF / 图片截图 | OCR / VLM parser，保留原图锚点 | image / document parser |
| 音频 / 视频 | 先按 VAKS 视频规则走字幕/ASR/ledger | media parser only as adapter |
| 网页 | 普通公开网页可抓取，私有网页禁止默认抓 | website parser with strict boundary |
| 高风险行动依据 | 解析后仍必须走 evidence gate | no direct action |

不要做：

```text
所有资料进来都强解析
所有解析结果都自动 candidate
所有 candidate 都自动 review
```

正确做法是轻重分流。

## Candidate Point 4: complement PaddleOCR and RAG-Anything

OmniParse 不是单点最强解析器。它更像“入口壳”。

对照我们已有材料：

| 工具 / 参考 | 更强在哪里 | 对 VAKS 的位置 |
|---|---|---|
| PaddleOCR | 扫描件、图片、复杂文档 OCR / layout / 表格 / 公式方向更专。 | 视觉文档 parser 候选。 |
| RAG-Anything | typed content list / multimodal element manifest / heavy source extractor 思路更强。 | 多模态元素清单和证据锚点参考。 |
| OmniParse | 覆盖文档、图片、音视频、网页的一站式入口更顺手。 | raw intake router / adapter shell 候选。 |

所以最好不是三选一，而是这样融合：

```text
VAKS Raw Intake Adapter
  router: OmniParse-like
  OCR parser: PaddleOCR / Marker / Surya / future parser
  element manifest: RAG-Anything-like
  authority: VAKS source card + candidate + review gate
```

## Candidate Point 5: plugin boundary should be file-first

如果以后做插件，不要让插件直接写 `wiki/claims`、`wiki/patterns`、`wiki/decisions`。

插件只能写：

```text
raw/<source>/original.*
raw/<source>/extraction/*
raw/<source>.md source card
outputs/review/<source>-candidate-distillation.md
```

插件不能写：

```text
reviewed claim
reviewed relation
truth confidence
action basis
decision
```

这样它可以强力整理 raw，但不会污染 VAKS 的权威边界。

## Candidate Point 6: web crawler must be treated as high-risk intake

OmniParse 的 web 方向用了 Selenium crawler，并且 crawl/search 还标成 coming soon。

对 VAKS 的规则应该更硬：

```text
public URL only
no cookies by default
no private account pages
no member-only content
record captured_at and URL
save raw HTML/text snapshot when important
web extraction is provenance/candidate only
```

网页解析最容易制造“看起来像资料，其实上下文丢了”的问题，所以不能让它直接变成 evidence support。

## Candidate Point 7: license and productization risk is real

这是必须写死的避坑点。

观察到：

```text
GitHub / LICENSE / README: GPL-3.0
pyproject.toml: license = "Apache"
README: Marker and Surya model weights have commercial restrictions
document router: notes Marker-derived GPL code
```

因此：

```text
可以借设计
可以做本地 sandbox
谨慎作为外部服务调用
不要直接复制/嵌入代码进产品核心
产品化前必须许可证复核
```

## VAKS Raw 整理融合方案

最小合理方案：

```text
1. raw inbox receives file / URL
2. source identity and hash are recorded first
3. router chooses parser only when needed
4. parser output is saved as retained raw extraction
5. source card points to original + extracted artifacts
6. candidate distillation reads extraction with warnings
7. review queue only opens for important points
8. action basis still requires later evidence support / sufficiency gate
```

建议的插件形态：

```text
vaks-raw-intake-adapter
  - input_classifier
  - parser_router
  - extraction_bundle_writer
  - source_card_writer
  - candidate_router
  - lint_boundary_checker
```

不建议的形态：

```text
omniparse-as-vault
omniparse-as-truth-engine
omniparse-auto-review
omniparse-always-on-crawler
omniparse-direct-action-basis
```

## Borrow / Avoid

### Borrow

- Unified endpoint family for documents, media, images, and websites.
- Lazy model loading by modality.
- Docker/Linux service isolation for heavy parsers.
- `text/images/metadata/chunks` as a first draft output object.
- Local-first parsing posture.
- Gradio/API demo surface as future workbench inspiration, not core.

### Adapt

- Wrap outputs in VAKS extraction bundle.
- Add original hash, parser config, model flags, source anchors, and known limits.
- Add typed element manifest if a source has tables/images/equations/page regions.
- Route parser output to candidate distillation only.
- Put extraction quality under source integrity, not truth confidence.

### Avoid

- Direct code embedding before license review.
- Treating parser output as reviewed evidence.
- Always-on heavy parser for normal notes.
- Private web crawling by default.
- Trusting SDK integration without endpoint tests.
- Hiding parser failures behind clean Markdown.

## Open Questions

- Can it parse our Chinese-heavy PDFs and screenshots better than PaddleOCR / MarkItDown / existing video intake?
- Does the Docker image run reliably on our local GPU/Windows-through-Docker setup?
- Can output preserve page/block/time anchors enough for evidence review?
- What license posture is acceptable if VAKS productizes raw intake?
- Should Omniparse be only a comparison reference while PaddleOCR handles documents and existing VAKS handles video?

## Routing Hint

Route this source to:

```text
source-intake
raw-material-organization
parser-adapter
document/video/web extraction boundary
future plugin comparison
```

Do not route to:

```text
reviewed truth
schema authority
action basis
core storage
```

## Bottom Line

OmniParse 对我们最有价值的一句话：

```text
它提醒 VAKS 需要一个“raw 入口整理层”，但这个层必须可替换、可审计、低权威。
```

我们的版本应该比它更强的地方：

```text
OmniParse focuses on converting data for LLM use.
VAKS must preserve provenance, authority boundaries, review readiness, and action safety.
```
