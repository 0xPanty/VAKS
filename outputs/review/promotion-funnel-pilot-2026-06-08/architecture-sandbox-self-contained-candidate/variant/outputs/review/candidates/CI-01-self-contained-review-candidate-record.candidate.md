---
record_type: review-candidate
status: pending
knowledge_status: candidate
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
candidate_id: CI-01-self-contained-review-candidate-record
source_candidate_points:
  - CI-01
promotion_target: pattern
proposed_title: Self-Contained Review Candidate Record
proposed_path: wiki/patterns/self-contained-review-candidate-record.md
review_object_state: fixed_for_review
candidate_body_location: "# Candidate Body"
body_hash: sha256:b9db816ba66069965395acfb9718a14d45097f647bcd5d1134a5b9f8596ce10b
body_hash_algorithm: sha256_utf8_lf_trim_body_without_heading
evidence_packet_ref: outputs/review/promotion-funnel-pilot-2026-06-08/PROMOTION_EVIDENCE_PACKETS.md#EP-01
source_anchor_refs:
  - raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip::src/compiler/candidates.ts:1-12
  - raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip::src/compiler/candidates.ts:34-58
  - raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip::src/compiler/candidates.ts:84-101
  - raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip::src/commands/review-approve.ts:47-64
scope_limits:
  - Applies to review or promotion candidates, not ordinary light capture.
  - Supports artifact discipline, not source truth.
risk_flags:
  - Candidate inbox can become stale without review habit.
  - Body hash must be recalculated if the candidate body changes.
known_counterevidence: []
missing_evidence:
  - Local VAKS implementation example before real script adoption.
approval_integrity:
  approved_by:
  approval_source:
  approved_at:
  llm_assisted: true
  checked_specific_evidence: false
  checked_body_hash:
---

# Candidate: Self-Contained Review Candidate Record

## Candidate Body

A review candidate should be a self-contained artifact with body, source
anchors, support checks, scope limits, risks, and approval-integrity facts, so
review and writeback refer to the same object.

This pattern applies when a candidate is being prepared for promotion, formal
writeback, a strong reviewed relation, action basis, or explicit reviewer
audit. It does not apply to ordinary light capture.

The candidate body proposed for writeback must be fixed before approval. If the
body changes after review, the body hash changes and the candidate returns to
review.

## Evidence Packet Summary

Support comes from `llm-wiki-compiler` code anchors, not from this candidate
record itself.

- `candidates.ts` routes generated pages into standalone candidate records.
- Candidate records preserve body, sources, source state, schema violations, and
  provenance violations.
- `review-approve.ts` re-reads the stored candidate body during approval instead
  of silently regenerating a different body.

## Self-Support Check

```text
self_support_loop: false
support_basis: independent local repo snapshot code anchors
support_state: supported
object_integrity_ready: true
approval_readiness: blocked_pending_approval
```

## Minimal Scope

Promote only the artifact-boundary pattern:

```text
fixed candidate object
-> evidence/support check
-> approval of exact body
-> writeback/archive receipt
```

Do not promote runtime choices from the reference implementation.

## Forbidden Interpretations

```text
candidate record = reviewed truth
source summary = independent proof
approval = evidence support
body_hash = truth confidence
automatic promotion
```
