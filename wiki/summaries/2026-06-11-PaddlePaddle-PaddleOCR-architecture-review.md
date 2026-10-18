---
type: summary
status: draft
title: "PaddleOCR architecture review for VAKS document intake"
created: 2026-06-11
source:
  - raw/repos/2026-06-11-PaddlePaddle-PaddleOCR-source.md
source_repo: https://github.com/PaddlePaddle/PaddleOCR
source_commit: 71c7fefbf5e8478bc7f14b2d9b095bb80580178b
related_patterns: []
related_decisions: []
confidence: medium
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
fusion_decision: adapt-after-sandbox
tags:
  - summary
  - architecture-review
  - candidate-only
  - document-intake
  - ocr
  - document-ai
---

# PaddleOCR 架构评审：VAKS 文档入库解析候选

## 一句话判断

PaddleOCR 对 VAKS **有强帮助**，但帮助点是“文档入库前解析”，不是“存储知识”。

最小正确融合是：

```text
VAKS keeps Markdown/source cards/review gates as authority.
PaddleOCR may become a sandboxed parser for scanned PDFs/images.
Parser output stays raw/candidate until later review.
```

## It Solves

PaddleOCR solves visual document understanding:

```text
image/PDF text recognition
layout detection
table recognition
formula recognition
seal recognition
chart parsing
reading-order recovery
Markdown/JSON output
MCP/API/loader integration surfaces
```

This is exactly the gap VAKS has for non-textual documents:

```text
plain Markdown/html/code -> already easy
scanned PDFs/images/screenshots -> need parser before VAKS can reason
```

## Core Design

The repo is better understood as layered pipelines:

