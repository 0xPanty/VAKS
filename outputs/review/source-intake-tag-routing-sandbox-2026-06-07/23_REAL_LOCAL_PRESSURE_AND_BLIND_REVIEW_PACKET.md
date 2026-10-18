---
record_kind: blind_review_packet_candidate
status: candidate
created_at: 2026-06-07T19:35:00+08:00
topic_id: source-intake-routing
truth_boundary: review_packet_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
---

# Real Local Pressure And Blind Review Packet

## Reviewer Instruction

Review this packet cold. Do not rely on chat context.

This is a sandbox-only workbench prototype. It is not mainline architecture, not
SCHEMA, not reviewed knowledge, not action basis, and not reviewer approval.

## What To Review

The current candidate chain is:

```text
real local question
-> context pack
-> evidence support check
-> answer-ready pack
-> answer draft skeleton
-> human-readable smoke draft
-> smoke lint
```

Review whether this chain is honestly bounded and whether the real-local tests
support the claimed maturity.

## Primary Files

```text
checks/real-local-answer-draft-smoke-pressure-test.md
checks/real-local-question-pack-smoke-boundary-generated.md
checks/real-local-question-pack-action-basis-generated.md
fixtures/evidence-support-check-v0-real-local-smoke-boundary.json
fixtures/evidence-support-check-v0-real-local-action-basis-negative.json
checks/evidence-support-check-v0-real-local-smoke-boundary-generated.md
checks/evidence-support-check-v0-real-local-action-basis-negative-generated.md
checks/answer-ready-context-pack-v0-real-local-smoke-boundary-generated.md
checks/answer-ready-context-pack-v0-real-local-action-basis-negative-generated.md
checks/answer-draft-skeleton-v0-real-local-smoke-boundary-generated.md
checks/answer-draft-skeleton-v0-real-local-action-basis-negative-blocked-generated.md
checks/answer-draft-smoke-v0-real-local-smoke-boundary-generated.md
checks/answer-draft-smoke-v0-real-local-action-basis-negative-blocked-generated.md
checks/answer-draft-smoke-v0-real-local-smoke-boundary-lint-generated.md
checks/answer-draft-smoke-v0-real-local-action-basis-negative-blocked-lint-generated.md
```

Upstream smoke-lint boundary context:

```text
22_ANSWER_DRAFT_SMOKE_V0_OPUS_REVIEW_BRIEF.md
checks/answer-draft-smoke-v0-test.md
tools/vaks-answer-draft-smoke-lint-v0.ps1
```

## Blind Review Protocol

Do not inspect any author-recorded result summary before running the commands.

After completing your own run, compare against:

```text
23A_AUTHOR_RECORDED_RESULTS_AFTER_BLIND_RUN.md
```

That file is an after-run appendix, not part of the cold packet.

## Read-Only Blind Commands

Run from:

```text
C:\Users\Administrator\Documents\资料库
```

These commands use `-Json` and omit write-output parameters. They print results
without refreshing generated sandbox files.

Real local ready support:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-evidence-support-check-v0.ps1 `
  -Root . `
  -PackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\real-local-question-pack-smoke-boundary-generated.md `
  -ClaimSpecPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures\evidence-support-check-v0-real-local-smoke-boundary.json `
  -Json
```

Real local negative support:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-evidence-support-check-v0.ps1 `
  -Root . `
  -PackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\real-local-question-pack-action-basis-generated.md `
  -ClaimSpecPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures\evidence-support-check-v0-real-local-action-basis-negative.json `
  -Json
```

Real local ready skeleton:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-answer-draft-skeleton-v0.ps1 `
  -Root . `
  -AnswerReadyPackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-ready-context-pack-v0-real-local-smoke-boundary-generated.md `
  -Json
```

Real local negative skeleton:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-answer-draft-skeleton-v0.ps1 `
  -Root . `
  -AnswerReadyPackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-ready-context-pack-v0-real-local-action-basis-negative-generated.md `
  -Json
```

