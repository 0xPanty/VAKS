---
record_kind: source_annotation
status: captured
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: source_annotated
overlay_state: none
review_pressure: none
annotation_scope: source_local_anchor
annotation_id: claude-obsidian-provenance-ledger-separation
source_ref: raw/repos/2026-08-24-AgriciDaniel-claude-obsidian-source.md
working_copy_ref:
source_snapshot_ref: raw/repos/_snapshots/2026-08-24-AgriciDaniel-claude-obsidian-1c1bc49-source.zip
external_annotation_id:
selector_type: line_range
selector_value: "skills/wiki/references/provenance.md:14-49"
selector_exact: "## Ledgers"
selector_prefix:
selector_suffix:
selector_position: "skills/wiki/references/provenance.md:14-49"
source_hash: 1c1bc49c03a685ee8f5d09c99efe52b42d6673f5
content_hash: "sha256:31693b375bc3bab5ac5604566fdd9ad590daf47c49799c32741878f8fa9bcfeb"
anchor_status: exact_verified
anchor_checked_at: 2026-08-24
anchor_stale: false
anchor_match_count: 1
annotation_role: candidate_seed
body_note: "Pin the explicit separation of legacy manifest, source ledger and claim ledger, plus the stated freshness, independence and contradiction rules."
blocked_reason:
next_action: inspect_source_span
support_checked: false
evidence_support_status: not_checked
evidence_packet_ref:
candidate_refs:
  - outputs/review/2026-08-24-AgriciDaniel-claude-obsidian-candidate-distillation.md
project_overlay_refs:
  - outputs/review/project_overlays/2026-08-24-AgriciDaniel-claude-obsidian-vaks-transaction-and-evidence-overlay.md
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
  - provenance
  - claim-ledger
---

# Source Annotation：Provenance Ledger Separation

## Locator

    selector_value: skills/wiki/references/provenance.md:14-49
    anchor_status: exact_verified

## Why This Span Matters

上游把 ingestion manifest、source identity 与 claim assessment 分开，并公开 freshness、independence、accepted 和 contradiction 规则。可借的是分层与 lint 思路，不是 accepted 的权威语义。

## Boundary

这是上游合同说明，不是对任何具体 claim 的 evidence support。

