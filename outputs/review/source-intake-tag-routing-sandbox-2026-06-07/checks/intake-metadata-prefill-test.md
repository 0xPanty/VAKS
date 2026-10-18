---
type: sandbox_check
status: pass
created_at: 2026-06-07
scope: source intake metadata prefill optimization
truth_boundary: sandbox evidence only; not reviewed knowledge; not action basis
---

# Intake Metadata Prefill Test

## Question

Does pre-filling a small number of discovery metadata fields at intake improve
retrieval without creating authority leakage?

## Patch Under Test

```text
15_INTAKE_METADATA_PREFILL_OPTIMIZATION.md
fixtures/source-card-prefilled-discovery-metadata.md
fixtures/source-card-no-prefill-control.md
fixtures/source-card-bad-prefill-authority.md
fixtures/intake-metadata-suggestion-bad-persistent.md
tools/vaks-intake-metadata-lint.ps1
```

## Metadata Lint

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-intake-metadata-lint.ps1 -Root .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures
```

Result:

```text
files_checked=7
pass=4
fail=3
```

Expected failing fixtures:

```text
intake-metadata-suggestion-bad-persistent.md
source-card-bad-prefill-authority.md
source-card-forbidden-authority-tags.md
```

Interpretation:

```text
The lint accepts confirmed discovery metadata and a non-persistent suggestion
sidecar. It rejects persistent suggestions, authority-like topics/entities/tags,
too many topics, non-registry topics, and action_basis_allowed on source cards.
```

## A/B Retrieval Check

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-retrieval-mvp.ps1 -Root .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures -Pattern 'metadata-routing|DataChain|registry-before-recompute' -Mode source-inspection -Limit 100 -Json
```

Result:

```text
total_hits=6
prefilled_hit=True
control_hit=False
bad_authority_hit=False
```

Interpretation:

```text
The source card with prefilled topics/entities/aliases is discoverable by
metadata terms even though its body text is generic. The equivalent control
source card without prefilled discovery metadata is not retrieved.
```

## Lane Boundary Regression Check

Commands:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-retrieval-mvp.ps1 -Root . -Pattern 'artifact registry|context pack builder|obsidian workbench|source-intake-routing|registry-before-recompute|metadata prefill' -Mode current-rule -Limit 200
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-retrieval-mvp.ps1 -Root . -Pattern 'artifact registry|context pack builder|obsidian workbench|source-intake-routing|registry-before-recompute|metadata prefill' -Mode action -Limit 200
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-retrieval-mvp.ps1 -Root . -Pattern 'artifact registry|context pack builder|obsidian workbench|source-intake-routing|registry-before-recompute|metadata prefill' -Mode audit -Limit 200
```

Result:

```text
mode=current-rule
total_hits=53
included_by_default: mainline_current=5 only

mode=action
total_hits=53
included_by_default: mainline_current=5, raw_drilldown=2, reviewed_support=2

mode=audit
total_hits=53
included_by_default: audit_evidence=23, mainline_current=5
```

Interpretation:

```text
Prefill improves discovery inside the allowed slice, but it does not change the
authority/status/project boundary. Sandbox artifacts remain audit evidence, raw
sources remain provenance drilldown, and candidate/provisional content does not
become action basis.
```

## Existing Lints

Usage-layer lint:

```text
files_checked=17
pass=16
fail=1
expected_fail=usage-layer-bad-authority-leak.md
```

KP lint:

```text
files_checked=2
pass=1
fail=1
expected_fail=candidate-distillation-bad-kp.md
```

## Verdict

```text
Use intake prefill, but keep it small and low-authority:

- prefill topics/entities/aliases/content_form/language/version_or_time_scope
- keep topics to 1-2 registry terms
- keep entities to a short recall list
- use sidecar suggestions when uncertain
- never prefill reviewed/adopted/action-basis/project borrowing judgments
- always run authority/status/project filters before topic/entity ranking
```

This gives a real retrieval lift while preserving the Source Intake Control Flow
guardrails.
