---
record_kind: source_annotation
annotation_id: movez-background-agent-after-stability
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
selector_type: line_range
selector_value: "pasted-text.txt:153-164"
selector_exact: "promote to background agent only once stable and skill-backed; run on trigger, apply constraints, verify, deliver output and diff, ping only above threshold"
selector_prefix:
selector_suffix:
source_hash: C9588B16C148648E9C493EA39FF681F37986986544DF9F7E56919CE80E7C6659
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: risk_signal
body_note: "This span anchors both the attractive background-agent pattern and its required order: only after loop stability and skill backing."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-06-23-movez-self-improving-loop-kimi-swarm-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_lens_overlays/2026-06-23-movez-self-improving-loop-kimi-swarm-vaks-loop-overlay.md
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
  - background-agent
  - trigger
---

# Source Annotation: Background Agent After Stability

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:153-164
anchor_status: exact_verified
```

## Why This Span Matters

This span is useful but high-risk:

```text
stable and skill-backed first
then schedule/file/URL trigger
apply constraints
verify
deliver output plus diff
alert only above threshold
```

For VAKS, this should be a future pilot shape, not ordinary intake behavior.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

