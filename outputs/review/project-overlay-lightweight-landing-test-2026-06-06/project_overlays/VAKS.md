---
type: project_overlay_note
status: cross_project_sandbox_sample
project_id: VAKS
created_at: 2026-06-06
truth_boundary: project overlay only; not truth; not ADR; not action basis
source_project_path: C:\Users\Administrator\Documents\资料库
tags:
  - project-overlay
  - project-vaks
  - sandbox
---

# VAKS Borrowing List

## Boundary

This file shows that the same reusable knowledge point can appear in another
project overlay without tagging or rewriting the knowledge point itself.

## Entries

### retrieval-is-activation-not-truth

- kp_ref: outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
- stance: partial
- borrow_scope: Keep retrieval, association, dashboard, and overlay hits as activation surfaces only.
- non_borrow_scope: Do not let retrieval order become support, confidence, truth, or action basis.
- target_hint:
  - MEMORY_TIER.md
  - ARCHITECTURE_PRINCIPLES.md
  - FUSION_ARCHITECTURE_V0_2_DRAFT.md
- updated_at: 2026-06-06

### memory-granularity-and-quarantine

- kp_ref: outputs/review/candidate_pattern_bank/memory-granularity-and-quarantine.md
- stance: partial
- borrow_scope: Keep future agent memory writes quarantined as candidate or feedback-event material.
- non_borrow_scope: Do not let agent memory write reviewed truth or promote relations directly.
- target_hint:
  - ARCHITECTURE_PRINCIPLES.md
  - MEMORY_TIER.md
  - FEEDBACK.md
- updated_at: 2026-06-06

### file-first-agent-workbench

- kp_ref: outputs/review/candidate_pattern_bank/file-first-agent-workbench.md
- stance: partial
- borrow_scope: Keep recovery, review, package, source, and handoff surfaces as visible files.
- non_borrow_scope: Visible files are not reviewed knowledge until the proper review layer says so.
- target_hint:
  - 00_handoff
  - outputs/review
  - wiki/indexes
- updated_at: 2026-06-06

### graph-and-ontology-as-candidate-context

- kp_ref: outputs/review/candidate_pattern_bank/graph-and-ontology-as-candidate-context.md
- stance: partial
- borrow_scope: Use graph or ontology only as candidate context and activation neighborhood.
- non_borrow_scope: Do not let graph edges or graph rank become reviewed relations.
- target_hint:
  - wiki/indexes/knowledge-graph-index.md
  - FUSION_ARCHITECTURE_V0_2_DRAFT.md
- updated_at: 2026-06-06

### visual-workbench-for-retrieval-diagnostics

- kp_ref: outputs/review/candidate_pattern_bank/visual-workbench-for-retrieval-diagnostics.md
- stance: defer
- borrow_scope: Revisit only if VAKS needs a human-facing review workbench after text surfaces prove insufficient.
- non_borrow_scope: Do not add dashboard or UI authority to the truth layer.
- target_hint:
  - outputs/review
  - templates/maintenance-manifest.md
- updated_at: 2026-06-06

### search-to-analysis-before-answer

- kp_ref: outputs/review/candidate_pattern_bank/search-to-analysis-before-answer.md
- stance: partial
- borrow_scope: Use as a light discipline before risky project answers, promotion, or architecture absorption.
- non_borrow_scope: Do not turn ordinary questions into full review packets.
- target_hint:
  - REFERENCE_REVIEW_PROTOCOL.md
  - REVIEW_QUEUE.md
  - ARCHITECTURE_PRINCIPLES.md
- updated_at: 2026-06-06

