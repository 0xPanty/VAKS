---
case_id: pass-counterexample-range
expected: PASS
target_claim: "A source range can act as a challenge, not only support."
source_anchor: "src/linter/rules.ts"
source_range: "src/linter/rules.ts:450-536"
evidence_support:
  span_supports_target: supported
  evidence_role: counterexample
  warrant: "The span shows broken citation checks that challenge treating malformed or missing citations as valid support."
  scope: "Valid as challenge evidence; it must enter challenge_refs or risk_refs, not support_refs."
---

# PASS: Counterexample Range

This fixture is valid because it marks the range as a counterexample instead of support.
