---
record_kind: read_only_query_scenario
expected_valid: false
expected_outcome: blocked
expected_codes: [QL_FORBIDDEN_SIDE_EFFECT]
scenario_id: ql-fail-forbidden-commit
story_kind: ordinary_orientation
query_mode: orientation
requested_authority_bucket: reviewed
included_buckets: [reviewed]
selected_authority_buckets: [reviewed]
selected_pack_roles: [orientation]
commit_attempted: true
---

# Failure: Forbidden Side Effect Commit

The read-only query loop attempts a commit side effect.
