---
type: kp_id_lint_contract
status: candidate_only
created_at: 2026-06-07
scope: candidate point ID format and lint checks
truth_boundary: candidate lint contract only
---

# KP ID Lint Contract

## Boundary

`KP-001` is a local candidate point reference.

It is not a global knowledge object, reviewed relation, truth confidence, or
action basis.

## Minimal Format

```yaml
candidate_points:
  - kp_ref: KP-001
    point_text:
    point_type:
    source_anchor_ref:
    review_route:
    routing_hint: []
    uncertainty:
```

## ID Rules

```text
Use `KP-001`, `KP-002`, `KP-003`.
IDs are local to one candidate distillation note unless explicitly promoted.
Do not reuse the same `kp_ref` twice inside one note.
Do not skip to large IDs without reason.
Do not encode topic, project, or authority in the ID.
```

Good:

```text
KP-001
KP-002
```

Bad:

```text
KP-reviewed-001
KP-vaks-adopt-001
best-practice-001
```

## Lint Checks

```text
candidate note has candidate_points but no kp_ref -> fail
duplicate kp_ref in one candidate note -> fail
kp_ref uses authority/adoption wording -> fail
candidate point has no point_text -> fail
candidate point has no review_route -> warn
candidate point has no source_anchor_ref -> warn or fail if action-facing
```

Sandbox implementation:

```text
tools/vaks-kp-lint.ps1
```

Positive fixture:

```text
fixtures/candidate-distillation-kp-refs.md
```

Negative fixture:

```text
fixtures/candidate-distillation-bad-kp.md
```

## Review Rule

Promotion still requires review.

The ID only makes retrieval and discussion easier:

```text
agent can say "KP-002 conflicts with X"
reviewer can keep/drop/split a point
topic pack can point to a specific candidate point
```
