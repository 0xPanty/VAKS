---
fixture_id: ci06-block-source-windows-default
expected_result: BLOCK_EXPECTED
include_sources: false
context_pack:
  version: 1
  prompt: Default pack should not include raw source windows.
  source_windows:
    - file: sources/example.md
      start: 10
      end: 18
      text: leaked default source excerpt
expected_violation: source_windows must be empty unless include_sources is explicit
---

# BLOCK: Source Windows Default

Raw snippets should not appear by default.

