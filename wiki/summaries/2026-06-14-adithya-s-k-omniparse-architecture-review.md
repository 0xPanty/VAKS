---
type: summary
status: draft
title: "OmniParse architecture review for VAKS raw intake"
created: "2026-06-14"
library_name: "OmniParse"
repo_url: "https://github.com/adithya-s-k/omniparse"
source_url: "raw/repos/2026-06-14-adithya-s-k-omniparse-source.md"
checked_commit: "9d1ae83c46de777427e67b48f82eaca45ad7994a"
commit_time: unknown
source_status: active
reviewed_at: "2026-06-14"
domain: "multimodal source parsing / raw intake"
related_projects:
  - verified-action-knowledge-system
current_branch: "source-intake / raw-material-organization"
extracted_patterns:
  - "multimodal raw intake router"
  - "parser output bundle"
  - "lazy modality loading"
  - "parser quarantine boundary"
fusion_decision: adapt-design-only
inspection_confidence: medium
evidence_count: 14
cross_validated_with:
  - "outputs/review/2026-06-11-PaddlePaddle-PaddleOCR-candidate-distillation.md"
  - "outputs/review/2026-05-30-rag-anything-external-multimodal-source-extractor-alpha.md"
negative_evidence:
  - "Linux-only server according to README."
  - "GPL-3.0 license / Apache pyproject mismatch."
  - "SDK and endpoint roughness observed in source."
  - "No local runtime benchmark."
extension_potential: "High as a replaceable parser adapter; low as core architecture."
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - summary
  - architecture-review
  - omniparse
  - raw-intake
  - parser-adapter
  - candidate-only
---

# OmniParse 架构评审：VAKS raw intake 候选

## 一句话判断

OmniParse 对 VAKS 有帮助，但帮助点很窄也很清楚：

```text
作为 raw 资料入口整理器 / parser router，可以借。
作为 VAKS 知识库架构、审核系统、真理层，不能借。
```

最小融合：

```text
VAKS authority stays file-first and review-gated.
OmniParse-like parser only creates retained raw extraction bundles.
```

## 它解决什么问题

OmniParse 解决的是 GenAI/RAG 前的非结构化资料解析：

```text
documents
tables
images
videos
audio files
web pages
```

它试图把这些输入转成 LLM 更容易吃的结构化 Markdown、图像、metadata、chunks。

对 VAKS 来说，这正好对应：

```text
Capture / Provenance 之前或之内的 raw extraction stage
```

不是：

```text
Review
Reviewed Relations
Decision
Action Basis
```

## 核心设计

它的核心不是一个复杂知识系统，而是一个 parser service：

```text
FastAPI server
  /parse_document/*
  /parse_image/*
  /parse_media/*
  /parse_website/*

Model loaders
  documents: Marker / Surya / Florence-2
  media: Whisper
  web: Selenium crawler

Response
  text
  images
  metadata
  chunks
```

这个结构对 VAKS 的启发是：

