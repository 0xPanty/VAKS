---
fixture_id: ci03-same-origin-changed-hash
source_identity:
  content_hash: sha256:2222222222222222222222222222222222222222222222222222222222222222
  hash_algorithm: sha256
  origin_uri: https://example.test/source-a
  origin_label: canonical article
  raw_path: raw/articles/source-a.md
  source_record_path: raw/articles/source-a-source.md
  previous_content_hash: sha256:1111111111111111111111111111111111111111111111111111111111111111
  source_changed: yes
  ingest_decision: replacement_candidate
  compiled_outputs:
    - outputs/review/candidates/source-a-v2.candidate.md
  referenced_by:
    - outputs/review/candidates/source-a.candidate.md
expected_ingest_decision: replacement_candidate
expected_registry_action: route_recompile_candidate
---

# Fixture: Same Origin Changed Hash

This is not a harmless duplicate. It must route to replacement/recompile review
and must not silently overwrite the old source record or old evidence chain.

