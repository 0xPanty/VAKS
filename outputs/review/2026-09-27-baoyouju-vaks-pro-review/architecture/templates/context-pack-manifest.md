---
record_kind: context_pack_manifest
status: draft
knowledge_status: candidate
processing_tier: medium
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: context_pack_not_action_basis
action_basis_allowed: false
truth_mutation_allowed: false
query_run_ref:
active_project:
query_mode: orientation
requested_authority_bucket:
included_buckets: []
excluded_buckets: []
items: []
support_checks: []
human_confirmation_required: false
tags:
  - context-pack
  - manifest
---

# Context Pack Manifest

## Boundary

A context pack prepares attention. It is not action basis by itself.

Every item must carry enough boundary metadata for an agent or reviewer to see
why it was included and what it is allowed to do.

## Items

```yaml
items:
  - ref:
    record_kind:
    knowledge_status:
    pack_role: orientation | review_input | support | anchor
    warning_code:
    project_scope:
    action_basis_allowed: false
    independent_anchor_ref:
    selected_by:
      lexical:
      semantic:
      graph:
      metadata:
      legacy_raw_metadata: false
    excluded_reason:
```

## Support Checks

```yaml
support_checks:
  - claim_ref:
    independent_anchor_ref:
    result: supported | weak | missing_anchor | self_support_loop | scope_limited | not_ready
```
