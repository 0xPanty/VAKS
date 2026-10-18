---
record_kind: source_annotation
annotation_id: let-codebase-harness-legible-executable-verifiable
knowledge_status: candidate
processing_tier: medium
annotation_scope: source_local_anchor
source_ref: raw/repos/2026-06-23-AI-Builder-Club-loop-engineer-template-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
selector_type: line_range
selector_value: ".claude/skills/setup-codebase-harness/SKILL.md:13-24; .claude/skills/setup-codebase-harness/SKILL.md:35-51; .claude/skills/setup-codebase-harness/SKILL.md:55-72; .claude/skills/setup-codebase-harness/SKILL.md:85-90; .claude/skills/dev-local-setup/SKILL.md:13-21"
selector_exact: "make the repo legible, executable, and verifiable; map not manual; custom lints; dev-local; e2e; /pr"
selector_prefix:
selector_suffix:
source_hash: a2267355209713a2184eaeef3b276ec680219d2b
content_hash:
anchor_status: exact_verified
anchor_checked_at: 2026-06-23
anchor_stale: false
anchor_match_count:
annotation_role: candidate_seed
body_note: "This span is the strongest engineering-harness anchor: agent productivity depends on repo scaffolding, not just asking the model to try harder."
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
  - codebase-harness
  - agent-engineering
---

# Source Annotation: Legible, Executable, Verifiable Harness

## Locator

```yaml
source_snapshot_ref: raw/repos/_snapshots/2026-06-23-AI-Builder-Club-loop-engineer-template-a226735-source.zip
selector_type: line_range
selector_value: .claude/skills/setup-codebase-harness/SKILL.md:13-24; .claude/skills/setup-codebase-harness/SKILL.md:35-51; .claude/skills/setup-codebase-harness/SKILL.md:55-72; .claude/skills/setup-codebase-harness/SKILL.md:85-90; .claude/skills/dev-local-setup/SKILL.md:13-21
anchor_status: exact_verified
```

## Why This Span Matters

This span is the most practical borrow for VAKS/MISA engineering:

```text
legible:
  repo map, docs, golden rules as lints

executable:
  one-command local stack, reachable logs

verifiable:
  e2e gate, feature verifier, regression sweep
```

The reusable lesson:

```text
agent failures often indicate missing repo capabilities,
not merely a weak prompt.
```

## Boundary

This annotation is a locator and review input only.

It is not evidence support, reviewed knowledge, a Project Overlay verdict, or action basis.

