---
case_id: pass-source-windows-opt-in-bounded
expected: PASS
include_sources: true
source_windows:
  default: off
  max_windows: 20
  max_lines_per_window: 30
  path_confined_to: sources/
budget:
  truncated: false
  trimmed_sections: []
warnings: []
gaps: []
---

# PASS: Source Windows Opt-In Bounded

Raw snippets are explicitly requested and bounded.
