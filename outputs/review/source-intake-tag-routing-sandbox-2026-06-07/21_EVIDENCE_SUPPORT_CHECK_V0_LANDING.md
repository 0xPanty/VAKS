---
record_kind: sandbox_design_landing_candidate
status: candidate_only
created_at: 2026-06-07
topic_id: source-intake-routing
scope: evidence-support-check v0 landing
truth_boundary: sandbox design / implementation note only; not reviewed knowledge; not action basis
action_basis_allowed: false
truth_mutation_allowed: false
---

# Evidence Support Check v0 Landing

## Plain Result

The previous reference distillation is now landed as a small sandbox extension:

```text
action context pack
-> anchor_queue
-> evidence-support-check fixture
-> claim-evidence map
-> answer-ready context pack candidate
```

This is not an automatic evaluator. The fixture names the claims and support
patterns explicitly, and the tool only scans local source anchors for those
patterns.

## Landed Pieces

```text
fixtures/evidence-support-check-v0-source-intake.json
tools/vaks-evidence-support-check-v0.ps1
checks/evidence-support-check-v0-source-intake-generated.md
checks/answer-ready-context-pack-v0-source-intake-generated.md
```

## Design Choices

```text
No LLM judge.
No score threshold.
No external API.
No vector database.
No action execution.
No truth mutation.
```

The tool keeps three things separate:

```text
anchor_queue:
  possible local anchors to inspect

evidence_support_check:
  claim -> source selector -> warrant -> support status

answer_ready_context_pack:
  answer-draft preparation only, still not action basis
```

## Why This Is The Small Landing

It improves the workbench without expanding the architecture:

```text
Before:
  final_support.state = none
  anchor_queue = navigation only
  evidence_support_check_not_run

After:
  answer claims are explicit
  source selectors are bound to each claim
  support status is visible
  final_support is checked only for answer_draft scope
```

## Boundary

```text
Supported in this sandbox means:
  source-span support was found by explicit local pattern check.

Supported does not mean:
  reviewed truth
  action basis
  causal citation faithfulness
  production RAG grounding
  automatic promotion
```

The next useful step is a slightly harder manual trial with one intentionally
unsupported or scope-mismatched claim, not a heavier evaluator.

## Test Result

Generated:

```text
checks/evidence-support-check-v0-source-intake-generated.md
checks/answer-ready-context-pack-v0-source-intake-generated.md
checks/evidence-support-check-v0-test.md
```

Result:

```text
anchor_queue_total=29
claims_checked=4
supported=4
missing_evidence=0
answer_readiness=ready_for_answer_draft
action_basis_allowed=false
citation_faithfulness_checked=false
```

Effect:

```text
before: anchor_queue only; final_support.state=none
after: claim-evidence map; final_support checked for answer_draft_only
```

Boundary:

```text
answer-ready still does not mean action basis.
support channels are exposed so explicit fixture refs do not masquerade as
anchor_queue evidence.
```

## Negative Pressure Test Result

The follow-up negative pressure test has landed:

```text
fixtures/evidence-support-check-v0-negative-source-intake.json
checks/evidence-support-check-v0-negative-generated.md
checks/answer-ready-context-pack-v0-negative-generated.md
checks/evidence-support-check-v0-negative-pressure-test.md
```

It deliberately checks unsupported and scope-mismatched overclaims:

```text
action-basis overclaim
navigation-as-support overclaim
production-evaluator scope overclaim
truth-layer promotion overclaim
```

The first run exposed a useful false positive: non-goal / negated text was
matched as positive support. The tool now skips excluded support context such
as `Supported does not mean`, `Non-Goals`, `must not become`, and forbidden-use
wording.

Final result:

```text
positive fixture: supported=4 missing_evidence=0 ready_for_answer_draft
negative fixture: supported=0 missing_evidence=4 not_ready
action_basis_allowed=false
citation_faithfulness_checked=false
```

## Mixed Pressure Test Result

The mixed pressure test has landed:

