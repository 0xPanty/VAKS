---
record_kind: project_overlay
type: project_lens_overlay
status: candidate
knowledge_status: candidate
processing_tier: heavy
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: VAKS
project_name: Verified Action Knowledge System / 资料库
target_ref: outputs/review/2026-06-11-PaddlePaddle-PaddleOCR-candidate-distillation.md
target_selector: candidate_distillation
target_hint:
  - type: workflow
    value: source-intake/scanned-document-parser
    status: conceptual
    anchor_version: candidate-workflow-only
  - type: doc
    value: SOURCE_INTAKE.md#Processing Levels
    status: healthy
    anchor_version: 2026-06-11-file-read
  - type: repo_snapshot
    value: raw/repos/_snapshots/2026-06-11-PaddlePaddle-PaddleOCR-71c7fef-source.zip
    status: healthy
    anchor_version: sha256:7EC1D91C0A3F2426C05442115CA2F22206E63DFB6F6BC5684CFB56FCEE1AEA3B
project_borrow_scope:
  - Use PaddleOCR as a candidate pre-storage parser for scanned PDFs, images, screenshots, table/formula-heavy pages, and visually structured documents.
  - Preserve original file hash, parser config, extracted Markdown, JSON/coordinates, page/image anchors, and extraction metadata.
  - Route parser choice lazily: text extraction first, PP-OCRv5 for simple OCR, PP-StructureV3 for structured layout, PaddleOCR-VL for complex document understanding.
  - Borrow MCP/loader adapter shape only as a future tool-interface reference.
project_non_borrow_scope:
  - Do not replace VAKS storage with PaddleOCR or any OCR runtime.
  - Do not treat OCR confidence, VLM output, Markdown conversion, layout order, or parser benchmarks as reviewed truth.
  - Do not enable cloud/API parsing by default for private local documents.
  - Do not add PaddleOCR-VL or paddleocr-mcp as mainline dependencies before a sandbox install/runtime pilot.
project_reopen_trigger:
  - User asks to implement scanned-document intake.
  - A local document pilot shows PP-StructureV3/PaddleOCR-VL produces clean retained artifacts with acceptable runtime.
  - VAKS needs page/block coordinate anchors for evidence review.
  - paddleocr-mcp package compatibility is verified or fixed upstream.
confirmation_basis:
  - user explicitly said "先蒸馏"
  - source card and candidate distillation created from official repo snapshot and PyPI metadata
last_checked_at: 2026-06-11
expires_at:
borrow_value: strong
borrow_order:
  - "P1: parser bundle contract for scanned/image/PDF source intake"
  - "P2: PP-StructureV3 as likely first sandbox candidate"
  - "P3: PaddleOCR-VL only for hard cases after runtime check"
avoid:
  - "No truth mutation from parser output."
  - "No automatic promotion from OCR-derived Markdown."
  - "No cloud/API use for private docs without explicit authorization."
tags:
  - project-lens
  - VAKS
  - document-intake
  - ocr
  - candidate-only
---

# Project Lens: PaddleOCR as VAKS Document Intake Parser

## Boundary

This is a project-scoped sidecar. It does not rewrite the source card,
candidate distillation, reviewed note, decision, or pattern.

It can guide VAKS document-intake experiments, but it cannot act as reviewed
knowledge or action basis.

## Project Borrow Scope

For VAKS, borrow PaddleOCR narrowly:

```text
Use it before storage when the source is visual or scanned.
Keep storage and authority in VAKS files and review gates.
```

Concrete borrow:

- `PP-OCRv5`: simple image/screenshot text extraction.
- `PP-StructureV3`: first candidate for structured scanned PDF parsing.
- `PaddleOCR-VL`: hard-case parser for complex layout, formula/table/chart/seal pages.
- MCP/LangChain surfaces: reference shapes for future adapter tools.

Preferred artifact bundle:

```text
raw/<source>/original.<ext>
raw/<source>/source-metadata.json
raw/<source>/extraction/paddleocr.md
raw/<source>/extraction/paddleocr.json
raw/<source>/extraction/page-blocks.json
raw/<source>/extraction/extraction-meta.json
raw/<source>.md source card
outputs/review/<source>-candidate-distillation.md
```

## Project Non-Borrow Scope

Do not borrow:

- PaddleOCR as vault/storage backend.
- OCR/VLM output as reviewed evidence.
- Parser confidence as truth confidence.
- OCR-derived Markdown as action basis.
- Always-on OCR for ordinary notes.
- Cloud parsing for private documents unless explicitly approved.
- Mainline dependency before local pilot.

## Reopen Trigger

Reopen this overlay when:

```text
VAKS starts a scanned-document intake implementation.
The user gives real local PDFs/images to process.
We need page/block anchors for evidence review.
A package/runtime pilot proves stable enough on this machine.
```

## Minimal Pilot Gate

```yaml
pilot_scope: sandbox_only
inputs:
  - scanned_chinese_pdf
  - mixed_cn_en_screenshot
  - table_heavy_pdf_page
  - optional_formula_page
checks:
  - readable_markdown
  - retained_original_hash
  - retained_json_or_coordinates
  - parser_config_saved
  - runtime_and_device_recorded
  - no_action_basis_fields_true
  - source_card_points_to_project_visible_artifacts
pass_result:
  - candidate_adapter_contract
fail_result:
  - keep_as_reference_only
```

## Confirmation

```yaml
confirmation_basis:
  user_request: "直接看看这个库 对我们存文档有没有帮助 先蒸馏"
  inspected_source:
    - raw/repos/2026-06-11-PaddlePaddle-PaddleOCR-source.md
    - raw/repos/_snapshots/2026-06-11-PaddlePaddle-PaddleOCR-71c7fef-source.zip
  conclusion: "strong candidate for pre-storage parser, not storage authority"
last_checked_at: 2026-06-11
```
