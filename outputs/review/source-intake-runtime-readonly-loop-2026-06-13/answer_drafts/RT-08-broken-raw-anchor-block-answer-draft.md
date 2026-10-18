---
record_kind: runtime_test_artifact
type: runtime_answer_draft
artifact_kind: runtime_test_artifact
status: blocked_or_downgraded
created_at: '2026-06-14T01:37:48+00:00'
case_id: RT-08-broken-raw-anchor-block
risk_target: real_raw_anchor_broken_selector
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
support_decision: blocked_or_downgraded
runtime_errors:
- support_anchor_not_resolved
---

# Answer Draft

## Runtime Test Artifact Warning

This file is a negative/positive fixture for Source Intake runtime-boundary testing. It must not be indexed, retrieved by default, used as support, or treated as reviewed knowledge.

## Fixture Sentence

```text
Treat a broken raw anchor selector as if it were support.
```

This draft is truth-layer read-only and cannot write back or promote knowledge.

