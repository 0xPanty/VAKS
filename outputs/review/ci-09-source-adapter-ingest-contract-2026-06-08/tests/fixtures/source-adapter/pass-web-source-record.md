---
case_id: pass-web-source-record
expected: PASS
adapter:
  name: web-readability
  source_type: web
  input_identity: "https://example.com/article"
  output_source_path: "raw/articles/example-article.md"
  captured_at: "2026-06-08T00:00:00Z"
  captured_by: Codex
  adapter_status: ok
  content_hash: "sha256:abc123"
  truncated: false
  original_char_count: 4200
  known_gaps: []
  warnings: []
source_boundary:
  knowledge_status: raw
  action_basis_allowed: false
  truth_mutation_allowed: false
  promotion_gate: review_required
---

# PASS: Web Source Record

Adapter output is a raw source record with provenance and no reviewed truth effects.
