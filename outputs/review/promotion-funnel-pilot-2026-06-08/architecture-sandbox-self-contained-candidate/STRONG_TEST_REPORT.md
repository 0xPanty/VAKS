# Strong Test Report: Self-Contained Review Candidate Record

## Plain Result

Strong test result: pass, with one expected block.

Second-pass strong-positive result: pass.

CI-01 works as a promotion-quality supplement. It improves review/writeback
alignment without replacing the architecture logic.

It is not approval-ready by itself because sandbox approval facts are still
empty. That is the desired behavior: the gate blocks final writeback until a
human checks the specific evidence and approved body hash.

## What Was Tested

The strong test asked whether the new candidate object can:

1. Preserve the exact body proposed for writeback.
2. Detect body changes after review.
3. Reject source-summary-only proof.
4. Keep Evidence Packet as the support check.
5. Stay out of ordinary light capture.
6. Avoid changing frozen architecture documents.
7. Block approval/writeback when approval-integrity facts are missing.
8. Pass a synthetic approval-ready positive case when approval facts and checked
   body hash are present.

## Test Cases

| Case | Expected | Result | Meaning |
| --- | --- | --- | --- |
| positive_fixed_review_object | pass | pass | The CI-01 sample has fixed body, hash, source anchors, scope limits, and evidence packet ref. |
| approval_ready_gate_expected_fail | fail | fail | Correctly blocks final approval because no human approval, checked evidence, or checked hash exists. |
| negative_body_hash_mismatch | fail | fail | Body/hash mismatch is caught. |
| negative_missing_candidate_body | fail | fail | Candidate without fixed body section is not a promotion object. |
| negative_source_summary_only_anchor | fail | fail | Source summary alone cannot count as independent support. |
| negative_not_fixed_for_review | fail | fail | Draft candidate cannot pass as fixed promotion object. |
| negative_body_changed_after_review | fail | fail | Body mutation after hash is caught. |
| strong_positive_approval_ready_synthetic | pass | pass | If human approval facts and checked body hash are present, the gate can pass. |
| negative_checked_hash_differs | fail | fail | Approval hash must match the fixed candidate body hash. |

## Code Quality Finding

Second-pass review found one sandbox quality issue:

```text
candidate_body in YAML/frontmatter examples can become parser-hostile if the
body is long Markdown.
```

Sandbox fix:

```text
Use candidate_body_location plus body_hash in metadata.
Keep the actual body in a Markdown section such as "## Candidate Body".
```

This keeps the object stable without making frontmatter carry long Markdown.

## Boundary Regression

Changed in variant:

```text
REVIEW_QUEUE.md
templates/review-candidate.md
wiki/patterns/self-contained-review-candidate-record.md
```

Added in variant:

```text
outputs/review/candidates/CI-01-self-contained-review-candidate-record.candidate.md
```

Frozen-copy checks:

```text
SCHEMA.md                         unchanged
ARCHITECTURE_PRINCIPLES.md        unchanged
FUSION_ARCHITECTURE_V0_2_DRAFT.md unchanged
```

No `self-contained review candidate` concept was inserted into the frozen docs.

## Improvement

Before CI-01:

```text
candidate point
-> Evidence Packet
-> promotion discussion
```

Weakness:

```text
The review target could drift.
The approved summary and final writeback body could differ.
Approval facts were not tied to an exact body hash.
Source summaries could be mistaken for support unless checked carefully.
```

After CI-01:

```text
candidate point
-> fixed candidate body + body_hash
-> independent source_anchor_refs
-> Evidence Packet / Evidence Sufficiency Gate
-> approval_integrity on exact body
-> writeback / archive receipt
```

Improvement:

```text
review/writeback drift is blocked
body changes force re-review
source-summary-only proof is blocked
approval is tied to the exact reviewed body
light capture remains light
Evidence Packet remains the support check
```

## What It Does Not Improve

```text
It does not prove the candidate true.
It does not create reviewer approval.
It does not replace source anchors.
It does not replace Evidence Packet.
It does not make action basis ready.
It does not automate promotion.
It does not decide where approved candidates should be archived.
```

## Adoption Shape

Recommended mainline shape, if adopted later:

```text
REVIEW_QUEUE.md:
  add a small 3.2.1 object-integrity rule
  add a Step 7 precondition for fixed candidate body + body_hash

templates/review-candidate.md:
  use top-level review-candidate frontmatter fields for the Self-Contained Review Object

wiki/patterns/self-contained-review-candidate-record.md:
  promote/update the existing note, scoped as object-integrity pattern
```

Do not change `SCHEMA.md`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md`, or
`ARCHITECTURE_PRINCIPLES.md` for this adoption.

## Remaining Risk

The main risk is operational friction. If applied to every capture, it will make
intake too heavy. The sandbox variant avoids that by limiting it to promotion,
formal writeback, strong reviewed relations, action basis, or reviewer-requested
audit.

The second risk is manual hash handling. A future helper may be useful, but the
architecture does not need that helper before adoption.
