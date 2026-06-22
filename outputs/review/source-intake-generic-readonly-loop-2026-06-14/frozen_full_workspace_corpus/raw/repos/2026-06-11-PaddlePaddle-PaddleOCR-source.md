---
type: source
record_kind: source_card
status: source-captured
title: "PaddlePaddle/PaddleOCR"
source_id: 2026-06-11-PaddlePaddle-PaddleOCR-source
source_uri: https://github.com/PaddlePaddle/PaddleOCR
source_url: https://github.com/PaddlePaddle/PaddleOCR
source_type: repository
author: PaddlePaddle
publisher: GitHub / PyPI
created_at: 2020-05-08T10:38:16Z
captured_at: 2026-06-11
captured_by: Codex
version_or_commit: 71c7fefbf5e8478bc7f14b2d9b095bb80580178b
release_version_checked: paddleocr 3.6.0
release_checked_at: 2026-06-11
processing_tier: heavy
review_priority: high
review_owner: Codex
formalization_status: candidate-generated
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
source_integrity:
  repository_head: 71c7fefbf5e8478bc7f14b2d9b095bb80580178b
  repository_head_date: 2026-06-10T14:21:02Z
  snapshot_location: raw/repos/_snapshots/2026-06-11-PaddlePaddle-PaddleOCR-71c7fef-source.zip
  snapshot_sha256: 7EC1D91C0A3F2426C05442115CA2F22206E63DFB6F6BC5684CFB56FCEE1AEA3B
  snapshot_size_bytes: 118060629
adapter_ingest:
  adapter_name: GitHub API + git ls-remote + codeload snapshot + PyPI JSON
  adapter_version: manual-codex-2026-06-11
  capture_method: repository metadata, default-branch commit, source snapshot, README/docs/source inspection, package metadata
  extraction_trace:
    - GitHub repository metadata checked 2026-06-11.
    - git ls-remote checked HEAD and tags on 2026-06-11.
    - codeload snapshot downloaded for commit 71c7fefbf5e8478bc7f14b2d9b095bb80580178b.
    - README, pyproject, pipeline docs, MCP docs, LangChain loader, MCP task adapters, and pipeline source files inspected.
    - PyPI package metadata checked for paddleocr, paddleocr-mcp, and langchain-paddleocr.
  known_limits:
    - Models were not installed or executed locally.
    - Benchmark and accuracy claims remain upstream-published claims, not VAKS-verified results.
    - GitHub stars and PyPI metadata are point-in-time facts captured on 2026-06-11.
    - paddleocr-mcp PyPI 0.8.4 declared a dependency on paddleocr>=3.7.0 while PyPI lookup found paddleocr 3.6.0 as latest and paddleocr 3.7.0 unavailable; treat MCP package usability as unverified.
source_status: active
raw_location: raw/repos/_snapshots/2026-06-11-PaddlePaddle-PaddleOCR-71c7fef-source.zip
topics:
  - document-ai
  - ocr
  - document-parsing
  - pdf-to-markdown
  - pdf-to-json
  - structure-extraction
  - mcp
  - langchain-loader
  - source-intake
  - scanned-document-ingest
projects:
  - verified-action-knowledge-system
source_family: PaddleOCR
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - source/repo
  - source/pypi
  - topic/ocr
  - topic/document-ai
  - topic/source-intake
  - candidate-only
why_saved: see_body_or_legacy_record
---

# PaddleOCR Source Record

## Why Captured

The user asked whether PaddleOCR helps VAKS store documents and explicitly said
"先蒸馏". This record preserves the source identity and inspection anchors.

Plain-language boundary:

```text
PaddleOCR can help before storage.
It can turn scanned PDFs/images into Markdown/JSON plus layout artifacts.
It should not become the VAKS storage layer, truth layer, or review layer.
```

## Source Identity

```yaml
repository: https://github.com/PaddlePaddle/PaddleOCR
repository_head_checked: 71c7fefbf5e8478bc7f14b2d9b095bb80580178b
repository_head_date: 2026-06-10T14:21:02Z
license: Apache-2.0
default_branch: main
github_stars_checked: 81745
github_forks_checked: 10722
github_open_issues_checked: 214
pypi_paddleocr_version_checked: 3.6.0
pypi_paddleocr_requires_python: ">=3.8"
pypi_paddleocr_upload_time: 2026-05-28T11:43:29.473061Z
```

Key entity note:

```text
The upstream docs use "PaddleOCR-VL-1.6" for the document parsing pipeline/model
release and also explain that "PaddleOCR-VL-0.9B" is the VLM component inside
the complete PaddleOCR-VL flow. Do not collapse the complete document parsing
pipeline into a standalone VLM call.
```

## Inspected Repository Areas

