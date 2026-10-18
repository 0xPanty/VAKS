---
type: source
status: source-captured
title: "microsoft/markitdown"
source_id: "repo:microsoft/markitdown@e144e0a2be95b34df17433bac904e635f2c5e551"
source_uri: "https://github.com/microsoft/markitdown"
source_url: "https://github.com/microsoft/markitdown"
source_type: repo
author: "Microsoft / AutoGen Team contributors"
publisher: GitHub
published_at: 2024-11-13
updated_at: 2026-06-07
captured_at: 2026-06-07
captured_by: Codex
version_or_commit: "e144e0a2be95b34df17433bac904e635f2c5e551"
source_status: active
raw_location: "raw/repos/_snapshots/microsoft-markitdown-e144e0a2be95b34df17433bac904e635f2c5e551.zip"
snapshot_sha256: "0426133834C4017E63F10A5E59CF4E1A6D8BDF3DACFA035C800F5B896DE80B47"
processing_mode: repo-intake
processing_level: medium
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
review_priority: high
review_owner: Codex
formalization_status: raw-only
topics:
  - file-conversion
  - markdown
  - source-intake
  - document-ingest
  - mcp
projects:
  - verified-action-knowledge-system
source_family: document-to-markdown
upstream_sources: []
verification_status: source-checked
candidate_relation_suggestions:
  - target: "[[source-intake-file-to-markdown-adapter]]"
    relation_type: derived_from
    relation_state: candidate
    why_suggested: "The repo provides a concrete file-to-Markdown conversion adapter shape for VAKS source intake."
    source_anchor: "packages/markitdown/src/markitdown/_markitdown.py:94"
    evidence_support:
      span_supports_target: true
      evidence_role: implementation_anchor
      reviewer_note: "Candidate relation only; not a reviewed pattern."
    suggested_at: 2026-06-07
tags:
  - source/repo
  - markitdown
  - document-ingest
  - candidate
---

# 来源记录：microsoft/markitdown

## 为什么收录

用户问这个仓库对“蒸馏文件内容 skill / VAKS”有没有帮助，并明确要求强蒸馏。

MarkItDown 的核心价值是把 PDF、Word、Excel、PowerPoint、HTML、图片、音频、ZIP、YouTube URL、EPub 等材料先转成 Markdown，让后续 LLM / text analysis pipeline 处理。这个问题刚好落在 VAKS 的 Source Intake 前置转换层。

## 来源信息

- 作者 / 组织：Microsoft / AutoGen Team contributors
- 发布方：GitHub
- 原始链接：https://github.com/microsoft/markitdown
- 默认分支：main
- 检查提交：`e144e0a2be95b34df17433bac904e635f2c5e551`
- commit 时间：2026-05-26T22:40:20Z
- commit message：`Bump version to 0.1.6 (#1914)`
- 包版本：`0.1.6`
- license：MIT
- GitHub API capture：stars 146837, forks 10049, open issues 816, captured 2026-06-07
- 本地快照：`raw/repos/_snapshots/microsoft-markitdown-e144e0a2be95b34df17433bac904e635f2c5e551.zip`
- 快照 SHA256：`0426133834C4017E63F10A5E59CF4E1A6D8BDF3DACFA035C800F5B896DE80B47`
- 采集方式：GitHub live page + GitHub API + commit zip snapshot + local source inspection

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

这个 source card 只记录来源、版本、锚点和初步看点。它不是采用结论、不是 reviewed knowledge、不是 action basis。

## 关键实体置信检查

| Entity | Checked By | Confidence | Note |
|---|---|---:|---|
| `microsoft/markitdown` | GitHub page + API + `git ls-remote` | high | repo URL and owner verified |
| latest checked commit | `git ls-remote` + commit API | high | `e144e0a2be95...` |
| package version | snapshot `packages/markitdown/src/markitdown/__about__.py` | high | `0.1.6` |
| license | GitHub API + snapshot LICENSE | high | MIT |
| VAKS relevance | local SOURCE_INTAKE / repo review protocol comparison | medium | candidate design relevance only |

## Source / Code Anchors

