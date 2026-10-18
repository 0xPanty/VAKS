---
record_kind: candidate_distillation
status: draft
provisional: true
title: "PaddleOCR：文档入库前的 OCR/结构化解析候选"
created_at: "2026-06-11"
created_by: Codex
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
derived_from:
  - raw/repos/2026-06-11-PaddlePaddle-PaddleOCR-source.md
  - raw/repos/_snapshots/2026-06-11-PaddlePaddle-PaddleOCR-71c7fef-source.zip
  - wiki/summaries/2026-06-11-PaddlePaddle-PaddleOCR-architecture-review.md
  - outputs/review/project_lens_overlays/2026-06-11-paddleocr-document-intake-parser.md
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
  - document-parsing
  - scanned-pdf
  - raw-extraction
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - raw/repos/2026-06-11-PaddlePaddle-PaddleOCR-source.md#Inspected Repository Areas
  - raw/repos/_snapshots/2026-06-11-PaddlePaddle-PaddleOCR-71c7fef-source.zip:README.md
  - raw/repos/_snapshots/2026-06-11-PaddlePaddle-PaddleOCR-71c7fef-source.zip:docs/version3.x/pipeline_usage/PP-StructureV3.md
  - raw/repos/_snapshots/2026-06-11-PaddlePaddle-PaddleOCR-71c7fef-source.zip:docs/version3.x/pipeline_usage/PaddleOCR-VL.md
borrow_value: strong
borrow_order:
  - "P1: scanned/image/PDF pre-storage parser with provenance-retained Markdown/JSON output"
  - "P2: adapter contract reference for MCP/loader-style document intake tools"
  - "P3: future sandbox benchmark source for OCR/parser quality and runtime"
avoid:
  - "Do not use PaddleOCR as the vault storage layer."
  - "Do not treat OCR, VLM output, Markdown conversion, or GitHub stars as evidence support or reviewed truth."
  - "Do not run PaddleOCR-VL by CPU for routine intake without a runtime pilot."
  - "Do not depend on paddleocr-mcp until the PyPI dependency mismatch is checked."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "the task is specifically about scanned PDF/image intake, OCR conversion, document parsing, or building a VAKS document-ingest adapter"
  support_when: "designing source acquisition, retained raw text bundles, parser metadata, or OCR quality gates"
  risk_when: "someone proposes OCR output as reviewed evidence, action basis, truth confidence, or automatic note promotion"
  cold_references:
    - raw/repos/2026-06-11-PaddlePaddle-PaddleOCR-source.md
    - raw/repos/_snapshots/2026-06-11-PaddlePaddle-PaddleOCR-71c7fef-source.zip
tags:
  - candidate
  - provisional
  - source-distillation
  - ocr
  - document-ai
  - source-intake
  - candidate-only
---

# 候选蒸馏：PaddleOCR

## 说人话

有帮助，而且是强相关，但位置要放准。

PaddleOCR **不是帮我们“存文档”的系统**。VAKS 仍然应该用文件、Markdown、
source card、候选蒸馏、review gate 来存和管知识。

PaddleOCR 真正有用的位置是：

```text
扫描件 / 图片 / PDF / 表格 / 公式 / 印章 / 图表
  -> 先解析成 Markdown / JSON / 坐标 / 页面结构
  -> 再进入 VAKS raw source + candidate intake
```

它是“入库前的文档解析器”，不是“资料库本体”。

## Candidate Point 1: PaddleOCR as pre-storage document parser

VAKS 对普通 Markdown、网页、代码仓库不需要 OCR。但对以下材料很有价值：

```text
扫描版 PDF
图片笔记
截图教程
带表格/公式/图表的论文或报告
OCR 质量不稳定的中文/英文混排资料
```

借鉴方式：

```text
original file retained
source hash recorded
PaddleOCR output saved as retained raw extraction
Markdown used for reading and candidate comprehension
JSON/coordinates used for audit, page anchors, and later review
```

不能做的事：

```text
OCR text != reviewed knowledge
OCR confidence != truth confidence
Markdown conversion != evidence support
layout order != reviewed relation
```

## Candidate Point 2: choose parser by document difficulty

PaddleOCR 的价值不是“一把梭都用最强 VLM”。更适合 VAKS 的路由是：

| Input type | Candidate route | Why |
|---|---|---|
| Clean text file / born-digital Markdown | skip OCR | OCR adds noise and cost |
| Simple screenshot / image text | PP-OCRv5 | light OCR, CPU/GPU both possible |
| Scanned PDF with layout/table/formula | PP-StructureV3 | structure-aware Markdown/JSON and coordinates |
| Complex layout, charts, rare chars, seals, hard table/formula pages | PaddleOCR-VL | stronger document VLM flow, but heavier |
| Agent-facing ad hoc extraction | MCP shape as reference | useful tool boundary, not immediate dependency |

This maps well to VAKS `light / medium / heavy` intake:

```text
light: simple OCR text capture
medium: Markdown + page metadata + source card
heavy: Markdown + JSON + coordinates + retained original + extraction ledger + review routing
```

