---
record_type: review-candidate
status: pending
knowledge_status: candidate
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
candidate_id: CI-04-decision-outcome-precondition-before-calibration
source_candidate_points:
  - CI-04
promotion_target: pattern
proposed_title: Decision Outcome Precondition Before Calibration
proposed_path: wiki/patterns/decision-outcome-precondition-before-calibration.md
review_object_state: fixed_for_review
candidate_body_location: "# Candidate Body"
body_hash: sha256:a52bb75af5d80c1ddc033b83e6098729a34c1a56444a59278a1eb0945edc94b6
body_hash_algorithm: sha256_utf8_lf_trim_body_without_heading
evidence_packet_ref: outputs/review/promotion-funnel-pilot-2026-06-08/PROMOTION_EVIDENCE_PACKETS.md#EP-04
source_anchor_refs:
  - https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/decision_option.py#L121-L130
  - https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/decision_options.py#L234-L280
  - https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/api/routes/decisions.py#L227-L243
scope_limits:
  - Applies to decision/use-ledger outcome calibration, not claim truth.
  - Adopts a small precondition pattern, not RKA runtime, SQLite, API, MCP, dashboard, or metrics.
risk_flags:
  - Outcome calibration can overfit if user choice or override is not recorded.
  - Brier/ECE-style metrics remain parked until enough outcome data exists.
known_counterevidence: []
missing_evidence:
  - Concrete VAKS decision-outcome example before implementation work.
approval_integrity:
  approved_by:
  approval_source:
  approved_at:
  llm_assisted: true
  checked_specific_evidence: false
  checked_body_hash:
---

# Candidate: Decision Outcome Precondition Before Calibration

## Candidate Body

Decision outcome calibration should not record a final outcome unless the
recommendation and user choice, or an explicit override, are already recorded.

Without a recorded recommendation-to-choice-or-override chain, an observed
outcome cannot show whether the recommendation itself worked. Outcome
calibration should improve future recommendation behavior, not mutate claim
truth confidence.

## Evidence Packet Summary

Support comes from RKA exact-commit code anchors.

- RKA's selection payload and service require either selected option or override rationale before recording PI selection.
- The route-level outcome guard rejects outcome recording when neither PI selected option nor override rationale exists.
- The local VAKS adaptation is only the precondition pattern, not the RKA runtime.

## Self-Support Check

```text
self_support_loop: false
support_basis: exact RKA commit code anchors
support_state: supported
object_integrity_ready: true
approval_readiness: blocked_pending_approval
```

## Minimal Scope

Promote only this chain:

```text
recommendation
-> user choice or explicit override
-> observed outcome
-> future recommendation calibration
```

Do not treat outcome calibration as proof that the underlying claim is true.

## Forbidden Interpretations

```text
outcome = truth confidence
approval = evidence support
RKA runtime = VAKS architecture
metrics before enough data
```
