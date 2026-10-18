---
case_id: block-hidden-gaps-after-trim
expected: BLOCK
budget:
  requested_tokens: 800
  estimated_tokens: 780
  truncated: true
  trimmed_sections:
    - chunks
warnings: []
gaps: []
known_before_trim:
  gaps:
    - missing_evidence
---

# BLOCK: Hidden Gaps After Trim

Budget trimming cannot erase known gaps.
