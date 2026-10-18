---
slice_id: 2026-06-19-p2-102-opus-result-intake-dry-run-validator-sandbox
status: planned
---

# Slice Plan

## Goal

Create a dry-run validator for future external Opus result intake.

## Why This Slice Now

p2-101 makes submission to external Opus executable. The next risk is accepting an ambiguous or over-authoritative Opus response when it returns. This slice proves the result intake gate with valid and invalid sample records before any real Opus result exists.

## Write Scope

Only this path may be written:

```text
outputs/review/vaks-implementation-sandbox/2026-06-19-p2-102-opus-result-intake-dry-run-validator-sandbox/
```

## Non-Write Scope

- No old slice edits.
- No root architecture document edits.
- No README edits.
- No wiki truth layer edits.
- No templates or tools edits.
- No Obsidian vault writes or sync.
- No commit, push, promotion, or mainline merge.
- No claim that Opus has approved anything.

## Acceptance Criteria

- Read p2-96 intake schema and p2-101 operator kit evidence.
- Generate three valid dry-run records: PASS, REVISE, and BLOCKED.
- Generate invalid failure cases for bad token, missing fields, authority overclaim, missing raw response path, and unsupported evidence.
- Provide a validator that accepts only schema-conformant dry-run records.
- Keep actual Opus result status false.
- Pass local verifier, Reviewer, Boundary Auditor, and GPT-5.5 Product Acceptance.

## Stop Conditions

- A real Opus result is needed.
- Any old slice or protected path would need modification.
- The validator would need to treat sample data as real Opus approval.
