# VAKS Audit Shell Output-Level Oracle Alpha Bakeoff

Status: sandbox-only. No main-vault writeback, no SCHEMA change, no truth-core change.

## Verdict

The strongest positive result is `guarded_combined`: trigger-held deep packet retention + sparse provenance mention pointer + folded recurrence card + versioned fingerprint grouping, with categorical feedback wording as a supporting constraint.

No structural alpha should be adopted alone. The safest standalone item is `categorical_feedback_revision_strip`, but it has narrow impact. The strongest core alpha is `trigger_held_deep_packet_retention`, because it protects the hard boundary: ordinary stays light, serious triggers become thick. It still needs the feedback/authority boundary strip to be safe across the whole framework.

## Full Pressure Table

This table runs every variant against the entire pressure set. A single-purpose alpha can fail here if it lacks another required boundary.

| variant | safety | score | false-lite | state mismatch | authority leakage | authority boundary fail | jumpback fail | severe over-group | front reduction | grouping recall | grouped reduction | burden units |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| guarded_combined | True | 89.99 | 0 | 0 | 0 | 0 | 0 | 0 | 56.3 | 1.0 | 50.0 | 686 |
| categorical_feedback_revision_strip | True | 77.12 | 0 | 0 | 0 | 0 | 0 | 0 | 59.5 | 0.0 | 0.0 | 684 |
| baseline_full_audit | False | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 58.3 | 0.0 | 0.0 | 838 |
| control_previous_patch_like | False | 0 | 15 | 21 | 13 | 13 | 0 | 0 | 61.2 | 0.0 | 0.0 | 578 |
| trigger_held_deep_packet_retention | False | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 58.3 | 0.0 | 0.0 | 698 |
| sparse_provenance_mention_pointer | False | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 58.3 | 0.0 | 0.0 | 655 |
| folded_recurrence_card | False | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 58.3 | 1.0 | 50.0 | 705 |
| versioned_fingerprint_grouping | False | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 58.3 | 1.0 | 50.0 | 705 |

## Relevant Slice Table

This table asks a narrower question: when an alpha is tested against the cases it is meant to solve, does it behave positively?

| alpha | slice cases | slice safety | slice hard failures | slice front reduction | full-set caveat |
| --- | ---: | --- | ---: | ---: | --- |
| trigger_held_deep_packet_retention | 8 | True | 0 | 58.3 | needs companion boundaries for full framework |
| sparse_provenance_mention_pointer | 14 | True | 0 | 58.3 | needs companion boundaries for full framework |
| folded_recurrence_card | 12 | True | 0 | 52.8 | needs companion boundaries for full framework |
| versioned_fingerprint_grouping | 5 | True | 0 | 58.3 | needs companion boundaries for full framework |
| categorical_feedback_revision_strip | 18 | True | 0 | 58.3 | safe as standalone wording constraint |
| guarded_combined | 49 | True | 0 | 56.3 | candidate stack for framework sandbox |

## Alpha Judgment

### Strong Positive Stack

- `guarded_combined` is the strongest result. It passes the output-level hard gates while keeping a substantial front-face reduction.
- This means the reasonable alpha is not one isolated trick; it is a guarded shell stack.

### Strong Positive Components

- `trigger_held_deep_packet_retention`: core engine. It should be carried forward as the main alpha, but not alone.
- `sparse_provenance_mention_pointer`: strong companion. It reduces repeated provenance text while preserving resolvable anchor pointers.
- `folded_recurrence_card`: strong but only under a hard break-fold rule. It reduces recurrence noise, but serious, missing-anchor, or regressed members must escape the fold.
- `versioned_fingerprint_grouping`: strong for long-term maintainability. It prevents new grouping rules from rewriting old grouping history.

### Supporting Constraint

- `categorical_feedback_revision_strip`: useful, but better treated as wording discipline inside the shell rather than the main alpha by itself.

## Why The Control Fails

The `control_previous_patch_like` variant is intentionally close to the old weakness. It fails output-level checks because state is not upgraded from ordinary-looking surfaces and authority traps can leak into rendered text.

## What This Proves

This proves the output-level oracle can catch the exact overclaim classes Pro identified: state mismatch, authority leakage, rendered-front violations, jump-back failure, and unsafe grouping.

It still does not prove real-data product readiness. The next step after this sandbox is a real-data paired pilot only if the user approves it.
