---
fixture_id: ci03-same-hash-different-origin
source_identity:
  content_hash: sha256:1111111111111111111111111111111111111111111111111111111111111111
  hash_algorithm: sha256
  origin_uri: https://mirror.example.test/source-a
  origin_label: mirror copy with separate provenance
  raw_path: raw/articles/source-a-mirror.md
  source_record_path: raw/articles/source-a-mirror-source.md
  previous_content_hash:
  source_changed: no
  ingest_decision: preserve_new_origin
  compiled_outputs: []
  referenced_by: []
expected_ingest_decision: preserve_new_origin
expected_registry_action: add_origin_to_existing_hash
---

# Fixture: Same Hash Different Origin

Same bytes do not erase provenance. This must preserve the second origin even
when compile can reuse previous content-derived artifacts.

