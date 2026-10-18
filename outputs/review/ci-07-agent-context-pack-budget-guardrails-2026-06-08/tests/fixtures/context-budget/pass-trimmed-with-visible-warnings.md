---
case_id: pass-trimmed-with-visible-warnings
expected: PASS
budget:
  requested_tokens: 1200
  estimated_tokens: 1180
  truncated: true
  trimmed_sections:
    - neighbors
    - sourceWindows
warnings:
  - code: source-window-unavailable
    message: "One citation window was unavailable."
gaps:
  - code: missing_evidence
    message: "Counterevidence not yet checked."
action_readiness:
  state: needs_review
---

# PASS: Trimmed With Visible Warnings

The pack is trimmed, but the loss remains visible and action readiness is not ready.
