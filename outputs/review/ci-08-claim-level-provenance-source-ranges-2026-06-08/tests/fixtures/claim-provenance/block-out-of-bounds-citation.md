---
case_id: block-out-of-bounds-citation
expected: BLOCK
target_claim: "Out-of-bounds citations should not support claims."
source_range: "src/utils/markdown.ts:999-1000"
evidence_support:
  span_supports_target: supported
  evidence_role: direct_support
  warrant: "The file does not have those lines."
---

# BLOCK: Out Of Bounds Citation

Out-of-bounds line ranges cannot be used as support.
