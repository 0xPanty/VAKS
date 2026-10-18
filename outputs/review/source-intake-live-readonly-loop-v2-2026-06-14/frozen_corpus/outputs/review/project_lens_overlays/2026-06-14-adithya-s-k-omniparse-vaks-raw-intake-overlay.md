---
record_kind: project_overlay
type: project_lens_overlay
status: candidate
knowledge_status: candidate
processing_tier: heavy
overlay_state: confirmed
review_pressure: none
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
project_name: "Verified Action Knowledge System / 资料库"
target_ref: "outputs/review/2026-06-14-adithya-s-k-omniparse-strong-distillation.md"
target_selector: candidate_distillation
target_hint:
  - type: workflow
    value: "source-intake/raw-material-parser-router"
    status: conceptual
    anchor_version: candidate-workflow-only
  - type: source_card
    value: "raw/repos/2026-06-14-adithya-s-k-omniparse-source.md"
    status: healthy
    anchor_version: "2026-06-14"
  - type: repo_snapshot
    value: "raw/repos/_snapshots/2026-06-14-adithya-s-k-omniparse-9d1ae83-source.zip"
    status: healthy
    anchor_version: "sha256:DB4E281447FC53BD3122EA20064017B6309AFCB9548CA174A52C888036DF9A2E"
project_borrow_scope:
  - "Use OmniParse as a design reference for a VAKS raw intake parser router across documents, images, audio, video, and public web pages."
  - "Borrow lazy modality loading and external parser-service isolation."
  - "Wrap parser output into a VAKS-owned extraction bundle with original hash, parser config, retained Markdown/JSON/images/chunks, anchors, known limits, and boundary flags."
  - "Compare OmniParse with PaddleOCR and RAG-Anything before choosing parser backends."
project_non_borrow_scope:
  - "For VAKS, do not currently borrow OmniParse as the vault storage layer, reviewed knowledge layer, review engine, or action-basis generator because parser output is raw/candidate material only."
  - "For VAKS, do not embed OmniParse/Marker-derived code into product code before license review because repository license signals include GPL-3.0 and commercial model-weight caveats."
  - "For VAKS, do not enable always-on document/media/web parsing because ordinary capture should stay light and strict parsing should be lazy."
  - "For VAKS, do not enable private/account web crawling by default because it would break source-intake and privacy boundaries."
project_reopen_trigger:
  - "User asks to implement a VAKS raw intake adapter or plugin."
  - "A real raw-material batch needs unified parsing beyond current Markdown/video/source-card flow."
  - "Sandbox benchmarks compare OmniParse, PaddleOCR, MarkItDown, and RAG-Anything-style element manifests."
  - "License, runtime, and output-anchor requirements are clarified."
confirmation_basis:
  - "User explicitly requested strong distillation and asked whether it can help organize raw materials."
  - "Official repo, raw source files, GitHub API metadata, and commit snapshot were inspected."
last_checked_at: "2026-06-14"
expires_at: null
borrow_value: strong
borrow_order:
  - "P1: raw intake parser router and extraction bundle workflow"
  - "P2: lazy parser service / modality flags"
  - "P3: sandbox comparison target for future plugin design"
avoid:
  - "No parser output as reviewed truth."
  - "No action basis from OmniParse Markdown."
  - "No direct product embedding before license review."
  - "No always-on heavy parser for ordinary notes."
  - "No private web crawling without explicit authorization."
tags:
  - project-lens
  - VAKS
  - raw-intake
  - parser-adapter
  - omniparse
  - candidate-only
legacy_overlay_compatibility: true
canonical_p0_included: false
canonical_current_lint_scope: false
legacy_storage: outputs/review/project_lens_overlays
truth_boundary: "project lens compatibility artifact only; not canonical reviewed knowledge; not action basis"
---

# Project Lens: OmniParse as VAKS Raw Intake Parser Router

## Boundary

This is a project-scoped sidecar. It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide future VAKS raw-intake design, but it cannot act as reviewed knowledge or action basis.

## Project Borrow Scope

For VAKS, borrow OmniParse narrowly:

```text
Use it as a reference for organizing messy raw inputs before they enter VAKS review.
```

Concrete borrow:

- One parser-router interface for documents, images, audio, video, and public web.
- Lazy parser loading by modality.
- External parser service isolation for heavy dependencies.
- Minimal response concept: `text / images / metadata / chunks`.
- Local-first parsing as default posture.

VAKS-specific wrapper:

```text
OmniParse-like output
  -> VAKS extraction bundle
  -> source card
  -> candidate distillation
  -> review only when needed
```

Preferred artifact bundle:

```text
raw/<source>/original.<ext>
raw/<source>/source-metadata.json
raw/<source>/extraction/parser-output.md
raw/<source>/extraction/parser-output.json
raw/<source>/extraction/images/
raw/<source>/extraction/chunks.json
raw/<source>/extraction/extraction-meta.json
raw/<source>.md source card
outputs/review/<source>-candidate-distillation.md
```

## Project Non-Borrow Scope

Do not borrow:

- OmniParse as VAKS storage backend.
- OmniParse as reviewed knowledge layer.
- Parser Markdown as evidence support.
- Parser confidence or clean formatting as truth confidence.
- Always-on heavy parser for ordinary notes.
- Web crawling for private/account pages without explicit approval.
- Direct GPL/Marker-derived code into product code before license review.

## Reopen Trigger

Reopen this overlay when:

```text
VAKS starts raw-intake adapter implementation.
The user gives real PDFs/images/audio/video/web pages to batch organize.
We need a sandbox comparison between OmniParse, PaddleOCR, MarkItDown, and RAG-Anything-style manifests.
License/runtime constraints are cleared enough for a pilot.
```

## Minimal Pilot Gate

```yaml
pilot_scope: sandbox_only
inputs:
  - clean_pdf
  - scanned_chinese_pdf
  - screenshot_image
  - short_audio_or_video
  - public_web_page
checks:
  - original_file_hash_retained
  - parser_config_saved
  - output_markdown_retained
  - output_json_or_metadata_retained
  - image_page_region_or_timestamp_anchors_retained
  - source_card_points_to_project_visible_artifacts
  - action_basis_allowed_false
  - truth_mutation_allowed_false
  - runtime_memory_and_os_recorded
pass_result:
  - candidate_adapter_contract
fail_result:
  - keep_as_design_reference_only
```

## Confirmation

```yaml
confirmation_basis:
  user_request: "强蒸馏这个 可以帮我们整理raw资料？"
  inspected_source:
    - raw/repos/2026-06-14-adithya-s-k-omniparse-source.md
    - raw/repos/_snapshots/2026-06-14-adithya-s-k-omniparse-9d1ae83-source.zip
  conclusion: "strong raw-intake router reference, not VAKS authority layer"
last_checked_at: 2026-06-14
```
