---
fixture_id: ci03-compile-failure-no-registry-commit
source_identity:
  content_hash: sha256:4444444444444444444444444444444444444444444444444444444444444444
  hash_algorithm: sha256
  origin_uri: https://example.test/source-c
  origin_label: malformed source
  raw_path: raw/articles/source-c.md
  source_record_path: raw/articles/source-c-source.md
  previous_content_hash:
  source_changed: unknown
  ingest_decision: new_source
  compiled_outputs: []
  referenced_by: []
compile_result: failed
expected_ingest_decision: new_source
expected_registry_action: no_registry_commit
---

# Fixture: Compile Failure No Registry Commit

The hash may be calculated, but registry must not mark it as processed until
capture/conversion/candidate creation succeeds.

