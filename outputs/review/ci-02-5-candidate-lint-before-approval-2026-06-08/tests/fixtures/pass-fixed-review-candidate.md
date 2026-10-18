---
record_type: review-candidate
status: pending
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
candidate_id: ci02-5-pass-fixed-review-candidate
promotion_target: pattern
proposed_title: "Candidate Lint Before Approval"
proposed_path: "wiki/patterns/candidate-lint-before-approval.md"
review_object_state: fixed_for_review
candidate_body_location: "# Candidate Body"
body_hash: "sha256:test-pass-body"
body_hash_algorithm: sha256_utf8_lf_trim_body_without_heading
evidence_packet_ref: "# Evidence Packet"
source_anchor_refs:
  - "raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip::src/compiler/index.ts:594-617"
candidate_lint:
  checked_at: 2026-06-08T00:00:00Z
  checked_by: Codex sandbox test
  lint_status: pass
  schema_violations: []
  provenance_violations: []
  evidence_support_violations: []
  approval_integrity_violations: []
  body_integrity_violations: []
  action_boundary_violations: []
approval_integrity:
  approved_by:
  approval_source:
  approved_at:
  llm_assisted: false
  checked_specific_evidence: false
  checked_body_hash:
---

# Review Candidate

## Candidate Body

Candidate lint should expose blocking candidate problems before approval.

## Evidence Packet

The source anchor points to candidate-time schema and provenance violation
capture in the local llm-wiki-compiler snapshot.
