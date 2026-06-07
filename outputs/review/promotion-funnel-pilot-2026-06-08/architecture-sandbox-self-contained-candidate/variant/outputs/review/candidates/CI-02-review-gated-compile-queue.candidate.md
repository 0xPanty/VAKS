---
record_type: review-candidate
status: pending
knowledge_status: candidate
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
candidate_id: CI-02-review-gated-compile-queue
source_candidate_points:
  - CI-02
promotion_target: pattern
proposed_title: Review-Gated Compile Queue
proposed_path: wiki/patterns/review-gated-compile-queue.md
review_object_state: fixed_for_review
candidate_body_location: "# Candidate Body"
body_hash: sha256:8064a811d4bc48d36a88d615e4140229571b230efe5fcd2e874613465ee41c62
body_hash_algorithm: sha256_utf8_lf_trim_body_without_heading
evidence_packet_ref: outputs/review/promotion-funnel-pilot-2026-06-08/PROMOTION_EVIDENCE_PACKETS.md#EP-02
source_anchor_refs:
  - raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip::llm-wiki-compiler-main/src/compiler/candidates.ts:1-12
  - raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip::llm-wiki-compiler-main/src/compiler/candidates.ts:77-103
  - raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip::llm-wiki-compiler-main/src/commands/review-approve.ts:35-64
  - REVIEW_QUEUE.md::Step 7 Promote
scope_limits:
  - Applies to AI-generated or compiler-generated knowledge writeback.
  - Promotes queue-before-wiki discipline, not the reference implementation runtime.
risk_flags:
  - Approval mechanics, lint passes, and test passes are not evidence review.
  - A queue without review habit can become stale.
known_counterevidence: []
missing_evidence:
  - Local VAKS candidate folder convention before implementation work.
approval_integrity:
  approved_by:
  approval_source:
  approved_at:
  llm_assisted: true
  checked_specific_evidence: false
  checked_body_hash:
---

# Candidate: Review-Gated Compile Queue

## Candidate Body

LLM-generated knowledge should enter a review queue before formal wiki writeback.
Only reviewed candidates may move into formal claim, pattern, anti-pattern, or
decision nodes.

This pattern applies to generated knowledge artifacts and compiler-assisted
writeback. It does not make the queue a truth layer, and it does not allow lint,
tests, or approval mechanics to stand in for evidence review.

## Evidence Packet Summary

Support comes from `llm-wiki-compiler` code anchors and local VAKS promotion
rules.

- `candidates.ts` routes generated pages into candidate records instead of direct wiki writes.
- `review-approve.ts` separates approval from generation and writes from the stored candidate.
- `REVIEW_QUEUE.md` defines promotion as reviewed, not automatic.

## Self-Support Check

```text
self_support_loop: false
support_basis: independent local repo snapshot code anchors plus local promotion boundary
support_state: supported
object_integrity_ready: true
approval_readiness: blocked_pending_approval
```

## Minimal Scope

Promote only this boundary:

```text
generated artifact
-> review queue candidate
-> evidence/support check
-> reviewer approval
-> formal writeback
```

Do not adopt the source runtime wholesale.

## Forbidden Interpretations

```text
queue = reviewed knowledge
lint/test pass = evidence review
approval command = truth confidence
automatic compile = automatic promotion
```
