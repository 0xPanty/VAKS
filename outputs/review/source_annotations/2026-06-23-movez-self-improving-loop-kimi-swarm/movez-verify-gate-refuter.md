---
record_kind: source_annotation
annotation_id: movez-verify-gate-refuter
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
selector_type: line_range
selector_value: "pasted-text.txt:95-99"
selector_exact: "the verify model's job is to refute and catch silent flaws before output becomes a skill"
selector_prefix:
selector_suffix:
source_hash: C9588B16C148648E9C493EA39FF681F37986986544DF9F7E56919CE80E7C6659
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: risk_signal
body_note: "This span anchors both a useful pattern and a risk: independent verifier as refuter is good, but verifier output is still review input rather than truth."
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
  - verify-gate
  - risk-signal
---

# Source Annotation: Verify Gate As Refuter

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:95-99
anchor_status: exact_verified
```

## Why This Span Matters

This span frames the verifier's role narrowly:

```text
catch under-cited claims
catch contradictions
refute rather than praise
stop flawed output from becoming a skill
```

For VAKS, the useful lesson is that verification should be adversarial. The boundary is that verifier output is still only review input.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