```text
fixtures/evidence-support-check-v0-mixed-source-intake.json
checks/evidence-support-check-v0-mixed-generated.md
checks/answer-ready-context-pack-v0-mixed-generated.md
checks/evidence-support-check-v0-mixed-pressure-test.md
```

It checks the more realistic case where one answer candidate contains both
supported and unsupported claims.

Result:

```text
positive fixture: supported=4 missing_evidence=0 ready_for_answer_draft
negative fixture: supported=0 missing_evidence=4 not_ready
mixed fixture: supported=2 missing_evidence=2 not_ready
```

The answer-ready pack now prints `failure_origin` per claim, so unsupported
claims can be distinguished as missing support or scope overclaim without
turning the check into a heavier evaluator.

## Revised Flip Test Result

The revised flip test has landed:

```text
fixtures/evidence-support-check-v0-revised-source-intake.json
checks/evidence-support-check-v0-revised-generated.md
checks/answer-ready-context-pack-v0-revised-generated.md
checks/evidence-support-check-v0-revised-flip-test.md
```

It verifies that a blocked mixed answer can become draft-ready after unsupported
or overclaimed parts are rewritten into supported boundary claims.

Result:

```text
mixed fixture: supported=2 missing_evidence=2 not_ready
revised fixture: supported=4 missing_evidence=0 ready_for_answer_draft
```

The revised claims use explicit field anchors such as
`citation_faithfulness_checked=false` and `action_basis_allowed=false`, keeping
the repair loop local and lightweight.

## E2E Repair Loop Result

The e2e repair loop test has landed:

```text
checks/source-intake-routing-workbench-pack-query-e2e-action-generated.md
fixtures/evidence-support-check-v0-e2e-mixed-source-intake.json
fixtures/evidence-support-check-v0-e2e-revised-source-intake.json
checks/evidence-support-check-v0-e2e-mixed-generated.md
checks/answer-ready-context-pack-v0-e2e-mixed-generated.md
checks/evidence-support-check-v0-e2e-revised-generated.md
checks/answer-ready-context-pack-v0-e2e-revised-generated.md
checks/evidence-support-check-v0-e2e-repair-loop-test.md
```

Result:

```text
natural question -> router: action / high confidence
action pack: anchor_queue_total=21, final_support.state=none
e2e mixed: supported=2 missing_evidence=2 not_ready
e2e revised: supported=4 missing_evidence=0 ready_for_answer_draft
```

The e2e-specific fixtures point their first claim at the newly generated
natural-question pack, and the generated checks confirm
`support_channel=context_pack_metadata`.

## Pack Containment Test Result

The pack containment pressure test has landed:

```text
fixtures/evidence-support-check-v0-pack-containment-source-intake.json
checks/evidence-support-check-v0-pack-containment-generated.md
checks/answer-ready-context-pack-v0-pack-containment-generated.md
checks/evidence-support-check-v0-pack-containment-test.md
```

Claims may now declare `required_support_channels`. If a match exists only
outside those channels, it becomes `weakly_supported` instead of silently
passing as current-pack support.

Result:

```text
pack containment: supported=2 weakly_supported=1 missing_evidence=0 not_ready
weak support reason: matched_outside_required_support_channel
```

This keeps external fixture refs visible as supplemental anchors while
preventing them from masquerading as pack-contained coverage.

## Pack Repair Test Result

The containment failure now has a repaired-pack pressure test:

```text
checks/source-intake-routing-workbench-pack-query-e2e-action-repaired-generated.md
fixtures/evidence-support-check-v0-pack-repair-source-intake.json
checks/evidence-support-check-v0-pack-repair-generated.md
checks/answer-ready-context-pack-v0-pack-repair-generated.md
checks/evidence-support-check-v0-pack-repair-test.md
```

Result:

```text
containment before: supported=2 weakly_supported=1 missing_evidence=0 not_ready
repair after: supported=3 weakly_supported=0 missing_evidence=0 ready_for_answer_draft
```