```text
把 parser 做成可换的边界服务，而不是把 parser 融进知识模型。
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| GitHub repo page | Public repo, GPL-3.0 license label, stars/forks/issues, README rendered. | Source identity and maturity signal. | Popularity is not correctness. |
| `README.md` | Claims local parsing, no external APIs, T4 fit, about 20 file types, structured Markdown, table/image/audio/video/web support. | Strong raw-intake relevance. | README feature claims need local verification. |
| `README.md` | States server only works on Linux-based systems. | Runtime boundary for this Windows workspace. | Does not block design borrowing. |
| `README.md` | Lists supported documents/images/video/audio/web types and API endpoints. | Parser router map. | File-type support is not quality support. |
| `README.md` | Lists limitations: GPU VRAM, equations, Chinese parsing, tables, whitespace, line joining, digital-PDF bias, small model variants. | Direct risk list for extraction quality. | Do not convert limitations into universal rejection. |
| `README.md` and `LICENSE` | GPL-3.0; Marker and Surya commercial caveats. | Productization/license risk. | Needs legal review before code embedding. |
| `pyproject.toml` | `name = "omniparse"`, version `0.0.1`, description as API for structured Markdown, heavy dependencies including Torch, Surya, Whisper, Selenium, Gradio, Marker, flash-attn. | Heavy parser service, not lightweight core dependency. | `license = "Apache"` conflicts with repo GPL signals. |
| `Dockerfile` | CUDA Ubuntu base, LibreOffice, FFmpeg, Chrome/ChromeDriver, Torch, `server.py --documents --media --web`. | Use isolation if piloting. | Not executed locally. |
| `server.py` | FastAPI routers, CLI flags `--documents`, `--media`, `--web`, Gradio mount. | Borrow lazy modality loading and route family. | Source appears rough; needs endpoint tests. |
| `omniparse/__init__.py` | Loads Marker/Surya models, Florence-2, Whisper small, and Selenium crawler into shared state. | Model-family map for parser adapter. | Global shared state is an implementation detail, not architecture to copy. |
| `omniparse/models/__init__.py` | `responseDocument` has `text`, `images`, `metadata`, `chunks`. | Minimal output contract. | VAKS needs stronger anchor and provenance contract. |
| `omniparse/documents/router.py` | Marker-derived document parsing endpoints; temp files for PDF/PPT/Word. | Document parser endpoint reference. | GPL-derived code and rough temp suffix in docs endpoint require caution. |
| `omniparse/image/process.py` | Florence-2 tasks: caption, OCR, object detection, dense region caption, region proposal, segmentation. | Useful for screenshots/image notes. | VLM outputs may hallucinate and need visual anchors. |
| `omniparse/media/utils.py` | Whisper transcription wrapper. | Media transcript adapter reference. | VAKS video intake already requires source-visible transcript/ledger. |
| `omniparse/web/router.py` | Website parse endpoint; crawl/search return "Coming soon". | Web parser is immature. | Public-only, no cookies/private crawling by default. |
| `python-sdk/omniparse_client/omniparse.py` | Async parser methods and allowed extension lists. | Client API shape. | Observed endpoint mismatches and `.docs` extension typo suggest immature SDK. |

## 当前支线价值

当前支线：source-intake / raw-material-organization。

它对当前支线：

```text
supports / refines / risk_of
```

具体价值：

- Supports: confirms VAKS needs a modality-aware raw parser entrypoint.
- Refines: parser output should become extraction bundles, not source cards directly.
- Risk_of: clean Markdown conversion can trick agents into treating extraction as evidence.

风险：

- Heavy runtime can make ordinary capture too expensive.
- Parser output can lose page/table/region/time anchors.
- License/dependency posture can contaminate productization.
- Web crawling can capture wrong/private/stale context.

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Helps ingest convert heterogeneous raw material into readable artifacts. | adapt |
| Dusk workbench | Could power a future "parse this raw item" workbench button. | watch |
| source ingest | Strong fit as parser router and retained extraction bundle generator. | adapt |
| review queue | Can create candidate points only after raw extraction is retained. | adapt |
| schema / reviewed knowledge | No authority; should not write reviewed nodes or relations. | reject |
| memory / dev context | Parsed raw can become Support or Cold Reference for dev tasks. | adapt |
| feedback | Parser failures can create scoped feedback / review pressure. | watch |
| retrieval / cache | Parsed Markdown/chunks improve search after authority filtering. | adapt |
| API / MCP / agent access | FastAPI shape useful; future VAKS plugin should be path-scoped. | adapt |
| viewer / workbench | Gradio/UI idea is optional; not core. | watch |
| publishing | Could later help source-to-draft conversion. | watch |
| risk / anti-pattern | Main anti-pattern is treating parser Markdown as reviewed truth. | adopt as guardrail |

## 值得提炼的模式

### 1. Parser quarantine boundary

Correct:

```text
source -> parser -> retained extraction -> source card -> candidate -> review
```

Wrong:

```text
source -> parser -> reviewed note
```

### 2. Multimodal raw intake router

One router can select parser families:

```text
documents
images
audio
video
web
```

VAKS should keep this as an adapter layer.

### 3. Extraction bundle stronger than parser response

OmniParse `responseDocument` is good enough for a demo but too weak for VAKS.

VAKS should wrap it with:

```text
original hash
parser config
runtime/model info
known limits
output paths
page/region/timestamp/url anchors
boundary flags
```

### 4. Lazy modality loading

Load document/media/web models only when needed. This matches VAKS:

```text
ordinary capture stays light
strict/heavy parsing only when needed
```

### 5. Design-only until sandbox

Given runtime/license/SDK risks, the current correct posture is:

```text
borrow design
retain snapshot
do not adopt dependency
pilot later with real VAKS raw files
```

## 标签与量化

- domain: multimodal parsing / source intake
- problem: heterogeneous raw material is hard to make searchable and reviewable
- pattern: parser router + retained extraction bundle
- maturity: emerging / rough implementation
- complexity: high as runtime, medium as design reference
- problem_fit: 5/5 for raw intake
- reuse_value: 4/5 for router and bundle design
- implementation_cost: 4/5 if running OmniParse itself
- integration_fit: 4/5 as adapter reference, 2/5 as mainline dependency
- evidence_strength: 3/5 for design fit, 1/5 for local runtime
- reversibility: 5/5 if kept as derived extraction layer

## 交叉验证

相似设计来源：

- PaddleOCR: stronger specialist for OCR/scanned/visual document parsing.
- RAG-Anything: stronger typed multimodal content-list / element-manifest idea.

支持证据：

- OmniParse README and source show a working intent for multimodal parsing.
- Server/router/code shape exposes document/image/media/web boundaries.
- Local VAKS manuals already define source intake, parser metadata, and candidate-only boundaries.

反例或失败边界：

- README states Chinese/table/layout limitations.
- Linux-only runtime and heavy dependency set make it unsuitable as default intake.
- SDK endpoint roughness suggests it is not polished enough as a direct plugin.

最小验证方式：

```yaml
pilot_scope: sandbox_only
inputs:
  - born_digital_pdf
  - scanned_chinese_pdf
  - image_screenshot
  - short_audio_or_video
  - public_web_page
