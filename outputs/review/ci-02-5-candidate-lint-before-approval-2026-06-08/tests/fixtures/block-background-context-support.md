---
record_type: review-candidate
status: pending
knowledge_status: candidate
action_basis_allowed: false
truth_mutation_allowed: false
candidate_id: ci02-5-block-background-context-support
promotion_target: pattern
proposed_title: "Background Context As Support"
proposed_path: "wiki/patterns/background-context-as-support.md"
review_object_state: fixed_for_review
candidate_body_location: "# Candidate Body"
body_hash: "sha256:test-background-context"
body_hash_algorithm: sha256_utf8_lf_trim_body_without_heading
evidence_packet_ref: "# Evidence Packet"
source_anchor_refs:
  - "wiki/summaries/2026-05-26-llm-wiki-compiler-architecture-review.md"
candidate_lint:
  checked_at: 2026-06-08T00:00:00Z
  checked_by: Codex sandbox test
  lint_status: blocking
  schema_violations: []
  provenance_violations: []
  evidence_support_violations:
    - background_context counted as promotion support
  approval_integrity_violations: []
  body_integrity_violations: []
  action_boundary_violations: []
---

# Review Candidate

## Candidate Body

This candidate incorrectly treats background context as support.

## Evidence Packet

```yaml
evidence_support:
  evidence_role: background_context
  span_supports_target: unclear
```
