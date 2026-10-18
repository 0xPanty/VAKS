---
record_kind: sandbox_validator_contract
slice_id: 2026-06-15-p0-03-body-hash-validator-sandbox
status: draft
truth_boundary: sandbox_contract_only
---

# Body Hash Validator Contract

## Purpose

The validator checks whether a review candidate record still points to the exact
body it claims to fix for review or approval.

It is process integrity only. Passing the validator does not mean reviewer
approval, evidence support, reviewed knowledge, mainline readiness, or action
basis.

## Input Contract

Input is a Markdown record with frontmatter fields:

```yaml
record_kind: review_candidate
candidate_body_location:
review_status: draft | fixed | approved | writeback_ready
review_object_state: draft | fixed_for_review | revised_after_review | archived
writeback_ready: true | false
body_hash:
approval_integrity:
  checked_body_hash:
```

`candidate_body_location` can be:

- a file path relative to the record file;
- a same-file Markdown section such as `# Candidate Body`;
- a file path plus Markdown section such as `candidate.md# Candidate Body`.

In this sandbox prototype, file locations must resolve inside the record's own
directory. This keeps fixture validation local and prevents absolute paths or
`..` traversal from becoming hidden evidence.

## Canonical Body Rule

Canonical body hash is:

```text
read candidate_body_location
-> normalize CRLF and CR to LF
-> remove the first non-empty Markdown heading line
-> trim leading/trailing whitespace
-> encode as UTF-8
-> SHA256 hex digest
```

## Blocking Rules

The validator blocks:

| Code | Meaning |
|---|---|
| `body_hash_mismatch` | Recorded `body_hash` differs from computed canonical body hash. |
| `checked_body_hash_mismatch` | `approval_integrity.checked_body_hash` differs from computed canonical body hash. |
| `fixed_or_approved_missing_body_hash` | A fixed, approved, or writeback-ready object lacks `body_hash`. |
| `writeback_ready_body_changed` | A writeback-ready object's current body differs from its recorded fixed body hash. |

Template-shaped records using `review_object_state: fixed_for_review` or
`review_object_state: revised_after_review` also require `body_hash`.

## Non-Claims

The validator is not:

- reviewer approval;
- approval integrity by itself;
- Evidence Packet;
- truth confidence;
- reviewed knowledge;
- action readiness;
- permission to write `wiki/`;
- permission to merge this slice into mainline.
