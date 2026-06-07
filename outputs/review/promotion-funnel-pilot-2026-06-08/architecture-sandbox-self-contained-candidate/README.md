# Architecture Sandbox: Self-Contained Review Candidate Record

## Purpose

Test what happens if CI-01, "Self-Contained Review Candidate Record", is added
to the current architecture as a sandbox-only variant.

This is not formal promotion and does not edit mainline architecture files.

For the adversarial / negative-case test pass, see:

```text
STRONG_TEST_REPORT.md
```

For the second-pass strong-positive and quality review, see:

```text
SECOND_PASS_REVIEW.md
```

For the no-context subagent cold review and applied fixes, see:

```text
SUBAGENT_COLD_REVIEW_FIXES.md
```

For the real candidate sample test, see:

```text
REAL_SAMPLE_TEST_REPORT.md
```

## Layout

```text
baseline/
  copied current architecture files

variant/
  same copied files, plus sandbox changes for CI-01
```

Copied architecture surface:

- `AGENTS.md`
- `README.md`
- `ARCHITECTURE_PRINCIPLES.md`
- `SCHEMA.md`
- `FUSION_ARCHITECTURE_V0_2_DRAFT.md`
- `SECOND_BRAIN_MODEL.md`
- `IMPLEMENTATION_BLUEPRINT.md`
- `SOURCE_INTAKE.md`
- `REFERENCE_REVIEW_PROTOCOL.md`
- `REVIEW_QUEUE.md`
- `MEMORY_TIER.md`
- `DEV_CONTEXT.md`
- `FEEDBACK.md`
- `wiki/indexes/knowledge-graph-index.md`
- `templates/review-candidate.md`
- `templates/candidate-distillation.md`
- `templates/source-record.md`
- `templates/library-review.md`
- `wiki/patterns/self-contained-review-candidate-record.md`

## Variant Changes

The variant changes only the promotion/review surface:

1. `variant/REVIEW_QUEUE.md`
   - Adds `self-contained review candidate record` between candidate point and promotion.
   - Adds section `3.2.1 Self-Contained Review Candidate Record`.
   - Adds a Step 7 promotion precondition: fixed candidate body + body hash before reviewer approval.

2. `variant/templates/review-candidate.md`
   - Adds a `Self-Contained Review Object` block.
   - Makes clear this block is only for promotion/formal writeback/strong relation/action basis/reviewer audit.
   - Keeps Evidence Packet as the actual support check.

3. `variant/wiki/patterns/self-contained-review-candidate-record.md`
   - Tests what the pattern would look like as adopted in the sandbox copy.
   - States that it is a promotion object-integrity gate, not a new truth layer.

4. `variant/outputs/review/candidates/CI-01-self-contained-review-candidate-record.candidate.md`
   - Adds a concrete sample candidate record with fixed candidate body, source anchors, scope limits, and body hash.

## Tests

Frozen-copy hash check:

```text
SCHEMA.md                         PASS
ARCHITECTURE_PRINCIPLES.md        PASS
FUSION_ARCHITECTURE_V0_2_DRAFT.md PASS
SOURCE_INTAKE.md                  PASS
REFERENCE_REVIEW_PROTOCOL.md      PASS
```

Expected variant diff:

```text
REVIEW_QUEUE.md
templates/review-candidate.md
wiki/patterns/self-contained-review-candidate-record.md
outputs/review/candidates/CI-01-self-contained-review-candidate-record.candidate.md
```

Candidate body hash check:

```text
declared: sha256:b9db816ba66069965395acfb9718a14d45097f647bcd5d1134a5b9f8596ce10b
actual:   sha256:b9db816ba66069965395acfb9718a14d45097f647bcd5d1134a5b9f8596ce10b
result:   PASS
```

Hash rule:

```text
sha256_utf8_lf_trim_body_without_heading
```

Boundary checks:

```text
ordinary light capture: not required
Evidence Packet: still required for support
body_hash: object integrity only, not truth confidence
approval: process evidence only, not evidence support
automatic promotion: explicitly forbidden
SCHEMA / FUSION / ARCHITECTURE_PRINCIPLES: unchanged in sandbox variant
```

## Result

CI-01 lands cleanly as a supplement, not a logic replacement.

The best landing shape is:

```text
candidate point
-> self-contained review candidate record
-> Evidence Packet / Evidence Sufficiency Gate
-> reviewer approval of exact body
-> formal writeback / archive receipt
```

This makes the review object stable. It does not add a new lane, truth layer,
schema family, runtime, or automation.

## Remaining Questions

1. Should the real mainline update only `REVIEW_QUEUE.md`, `templates/review-candidate.md`, and the existing pattern note?
2. Should `body_hash` be manual at first, or should a later helper calculate it?
3. Should approved candidates archive under `outputs/review/archived/` or a promotion-specific receipt folder?
