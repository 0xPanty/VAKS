---
type: sandbox_check
status: completed
created_at: 2026-06-06
truth_boundary: test report only; not action basis
---

# Misa Test Run

## Command

Run from:

```text
C:\Users\Administrator\Documents\New project\misa-cybernetic-evolution
```

Command:

```powershell
node --test --test-concurrency=1 test/v028-runtime-thread.test.mjs test/component-health.test.mjs test/sidecar-status.test.mjs test/vps-shadow-deploy.test.mjs
```

## Result

```text
tests: 25
pass: 25
fail: 0
duration_ms: 4209.4459
```

## Boundary

This proves the referenced Misa local test slice still passes. It does not prove
that any overlay entry is ready for action. Action-facing use still requires
v0.2.13.

## Misa Worktree After Test

```text
## main...origin/main
?? docs/current/_handoff-next-window.md
```

Only the pre-existing untracked handoff file is visible.

