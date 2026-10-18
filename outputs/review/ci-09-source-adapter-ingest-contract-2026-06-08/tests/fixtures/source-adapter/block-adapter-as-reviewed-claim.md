---
case_id: block-adapter-as-reviewed-claim
expected: BLOCK
adapter:
  name: web-readability
  source_type: web
  input_identity: "https://example.com/article"
  adapter_status: ok
reviewed_claim: "Adapter says this claim is true."
verification_status: cross-checked
truth_confidence: high
---

# BLOCK: Adapter As Reviewed Claim

Adapter output cannot create reviewed claims, verification upgrades, or truth confidence.
