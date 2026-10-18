---
record_kind: sandbox_contract_notes
slice_id: 2026-06-15-p0-02-operation-receipt-template-sandbox
status: draft
truth_boundary: sandbox_notes_only
---

# Contract Notes

## Minimal Contract

An operation receipt is valid only as process trace. It must keep three ideas
separate:

```text
operation trace != truth
operation trace != reviewer approval
operation trace != action basis
```

## Permission Contract

The actor tier must constrain the operation mode:

- `read_only` can only read;
- `suggest_only` can suggest or propose but cannot perform writes;
- `candidate_write` can write only inside an approved candidate or sandbox path;
- `reviewed_write` needs approval and checked body hash;
- `owner_final` is required for schema changes and destructive operations.

## Basis Contract

The receipt can name context packs, candidates, feedback, retrieval receipts,
and reviewed support, but only reviewed support can be eligible for action
support. Even then, action readiness still depends on later support, sufficiency,
scope, temporal, risk, approval, and rollback gates.

## Body Hash Contract

This slice records the field and failure pattern for body hashes. P0-03 is the
future body hash validator. A hash-looking string in this slice is test fixture
data, not validated authority.

## Product Reuse Contract

Future slices can reuse this package as:

- the source contract for an operation receipt validator pilot;
- fixture material for permission-tier tests;
- failure-case input for action-boundary matrix tests.

Future slices must not reuse it as:

- mainline architecture;
- a reviewed template under `templates/`;
- proof that any real operation was approved;
- proof that a sandbox operation may merge into mainline.
