---
type: sandbox_check
status: completed
created_at: 2026-06-06
truth_boundary: repeated test report only
---

# Repeated Full Sandbox Test 2

## Purpose

This reruns the core checks after the first package was assembled. The goal is
to avoid treating one green pass as enough.

## Field Check

```text
MISA.md: entries=8 kp_ref=8 stance=8 borrow_scope=8 updated_at=8
VAKS.md: entries=6 kp_ref=6 stance=6 borrow_scope=6 updated_at=6
```

Result:

```text
pass
```

## Strict Live Overlay Forbidden-Language Scan

Scope:

```text
project_overlays/
```

Result:

```text
matches: 0
rg exit code: 1
pass
```

## Mainline Contamination Check

Checked:

```text
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SCHEMA.md
REVIEW_QUEUE.md
templates/
staged area
```

Result:

```text
diff_files: 0
staged_files: 0
pass
```

## Misa Target Hint Check

```text
checked: 18
missing_or_weak: 0
pass
```

## Misa Deterministic Test Slice

Command:

```powershell
node --test --test-concurrency=1 test/v028-runtime-thread.test.mjs test/component-health.test.mjs test/sidecar-status.test.mjs test/vps-shadow-deploy.test.mjs
```

Result:

```text
tests: 25
pass: 25
fail: 0
duration_ms: 4375.1285
```

## Verdict

The second full sandbox pass matches the first pass:

```text
lightweight overlay shape holds
mainline remains untouched
Misa project anchors remain concrete
Misa local test slice remains green
```

