---
record_kind: sandbox_matrix_contract
slice_id: 2026-06-15-p0-07-action-boundary-failure-matrix-sandbox
artifact: artifact/action-boundary-failure-matrix.json
truth_boundary: matrix_contract_for_sandbox_only
---

# Matrix Contract

## Purpose

The matrix records the P0 action-boundary failure cases that must remain
visible before P1 receipt validators and read-only query pilots. It is a
cross-slice coverage artifact, not a runtime validator, truth source, promotion
approval, or mainline merge plan.

## Required Cases

```text
AB-01 body_hash mismatch still approved
AB-02 checked_body_hash mismatch writeback
AB-03 candidate item marked support
AB-04 URL-only citation marked direct_support
AB-05 graph_rank marked trust
AB-06 feedback modifies truth_confidence
AB-07 stale point produces ready action basis
AB-08 budget trimming hides missing evidence
AB-09 read-only actor writes file
AB-10 schema change without owner_final
AB-11 destructive operation without rollback
AB-12 retrieval receipt crosses authority buckets
```

## Required Fields

Each case must include:

```text
case_id
title
failure_mode
boundary_class
source_refs
blocked_by
detection
expected_outcome
fixture_refs
validator_or_check_refs
authority_non_claims
```

The matrix-level and case-level `authority_non_claims` must explicitly keep
these false:

```text
mainline_ready
reviewer_approval_created
reviewed_knowledge_created
evidence_support_created
action_basis_created
promotion_authorized
```

## Verification

`artifact/verify_failure_matrix_sandbox.py` checks:

- all required AB cases are present;
- no duplicate case IDs exist;
- no unknown `AB-*` case appears;
- each case has required fields and non-empty guard/detection/fixture refs;
- each case outcome is blocking, not approving;
- matrix and case records do not claim mainline, reviewed knowledge, evidence
  support, action basis, promotion, or reviewer approval authority.

## Authority Boundary

Matrix pass means only:

```text
the sandbox matrix has modeled P0-07 coverage for the required cases
```

Matrix pass does not mean:

```text
mainline readiness
reviewer approval
Product Acceptance
evidence support
reviewed knowledge
action basis
validator promotion
permission to edit tools/templates/wiki/architecture files
```

