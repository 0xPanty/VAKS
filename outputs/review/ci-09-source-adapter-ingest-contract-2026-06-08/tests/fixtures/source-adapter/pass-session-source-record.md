---
case_id: pass-session-source-record
expected: PASS
adapter:
  name: codex-session
  source_type: session
  input_identity: "local:session.jsonl"
  output_source_path: "raw/articles/session-source.md"
  captured_at: "2026-06-08T00:00:00Z"
  captured_by: Codex
  adapter_status: ok
  known_gaps: []
  warnings: []
session:
  started_at: "2026-06-08T00:00:00Z"
  ended_at: "2026-06-08T00:30:00Z"
  participant_identity: Codex
source_boundary:
  knowledge_status: raw
  action_basis_allowed: false
  truth_mutation_allowed: false
  promotion_gate: review_required
---

# PASS: Session Source Record

Session import keeps adapter identity and timing as provenance only.
