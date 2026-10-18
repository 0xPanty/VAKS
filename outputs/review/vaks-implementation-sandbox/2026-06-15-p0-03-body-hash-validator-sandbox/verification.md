---
record_kind: sandbox_verification
slice_id: 2026-06-15-p0-03-body-hash-validator-sandbox
status: local_verification_passed
truth_boundary: verification_for_sandbox_only
---

# Verification

## Required Files

Result:

```text
REQUIRED_FILES_PASS count=13
```

Checked:

```text
slice-plan.md
source-map.md
artifact/body_hash_validator_sandbox.py
artifact/validator-contract.md
artifact/contract-notes.md
artifact/failure-case-oracle.md
fixtures/
failure-cases/
verification.md
reviewer-report.md
boundary-audit.md
product-acceptance-report.md
next-step.md
```

## Script Syntax

Command:

```powershell
python -m py_compile artifact/body_hash_validator_sandbox.py
```

Result:

```text
PY_COMPILE_PASS
```

The generated `artifact/__pycache__/` runtime cache was removed after verifying
that the resolved path stayed inside this sandbox directory.

## Positive Fixtures

Command:

```powershell
python artifact/body_hash_validator_sandbox.py `
  fixtures/valid-approved-candidate.md `
  fixtures/valid-draft-no-hash.md `
  fixtures/valid-heading-normalization.md
```

Result:

```text
PASS .../fixtures/valid-approved-candidate.md body_hash=e1014d39422754ccdc6a5e609faf6266a8eddb9e4c6394c74685c3b4eb50932b
PASS .../fixtures/valid-draft-no-hash.md body_hash=8eb4c4a4ac250a53818fefd2951b4ee36ed499b05e2905be3d8568df3b7a33c8
PASS .../fixtures/valid-heading-normalization.md body_hash=eae10daa1abaf21f742f906f1f3222f03de23a1c85f890cf41817ddc8cdd77ee
POSITIVE_FIXTURES_PASS exit=0
```

## Failure Cases

Each failure case was run individually with JSON output. The command expected
exit code `1` and the fixture's `expected_failure_reason` inside `codes`.

Result:

```text
FAILURE_CASE_EXPECTED_BLOCK body-hash-mismatch.md code=body_hash_mismatch
FAILURE_CASE_EXPECTED_BLOCK checked-body-hash-mismatch.md code=checked_body_hash_mismatch
FAILURE_CASE_EXPECTED_BLOCK fixed-approved-missing-body-hash.md code=fixed_or_approved_missing_body_hash
FAILURE_CASE_EXPECTED_BLOCK writeback-ready-body-changed.md code=writeback_ready_body_changed
FAILURE_CASES_PASS count=4
```

## Fixture Counts

Result:

```text
FIXTURE_COUNT fixtures=3 failure_cases=4
```

## Git Status For This Slice

Command:

```powershell
git status --short -- "outputs/review/vaks-implementation-sandbox/2026-06-15-p0-03-body-hash-validator-sandbox"
```

Result:

```text
?? outputs/review/vaks-implementation-sandbox/2026-06-15-p0-03-body-hash-validator-sandbox/
```

## Boundary Meaning

These checks prove only that the sandbox-local validator prototype behaves as
expected on its fixtures. They do not prove reviewer approval, Product
Acceptance, reviewed knowledge, mainline readiness, or action basis.

## Post-Reviewer Repair Verification

Reviewer Round 1 found two blockers:

- validator did not support the canonical `templates/review-candidate.md`
  fields `review_object_state: fixed_for_review` and
  `candidate_body_location: "# Candidate Body"`;
- fixtures did not include template-shaped section locator or explicit CRLF
  normalization checks.

Repairs:

- added `review_object_state` support for `fixed_for_review`,
  `revised_after_review`, `approved`, and `writeback_ready`;
- added same-file and file-plus-section Markdown section locator support;
- added `fixtures/valid-template-section-candidate.md`;
- added `fixtures/valid-crlf-normalization.md`;
- added `failure-cases/template-fixed-missing-body-hash.md`;
- updated validator contract, source map, and oracle.

Template source check:

```text
templates/review-candidate.md:41 review_object_state: draft | fixed_for_review | revised_after_review | archived
templates/review-candidate.md:42 candidate_body_location: "# Candidate Body"
templates/review-candidate.md:43 body_hash:
templates/review-candidate.md:44 body_hash_algorithm: sha256_utf8_lf_trim_body_without_heading
```

Positive fixture rerun:

```text
POSITIVE_FIXTURES_PASS_AFTER_REPAIR exit=0
```

Failure case rerun:

```text
FAILURE_CASE_EXPECTED_BLOCK_AFTER_REPAIR body-hash-mismatch.md code=body_hash_mismatch
FAILURE_CASE_EXPECTED_BLOCK_AFTER_REPAIR checked-body-hash-mismatch.md code=checked_body_hash_mismatch
FAILURE_CASE_EXPECTED_BLOCK_AFTER_REPAIR fixed-approved-missing-body-hash.md code=fixed_or_approved_missing_body_hash
FAILURE_CASE_EXPECTED_BLOCK_AFTER_REPAIR template-fixed-missing-body-hash.md code=fixed_or_approved_missing_body_hash
FAILURE_CASE_EXPECTED_BLOCK_AFTER_REPAIR writeback-ready-body-changed.md code=writeback_ready_body_changed
FAILURE_CASES_PASS_AFTER_REPAIR count=5
```

CRLF literal check:

```text
CRLF_NORMALIZATION_PASS hash=2f9ce0b72be8c99f2560d28081f32ace70d5ff46c732191ea75ca22158af8e3e
```

Script syntax after repair:

```text
PY_COMPILE_PASS_AFTER_REPAIR
REMOVED_SANDBOX_RUNTIME_CACHE_AFTER_REPAIR
```

## Path Guard Repair Verification

Boundary Round 1 noted that the first script version allowed absolute
`candidate_body_location` paths. Builder repaired the sandbox prototype so
file-based body locations must resolve inside the record directory.

Final fixture rerun after path guard:

```text
POSITIVE_FIXTURES_PASS_AFTER_PATH_GUARD exit=0
FAILURE_CASES_PASS_AFTER_PATH_GUARD count=5
FINAL_FIXTURE_COUNT fixtures=5 failure_cases=5
PY_COMPILE_PASS_AFTER_PATH_GUARD
REMOVED_SANDBOX_RUNTIME_CACHE_AFTER_PATH_GUARD
```
