---
record_type: review-candidate
status: pending
knowledge_status: candidate
action_basis_allowed: true
truth_mutation_allowed: false
candidate_id: ci02-5-block-action-basis-candidate
promotion_target: pattern
proposed_title: "Candidate As Action Basis"
proposed_path: "wiki/patterns/candidate-as-action-basis.md"
review_object_state: fixed_for_review
candidate_body_location: "# Candidate Body"
body_hash: "sha256:test-action-basis"
body_hash_algorithm: sha256_utf8_lf_trim_body_without_heading
evidence_packet_ref: "# Evidence Packet"
source_anchor_refs:
  - "raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip::src/compiler/index.ts:594-617"
candidate_lint:
  checked_at: 2026-06-08T00:00:00Z
  checked_by: Codex sandbox test
  lint_status: blocking
  schema_violations: []
  provenance_violations: []
  evidence_support_violations: []
  approval_integrity_violations: []
  body_integrity_violations: []
  action_boundary_violations:
    - action_basis_allowed true while knowledge_status is candidate
---

# Review Candidate

## Candidate Body

This candidate incorrectly allows action-basis use before review.
