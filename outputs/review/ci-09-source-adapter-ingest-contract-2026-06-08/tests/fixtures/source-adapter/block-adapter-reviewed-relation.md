---
case_id: block-adapter-reviewed-relation
expected: BLOCK
adapter:
  name: repo-snapshot
  source_type: repo
  input_identity: "local:repo.zip"
  adapter_status: ok
relations:
  - target: "[[pattern]]"
    type: supports
    relation_state: reviewed
---

# BLOCK: Adapter Reviewed Relation

Adapter output may suggest candidate relations, but cannot create reviewed relations.
