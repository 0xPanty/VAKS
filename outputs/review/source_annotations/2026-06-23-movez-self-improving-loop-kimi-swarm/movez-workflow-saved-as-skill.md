---
record_kind: source_annotation
annotation_id: movez-workflow-saved-as-skill
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
selector_type: line_range
selector_value: "pasted-text.txt:101-114"
selector_exact: "save workflow as reusable skill, including input format, agent steps, output format, naming, and validation rules"
selector_prefix:
selector_suffix:
source_hash: C9588B16C148648E9C493EA39FF681F37986986544DF9F7E56919CE80E7C6659
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: candidate_seed
body_note: "This span anchors the article's practical self-improvement definition: save the successful workflow as a reusable skill rather than claiming model weight learning."
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
  - skill-capture
  - self-improvement
---

# Source Annotation: Workflow Saved As Skill

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-06-23-movez-self-improving-loop-kimi-swarm-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:101-114
anchor_status: exact_verified
```

## Why This Span Matters

This span gives the article's definition of self-improvement:

```text
capture input format
capture agent steps that worked
capture output format and naming
capture validation rules
reuse same shape next time
```

For VAKS, this is a candidate pattern for loop skill capture, but only after the workflow is bounded and verified.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

