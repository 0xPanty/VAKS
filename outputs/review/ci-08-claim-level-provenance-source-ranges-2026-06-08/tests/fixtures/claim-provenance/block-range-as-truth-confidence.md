---
case_id: block-range-as-truth-confidence
expected: BLOCK
target_claim: "A valid source range automatically makes truth confidence high."
source_range: "src/context/provenance.ts:222-246"
truth_confidence: high
verification_status: cross-checked
evidence_support:
  span_supports_target: supported
  evidence_role: direct_support
  warrant: "The source range is valid."
---

# BLOCK: Range As Truth Confidence

A valid source range cannot automatically change truth confidence or verification status.
