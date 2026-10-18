---
case_id: block-empty-content-success
expected: BLOCK
adapter:
  name: pdf-text
  source_type: pdf
  input_identity: "local:empty.pdf"
  output_source_path: "raw/papers/empty.md"
  adapter_status: ok
content: ""
---

# BLOCK: Empty Content Success

Empty extracted content must be failed or blocked, not ok.
