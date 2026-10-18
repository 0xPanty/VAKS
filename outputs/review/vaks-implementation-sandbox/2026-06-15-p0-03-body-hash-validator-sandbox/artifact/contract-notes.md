---
record_kind: sandbox_contract_notes
slice_id: 2026-06-15-p0-03-body-hash-validator-sandbox
status: draft
truth_boundary: sandbox_notes_only
---

# Contract Notes

## Why Body Hash Exists

The body hash fixes the review object. A reviewer can approve only the exact
body they checked. If the body changes later, approval cannot silently follow
the changed body.

## What This Validator Can Say

The sandbox validator can say:

```text
the recorded body hash matches the current canonical body
the recorded body hash does not match
the checked approval hash does not match
a fixed/approved/writeback-ready record is missing its hash
```

## What This Validator Cannot Say

The sandbox validator cannot say:

```text
the body is true
the body is reviewed knowledge
the body has evidence support
the reviewer approved it
the writeback is ready
the action basis is safe
the sandbox can merge into mainline
```

## Product Reuse

Future slices can reuse this package for:

- P1 retrieval/operation receipt validator pilot fixture style;
- action-boundary failure matrix examples;
- future mainline validator design review.

Future slices must not reuse it as:

- a mainline `tools/` implementation without separate approval;
- a replacement for human review;
- evidence support or truth confidence.
