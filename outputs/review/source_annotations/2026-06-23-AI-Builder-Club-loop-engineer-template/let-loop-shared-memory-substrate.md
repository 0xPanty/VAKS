---
record_kind: source_annotation
annotation_id: let-loop-shared-memory-substrate
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/repos/2026-06-23-AI-Builder-Club-loop-engineer-template-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
selector_type: line_range
selector_value: "README.md:3-6; README.md:12-26; README.md:51-54; README.md:56-69"
selector_exact: "agent wakes on trigger, does work, writes shared file memory, then next run reads it; template includes knowledge base and codebase harness"
selector_prefix:
selector_suffix:
source_hash: a2267355209713a2184eaeef3b276ec680219d2b
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: candidate_seed
body_note: "This span captures the source's central loop-engineer claim: recurring triggered agents compound through shared file-based memory plus a codebase harness."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-06-23-AI-Builder-Club-loop-engineer-template-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_lens_overlays/2026-06-23-AI-Builder-Club-loop-engineer-template-vaks-loop-engineering-overlay.md
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
  - loop-engineer
  - shared-memory
---

# Source Annotation: Loop Shared Memory Substrate

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
selector_type: line_range
selector_value: README.md:3-6; README.md:12-26; README.md:51-54; README.md:56-69
anchor_status: exact_verified
```

## Why This Span Matters

This span defines the source's central loop-engineer operating model:

```text
triggered agent
-> work
-> verify
-> write shared file memory
-> next run reads memory
-> multiple loops compound through same folders
```

For VAKS, this is a candidate seed for future loop workspace and operator-memory design.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

