---
case_id: block-missing-source
expected: BLOCK
target_claim: "Missing source files should not support claims."
source_range: "src/missing/file.ts:1-5"
evidence_support:
  span_supports_target: supported
  evidence_role: direct_support
  warrant: "The source file is missing."
---

# BLOCK: Missing Source

A missing source cannot support promotion.
