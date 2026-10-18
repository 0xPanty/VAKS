---
fixture_id: ci03-block-hash-as-truth
source_identity:
  content_hash: sha256:5555555555555555555555555555555555555555555555555555555555555555
  hash_algorithm: sha256
  origin_uri: https://example.test/source-d
  origin_label: tempting but invalid shortcut
  raw_path: raw/articles/source-d.md
  source_record_path: raw/articles/source-d-source.md
  previous_content_hash:
  source_changed: no
  ingest_decision: new_source
  compiled_outputs: []
  referenced_by: []
proposed_misuse: hash_as_truth_confidence
expected_test_result: BLOCK_EXPECTED
expected_violation: source hash cannot provide truth confidence, evidence support, approval, reviewed relation, action readiness, or wiki writeback
---

# Fixture: Block Hash As Truth

This fixture intentionally proposes a bad shortcut. Hash equality can support
idempotent intake, but it cannot make a claim true.

