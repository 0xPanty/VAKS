---
record_kind: sandbox_pressure_test
status: pass
created_at: 2026-06-07
topic_id: source-intake-routing
scope: natural-question router to pack to evidence-support repair loop
truth_boundary: sandbox check only; not reviewed knowledge; not action basis
action_basis_allowed: false
truth_mutation_allowed: false
---

# Evidence Support Check v0 E2E Repair Loop Test

## Purpose

Verify the whole workbench chain on a natural-language question:

```text
natural question
-> query-intent-router
-> context pack builder
-> action anchor_queue
-> evidence-support-check
-> mixed answer blocked
-> revised answer draft-ready
```

This is not a production RAG test and not an answer generator. It checks whether
the sandbox workbench flow behaves coherently end to end.

## Natural Question

```text
Can we draft the revised source-intake-routing answer after evidence support
check, and is it safe to use as action basis?
```

## Router Result

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-query-intent-router-v0.ps1 `
  -Query 'Can we draft the revised source-intake-routing answer after evidence support check, and is it safe to use as action basis?' `
  -Json
```

Result:

```text
selected_mode=action
confidence=high
score=24
fallback_used=false
matched_terms=action, basis, support, safe to, evidence, source-intake-routing
warnings=action_mode_requires_evidence_support_check, candidate_overlay_audit_not_action_basis
action_basis_allowed=false
```

## Pack Builder Result

The first builder attempt used `Limit 260` and timed out after 30 seconds with
no output file. The timed-out PowerShell process was identified by command line
and stopped before rerun.

The successful rerun used `Limit 160`:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-context-pack-builder-v0.ps1 `
  -Root . `
  -Query 'Can we draft the revised source-intake-routing answer after evidence support check, and is it safe to use as action basis?' `
  -TopicId source-intake-routing `
  -Limit 160 `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\source-intake-routing-workbench-pack-query-e2e-action-generated.md `
  -Json
```

Result:

```text
mode=action
query_intent_selected_mode=action
anchor_queue_total=21
mainline_current=13
reviewed_support=8
raw_drilldown=0
candidate_orientation=0
active_project_overlay=0
action_basis_allowed=false
final_support.state=none
answer_readiness.state=not_ready
required_next_step=open raw/reviewed anchors and run evidence support check before action-facing use
```

Generated pack:

```text
checks/source-intake-routing-workbench-pack-query-e2e-action-generated.md
```

## Fixture Tightening

A first pass using the generic mixed/revised fixtures passed, but it was not
strict enough for an e2e claim: the first claim still preferred the older
query-action pack.

Fix:

```text
fixtures/evidence-support-check-v0-e2e-mixed-source-intake.json
fixtures/evidence-support-check-v0-e2e-revised-source-intake.json
```

These e2e fixtures make the first claim prefer the newly generated natural
question pack:

```text
checks/source-intake-routing-workbench-pack-query-e2e-action-generated.md
```

The final generated support maps confirm `support_channel=context_pack_metadata`
for that first claim.

## E2E Mixed Result

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-evidence-support-check-v0.ps1 `
  -Root . `
  -PackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\source-intake-routing-workbench-pack-query-e2e-action-generated.md `
  -ClaimSpecPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures\evidence-support-check-v0-e2e-mixed-source-intake.json `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\evidence-support-check-v0-e2e-mixed-generated.md `
  -AnswerReadyOutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-ready-context-pack-v0-e2e-mixed-generated.md `
  -Json
```

Result:

```json
{
  "anchor_queue_total": 21,
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

Claim-level check:

```text
em1 supported
  source_ref: checks/source-intake-routing-workbench-pack-query-e2e-action-generated.md
  selector: line:485
  support_channel: context_pack_metadata

em2 supported
  support_channel: explicit_fixture_ref

em3 missing_evidence
  failure_origin: missing_evidence_or_unavailable_support

em4 missing_evidence
  failure_origin: scope_mismatch_or_overclaim
```

## E2E Revised Result

Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\tools\vaks-evidence-support-check-v0.ps1 `
  -Root . `
  -PackPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\source-intake-routing-workbench-pack-query-e2e-action-generated.md `
  -ClaimSpecPath .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\fixtures\evidence-support-check-v0-e2e-revised-source-intake.json `
  -OutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\evidence-support-check-v0-e2e-revised-generated.md `
  -AnswerReadyOutFile .\outputs\review\source-intake-tag-routing-sandbox-2026-06-07\checks\answer-ready-context-pack-v0-e2e-revised-generated.md `
  -Json
```

Result:

```json
{
  "anchor_queue_total": 21,
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

Claim-level check:

```text
er1 supported
  source_ref: checks/source-intake-routing-workbench-pack-query-e2e-action-generated.md
  selector: line:485
  support_channel: context_pack_metadata

er2 supported
  support_channel: explicit_fixture_ref

er3 supported
  matched field: citation_faithfulness_checked=false

er4 supported
  matched field: action_basis_allowed=false
```

## Outcome

The end-to-end repair loop works:

```text
natural question routes to action
action pack remains anchor_queue only
mixed answer is blocked as not_ready
revised answer flips to ready_for_answer_draft
action_basis_allowed stays false throughout
citation_faithfulness_checked stays false throughout
```

This confirms the workbench can guide an answer-draft repair loop without
pretending to be action-ready, truth-ready, or citation-faithfulness complete.
