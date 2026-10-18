---
record_kind: sandbox_test_report
status: candidate
created_at: 2026-06-07T19:35:00+08:00
topic_id: source-intake-routing
truth_boundary: test_report_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
---

# Real Local Answer Draft Smoke Pressure Test

## Purpose

This test moves beyond the original hand-built `pr1/pr2/pr3` smoke examples.
It uses local sandbox/workbench files as real source material and asks two
real questions:

```text
1. What does answer draft smoke lint guarantee, and what does it not guarantee?
2. Can the answer draft smoke output be used as action basis?
```

The goal is still sandbox-only pressure testing. This is not mainline
promotion, schema adoption, reviewer approval, or action basis.

## Generated Context Packs

```text
checks/real-local-question-pack-smoke-boundary-generated.md
  query: What does answer draft smoke lint guarantee, and what does it explicitly not guarantee?
  router_mode: audit
  action_basis_allowed=false

checks/real-local-question-pack-action-basis-generated.md
  query: Can the answer draft smoke output be used as action basis?
  router_mode: action
  anchor_queue_total=29
  action_basis_allowed=false
```

One exploratory query also surfaced a router nuance:

```text
checks/real-local-question-pack-answer-draft-smoke-generated.md
  query: Can the source-intake-routing workbench safely produce a human-readable answer draft, and what boundaries still apply?
  router_mode: source-inspection
  note: useful as a source-inspection route, but not used as the final action-safety sample
```

## Real Local Ready Sample

Fixture:

```text
fixtures/evidence-support-check-v0-real-local-smoke-boundary.json
```

Support check:

```text
checks/evidence-support-check-v0-real-local-smoke-boundary-generated.md
checks/answer-ready-context-pack-v0-real-local-smoke-boundary-generated.md
```

Result:

```text
claims_checked=5
supported=5
weakly_supported=0
missing_evidence=0
answer_readiness=ready_for_answer_draft
action_basis_allowed=false
citation_faithfulness_checked=false
```

Skeleton and smoke draft:

```text
checks/answer-draft-skeleton-v0-real-local-smoke-boundary-generated.md
checks/answer-draft-smoke-v0-real-local-smoke-boundary-generated.md
checks/answer-draft-smoke-v0-real-local-smoke-boundary-lint-generated.md
```

Smoke lint result:

```text
status=pass
skeleton_state=ready_for_human_draft
draft_answer_emitted=true
skeleton_claim_ids=rl1,rl2,rl3,rl4,rl5
draft_claim_refs=rl1,rl2,rl3,rl4,rl5
draft_answer_lines=5
untagged_draft_lines=0
empty_claim_ref_tags=0
unknown_claim_refs=0
```

## Real Local Negative Sample

Fixture:

```text
fixtures/evidence-support-check-v0-real-local-action-basis-negative.json
```

The negative sample deliberately overclaims:

```text
answer draft smoke output can be action basis
smoke lint is reviewer approval
claim_refs prove semantic support
smoke lint performs coverage and omission review
```

Support check:

```text
checks/evidence-support-check-v0-real-local-action-basis-negative-generated.md
checks/answer-ready-context-pack-v0-real-local-action-basis-negative-generated.md
```

Result:

```text
claims_checked=4
supported=0
weakly_supported=0
missing_evidence=4
answer_readiness=not_ready
action_basis_allowed=false
citation_faithfulness_checked=false
```

Skeleton and blocked smoke draft:

```text
checks/answer-draft-skeleton-v0-real-local-action-basis-negative-blocked-generated.md
checks/answer-draft-smoke-v0-real-local-action-basis-negative-blocked-generated.md
checks/answer-draft-smoke-v0-real-local-action-basis-negative-blocked-lint-generated.md
```

Smoke lint result:

```text
status=pass
skeleton_state=blocked_not_ready
draft_answer_emitted=false
draft_answer_lines=0
draft_claim_refs=0
issues=[]
```

## Boundary Result

```text
real local ready sample can produce a claim-tagged human-readable draft
real local action-basis overclaim is blocked before draft text
claim_refs remain reference handles, not semantic support
smoke lint remains diagnostic, not reviewer approval
answer-ready remains answer_draft_only, not action basis
```

## Remaining Blind Review Status

This file records an author-run real-local pressure test. It is not a strict
blind non-author pass.

The separate review packet is:

```text
23_REAL_LOCAL_PRESSURE_AND_BLIND_REVIEW_PACKET.md
```

The original packet leaked author-recorded result values before the commands.
That made the first blind pass useful as a critique, but not procedurally clean
as a final blind pass.

Repair:

```text
23_REAL_LOCAL_PRESSURE_AND_BLIND_REVIEW_PACKET.md
  cold protocol and commands only

23A_AUTHOR_RECORDED_RESULTS_AFTER_BLIND_RUN.md
  author-recorded results for after-run comparison only

24_BLIND_OPUS_REVIEW_ABSORPTION.md
  blind-review findings and sandbox-only limitations
```
