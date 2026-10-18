---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: opus5-workload-shaped-model-routing
source_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source.md
working_copy_ref:
source_snapshot_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
external_annotation_id:
selector_type: line_range
selector_value: "pasted-text.txt:3-9"
selector_exact:
selector_prefix:
selector_suffix:
selector_position: "pasted-text.txt:3-9"
selector_timestamp_start:
selector_timestamp_end:
selector_page:
selector_rect:
source_hash: 63CCB9472E75A3D0CE099DD74A440C6816EEE8CEAADC9EDF3D89A0CF1406C73C
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-08-02
anchor_stale: false
anchor_match_count: 1
annotation_role: risk_signal
body_note: "The passage distinguishes repeated volume work from occasional high-depth work, but infers a VAKS default model from vendor positioning and a legal-domain evaluation without representative local task evidence."
blocked_reason:
next_action: compare_on_representative_vaks_tasks_before_routing
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-08-02-opus-5-obsidian-research-system-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_overlays/VAKS/VAKS-opus-5-obsidian-research-system-2026-08-02.md
source_digest_required: false
source_digest_ref:
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: review_input_only
  action_basis_allowed: false
  warning_code: annotation_not_support
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
tags:
  - source-annotation
  - model-routing
  - local-evaluation
  - risk-signal
---

# Source Annotation: Workload-Shaped Model Routing

## Locator

```yaml
source_snapshot_ref: raw/articles/2026-08-02-opus-5-obsidian-research-system-source/pasted-text.txt
selector_type: line_range
selector_value: pasted-text.txt:3-9
anchor_status: exact_verified
```

## Why This Span Matters

This span contains a useful routing hypothesis:

```text
repeated extraction / linking / digest work
!=
occasional high-risk deep synthesis
```

The reusable principle is workload-shaped evaluation. The model assignment in the article remains a candidate until representative VAKS tasks compare anchor coverage, omissions, contradiction quality, human corrections, cost, latency, and stability.

## Boundary

This annotation is a locator and review input only. It is not evidence that Opus 5 is the correct VAKS default, not a model-routing decision, and not action basis.

