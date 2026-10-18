---
fixture_id: ci03-repeat-same-origin-same-hash
source_identity:
  content_hash: sha256:1111111111111111111111111111111111111111111111111111111111111111
  hash_algorithm: sha256
  origin_uri: https://example.test/source-a
  origin_label: canonical article
  raw_path: raw/articles/source-a.md
  source_record_path: raw/articles/source-a-source.md
  previous_content_hash: sha256:1111111111111111111111111111111111111111111111111111111111111111
  source_changed: no
  ingest_decision: idempotent_skip
  compiled_outputs:
    - outputs/review/candidates/source-a.candidate.md
  referenced_by:
    - outputs/review/candidates/source-a.candidate.md
expected_ingest_decision: idempotent_skip
expected_registry_action: no_new_candidate
---

# Fixture: Repeat Same Origin Same Hash

This is a safe duplicate. The system may skip compile, but should leave the
existing source record and candidate trace alone.