## Candidate Point 3: preserve structure, not just text

The important alpha is structure preservation.

If a PDF page has:

```text
title
paragraph blocks
tables
formulas
figures
seals
sidebars
headers/footers
reading order
page coordinates
```

VAKS should not collapse it into one flat paragraph. The better bundle is:

```text
raw/original.pdf
raw/rendered-pages/page-001.png
raw/extraction/paddleocr.md
raw/extraction/paddleocr.json
raw/extraction/page-blocks.json
raw/extraction/extraction-meta.json
source card pointing to all retained artifacts
candidate distillation only after extraction
```

This preserves the future ability to ask:

```text
Where did this sentence come from?
Which page/block/table supported this candidate point?
Was the table parsed, inferred, or hallucinated?
Can a reviewer inspect the original visual source?
```

## Candidate Point 4: MCP and LangChain are adapter-shape references

The repo includes MCP and LangChain integration surfaces. For VAKS, the useful
part is not adopting their framework wholesale. The useful part is their adapter
shape:

```text
input file/URL
pipeline selection
parser config
Markdown output
images mapping
raw response metadata
tool boundary
```

This is directly relevant to future VAKS tools, but it should remain a
sandbox/reference until package compatibility and local runtime are checked.

## Candidate Point 5: PaddleOCR-VL needs full-flow discipline

The upstream docs warn that PaddleOCR-VL quality depends on the complete flow:

```text
layout analysis
element cropping / reading order
VLM recognition
merge into whole-page Markdown
```

For VAKS this becomes a hard boundary:

```text
Do not call a standalone VLM component and label it PaddleOCR-VL extraction.
Do not trust hallucinated text without original page anchors.
Do not promote extracted text without review.
```

## VAKS Mapping

| VAKS layer | Fit | Borrow |
|---|---:|---|
| Capture / Provenance | High | Preserve original file, hash, parser config, output Markdown/JSON. |
| Candidate Comprehension | High | Use OCR/parser output to summarize and route scanned documents. |
| Knowledge Calibration | Medium | Use page/block anchors to compare candidate points later. |
| Review / Consolidation | Indirect | Review must inspect original/source anchors, not only OCR text. |
| Association / Connect | Low-Medium | Coordinates/page anchors can help relation review, not create relations. |
| Activation / Dev Context | Medium | Parsed text makes scanned documents searchable. |
| Context Pack | Medium | Parsed Markdown can enter activation packs with warning labels. |
| Decision / Action | No | Needs independent evidence packet and review gate. |
| Feedback | Low | Extraction quality feedback can tune parser choice, not truth. |

## Borrow Gradient

```yaml
borrow_value: strong
borrow_order:
  - P1: use as scanned/image/PDF pre-storage parser candidate
  - P2: borrow adapter/config/output-bundle shape
  - P3: later benchmark against MarkItDown/MinerU/other parsers
```

The strongest borrow is not "PaddleOCR is accurate". The strongest borrow is:

```text
Visual document intake should preserve page structure and extraction metadata.
```

## Do Not Borrow

- Do not make PaddleOCR a storage backend.
- Do not auto-run it on every normal source.
- Do not treat OCR/VLM output as reviewed knowledge.
- Do not let OCR confidence become VAKS truth confidence.
- Do not let MCP/API output bypass source card and review queue boundaries.
- Do not add PaddleOCR-VL as a mainline dependency without a sandbox pilot.
- Do not trust `paddleocr-mcp` package compatibility until the observed PyPI
  dependency mismatch is tested.

## Pilot Shape

Minimum useful pilot:

```text
inputs:
  1 scanned Chinese PDF
  1 mixed Chinese/English screenshot
  1 table-heavy PDF page
  1 formula-heavy page if available

compare:
  PP-OCRv5
  PP-StructureV3
  PaddleOCR-VL only if hardware/runtime is acceptable

retain:
  original file hash
  rendered image/page hash when used
  extracted Markdown
  extracted JSON/coordinates
  parser config
  runtime / device / package versions
  known failures

pass gate:
  source-card can point to real project-visible artifacts
  extracted Markdown is readable enough for candidate comprehension
  JSON/coordinates can support later reviewer drilldown
  output never claims action-basis or reviewed truth
```

## Open Questions

- On this Windows machine, which PaddlePaddle package path is actually stable:
  CPU, CUDA, or container?
- Does PP-StructureV3 give enough coordinates/page anchors for our review needs?
- Does PaddleOCR-VL hallucinate on our likely Chinese/English mixed documents?
- Should VAKS prefer MarkItDown first for born-digital Office/PDF, then
  PaddleOCR only when text extraction is missing or visually structured?
- Can a small local adapter produce a clean VAKS artifact bundle without pulling
  LangChain/MCP into the core?

## Current Judgment

```yaml
direct_use: no_for_storage_yes_for_sandbox_parser
fork: no
design_only: yes_for_adapter_contract
implementation_next: sandbox_pilot_only
mainline_change_now: no
reviewed_knowledge_created: false
action_basis_allowed: false
truth_mutation_allowed: false
```
