---
fixture_id: ci06-block-truncated-hides-gaps
expected_result: BLOCK_EXPECTED
context_pack:
  version: 1
  prompt: Budget trimmed context.
  budget:
    requested_tokens: 300
    estimated_tokens: 450
    truncated: true
    trimmed_sections:
      - neighbors
      - source_windows
  warnings: []
  gaps: []
expected_violation: truncated packs must expose warnings or gaps rather than hiding missing context
---

# BLOCK: Truncated Hides Gaps

Budget trimming is a warning, not permission to pretend the pack is complete.

