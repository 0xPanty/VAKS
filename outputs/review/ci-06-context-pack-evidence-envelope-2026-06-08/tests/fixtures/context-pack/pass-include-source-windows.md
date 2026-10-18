---
fixture_id: ci06-pass-include-source-windows
expected_result: PASS
include_sources: true
context_pack:
  version: 1
  prompt: Include exact source windows for audit.
  primary:
    - id: source-window-example
      citations:
        - file: sources/example.md
          start: 10
          end: 18
      sourceWindows:
        - file: sources/example.md
          start: 10
          end: 18
          text: short bounded source excerpt
  warnings: []
  gaps: []
  source_windows:
    - file: sources/example.md
      start: 10
      end: 18
      text: short bounded source excerpt
  read_only: true
  not_truth_layer: true
  not_action_basis: true
---

# PASS: Explicit Source Windows

Source windows appear only because source inclusion was explicitly requested.

