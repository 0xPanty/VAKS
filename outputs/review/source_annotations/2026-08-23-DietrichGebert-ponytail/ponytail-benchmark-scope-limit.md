---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: medium
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: ponytail-benchmark-scope-limit
source_ref: raw/repos/2026-08-23-DietrichGebert-ponytail-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "benchmarks/results/2026-06-18-agentic.md:186-198"
selector_exact: "Limitations"
selector_prefix:
selector_suffix:
selector_position: "benchmarks/results/2026-06-18-agentic.md:186-198"
source_hash: 2ed6c52c9d7e5e56942508591085fd45dea277d3
content_hash: "sha256:dde797c1678ac2c0589d74c8926f5069b905ae95af54b815d5dd60ce496da0ad"
anchor_status: exact_verified
anchor_checked_at: 2026-08-23
anchor_stale: false
anchor_match_count: 1
annotation_role: scope_limit
body_note: "Pin the benchmark's own scope limits: one model, deterministic safety floor, n=4 nondeterminism, and timeout-affected cells."
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
  - benchmark-limitations
  - scope-limit
---

# Source Annotation：Benchmark Scope Limits

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-08-23-DietrichGebert-ponytail-2ed6c52-source.zip
selector_type: line_range
selector_value: benchmarks/results/2026-06-18-agentic.md:186-198
anchor_status: exact_verified
```

## Why This Span Matters

作者自己限定了结论范围：单一模型、deterministic safety 只是下限、样本小且有 nondeterminism，并存在 timeout-affected cells。因而 README 的 LOC / cost / safety 数字只能作为 source-authored benchmark diagnostics。

## Boundary

这是 scope-limit locator，不是 benchmark validation、security proof 或 action readiness。

