---
record_kind: sandbox_pressure_test
status: pass
created_at: 2026-06-07
topic_id: source-intake-routing
scope: evidence-support-check v0 negative pressure test
truth_boundary: sandbox check only; not reviewed knowledge; not action basis
action_basis_allowed: false
truth_mutation_allowed: false
---

# Evidence Support Check v0 Negative Pressure Test

## Purpose

Test whether the v0 support checker can cleanly reject deliberately unsupported
or scope-mismatched answer claims.

This test is intentionally narrow. It does not add an evaluator, score,
retriever, LLM judge, or truth-layer rule.

## Negative Fixture

```text
fixtures/evidence-support-check-v0-negative-source-intake.json
```

The negative fixture asks the checker to validate four bad claim types:

```text
n1: action-basis overclaim
n2: navigation-as-support overclaim
n3: production-evaluator scope overclaim
n4: truth-layer promotion overclaim
```

Expected result:

```text
supported=0
missing_evidence=4
answer_readiness=not_ready
```

## First Run Finding

The first pressure run caught a real false positive:

```text
supported=1
missing_evidence=3
answer_readiness=not_ready
```

The false positive was `n3`.

Root cause:

```text
The checker matched "production RAG" inside non-goal / negated context:

21_EVIDENCE_SUPPORT_CHECK_V0_LANDING.md
  Supported does not mean:
    production RAG grounding

20_EVIDENCE_SUPPORT_CHECK_REFERENCE_DISTILLATION.md
  Non-Goals
    production RAG
```

This proved the old scan was still too lexical: it could find the right words
without noticing that the words were used as exclusions.

## Patch

The checker now skips matches in excluded support context:

```text
current line negation
nearby "Supported does not mean"
nearby "Non-Goals"
nearby "must not become"
nearby forbidden-use wording
```

This is deliberately small. It is a guardrail around local pattern matching,
not a semantic classifier.

## Documentation Pollution Check

After the first patch, the pressure test report and landing note were added.
A rerun then exposed a second useful failure:

```text
supported=2
missing_evidence=2
answer_readiness=not_ready
```

Root cause:

```text
The new documentation repeated two bad claims as plain text inside the landing
note. Because that landing note was a preferred reference, the checker treated
the repeated test claims as positive support.
```

Fix:

```text
1. Excluded support context now also catches negative fixture / bad claim /
   deliberately checks / unsupported-and-scope-mismatched wording.
2. The landing note and pressure report now describe bad claims as short
   overclaim labels instead of replaying the unsupported claims verbatim.
```

This matters because sandbox documentation can itself become retrievable
context. Negative examples must not accidentally create positive support.

## Final Negative Result

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-evidence-support-check-v0.ps1 `
  -Root . `
  -PackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\source-intake-routing-workbench-pack-query-action-generated.md `
  -ClaimSpecPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures\evidence-support-check-v0-negative-source-intake.json `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\evidence-support-check-v0-negative-generated.md `
  -AnswerReadyOutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-ready-context-pack-v0-negative-generated.md `
  -Json
```

Result:

```json
{
  "anchor_queue_total": 29,
  "claims_checked": 4,
  "supported": 0,
  "weakly_supported": 0,
  "unsupported": 0,
  "missing_evidence": 4,
  "answer_readiness": "not_ready",
  "action_basis_allowed": false,
  "citation_faithfulness_checked": false
}
```

Generated outputs:

```text
checks/evidence-support-check-v0-negative-generated.md
checks/answer-ready-context-pack-v0-negative-generated.md
```

## Positive Regression

The original positive fixture still passes after the guard:

```json
{
  "anchor_queue_total": 29,
  "claims_checked": 4,
  "supported": 4,
  "weakly_supported": 0,
  "unsupported": 0,
  "missing_evidence": 0,
  "answer_readiness": "ready_for_answer_draft",
  "action_basis_allowed": false,
  "citation_faithfulness_checked": false
}
```

## Outcome

The v0 checker now catches the most important early failure mode:

```text
unsupported / scope-mismatched answer claims stay missing_evidence
negated or non-goal language does not count as positive support
positive answer-draft claims still resolve to source-span support
```

This is a real workbench-quality improvement, but it stays within the sandbox
boundary:

```text
answer-ready != action basis
support check != truth layer
local pattern match != citation faithfulness
negative pressure test != production evaluator
```
