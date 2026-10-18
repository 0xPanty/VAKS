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
target_ref: outputs/review/2026-06-12-bilibili-apex-knowledge-schema-rag-candidate-distillation.md
target_selector: candidate_distillation
target_hint:
  - type: retrieval-layer
    value: schema-first-document-intake
    status: P1-candidate
    anchor_version: 2026-06-12-video-source
  - type: retrieval-layer
    value: structured-object-plus-semantic-brief
    status: P1-candidate
    anchor_version: 2026-06-12-video-source
  - type: risk
    value: extracted-object-as-false-authority
    status: active-risk-reference
    anchor_version: 2026-06-12-source-capture
  - type: doc
    value: outputs/review/vaks-retrieval-layer-design-2026-06-11/
    status: candidate-workspace
    anchor_version: 2026-06-12-file-read
project_borrow_scope:
  - Borrow schema-first document intake for vertical business documents.
  - Borrow structured object plus semantic brief as a dual representation.
  - Borrow natural-language query to object-query translation before vector rerank.
  - Borrow object-level retrieval as a complement to chunk retrieval, not a replacement for review.
  - Borrow cross-schema relation only as candidate relation suggestions.
project_non_borrow_scope:
  - Do not treat extracted JSON fields as reviewed knowledge.
  - Do not let semantic briefs count as evidence support.
  - Do not map object-query hits to action basis.
  - Do not let dynamic schema learning mutate the main schema without review.
  - Do not create reviewed relations from BOM/cross-schema links automatically.
  - Do not treat product-demo claims as independent validation.
project_reopen_trigger:
  - VAKS designs document-intake parser output beyond Markdown summary.
  - VAKS retrieval layer needs object-aware retrieval or schema field filters.
  - VAKS builds Evidence Packet prefill from contracts, policies, papers, drawings, logs, or reports.
  - User asks whether VAKS should implement Apex Knowledge-style schema extraction.
confirmation_basis:
  - user explicitly said "强蒸馏"
  - public Bilibili metadata captured without cookies
  - public subtitles empty; public audio transcribed locally with faster-whisper small on CUDA
  - transcript artifacts retained under raw/videos and source card points to project-visible files
last_checked_at: 2026-06-12
expires_at:
borrow_value: strong
borrow_order:
  - "P1: schema-first document intake for vertical business documents"
  - "P1: structured object plus semantic brief"
  - "P1: object-query route before vector rerank"
  - "P2: cross-schema candidate relation"
  - "P3: dynamic schema learning and multimodal parser"
avoid:
  - "No extracted-object-as-truth."
  - "No brief-as-evidence."
  - "No object hit as action basis."
  - "No automatic schema mutation."
tags:
  - project-lens
  - VAKS
  - retrieval-layer
  - document-intake
  - schema-extraction
  - structured-retrieval
  - candidate-only
---

# Project Lens: Apex Knowledge Schema RAG for VAKS

## Boundary

This is a project-scoped sidecar. It does not rewrite the source card,
candidate distillation, reviewed note, decision, or pattern.

It can guide future VAKS document-intake and retrieval-layer design, but it
cannot act as reviewed knowledge or action basis.

## Project Borrow Scope

For VAKS, borrow the source as a P1 retrieval/document-intake reference:

```text
Use schema-first extraction for vertical documents.
Use object retrieval as an activation path.
Do not borrow the authority model.
```

Concrete borrow:

- Use a domain Schema before chunking when the document has strong business structure.
- Preserve structured object and semantic brief as separate artifacts.
- Require field-level source anchors for extracted objects.
- Convert natural language query into object constraints where possible.
- Keep cross-document/BOM/product relations as candidate relation suggestions.
- Feed corrected extraction/query failures into maintenance and extractor improvement, not truth mutation.

## Project Non-Borrow Scope

Do not borrow:

- Extracted JSON as reviewed truth.
- Brief as evidence support.
- Vector score or object hit as confidence.
- Product demo claims as validation.
- Direct Agent execution from candidate objects.
- Dynamic Schema learning without versioning and human review.
- Cross-Schema relation as reviewed relation.

## Reopen Trigger

Reopen this overlay when:

```text
VAKS designs document-intake parser output.
VAKS retrieval layer needs object-aware filtering.
VAKS creates an Evidence Packet prefill workflow.
VAKS tests contracts / policies / papers / logs / reports as structured candidate objects.
```

## Minimal Pilot Shape

```yaml
pilot_scope: sandbox_only
first_candidate_document_type: policy_or_contract_or_repo_readme
schema_size: 5_to_8_fields
required_outputs:
  - raw source retained
  - extracted candidate object
  - field-level source anchors
  - semantic brief
  - extraction receipt
  - query translation receipt
checks:
  - object fields never marked reviewed
  - brief only used for activation
  - source anchors present for important fields
  - reviewed/action-basis use blocked without later gate
  - boundary violation count measured
compare_against:
  - ordinary chunk retrieval
  - vector-only retrieval
  - schema object query plus brief rerank
pass_result:
  - candidate document-intake pattern
fail_result:
  - keep as design-only reference
```

## Confirmation

```yaml
confirmation_basis:
  user_request: "强蒸馏"
  inspected_source:
    - raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source.md
    - raw/videos/2026-06-12-bilibili-bv1jtgq6cese-source/transcript.txt
  conclusion: "strong P1 candidate for VAKS document-intake and retrieval-layer design; high-risk if copied as direct truth/action authority"
last_checked_at: 2026-06-12
```
