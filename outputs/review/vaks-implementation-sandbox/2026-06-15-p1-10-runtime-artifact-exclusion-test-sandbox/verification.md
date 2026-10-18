---
record_kind: sandbox_verification
slice_id: 2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox
status: local_verification_passed
truth_boundary: sandbox_verification_only
---

# Verification

## Commands Run

```powershell
python -B -m py_compile `
  outputs/review/vaks-implementation-sandbox/2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox/artifact/runtime_artifact_exclusion_test.py `
  outputs/review/vaks-implementation-sandbox/2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox/artifact/verify_runtime_artifact_exclusion_test.py

python -B outputs/review/vaks-implementation-sandbox/2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox/artifact/verify_runtime_artifact_exclusion_test.py
```

## Result

```text
py_compile: pass
suite_runner: pass
positive_fixtures: 4
failure_cases: 20
failures: 0
```

## Verified Positive Fixtures

- `fixtures/valid-mixed-corpus-runtime-excluded.json`
- `fixtures/valid-query-loop-output-excluded.json`
- `fixtures/valid-durable-sandbox-doc-not-runtime.json`
- `fixtures/valid-derived-index-excluded-with-raw-anchor.json`

## Verified Failure Cases

- runtime filter disabled;
- runtime cache/bytecode/log/output selected;
- suite/verifier/generated outputs used as support or action basis;
- runtime artifact missing or using bad exclusion reason;
- path/kind runtime mismatch;
- unknown artifact kind;
- runtime artifact with reviewed authority bucket;
- runtime artifact with raw authority bucket;
- runtime artifact with support authority bucket;
- runtime artifact with action authority bucket;
- runtime artifact claiming authority;
- runtime artifact using `evidence_support` or `action_basis` pack roles;
- runtime paths with underscore or space separators that try to masquerade as
  durable sandbox documents;
- duplicate item id;
- missing item list.

Each failure case was invalid and emitted its expected issue code.

## Reviewer-Triggered Revision

The first Reviewer pass found blocking gaps:

- `ACTION_ROLES` was defined but not used, allowing `pack_role: action_basis`.
- `SUPPORT_ROLES` lacked `evidence_support`.
- Runtime path detection did not normalize `_`, `-`, and space variants.

Builder fixed these inside this sandbox:

- `evidence_support` is now a support role.
- `action_basis` and `ready_action_basis` pack/evidence roles are blocked as
  action basis.
- Runtime path detection normalizes underscore and space variants.
- New failure cases cover action-basis pack role, evidence-support pack role,
  underscore runtime path, and space-separated runtime path.

After these fixes, the suite passed with 4 positive fixtures and 17 failure
cases.

The Reviewer then found one remaining blocker: `authority_bucket: support` was
not included in the runtime-forbidden authority bucket set. Builder added
`support` to the forbidden set and added
`failure-cases/runtime-support-authority-bucket.json`. After that fix, the
suite passed with 4 positive fixtures and 18 failure cases.

Product Acceptance then returned `REVISE_BEFORE_NEXT` because the contract also
forbids literal `authority_bucket: raw` and `authority_bucket: action`, while
the implementation only covered `raw_anchor` and `action_basis`. Builder added
`raw` and `action` to the forbidden authority bucket set and added
`failure-cases/runtime-raw-authority-bucket.json` and
`failure-cases/runtime-action-authority-bucket.json`. After that fix, the suite
passed with 4 positive fixtures and 20 failure cases.

## Cache Cleanup

`py_compile` created a local `__pycache__` under the sandbox artifact directory.
It was removed after verification. This cleanup stayed inside the approved
sandbox path.

## Non-Claims

Passing verification means only that this sandbox runtime artifact exclusion
test behaves as expected on its fixtures and failure cases. It is not reviewer
approval, product acceptance, evidence support, reviewed knowledge, action
basis, mainline readiness, commit approval, push approval, or Obsidian sync
approval.
