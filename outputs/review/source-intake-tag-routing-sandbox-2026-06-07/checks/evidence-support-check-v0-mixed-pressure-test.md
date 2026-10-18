---
record_kind: sandbox_pressure_test
status: pass
created_at: 2026-06-07
topic_id: source-intake-routing
scope: evidence-support-check v0 mixed pressure test
truth_boundary: sandbox check only; not reviewed knowledge; not action basis
action_basis_allowed: false
truth_mutation_allowed: false
---

# Evidence Support Check v0 Mixed Pressure Test

## Purpose

Test the realistic case where one answer candidate contains both supported and
unsupported claims.

Expected behavior:

```text
supported claims keep their anchors
unsupported claims stay missing_evidence
failure origins remain visible
overall answer_readiness stays not_ready
action_basis_allowed remains false
```

This test does not add a new evaluator or truth rule. It only verifies whether
the v0 checker can avoid both failure modes:

```text
do not approve the whole answer just because some claims are supported
do not discard supported claims just because other claims are missing evidence
```

## Fixture

```text
fixtures/evidence-support-check-v0-mixed-source-intake.json
```

The mixed fixture contains:

```text
m1: supported anchor_queue boundary claim
m2: supported selector/snippet navigation-only claim
m3: unsupported citation-faithfulness overclaim
m4: unsupported action-basis overclaim
```

The fixture also gives missing claims explicit diagnostic origins:

```text
m3 -> missing_evidence_or_unavailable_support
m4 -> scope_mismatch_or_overclaim
```

## Small Tool Change

The checker still uses the same support statuses:

```text
supported
weakly_supported
missing_evidence
unsupported
not_checked
```

The only diagnostic addition is:

```text
failure_origin_if_missing
```

When a fixture provides this field and no source-span support is found, the
generated evidence map uses the configured failure origin. This keeps the
answer-ready pack readable without inventing a new scoring system.

The answer-ready context pack now also prints `failure_origin` for each claim.

## Result

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-evidence-support-check-v0.ps1 `
  -Root . `
  -PackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\source-intake-routing-workbench-pack-query-action-generated.md `
  -ClaimSpecPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures\evidence-support-check-v0-mixed-source-intake.json `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\evidence-support-check-v0-mixed-generated.md `
  -AnswerReadyOutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-ready-context-pack-v0-mixed-generated.md `
  -Json
```

Result:

```json
{
  "anchor_queue_total": 29,
  "claims_checked": 4,
  "supported": 2,
  "weakly_supported": 0,
  "unsupported": 0,
  "missing_evidence": 2,
  "answer_readiness": "not_ready",
  "action_basis_allowed": false,
  "citation_faithfulness_checked": false
}
```

Generated outputs:

```text
checks/evidence-support-check-v0-mixed-generated.md
checks/answer-ready-context-pack-v0-mixed-generated.md
```

## Claim-Level Outcome

```text
m1 supported
  support_channel: context_pack_metadata, explicit_fixture_ref
  selectors: line:633, line:255

m2 supported
  support_channel: explicit_fixture_ref
  selector: line:219

m3 missing_evidence
  failure_origin: missing_evidence_or_unavailable_support

m4 missing_evidence
  failure_origin: scope_mismatch_or_overclaim
```

## Regression Set

The mixed test was run together with the existing positive and negative
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
```

## Outcome

The workbench can now preserve partial support without allowing an unsafe final
answer draft.

In practical terms:

```text
good claims remain usable as anchored context
bad claims remain visible as blockers
the whole answer is not ready until missing or overclaimed parts are removed,
rewritten, or reviewed
```

Boundary remains unchanged:

```text
answer-ready != action basis
support check != truth layer
failure origin != reviewed judgment
citation correctness marker != citation faithfulness
```
