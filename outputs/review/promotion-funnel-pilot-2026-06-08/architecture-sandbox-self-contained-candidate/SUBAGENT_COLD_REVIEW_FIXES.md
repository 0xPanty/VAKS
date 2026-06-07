# Subagent Cold Review Fixes

## Cold Review Result

Independent no-context subagent result:

```text
PASS_WITH_FIXES
```

The subagent agreed the change is a supplement, not a replacement:

```text
candidate point
-> fixed candidate body + body_hash + approval facts
-> Evidence Packet / Evidence Sufficiency Gate
-> promotion
```

It found no conflict with the frozen architecture documents, but raised three
fixes before formal adoption.

## Fix 1: Misleading Promote-Ready Wording

Finding:

```text
The sample candidate had empty approval facts but still said
promotion_readiness: promote_ready.
```

Fix applied:

```text
support_state: supported
object_integrity_ready: true
approval_readiness: blocked_pending_approval
```

Meaning:

```text
The evidence support and object integrity can be ready, while final approval is
still blocked until the specific evidence and body hash are checked.
```

## Fix 2: Canonical Field Shape

Finding:

```text
REVIEW_QUEUE.md and the sample used top-level review-candidate fields, while the
template showed a nested self_contained_review_object block.
```

Fix applied:

```text
templates/review-candidate.md now uses top-level frontmatter fields:
  record_type: review-candidate
  candidate_id
  source_candidate_points
  proposed_title
  proposed_path
  candidate_body_location
  body_hash
  body_hash_algorithm
  evidence_packet_ref
  source_anchor_refs
  approval_integrity
```

The template section now says the canonical fields live in top-level frontmatter
and should not be duplicated as a second nested schema.

## Fix 3: Body Hash Canonicalization

Finding:

```text
body_hash existed, but the exact calculation rule was not specified.
```

Fix applied:

```text
body_hash_algorithm: sha256_utf8_lf_trim_body_without_heading
```

Canonical rule:

```text
Hash the content pointed to by candidate_body_location, excluding the heading,
normalizing CRLF to LF, trimming leading/trailing whitespace, encoded as UTF-8
SHA256.
```

## Re-Test After Fixes

```text
strong_positive_approval_ready_synthetic        PASS
positive_fixed_review_object_not_final_approval PASS
approval_missing_facts_expected_block           FAIL as expected
negative_checked_hash_differs                   FAIL as expected
negative_body_hash_mismatch                     FAIL as expected
negative_missing_hash_algorithm                 FAIL as expected
```

Frozen-copy checks remain unchanged:

```text
SCHEMA.md                         unchanged
ARCHITECTURE_PRINCIPLES.md        unchanged
FUSION_ARCHITECTURE_V0_2_DRAFT.md unchanged
SOURCE_INTAKE.md                  unchanged
REFERENCE_REVIEW_PROTOCOL.md      unchanged
```

## Updated Recommendation

After applying the cold-review fixes, this sandbox variant is stronger than the
first pass.

Recommended status:

```text
PASS_FOR_SANDBOX_ADOPTION_TEST
```

Formal mainline adoption still needs user approval and should remain a small
patch only:

```text
REVIEW_QUEUE.md
templates/review-candidate.md
wiki/patterns/self-contained-review-candidate-record.md
```

Do not patch:

```text
SCHEMA.md
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
```