The key claim now supports through `anchor_queue` from
`19_SOURCE_INTAKE_ROUTING_WORKBENCH_HARDENING.md` line 219, so this is a pack
repair result rather than a relaxed fixture match.

Boundary remains unchanged:

```text
action_basis_allowed=false
truth_mutation_allowed=false
citation_faithfulness_checked=false
final_support.scope=answer_draft_only
```

## Answer Draft Skeleton Result

The answer-ready output now feeds a thin answer draft skeleton:

```text
tools/vaks-answer-draft-skeleton-v0.ps1
checks/answer-draft-skeleton-v0-pack-repair-generated.md
checks/answer-draft-skeleton-v0-e2e-mixed-blocked-generated.md
checks/answer-draft-skeleton-v0-test.md
```

Ready input result:

```text
draft_skeleton_state=ready_for_human_draft
claims_seen=3
draft_claims_emitted=3
source_refs_policy=claim_evidence_map_only
action_basis_allowed=false
```

Not-ready input result:

```text
draft_skeleton_state=blocked_not_ready
claims_seen=4
draft_claims_emitted=0
block_reasons=input_answer_readiness_not_ready_for_answer_draft,claim_evidence_map_contains_non_supported_claim
```

The skeleton is only a drafting handoff. It does not introduce claims outside
`claim_evidence_map`, and it does not convert answer readiness into action
basis.

## Answer Draft Smoke Result

The answer skeleton now has a human-readable smoke draft and lint check:

```text
tools/vaks-answer-draft-smoke-lint-v0.ps1
checks/answer-draft-smoke-v0-pack-repair-generated.md
checks/answer-draft-smoke-v0-e2e-mixed-blocked-generated.md
checks/answer-draft-smoke-v0-pack-repair-lint-generated.md
checks/answer-draft-smoke-v0-e2e-mixed-blocked-lint-generated.md
checks/answer-draft-smoke-v0-test.md
22_ANSWER_DRAFT_SMOKE_V0_OPUS_REVIEW_BRIEF.md
```

Result:

```text
ready smoke lint: pass
  draft_answer_emitted=true
  draft_answer_lines=3
  claim_refs=pr1,pr2,pr3
  unknown_claim_refs=0
  untagged_draft_lines=0

blocked smoke lint: pass
  draft_answer_emitted=false
  draft_answer_lines=0
  claim_refs=0

empty claim_refs: expected fail / actual fail
paragraph blocked answer: expected fail / actual fail
fenced heading blocked answer: expected fail / actual fail
mismatched ref: expected pass known limitation
omitted claim: expected pass known limitation
```

The smoke draft is still only answer preparation. Claim tags are trace handles,
not truth proof, and this output remains outside action basis.

Smoke lint assumes skeleton readiness was decided upstream. It checks shape
compliance and reference-handle existence only; semantic support, citation
faithfulness, coverage, and omissions remain outside this layer.

## Real Local Pressure Result

The same chain was then run against local sandbox material rather than only
synthetic claim fixtures:

```text
checks/real-local-question-pack-smoke-boundary-generated.md
checks/real-local-question-pack-action-basis-generated.md
fixtures/evidence-support-check-v0-real-local-smoke-boundary.json
fixtures/evidence-support-check-v0-real-local-action-basis-negative.json
checks/real-local-answer-draft-smoke-pressure-test.md
23_REAL_LOCAL_PRESSURE_AND_BLIND_REVIEW_PACKET.md
```

Result:

```text
real-local ready sample:
  claims_checked=5
  supported=5
  missing_evidence=0
  answer_readiness=ready_for_answer_draft
  smoke_lint=pass
  draft_answer_lines=5

real-local negative sample:
  claims_checked=4
  supported=0
  missing_evidence=4
  answer_readiness=not_ready
  smoke_lint=pass
  draft_answer_lines=0
```

This strengthens the sandbox confidence from fixture-only confirmation to a
small local-sample pressure test. It still does not create blind approval,
reviewed knowledge, action basis, or truth-layer readiness.