| Anchor | What exists | Why it matters |
|---|---|---|
| `README.md:8-12` | Security note plus lightweight file-to-Markdown positioning | Fits VAKS as a converter, not a truth layer |
| `README.md:14-24` | Supported input list: PDF, Office docs, images, audio, HTML, CSV/JSON/XML, ZIP, YouTube, EPUB | Covers common file-distillation sources |
| `README.md:91-112` | Optional dependency groups | Useful for staged install policy: do not install `[all]` by default |
| `README.md:342-348` | Security considerations and narrow conversion API guidance | Directly relevant to VAKS source hygiene |
| `packages/markitdown/pyproject.toml:18-51` | Core and optional dependencies | Shows dependency surface and cloud/API optionality |
| `packages/markitdown/src/markitdown/_markitdown.py:94-139` | Main `MarkItDown` class, builtins/plugins toggles | Central adapter object |
| `packages/markitdown/src/markitdown/_markitdown.py:182-205` | Built-in converter registration list | Concrete multi-format routing pattern |
| `packages/markitdown/src/markitdown/_markitdown.py:428-497` | URI/response conversion APIs | Needs VAKS allowlist and network/path policy |
| `packages/markitdown/src/markitdown/_markitdown.py:569-578` | Sorted converter attempts | Converter fallback pattern |
| `packages/markitdown/src/markitdown/_base_converter.py:5-42` | `DocumentConverterResult` and `DocumentConverter` base | Simple interface shape |
| `packages/markitdown/src/markitdown/converters/_pdf_converter.py:495-584` | PDF converter with pdfplumber/pdfminer fallback | Good but not enough for source-span fidelity |
| `packages/markitdown/src/markitdown/__main__.py:57-66` | CLI output and extension hints | Useful for tool contract design |
| `packages/markitdown/src/markitdown/__main__.py:90-130` | Cloud CU and plugin flags | Must stay explicit / opt-in |
| `packages/markitdown-mcp/src/markitdown_mcp/__main__.py:20-23` | MCP `convert_to_markdown(uri)` tool | Useful reference, risky default |
| `packages/markitdown-mcp/README.md:132-134` | MCP server security warning | Strong warning for agent-access boundary |
| `packages/markitdown-ocr/src/markitdown_ocr/_plugin.py:19-68` | OCR plugin registers priority converters | Plugin replacement mechanism |
| `packages/markitdown/tests/_test_vectors.py:16-260` | Multi-format fixture list | Good test-matrix seed for VAKS |
| `packages/markitdown/tests/test_module_vectors.py:57-147` | Local, stream, HTTP URI, file URI, data URI tests | Helps define allowed/forbidden input modes |

## 初步看点

- 它是一个成熟度较高的 document-to-Markdown adapter 候选，不是知识系统。
- 对 VAKS 最有用的是“文件先标准化成 Markdown，再进入 candidate comprehension”。
- 它的安全说明和 MCP 说明反而很重要：如果转换器能读任意 file/URI，就必须被 VAKS 的 path/network/write policy 包起来。
- optional dependency 设计适合 VAKS：默认只装小集，按 source type 启用 PDF/DOCX/PPTX/XLSX。
- OCR / Azure / MCP 是 later-stage 支线，不应默认启用。

## 明显疑点

- Markdown 输出不天然保留可复核 source spans、页码、单元格坐标或截图区域。
- `convert()` 太宽，能处理 local file、remote URI、byte stream；VAKS 需要更窄的 wrapper。
- MCP server 没有认证，且工具可读当前用户能读的本机文件或网络内容；不能直接作为 VAKS agent tool 暴露。
- PDF / Office 转换质量需要用本地真实材料跑 fixture；本次未安装运行。
- 依赖 `[all]` 会引入云能力、音频转写和较宽依赖面；不适合作为默认。

## 可抽取 Candidate Points

1. VAKS 可以把 MarkItDown 作为文件蒸馏的前置规范化 adapter，而不是知识判断器。
2. 文件蒸馏入口应该先产生 retained raw markdown + conversion metadata + source hash，再进入 candidate distillation。
3. 转换器 API 要限定为 `convert_local` / `convert_stream` 风格，并由 VAKS 外层控制 path、URI、network、output。
4. 多格式 fixture matrix 可以借鉴 MarkItDown tests：docx/xlsx/pptx/pdf/html/json/zip/audio/image、本地路径、stream、URI、stdin/stdout。
5. 插件 / OCR / MCP / cloud analyzers 应保持 opt-in，并写入 provenance / tool activity，而不是默认 source intake。

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 要把 MarkItDown 接进真实 VAKS file-intake skill；
- 要处理用户真实文件；
- 要把转换结果作为 action-facing answer 的 source envelope；
- 要开放给 agent / MCP 调用。

## 下一步

- 保持候选层。
- 若后续要实现 VAKS 文件蒸馏 skill，先写最小 wrapper 合约和 fixture matrix。
- 在任何运行前确认：路径范围、网络开关、插件开关、云 API 开关、输出目录、hash ledger、source-span/locator 保留策略。
