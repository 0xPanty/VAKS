---
case_id: block-malformed-citation
expected: BLOCK
target_claim: "Malformed citations should not support claims."
source_range: "src/utils/markdown.ts:0-5"
evidence_support:
  span_supports_target: supported
  evidence_role: direct_support
  warrant: "Line zero is invalid."
---

# BLOCK: Malformed Citation

Line 0 is malformed and cannot support promotion.
