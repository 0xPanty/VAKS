---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ponytail-benchmark-isolation-risk
source_ref: raw/repos/2026-08-23-DietrichGebert-ponytail-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "benchmarks/results/2026-06-18-agentic.md:40-47"
selector_exact: "A contamination bug we found in our own numbers"
selector_prefix:
selector_suffix:
selector_position: "benchmarks/results/2026-06-18-agentic.md:40-47"
source_hash: 2ed6c52c9d7e5e56942508591085fd45dea277d3
content_hash: "sha256:dde797c1678ac2c0589d74c8926f5069b905ae95af54b815d5dd60ce496da0ad"
anchor_status: exact_verified
anchor_checked_at: 2026-08-23
anchor_stale: false
anchor_match_count: 1
annotation_role: risk_signal
body_note: "The project's own SessionStart hook contaminated its baseline; future agent evaluations must isolate global instructions, plugins, hooks, state, and per-arm context."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-08-23-DietrichGebert-ponytail-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_overlays/2026-08-23-DietrichGebert-ponytail-vaks-minimalism-overlay.md
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
  - benchmark-isolation
  - contamination-risk
---

# Source Annotation：Always-On Hook Contaminated The Baseline

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
selector_type: line_range
selector_value: benchmarks/results/2026-06-18-agentic.md:40-47
anchor_status: exact_verified
```

## Why This Span Matters

这是本来源最强的负面经验：常驻 plugin 的 SessionStart hook 同时进入 baseline，导致实验对照失效。未来 VAKS agent / workflow eval 必须显式记录并隔离 instruction、plugin、hook、state 与 subagent 注入源。

## Boundary

这是 risk locator，不是对整个 benchmark 的独立审计，也不自动证明任何 VAKS 结论。

