---
case_id: block-source-windows-default-on
expected: BLOCK
include_sources: false
source_windows:
  default: on
  emitted:
    - file: "../private.txt"
      start: 1
      end: 5
---

# BLOCK: Source Windows Default On

Raw snippets must not appear by default.
