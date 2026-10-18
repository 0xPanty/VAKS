---
record_kind: source_annotation
annotation_id: movez-constraints-from-verifier-feedback
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
selector_type: line_range
selector_value: "pasted-text.txt:129-139"
selector_exact: "turn verifier feedback into project-level constraints; figures must trace to primary source, no silent conflict resolution, scope lock"
selector_prefix:
selector_suffix:
source_hash: C9588B16C148648E9C493EA39FF681F37986986544DF9F7E56919CE80E7C6659
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: implementation_note
body_note: "This span anchors a reusable loop-memory pattern: verifier feedback should become future-run constraints, while remaining separate from truth mutation."
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
  - constraints-file
  - verifier-feedback
---

# Source Annotation: Constraints From Verifier Feedback

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:129-139
anchor_status: exact_verified
```

## Why This Span Matters

This span shows how the loop "learns" from verifier feedback:

```text
distill the mistake
write it as a project-level constraint
load it at the start of future sessions
keep source tracing and conflict surfacing as permanent rules
scope-lock the run
```

For VAKS, the useful idea is constraints as operational memory. The risk is accidentally letting constraints mutate reviewed truth.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

