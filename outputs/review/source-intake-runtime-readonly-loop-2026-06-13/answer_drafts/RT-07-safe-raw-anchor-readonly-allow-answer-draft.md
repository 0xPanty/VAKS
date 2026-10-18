---
record_kind: runtime_test_artifact
type: runtime_answer_draft
artifact_kind: runtime_test_artifact
status: allowed_readonly
created_at: '2026-06-14T01:37:48+00:00'
case_id: RT-07-safe-raw-anchor-readonly-allow
risk_target: real_raw_anchor_allow
knowledge_status: candidate
retrieval_exclusion: true
default_retrieval: false
indexing_policy: exclude_from_default_retrieval_graph_pack_support
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: none
  action_basis_allowed: false
  warning_code: context_pack_not_action_basis
read_only: true
writeback_attempted: false
promotion_attempted: false
truth_mutation_attempted: false
action_basis_allowed: false
support_decision: allowed_readonly
runtime_errors: []
---

# Answer Draft

## Runtime Test Artifact Warning

This file is a negative/positive fixture for Source Intake runtime-boundary testing. It must not be indexed, retrieved by default, used as support, or treated as reviewed knowledge.

## Fixture Sentence

```text
Use the inspected raw source section as a read-only citation, not an action basis.
```

This draft is truth-layer read-only and cannot write back or promote knowledge.

