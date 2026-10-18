---
record_kind: sandbox_pressure_test
status: pass
created_at: 2026-06-07
topic_id: source-intake-routing
scope: evidence-support-check v0 pack containment and support channel pressure test
truth_boundary: sandbox check only; not reviewed knowledge; not action basis
action_basis_allowed: false
truth_mutation_allowed: false
---

# Evidence Support Check v0 Pack Containment Test

## Purpose

Verify that the checker distinguishes current-pack support from fixture-supplied
external support.

This prevents a quiet failure mode:

```text
the current context pack did not contain enough support
but the fixture pointed at another file that did
the checker accidentally treated that as if the current pack was covered
```

## Small Tool Change

Claims may now specify:

```text
required_support_channels
```

Supported channels used in this sandbox:

```text
context_pack_metadata
anchor_queue
explicit_fixture_ref
```

Rule:

```text
If required_support_channels is set, a claim is supported only when a preferred
source matches through one of those required channels.

If a match exists only outside the required channels, the claim becomes
weakly_supported with:

failure_origin=matched_outside_required_support_channel
```

Answer readiness now treats weak support as a blocker:

```text
weakly_supported > 0 => answer_readiness=not_ready
```

This is not a new truth rule. It is a context-pack coverage guard.

## Fixture

```text
fixtures/evidence-support-check-v0-pack-containment-source-intake.json
```

The fixture checks three claims:

```text
pc1: support is inside current e2e pack metadata
pc2: support exists, but only as explicit fixture ref outside current pack
pc3: support comes from SOURCE_INTAKE.md inside current anchor_queue
```

Expected result:

```text
supported=2
weakly_supported=1
missing_evidence=0
answer_readiness=not_ready
```

## Result

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-evidence-support-check-v0.ps1 `
  -Root . `
  -PackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\source-intake-routing-workbench-pack-query-e2e-action-generated.md `
  -ClaimSpecPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures\evidence-support-check-v0-pack-containment-source-intake.json `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\evidence-support-check-v0-pack-containment-generated.md `
  -AnswerReadyOutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-ready-context-pack-v0-pack-containment-generated.md `
  -Json
```

Result:

```json
{
  "anchor_queue_total": 21,
  "claims_checked": 3,
  "supported": 2,
  "weakly_supported": 1,
  "unsupported": 0,
  "missing_evidence": 0,
  "answer_readiness": "not_ready",
  "action_basis_allowed": false,
  "citation_faithfulness_checked": false
}
```

Generated outputs:

```text
checks/evidence-support-check-v0-pack-containment-generated.md
checks/answer-ready-context-pack-v0-pack-containment-generated.md
```

## Claim-Level Outcome

```text
pc1 supported
  required_support_channels: context_pack_metadata
  actual support_channel: context_pack_metadata

pc2 weakly_supported
  required_support_channels: context_pack_metadata, anchor_queue
  actual support_channel: explicit_fixture_ref
  failure_origin: matched_outside_required_support_channel

pc3 supported
  required_support_channels: anchor_queue, context_pack_metadata
  actual support_channels: anchor_queue, context_pack_metadata
```

## Outcome

The checker now exposes the difference between:

```text
pack-contained support
external supplement support
missing support
```

Weak support remains visible for human repair, but it does not make the answer
draft-ready.

Boundary remains unchanged:

```text
pack-contained support != action basis
explicit_fixture_ref != current pack coverage
weakly_supported != ready_for_answer_draft
support channel check != truth layer
```
