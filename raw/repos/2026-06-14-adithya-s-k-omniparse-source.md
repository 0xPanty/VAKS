---
type: source
record_kind: source_card
status: source-captured
title: "OmniParse"
source_id: "repo:adithya-s-k/omniparse@9d1ae83c46de777427e67b48f82eaca45ad7994a"
source_uri: "github:adithya-s-k/omniparse@9d1ae83c46de777427e67b48f82eaca45ad7994a"
source_url: "https://github.com/adithya-s-k/omniparse"
source_type: repository
author: "adithya-s-k"
publisher: GitHub
published_at: unknown
updated_at: "2026-06-13T17:30:42Z"
captured_at: "2026-06-14"
captured_by: Codex
version_or_commit: "9d1ae83c46de777427e67b48f82eaca45ad7994a"
source_integrity:
  source_hash: null
  snapshot_hash: "sha256:DB4E281447FC53BD3122EA20064017B6309AFCB9548CA174A52C888036DF9A2E"
  ingest_state: new
adapter_ingest:
  adapter_name: "manual-github-review"
  adapter_version: "2026-06-14"
  capture_method: "GitHub repo page, GitHub API, raw file reads, and commit zip snapshot"
  extraction_trace:
    - "git ls-remote HEAD"
    - "GitHub API repo metadata"
    - "raw.githubusercontent.com file inspection"
    - "GitHub commit zip snapshot"
  known_limits:
    - "Repository was inspected but not executed locally."
    - "Open issues and pull requests were not exhaustively reviewed."
    - "Parser quality was not benchmarked on local VAKS documents."
    - "License posture needs legal review before code embedding or commercial distribution."
source_status: active
raw_location: "raw/repos/_snapshots/2026-06-14-adithya-s-k-omniparse-9d1ae83-source.zip"
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
why_saved: "User asked to strongly distill OmniParse and judge whether it can help VAKS organize raw materials."
topics:
  - source-intake
  - multimodal-parsing
  - raw-material-organization
  - document-parsing
  - OCR
  - audio-video-transcription
  - website-crawling
projects:
  - verified-action-knowledge-system
source_family:
  - parser
  - ingestion-api
  - multimodal-rag-support
upstream_sources:
  - "https://github.com/adithya-s-k/omniparse"
  - "https://github.com/VikParuchuri/marker"
  - "https://github.com/datalab-to/surya"
  - "https://github.com/microsoft/Florence-2"
  - "https://github.com/openai/whisper"
  - "https://github.com/unclecode/crawl4ai"
verification_status: source_identity_checked
candidate_relation_suggestions:
  - target: "outputs/review/2026-06-14-adithya-s-k-omniparse-strong-distillation.md"
    relation_type: derived_from
    relation_state: candidate
    why_suggested: "Strong distillation extracts VAKS raw-intake parser lessons from this repository."
    suggested_at: "2026-06-14"
tags:
  - source
  - repository
  - candidate-only
  - omniparse
  - source-intake
---

# 来源记录：OmniParse

## 为什么收录

用户问：

```text
[adithya-s-k/omniparse](https://github.com/adithya-s-k/omniparse) 强蒸馏这个 可以帮我们整理raw资料？
```

这个仓库直接触到 VAKS 的一个现实短板：

```text
raw 资料来源越来越杂：
PDF / Word / PPT / 图片 / 截图 / 音频 / 视频 / 网页
```

VAKS 主体不应该变成解析器大杂烩，但需要一个可替换的入口层把这些资料转成可追踪的 raw extraction bundle。

## 来源信息

- 作者：adithya-s-k
- 发布方：GitHub
- 原始链接：https://github.com/adithya-s-k/omniparse
- 版本 / commit：`9d1ae83c46de777427e67b48f82eaca45ad7994a`
- 默认分支：`main`
- 仓库状态：未归档；GitHub API 显示最近 push 为 `2025-12-12T15:47:46Z`，repo updated 为 `2026-06-13T17:30:42Z`
- GitHub API 快照：stars `7585`，forks `646`，open issues `73`
- 许可证信号：GitHub / LICENSE / README 指向 `GPL-3.0`；`pyproject.toml` 写 `license = "Apache"`，存在许可证元数据不一致
- 本地快照：`raw/repos/_snapshots/2026-06-14-adithya-s-k-omniparse-9d1ae83-source.zip`
- 快照 SHA256：`DB4E281447FC53BD3122EA20064017B6309AFCB9548CA174A52C888036DF9A2E`

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

Source records provide provenance and findability. This record does not adopt OmniParse, does not approve runtime use, and does not make parser output reviewed knowledge.

## Inspected Repository Areas

