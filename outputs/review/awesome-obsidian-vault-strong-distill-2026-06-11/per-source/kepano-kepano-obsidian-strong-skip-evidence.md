---
record_kind: strong_existing_evidence_skip
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
source_family: awesome-obsidian-vault
source_url: "https://github.com/kepano/kepano-obsidian"
repo_key: "kepano/kepano-obsidian"
checked_commit: "473697347a0eaac790a6596229c741b3915f3b77"
checked_at: 2026-06-11
derived_from:
  - outputs/review/awesome-obsidian-vault-strong-distill-2026-06-11/source-anchor-manifests/kepano-kepano-obsidian-anchor-manifest.json
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: evidence_aware_review_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: high
borrow_order: P3
routing_hint:
  - evidence-backed-skip
  - already-absorbed
  - property-driven-workbench
fit_layer:
  - activation
  - maintenance
  - dev-context
  - risk-inhibition
not_fit_layer:
  - reviewed-knowledge
  - action-basis
  - truth-confidence
avoid:
  - "Do not re-distill from scratch unless upstream changed or local evidence is found stale."
  - "Do not treat link overlap, ratings, recency, or categories as reviewed truth."
  - "Do not promote existing Kepano-derived patterns without evidence-aware review."
dev_context_hint:
  default_layer: support
  core_only_when: "When modifying property-driven activation, Bases-style workbench views, or derived-relatedness boundaries."
  support_when: "When comparing public Obsidian vault templates already absorbed into VAKS."
  risk_when: "When organic links or metadata are being interpreted as truth/reviewed relations."
  cold_references:
    - raw/repos/2026-05-27-kepano-obsidian-source.md
    - wiki/summaries/2026-05-27-kepano-obsidian-architecture-review.md
    - wiki/patterns/property-driven-context-workbench.md
    - wiki/anti-patterns/derived-relatedness-as-truth-signal.md
tags:
  - candidate-only
  - strong-distillation
  - awesome-obsidian-vault
  - evidence-backed-skip
  - kepano
---

# Evidence-Backed Skip: kepano / kepano-obsidian

## Boundary

This entry is not skipped because it is unimportant. It is skipped because the
current VAKS repo already contains a source-level capture, architecture review,
absorbed patterns, an anti-pattern, and index references for the exact repo and
commit listed by the awesome-batch ledger.

This file records that skip decision so the batch remains auditable.

## Existing Local Evidence

| Local file | What it contains | Skip relevance |
|---|---|---|
| `raw/repos/2026-05-27-kepano-obsidian-source.md` | Source review for `kepano/kepano-obsidian`, including checked commit `473697347a0eaac790a6596229c741b3915f3b77`, source/vault map, templates, Bases, config, observations, limits, and candidate points. | Equivalent or stronger than a new per-source distillation. |
| `wiki/summaries/2026-05-27-kepano-obsidian-architecture-review.md` | Architecture review mapping Kepano to memory-tier/dev-context activation and warning against truth-layer misuse. | Existing synthesis already targets VAKS architecture. |
| `wiki/patterns/property-driven-context-workbench.md` | Pattern for using properties and views to surface context instead of moving files. | Already absorbed core borrow. |
| `wiki/patterns/link-overlap-related-context-surface.md` | Pattern for links/backlinks/tags as candidate relatedness. | Already extracted relatedness mechanism. |
| `wiki/patterns/random-revisit-cold-memory-maintenance.md` | Pattern for bounded revisit of cold notes. | Already extracted maintenance borrow. |
| `wiki/anti-patterns/derived-relatedness-as-truth-signal.md` | Anti-pattern warning that link overlap, backlinks, tags, ratings, and recency are not truth evidence. | Already protects the main risk. |
| `wiki/indexes/memory-tier-reference-index.md` and `wiki/indexes/knowledge-graph-index.md` | Index references to the source, review, extracted patterns, and anti-pattern. | Shows durable graph/index absorption. |

## Already Absorbed Borrow Points

1. **Property-driven context workbench.**  
   Use metadata and Bases-style views to surface activation context without
   moving files.

2. **Relatedness as candidate support only.**  
   Links, backlinks, tags, ratings, and recency can suggest adjacent context but
   cannot create reviewed relations or truth confidence.

3. **Random revisit / cold-memory maintenance.**  
   Old notes can be reactivated deliberately to find missing links or forgotten
   context, but not automatically promoted.

4. **Reusable property vocabulary.**  
   A small shared property set makes cross-category views practical.

## Why Not Re-Distill Now

The awesome-batch ledger points to the same checked commit already captured in
the local source record. Re-running a new source review would mostly duplicate
existing VAKS material and create parallel candidates with the same conclusions.

The correct batch action is to record an evidence-backed skip and route readers
to the existing source/review/pattern files.

## Anti-Borrow Reminder

- Organic links are not reviewed relations.
- Ratings are not confidence.
- Recency is not reliability.
- Category/dashboard views are activation surfaces, not truth authority.
- Personal vault style is not a universal VAKS schema.

## Fusion Judgment

Skip as already strongly absorbed. Keep the existing local evidence as the
canonical VAKS reference unless upstream changes or the prior review becomes
stale.
