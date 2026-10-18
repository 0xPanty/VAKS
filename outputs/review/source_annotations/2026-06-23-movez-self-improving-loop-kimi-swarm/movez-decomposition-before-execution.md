---
record_kind: source_annotation
annotation_id: movez-decomposition-before-execution
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
selector_type: line_range
selector_value: "pasted-text.txt:53-65"
selector_exact: "show proposed decomposition before running; inspect subagents, dependencies, step budget, risk, and wait for confirmation"
selector_prefix:
selector_suffix:
source_hash: C9588B16C148648E9C493EA39FF681F37986986544DF9F7E56919CE80E7C6659
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: candidate_seed
body_note: "This span anchors a useful pre-execution gate: inspect decomposition and quality risk before spending a large swarm run."
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
  - decomposition-gate
  - budget
---

# Source Annotation: Decomposition Before Execution

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:53-65
anchor_status: exact_verified
```

## Why This Span Matters

This span turns "run a swarm" into an inspectable preflight:

```text
how many sub-agents
what each handles
dependency order
estimated step budget
largest quality-drop risk
do not execute until confirmed
```

For VAKS/MISA, this is a candidate guard before any expensive or autonomous loop run.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

