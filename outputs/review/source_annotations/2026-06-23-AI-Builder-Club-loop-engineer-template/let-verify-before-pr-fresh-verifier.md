---
record_kind: source_annotation
annotation_id: let-verify-before-pr-fresh-verifier
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/repos/2026-06-23-AI-Builder-Club-loop-engineer-template-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
selector_type: line_range
selector_value: ".claude/skills/pr/SKILL.md:11-24; .claude/skills/pr/SKILL.md:33-65; .claude/skills/pr/SKILL.md:67-89; .claude/workflows/ship-change.js:1-14; .claude/workflows/ship-change.js:216-253; .claude/workflows/ship-change.js:255-309"
selector_exact: "fresh verifier sub-agent drives real app before PR; objective checks after; ship-change workflow gates PR on verification"
selector_prefix:
selector_suffix:
source_hash: a2267355209713a2184eaeef3b276ec680219d2b
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: candidate_seed
body_note: "This span captures the source's anti-false-done pattern: feature proof by independent app-driving verifier, then objective regression checks, then PR only after verification."
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
  - verify-before-pr
  - verifier
---

# Source Annotation: Verify Before PR With Fresh Verifier

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
selector_type: line_range
selector_value: .claude/skills/pr/SKILL.md:11-24; .claude/skills/pr/SKILL.md:33-65; .claude/skills/pr/SKILL.md:67-89; .claude/workflows/ship-change.js:1-14; .claude/workflows/ship-change.js:216-253; .claude/workflows/ship-change.js:255-309
anchor_status: exact_verified
```

## Why This Span Matters

This span gives a strong anti-false-done shipping pattern:

```text
feature works? -> fresh verifier drives real app
regression safe? -> orchestrator runs objective checks
PR opened? -> only after proof and checks
```

For VAKS/MISA, this is useful as an engineering workflow pattern. It should not be promoted into a knowledge review or action-basis gate without a separate VAKS review process.

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

