---
case_id: pass-direct-source-range-support
expected: PASS
target_claim: "llm-wiki-compiler supports line-addressed claim citations."
source_anchor: "src/utils/markdown.ts"
source_range: "src/utils/markdown.ts:18-25"
evidence_support:
  span_supports_target: supported
  evidence_role: direct_support
  warrant: "The span defines claim citation markers and accepted line range suffixes."
  scope: "Implementation-level support for citation syntax only."
---

# PASS: Direct Source Range Support

This fixture is valid because the ranged source span is tied to an exact target claim and includes support role, warrant, and scope.
