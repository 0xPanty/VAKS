---
fixture_id: ci03-new-source
source_identity:
  content_hash: sha256:1111111111111111111111111111111111111111111111111111111111111111
  hash_algorithm: sha256
  origin_uri: https://example.test/source-a
  origin_label: canonical article
  raw_path: raw/articles/source-a.md
  source_record_path: raw/articles/source-a-source.md
  previous_content_hash:
  source_changed: no
  ingest_decision: new_source
  compiled_outputs: []
  referenced_by: []
expected_ingest_decision: new_source
expected_registry_action: add_after_success
---

# Fixture: New Source

This represents first-time durable source capture. It may create a candidate
after capture succeeds, but it must not write reviewed wiki content directly.

