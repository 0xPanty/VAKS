---
case_id: block-json-string-sliced
expected: BLOCK
budget:
  truncated: true
  trim_method: slice_serialized_json
warnings:
  - code: malformed-json-risk
---

# BLOCK: JSON String Sliced

Budget trimming must preserve structured JSON validity.
