---
type: sandbox_check
status: pass_with_expected_failure
created_at: 2026-06-07
scope: usage-layer lint test for registry, context-pack, and workbench fixtures
truth_boundary: sandbox check only; process evidence, not reviewed knowledge
---

# Usage-Layer Lint Test

## Tool

```text
tools/vaks-usage-layer-lint.ps1
```

## Command

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-usage-layer-lint.ps1 `
  -Root .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures
```

## Result

```text
files_checked=13
pass=12
fail=1
status=pass_with_expected_failure
```

Expected failing fixture:

```text
fixtures/usage-layer-bad-authority-leak.md
```

Detected issues:

```text
context_pack_missing:coverage_overview
context_pack_missing:context_pack_trace
candidate_item_action_leak
```

## Interpretation

The lint catches the exact failure this sandbox must prevent:

```text
candidate_orientation item
-> citable_status: span_ready
-> action_basis_allowed: true
```

That path is forbidden.

Good fixtures passed:

```text
artifact-registry-source-intake.md
context-pack-builder-v0-source-intake.md
obsidian-workbench-entrypoint-source-intake.md
```

This test does not prove production readiness.

It proves that the candidate usage-layer contract can detect a basic authority
leak before mainline writeback.
