---
record_type: review-candidate
status: pending
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
candidate_id: ci02-5-block-missing-body-hash
promotion_target: pattern
proposed_title: "Missing Body Hash"
proposed_path: "wiki/patterns/missing-body-hash.md"
review_object_state: fixed_for_review
candidate_body_location: "# Candidate Body"
body_hash:
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
  body_integrity_violations:
    - body_hash missing for fixed review object
  action_boundary_violations: []
---

# Review Candidate

## Candidate Body

This candidate has no body hash and must not be approved.
