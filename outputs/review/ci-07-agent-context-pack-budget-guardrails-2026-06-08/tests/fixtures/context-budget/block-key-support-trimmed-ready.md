---
case_id: block-key-support-trimmed-ready
expected: BLOCK
budget:
  truncated: true
  trimmed_sections:
    - sourceWindows
    - chunks
key_support_trimmed: true
action_readiness:
  state: ready
---

# BLOCK: Key Support Trimmed But Ready

If key support was trimmed, the pack cannot be action-ready.
