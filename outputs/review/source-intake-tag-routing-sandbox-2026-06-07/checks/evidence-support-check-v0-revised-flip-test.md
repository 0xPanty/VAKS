---
record_kind: sandbox_pressure_test
status: pass
created_at: 2026-06-07
topic_id: source-intake-routing
scope: evidence-support-check v0 revised answer flip test
truth_boundary: sandbox check only; not reviewed knowledge; not action basis
action_basis_allowed: false
truth_mutation_allowed: false
---

# Evidence Support Check v0 Revised Flip Test

## Purpose

Verify that the checker can guide a mixed answer from blocked to draft-ready
after unsupported or overclaimed parts are removed or rewritten.

This test is the counterpart to the mixed pressure test:

```text
mixed fixture:
  supported=2
  missing_evidence=2
  answer_readiness=not_ready

revised fixture:
  supported=4
  missing_evidence=0
  answer_readiness=ready_for_answer_draft
```

The point is not to make a production answer generator. The point is to verify
that the workbench gives actionable feedback:

```text
keep the supported claims
rewrite or remove the blockers
rerun the same support check
only then return to answer-draft readiness
```

## Fixture

```text
fixtures/evidence-support-check-v0-revised-source-intake.json
```

The revised fixture keeps the two supported mixed claims:

```text
r1: anchor_queue is preparation only and needs evidence support check
r2: selector/snippet are navigation only, not evidence support
```

It rewrites the two blocked mixed claims into field-anchored boundary claims:

```text
r3: v0 records citation_faithfulness_checked=false
r4: sandbox records action_basis_allowed=false
```

This uses explicit local fields instead of natural-language denial as the main
support surface, which avoids fighting the negation-context guard.

## Result

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-evidence-support-check-v0.ps1 `
  -Root . `
  -PackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\source-intake-routing-workbench-pack-query-action-generated.md `
  -ClaimSpecPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures\evidence-support-check-v0-revised-source-intake.json `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\evidence-support-check-v0-revised-generated.md `
  -AnswerReadyOutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-ready-context-pack-v0-revised-generated.md `
  -Json
```

Result:

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

Generated outputs:

```text
checks/evidence-support-check-v0-revised-generated.md
checks/answer-ready-context-pack-v0-revised-generated.md
```

## Claim-Level Outcome

```text
r1 supported
  selectors: line:633, line:255

r2 supported
  selector: line:219

r3 supported
  selectors: line:116, line:24
  matched fields: citation_faithfulness_checked=false / citation_faithfulness_checked: false

r4 supported
  selectors: line:8, line:240, line:109
  matched fields: action_basis_allowed: false / action_basis_allowed=false
```

## Four-Fixture Regression

The revised flip test was run with the existing positive, negative, and mixed
fixtures.

```text
positive fixture:
  supported=4
  missing_evidence=0
  answer_readiness=ready_for_answer_draft

negative fixture:
  supported=0
  missing_evidence=4
  answer_readiness=not_ready

mixed fixture:
  supported=2
  missing_evidence=2
  answer_readiness=not_ready

revised fixture:
  supported=4
  missing_evidence=0
  answer_readiness=ready_for_answer_draft
```

## Outcome

The workbench now demonstrates a useful repair loop:

```text
detect unsupported / overclaimed claims
preserve supported anchors
rewrite blockers into supported boundary claims
rerun the check
flip not_ready -> ready_for_answer_draft
```

Boundary remains unchanged:

```text
ready_for_answer_draft != action basis
field support != reviewed truth
citation_faithfulness_checked=false means citation faithfulness is not checked
action_basis_allowed=false means action-facing use still needs human review
```
