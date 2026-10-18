---
type: pattern
status: sandbox-candidate
created: 2026-06-08
updated: 2026-06-08
source_libraries:
  - RKA
related_projects:
  - verified-knowledge-system
adoption_status: sandbox-test
tags:
  - pattern/feedback
  - use-ledger
  - decision-calibration
evidence_count: 2
confidence: medium
relations:
  - target: "[[conversation-derived-feedback-routing]]"
    type: refines
    strength: 4
    confidence: medium
    evidence:
      - "[[decision-outcome-precondition-before-calibration]]"
    rationale: "Decision outcomes need a recorded recommendation and user choice or explicit override before they can calibrate future recommendations."
    created: 2026-06-08
    last_verified: 2026-06-08
---

# Decision Outcome Precondition Before Calibration

## Plain Rule

Do not record a final decision outcome unless the original recommendation and
the user's choice, or an explicit user override, are already recorded.

## Why It Exists

If the vault only records "the result was good/bad" but does not record what was
recommended and what the user actually chose, the outcome cannot tell whether
the recommendation worked.

That kind of outcome may be useful as a note, but it must not calibrate future
recommendations.

## Source Evidence

Evidence packet:

```text
outputs/review/promotion-funnel-pilot-2026-06-08/PROMOTION_EVIDENCE_PACKETS.md#EP-04
```

Local RKA review:

```text
outputs/review/2026-05-30-rka-source-code-anchor-review.md
```

Exact RKA anchors recorded by the evidence packet:

```text
https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/decision_option.py#L121-L130
https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/decision_options.py#L234-L280
https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/api/routes/decisions.py#L227-L243
```

## Minimum Chain

```text
recommendation
-> confidence_at_decision
-> user_choice OR explicit_user_override
-> outcome_note
-> future recommendation calibration
```

## Allowed Effects

Decision outcome calibration may affect:

```text
future_recommendation
risk_calibration
scope_fit
option_framing
review_due
```

## Forbidden Effects

Decision outcome calibration must not directly affect:

```text
truth_confidence
verification_status
source_reliability
review_verdict
reviewed_relation
reviewed_relation_strength
action_basis_readiness
```

It must not import:

```text
RKA runtime
RKA MCP
RKA API server
RKA dashboard
RKA SQLite database
calibration metrics as truth confidence
```

## Valid Outcome Cases

| Case | Status | Reason |
|---|---|---|
| recommendation + user_choice + outcome_note | allowed | The recommendation chain is auditable. |
| recommendation + explicit_user_override + outcome_note | allowed | The user intentionally overrode or replaced the recommendation. |
| outcome only | blocked | No recommendation chain exists. |
| recommendation + outcome, but no user choice or override | blocked | Cannot tell whether the user followed the recommendation. |
| casual approval text only | blocked | "Looks good" is not a recorded user choice or explicit override. |
| outcome mutates truth fields | blocked | Outcomes calibrate future recommendation, not truth. |

## Integration Boundary

This is a Use Ledger / Feedback Ledger hardening rule. It does not create a new
decision runtime, does not replace Evidence Packet review, and does not change
the reviewed knowledge schema by itself.

