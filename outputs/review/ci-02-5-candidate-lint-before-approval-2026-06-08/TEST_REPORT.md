# CI-02.5 Candidate Lint Before Approval Sandbox Test Report

Date: 2026-06-08
Scope: sandbox only
Target: Candidate lint before approval

## What Was Tested

This sandbox copied the current architecture surface into:

```text
outputs/review/ci-02-5-candidate-lint-before-approval-2026-06-08/architecture/
```

The test added candidate-lint rules only to the sandbox copies of:

```text
architecture/REVIEW_QUEUE.md
architecture/templates/review-candidate.md
architecture/wiki/indexes/knowledge-graph-index.md
```

No root architecture file was changed for this candidate-lint pass.

## Candidate Lint Shape Tested

```yaml
candidate_lint:
  checked_at:
  checked_by:
  lint_status: pass | warnings | blocking
  schema_violations: []
  provenance_violations: []
  evidence_support_violations: []
  approval_integrity_violations: []
  body_integrity_violations: []
  action_boundary_violations: []
```

## Boundary

Candidate lint is approval-prep structure, not truth.

It does not create:

```text
evidence support
review approval
truth confidence
reviewed relation
action readiness
automatic promotion
```

Passing lint only means the candidate is structurally safe enough to review or
approve.

## Fixtures

```text
tests/fixtures/pass-fixed-review-candidate.md
tests/fixtures/block-missing-body-hash.md
tests/fixtures/block-background-context-support.md
tests/fixtures/block-action-basis-candidate.md
tests/fixtures/pass-ordinary-raw-capture.md
```

## First Run

Initial run:

```text
TOTAL=28 PASS=25 FAIL=3
```

False-positive causes:

```text
README uses numbered five-layer wording instead of one arrow line.
The llm-wiki source-basis regex expected a stricter order than the text used.
Copied historical architecture files contain existing trailing whitespace; this is outside the candidate-lint patch surface.
```

No architecture failure was found in that first run.

## Final Run

Final adjusted high-pressure run:

```text
TOTAL=28 PASS=28 FAIL=0
```

Covered checks:

```text
public five-layer story preserved
lint section placement after CI-02 compile/writeback gate
llm-wiki-compiler schemaViolations / provenanceViolations source basis preserved
candidate_lint minimal shape complete
critical blocking examples covered
lint is not evidence support / approval / truth / action readiness
ordinary raw capture remains light
template frontmatter and guidance updated
sandbox index marks this as sandbox candidate, not adopted mainline
CI-02 boundary remains narrow
pass fixture stays candidate-only
missing body_hash blocks approval
background_context-as-support blocks approval
candidate action-basis use blocks approval
ordinary raw capture does not require candidate_lint
local source-code anchor exists and supports candidate lint storage
changed sandbox files have no trailing whitespace
```

## Source Anchor

The key source-code anchor was checked against:

```text
raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip
llm-wiki-compiler-main/src/compiler/index.ts:594-617
```

The checked lines include candidate-time `schemaViolations`,
`provenanceViolations`, and `writeCandidate`.

## Recommendation

Positive, but keep it scoped.

Recommended mainline merge shape:

```text
REVIEW_QUEUE.md:
  add Candidate Lint Before Approval after Review-Gated Compile / Writeback Queue

templates/review-candidate.md:
  add candidate_lint frontmatter block and guidance section

wiki/indexes/knowledge-graph-index.md:
  record only after mainline merge, not as adopted before merge
```

Do not add scripts yet.
Do not make lint evidence support.
Do not require full lint for ordinary raw capture or ordinary outputs/qa.
