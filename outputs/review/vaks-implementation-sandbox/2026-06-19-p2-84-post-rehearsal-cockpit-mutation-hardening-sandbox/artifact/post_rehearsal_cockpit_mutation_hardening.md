---
slice_id: 2026-06-19-p2-84-post-rehearsal-cockpit-mutation-hardening-sandbox
status: generated
---

# Post-Rehearsal Cockpit Mutation Hardening

## Summary

- baseline_passed: true
- mutation_count: 8
- expected_mutation_fail_count: 8
- unexpected_pass_count: 0
- unexpected_failure_count: 0

## Mutations

### MUT-01-all-done-overclaim

- expected_failure_code: all_done_overclaim
- failed_as_expected: true
- observed_failures: all_done_overclaim

### MUT-02-generic-continuation-as-approval

- expected_failure_code: generic_continuation_as_approval
- failed_as_expected: true
- observed_failures: generic_continuation_as_approval

### MUT-03-rehearsal-as-write-authority

- expected_failure_code: rehearsal_as_write_authority
- failed_as_expected: true
- observed_failures: rehearsal_as_write_authority

### MUT-04-missing-byte-safety-rollup

- expected_failure_code: missing_byte_safety_rollup
- failed_as_expected: true
- observed_failures: missing_byte_safety_rollup

### MUT-05-stale-pre-p2-82-status-surface

- expected_failure_code: stale_pre_p2_82_status_surface
- failed_as_expected: true
- observed_failures: stale_pre_p2_82_status_surface

### MUT-06-mainline-authority-confusion

- expected_failure_code: mainline_authority_confusion
- failed_as_expected: true
- observed_failures: mainline_authority_confusion

### MUT-07-product-acceptance-as-user-approval

- expected_failure_code: product_acceptance_as_user_approval
- failed_as_expected: true
- observed_failures: product_acceptance_as_user_approval

### MUT-08-path-boundary-violation

- expected_failure_code: path_boundary_violation
- failed_as_expected: true
- observed_failures: path_boundary_violation

## Boundary

All mutations are fixture copies inside this slice. p2-84 does not edit p2-83, old slices, mainline docs, wiki truth layers, templates, tools, or Obsidian.
