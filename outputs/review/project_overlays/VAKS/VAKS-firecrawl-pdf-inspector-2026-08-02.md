---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
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
project_id: verified-action-knowledge-system
target_ref: "raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md"
target_selector: "repo:firecrawl/pdf-inspector@a15ec2d68d51dbe6a39d1da688ec7a3f642d846c"
target_hint: "native PDF text preflight, positioned extraction, page-level OCR routing, table recovery, and parser regression diagnostics"
source_annotation_refs: "[ann-pdf-inspector-001-sampled-routing-gap, ann-pdf-inspector-002-single-load-positioned-extraction, ann-pdf-inspector-003-text-quality-ocr-reasons, ann-pdf-inspector-004-multi-hypothesis-tables, ann-pdf-inspector-005-lossy-markdown, ann-pdf-inspector-006-region-tsr-hybrid, ann-pdf-inspector-007-per-page-contract-drift, ann-pdf-inspector-008-benchmark-diagnostic-gates, ann-pdf-inspector-009-runtime-package-boundaries]"
project_borrow_scope: "native-text-first PDF route; explicit Full/per-page strategy; positioned extraction bundle; page/region OCR reasons; multi-hypothesis table fallback; paired parser regression diagnostics"
project_non_borrow_scope: "classification confidence as probability or completeness; Markdown/bbox/table output as original evidence; default sampled mode for high-impact intake; cross-page merge as confirmed identity; unbounded in-process parsing; all bindings at once; parser result as reviewed truth/action basis"
project_reopen_trigger: "real PDF adapter sandbox starts; representative Chinese/English/mixed/table/long/corrupt corpus exists; isolated host budgets exist; package-level smoke and PaddleOCR comparison are ready"
confirmation_basis: "User explicitly requested distillation of firecrawl/pdf-inspector in the VAKS workspace on 2026-08-02."
last_checked_at: "2026-08-02"
expires_at: null
---

# Project Overlay：firecrawl/pdf-inspector -> VAKS

## Boundary

This is a project-scoped sidecar.

It records what the VAKS project may borrow or avoid from this source. It does
not rewrite the source card, create reviewed knowledge, approve a dependency,
or provide action basis.

## Target

```yaml
target_ref: raw/repos/2026-08-02-firecrawl-pdf-inspector-source.md
target_selector: repo:firecrawl/pdf-inspector@a15ec2d68d51dbe6a39d1da688ec7a3f642d846c
target_hint: native PDF preflight and selective OCR adapter candidate
source_annotation_refs:
  - ann-pdf-inspector-001-sampled-routing-gap
  - ann-pdf-inspector-002-single-load-positioned-extraction
  - ann-pdf-inspector-003-text-quality-ocr-reasons
  - ann-pdf-inspector-004-multi-hypothesis-tables
  - ann-pdf-inspector-005-lossy-markdown
  - ann-pdf-inspector-006-region-tsr-hybrid
  - ann-pdf-inspector-007-per-page-contract-drift
  - ann-pdf-inspector-008-benchmark-diagnostic-gates
  - ann-pdf-inspector-009-runtime-package-boundaries
```

## Project Borrow Scope

For VAKS, this source may be borrowed as:

```text
1. Native-text-first PDF route
   Put a lightweight native parser before expensive OCR.

2. Explicit page-level escalation
   Preserve pages_needing_ocr and machine-readable reasons.

3. Positioned retained extraction
   Keep page/bbox/font/MCID plus original PDF hash and adapter receipt.

4. Multi-hypothesis table recovery
   Try structure/geometry/text candidates, reject suspicious fragments,
   and retain fallback reasons.

5. Region/TSR hybrid
   Let an external layout/TSR model supply regions, use native text where
   reliable, and OCR only failed cells/regions.

6. Paired parser regression diagnostics
   Compare baseline/candidate on the same corpus and expose aggregate,
   missing-output, and worst-document regressions.
```

Minimal project fit:

```text
Original PDF + SHA256
-> existing document_parse router
-> one normalized, isolated pdf-inspector adapter
-> native page extraction + receipts
-> selected pages/regions to PaddleOCR
-> optional long-document index
-> candidate-only artifacts
```

## Project Non-Borrow Scope

For VAKS, do not currently borrow:

```text
1. Sampled confidence as a completeness or truth signal.
2. needs_ocr=false as proof that nothing was omitted.
3. Default Markdown as original source or the only retained text.
4. Bbox/layout/table output as evidence support without the original page.
5. Cross-page table merging as confirmed table identity.
6. In-process parsing of untrusted PDFs without bytes/pages/time/memory caps.
7. Rust/Python/Node/WASM surfaces simultaneously.
8. Package name plus vague version as deployment identity.
9. Benchmark score as mainline or production approval.
10. Parser output written directly into reviewed truth, relations, decisions,
    memory, or action basis.
```

This source does not replace:

```text
PaddleOCR for scanned/complex OCR
OpenKB-style long-document navigation
linXiv/source adapters for acquisition and identity
VAKS review/evidence/action boundaries
```

## Reopen Trigger

Reconsider this overlay when all necessary work is in scope:

```text
real PDF adapter sandbox starts
representative Chinese/English/mixed/table/long/corrupt fixture set exists
explicit Full/per-page strategy can be tested
isolated worker + bytes/pages/time/memory/output budgets exist
published wheel/CLI package-level smoke is ready
PaddleOCR hybrid comparison and omission/anchor evaluation are ready
CMap packaging, dependency audit, and third-party notice can be checked
```

## Confirmation

```yaml
confirmation_basis: explicit user request to distill this repository
last_checked_at: 2026-08-02
expires_at:
```

## Operational Verdict

```text
borrow_value: medium-high
borrow_now: design and evaluation shape only
borrow_later: sandboxed single-distribution PDF adapter
do_not_borrow_now: mainline dependency, authority semantics, unbounded runtime
formal_pattern_needed: no
schema_change_needed: no
```

## Forbidden

```text
truth confidence
reviewed relation
automatic promotion
action basis
dependency adoption approval
silent replacement of original PDF
```
