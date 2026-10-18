---
record_kind: sandbox_test_report
status: candidate
created_at: 2026-06-07T18:45:00+08:00
topic_id: source-intake-routing
truth_boundary: test_report_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
---

# Answer Draft Smoke v0 Test

## Purpose

This test checks whether an answer draft skeleton can become a human-readable
answer draft without adding unsupported claims or turning answer readiness into
action basis.

The rule is simple:

```text
every emitted answer claim must carry [claim_refs: ...]
each claim_ref must exist in the source skeleton
blocked skeletons must emit no answer claim
```

Trust boundaries:

```text
smoke lint assumes the skeleton readiness label is correct
readiness correctness belongs to the upstream evidence support check
smoke lint checks shape compliance and reference-handle existence
it does not check semantic support, citation faithfulness, coverage, or omissions
```

## Ready Draft Smoke

Input:

```text
checks/answer-draft-skeleton-v0-pack-repair-generated.md
```

Draft:

```text
checks/answer-draft-smoke-v0-pack-repair-generated.md
```

Lint:

```text
checks/answer-draft-smoke-v0-pack-repair-lint-generated.md
```

Result:

```text
status=pass
skeleton_state=ready_for_human_draft
draft_answer_emitted=true
skeleton_claim_ids=pr1,pr2,pr3
draft_claim_refs=pr1,pr2,pr3
draft_answer_lines=3
draft_answer_bullets=3
untagged_draft_lines=0
empty_claim_ref_tags=0
unknown_claim_refs=0
```

## Blocked Draft Smoke

Input:

```text
checks/answer-draft-skeleton-v0-e2e-mixed-blocked-generated.md
```

Draft:

```text
checks/answer-draft-smoke-v0-e2e-mixed-blocked-generated.md
```

Lint:

```text
checks/answer-draft-smoke-v0-e2e-mixed-blocked-lint-generated.md
```

Result:

```text
status=pass
skeleton_state=blocked_not_ready
draft_answer_emitted=false
draft_claim_refs=0
draft_answer_lines=0
draft_answer_bullets=0
untagged_draft_lines=0
empty_claim_ref_tags=0
unknown_claim_refs=0
```

## Adversarial Shape Cases

```text
empty [claim_refs:]:
  expected=fail
  actual=fail
  issue=ready_draft_has_empty_claim_refs
  reason=shape problem, lint can and should catch it

paragraph-style blocked answer:
  expected=fail
  actual=fail
  issue=blocked_draft_has_answer_text
  reason=shape problem, blocked skeleton emitted substantive Draft Answer text

fenced heading then blocked answer:
  expected=fail
  actual=fail
  issue=blocked_draft_has_answer_text
  reason=regression guard, headings inside fenced blocks must not end scanning
```

## Known-Limitation Cases

These are expected-pass cases. They document the smoke lint boundary instead of
pretending this layer can solve semantic or coverage problems.

```text
valid but mismatched ref:
  expected=pass
  actual=pass
  reason=claim_ref exists and the line is structurally tagged
  known_limitation=semantic support / citation faithfulness is not checked here

omitted claim / picked subset:
  expected=pass
  actual=pass
  reason=smoke lint does not require full skeleton claim coverage
  known_limitation=coverage / omission review belongs to another layer
```

## Real Local Pressure Cases

These cases use local sandbox files instead of only synthetic `pr1/pr2/pr3`
fixtures:

```text
real-local smoke boundary ready sample:
  expected=pass
  actual=pass
  evidence_support=5 checked / 5 supported / 0 missing
  answer_readiness=ready_for_answer_draft
  smoke_lint=5 draft lines / 0 unknown refs

real-local action-basis negative sample:
  expected=blocked
  actual=blocked
  evidence_support=4 checked / 0 supported / 4 missing
  answer_readiness=not_ready
  smoke_lint=0 draft lines emitted from blocked skeleton
```

## Boundary Result

```text
action_basis_allowed=false
truth_mutation_allowed=false
source_refs_policy=claim_evidence_map_only
no actionable forbidden true flags outside fixtures/tools and expected-fail report
ready draft is human-readable but still answer-draft-only
blocked draft emits no unsupported answer sentence
known limitation: valid claim_refs do not prove semantic support
known limitation: smoke lint does not perform coverage or omission checks
```

## Practical Result

The workbench now has a complete candidate-only answer-preparation chain:

```text
context pack
-> evidence support check
-> answer-ready pack
-> answer draft skeleton
-> human-readable smoke draft
-> smoke lint
```

This is the end of the useful sandbox loop for now. It is ready for Opus review
as a workbench prototype, not as production RAG or action execution.

## Final Regression

```text
smoke lint: 7 checked / 4 pass / 3 expected fail
known-limitation cases: 2 expected pass
evidence support regression: 8 checked / expected results preserved
real-local ready sample: 5 checked / 5 supported / smoke lint pass
real-local negative sample: 4 checked / 4 missing / blocked smoke lint pass
context-pack lint: 17 checked / 16 pass / 1 expected fail
json fixture parse: 12 checked / 12 pass
boundary scan: no actionable forbidden true flags outside fixtures/tools and expected-fail report
truth-layer status check: no changes in SCHEMA / ARCHITECTURE / FUSION / claims / decisions / patterns
process check: no lingering powershell process for this sandbox
```
