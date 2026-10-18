---
fixture_id: ci06-block-neighbor-as-relation
expected_result: BLOCK_EXPECTED
context_pack:
  version: 1
  prompt: Neighbor should create relation.
  neighbors:
    - from: A
      to: B
      reason: wikilink
  proposed_mutation:
    reviewed_relation: supports
expected_violation: neighbors explain activation but cannot create reviewed_relation
---

# BLOCK: Neighbor As Reviewed Relation

Graph neighbors are context, not reviewed relation evidence.