checks:
  - original_sha256_retained
  - markdown_output_readable
  - image_or_page_anchors_retained
  - metadata_and_parser_config_saved
  - no_action_basis_true
  - source_card_points_to_artifacts
  - runtime_memory_recorded
pass_result:
  - candidate adapter reference
fail_result:
  - design-only reference
```

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed / Candidate Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Parser output should be raw extraction only. | SOURCE_INTAKE says adapter output may create raw/candidate material but not reviewed nodes or truth. | candidate_relation | Can future lint block parser-derived Markdown from being used as support? |
| Unified multimodal router helps raw organization. | VAKS Capture / Provenance layer needs easy capture and source hygiene. | refines | What is the minimal router that avoids overdesign? |
| Output needs text/images/metadata/chunks. | RAG-Anything review adds typed source element manifest. | scope_mismatch | Should VAKS require typed elements only for heavy sources? |
| Image/OCR/VLM parsing helps screenshots and visual docs. | PaddleOCR review already covers stronger OCR/parser candidates. | refines | Is OmniParse a router shell while PaddleOCR is a parser backend? |
| Web crawler can parse dynamic pages. | VAKS forbids private/cookie/account content without explicit approval. | risk_candidate | Should web parser be disabled by default? |

## Support / Challenge Review

What supports it:

- Official repo and source code expose multimodal parser service shape.
- VAKS currently needs a clean pre-review raw intake path for mixed documents.
- Existing PaddleOCR and RAG-Anything reviews point to the same raw extraction gap.

What challenges it:

- Runtime is Linux-only and heavy.
- License and commercial model-weight caveats matter.
- SDK/API roughness makes direct plugin adoption risky.
- Parser quality on Chinese/layout-heavy material is not proven locally.

Challenge severity:

```text
major for direct use
minor for design-only borrowing
```

Scope limits:

```text
Use only as raw intake parser/router reference.
Do not use as knowledge authority or review engine.
```

Known risks:

- License contamination.
- Dirty Markdown mistaken for clean evidence.
- Web crawling overreach.
- Overbuilding parser infrastructure before real raw input pilots.

Review again when:

- User asks to implement raw intake adapter.
- Real VAKS raw files are available for parser benchmark.
- License/dependency posture is clarified.

Action readiness:

```text
not_ready
```

## 对当前项目的适配点

Best VAKS shape:

```text
Raw Inbox
  -> Input Classifier
  -> Parser Router
  -> Extraction Bundle Writer
  -> Source Card Writer
  -> Candidate Router
  -> Review Queue only when needed
```

OmniParse can inspire:

- parser endpoint family;
- lazy model flags;
- Docker-isolated heavy parser service;
- unified output object;
- raw material workbench button.

VAKS must add:

- authority bucket filtering;
- source hash and snapshot;
- source anchors;
- extraction ledger;
- `action_basis_allowed: false`;
- parser-output warning codes;
- review gate before any action use.

## 可拓展性

- 是否适合作为插件/适配层：yes, as external parser service or design reference.
- 是否会绑定核心结构：should not; keep replaceable.
- 未来替换成本：low if extraction bundle contract is VAKS-owned.
- 可迁移路径：start with design-only contract, then sandbox OmniParse/PaddleOCR/MarkItDown/RAG-Anything style parser adapters.

## 复杂度和风险

- High runtime complexity if running full OmniParse.
- Medium integration complexity if only borrowing API shape.
- High license risk for embedded code.
- Medium source hygiene risk if crawler/parser outputs are not anchored.
- Low architecture risk if kept outside truth/review layers.

## 不可行点 / 避坑

- Do not install as mainline dependency now.
- Do not copy code into product without license review.
- Do not use it for private web/account data.
- Do not trust generated Markdown without original source anchors.
- Do not allow parser confidence to become truth confidence.
- Do not use it to bypass VAKS video intake ledger.

## 融合判断

- 结论：adapt / design-only now; sandbox later.
- 理由：raw intake router design is valuable, but runtime/license/maturity risks are too high for direct adoption.
- 验证方式：small sandbox against real VAKS raw files, compared with PaddleOCR and existing intake flow.

## 直接判断

- Direct use: no, not now.
- Fork: no.
- Design-only: yes, strong.
- Reject: no; reject only core-dependency/direct-authority use.
- Current branch value: strong for raw-material organization.
- Whole architecture value: medium-high as source ingest adapter reference.
- Risk: major if parser output is treated as evidence/truth; major if code is embedded without license review.
- Next action: keep as candidate reference; if implementing raw intake, define VAKS extraction bundle contract first, then run sandbox.

## 后续行动

Do not update core architecture from this file alone.

If the user asks for implementation planning later, start with:

```text
VAKS-owned extraction bundle schema
parser adapter interface
small sandbox benchmark
license/runtime check
boundary lint
```
