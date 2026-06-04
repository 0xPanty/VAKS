---
record_type: lightweight-path-comparison
status: draft
created: 2026-06-01
scope: sandbox-only
main_vault_write: false
schema_change: false
final_conclusion: false
---

# Lightweight Path Comparison

## What Was Tested

Same trial material as the original E2E run:

```text
ALCE
Attributed QA
GopherCite
FRONT
```

Instead of changing the architecture, this variant tested three compressed paths:

```text
small claim -> mini review
support/refine collision -> collision summary
scope-fit feedback -> feedback stub
```

No SCHEMA change, no main-vault write, no runtime, no scripts.

## Result Table

| Pain from original trial | Lightweight variant | Improved? | Notes |
|---|---|---|---|
| Evidence Packet too heavy for one small claim | `mini-review-alce-citation-quality.md` | yes | Keeps point, anchor, support check, scope limit, risk note, promotion result. Drops full packet fields. |
| Repeating Evidence Packet for 4-source convergence | `support-refine-collision-citation-support.md` | yes | Better matches support/refine collision. Does not force dramatic contradiction framing. |
| Feedback-event frontmatter too long for scope-fit correction | `scope-fit-feedback-stub-q1.md` | yes | Keeps activation guidance and truth boundary. Drops numeric deltas and decision_outcome. |
| `processing_level` vs `source_access` confusion | Not directly fixed | partial | Mini review makes source access visible near support check, but Source record ambiguity remains. |
| source independence unclear | Not fixed | no | Variant still records same research family as remaining gap. Independence remains a real review issue. |
| coverage_map too large for real question | Not retested as mini context pack | unknown | This variant focused on the three Opus targets, not a compact coverage_map. |
| local rule plus external support label missing | Not fixed | no | Still needs wording if future packs combine local architecture rule and outside evidence. |
| no runtime for activation change | Not fixed | no | Feedback stub is easier, but activation change is still manually recorded. |

## Concrete Before / After

### Small Claim

Original:

```text
candidate review + full Evidence Packet + omission_check + strongest_rebuttal + minimal_revision_needed
```

Variant:

```text
point
source_anchor
support_check
scope_limit
risk_note
promotion_result
```

Effect:

```text
The same support boundary is preserved with much less ceremony.
```

Risk:

```text
If used for action basis, this would be too thin. Escalation rule is required.
```

### Support / Refine Collision

Original:

```text
full point collision + Evidence Packet + review queue item + promoted claim
```

Variant:

```text
cluster_point
source contribution table
shared_scope
remaining_gap
resolution
escalation_decision
```

Effect:

```text
This fits the first real collision better because the sources converged rather than contradicted each other.
```

Risk:

```text
It does not solve source independence. It must preserve "same research family" as a gap.
```

### Scope-Fit Feedback

Original:

```text
full feedback-event with signal_strength, signal_confidence, deltas, decision_outcome
```

Variant:

```text
feedback
target
problem
next_time_activate
next_time_avoid
truth_boundary
```

Effect:

```text
This is much closer to what a human would actually write after a small answer-framing issue.
```

Risk:

```text
No numeric deltas means less machine-like data. But the original numbers were fake precision anyway.
```

## New Risk Introduced By Lightweight Path

The main new risk is under-documenting why escalation was not needed.

Mitigation:

```text
Every lightweight record needs one explicit escalation rule:
  when this becomes action basis / contested / high-impact / strong relation,
  switch to full Evidence Packet or full feedback event.
```

## Verdict For This Sandbox Trial

Opus's suggestion improved the targeted friction.

The lightweight path did not fix every pain:

```text
source independence
processing_level vs source_access
coverage status for local-rule-plus-external-support
manual-only activation change
```

But it clearly reduced friction for:

```text
small reviewed claim
support/refine collision
scope-fit feedback
```

This supports continuing the idea in sandbox as a small "review lite" operating convention, not as a schema change.

## Do Not Land Automatically

Do not modify main vault from this comparison alone.

If the user and Opus decide to land anything later, the smallest candidate would be wording-level guidance, not SCHEMA:

```text
small claim mini review
support/refine collision summary
scope-fit feedback stub
explicit escalation rule
```