```text
PP-OCRv5:
  general OCR, text boxes, recognition scores, multilingual text.

PP-StructureV3:
  structure-aware document parsing, tables/formulas/seals/charts/layout,
  Markdown/JSON conversion and finer coordinates.

PaddleOCR-VL:
  heavier document VLM flow: layout analysis + element VLM recognition +
  reading-order merge into full-page Markdown/structured output.

MCP / LangChain / API:
  adapter surfaces, not core truth stores.
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | Official positioning as OCR toolkit and document AI engine that converts PDFs/images into JSON/Markdown. | Confirms VAKS source-intake relevance. | README claims are not independent validation. |
| `pyproject.toml` | Core `paddleocr` package, optional `doc-parser`, `ie`, `trans`, `doc2md`. | Dependency split suggests VAKS should not install heavy parser by default. | Package install not tested. |
| `docs/version3.x/pipeline_usage/OCR.md` | PP-OCRv5 OCR pipeline, device config, thresholds, word boxes. | Good for simple OCR extraction and confidence/coordinate retention. | Raw OCR text only. |
| `docs/version3.x/pipeline_usage/PP-StructureV3.md` | Layout parsing plus optional table, formula, seal, chart, reading order and Markdown conversion. | Best default candidate for structured scanned PDF intake. | Accuracy claims remain upstream. |
| `docs/version3.x/pipeline_usage/PaddleOCR-VL.md` | Complete document-VL flow, hardware matrix, CLI/Python API, JSON/Markdown save. | Useful for hard documents and page restructuring. | Requires full flow; CPU may be too slow. |
| `paddleocr/_pipelines/pp_structurev3.py` | Configurable wrapper for layout, chart, table, formula, seal, OCR, Markdown ignore labels. | VAKS adapter should expose parser config and save it with output. | Do not copy upstream config into schema. |
| `paddleocr/_pipelines/paddleocr_vl.py` | Versioned VL pipeline, layout/VLM settings, queues, Markdown concat/restructure methods. | Long-document parsing should be page-aware and reconstructable. | VLM can hallucinate; raw page anchors required. |
| `mcp_server/paddleocr_mcp/tasks/doc_parsing.py` | MCP task formats parsing results as Markdown and optional image content. | Tool boundary design reference. | Tool output cannot bypass VAKS intake boundary. |
| `mcp_server/paddleocr_mcp/inference/shared/doc_parsing_result_adapters.py` | Adapts local/API parsing results into Markdown + page count + image mapping. | Strong model for VAKS retained extraction bundle. | Package compatibility not proven. |
| `langchain-paddleocr/langchain_paddleocr/document_loaders/paddleocr_vl.py` | Loader emits LangChain `Document` with page content and raw response metadata. | Metadata-preserving loader shape is useful. | VAKS need not use LangChain. |

## Current Branch Value

Current local concern: source intake and document storage.

```yaml
supports: source-intake, retained-raw-text, document-parser-bundle
refines: light/medium/heavy intake routing
risk_of: parser output being over-credited as reviewed knowledge
```

Value:

- Strong for scanned/image/PDF intake.
- Medium for future agent/MCP tool design.
- Low for born-digital Markdown or already-readable text.

Risk:

- Overuse would make ordinary capture heavy.
- VLM output may hallucinate.
- Package/runtime complexity can create friction.
- OCR output can look authoritative while still being extraction-only.

## Whole Architecture Value

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Helps `ingest` convert visual docs to Markdown, but should not change raw/wiki/index/log spine. | adapt |
| Dusk workbench | Could power a future "parse this document" tool surface. | watch |
| source ingest | Strong fit for parser bundles, source hash, extraction metadata, and retained Markdown/JSON. | adapt |
| review queue | Can produce candidate points with page/block anchors. | adapt |
| schema / reviewed knowledge | No direct schema authority. | reject |
| memory / dev context | Parsed text can become support/cold reference. | adapt |
| feedback | Extraction-quality feedback can tune parser choice. | watch |
| retrieval / cache | Makes scanned docs searchable after extraction. | adapt |
| API / MCP / agent access | MCP server is a useful adapter reference. | watch |
| viewer / workbench | Page images + Markdown/JSON could support reviewer drilldown. | watch |
| publishing | Could help convert complex PDFs into drafts, later only. | watch |
| risk / anti-pattern | OCR/VLM output must not become truth or action basis. | adopt as guardrail |

## Extracted Patterns

### 1. Parser as quarantine boundary

The parser should sit before candidate distillation:

```text
source file -> extraction bundle -> candidate comprehension -> review
```

Not:

```text
source file -> PaddleOCR -> reviewed note
```

### 2. Structure-aware retained raw text

Store Markdown and JSON/coordinates together. Markdown helps humans and agents
read. JSON/coordinates help review and traceability.

### 3. Lazy parser escalation

Escalate by need:

```text
normal text extraction first
PP-OCRv5 for simple image text
PP-StructureV3 for layout-heavy docs
PaddleOCR-VL for complex document understanding
```

This preserves VAKS's "strict only when needed" design.

### 4. Adapter surface before runtime adoption

The MCP and LangChain layers are useful mostly as interface examples:

```text
input path
pipeline
config
Markdown
images mapping
raw response metadata
tool/runtime mode
```

Do not adopt framework dependencies until a sandbox proves they are worth it.

## Tags And Quantification

- domain: document AI / OCR / document parsing
- problem: visual documents are hard to ingest into a text-first vault
- pattern: pre-storage parser with retained source/extraction bundle
- maturity: proven project, local fit untested
- complexity: high for VL, medium for PP-StructureV3, low-medium for OCR
- problem_fit: 5/5 for scanned documents, 1/5 for normal text notes
- reuse_value: 5/5 for parser bundle design
- implementation_cost: 4/5 if local VL, 2/5 if simple OCR pilot
- integration_fit: 4/5 as sandbox adapter, 2/5 as core dependency
- evidence_strength: 3/5 for design fit, 1/5 for local runtime
- reversibility: 5/5 if kept as derived extraction bundle

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| OCR/parser output should be raw extraction only. | SOURCE_INTAKE says source records/raw extraction are provenance and candidate inputs, not truth. | candidate_relation | Can lint detect OCR-derived Markdown being promoted without original anchors? |
| Use structure-aware Markdown/JSON bundles. | VAKS already values source anchors and retained raw text. | refines | What minimum metadata is enough without making every intake heavy? |
| PaddleOCR-VL can parse complex pages. | Evidence support must be source-span/anchor specific. | scope_mismatch | How do we expose visual/page anchors for reviewer drilldown? |
| MCP can expose parsing to agents. | Agent memory/write quarantine forbids direct truth mutation. | risk_candidate | Should future MCP parser tools write only to staging/candidate folders? |

Boundary:

- Similarity to VAKS needs is not adoption.
- Upstream benchmarks are not local sufficiency.
- OCR text can support reading, but not reviewed evidence without source anchors.

## Support / Challenge Review

What supports the candidate:

- Official repo and docs expose OCR, PP-StructureV3, PaddleOCR-VL, MCP, and
  loader surfaces.
- Source code contains configurable pipelines and adapters for Markdown output.
- License is Apache-2.0.
- Project is active and high-usage by GitHub metadata.

What challenges it:

- No local install/runtime test.
- PaddleOCR-VL is resource-heavy relative to ordinary intake.
- MCP package compatibility looked inconsistent in PyPI metadata.
- VLM extraction can hallucinate if used outside the complete flow.
- OCR quality varies by source type and language.

Challenge severity:

```yaml
local_runtime_unknown: major
truth_boundary_risk: major
mcp_package_mismatch: minor_to_major_for_mcp_only
ordinary_intake_overhead: major_if_overused
license_risk: minor
```

Action readiness:

```yaml
action_readiness: not_ready
ready_for: sandbox_pilot
not_ready_for: mainline_dependency_or_action_basis
```

## Fusion Judgment

Conclusion:

```yaml
fusion_decision: adapt-after-sandbox
direct_use: no_for_storage_yes_for_parser_pilot
fork: no
design_only: yes_for_adapter_contract
reject: no
current_branch_value: strong
whole_architecture_value: medium_high
risk: over-crediting_parser_output
next_action: sandbox_pilot_only
```

The fused VAKS version should be smaller than PaddleOCR:

```text
one parser adapter contract
one extraction bundle shape
one parser-choice gate
one local pilot
no new truth layer
no mainline dependency yet
```

## Minimal Adoption Shape

If later approved:

```text
tools/document-intake/
  parse-local-document.ps1 or python adapter
  input: local PDF/image only
  output: retained Markdown + JSON + metadata under raw/<source>/
  policy: no cloud API by default
  policy: source card remains raw
  policy: candidate distillation only after extraction
  policy: action_basis_allowed false
```

Do not build:

```text
automatic OCR for every note
always-on MCP parser
automatic source promotion
PaddleOCR-backed truth/confidence layer
```
