---
slice_id: 2026-06-19-p2-85-exact-approval-classifier-hardening-sandbox
status: generated
---

# Exact Approval Classifier Hardening

## Summary

- exact_phrase_sha256: 3aa60d89b13671c099ca35db166b00b329600e91164d8ebabdb03b8da0190775
- positive_case_count: 1
- negative_case_count: 9
- classification_pass_count: 10
- classification_failure_count: 0
- user_approval_collected_by_this_slice: false

## Cases

### POS-01-exact-phrase

- kind: positive
- expected_match: true
- matched_exact_phrase: true
- approval_class: exact_p2_75_approval

### NEG-01-chinese-generic-continue

- kind: negative
- expected_match: false
- matched_exact_phrase: false
- approval_class: not_approval

### NEG-02-english-generic-go-ahead

- kind: negative
- expected_match: false
- matched_exact_phrase: false
- approval_class: not_approval

### NEG-03-paraphrase

- kind: negative
- expected_match: false
- matched_exact_phrase: false
- approval_class: not_approval

### NEG-04-partial-phrase

- kind: negative
- expected_match: false
- matched_exact_phrase: false
- approval_class: not_approval

### NEG-05-wrong-count

- kind: negative
- expected_match: false
- matched_exact_phrase: false
- approval_class: not_approval

### NEG-06-missing-prohibitions

- kind: negative
- expected_match: false
- matched_exact_phrase: false
- approval_class: not_approval

### NEG-07-extra-authority

- kind: negative
- expected_match: false
- matched_exact_phrase: false
- approval_class: not_approval

### NEG-08-whitespace-variation

- kind: negative
- expected_match: false
- matched_exact_phrase: false
- approval_class: not_approval

### NEG-09-case-variation

- kind: negative
- expected_match: false
- matched_exact_phrase: false
- approval_class: not_approval

## Boundary

This classifier is a sandbox hardening artifact. A fixture match is not user approval collected now and does not authorize old-file writes.
