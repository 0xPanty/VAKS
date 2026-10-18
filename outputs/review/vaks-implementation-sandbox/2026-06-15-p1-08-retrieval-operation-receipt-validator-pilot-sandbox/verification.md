---
record_kind: sandbox_verification
slice_id: 2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox
status: local_verification_passed
truth_boundary: sandbox_verification_only
---

# Verification

## Commands Run

```powershell
python -B -m py_compile `
  outputs/review/vaks-implementation-sandbox/2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox/artifact/receipt_validator_pilot.py `
  outputs/review/vaks-implementation-sandbox/2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox/artifact/verify_receipt_validator_pilot.py

python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox/artifact/verify_receipt_validator_pilot.py
```

## Result

```text
py_compile: pass
suite_runner: pass
positive_fixtures: 4
failure_cases: 27
failures: 0
```

## Verified Positive Fixtures

- `fixtures/valid-retrieval-orientation-receipt.md`
- `fixtures/valid-retrieval-direct-anchor-receipt.md`
- `fixtures/valid-operation-suggest-only-proposal.md`
- `fixtures/valid-operation-reviewed-write-receipt.md`

## Verified Failure Cases

- 13 retrieval receipt failure cases.
- 14 operation receipt failure cases.

Each failure case was invalid and emitted its expected issue code.

## Fixes During Verification

Two local implementation issues were found and fixed inside this sandbox path:

- The suite runner originally normalized expected codes to lower case while the
  validator emitted upper-case issue codes.
- A delete failure case was being incorrectly checked as a reviewed write
  because `target_scope: reviewed` was not gated by `operation_mode: write`.

After the fixes, the suite passed.

## Reviewer-Triggered Revision

The first Reviewer pass returned blocking findings. The following fixes were
made inside this sandbox path:

- Added fail-closed enum checks for retrieval authority buckets, retrieval pack
  roles, operation actor tiers, operation modes, and target scopes.
- Added failure cases for unknown retrieval buckets, unknown pack roles,
  unknown actor tier, and unknown operation mode.
- Required approval and checked body hash for mainline/formal/schema/protected
  writes, then added a mainline-write failure case.
- Changed URL-only support blocking so any claimed support with URL-only,
  metadata-only, or summary-only anchor is blocked, even when
  `support_evidence_role: none`.
- Added a failure case for `support_result: supported` with URL-only anchor and
  `support_evidence_role: none`.

After these revisions, the suite passed with 4 positive fixtures and 27 failure
cases.

## Non-Claims

Passing verification means only that this sandbox validator pilot behaves as
expected on its fixtures and failure cases. It is not reviewer approval, product
acceptance, evidence support, reviewed knowledge, action basis, mainline
readiness, commit approval, push approval, or Obsidian sync approval.