| Anchor | What exists | VAKS extraction | Boundary |
|---|---|---|---|
| `README.md` | Positions OmniParse as local unstructured-data parsing for documents, tables, images, video, audio, and webpages. | Confirms raw-intake relevance. | README positioning is not local benchmark evidence. |
| `README.md` | Documents Linux-only server limitation, supported file types, GPU VRAM need, and document parsing limitations. | Direct risk input for VAKS runtime planning. | Limitations are upstream statements, not tested locally. |
| `LICENSE` | GNU GPL v3 license text. | License risk for direct code embedding. | Legal interpretation still needs review. |
| `pyproject.toml` | Package name/version, dependencies, parser stack, and `license = "Apache"` metadata. | Shows heavy dependency profile and license inconsistency. | Dependency install not tested. |
| `Dockerfile` | CUDA Ubuntu base with LibreOffice, FFmpeg, Chrome/ChromeDriver, Torch, and server run command. | Best shape if sandboxing a parser service. | Not run locally. |
| `server.py` | FastAPI routers for document, image, media, and web; CLI flags `--documents`, `--media`, `--web`; Gradio mount. | Borrow lazy module-loading idea. | Router inclusion appears rough and should not be trusted without tests. |
| `omniparse/__init__.py` | Shared model state; loads Marker/Surya, Florence-2, Whisper Small, Selenium crawler. | Useful model-family map for parser adapter design. | Global shared state is not VAKS architecture. |
| `omniparse/models/__init__.py` | `responseDocument` with `text`, `images`, `metadata`, and `chunks`. | Minimal extraction-output contract. | Too weak alone for VAKS source anchors; needs wrapping. |
| `omniparse/documents/router.py` | PDF/PPT/Word endpoints, temp files, Marker-derived code and GPL note. | Document parser adapter candidate. | Includes roughness such as doc endpoint temp suffix mismatch; not production-ready without fixes. |
| `omniparse/image/router.py` and `omniparse/image/process.py` | Image parse/process endpoints with Florence-2 tasks including OCR, caption, object detection, region proposals. | Useful for screenshot / image raw extraction. | VLM output is candidate extraction only. |
| `omniparse/media/router.py` and `omniparse/media/utils.py` | Audio/video endpoints using Whisper transcription. | Can inspire audio/video raw text extraction path. | VAKS already has stricter video intake rules; do not bypass them. |
| `omniparse/web/router.py` and `omniparse/web/web_crawler.py` | Website parse endpoint, Selenium crawler, crawl/search marked coming soon. | Web capture adapter reference. | Do not use private pages/cookies or treat crawled text as evidence support. |
| `python-sdk/omniparse_client/omniparse.py` | Sync/async client methods. | Client shape reference. | SDK appears rough: endpoint mismatches and `.docs` extension typo require caution. |
| `docs/integration.md` | LangChain and LlamaIndex integrations listed as coming soon. | Do not assume mature ecosystem integration. | Integration not available from inspected doc. |

## 初步看点

OmniParse is not a knowledge system. It is a raw parsing gateway:

```text
heterogeneous file / URL
-> parser service
-> structured markdown-like output
-> images / metadata / chunks
```

For VAKS, the useful position is:

```text
raw input staging
-> OmniParse-like parser adapter
-> retained extraction bundle
-> source card
-> candidate distillation
-> later review
```

## 明显疑点

- Linux-only server means it is not a clean native Windows default for this machine.
- Heavy dependencies and GPU/VRAM requirements make it unsuitable as always-on ordinary intake.
- GPL-3.0 / Apache metadata mismatch must be treated as a direct-use risk.
- README says Marker and Surya model weights have commercial usage constraints; this matters if VAKS becomes productized.
- `responseDocument` is convenient but under-specified for VAKS evidence anchors.
- SDK and endpoints show rough edges; do not rely on it as a stable plugin without sandbox tests.
- Parser output can look clean while losing tables, columns, whitespace, Chinese quality, or reading order.

## 可抽取 Candidate Points

1. OmniParse can help VAKS organize raw materials only as a pre-review parser/router.
2. VAKS should borrow the multimodal entrypoint shape, not the authority model.
3. Parser output must be wrapped into a VAKS extraction bundle with original hash, parser config, output files, source anchors, and known limits.
4. Borrow the lazy `--documents / --media / --web` loading posture to avoid turning ordinary capture into heavy infrastructure.
5. Use Omniparse as a comparison reference beside PaddleOCR and RAG-Anything: broader modality coverage than PaddleOCR, weaker typed element manifest than RAG-Anything.

## 当前处理等级

```text
heavy source review, candidate only
```

升级条件：

- User asks to implement a raw-intake parser adapter.
- A sandbox pilot runs OmniParse against real VAKS raw material.
- License and dependency risks are resolved.
- Output bundle can preserve stable page/block/media/source anchors.

## 下一步

Read:

- `outputs/review/2026-06-14-adithya-s-k-omniparse-strong-distillation.md`
- `wiki/summaries/2026-06-14-adithya-s-k-omniparse-architecture-review.md`
- `outputs/review/project_lens_overlays/2026-06-14-adithya-s-k-omniparse-vaks-raw-intake-overlay.md`
