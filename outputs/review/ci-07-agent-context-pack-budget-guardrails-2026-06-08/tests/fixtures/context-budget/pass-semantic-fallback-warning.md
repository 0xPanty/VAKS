---
case_id: pass-semantic-fallback-warning
expected: PASS
budget:
  requested_tokens: 2000
  estimated_tokens: 1600
  truncated: false
  trimmed_sections: []
warnings:
  - code: embedding-store-missing
    message: "Semantic retrieval skipped; lexical signals still applied."
gaps: []
retrieval:
  semantic_hits: []
  lexical_fallback_used: true
action_readiness:
  state: needs_review
---

# PASS: Semantic Fallback Warning

Semantic retrieval failure is visible as a warning instead of silent completeness.