Real local ready smoke lint:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-answer-draft-smoke-lint-v0.ps1 `
  -Root . `
  -SkeletonPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-draft-skeleton-v0-real-local-smoke-boundary-generated.md `
  -DraftPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-draft-smoke-v0-real-local-smoke-boundary-generated.md `
  -Json
```

Real local negative smoke lint:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-answer-draft-smoke-lint-v0.ps1 `
  -Root . `
  -SkeletonPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-draft-skeleton-v0-real-local-action-basis-negative-blocked-generated.md `
  -DraftPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-draft-smoke-v0-real-local-action-basis-negative-blocked-generated.md `
  -Json
```

Optional context-pack lint:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-context-pack-lint.ps1 `
  -Root .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07
```

Optional JSON fixture parse:

```powershell
$root = '.\outputs\review\source-intake-tag-routing-sandbox-2026-06-07'
$files = Get-ChildItem -LiteralPath "$root\fixtures" -Filter '*.json' -File
foreach ($file in $files) {
  Get-Content -Raw -LiteralPath $file.FullName | ConvertFrom-Json | Out-Null
}
$files.Count
```

Optional truth-layer status check:

```powershell
git status --short -- `
  SCHEMA.md `
  ARCHITECTURE_PRINCIPLES.md `
  FUSION_ARCHITECTURE_V0_2_DRAFT.md `
  wiki/claims `
  wiki/decisions `
  wiki/patterns
```

Optional formal Obsidian sync hash check:

```powershell
$repo = 'C:\Users\Administrator\Documents\资料库'
$vault = 'H:\Obsidian\资料库'
$rel = 'outputs\review\source-intake-tag-routing-sandbox-2026-06-07'
$src = Join-Path $repo $rel
$dst = Join-Path $vault $rel
$srcFiles = Get-ChildItem -LiteralPath $src -Recurse -File
$mismatch = 0
foreach ($sf in $srcFiles) {
  $relative = $sf.FullName.Substring($src.Length).TrimStart('\')
  $tf = Join-Path $dst $relative
  if (-not (Test-Path -LiteralPath $tf)) { $mismatch++; continue }
  if ((Get-FileHash -LiteralPath $sf.FullName).Hash -ne (Get-FileHash -LiteralPath $tf).Hash) {
    $mismatch++
  }
}
[pscustomobject]@{ files = $srcFiles.Count; mismatch = $mismatch }
```

## Known Limits To Evaluate

These limits are in scope for review. They are not solved by this packet.

```text
real-local positive support is partly self-referential author-document support;
  it checks anchored string support, not independent evidence maturity

negative real-local claims are author-constructed misses;
  they test no support fabrication, not robust semantic overclaim detection

Test-ExcludedSupportContext is a lexical negation guard with a small window;
  it can false-positive near "not" and can miss differently phrased negation

real-local fixtures did not exercise required_support_channels or weakly_supported;
  those paths remain covered by earlier synthetic containment fixtures only

supported / ready_for_answer_draft remains diagnostic answer preparation;
  it is not truth, reviewer approval, faithfulness, coverage, or action basis
```

## Review Questions

```text
1. Do the real-local samples use actual local files, not only pr1/pr2/pr3 hand examples?
2. Does the ready sample stay inside shape/ref-handle guarantees?
3. Does the negative action-basis sample stay blocked and emit no draft text?
4. Are semantic support, faithfulness, coverage, and omission still kept outside smoke lint?
5. Does the support check prove anything beyond anchored string/selector presence?
6. Can the negative case catch semantic overclaim, or only missing string support?
7. Is this ready for a sandbox candidate commit only, not mainline/schema adoption?
```

## Blind Status

This packet is ready for a cleaner blind non-author review because it no longer
contains author-recorded result values before the commands.

The author-recorded result appendix exists for after-run comparison only. A
strict blind reviewer should use this packet and the files it points to, not
chat context and not the after-run appendix.
