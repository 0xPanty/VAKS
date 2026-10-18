---
fixture_id: ci03-deleted-source-still-referenced
source_identity:
  content_hash: sha256:3333333333333333333333333333333333333333333333333333333333333333
  hash_algorithm: sha256
  origin_uri: https://example.test/source-b
  origin_label: article later removed
  raw_path: raw/articles/source-b.md
  source_record_path: raw/articles/source-b-source.md
  previous_content_hash: sha256:3333333333333333333333333333333333333333333333333333333333333333
  source_changed: unknown
  ingest_decision: orphan_review_due
  compiled_outputs:
    - outputs/review/candidates/source-b.candidate.md
  referenced_by:
    - outputs/review/evidence-packets/source-b-evidence.md
    - wiki/patterns/example-reviewed-pattern.md
  review_due_reason: raw source missing but downstream evidence still references it
expected_ingest_decision: orphan_review_due
expected_registry_action: preserve_trace_and_flag_review_due
---

# Fixture: Deleted Source Still Referenced

This source cannot be silently removed because downstream artifacts still point
to it. The correct behavior is orphan/review_due, not deletion.

