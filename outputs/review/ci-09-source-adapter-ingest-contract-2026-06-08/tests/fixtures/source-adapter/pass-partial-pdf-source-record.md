---
case_id: pass-partial-pdf-source-record
expected: PASS
adapter:
  name: pdf-text
  source_type: pdf
  input_identity: "local:paper.pdf"
  output_source_path: "raw/papers/paper-source.md"
  captured_at: "2026-06-08T00:00:00Z"
  captured_by: Codex
  adapter_status: partial
  content_hash: "sha256:def456"
  truncated: true
  original_char_count: 240000
  known_gaps:
    - "Figures not extracted."
  warnings:
    - "Source was truncated."
source_boundary:
  knowledge_status: raw
  action_basis_allowed: false
  truth_mutation_allowed: false
  promotion_gate: review_required
---

# PASS: Partial PDF Source Record

Partial adapter output is allowed when truncation and gaps are explicit.
