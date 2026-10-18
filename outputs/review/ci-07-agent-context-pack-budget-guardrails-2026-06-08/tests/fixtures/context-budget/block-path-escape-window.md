---
case_id: block-path-escape-window
expected: BLOCK
include_sources: true
source_windows:
  default: off
  emitted:
    - file: "../outside.md"
      start: 1
      end: 5
---

# BLOCK: Path Escape Window

Source windows must stay path-confined to sources/.
