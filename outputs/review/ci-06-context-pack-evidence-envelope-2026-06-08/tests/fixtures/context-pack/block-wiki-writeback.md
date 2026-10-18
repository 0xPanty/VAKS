---
fixture_id: ci06-block-wiki-writeback
expected_result: BLOCK_EXPECTED
context_pack:
  version: 1
  prompt: Write context into wiki.
  read_only: false
  proposed_mutation:
    wiki_writeback: true
    candidate_promotion: true
expected_violation: context pack must be read-only and cannot write wiki or promote candidates
---

# BLOCK: Wiki Writeback

Context pack generation is not writeback or promotion.

