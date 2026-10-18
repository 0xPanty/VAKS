---
record_kind: author_recorded_results_after_blind_run_candidate
status: candidate
created_at: 2026-06-07T20:10:00+08:00
topic_id: source-intake-routing
truth_boundary: author_report_not_blind_evidence
action_basis_allowed: false
truth_mutation_allowed: false
---

# Author Recorded Results After Blind Run

Do not use this file for an initial cold review. Open it only after running the
commands in:

```text
23_REAL_LOCAL_PRESSURE_AND_BLIND_REVIEW_PACKET.md
```

## Author Refresh Output Commands

These commands write or refresh generated sandbox files. Do not use them for an
initial blind read-only run.

Run from:

```text
C:\Users\Administrator\Documents\资料库
```

Real local ready support refresh:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-evidence-support-check-v0.ps1 `
  -Root . `
  -PackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\real-local-question-pack-smoke-boundary-generated.md `
  -ClaimSpecPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures\evidence-support-check-v0-real-local-smoke-boundary.json `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\evidence-support-check-v0-real-local-smoke-boundary-generated.md `
  -AnswerReadyOutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-ready-context-pack-v0-real-local-smoke-boundary-generated.md `
  -Json
```

Real local negative support refresh:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-evidence-support-check-v0.ps1 `
  -Root . `
  -PackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\real-local-question-pack-action-basis-generated.md `
  -ClaimSpecPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures\evidence-support-check-v0-real-local-action-basis-negative.json `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\evidence-support-check-v0-real-local-action-basis-negative-generated.md `
  -AnswerReadyOutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-ready-context-pack-v0-real-local-action-basis-negative-generated.md `
  -Json
```

Real local ready skeleton refresh:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-answer-draft-skeleton-v0.ps1 `
  -Root . `
  -AnswerReadyPackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-ready-context-pack-v0-real-local-smoke-boundary-generated.md `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-draft-skeleton-v0-real-local-smoke-boundary-generated.md `
  -Json
```

Real local negative skeleton refresh:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-answer-draft-skeleton-v0.ps1 `
  -Root . `
  -AnswerReadyPackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-ready-context-pack-v0-real-local-action-basis-negative-generated.md `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-draft-skeleton-v0-real-local-action-basis-negative-blocked-generated.md `
  -Json
```

Real local ready smoke lint refresh:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-answer-draft-smoke-lint-v0.ps1 `
  -Root . `
  -SkeletonPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-draft-skeleton-v0-real-local-smoke-boundary-generated.md `
  -DraftPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-draft-smoke-v0-real-local-smoke-boundary-generated.md `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-draft-smoke-v0-real-local-smoke-boundary-lint-generated.md `
  -Json
```

Real local negative smoke lint refresh:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-answer-draft-smoke-lint-v0.ps1 `
  -Root . `
  -SkeletonPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-draft-skeleton-v0-real-local-action-basis-negative-blocked-generated.md `
  -DraftPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-draft-smoke-v0-real-local-action-basis-negative-blocked-generated.md `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-draft-smoke-v0-real-local-action-basis-negative-blocked-lint-generated.md `
  -Json
```

## Real Local Results

```text
real-local ready support:
  claims_checked=5
  supported=5
  missing_evidence=0
  answer_readiness=ready_for_answer_draft

real-local ready skeleton:
  draft_skeleton_state=ready_for_human_draft
  draft_claims_emitted=5

real-local ready smoke lint:
  status=pass
  draft_answer_lines=5
  unknown_claim_refs=0

real-local negative support:
  claims_checked=4
  supported=0
  missing_evidence=4
  answer_readiness=not_ready

real-local negative skeleton:
  draft_skeleton_state=blocked_not_ready
  draft_claims_emitted=0

real-local negative smoke lint:
  status=pass
  draft_answer_lines=0
```

## Existing Smoke Matrix

```text
ready: pass
blocked: pass
empty claim_refs: expected fail / actual fail
paragraph blocked answer: expected fail / actual fail
fenced heading blocked answer: expected fail / actual fail
mismatched ref known limitation: expected pass / actual pass
omitted claim known limitation: expected pass / actual pass
```

## Supporting Regression

```text
evidence support regression: 8 checked / expected results preserved
context-pack lint: 17 checked / 16 pass / 1 expected fail
json fixture parse: 12 checked / 12 pass
boundary scan: no unexpected forbidden true flags outside fixtures/tools/expected-fail reports
truth layer: no changes in SCHEMA / ARCHITECTURE / FUSION / claims / decisions / patterns
formal Obsidian sync before blind-review absorption: 157 files / 157 hash match
```

These are author-recorded outputs. They are useful for comparison, but they are
not blind evidence by themselves.
