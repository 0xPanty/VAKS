# Pro Upload Context

## Human Summary

This upload is for the VAKS Source Intake generic read-only sandbox closeout.

The work is not a new architecture design pass. It is a sandbox validation lane
for the retrieval-to-pack-to-answer/use boundary. Candidate distillations,
project overlays, retrieval rank, graph, score, and diagnostic metadata must not
become final evidence support. Raw source cards can support read-only answers
only through resolved raw/stable anchors.

The local evidence lane has reached the judge-dispatch stage. The remaining
real-world step is to send Judge A and Judge B their separate packets, collect
their filled CSVs, then run merge/arbitration.

## Upload Contents

```text
source-intake-generic-readonly-loop-pro-review-package.zip
SHA256: 3b7fd00264bcd367a2b7245f20c3bf89b3e0de7e6e95611ab6b4b09d8342763e

semantic-support-judge-followup-kit.zip
SHA256: b8a4421bccb3d3c0faa669748bd86d88c92507f04d0b0a2be9e61d61b3dfa335

semantic-support-judge-ready-to-send.zip
SHA256: ef474daf79d1d24f96eda364bc7912566d1580a36d5ceaa169666ce5a1624de7
```

The ready-to-send zip is for the operator, not for a judge directly. Judge A and
Judge B must receive only their separated sub-packets.

## Current Status

- Generic read-only sandbox evidence: can keep.
- QueryPolicy / authority-bucket receipt: sandbox-level evidence only.
- Judge followup kit: ready for real Judge A/B dispatch after this upload is checked.
- Judge-facing G3-19 claim is now explicit and content-only, not a hidden case reference.
- Judges must not receive the full Pro review package.
- External semantic support completed: no, because real Judge A/B returns are not filled yet.
- Source Intake P0 passed: no.
- Production runtime validated: no.
- Vector/graph/hybrid retrieval validated: no.
- Live LLM/tool runtime validated: no.

## What Pro Should Check

Please do not reopen the whole architecture unless a packaged hard blocker is found.

1. Are the included artifact hashes correct?
2. Does judge-row-011 now have a concrete, judge-visible semantic support claim?
3. Is it clear that judges must not request or receive the full Pro review package?
4. Is it clear that `semantic-support-judge-ready-to-send.zip` must not be sent directly to a judge as a combined A/B packet?
5. Are there any hard blockers that would prevent sending the separated Judge A and Judge B packets now?

## Non-Goals

This upload does not prove Source Intake P0 passed, reviewed truth promotion,
action readiness, production runtime readiness, vector/graph/hybrid retrieval
correctness, or external semantic support completion.
