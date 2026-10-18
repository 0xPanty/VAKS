---
record_kind: opus_review_brief_candidate
status: candidate
created_at: 2026-06-07T18:45:00+08:00
topic_id: source-intake-routing
truth_boundary: review_brief_not_truth
action_basis_allowed: false
truth_mutation_allowed: false
---

# Opus Review Brief: Answer Draft Smoke v0

## What Changed

The source-intake-routing workbench now has a complete sandbox-only
answer-preparation loop:

```text
context pack
-> evidence support check
-> answer-ready context pack
-> answer draft skeleton
-> human-readable smoke draft
-> smoke lint
```

The new step is intentionally small. It checks whether a ready skeleton can be
turned into a readable answer draft while keeping each emitted answer line tied
to an existing `claim_refs` handle.

It does not prove semantic support. A valid `claim_refs` handle means the
referenced claim id exists in the skeleton; citation faithfulness and coverage
belong to evidence support, faithfulness, sufficiency, or human review layers.

## Main Review Files

```text
tools/vaks-answer-draft-smoke-lint-v0.ps1
checks/answer-draft-smoke-v0-pack-repair-generated.md
checks/answer-draft-smoke-v0-e2e-mixed-blocked-generated.md
checks/answer-draft-smoke-v0-pack-repair-lint-generated.md
checks/answer-draft-smoke-v0-e2e-mixed-blocked-lint-generated.md
checks/answer-draft-smoke-v0-empty-claim-refs-generated.md
checks/answer-draft-smoke-v0-empty-claim-refs-lint-generated.md
checks/answer-draft-smoke-v0-paragraph-blocked-generated.md
checks/answer-draft-smoke-v0-paragraph-blocked-lint-generated.md
checks/answer-draft-smoke-v0-fenced-heading-blocked-generated.md
checks/answer-draft-smoke-v0-fenced-heading-blocked-lint-generated.md
checks/answer-draft-smoke-v0-mismatched-ref-known-limitation-generated.md
checks/answer-draft-smoke-v0-mismatched-ref-known-limitation-lint-generated.md
checks/answer-draft-smoke-v0-omitted-claim-known-limitation-generated.md
checks/answer-draft-smoke-v0-omitted-claim-known-limitation-lint-generated.md
checks/answer-draft-smoke-v0-test.md
```

Important upstream context:

```text
checks/answer-draft-skeleton-v0-pack-repair-generated.md
checks/answer-draft-skeleton-v0-e2e-mixed-blocked-generated.md
checks/answer-draft-skeleton-v0-test.md
checks/evidence-support-check-v0-pack-repair-test.md
```

Real-local pressure and blind review packet:

```text
checks/real-local-answer-draft-smoke-pressure-test.md
23_REAL_LOCAL_PRESSURE_AND_BLIND_REVIEW_PACKET.md
23A_AUTHOR_RECORDED_RESULTS_AFTER_BLIND_RUN.md
24_BLIND_OPUS_REVIEW_ABSORPTION.md
```

## Expected Result

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

empty claim_refs adversary: expected fail / actual fail
paragraph blocked answer adversary: expected fail / actual fail
fenced heading blocked answer adversary: expected fail / actual fail
mismatched ref known limitation: expected pass / actual pass
omitted claim known limitation: expected pass / actual pass
```

## Boundary To Review

The intended boundary is:

```text
answer draft smoke = drafting aid only
claim_refs = trace handles, not proof of truth
claim_refs existence = not semantic support
answer-ready = not action basis
smoke lint = diagnostic, not reviewer approval
smoke lint assumes skeleton readiness was decided upstream
smoke lint does not perform coverage or omission review
```

Forbidden interpretations:

```text
not production RAG
not citation-faithfulness checked
not reviewed knowledge
not truth-layer mutation
not action execution
not mainline promotion
```

## Review Questions

```text
1. Does the smoke draft stay within skeleton claim ids at the reference-handle level?
2. Does the blocked path really emit no answer claim?
3. Are expected-pass known-limitation cases clearly labeled as semantic/coverage gaps outside smoke lint?
4. Are the boundary labels strong enough to prevent answer-ready from being read as action basis?
5. Is the added lint light enough for the workbench, or is it already overfitted?
```

## Current Test Summary

```text
smoke lint: 7 checked / 4 pass / 3 expected fail
known-limitation cases: 2 expected pass
evidence support regression: 8 checked / expected results preserved
real-local ready sample: 5 checked / 5 supported / smoke lint pass
real-local negative sample: 4 checked / 4 missing / blocked smoke lint pass
context-pack lint: 17 checked / 16 pass / 1 expected fail
json fixture parse: 12 checked / 12 pass
boundary scan: no actionable forbidden true flags outside fixtures/tools and expected-fail report
truth layer: no changes in SCHEMA / ARCHITECTURE / FUSION / claims / decisions / patterns
```

## Blind Review Follow-Up

The first zero-context blind review is accepted as useful precisely because it
found real issues. It does not promote the sandbox.

```text
procedural issue: original blind packet leaked author-recorded expected results
repair: 23 no longer contains result values before commands
after-run comparison: 23A
absorbed design limits: 24
status: sandbox_candidate_only
```

The main design limit remains:

```text
real-local support can be self-referential when it checks author-produced
sandbox docs; the next maturity step must use reviewed vault claims on a
non-self-referential question
```

## Bottom Line

The prototype is now a usable retrieval-to-answer-preparation workbench. It is
not production automation, but it can route a question, assemble a bounded pack,
check support, repair pack containment, build an answer skeleton, and produce a
claim-tagged human draft while refusing not-ready input.