| Anchor | What exists | Why it matters for VAKS | Boundary |
|---|---|---|---|
| `README.md` | Positions PaddleOCR as PDF/image to structured JSON/Markdown; lists PP-OCRv5, PP-StructureV3, PaddleOCR-VL, MCP/LangChain ecosystem. | Confirms document-intake relevance from primary source. | README claims are source claims, not VAKS verification. |
| `pyproject.toml` | Package `paddleocr`, Python `>=3.8`, Apache 2.0, core dependency `paddlex[ocr-core]`, optional `doc-parser`, `ie`, `trans`, `doc2md`. | Shows dependency split between basic OCR and heavier document parsing. | Installation feasibility not tested. |
| `docs/version3.x/pipeline_usage/OCR.md` | General OCR pipeline, PP-OCRv5 defaults, CPU/GPU device config, text boxes and recognition thresholds. | Useful for light scanned-text capture and OCR confidence/coordinate retention. | OCR text is raw extraction, not reviewed evidence. |
| `docs/version3.x/pipeline_usage/PP-StructureV3.md` | Layout parsing pipeline with OCR, preprocessor, table, seal, formula, chart, reading-order and Markdown conversion. | Best fit for local PDF/image-to-Markdown preprocessing. | Upstream accuracy tables are not VAKS adoption proof. |
| `docs/version3.x/pipeline_usage/PaddleOCR-VL.md` | Complete flow combines layout analysis and VLM recognition; supports CLI/Python, JSON/Markdown save, PDF/image input, hardware matrix. | Useful for complex document parsing where tables, formulas, charts, seals, and reading order matter. | CPU use may be slow; full flow required to avoid hallucination/quality mismatch. |
| `paddleocr/_pipelines/pp_structurev3.py` | `PPStructureV3` wrapper exposes optional table, formula, chart, seal, OCR, layout, and Markdown-ignore settings. | Suggests a configurable intake adapter rather than one fixed OCR mode. | Do not import upstream config directly into VAKS schema. |
| `paddleocr/_pipelines/paddleocr_vl.py` | `PaddleOCRVL` wrapper exposes pipeline versions, layout detection, chart/seal recognition, queues, Markdown concatenation and restructuring. | Important for long PDF/page restructuring experiments. | VLM output can hallucinate; retain raw images/PDF and extraction metadata. |
| `mcp_server/` and `docs/version3.x/integrations/mcp_server.md` | MCP tools for OCR, PP-StructureV3, and PaddleOCR-VL with local/API/self-hosted modes. | Design reference for a future VAKS document-ingest adapter or operator tool. | PyPI package metadata currently needs compatibility verification. |
| `langchain-paddleocr/` | LangChain document loader for PaddleOCR-VL, returning text plus raw response metadata. | Design reference for source-to-document loader shape and provenance metadata. | LangChain integration is not required for VAKS. |

## Initial Takeaways

- PaddleOCR is relevant to VAKS primarily as a **document intake parser**.
- For born-digital Markdown/TXT/HTML, it is unnecessary overhead.
- For scanned PDFs, photos, screenshots, handwritten notes, formulas, tables,
  seals, charts, and page layout, it is a strong candidate parser.
- The most VAKS-aligned output is not just text; it is:

```text
original file path/hash
rendered page/image references
OCR or parsing output Markdown
structured JSON
page/block/table/formula coordinates
model/version/config metadata
known extraction limits
```

## Obvious Doubts

- Local runtime cost and Windows/CUDA behavior were not tested.
- PaddleOCR-VL is heavier than ordinary source intake needs.
- CPU is acceptable for basic OCR, but upstream docs warn that PaddleOCR-VL CPU
  use may be slow and production use should use a proper inference service.
- MCP package metadata showed a version mismatch that needs a separate install
  check before treating the MCP server as usable.
- OCR/Doc-VLM output must be quarantined as raw extraction, not reviewed truth.

## Candidate Points

```yaml
candidate_points:
  - id: paddleocr-as-pre-storage-parser
    summary: Use PaddleOCR before storage for scanned/image/PDF documents, then store extracted Markdown/JSON as raw/candidate artifacts with original provenance.
  - id: structure-aware-intake-bundle
    summary: Preserve Markdown plus JSON/coordinates/page metadata instead of flattening everything into plain text.
  - id: pipeline-choice-gate
    summary: Use PP-OCRv5 for simple OCR, PP-StructureV3 for structured document parsing, and PaddleOCR-VL only for complex layout/VLM needs.
  - id: mcp-loader-design-reference
    summary: MCP and LangChain integrations are useful adapter-shape references, but not immediate VAKS dependencies.
```

## Current Processing Level

```text
heavy repo/library intake
candidate-only
no reviewed knowledge
no action basis
no truth mutation
```

## Next Step

If the user wants implementation later, run a sandbox-only pilot on 3-5 local
documents:

```text
1 scanned PDF
1 screenshot/article image
1 table-heavy PDF
optional: formula-heavy page
optional: Chinese/English mixed page
```

Measure extraction quality, coordinates, model metadata, runtime, file size, and
whether the result can cleanly fit VAKS source-card + retained raw text rules.
