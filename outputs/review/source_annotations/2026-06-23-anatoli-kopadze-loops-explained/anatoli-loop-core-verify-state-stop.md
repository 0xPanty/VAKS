---
record_kind: source_annotation
annotation_id: anatoli-loop-core-verify-state-stop
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
selector_type: line_range
selector_value: "pasted-text.txt:28-40"
selector_exact: "loop runs discover/plan/execute/verify/iterate; verify, state, and stop condition are the real work"
selector_prefix:
selector_suffix:
source_hash: 939BDC7966CDACAF8B9EE33B7128287697C06B61DB502ACA7F891EA120509D6E
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: candidate_seed
body_note: "This span anchors the article's core loop anatomy: verify, state, and stop are what turn repetition into a sane loop."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-06-23-anatoli-kopadze-loops-explained-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_lens_overlays/2026-06-23-anatoli-kopadze-loops-explained-vaks-loop-overlay.md
source_digest_required: false
source_digest_ref:
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: annotation_not_support
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - source-annotation
  - verify-state-stop
  - loop-core
---

# Source Annotation: Loop Core Verify State Stop

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-06-23-anatoli-kopadze-loops-explained-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:28-40
anchor_status: exact_verified
```

## Why This Span Matters

This span gives the article's best loop definition:

```text
discover
plan
execute
verify
iterate
```

and its stronger constraint:

```text
verify
state
stop condition
```

For VAKS, this is a candidate seed for a minimal loop receipt.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

