---
type: sandbox_kp_lint_test
status: pass_with_expected_failure
created_at: 2026-06-07
scope: candidate point kp_ref lint
truth_boundary: sandbox lint only
---

# KP Lint Test

## Tool

```text
tools/vaks-kp-lint.ps1
```

## Fixtures

```text
fixtures/candidate-distillation-kp-refs.md
fixtures/candidate-distillation-bad-kp.md
```

## Result

```text
files_checked=2
pass=1
fail=1
```

Good fixture:

```text
candidate-distillation-kp-refs.md
kp_ref_count=2
status=pass
```

Bad fixture:

```text
candidate-distillation-bad-kp.md
kp_ref_count=2
status=fail
issues:
  - kp_ref_bad_format:KP-reviewed-001
  - kp_ref_authority_word:KP-reviewed-001
  - duplicate_kp_ref:KP-reviewed-001
```

## Verdict

```text
kp_lint_test: pass_with_expected_failure
kp_good_fixture_passed: yes
kp_bad_fixture_blocked: yes
```
