---
record_kind: topic_retrieval_pack
status: candidate
truth_boundary: navigation_only
topic_id:
created_at:
default_include_path_roles: []
default_exclude_path_roles: []
lanes:
  mainline: []
  candidate: []
  raw: []
  overlay: []
  audit: []
allowed_use:
  - navigation
  - query expansion
  - include/exclude defaults
forbidden_use:
  - truth
  - reviewed relation
  - action basis
  - ontology
---

# Topic Retrieval Pack

## Boundary

This is a navigation and retrieval-slicing aid.

It is not reviewed knowledge, not a relation, not action basis, and not a topic
ontology.

## Include / Exclude Defaults

```yaml
default_include_path_roles: []
default_exclude_path_roles: []
```

## Lanes

```yaml
mainline: []
candidate: []
raw: []
overlay: []
audit: []
```

## Notes

Use only for high-value topics where a human entry page reduces search noise.
